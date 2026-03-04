# Day 7 — Educator: What RAG Tutorials Skip
**Pillar:** Educator | **Week:** 2 | **CTA:** Save

---

## LinkedIn Post

RAG is not just search + LLM.
Here's the part most tutorials skip.

Every RAG tutorial covers:
✓ Embed documents
✓ Store in vector database
✓ Query by semantic similarity
✓ Pass results to LLM

Here's what they don't cover — the part where most production systems fail:

**Chunking strategy is retrieval quality.**
How you split documents is how you define what's retrievable. Too small: context is lost. Too large: signal is diluted. The right chunk size depends on your documents, your queries, and your LLM context window. There's no universal answer. You have to measure.

**Metadata filtering is the other half of retrieval.**
Pure semantic similarity ignores everything you know about your documents. If you know the user is asking about a 2023 policy, you should filter by year before semantic search runs. Metadata filtering reduces your search space and dramatically improves precision. Most tutorials don't build it.

**Retrieval evaluation must come before retrieval optimization.**
You cannot improve what you don't measure. Build a test set of real questions with validated answers from a domain expert. Measure retrieval precision and recall against it. Then optimize. This order matters. Many teams build first and never evaluate at all.

**Hallucination and groundedness are different problems.**
Hallucination = the LLM makes something up. Groundedness = the answer is supported by what was retrieved. You can have a grounded answer that's still wrong (if retrieval was wrong). You can have an ungrounded answer that happens to be correct (lucky hallucination). Measure both separately.

**Re-ranking changes everything.**
A cross-encoder re-ranker that scores retrieved passages for relevance to the query can take your retrieval from 70% to 85%+ quality with no changes to your embedding model or vector store. It's one of the highest-leverage improvements in the RAG stack.

**These aren't advanced topics. They're prerequisites for a system that actually works in production.**

Save this. Share it with whoever just started their first RAG project.

#RAG #AIEngineering #LLM #AWSBedrock #ProductionAI

---

## Blog Post

### The RAG Stack Nobody Talks About: What Separates Demos from Production Systems

If you've followed any "build a RAG system in 30 minutes" tutorial, you know the architecture: embed documents, store vectors, query by similarity, generate with an LLM. This architecture works. For demos.

Production RAG systems — the ones that handle real queries, from real users, in domains where wrong answers have consequences — require a deeper stack. Here are the components that most tutorials skip, and why each one matters.

#### Component 1: Chunking Strategy

When you split a document into chunks for embedding, you're making a foundational decision about what information is retrievable. Too small, and individual chunks lose the context needed to answer a question. Too large, and the semantic signal is diluted — a 2,000-token chunk about policy terms might match a query about claims procedure simply because both topics appear in the same section.

The right chunking strategy depends on three things: the structure of your source documents, the nature of your queries, and the context window of your LLM.

For insurance documents at Insly, we tested chunk sizes from 200 to 1,200 tokens. We tested overlapping chunks (where adjacent chunks share a fixed number of tokens to preserve context at boundaries). We tested semantic chunking (splitting on sentence or paragraph boundaries rather than fixed token counts). We tested hierarchical chunking (preserving section and subsection relationships in the metadata).

What we learned: there is no universal answer. The optimal strategy depends on your data. The only way to find it is to measure retrieval quality under different strategies against a real evaluation set.

This is why chunking strategy and evaluation infrastructure need to be built together. You can't evaluate chunking choices without a way to measure retrieval quality, and you can't measure retrieval quality without a consistent chunking baseline.

#### Component 2: Metadata Filtering

Semantic similarity search finds chunks that are semantically close to the query. It doesn't use the structured information you have about your documents — when they were created, which product they describe, which jurisdiction they cover, which version they represent.

Metadata filtering is the ability to constrain your semantic search using this structured information. Before running the embedding similarity calculation, you filter down to the relevant subset of documents. This has two effects: it reduces your search space (which improves latency and cost) and it prevents semantically similar but contextually irrelevant documents from being retrieved.

At Insly, we tag every document chunk with metadata: document type, product line, issuing jurisdiction, effective date range, amendment status. When a user query has clear metadata signals ("2023 residential policy in Poland"), we filter before we search. This alone improved retrieval precision by roughly 15 percentage points on our evaluation set.

This seems obvious in retrospect. It wasn't obvious when we started.

#### Component 3: Retrieval Evaluation Infrastructure

This is the component that most tutorials skip entirely — and the one that matters most for production deployment.

You cannot improve what you don't measure. And in a RAG system, "improvement" isn't self-evident. Is this retrieval result better than that one? You need a standard to measure against.

An evaluation set for RAG consists of: a collection of realistic questions, the expected retrieved passages for each question, and the expected answers for each question. The questions and expected passages should be validated by a domain expert — someone who actually knows what the right answer looks like.

With an evaluation set in place, you can measure:
→ Retrieval precision: of the passages retrieved, what fraction are relevant?
→ Retrieval recall: of the relevant passages in your corpus, what fraction are retrieved?
→ Answer faithfulness: is the generated answer supported by the retrieved passages?
→ Answer relevance: does the answer address the question that was asked?

Each of these metrics can be tracked independently and can guide specific optimizations. Without them, you're guessing about quality and making architectural changes in the dark.

Build your evaluation set before you optimize anything. Every optimization you make should be validated against it.

#### Component 4: Re-ranking

A bi-encoder retrieval system — the standard vector similarity search — is fast but imprecise. It encodes queries and passages independently, which means it can't directly model the interaction between a specific query and a specific passage.

A cross-encoder re-ranker fixes this. It takes each retrieved passage and the query together, and produces a relevance score that explicitly models their relationship. This is much slower than bi-encoder retrieval, which is why it's used as a second stage: retrieve a larger candidate set with fast bi-encoder retrieval, then re-rank with a cross-encoder and return only the top results.

The quality improvement from adding re-ranking to a baseline retrieval system is typically 10–20 percentage points. It's one of the highest-leverage improvements in the RAG stack, and it requires no changes to your embedding model or vector store.

For our insurance document system, adding a cross-encoder re-ranking step (using a model fine-tuned on insurance text) was the single change that moved our retrieval quality from 72% to 85% before we introduced LightRAG's graph-based retrieval.

#### Component 5: Groundedness vs. Hallucination

These are related but distinct problems, and conflating them leads to solutions that address the wrong thing.

Hallucination is when an LLM generates content that isn't present anywhere in its context. The model invents a policy clause, a statistic, a company name. This is a generation problem.

Groundedness is whether the generated answer is supported by the retrieved passages. An answer can be grounded but wrong (if retrieval returned the wrong passages). An answer can be ungrounded but accidentally correct (if the model's parametric knowledge happens to be accurate). Measuring groundedness independently from factual accuracy helps you distinguish retrieval failures from generation failures.

Tools like RAGAS (RAG Assessment) provide automated metrics for groundedness and answer faithfulness. They're not perfect — automated metrics can miss nuanced errors — but they're a necessary component of evaluation at scale.

#### Putting It Together

These five components aren't advanced optimizations for mature systems. They're prerequisites for a system you can trust in production. The teams I've seen succeed with RAG built evaluation infrastructure first, optimized retrieval second, and treated generation as the last thing to tune.

The teams I've seen fail built the prettiest demo first and discovered quality problems when real users found them.

Save this as a checklist for your next RAG project. And if you're working through any of these specific challenges — chunking strategy, evaluation design, re-ranking implementation — let me know in the comments. I've hit every one of these problems in production and I'm glad to share what worked.
