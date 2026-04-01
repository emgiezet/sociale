---
day: 5
title: "Three RAG Prototypes, Three Lessons, One System That Works"
pillar: Builder
language: en
image: ../../images/day-05.jpg
image_unsplash_query: "prototype testing laboratory"
---

# Three RAG Prototypes, Three Lessons, One System That Works

Building a production RAG system is not a single decision. It's a sequence of experiments, each one revealing a problem the previous prototype couldn't solve.

At Insly, we spent twelve months iterating through multiple substantively different RAG architectures before we had a system we trusted enough to put in front of real users. Here's what each prototype taught us — and the single most important lesson that connects all of them.

## The Question We Were Trying to Answer

All of our prototypes were built to answer the same question: can insurance brokers query our knowledge base in plain language and get accurate, auditable answers?

The user is a licensed broker. The question might be "what does this policy cover for flood damage?" or "which exclusions apply to commercial vehicle liability for this client?" The answer needs to be precise — in insurance, an approximate answer delivered confidently is worse than saying "I don't know."

We also have a strict compliance requirement: every answer must be traceable to a specific source document. "The AI said so" is not an acceptable answer to a regulator or to a broker defending a claim decision.

With that context, here's what we learned from each prototype.

## Prototype 1: Standard Vector Search on AWS Bedrock

The canonical RAG tutorial suggests a straightforward architecture: embed your documents into a vector store, embed the user query, retrieve the top-k most similar chunks, and pass them to your LLM for generation.

We built this on AWS Bedrock Knowledge Bases. The setup was fast — days rather than weeks. The demo was impressive. Brokers could ask questions in natural language and get relevant-sounding answers drawn from real policy documents.

The production numbers told a different story. On our evaluation set — real questions from broker support tickets — retrieval quality was around 60%. Meaning four out of ten questions returned an answer based on the wrong document section, or retrieved relevant text but missed the critical context.

The root cause: insurance policy documents are hierarchically structured and cross-referenced. A clause about water damage coverage might say "subject to the exclusions listed in section 12.3." Semantic similarity search retrieves the coverage clause. It doesn't retrieve section 12.3 unless it's also semantically similar to the query — which it often isn't.

Off-the-shelf embeddings trained on general text also underperform on specialized domain terminology. Brokers use industry-specific jargon. The model didn't consistently match it.

Lesson: flat vector search doesn't understand document structure. Off-the-shelf embeddings don't understand specialized domains.

## Prototype 2: Fine-Tuned Embeddings and Hybrid Search

We attacked both problems from prototype 1. We fine-tuned our embedding model on insurance documents to better capture domain terminology. We added BM25 keyword search alongside vector search to improve exact terminology matching.

Retrieval quality improved — we got to approximately 72% on our evaluation set. Meaningful progress.

But two new problems emerged.

First, keyword matching helped with terminology but didn't solve the structural problem. We were still retrieving semantically relevant chunks that lacked the relational context needed for accurate answers. A clause about liability coverage is semantically similar to a query about liability coverage. But if the actual answer depends on an endorsement added six months later, and that endorsement uses different language, hybrid search doesn't connect them.

Second, we were hitting context limits. With hybrid retrieval returning more candidate chunks, we were passing more text to the LLM, which made answers longer, more expensive, and in some cases less focused.

Lesson: quantity of retrieved context is not quality of retrieved context. And domain fine-tuning helps, but doesn't solve structural problems.

## Prototype 3: Graph-Based Retrieval with LightRAG

LightRAG builds a knowledge graph from your documents — extracting entities and the relationships between them, not just the raw text. The intuition: documents reference other documents, clauses reference other clauses, and a policy amendment might override a condition in the base policy. Modeling these relationships explicitly should improve retrieval for queries that depend on connected information.

In theory, this was exactly the right approach.

In practice, we hit a problem specific to our domain. Our insurance documents and General Terms and Conditions (GTC) files are structurally and linguistically similar — same format, same terminology, different details for different carriers. In this environment, vector representations became equally good and equally bad at distinguishing between documents. LightRAG's graph traversal couldn't reliably determine which carrier's context was relevant for a given query.

More critically: LightRAG had no built-in way to filter context by company name, product line, or risk type. In insurance, this is not optional. A broker asking about liability coverage for one carrier cannot receive context that bleeds in from another carrier's documents. Every answer must be auditable and attributable.

We couldn't make LightRAG satisfy this requirement without rebuilding significant parts of it — at which point we were better off building from scratch.

Lesson: knowledge graphs don't solve filtering. If your domain requires strict context scoping, graph retrieval can make the problem worse.

## Prototype 4: Intent-Based Routing, Built From Scratch

We scrapped the black-box approaches and built from scratch in Python. The insight that drove this decision came from looking at the actual queries brokers were sending.

Brokers don't ask random questions. The question distribution is concentrated. We analyzed a corpus of broker queries and identified 11 distinct user intentions: coverage verification, exclusion lookup, liability limits, claims procedure, premium calculation, amendment history, and several others. Each intention maps to a different retrieval strategy — some need exact clause lookup, some need cross-document comparison, some need structured data lookup rather than semantic search.

The right retrieval strategy applied per intention. Everything filterable by company, product line, and risk type. Everything auditable with source attribution.

We validated the system against a dataset we extracted from the KNF Broker Exam — the official Polish Financial Supervisory Authority's licensing exam for insurance brokers. If our system can pass the exam that licensed brokers take, we can trust it in production. It passed with strong scores.

The retrieval architecture matters more than the model. We used AWS Bedrock Claude throughout. Same model, same generation quality. What changed was the quality of what we gave it to work with.

## What I'd Tell Myself at the Start

The right RAG architecture depends entirely on your data structure and compliance requirements, not on what was trending when you started the project.

Before you build anything, ask:
→ What are the structural relationships in my data that semantic similarity won't capture?
→ What are my filtering requirements, and can my retrieval architecture enforce them?
→ What does "correct" mean for my specific use case, and how will I measure it?
→ What are my audit and attribution requirements?

These questions would have saved us months. They're the starting point for any honest RAG architecture decision.
