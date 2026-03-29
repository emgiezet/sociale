---
day: 10
title: "I use a 3-question framework before starting any AI project. It's saved me months."
pillar: Educator
format: Framework
language: English
scheduled_date: 2026-04-03
posting_time: "08:00 CET"
hashtags: ["#AI", "#SoftwareEngineering", "#EngineeringLeadership", "#RAG"]
image: ./images/day-10.jpg
image_unsplash_query: "decision framework whiteboard"
cta: "DM me 'framework' for the full template."
---

I use a 3-question framework before starting any AI project. It's saved me months.

After building 3 RAG systems in production and watching one of them fail expensively, I started forcing myself to answer these three questions before writing a single line of code. Every time I've skipped one, I've regretted it 🫠

**Question 1: Is this a retrieval problem or a generation problem?**

Most "AI" requests are actually retrieval problems in disguise. A broker asking "what does this policy cover?" doesn't need a creative answer. They need the exact text from the right document, surfaced fast. That's retrieval. Solving it with a generative model adds complexity, latency, and hallucination risk without adding value.

If the answer exists in your data and just needs to be found: optimize retrieval.
If the answer needs to be synthesized from multiple sources: then you need generation.

Getting this wrong costs you months.

**Question 2: What is the compliance boundary?**

In insurance, this question has teeth. Before we build anything, we map:
→ What data does this system touch?
→ Where does that data live, and can it leave that jurisdiction?
→ Do automated decisions using this system require explainability under EU law?
→ What's the audit trail requirement?

If you can't answer these before you start, your architecture will change under you halfway through. I've seen that happen. It's not a good sprint review 😅

**Question 3: Can we evaluate this before it ships?**

Not "can we test it," but can we measure whether it's actually good enough? This means defining what "good enough" looks like in advance: precision thresholds, recall targets, latency budgets, error rate limits.

For our production RAG system, "good enough" meant: >85% retrieval precision on our 200-question labeled test set, <2 seconds response time at p95, zero answers citing sources that don't exist.

If you can't define evaluation criteria before building, you're not ready to build.

**These three questions won't guarantee a successful AI project. But skipping any one of them will almost guarantee a painful one.**

DM me 'framework' for the full template.

#AI #SoftwareEngineering #EngineeringLeadership #RAG
