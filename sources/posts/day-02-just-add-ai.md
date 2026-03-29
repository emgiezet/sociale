---
day: 2
title: "\"Just add AI\" is the new \"just add a database.\" And it's equally dangerous."
pillar: Trenches
format: Hot take
language: English
scheduled_date: 2026-03-24
posting_time: "07:30 CET"
hashtags: ["#AI", "#InsurTech", "#SoftwareEngineering", "#EngineeringLeadership"]
image: ./images/day-02.jpg
image_unsplash_query: "warning sign database technology"
cta: "Agree or disagree? Comments open."
---

"Just add AI" is the new "just add a database." And it's equally dangerous.

I've watched teams bolt AI onto existing products and wonder why it breaks in production. The pattern is familiar. We saw the same thing when NoSQL was going to solve everything, when microservices were going to fix monoliths. New technology, same mistake: skipping the hard questions.

In insurance, the stakes are concrete.

A broker asks our AI: "Is this client covered for flood damage?" A wrong answer, delivered confidently, doesn't just frustrate a user. It creates liability. It can affect a real claim. Regulators in the EU are not impressed by "the model said so" 😬

Here's what "just add AI" ignores in regulated industries:

→ Your training data reflects historical decisions, including wrong ones
→ GDPR requires you to explain automated decisions, and LLMs are not explainable by default
→ Legacy systems weren't designed for AI-readable data formats
→ Insurance products are jurisdiction-specific; a generic model doesn't know Polish law
→ Evaluation is not optional. You need metrics before you ship, not after

We spent 3 months on data preparation before our first RAG system touched production. Not building. Not training. Cleaning, classifying, and auditing what we already had.

Nobody talks about that part. Everyone talks about the demo 🙃

**The technology is not the hard part. The hard part is everything that surrounds it.**

Agree or disagree? Comments open.

#AI #InsurTech #SoftwareEngineering #EngineeringLeadership
