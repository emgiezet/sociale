---
day: 5
title: "We built 4 RAG prototypes in 12 months. Here's what actually worked (and what didn't)."
pillar: Builder
format: Technical
language: English
scheduled_date: 2026-03-27
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AWS", "#AI", "#InsurTech", "#SoftwareEngineering"]
image: ./images/day-05.jpg
image_unsplash_query: "prototype testing laboratory"
cta: Repost if your team is evaluating RAG approaches.
---

We built 4 RAG prototypes in 12 months. Here's what actually worked (and what didn't).

All four were built to answer the same question: can brokers query our insurance knowledge base in plain language and get accurate, auditable answers?

**Prototype 1: Naive RAG on AWS Bedrock**
Simple embedding + vector search + Claude. Took 2 weeks to build, 2 months to realize it wasn't good enough 😅 The problem: retrieval recall was too low on domain-specific insurance terminology. Brokers use jargon. The model didn't consistently match it. We'd get confident wrong answers, which in insurance is worse than no answer.

Lesson: off-the-shelf embeddings trained on general text underperform on specialized domains.

**Prototype 2: Fine-tuned embeddings + AWS Bedrock**
We fine-tuned the embedding model on insurance documents. Retrieval quality improved significantly. But we hit a different wall: the knowledge graph between policy documents, endorsements, and conditions was implicit. Standard chunk retrieval couldn't follow it. A clause in one document depends on definitions from another. Flat vector search doesn't know that.

Lesson: if your domain has deep relational context, vector search alone isn't enough.

**Prototype 3: LightRAG**
LightRAG builds a knowledge graph on top of the document corpus. It explicitly models entity relationships. Promising in theory, but it never made it to production.

The problem: our industry-specific docs and GTC files are structurally and linguistically similar. Vectors became equally good and equally bad at distinguishing them. More importantly, LightRAG had no way to filter context by company name, product line, or risk type. In insurance, that's not optional. A broker asking about liability coverage for one carrier cannot get context bleed from another. We couldn't make it auditable.

Lesson: knowledge graphs don't solve filtering. If your domain requires strict context scoping, graph retrieval can make the problem worse.

**Prototype 4: 100% in-house Python, intent-based routing**
We scrapped the black-box approaches and built from scratch in Python. The core insight: brokers don't ask random questions. We identified 11 distinct user intentions and built explicit detection for each. The right retrieval strategy is applied per intent. Everything is filterable by company, product line, and risk type. Everything is auditable.

Proof: we extracted a large KNF Broker Exam dataset, the official Polish financial regulator's exam for licensed brokers, and our system passed it with flying colours 🎓

**The right RAG architecture depends entirely on your data structure and compliance requirements, not on what was trending when you started the project.**

Repost if your team is evaluating RAG approaches.

#RAG #AWS #AI #InsurTech #SoftwareEngineering
