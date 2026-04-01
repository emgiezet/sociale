---
day: 6
title: "Why Your RAG System Breaks When You Scale It: The 4 Problems Nobody Warns You About"
pillar: Builder
language: en
image: ../../images/day-06.jpg
image_unsplash_query: "library books knowledge continuous"
---

# Why Your RAG System Breaks When You Scale It: The 4 Problems Nobody Warns You About

RAG works perfectly for 10 documents. Then you add 5 more and it breaks.

It's not a bug. It's four unsolved problems hitting you at once.

This is a pattern I've seen repeatedly while building RAG systems in production at Insly, where we process insurance documents at scale for 150,000+ users. The YouTube tutorial gets you to working. Production gets you to all four of these.

## Problem 1: Chunking Strategy Falls Apart on Structured Documents

Most tutorials split text every N characters. That's fine for demos. It falls apart on structured documents where a single clause references definitions from three other sections.

The core issue: chunking by token count treats text as a uniform stream. But insurance policy documents — like legal documents, medical records, technical specifications — have internal structure that carries meaning. A clause in section 4 might say "as defined in section 1.3" and "subject to the exclusions in section 12." A chunk containing the section 4 clause, split arbitrarily at 512 tokens, loses both of those references.

The fix isn't smaller chunks. It's smarter ones.

We use several techniques together:

**RAPTOR (Recursive Abstractive Processing Tree Organization for Retrieval)** builds hierarchical summaries of document trees. Instead of only chunking at the leaf level, you also create summary nodes at higher levels of the document hierarchy. A query about water damage coverage can retrieve both the specific clause and the section summary that gives it context.

**Metadata tagging** ensures every chunk knows where it came from: document type, section, parent section, document ID, effective date, issuer. This metadata becomes available for filtering before semantic search runs.

**HyDE (Hypothetical Document Embeddings)** bridges the language gap between how questions are asked and how answers are written. A broker asking "does this cover flood damage?" sounds nothing like the policy clause that answers it. HyDE generates a hypothetical answer document and embeds that for retrieval, rather than embedding the question directly.

This sounds complex. It is complex. But "smart chunking once" is much cheaper than "retrieve wrong chunks forever."

## Problem 2: Vector Search Alone Breaks Down on Similar Documents

As your document corpus grows and documents become more structurally similar, vector representations stop discriminating reliably.

In our insurance context: our OWU (Ogólne Warunki Ubezpieczenia — General Terms and Conditions) files for different carriers share the same overall structure, the same legal boilerplate, the same section headers. The documents are different in the details that matter — specific coverage limits, specific exclusion lists, specific premium calculation rules. But their vectors are close to each other, which means semantic search returns a mix of documents from different carriers rather than reliably returning the right one.

Pure vector search also misses exact terminology matches. A broker asking about "OC komunikacyjne" (motor third-party liability) might not match a document that uses the full phrase "ubezpieczenie odpowiedzialności cywilnej posiadaczy pojazdów mechanicznych" even though they refer to the same thing.

The answer is hybrid retrieval:

→ Dense vector search for semantic similarity and paraphrase matching
→ Sparse keyword search (BM25) for exact term matching and domain-specific terminology
→ A reranking layer that scores candidate chunks from both retrieval paths for actual relevance to the specific query before passing them to the model

Large knowledge graphs add another consideration: without efficient graph traversal and filtering, retrieval latency becomes unacceptable at scale. You need to be able to say "retrieve from documents belonging to carrier X, product line Y, effective in 2024" before the semantic search runs.

## Problem 3: Retrieval Configuration Is a Moving Target

This is where most teams bleed quietly. Your RAG configuration isn't a one-time decision — it's a function of your document count, domain specificity, and query distribution.

What works at 100 documents will fail at 10,000. What works for English-language queries will fail for Polish-language queries. What works for coverage verification questions will fail for complex multi-document comparison queries.

Every parameter needs to be tunable independently and measured continuously:

→ **Chunk overlap**: too little and you lose context at boundaries, too much and you create redundant retrievals that waste context window
→ **Embedding model**: the right model depends on your domain and languages
→ **Top-k**: too low and you miss relevant context, too high and you dilute signal with noise
→ **Similarity threshold**: too permissive and the model hallucinates confidently, too strict and it says "I don't know" too often
→ **Reranking cutoff**: how many candidates do you pass to the reranker, and how many does the reranker return?
→ **Prompt template**: how you frame the retrieved context affects answer quality significantly

None of these parameters has a universally correct value. Each one has a correct range for your specific data, query distribution, and quality requirements. Finding that range requires measurement. Maintaining it requires continuous monitoring.

Configuration isn't set-and-forget.

## Problem 4: Without Evaluation Infrastructure, You're Flying Blind

You can't improve what you can't measure. Most teams have no idea whether their RAG is getting better or worse after each change.

This is the most dangerous failure mode. You make an architectural change — new embedding model, different chunk size, adjusted similarity threshold — and the system feels different but you don't know if it's actually better. So you make another change. And another. And at some point users start complaining about quality problems that you can't trace back to a specific decision.

Build an evaluation dataset before you touch production. This means:

**Ground-truth query-answer pairs**: a representative set of real queries with validated correct answers. For our insurance system, this meant working with licensed underwriters to validate answers against actual policy documents. For our production system, we validated against the KNF Broker Exam dataset — the official Polish Financial Supervisory Authority's licensing exam for insurance brokers. If the RAG passes the exam that licensed brokers take, we can trust it in production.

**Three separate metrics**:
- Retrieval recall: did the right source documents come back?
- Answer faithfulness: did the model stay grounded in what was retrieved?
- Answer correctness: was the final answer actually right?

These three metrics can diverge. You can have good retrieval but poor faithfulness (the model ignores what you gave it). You can have good faithfulness but poor correctness (you retrieved the wrong documents but the model faithfully described them). Measuring all three tells you which layer of the system needs work.

**Automated CI integration**: run your evaluation dataset on every significant change. Set a threshold — for us, a drop of more than 3% in answer accuracy on our test set means we don't ship, no exceptions. This forces the question: is this change actually an improvement or just a different configuration?

## The 90% That Tutorials Skip

YouTube RAG tutorials teach you to build the first 10%: embed documents, store vectors, retrieve on query, generate with LLM. That part is genuinely fast and genuinely impressive.

The other 90% is:
→ Chunking strategy tailored to your document structure
→ Hybrid retrieval with reranking for mixed query types
→ Configuration discipline and continuous monitoring
→ Evaluation infrastructure with ground-truth data from domain experts

None of this is exotic. All of it is necessary. The teams that skip it build demos that impress in presentations and fail in production. The teams that invest in it build systems that users actually trust.
