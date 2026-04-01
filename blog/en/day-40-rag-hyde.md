---
day: 40
title: "HyDE: Closing the Semantic Gap Between User Questions and Document Language"
pillar: Educator
language: en
image: ../../images/day-40.jpg
image_unsplash_query: "semantic search document retrieval bridge gap"
---

# HyDE: Closing the Semantic Gap Between User Questions and Document Language

On day 7, I wrote about why RAG systems built from tutorials break down when they hit real documents. One of the core reasons is a problem called the semantic gap — and HyDE is one of the most elegant solutions I've found for it.

Let me show you the problem concretely, then walk through how HyDE fixes it, where it works, and where it doesn't.

## The Semantic Gap Problem

A broker asks: "Does this policy cover flood damage to the property?"

The relevant clause reads: "The scope of coverage includes accidental events involving damage to the insured property in accordance with §4 subsection 2, including events classified as natural disasters under applicable Polish law."

The word "flood" never appears in the clause. The phrase "flood damage" has no direct lexical match in the document. The user's question and the relevant answer occupy different neighborhoods in the embedding space.

Vector similarity search works by finding documents whose embeddings are geometrically close to the query embedding. If the query contains "flood damage" and the relevant passage contains "accidental events involving damage in accordance with §4", the cosine similarity between these embeddings may be low — even though this is exactly the right document.

This is the semantic gap: the language in which users ask questions and the language in which formal documents are written often differ significantly. This problem is worst in domains with heavy specialized jargon: insurance, law, medicine, financial regulation.

In our production experience at Insly, naive semantic search on insurance documents had a retrieval recall of approximately 0.61 on our golden test set — meaning 39% of the time, the right clause wasn't in the top-5 retrieved results. The LLM then answered from insufficient context, producing incomplete or incorrect responses.

HyDE was one of the interventions that moved that number significantly.

## How HyDE Works

HyDE — Hypothetical Document Embeddings — was proposed by Gao et al. in the 2022 paper "Precise Zero-Shot Dense Retrieval without Relevance Labels." The core insight is simple and effective.

**Standard RAG retrieval:**
1. Embed the user query: `query_embedding = embed("Does this policy cover flood damage?")`
2. Search for similar chunks: `results = vector_search(query_embedding, top_k=5)`

**HyDE retrieval:**
1. Ask an LLM to generate a hypothetical answer to the query: an answer that *looks like it would appear in the target document corpus*
2. Embed the hypothetical answer: `hyde_embedding = embed(hypothetical_answer)`
3. Search for similar chunks using the hypothetical answer embedding: `results = vector_search(hyde_embedding, top_k=5)`

The hypothetical answer doesn't need to be factually correct — it doesn't matter if the LLM invents details. What matters is that it's written in the same register, vocabulary, and style as the actual documents. When the LLM generates "The policy covers flood damage as an accidental event under §4, subject to exclusions listed in §7", that generated text lives in the same embedding neighborhood as the actual clauses in the document.

You're not searching for the question. You're searching for documents that look like the answer.

## Python Implementation

Here's the core implementation we use. It's straightforward once you understand the principle.

```python
from anthropic import Anthropic
import boto3
import numpy as np

client = Anthropic()
bedrock = boto3.client("bedrock-runtime", region_name="eu-west-1")

def generate_hypothetical_document(query: str, domain_context: str) -> str:
    """Generate a hypothetical answer document using an LLM."""
    prompt = f"""You are generating a hypothetical passage from a formal {domain_context} document.
    
A user asked: "{query}"

Write a short passage (2-4 sentences) that WOULD answer this question if it appeared in a formal {domain_context} document. 
Use formal document language and terminology. Do not indicate that this is hypothetical.
The passage should be written as if it is an excerpt from the actual document."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def embed_text(text: str) -> list[float]:
    """Get embeddings via AWS Bedrock Titan Embed."""
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": text, "dimensions": 1024})
    )
    return json.loads(response["body"].read())["embedding"]

def hyde_retrieve(query: str, vector_store, domain_context: str = "insurance policy", top_k: int = 5):
    """Retrieve using HyDE: generate hypothetical document, embed it, search."""
    # Generate hypothetical answer
    hypothetical_doc = generate_hypothetical_document(query, domain_context)
    
    # Embed the hypothetical document
    hyde_embedding = embed_text(hypothetical_doc)
    
    # Search using the hypothetical embedding
    results = vector_store.similarity_search_by_vector(hyde_embedding, k=top_k)
    
    return results, hypothetical_doc  # Return the hypothetical doc for debugging

# Example usage
query = "Does the policy cover flood damage to the insured property?"
results, hyp_doc = hyde_retrieve(query, vector_store, domain_context="Polish insurance policy")

print(f"Hypothetical document: {hyp_doc}")
print(f"Retrieved {len(results)} chunks")
```

**What the hypothetical document might look like for our flood query:**

> "The insurer provides coverage for damages resulting from natural disaster events, including flooding caused by overflow of water bodies and extreme precipitation. Such events are classified as accidental events within the meaning of §4 subsection 2, provided that the insured has maintained continuous coverage and that the event is documented in accordance with §12."

This text contains "flooding", "water bodies", "accidental events", "§4", "coverage" — the vocabulary of the actual policy documents. The embedding of this hypothetical text will be much closer to the actual clause than the embedding of the original user question.

## Measuring the Impact

We measured HyDE performance on our insurance document test set: 80 queries, each with manually verified ground-truth source chunks.

**Retrieval recall@5 (the target chunk appears in top 5 results):**

| Method | Recall@5 | Notes |
|---|---|---|
| Naive semantic search | 0.61 | Baseline |
| + Metadata filtering | 0.71 | Filters by document type, market |
| + HyDE | 0.79 | On queries with domain jargon |
| + HyDE + reranking | 0.84 | Cohere Rerank on top-20, return top-5 |

HyDE added 8 percentage points of retrieval recall on top of metadata filtering. On the subset of queries that involved heavy insurance jargon (roughly 60% of our test set), the improvement was 13-15 percentage points.

**Important nuance:** HyDE helped most on queries where the user's vocabulary differed significantly from the document vocabulary. On queries where the user's phrasing directly matched document language ("cancellation clause", "policy number", "premium due date"), HyDE added no measurable benefit.

## When HyDE Helps vs When It Doesn't

**HyDE is valuable when:**
- User queries use natural language; documents use formal/legal/technical language
- Domain vocabulary is specialized and not widely used in general language models' training data
- The documents contain dense, reference-heavy text where a single concept has many synonyms
- Retrieval quality is the bottleneck (not generation quality)

**HyDE adds cost and latency with limited benefit when:**
- Queries are simple factual lookups ("what is the policy number?")
- User vocabulary and document vocabulary are already similar
- The corpus is small enough that full-scan hybrid search (BM25 + vector) already achieves high recall
- Latency budget is tight — HyDE adds one LLM call per query, typically 300–600ms

**HyDE can hurt when:**
- The LLM generates a hypothetical document that confidently describes something incorrect, pulling retrieval away from the right documents
- The domain is highly specialized and the LLM doesn't have good priors for document language (e.g., very niche technical specifications)

We ran an ablation test where we deliberately used a poor-quality hypothetical generation (too short, not domain-specific). Retrieval recall dropped below baseline — the bad hypothetical was actively misleading the retrieval.

The quality of the hypothetical generation matters. Use a capable model and a well-crafted prompt.

## Cost Analysis

HyDE adds one LLM call per user query. At Claude Sonnet pricing (~$3/1M input + $15/1M output):

- Hypothetical generation prompt: ~150 tokens
- Hypothetical output: ~100-150 tokens
- Cost per query: ~$0.00045 + ~$0.0015 ≈ **$0.002 per query**

At 10,000 queries/month: ~$20/month additional cost for HyDE generation.
At 50,000 queries/month: ~$100/month additional.
At 200,000 queries/month: ~$400/month additional.

Compare this to the value of 8–15 percentage points of retrieval recall improvement. For a production system where incorrect retrieval means wrong answers to insurance questions, the value is clear. For a demo or an internal tool with low stakes, it might not be worth the additional latency and cost.

**Latency impact:** The additional LLM call adds ~300–800ms to p50 latency. For interactive applications, this is noticeable. You can mitigate this with:
- Async generation (start retrieval with original query while hypothetical generates, merge results)
- Caching hypothetical documents for common query patterns
- Using a faster/cheaper model for hypothetical generation (e.g., Claude Haiku)

## Connecting to the Broader Pipeline

This is day 40 — the start of the RAG Masterclass — but HyDE doesn't live in isolation. It connects directly to everything covered in the past week:

- **Day 38 (chunking):** Better chunks → better retrieval even without HyDE. HyDE doesn't fix bad chunking; it adds on top of good chunking.
- **Day 37 (model selection):** The model you use for HyDE generation affects the quality of the hypothetical document. A model without strong domain knowledge generates weaker hypotheticals.
- **Day 39 (costs):** Every HyDE call adds to your API costs. Factor this into your cost model before enabling it globally.

HyDE is one technique in a layered retrieval stack. Tomorrow: RAPTOR — what to do when even good chunking loses context across sections of a long document.

---

*Day 40 of the RAG Masterclass series. This series builds on the RAG Deep Dive (days 37–39). If you missed those, start there.*
