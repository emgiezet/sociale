---
day: 37
title: "RAG LLM Selection: How to Choose the Right Model for Your Data (Not Just Your Benchmarks)"
pillar: Educator
language: en
image: ../../images/day-37.jpg
image_unsplash_query: "comparison chart decision making technology models"
---

# RAG LLM Selection: How to Choose the Right Model for Your Data (Not Just Your Benchmarks)

When we started building RAG systems at Insly — a European InsurTech SaaS with 150,000+ users — our LLM selection process looked like most teams': check the leaderboard, sort by MMLU or HELM, shortlist the top performers, and run a quick demo. GPT-4o came out on top. Decision made.

Three months later we started asking the right questions.

Not "which model is globally best?" — but "which model is best on our data, in our language, at our query volume, within our compliance constraints?" That shift sounds obvious in hindsight. But it changes every decision you make downstream.

This post is the comparison I wish I'd had before we started.

## Why Benchmarks Lie to You

MMLU, HellaSwag, HumanEval, MATH — these are good benchmarks. They measure real things. What they don't measure is how a model handles a paragraph from a Polish insurance policy written in 2009, extracted imperfectly from a decade-old Word file, after being chunked by a tokenizer that didn't account for Polish compound nouns.

The domain gap between benchmark conditions and production conditions is enormous. And the language gap is even larger if your documents aren't in English.

We build systems that process insurance documents across multiple European markets. A model that scores 85% on MMLU but produces fluent hallucinations when reasoning about subrogation clauses in Polish is not a good model for our use case.

The only benchmark that matters is your own evaluation set.

## The Four Models We Evaluated

I ran a structured comparison on a test set of 80 real insurance queries — questions our users actually ask, with ground-truth answers drawn from our policy documents. Here's what I found.

### Claude Sonnet 3.5 / Claude Sonnet (via AWS Bedrock)

**Pricing:** ~$3/1M input tokens, ~$15/1M output tokens (published Bedrock pricing)

**Context window:** 200k tokens

**p95 latency:** ~2.1s for typical RAG responses (~300 token output)

**Polish language support:** Good. Not perfect — occasional awkward phrasing on very formal legal text — but consistently understood context and produced coherent Polish output.

**Compliance story:** Native AWS deployment. Data stays in your VPC. For European insurance clients, this simplifies the GDPR conversation considerably. This was a meaningful differentiator for us.

**Our evaluation:** Faithfulness score 0.87, answer relevance 0.84. Slightly below GPT-4o on raw quality, but the compliance and pricing combination made it our primary choice for the AWS Bedrock-based pipeline.

### GPT-4o (OpenAI API)

**Pricing:** ~$5/1M input tokens, ~$15/1M output tokens (OpenAI published pricing)

**Context window:** 128k tokens

**p95 latency:** ~1.8s for similar outputs

**Polish language support:** Excellent. The best of the managed APIs we tested on Polish legal and insurance text.

**Compliance story:** More complex for European enterprise clients. OpenAI's enterprise tier and data processing agreements help, but the "data leaving EU" question comes up in every enterprise sales conversation. Not a dealbreaker, but an overhead.

**Our evaluation:** Faithfulness score 0.91, answer relevance 0.88. Best raw quality in the managed API category.

### Mistral Medium (Mistral API)

**Pricing:** approx. ~$0.4/1M input tokens, ~$1.2/1M output tokens (estimated based on published Mistral pricing tiers)

**Context window:** 32k tokens

**p95 latency:** ~1.2s

**Polish language support:** Sufficient for technical content, weaker on formal legal Polish. Occasional translation-like phrasing that doesn't match how Polish speakers actually write insurance documents.

**Compliance story:** Mistral is a French company with EU data residency options — a genuine advantage over OpenAI for European regulated industries.

**Our evaluation:** Faithfulness score 0.78, answer relevance 0.76. Meaningful quality gap vs Claude/GPT-4o on our domain. However, the price-to-quality ratio is the best of the managed APIs if your language requirements are more forgiving.

### Bielik (Self-Hosted)

Bielik is an open-source Polish language model developed as part of the SpeakLeash project, specifically trained on Polish text. We ran it on a self-managed GPU instance (A100 40GB).

**Pricing per token:** Effectively zero once the GPU is running. The cost is in the infrastructure.

**Context window:** 8k tokens (earlier versions) — this is a real constraint

**p95 latency:** ~1.4s on A100 (highly dependent on batching and hardware)

**Polish language support:** Exceptional on Polish insurance text. This is what it was built for.

**Compliance story:** Perfect — data never leaves your infrastructure.

**Our evaluation:** On our insurance document test set, Bielik outperformed Mistral Medium by **12 percentage points on precision** for questions involving Polish-specific clauses and terminology. It was within 5pp of Claude Sonnet on our evaluation set. That's a remarkable result for an open-source model.

The catch is everything else.

## The Hidden Costs of Self-Hosting

Bielik's per-token cost is zero. The operational cost is not.

Running a model in production requires:

- **GPU infrastructure:** An A100 instance on AWS (p4d.24xlarge) runs approx. $32/hour on-demand, or ~$15/hour reserved. Monthly: $10,800–$23,000 depending on reserved capacity.
- **Engineering overhead:** Model deployment, inference optimization, autoscaling, monitoring, updates. We estimated 0.5 FTE to run this properly.
- **Storage and serving infrastructure:** Model weights (~14GB for Bielik 13B), serving framework (vLLM, TGI), load balancer, health checks.

At 10,000 queries/month, self-hosting costs dramatically more than a managed API. At 200,000 queries/month with average response generation of ~500 tokens, managed API costs start to become painful.

The **break-even point** between self-hosted and managed depends heavily on your architecture, but for most teams it's somewhere in the range of 50,000–100,000 queries/month. Most teams building their first RAG system don't hit this in year one.

## Comparison Table

| Model | Input $/1M | Output $/1M | Context | Polish | Compliance |
|---|---|---|---|---|---|
| Claude Sonnet (Bedrock) | $3 | $15 | 200k | Good | AWS VPC, GDPR-friendly |
| GPT-4o | $5 | $15 | 128k | Excellent | Enterprise tier required |
| Mistral Medium | ~$0.4* | ~$1.2* | 32k | Sufficient | EU data residency option |
| Bielik (self-hosted) | $0/token | $0/token | 8k | Exceptional | Full control |

*Approx. based on published tier pricing as of early 2026. Verify before committing.

## How to Actually Evaluate Models on Your Data

Here's the evaluation process we use. It takes 2–3 days to set up; it saves you weeks of bad decisions.

**Step 1: Build a golden test set.**
Take 50–100 real queries from your system — questions users have actually asked or will ask. For each, write an expected answer, and tag the source chunk in your document corpus that should be retrieved.

**Step 2: Run full RAG pipeline per model.**
Don't just evaluate generation in isolation. Run the full pipeline: query → retrieval → context construction → generation → response. Isolate models only to understand generation quality separately.

**Step 3: Measure what matters.**

- **Faithfulness:** Does the answer stay within the retrieved context, or does the model introduce information not in the documents? (Use RAGAS or a custom LLM-as-judge setup)
- **Answer relevance:** Does the answer actually address the question asked?
- **Retrieval recall:** Are the ground-truth source chunks appearing in the top-5 retrieved results? (Evaluate retrieval separately — often the bottleneck is there, not in generation)

**Step 4: Measure latency under realistic load.**
Single-query latency is irrelevant. What matters is p95 latency when 10 users query simultaneously. This often reveals that the cheapest API becomes expensive when you add timeout handling and retries.

## The Decision Framework

Ask these questions in order:

1. **Volume:** Fewer than 50k queries/month? Use a managed API. More? Start modeling self-hosted break-even.
2. **Language:** Polish-heavy or other non-English European language? Bielik or Claude Sonnet outperform general models. Don't overlook this.
3. **Compliance:** Regulated industry, European clients, sensitive data? AWS Bedrock (Claude) or Mistral EU tier will make your legal conversations simpler.
4. **Context length:** Do your documents require >32k token context windows? GPT-4o or Claude Sonnet. Mistral Medium and Bielik have real constraints here.
5. **Quality floor:** Run your evaluation set. If faithfulness drops below 0.80 or answer relevance below 0.75, that model isn't production-ready for your use case — regardless of price.

The model that wins on benchmarks almost never wins on all five dimensions simultaneously. That's why you evaluate on your data, not on leaderboards.

## What We Ended Up With

Our primary production system uses Claude Sonnet via AWS Bedrock. The compliance story, the context window, and the overall quality-to-cost ratio at our current volume made it the clear choice.

We run Bielik in a secondary pipeline for a specific subset of Polish-language queries where precision matters more than cost or latency. That 12pp precision improvement on Polish insurance clauses is real and worth the infrastructure overhead for that use case.

GPT-4o sits in our evaluation pipeline as a reference standard — we use it to generate reference answers when building new golden test sets, because its output quality on complex reasoning is still the best we've tested.

The "right" model changes as your volume grows and as the models themselves improve. Build an evaluation system that lets you re-run comparisons quarterly. The landscape is moving too fast for a one-time decision.

---

*Day 37 of the RAG Deep Dive series. Tomorrow: chunking strategies — why the retrieval problem is mostly a data preparation problem.*
