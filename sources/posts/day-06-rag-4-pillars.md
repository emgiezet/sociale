---
day: 6
title: "RAG works perfectly for 10 documents. Then you add 5 more and it breaks. Here's why."
pillar: Builder
format: Technical
language: English
scheduled_date: 2026-03-30
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#SoftwareEngineering", "#InsurTech"]
image: ./images/day-06.jpg
image_unsplash_url: "https://unsplash.com/photos/kMmzEYfkwBw"
image_unsplash_author: "Kimberly Farmer"
image_unsplash_query: "library books knowledge continuous"
cta: Repost if your team is scaling a RAG system.
---

RAG works perfectly for 10 documents. Then you add 5 more and it breaks.

It's not a bug. It's four unsolved problems hitting you at once.

**1. Chunking**
Most tutorials split text every N characters. That's fine for demos. It falls apart on structured documents where a single clause references definitions from three other sections.

The fix isn't smaller chunks — it's smarter ones. We use RAPTOR for hierarchical summarization across document trees, metadata tagging so every chunk knows where it came from, and HyDE (Hypothetical Document Embeddings) to bridge the gap between how questions are asked and how answers are written. A broker asking "does this cover flood damage?" sounds nothing like the policy clause that answers it.

**2. Context Management and Search**
Vector search alone breaks down as your corpus grows. When your documents are structurally similar — same format, same terminology, different details — vectors stop discriminating reliably.

The answer is hybrid retrieval: vector search for semantic similarity, keyword search for precision on specific terms, and a reranking layer that scores candidate chunks before they reach the model. Large knowledge graphs add another layer: without efficient graph traversal, retrieval latency becomes unacceptable at scale.

**3. Retrieval Configuration**
This is where most teams bleed quietly. Top-k too low and you miss relevant context. Too high and you dilute the signal with noise. Similarity thresholds set too permissive and the model hallucinates confidently. Context window mismanagement means the most relevant chunks get buried.

Configuration isn't set-and-forget. It's a function of your document count, domain specificity, and query distribution. What works at 100 documents will fail at 10,000. Every parameter — chunk overlap, embedding model, top-k, reranking cutoff, prompt template — needs to be tunable independently and measured continuously.

**4. Benchmarking and Evaluation**
You can't improve what you can't measure. Most teams have no idea if their RAG is getting better or worse after each change.

Build an evaluation dataset before you touch production. Define ground-truth answers for a representative set of queries. Measure retrieval recall (did the right chunks come back?), answer faithfulness (did the model stay grounded?), and answer correctness (was it actually right?). Automate this in CI. We validated ours against a formal KNF Broker Exam dataset — the official Polish financial regulator's licensing exam — and used it as our benchmark. If the RAG passes the exam, brokers can trust it.

**YouTube RAG tutorials teach you to build the first 10%. The other 90% is chunking strategy, hybrid retrieval, configuration discipline, and relentless evaluation.**

Repost if your team is scaling a RAG system.

#RAG #AI #SoftwareEngineering #InsurTech
