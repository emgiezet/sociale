---
day: 39
title: "The Real Cost of Running RAG in Production: Three Architectures, Three Cost Models"
pillar: Educator
language: en
image: ../../images/day-39.jpg
image_unsplash_query: "cloud computing costs infrastructure billing dashboard"
---

# The Real Cost of Running RAG in Production: Three Architectures, Three Cost Models

Every RAG tutorial ends with a working demo. None of them mention what it costs to run that demo at 10,000 queries a month. Or 200,000.

I've built and run three RAG systems in production at Insly — a European InsurTech SaaS serving 150,000+ users with an 11-engineer team. In this post, I'm breaking down the real cost of three different RAG architectures, with actual numbers, hidden costs, and the break-even analysis that most teams build too late.

Counterintuitive opening claim: self-hosted RAG is often more expensive than managed. At least for the first year.

## The Cost Components of a RAG System

Before comparing architectures, let's map what actually costs money. A RAG system has four cost layers:

1. **Embedding:** Turning text into vectors (both at indexing time and query time)
2. **Vector storage and retrieval:** The database that stores and searches embeddings
3. **Generation:** The LLM that produces the final answer given the retrieved context
4. **Operational overhead:** Engineering time, monitoring, evaluation, iteration

Layer 4 is real money. It's just not in any pricing calculator.

## Architecture 1: AWS Bedrock (Fully Managed)

This is the "lowest operational overhead" option. AWS Bedrock provides managed embeddings (Amazon Titan Embed), managed vector storage (OpenSearch Serverless via Bedrock Knowledge Base), and managed LLM inference (Claude Sonnet, Llama, Titan).

**Component costs at 10,000 queries/month:**

| Component | Unit price | Monthly volume | Monthly cost |
|---|---|---|---|
| Titan Embed v2 (indexing, one-time) | $0.02/1M tokens | Variable (depends on corpus size) | ~$2–5 one-time |
| Titan Embed v2 (query-time) | $0.02/1M tokens | 10k queries × ~50 tokens avg | ~$0.10 |
| OpenSearch Serverless (OCU) | ~$0.24/OCU-hour | Minimum 2 OCU | ~$350/month |
| Claude Sonnet generation | $3/1M input + $15/1M output | 10k × (500 input + 300 output) | ~$49 |
| Bedrock Knowledge Base requests | $0.000004/request | 10,000 requests | ~$0.04 |

**Total at 10,000 queries/month: approximately $400/month**

Wait — $350 for OpenSearch Serverless? Yes. OpenSearch Serverless has a minimum of 2 OCU (OpenSearch Compute Units) per collection, at $0.24/OCU-hour. That's $172.80/month per OCU, minimum $345.60/month just for the vector store, before you've made a single query.

This is the biggest hidden cost in the AWS Bedrock stack. For small deployments, you're paying for capacity you don't use.

**Mitigation:** For development and small-scale deployments, use OpenSearch Serverless only when you need the full Bedrock Knowledge Base integration. For smaller workloads, an alternative is to use a separate vector database (Pinecone, Qdrant, pgvector) with Bedrock for embeddings and generation only.

**Revised estimate using Bedrock for LLM + embeddings only, external vector DB:**

| Component | Monthly cost |
|---|---|
| Titan Embed v2 (query-time, 10k queries) | ~$0.10 |
| Qdrant Cloud (free tier or basic tier) | $0–$25 |
| Claude Sonnet generation (10k queries) | ~$49 |
| **Total** | **~$50–75/month** |

This is a much more reasonable number for early-stage systems. Scale to 50k queries: ~$200–250/month. Scale to 200k queries: ~$750–900/month.

**At 200k queries/month, Bedrock generation cost alone is ~$1,000/month.** That's when the self-hosted conversation starts making sense.

## Architecture 2: Self-Hosted GPU (Mistral or Bielik)

Running your own LLM eliminates the per-token generation cost. The trade is fixed infrastructure cost and engineering overhead.

**GPU infrastructure options:**

| Instance type | GPU | On-demand $/hr | Reserved $/hr (approx.) | Monthly (reserved) |
|---|---|---|---|---|
| p3.2xlarge | V100 16GB | $3.06 | ~$1.50 | ~$1,080 |
| p4d.24xlarge | 8× A100 40GB | $32.77 | ~$15 | ~$10,800 |
| g5.2xlarge | A10G 24GB | $1.21 | ~$0.60 | ~$432 |

For Mistral 7B or Bielik 7B, an A10G (g5.2xlarge) is sufficient for moderate throughput. For Mistral 13B or Bielik 13B at production load, you need at minimum a V100 or A100.

**Full cost model for self-hosted (g5.2xlarge, Mistral 7B):**

| Component | Monthly cost |
|---|---|
| GPU instance (g5.2xlarge, reserved) | ~$432 |
| Model storage (EBS, 20GB) | ~$2 |
| Vector database (Qdrant, self-hosted EC2 c5.xlarge) | ~$140 |
| Embedding (self-hosted or API) | ~$5–30 |
| Engineering overhead (0.3 FTE @ $10k/month FTE cost) | ~$3,000 |
| **Total (excluding eng. overhead)** | **~$580/month** |
| **Total (including eng. overhead estimate)** | **~$3,580/month** |

The engineering overhead number is the important one. Someone has to deploy the model, configure vLLM or TGI for serving, set up autoscaling, monitor inference latency, handle model updates, and debug serving failures at 2am. At 0.3 FTE of an experienced ML engineer, this is not a trivial cost.

**Per-token cost at scale:** Once the GPU is paid for, additional tokens are essentially free. At 200k queries/month with 800 tokens of generation per query, the generation cost is the GPU cost divided by the throughput — roughly $0.003–0.010 per query on a reserved A10G, depending on batch efficiency.

**Break-even vs managed API:**

| Monthly queries | Bedrock (Claude Sonnet only) | Self-hosted (g5.2xlarge + 0.3 FTE) | Self-hosted cheaper? |
|---|---|---|---|
| 10,000 | ~$50 | ~$3,580 | No |
| 50,000 | ~$240 | ~$3,590 | No |
| 200,000 | ~$960 | ~$3,620 | No |
| 500,000 | ~$2,400 | ~$3,650 | Borderline |
| 1,000,000 | ~$4,800 | ~$3,700 | Yes |

These numbers illustrate the key insight: **if you include realistic engineering overhead, self-hosted doesn't break even until you're above 500k-1M queries/month.** Most teams building their first RAG system don't reach this volume in year one.

**When self-hosted is genuinely the right call:**
- Compliance requirement: data cannot leave your infrastructure (common in European regulated industries)
- Volume above 500k queries/month consistently
- Latency requirement: sub-500ms response, and the API round-trip plus rate limits are the bottleneck
- Specific model requirement: you need Bielik for Polish-language precision and there's no managed API for it

## Architecture 3: Hybrid (Self-Hosted Retrieval + Managed Generation)

The middle path: run your own vector database and retrieval infrastructure (full control over chunking, metadata, re-ranking), but use a managed API for LLM generation.

**Cost model:**

| Component | Monthly cost |
|---|---|
| EC2 c5.xlarge (Qdrant self-hosted) | ~$140 |
| Titan Embed v2 or Cohere Embed (10k queries) | ~$0.50–2 |
| Claude Sonnet via Bedrock (10k queries) | ~$49 |
| Reranking (Cohere Rerank API, optional) | ~$10–40 |
| Engineering overhead (0.1 FTE) | ~$1,000 |
| **Total (excluding eng. overhead)** | **~$190–230/month** |
| **Total (including eng. overhead estimate)** | **~$1,190–1,230/month** |

The hybrid approach gives you control over the retrieval layer — you can use custom chunking, metadata filtering, hybrid search (vector + BM25), and advanced reranking — without the cost of self-hosting the LLM.

It's our preferred architecture for medium-scale deployments where retrieval quality matters more than generation cost, and where compliance allows using a managed LLM API.

## The Costs That Don't Appear in Pricing Pages

The token costs are visible. These costs are real but invisible:

**Evaluation costs.** Running your golden test set to measure faithfulness and recall costs money. At 100 test queries, with 2 LLM calls per evaluation (generation + LLM-as-judge), at 1,000 tokens per call, at $18/1M tokens combined: each evaluation run costs ~$3.60. You run this on every significant change. At 3-5 runs per week during active development, that's $50–90/month.

**Re-indexing costs.** When you change your chunking strategy (which you will), you re-embed and re-index your entire corpus. For a 100k document corpus at 500 tokens per chunk, 2 chunks per document: 100M tokens × $0.02/1M = $2. Doesn't sound like much until you re-index weekly.

**Reranking.** Adding a reranker (Cohere Rerank, or a cross-encoder running on a small GPU) adds latency and cost to every query. Cohere Rerank API: $1/1k queries = $10 at 10k queries. Cheap, but adds 100–200ms p50 latency.

**Monitoring and logging.** Storing query logs, retrieved chunks, and generated responses for debugging and compliance: S3 costs, CloudWatch costs, or equivalent. Small individually, non-trivial at scale.

**The iteration cycle.** Most teams change their RAG pipeline significantly 3–5 times in the first six months. Each change requires evaluation, re-indexing, and re-deployment. The person doing this is an engineer. Their time is the biggest cost.

## What We Run at Insly

Our primary pipeline is the hybrid architecture: Qdrant (self-hosted on EC2) for retrieval, Claude Sonnet via AWS Bedrock for generation. This gives us control over chunking and retrieval logic while keeping the LLM managed.

At our current volume, this costs approximately $400–600/month in infrastructure and API costs. The real cost, when you include the engineering time to maintain it, is higher — but that cost is shared across three RAG systems, not just one.

The decision to stay on managed LLM (not self-host the generation model) was driven by compliance and simplicity, not cost. At our volume, the API cost is manageable. When it stops being manageable, we have Bielik ready for evaluation.

## The Summary Table

| Architecture | 10k queries/month | 50k queries/month | 200k queries/month | Ops overhead |
|---|---|---|---|---|
| AWS Bedrock (full) | ~$400 | ~$800 | ~$2,000 | Very low |
| AWS Bedrock (LLM + embeds only, ext. vector DB) | ~$75 | ~$250 | ~$950 | Low |
| Self-hosted (A10G, 0.3 FTE) | ~$3,600 | ~$3,620 | ~$3,650 | High |
| Hybrid (ext. vector DB + managed LLM) | ~$200 | ~$450 | ~$1,200 | Medium |

All costs approximate. Verify current pricing before architectural decisions. Engineering overhead is estimated at $10k/month FTE cost — adjust for your market.

---

*Day 39 of the RAG Deep Dive series. Next week: RAG Masterclass — advanced retrieval techniques. We start with HyDE: bridging the semantic gap between user questions and document language.*
