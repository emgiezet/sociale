---
day: 23
title: "How to evaluate your RAG system's quality without an ML team."
pillar: Educator
format: Tutorial
language: English
scheduled_date: 2026-04-24
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#MachineLearning", "#SoftwareEngineering", "#QualityAssurance"]
image: ./images/day-23.jpg
image_unsplash_query: "data quality metrics dashboard"
cta: Bookmark this — you'll need it
---

How to evaluate your RAG system's quality without an ML team.

After building 3 RAG systems in production — two of which taught us expensive lessons — this is the evaluation framework I wish I'd had on day one. You don't need a data science team. You need a process.

**1. Retrieval precision**

Does your retriever surface the right chunks? Build a test set of 50–100 question/expected-document pairs. Run your retriever and check what percentage of the right documents appear in the top-5 results. Aim for >80% before touching the LLM layer. We wasted two weeks optimizing prompts before realizing our retriever was the actual problem.

**2. Answer faithfulness**

Is the answer grounded in what was retrieved? Use an LLM judge (GPT-4o or Claude) to check whether each answer can be traced back to the retrieved context. Flag anything below 90%. This catches hallucinations that look confident.

**3. Answer relevance**

Does the answer actually address the question? Different from faithfulness — a fully grounded answer can still miss the point. Score on a 1–5 scale. Anything below 3.5 average is a prompt or chunking problem, not a model problem.

**4. Hallucination red lines**

In insurance, certain failure types are catastrophic: wrong coverage amounts, incorrect policy terms, fabricated legal references. We maintain a list of ~30 "canary questions" — questions where any hallucination is a blocker. These run on every deployment.

**5. A/B evaluation before changes**

Never change chunking strategy, retrieval parameters, or prompts without running your full test set on both old and new. Even changes that feel like improvements can break edge cases. We maintain a regression baseline and require net improvement across all four metrics before merging.

**The tooling we use:** custom evaluation scripts in Python, LLM-as-judge via AWS Bedrock, results logged to a simple spreadsheet. You don't need RAGAS or a $50K observability platform to start.

**A RAG system without evaluation is a demo. With evaluation, it becomes a product.**

Bookmark this — you'll need it when your first evaluation reveals your retriever was the bottleneck all along.

#RAG #AI #MachineLearning #SoftwareEngineering #QualityAssurance
