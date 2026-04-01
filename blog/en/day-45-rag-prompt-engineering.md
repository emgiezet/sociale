---
day: 45
title: "There Is No Universal RAG Prompt"
pillar: Educator
language: en
image: ../../images/day-45.jpg
image_unsplash_query: "programming code text editor crafting writing precision"
---

# There Is No Universal RAG Prompt

I've seen the "ultimate RAG prompt" posted on social media. 47 lines. Works beautifully on a demo with 5 curated documents.

In production with 3,000 insurance policy documents across multiple product lines, in Polish, with users asking everything from simple fact lookups to cross-document coverage comparisons? It hallucinated on roughly 40% of queries.

The prompt wasn't bad. The problem was believing that one prompt could handle all retrieval scenarios with equal competence.

This post describes how I think about RAG prompt engineering as a system — not a single template, but a set of strategies matched to intent, retrieval quality, and context characteristics.

---

## Why a Single Prompt Fails at Scale

The intuition behind "one prompt to rule them all" is sound in theory: write clear instructions, give the model good context, get good answers. In demos, this works because demos use:
- High-quality, curated documents
- Questions specifically chosen to work well
- A small corpus where every query gets relevant retrieval

Production is different. Production means:
- Documents of varying quality, structure, and length
- Users asking questions you didn't anticipate
- Variable retrieval quality across the corpus (some topics well-covered, some barely covered)
- Multiple languages and register levels in the same index

A prompt that says "answer comprehensively using the context below" works fine when the context is excellent. When the context is mediocre (retrieval score 0.64), the same prompt produces a confident-sounding answer synthesized from marginally relevant text. That's a hallucination dressed as helpfulness.

The fix isn't a better single prompt. It's a system that selects the right prompt for the retrieval scenario.

---

## The Four Variables in RAG Prompt Engineering

Before I can select a prompt strategy, I need to characterize the query and context across four dimensions:

### Variable 1: User Intent Type

Different intents require fundamentally different answer behaviors:

**Fact retrieval** ("What is the liability coverage limit for passenger cars?"): The answer is a specific value that appears — or doesn't — in the retrieved context. Prompt must prioritize precision and verbatim quotation over synthesis. Length: short. Format: answer + exact quote + source.

**Comparison** ("How does plan A differ from plan B on X?"): Requires multi-source synthesis with explicit source attribution. If document A and document B conflict on the same point (which they do in insurance — same regulatory term, different company interpretation), the prompt must instruct the model to surface the conflict rather than reconcile it arbitrarily.

**Procedure** ("How do I file a third-party claim?"): Sequential steps, numbered format, no skipping. The answer is judged on completeness of the procedure, not on factual precision in the same sense as a coverage amount.

**Exclusion check** ("Is flood damage excluded?"): Binary answer (yes/no/unclear) with supporting quote. False negatives (saying "not excluded" when it is) are the most dangerous failure mode. Prompt must be calibrated to err toward "unclear" rather than "not excluded."

### Variable 2: Context Quality

I measure context quality through the retrieval quality score — the similarity score of the top-k chunks.

Three zones:
- **High confidence** (≥ 0.78): Context is highly relevant. Model can answer freely using the retrieved material.
- **Medium confidence** (0.62–0.78): Context is relevant but may not directly address the specific question. Model needs to be more cautious about inference.
- **Low confidence** (< 0.62): This should have been blocked by the retrieval gate. If it reaches the prompt stage, the prompt must be nearly fully defensive.

The retrieval quality score is the single most important input to prompt strategy selection.

### Variable 3: Language and Domain Register

Our insurance documents are in Polish. Polish legal-register text has structural characteristics that affect how prompts should instruct the model:

- Sentence structures are longer and more complex, with more embedded subclauses
- Technical terms often have no direct English equivalent and must be kept verbatim
- Regulatory references (to specific Polish insurance law articles) should not be paraphrased

A prompt instruction like "summarize concisely" applied to Polish insurance contract language tends to produce condensed paraphrases that lose regulatory precision. We learned this the hard way. The instruction became "preserve all numerical values, legal term names, and regulatory references verbatim."

English technical documentation is handled differently — the same summarization instructions that fail on Polish contracts work fine on English API documentation.

### Variable 4: Output Format

The same answer content needs different formatting depending on:
- Where it's displayed (broker portal UI → short; email draft → longer + context)
- Who reads it (broker checking a fact quickly → minimal formatting; end customer explanation → clear structure with headers)
- Downstream processing (human reader → natural language; structured data extraction → JSON)

---

## The Four Prompt Strategies

### Strategy 1: High-Confidence Direct Answer

**When to use**: Retrieval score ≥ 0.78, intent is fact retrieval or exclusion check.

**Core instruction logic**:
```
You are an insurance documentation assistant. Answer the following question 
using ONLY the information in the context below.

Rules:
- Quote the relevant policy text verbatim, placing it in "quotes"
- State the source document and section
- If the answer involves a specific number (amount, date, percentage), 
  include it exactly as it appears in the source
- Do not add information not present in the context

Question: {question}

Context:
{retrieved_chunks}
```

**What this prompt optimizes for**: Precision. Verbatim quotation. Source attribution. It doesn't try to be helpful beyond what the context contains.

**What it sacrifices**: Fluency. These answers can sound mechanical. That's fine for broker fact lookups — they want the number, not a friendly explanation.

### Strategy 2: Low-Confidence Cautious Answer

**When to use**: Retrieval score 0.62–0.78, or any intent where the retrieval gate passed but confidence is marginal.

**Core instruction logic**:
```
You are an insurance documentation assistant. The context below may or may not 
directly answer the question.

Rules:
- Answer ONLY if the context contains a direct, unambiguous answer
- If the context only partially addresses the question, say: 
  "The available documentation partially addresses this: [what you found]. 
   For a complete answer, please consult [escalation path]."
- If the context does not directly address the question, say:
  "The available documentation does not contain a direct answer to this question."
- Do NOT infer, extrapolate, or reason beyond what is explicitly stated

Question: {question}

Context:
{retrieved_chunks}
```

**What this prompt optimizes for**: Avoiding hallucination when retrieval is weak. It explicitly breaks the model's default "be helpful" drive and replaces it with "be honest about uncertainty."

**The key instruction**: "Do NOT infer or extrapolate." LLMs are trained to be helpful by filling gaps with inference. In insurance, inference from a marginally relevant clause to a coverage conclusion is exactly the hallucination pattern we're preventing.

### Strategy 3: Multi-Source Synthesis

**When to use**: Retrieval score ≥ 0.78, intent is comparison or multi-document synthesis.

**Core instruction logic**:
```
You are an insurance documentation assistant comparing information across 
multiple source documents. The context below contains chunks from {n} documents.

Rules:
- Attribute every factual claim to its source document: "[Source: Document X, Section Y]"
- If two documents contain conflicting information on the same point, 
  explicitly flag this: "Note: Documents X and Y differ on this point: [details]"
- Do not synthesize conflicting information into a single answer — preserve 
  the conflict for the user to resolve
- Structure your answer with clear headers for each document/dimension being compared

Question: {question}

Context:
{retrieved_chunks_with_source_labels}
```

**The critical rule**: Do not reconcile conflicts. This is counterintuitive — we usually want synthesized answers. But in insurance, if Policy A says "flood damage excluded" and Policy B says "flood damage covered with conditions," the correct answer is to surface both, not to average them.

**What it sacrifices**: Conciseness. Multi-source synthesis answers are long. That's appropriate for the use case (brokers doing product comparison research).

### Strategy 4: Refusal Prompt

**When to use**: Retrieval gate blocked (score < 0.62), intent classified as out-of-scope, or explicit refusal required.

**Core instruction logic**:
```
The available documentation does not contain sufficient information to answer 
this question reliably.

Please [escalation path based on query type]:
- For coverage questions: consult the full policy document at [link]
- For claims questions: contact the claims team at [contact]
- For product advice: speak with your broker specialist

Reference ID: {query_id} (for support reference)
```

**Note**: This isn't a prompt sent to the LLM. It's a canned response returned directly by the pipeline when the refusal condition is met. No LLM invocation, no generation cost, no hallucination risk.

Why not just let the LLM say "I don't know"? Because "I don't know" in LLM output is inconsistently phrased, sometimes padded with hedging that still sounds like partial information, and occasionally overridden by the model's training to be helpful. A canned refusal is deterministic, controlled, and auditable.

---

## Dynamic Prompt Selection: The Routing Logic

The prompt selection system works like this:

```python
def select_prompt_strategy(
    intent: QueryIntent,
    retrieval_score: float,
    source_count: int,
    language: str
) -> PromptStrategy:
    
    # Out-of-scope or below minimum threshold: always refusal
    if intent == QueryIntent.OUT_OF_SCOPE:
        return PromptStrategy.REFUSAL
    if retrieval_score < 0.62:
        return PromptStrategy.REFUSAL
    
    # Multi-source: synthesis strategy
    if intent == QueryIntent.COMPARISON and source_count > 1:
        return PromptStrategy.MULTI_SOURCE_SYNTHESIS
    
    # High-confidence: direct answer
    if retrieval_score >= 0.78:
        return PromptStrategy.HIGH_CONFIDENCE_DIRECT
    
    # Medium confidence: cautious
    return PromptStrategy.LOW_CONFIDENCE_CAUTIOUS


def build_prompt(
    strategy: PromptStrategy,
    question: str,
    chunks: list[ScoredChunk],
    language: str,
    output_format: OutputFormat
) -> str:
    template = PROMPT_TEMPLATES[strategy][language]
    return template.format(
        question=question,
        retrieved_chunks=format_chunks(chunks, strategy),
        output_instructions=OUTPUT_FORMAT_INSTRUCTIONS[output_format]
    )
```

The routing logic is simple. The complexity lives in the prompt templates themselves, which are maintained per-language and per-strategy — 4 strategies × 2 languages = 8 base templates, with output format variations on top.

---

## Anti-Patterns I've Observed and Fixed

### Anti-pattern 1: The Overlong System Prompt

The 47-line prompt I referenced at the start contained instructions that contradicted each other:
- "Be concise" and "provide full context for your answer"
- "Always cite sources" and "keep the answer readable"
- "Refuse if uncertain" and "do your best to help"

LLMs resolve contradictions inconsistently — different choices on different runs. The result is answer variance that's hard to debug because the variance isn't in retrieval, it's in the prompt interpretation.

Fix: One primary instruction per prompt. No more than three supporting constraints. Contradictions in the prompt translate directly to inconsistency in production.

### Anti-pattern 2: Prompt Stuffing

"Chain of thought, few-shot examples, persona definition, output format, content guidelines, safety instructions, language instructions, citation format, fallback instructions — all in one prompt."

Each addition is individually reasonable. Combined, they compete for the model's attention and increase the probability of instruction-following failures on any one dimension.

Fix: Few-shot examples live in the template system, not the system prompt. Persona is kept to one sentence. Safety instructions are handled at the architecture layer (guardrails), not the prompt layer.

### Anti-pattern 3: Prompting for Courage Instead of Calibration

"Answer even if uncertain. Do your best. The user is counting on you."

This is encouraging hallucination. "Do your best" with weak retrieval means confident synthesis of weakly relevant context. In insurance, that's a coverage misrepresentation.

Fix: Replace motivational language with behavioral constraints. "Answer only if context directly supports it" is more reliable than "be helpful but be honest."

### Anti-pattern 4: Ignoring Retrieval Quality in Prompt Design

Treating all queries the same regardless of retrieval score. The same prompt for a 0.87-score retrieval and a 0.65-score retrieval.

Fix: Retrieval score is an input to the prompt selection system, not just a logging field.

---

## Production Metrics for Prompt Strategy Effectiveness

I track prompt-level performance in production:

- **Per-strategy precision** on the canary test set: is Strategy 1 (direct) maintaining ≥ 0.95?
- **Refusal rate per strategy**: is Strategy 2 (cautious) refusing too much? Too little?
- **User feedback by strategy**: thumbs-down rates correlated by which prompt strategy was used
- **Escalation triggers**: how often does each strategy route to human review?

When the cautious strategy started generating refusals at 22% (up from 14% baseline), investigation showed a corpus update had introduced new document formats with shorter, less context-rich chunks — causing more queries to fall into the medium-confidence zone. The fix was re-tuning chunk size for the new document format, not changing the prompt.

---

## Summary

The universal RAG prompt fails because it assumes a uniform retrieval quality and uniform answer requirements. Production is neither.

Prompt strategy in RAG should be a function of:
1. User intent type (what kind of answer is needed?)
2. Retrieval quality score (how confident can we be in the context?)
3. Domain and language (what does "cite accurately" mean for this corpus?)
4. Output format (who reads this, and where?)

Four strategies cover the space: high-confidence direct, low-confidence cautious, multi-source synthesis, and canned refusal. Dynamic routing selects among them based on retrieval score and intent.

The 47-line universal prompt doesn't fail because it's long. It fails because it tries to be all four strategies simultaneously.
