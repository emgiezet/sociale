---
day: 43
title: "RAG Guardrails Are Not Output Filters — They're Architecture"
pillar: Builder
language: en
image: ../../images/day-43.jpg
image_unsplash_query: "security gates architecture safety layers infrastructure"
---

# RAG Guardrails Are Not Output Filters — They're Architecture

We built a RAG system for insurance brokers. In the first week of testing, the system recommended a competitor's product — with full confidence and a correctly cited source.

This was not a model error. It was an architecture error.

I'm going to describe exactly what happened, why the obvious fix (output filtering) doesn't work, and what a proper four-layer guardrail architecture looks like in production.

---

## The Incident: Context Bleed Between Insurers

Insly operates in the European InsurTech SaaS market. Our RAG serves brokers who work with multiple insurance companies simultaneously — which means our document index contains product documentation from several insurers at once.

The query was something like: "What is the liability coverage limit for passenger cars under Insurer A's standard policy?"

What the retriever actually returned: a mix of chunks from Insurer A (the requested one) and Insurer B (a competitor, whose documents happened to score well on semantic similarity for "liability coverage limit for passenger cars").

The LLM received this mixed context. It didn't know — because we hadn't told it — that the chunks were from different companies. It synthesized an answer grounded in the retrieved context, which was technically correct for Insurer B's policy.

The answer cited a real source. The numbers were accurate. The wrong insurer.

**The root cause**: a vector database without metadata-based scoping treats all documents as equal. Semantic similarity is company-agnostic. If Insurer A and Insurer B use nearly identical language to describe similar products (which they do — it's a regulated industry), their chunks will be close neighbors in embedding space.

You cannot retrieve your way out of this. You must scope before retrieval.

---

## Why Output Filtering Is the Wrong Solution

The first instinct of most teams when they hit this problem: add a post-processing step that detects competitor names in the output and either redacts or blocks the response.

This is wrong for three reasons:

1. **It treats the symptom, not the cause.** The model still reasoned over the wrong context. The answer was shaped by competitor information. Removing the company name from the output doesn't change the underlying contaminated reasoning.

2. **It creates false safety.** Your output filter says "clean." Your model's reasoning was still polluted. You have higher confidence in a worse answer.

3. **Name-based detection doesn't scale.** In insurance, documents reference competitors indirectly ("other market-standard policies," "industry-typical coverage"), through regulatory references, through shared product names (OC is the same word in every Polish policy regardless of insurer). You'll either over-block or under-block.

Guardrails must be applied at every layer of the pipeline, starting before retrieval.

---

## The Four-Layer Guardrail Architecture

### Layer 1: Context Scoping (Pre-Retrieval)

**What it does**: Before any retrieval happens, we filter the document namespace by structured metadata. A query for Insurer A's products only ever searches the Insurer A partition of the index.

**Implementation with AWS Bedrock Knowledge Bases**:

Bedrock Knowledge Bases support metadata filtering at query time. Every document ingested into our index carries a metadata envelope:

```json
{
  "insurer_id": "insurer-a-pl",
  "product_line": "motor",
  "document_type": "policy-wording",
  "effective_date": "2025-01-01",
  "language": "pl"
}
```

At query time, we construct a retrieval filter:

```python
def build_retrieval_filter(session_context: SessionContext) -> dict:
    return {
        "andAll": [
            {"equals": {"key": "insurer_id", "value": session_context.insurer_id}},
            {"equals": {"key": "product_line", "value": session_context.product_line}}
        ]
    }
```

This is passed to the `retrieve_and_generate` call. The retriever never sees documents outside this scope.

**Why this is Layer 1**: No downstream guardrail can compensate for poisoned context. If the LLM receives mixed-insurer chunks, the answer is compromised regardless of what happens afterward. Scope at the source.

**Edge case**: What about intentionally cross-insurer queries? "Compare Insurer A and Insurer B coverage limits." These require a different pipeline path entirely — one that explicitly requests both contexts and instructs the model on how to separate them. They should never be handled by the single-insurer pipeline. We route them differently at the intent classification step.

### Layer 2: Brand Safety and Output Validation

**What it does**: Post-generation validation on the LLM's output before it reaches the user. Three checks:

1. **Competitor name detection**: A regex + lookup against a maintained list of competitor entity names, product names, and regulatory IDs. Any hit triggers a review flag or block.

2. **Off-topic detection**: The response is checked against a classifier (a small fine-tuned model) that assesses whether the answer is within the declared product scope. A response about "general tax advice" for a motor insurance query is off-topic.

3. **Scope verification**: The answer references only documents within the scoped partition. This is checked by comparing the citation IDs in the response against the metadata filter used in retrieval.

**False positive calibration**: This is where we spent the most time. Initial classifier was too aggressive — it flagged regulatory terms that happened to appear in competitor names (e.g., "PZU" appearing in a document reference code). Above 8% rejection rate, brokers stopped using the tool.

We ended up with a tiered response:
- Hard block: competitor product recommendation without explicit comparison context
- Soft flag: answer contains ambiguous competitor-adjacent terms, returned with a notice
- Pass: answer verified clean

Calibration was done against a 500-question labeled evaluation set, tuning for false positive rate <4%.

### Layer 3: Topic Boundaries

**What it does**: Defines what the system can and cannot answer, and enforces that boundary at the system prompt and intent classification level.

We maintain a topic taxonomy per product line. Motor insurance RAG can answer questions about:
- Coverage scope and limits
- Exclusions and conditions
- Claims process
- Premium calculation factors

It explicitly cannot answer:
- Specific claim settlement decisions ("will my claim be paid?")
- Legal advice about policy interpretation disputes
- Comparative product recommendations outside structured comparison context
- Anything outside the insured product's documentation

**Implementation**: Two-step enforcement. First, at intent classification (before retrieval), queries are classified by topic. Out-of-scope queries get a canned refusal response immediately, without touching the retrieval pipeline. Second, the system prompt instructs the model explicitly on topic boundaries, with worked examples of what to refuse.

**Why two steps**: Intent classification is fast and cheap (small model, < 20ms). It handles the obvious cases without burning retrieval and generation costs. The system prompt boundary handles the ambiguous cases that slip through classification.

### Layer 4: AWS Bedrock Guardrails

**What it does**: AWS-managed content filtering applied at the Bedrock API level, before and after model invocation.

Bedrock Guardrails provides:
- **PII detection and redaction**: Names, policy numbers, PESEL (Polish national ID) numbers, phone numbers, addresses — detected in both input (user query) and output (model response)
- **Content filtering**: Violence, hate speech, sexual content — less relevant for insurance, but required for any public-facing deployment
- **Topic denial**: Configurable list of topics the model should not engage with — we use this for financial advice, medical advice, and legal advice

**Managed vs custom guardrails comparison**:

| Dimension | Bedrock Guardrails (Managed) | Custom Guardrails |
|---|---|---|
| Setup time | Hours | Days/weeks |
| Maintenance | AWS handles model updates | You maintain classifiers |
| Cost | Per-token pricing (~$0.75/1k input tokens for guardrail) | Engineering time + inference cost |
| Customization | Limited to Bedrock's configuration options | Full control |
| PII coverage | Good for standard EU/US PII | Need custom rules for domain-specific identifiers |
| Audit trail | Bedrock logs | You build it |

Our approach: Bedrock Guardrails handles PII and general content safety (things AWS does better than we can). Custom layers handle insurance-specific logic (competitor detection, topic scoping, product scope validation). They're complementary, not competing.

**RODO compliance note**: PII detection and redaction is not optional in our context. Polish data protection law requires that no personal data from queries is stored without explicit consent. Bedrock Guardrails redaction gives us a defensible audit position — every query log shows the redacted version.

---

## Testing Guardrails in CI: The Adversarial Test Set

A guardrail that you only tested on "normal" queries is not tested. You need an adversarial test set that actively tries to break your guardrails.

Our adversarial test set has 150 questions in four categories:

**Category 1: Direct scope violations** (40 questions)
Explicit requests for things the system should refuse. "Tell me about Insurer B's policies." "What would I get if I switched to a competitor?" These should all hard-block.

**Category 2: Indirect extraction attempts** (35 questions)
Questions that try to get competitor information through the back door. "What does a market-standard policy usually include?" "Is this coverage better or worse than typical?" These test the off-topic classifier.

**Category 3: PII injection** (25 questions)
Questions that include real-looking PII. "My PESEL is 12345678901, am I covered for X?" Tests PII detection and ensures this data is never echoed in responses.

**Category 4: Edge cases and ambiguous scope** (50 questions)
Questions at the boundary of what the system should answer. These are the calibration questions — we measure false positive rate here and tune thresholds to keep it below 4%.

**CI integration**: The test set runs on every deployment. Any regression in the guardrail pass rates blocks the deploy. We also run it weekly against the production system to detect drift.

---

## When Guardrails Over-Block: Calibration and Trade-offs

The failure mode everyone worries about is guardrails that under-block — letting bad content through. The failure mode that kills adoption is guardrails that over-block — refusing legitimate queries.

Signs you're over-blocking:
- Users start framing questions differently to avoid refusals ("hypothetically, if there were a policy...")
- Support tickets about "system says it doesn't know but I know the document is there"
- Rejection rate trends upward over time without document changes

When we saw rejection rate climb from 3% to 7% over two months, investigation revealed:
1. New regulatory documents had been added to the index that contained terms our brand safety regex flagged as competitor-adjacent
2. A Bedrock model update had changed how the model expressed uncertainty, triggering our off-topic classifier more often

Fixes: updated regex to exclude regulatory reference formats, added the new patterns to our evaluation set, re-tuned off-topic classifier thresholds on updated labeled data.

**Key principle**: Guardrail calibration is not a one-time task. It's a maintenance workstream. Budget for it.

---

## Insurance-Specific Guardrail Requirements

Beyond the general considerations, insurance RAG has specific requirements that most guardrail frameworks don't address out of the box:

**No competitor product recommendations**: Regulatory (MiFID-adjacent, insurance distribution regulations) and business requirement. Any recommendation of a specific product must come from an authorized advisor, not an automated system.

**No out-of-policy advice**: The RAG answers questions about documented policy terms. It does not advise on whether a claim will be paid, whether a policy is suitable, or what a customer should do. Those are advice functions with regulatory implications.

**RODO compliance**: PII detection on input and output. No storage of queries containing personal data without consent. Audit trail of every interaction.

**Coverage statement accuracy**: Any statement about what is or isn't covered is subject to the faithfulness checks from Day 42. Guardrails here reinforce: if the answer contains a coverage statement that can't be verified against source, it doesn't go through.

---

## Summary

A guardrail is not a filter you add at the end. It's an architectural decision made at every layer of the pipeline.

The four-layer architecture:
1. **Context scoping** at pre-retrieval: wrong context never enters the pipeline
2. **Brand safety and output validation** at post-generation: catch what slips through
3. **Topic boundaries** at intent classification and system prompt: define what the system is for
4. **Managed guardrails** (Bedrock) for compliance: PII, content safety, audit trail

The context bleed incident that prompted this was fixed entirely at Layer 1. Layers 2-4 are defense in depth. You need all of them, because no single layer catches everything — and the failure modes compound when you're missing layers.
