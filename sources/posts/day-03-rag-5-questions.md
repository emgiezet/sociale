---
day: 3
title: "Before you build your first RAG system, answer these 5 questions."
pillar: Educator
format: Checklist
language: English
scheduled_date: 2026-03-25
posting_time: "07:30 CET"
hashtags: ["#RAG", "#AI", "#SoftwareEngineering", "#MachineLearning"]
image: ./images/day-03.jpg
image_unsplash_query: "checklist planning document"
cta: Save this for your next project
---

Before you build your first RAG system, answer these 5 questions.

I've built 3 RAG systems in production. The first two had answers to some of these. The third had answers to all of them. Guess which one is still running.

**1. What is the actual quality of your source data?**
Not "is it stored somewhere" — is it consistent, structured, complete? In insurance, we have policy documents from 15 years ago in 4 different formats. PDFs with scanned text. Excel sheets converted to CSV. Quality problems upstream become retrieval failures downstream, guaranteed.

**2. What is your chunking strategy and why?**
Most tutorials chunk by token count. That's fine for generic text. Insurance clauses have legal context — split one in the wrong place and the retrieved chunk means something different. We chunk by section boundary, not by character count.

**3. What's the split between retrieval precision and generation quality?**
If your retrieval returns irrelevant chunks, no model will save you. We spent more time tuning retrieval than we did on prompts. Measure both separately.

**4. How will you evaluate this system before users touch it?**
You need a test set of real questions with expected answers. "It seems to work" is not an evaluation strategy. We built 200 labeled Q&A pairs from real broker queries before shipping anything.

**5. What are your compliance constraints?**
GDPR. Data residency. Audit logs. Explainability requirements. These are not afterthoughts in regulated industries. Build them into the architecture on day one.

**Most RAG failures I've seen could have been avoided by answering these questions before writing a single line of code.**

Save this for your next project.

#RAG #AI #SoftwareEngineering #MachineLearning
