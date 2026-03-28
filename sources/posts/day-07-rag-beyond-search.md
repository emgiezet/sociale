---
day: 7
title: "RAG is not just search + LLM. Here's the part most tutorials skip."
pillar: Educator
format: Educational
language: English
scheduled_date: 2026-03-31
posting_time: "07:30 CET"
hashtags: ["#RAG", "#AI", "#MachineLearning", "#SoftwareEngineering"]
image: ./images/day-07.jpg
image_unsplash_query: "search pipeline architecture"
cta: Save this and send it to your AI team.
---

RAG is not just search + LLM. Here's the part most tutorials skip.

Every RAG tutorial shows you the same diagram: embed your documents, store vectors, retrieve on query, pass to LLM, done. That diagram is correct. It is also dangerously incomplete.

**The evaluation layer is where RAG systems actually live or die.**

Here's what I mean, from building 3 of these in production:

**Retrieval quality is a separate problem from generation quality.**
You need to measure them independently. A retrieval that returns the top 5 wrong chunks will produce confidently wrong answers no matter how good your model is. We track retrieval recall and precision separately from answer quality. If retrieval degrades, we know before users notice.

**Reranking matters more than most people think.**
Raw vector similarity retrieves semantically similar text — not necessarily the most relevant text for answering a specific question. We added a cross-encoder reranker after the initial retrieval step. It added latency (about 200ms), but answer accuracy improved enough to justify it. For insurance queries, accuracy beats speed.

**Chunking strategy is more important than model choice.**
I've seen teams spend weeks evaluating GPT-4 vs Claude vs Gemini while their chunking splits policy clauses in the middle of a sentence. Fix your chunking. The model matters less than you think at this stage.

**You need a labeled evaluation dataset before you ship.**
Not after. Before. Ours has 200 broker questions with expected answers, pulled from real support tickets. We run it on every major change. If accuracy drops more than 3%, we don't ship.

**RAG is an engineering system, not a prompt. Treat it like one.**

Save this and send it to your AI team.

#RAG #AI #MachineLearning #SoftwareEngineering
