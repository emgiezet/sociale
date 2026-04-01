---
day: 46
title: "How Much Does RAG Actually Cost? A TCO Framework Across Three Architectures"
pillar: Educator
language: en
image: ../../images/day-46.jpg
image_unsplash_query: "financial model spreadsheet cost analysis infrastructure budget"
---

# How Much Does RAG Actually Cost? A TCO Framework Across Three Architectures

"How much does RAG cost?" is the wrong question. It's like asking "how much does a car cost?" — the answer is anywhere from $8,000 to $250,000 depending on what you're buying, why you're buying it, and what it costs to run over three years.

I've been asked this question enough times, and watched enough projects underestimate their costs enough times, that I built a proper TCO model for it. This post shares that model, with realistic (clearly estimated) numbers across three common architectures for a fixed use case.

---

## The Six Variables That Determine RAG Pricing

Before we can talk about numbers, we need to talk about the inputs to the model. These six variables explain most of the price variance I've seen across real projects.

### Variable 1: Document Volume and Query Volume

Document count determines your indexing cost (one-time per batch + recurring on updates) and your index hosting cost (vector database storage). Query volume determines your inference cost (embeddings per query + LLM tokens per generation).

The relationship isn't linear. Going from 1,000 to 10,000 documents is mostly a storage cost. Going from 1,000 to 10,000 queries/day is primarily an inference cost — and inference costs compound because both the embedding model and the LLM run on every query.

### Variable 2: Language and Domain

English documents: you have access to the full range of high-quality, cost-efficient models. Amazon Titan Embed, Cohere Embed, Claude Haiku/Sonnet — the market is competitive and prices reflect that.

Polish documents (and many other non-English European languages): your options narrow meaningfully:

- You can use multilingual embedding models (E5-multilingual, Cohere multilingual) at higher cost per token than English-optimized models
- You can use Claude or GPT-4 class models which handle Polish adequately but at premium pricing
- You can self-host Polish-native models like Bielik (12 billion parameter model, open weights) at infrastructure cost instead of per-token cost

At Insly, we found a 12 percentage point precision improvement switching from multilingual embeddings to Bielik for Polish insurance document retrieval. The self-hosting cost was justified by both quality and data residency requirements.

### Variable 3: Quality SLA

This is the variable most clients underestimate when scoping. The difference between targeting 80% answer accuracy and 95% answer accuracy is not a 15% engineering effort increase. It's roughly 3x the total cost of the quality assurance and iteration loop.

Why? Because:
- Each percentage point above ~85% requires significantly more labeled evaluation data to measure reliably
- The improvement techniques that get you from 80% to 90% (better chunking, better prompts) are cheap. Getting from 90% to 95% requires specialized retrieval strategies, extensive fine-tuning, and ongoing human evaluation — all expensive.
- The monitoring overhead scales with your quality target: a 95% precision system requires continuous evaluation; an 80% system can tolerate weekly spot checks.

In insurance, where we need > 92% precision on factual queries about coverage amounts and exclusions, this variable alone determines whether the system costs $1,200/month or $3,500/month.

### Variable 4: Compliance Requirements

Each compliance requirement translates directly to an architectural cost:

**RODO / GDPR data residency**: Data cannot leave the EU. This eliminates some commercial API options or requires specific configuration. In practice, it means running on EU-region AWS (Frankfurt, Ireland) and verifying that no query data transits to US-region endpoints.

**PII handling**: Requires detection and redaction of personal data in both inputs and outputs. Either Bedrock Guardrails (adds ~$0.75/1k input tokens for guardrail processing) or custom PII pipeline (engineering cost).

**Audit trail**: Every query and response must be logged with sufficient metadata for compliance review. This requires a dedicated logging infrastructure — not just CloudWatch, but structured logs with immutable retention.

**Insurance-specific**: In Poland, insurance distribution regulations require that any system giving product information to brokers maintains an audit trail that can be produced in regulatory review. This architectural requirement isn't optional.

Cost impact: a fully compliant insurance RAG costs approximately 40-60% more in total development and annual maintenance than a non-regulated internal tool of equivalent query volume.

### Variable 5: Integration Complexity

A standalone chatbot (separate URL, users navigate to it) is the simplest integration: a web frontend calling an API. Development time: 2-4 weeks.

Embedding in an existing broker portal (inline in the product search workflow, authenticated, context-aware): 3-5x more development time. You're building an integration into an existing system, handling session context, authentication, role-based access, and potentially displaying results in a structured format native to the existing UI.

The integration cost often exceeds the RAG pipeline cost in enterprise projects. Clients focusing on "the AI cost" miss this entirely.

### Variable 6: Ongoing Maintenance

This is the most commonly underestimated cost, and the one that kills projects in year 2.

Ongoing maintenance work:
- **Evaluation cadence**: running the canary test set, reviewing results, investigating regressions. Budget 4-8 engineering hours per month minimum.
- **Model updates**: cloud providers silently update models. Bedrock model updates have shifted our precision metrics by up to 6 points. Someone has to catch this.
- **Document reindexing**: insurance policies change annually. Reindexing 1,000 documents takes roughly 2-4 engineering hours plus embedding costs.
- **Prompt iteration**: user queries evolve. New query patterns appear that your current prompts handle poorly. Prompt tuning is an ongoing activity.
- **User support for first 3-6 months**: "Why doesn't it know about X?" takes disproportionate engineering time after launch.

If you staff zero ongoing maintenance, expect precision to drift from 92% to 78% within 18 months as documents change, models update, and query patterns evolve.

---

## Case Study: Three Architectures, One Use Case

**Fixed scenario**: 1,000 Polish-language insurance documents, 5,000 queries/month, 90%+ precision target, RODO-compliant, standalone chatbot (no integration), EU deployment.

All numbers below are estimates based on published AWS pricing (current as of early 2026), typical GPU rental rates, and my experience with engineering time for similar projects. They are clearly labeled as estimates where uncertainty exists.

### Option A: Full Managed (AWS Bedrock)

All components are managed AWS services. No infrastructure to operate.

**Components**:
- Embeddings: Amazon Titan Embed v2 (Polish-capable multilingual)
- Vector store: Amazon OpenSearch Serverless
- LLM: Claude Sonnet 3.5 via Bedrock
- Guardrails: Bedrock Guardrails for PII
- Evaluation: custom canary set + CloudWatch

**Development cost** (one-time, estimate):
- Pipeline setup and integration: ~40 engineering hours (~$4,000 at blended senior dev rate)
- Evaluation set creation (80 labeled questions): ~16 hours (~$1,600)
- Total one-time: ~$5,600

**Monthly recurring cost** (at 5,000 queries/month):
- Titan Embed v2: ~$0.02/1k tokens × ~200k tokens/month = ~$4
- OpenSearch Serverless: minimum ~$175/month (OCU pricing, serverless floor)
- Claude Sonnet 3.5: ~$3/1k output tokens × ~50k output tokens/month = ~$150
- Bedrock Guardrails: ~$0.75/1k input tokens × ~100k tokens/month = ~$75
- CloudWatch + logging: ~$20
- Engineering maintenance: 6h/month × $100/h = ~$600
- **Total monthly recurring: ~$1,025**

**TCO**:
- Year 1: $5,600 + (12 × $1,025) = ~$17,900
- Year 2: 12 × $1,025 = ~$12,300
- Year 3: 12 × $1,025 = ~$12,300
- **3-year total: ~$42,500**

**Trade-offs**:
- Lowest barrier to entry
- No infrastructure to manage
- Limited control over model behavior (dependent on AWS model updates)
- Data residency requires EU-region configuration
- Highest per-query cost at scale (costs scale linearly with query volume)

### Option B: Self-Hosted (Bielik + Qdrant)

Bielik 12B for both embeddings and generation (Polish-native), Qdrant as self-hosted vector database on EC2.

**Infrastructure**:
- Embedding and generation: g4dn.2xlarge (1x T4 GPU, $0.752/hour) — dedicated instance for 24/7 operation
- Vector database: m6i.large for Qdrant (~$0.096/hour)
- 24/7 monthly estimate: (~$0.752 + ~$0.096) × 730h = ~$620/month infrastructure

**Development cost** (one-time, estimate):
- Bielik setup, quantization, serving: ~60 engineering hours (~$6,000)
- Qdrant setup, indexing pipeline: ~40 hours (~$4,000)
- Evaluation infrastructure: ~20 hours (~$2,000)
- Total one-time: ~$12,000

**Monthly recurring cost**:
- EC2 infrastructure: ~$620
- Engineering maintenance (higher than managed — you own the infra): ~10h × $100/h = ~$1,000
- CloudWatch equivalent logging: ~$15
- **Total monthly recurring: ~$1,635**

**Note on quality**: Bielik gives ~12pp precision improvement on Polish insurance documents over multilingual alternatives in our testing. At 90% SLA target, this is meaningful — it may be the difference between meeting the target and extensive prompt engineering to compensate for weaker embeddings.

**TCO**:
- Year 1: $12,000 + (12 × $1,635) = ~$31,600
- Year 2: 12 × $1,635 = ~$19,600
- Year 3: 12 × $1,635 = ~$19,600
- **3-year total: ~$70,800**

Wait — self-hosted is more expensive? Yes, at this scale. Self-hosted makes economic sense when query volume is 20x higher (infrastructure cost amortizes) or when data residency requirements are stricter than managed services can accommodate.

**Trade-offs**:
- Full control over model behavior and updates
- Best Polish-language precision
- Highest data residency control
- Significant infrastructure overhead
- Higher total cost at 5k queries/month scale

### Option C: Hybrid (Bedrock Generation + Self-Hosted Embeddings)

Use Bielik for embeddings (self-hosted, for precision) and Claude via Bedrock for generation (managed, for reliability and compliance).

**Components**:
- Embeddings: Bielik 7B embedding model on t3.xlarge (~$0.166/hour, smaller GPU not needed for inference-only embeddings — CPU-based with batching)
- Vector store: Qdrant on t3.medium (~$0.042/hour)
- Generation: Claude Haiku via Bedrock (cheaper than Sonnet; sufficient when retrieval is high-quality)
- Guardrails: Bedrock Guardrails

**Development cost** (one-time, estimate):
- Hybrid pipeline setup: ~80 engineering hours (~$8,000)
- (More complex than either pure approach due to mixed infrastructure)

**Monthly recurring cost**:
- t3.xlarge (embedding): ~$120/month
- Qdrant on t3.medium: ~$31/month
- Claude Haiku via Bedrock: ~$0.25/1k input × ~200k tokens/month = ~$50
- Bedrock Guardrails: ~$75
- Engineering maintenance: ~7h × $100/h = ~$700
- **Total monthly recurring: ~$976**

**TCO**:
- Year 1: $8,000 + (12 × $976) = ~$19,700
- Year 2: 12 × $976 = ~$11,700
- Year 3: 12 × $976 = ~$11,700
- **3-year total: ~$43,100**

**TCO Comparison Table**:

| | Option A (Full Managed) | Option B (Self-Hosted) | Option C (Hybrid) |
|---|---|---|---|
| One-time dev cost | ~$5,600 | ~$12,000 | ~$8,000 |
| Monthly recurring | ~$1,025 | ~$1,635 | ~$976 |
| Year 1 total | ~$17,900 | ~$31,600 | ~$19,700 |
| Year 2 total | ~$12,300 | ~$19,600 | ~$11,700 |
| Year 3 total | ~$12,300 | ~$19,600 | ~$11,700 |
| 3-year TCO | ~$42,500 | ~$70,800 | ~$43,100 |
| Polish precision | Medium | Highest | High |
| Infra overhead | Low | High | Medium |
| Control | Low | Full | Medium |

The client who prompted me to build this model initially assumed self-hosted was cheapest ("no API costs!"). At 5,000 queries/month, it's substantially more expensive due to fixed infrastructure costs. Option C delivered the best balance at this scale: nearly the precision benefit of Bielik for retrieval, the reliability of managed Bedrock for generation, and the lowest 3-year TCO.

---

## Hidden Costs Clients Don't See

The numbers above assume competent ongoing maintenance. Here's what "competent maintenance" actually looks like in hours and cost:

**Evaluation and monitoring** (4-8h/month): Running the canary test set, reviewing dashboards, investigating precision regressions. This cannot be automated away entirely — someone has to interpret results and decide when to act.

**Annual document reindexing** (2-4h + embedding costs): Insurance policies change annually. The full corpus reindex needs quality verification against the evaluation set after completion.

**Model drift incidents** (variable, ~10-20h/incident): Cloud providers silently update models. When it happens, you need to detect it, characterize the impact, and recalibrate thresholds. Budget for 1-2 incidents per year.

**New query pattern handling** (4-8h/quarter): User behavior evolves. Prompt strategies that worked at launch need updates as query patterns shift. This is prompt engineering, not infrastructure.

**Year 2 user support tail-off**: First 3-6 months post-launch, user support overhead is high (~20% of engineering time touching the system). It drops to ~5% by month 12 as users learn the system's capabilities and limitations.

If a client builds Option A and assumes the $5,600 one-time cost covers everything: by month 18, they have an unmonitored system with drifting precision and no budget to fix it. I've seen this pattern more than once.

---

## How to Present Pricing to Clients

The wrong way: "RAG costs $X/month."

The right way: "Here are three architectures for your use case, with trade-offs and 3-year TCO for each. The cheapest option at year 1 is not the cheapest option at year 3. Here's why, and here's which one I recommend given your constraints."

This conversation does three things:
1. Sets realistic expectations about ongoing cost (not just build cost)
2. Surfaces compliance and quality requirements that change the analysis
3. Positions you as someone solving a business problem, not selling a technology

The clients who are surprised by year-2 RAG costs are usually clients who were sold on "build cost" without a TCO conversation. Don't be the person who creates that surprise.

---

## Summary

RAG pricing depends on six variables: document volume, query volume, language, quality SLA, compliance requirements, and integration complexity. Get clarity on all six before quoting anything.

For 1,000 Polish insurance documents at 5,000 queries/month with 90%+ precision:
- Full managed (Bedrock): ~$42,500 over 3 years, lowest setup friction
- Self-hosted (Bielik + Qdrant): ~$70,800 over 3 years, best precision and control
- Hybrid (Bielik embeddings + Bedrock generation): ~$43,100 over 3 years, best balance at this scale

The cheapest infra isn't the cheapest TCO. The most expensive infra isn't always the best quality. Run the numbers before committing to an architecture.

DM me "RAG PRICING" if you're scoping a RAG project — I can share the spreadsheet version of this model.
