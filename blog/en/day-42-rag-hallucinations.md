---
day: 42
title: "RAG Doesn't Eliminate Hallucinations — It Changes Their Character"
pillar: Educator
language: en
image: ../../images/day-42.jpg
image_unsplash_query: "AI safety checkpoint inspection quality control"
---

# RAG Doesn't Eliminate Hallucinations — It Changes Their Character

There is a belief, widely repeated in AI demos and vendor pitches, that Retrieval-Augmented Generation solves the hallucination problem. The model no longer invents — it reads from your documents and answers from there. Case closed.

I've built three RAG systems in production, two of which taught me expensive lessons. The belief is wrong, and it's dangerously wrong in a specific way: RAG doesn't eliminate hallucinations, it makes them harder to spot.

A hallucinating RAG model answers confidently, cites a source, and gets the answer subtly wrong. In insurance, where I work, "subtly wrong" can mean quoting the wrong deductible amount, mischaracterizing a coverage exclusion, or blending two policies into a fictional third. Every one of those errors has legal and financial consequences.

This post is about how I built a five-checkpoint anti-hallucination pipeline, what each checkpoint costs, and where the line is between "cautious system" and "system that refuses to answer anything useful."

---

## Why RAG Changes (But Doesn't Fix) Hallucinations

A classic LLM hallucinating is relatively easy to detect: it invents entities, fabricates citations, produces facts with no grounding. The signal is absence — there's no real source backing the claim.

A RAG system hallucinating is harder. The model has retrieved real documents. It has real context. The failure happens at the synthesis layer:

- **Loose paraphrase**: the model summarizes a passage but drifts from its precise meaning. "Coverage applies to accidental damage" becomes "coverage applies to all damage."
- **Cross-document blending**: two chunks from different policies get merged. Neither chunk alone is wrong, but the combined answer is a fiction.
- **Extrapolation from similar cases**: the retrieved document doesn't directly answer the question, but the model infers from a similar case — without flagging this is inference, not retrieval.
- **Confidence about low-confidence retrieval**: the retriever returns a weakly relevant chunk (score 0.61), but the LLM treats it as if it were authoritative.

The common thread: the model acts with confidence it hasn't earned. The hallucination is dressed in the authority of citation.

---

## The Five-Checkpoint Pipeline

I built this pipeline iteratively over about eight months of production operation on insurance document RAG. Each checkpoint was added in response to a real failure mode, not theoretical caution.

### Checkpoint 1: Retrieval Precision Gate

**What it does**: Before the retrieved context reaches the LLM, I evaluate the relevance scores of the top-k chunks. If the best chunk falls below a threshold, the pipeline refuses to proceed.

**Our threshold**: 0.72 cosine similarity on embeddings from Amazon Titan Embed v2. This value was calibrated by hand-labeling 500 queries as "retrievable" or "not retrievable" and finding the cutoff that gave <5% false positives (bad context passing through).

**Implementation**:
```python
def retrieval_gate(chunks: list[ScoredChunk], threshold: float = 0.72) -> bool:
    if not chunks:
        return False
    top_score = chunks[0].score
    if top_score < threshold:
        logger.info(f"Retrieval gate blocked: top score {top_score:.3f} < {threshold}")
        return False
    return True
```

**What it catches**: "I know nothing about this topic" queries that somehow return low-relevance chunks. Forces the system to say "I don't have information on that" rather than generating an answer from irrelevant context.

**Cost**: Essentially free — the scores come from the retrieval step anyway.

### Checkpoint 2: LLM-as-Judge Faithfulness Check

**What it does**: A separate, smaller LLM (Claude Haiku in our case) evaluates whether the generated answer is grounded in the provided context. It receives the question, the retrieved chunks, and the draft answer, and returns a verdict: faithful, partially faithful, or unfaithful.

**Prompt skeleton**:
```
You are a faithfulness evaluator. Given the user question, the retrieved context, 
and the assistant's answer, assess whether every factual claim in the answer 
is directly supported by the context.

Return JSON: {"verdict": "faithful|partial|unfaithful", "reason": "..."}

Do not penalize the answer for being incomplete. Penalize it only for containing 
claims not present in or inferable from the context.
```

**Our thresholds**: `faithful` → proceed; `partial` → log and flag for review, still return answer with disclaimer; `unfaithful` → block, return "I cannot confirm this from available documents."

**Latency**: ~150ms average for a 500-token context. Acceptable for our use case (async document queries, not real-time chat).

**Cost (estimate)**: ~$0.0003 per call at Haiku pricing. At 5,000 queries/day, that's ~$45/month — cheap insurance.

**What it catches**: The most common failure mode — the model rephrasing context in a way that subtly changes meaning. "Deductible applies after the third claim" paraphrased as "deductible applies from the third claim."

### Checkpoint 3: Source-Answer Alignment

**What it does**: Extracts key numerical and named entities from the generated answer, then checks whether those specific values appear in the cited source chunks.

This is deliberately simple — not an NLP pipeline, just structured extraction and lookup.

**Implementation sketch**:
```python
def source_alignment_check(answer: str, chunks: list[ScoredChunk]) -> AlignmentResult:
    # Extract numbers and named insurance terms from answer
    extracted = extract_key_terms(answer)  # regex + small lookup table
    
    chunk_text = " ".join(c.text for c in chunks)
    
    missing = []
    for term in extracted.numbers + extracted.named_terms:
        if term not in chunk_text:
            missing.append(term)
    
    if missing:
        return AlignmentResult(aligned=False, missing_terms=missing)
    return AlignmentResult(aligned=True)
```

**What it catches**: The specific hallucination that worries me most in insurance — fabricated or misquoted numbers. A model generating "PLN 2,000 deductible" when the source says "PLN 1,500" will fail this check.

**Limitation**: It won't catch hallucinated qualitative statements that use no unique terms. Checkpoint 2 handles those.

### Checkpoint 4: Confidence Scoring

**What it does**: The generating LLM reports its own confidence as a structured output field alongside the answer.

I'm under no illusion that LLM self-reported confidence is calibrated. It isn't. But it is a useful signal for:
1. Routing low-confidence answers to a human review queue
2. Logging for drift analysis over time

**Implementation**: System prompt includes: "After your answer, output a confidence score 1-5 where 1 = educated guess, 5 = directly and completely addressed by context."

Answers with score ≤ 2 get a UI flag ("This answer may be incomplete") and enter a review queue.

**What it does NOT do**: It does not replace checkpoints 1-3. It's a supplementary signal, not a gate.

### Checkpoint 5: Canary Test Set

**What it does**: A maintained set of ~80 questions with known correct answers, run on every deployment and every night in production. Precision on this set must stay above 0.90 or I get paged.

This is continuous regression testing for hallucination quality.

**Test set composition**:
- 30 factual questions about specific policy terms (amounts, dates, exclusions)
- 20 comparison questions across multiple documents
- 15 edge cases (ambiguous coverage, overlapping policies)
- 15 "should refuse" questions — topics not covered in the document set

**Why the canary catches what others miss**: The canary operates at the system level, including model updates, embedding model changes, and chunk strategy changes. A Bedrock model update in October 2025 shifted our semantic similarity scores by ~0.04 on average — barely noticeable per-query, but the canary test caught a 6-point precision drop overnight and I had time to re-calibrate before users noticed.

---

## A Real Incident: The Hallucination That Passed Four Checkpoints

A query about coverage limits for a third-party liability claim on a commercial vehicle policy. The model returned:

> "Based on policy document X, section 4.2, the coverage limit for third-party liability is PLN 500,000."

Result from each checkpoint:
1. Retrieval gate: PASS (top chunk score 0.81)
2. LLM faithfulness: PASS (the number appeared in context)
3. Source alignment: PASS (PLN 500,000 appeared in a chunk)
4. Confidence: PASS (model rated itself 4/5)

The problem: section 4.2 of the cited document described a *different* vehicle class. The 500,000 figure was real, but it applied to private vehicles, not commercial. The answer was technically present in the retrieved text — but the LLM had dropped the qualifying condition.

Checkpoint 5, the canary, caught a similar question in the regression set three days after a prompt template update. The test expected "coverage for commercial vehicles: PLN 1,200,000" and got "PLN 500,000." Precision dropped to 0.87, below threshold. I traced it to a prompt change that had inadvertently removed instruction to preserve vehicle class context.

Lesson: checkpoints 1-4 operate on the individual response. Only checkpoint 5 catches systemic regressions that affect a class of questions.

---

## Red Lines in Insurance

There are three categories where any hallucination — no matter how small — is a hard block:

1. **Monetary amounts**: deductibles, coverage limits, premiums. Any discrepancy blocks the answer.
2. **Coverage scope**: what is and isn't covered. Overstating coverage is a legal liability risk.
3. **Exclusions**: what invalidates a claim. Missing an exclusion is potentially fraudulent misrepresentation.

For these categories, I run stricter thresholds: retrieval gate at 0.80 (vs 0.72 default), faithfulness check requires "faithful" verdict (not "partial"), and source alignment requires exact numeric match.

---

## Monitoring Hallucination Drift Over Time

Hallucination rates are not static. They drift as:
- Documents in the index get updated (coverage terms change yearly in insurance)
- Underlying LLM models get updated by the provider
- Query distribution shifts (users find new ways to ask)

I track three metrics in production dashboards:

1. **Canary precision**: checked nightly, alerts on 3-point drop from 30-day baseline
2. **Faithfulness check failure rate**: ratio of "unfaithful" verdicts over rolling 7 days
3. **Retrieval gate rejection rate**: how often the system refuses due to low retrieval quality (sudden spikes indicate document index issues)

These three numbers tell me if the system is getting worse before users do.

---

## Costs and Trade-offs

| Checkpoint | Latency added | Cost per 1k queries | What it catches |
|---|---|---|---|
| Retrieval gate | ~0ms | ~$0 | Low-quality context |
| LLM-as-judge | ~150ms | ~$0.30 | Unfaithful synthesis |
| Source alignment | ~10ms | ~$0 | Numeric/term hallucinations |
| Confidence scoring | ~0ms (in-prompt) | ~$0 | Routing signal |
| Canary test set | Async, no user latency | ~$2/run | Systemic regression |

Total: ~$0.30/1k queries for the faithfulness check, near-zero for everything else. For 5,000 queries/day, the full pipeline costs roughly $45/month. For a system making decisions about insurance coverage, that is not a hard trade-off.

---

## Summary

RAG doesn't eliminate hallucinations. It changes them from "invented facts" to "misquoted sources" — which are harder to catch and more dangerous in regulated domains.

The five-checkpoint pipeline I described catches different failure modes at different layers:
- Gate at retrieval quality
- Verify faithfulness at synthesis
- Check source alignment for key terms
- Track confidence as a routing signal
- Run canaries to catch systemic drift

No single checkpoint is sufficient. Together, they've reduced our hallucination rate from ~12% (single-pass RAG) to ~1.8% over 6 months of production data — on a domain where the other 1.8% still keeps me up at night.
