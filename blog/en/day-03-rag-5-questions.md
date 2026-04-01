---
day: 3
title: "The 5 Questions That Separate Good RAG Systems from Expensive Mistakes"
pillar: Educator
language: en
image: ../../images/day-03.jpg
image_unsplash_query: "checklist planning document"
---

# The 5 Questions That Separate Good RAG Systems from Expensive Mistakes

If you search "how to build a RAG system," you'll find hundreds of tutorials. Most of them will have you set up a vector store, embed some documents, and run your first query within 30 minutes.

The tutorial will work. Your production system probably won't — not without answers to the five questions I'm about to give you.

I've built three RAG systems at Insly, an insurance platform with 150,000+ users. The first was built fast without asking these questions. The second incorporated some of them. The third, which is now in production, started from a clear answer to all five. The difference in outcome was not subtle.

## Question 1: What Is the Actual User Question?

This sounds obvious. It's not.

"We want our documents to be searchable by AI" is not a user question. It's a product vision. And building a RAG system to fulfill a product vision, rather than to answer a specific question, leads to systems that are architecturally overfit for the general case and practically underfit for the real one.

Before you build anything, sit with a real user — an actual person who will use the system — and ask them to show you the question they most need answered. Not the most interesting question. Not the most impressive one. The most common one. The one that, if answered reliably, would save them time every single day.

For Insly's underwriting team, that question was specific and narrow: given this policy document, what coverage applies to this type of incident? Everything we built was tuned to answer that question well.

Start there. Generalize later.

## Question 2: What Shape Is Your Data In?

The single most underestimated challenge in building enterprise RAG systems is data preparation. Tutorials use clean PDFs. Real enterprise data is a different story.

At Insly, we have documents in multiple formats, multiple languages, varying quality levels (some scanned from paper, some generated programmatically), and spanning different schema conventions across brokers and countries. Before we could embed anything useful, we needed to:

→ Extract text from multiple formats reliably (PDF, DOCX, HTML, scanned images via OCR)
→ Normalize language and terminology differences
→ Handle document structure — headers, tables, footnotes — in ways that preserved semantic meaning
→ Identify and tag metadata (document type, date, issuer, jurisdiction) that we'd need for filtered retrieval

This work took weeks. It showed up nowhere in a demo. And it was the foundation everything else rested on.

Be honest with yourself about what you're dealing with before you write a single line of retrieval code. In insurance, we have policy documents spanning 15 years in 4 different formats. PDFs with scanned text. Excel sheets converted to CSV. Quality problems upstream become retrieval failures downstream — guaranteed.

## Question 3: What Does "Correct" Look Like?

This is the question that separates systems that work from systems that seem to work.

A RAG system that returns a fluent, confident, well-formatted wrong answer is worse than one that says "I don't know." The fluent wrong answer gets used. It affects decisions. It builds misplaced trust in the system.

To build a good RAG system, you need to define ground truth. What does a correct answer look like? Who in the business has the domain knowledge to evaluate answer quality? What percentage of answers need to be correct before this goes to production?

These aren't questions your ML framework will answer for you. They require involvement from domain experts — in our case, experienced underwriters who could review system outputs and tell us when the answer was technically present in the retrieved document but contextually misleading.

Build your evaluation infrastructure before you build your retrieval pipeline. The evaluation data you create in this step will be the most valuable artifact of your entire project. We built 200 labeled Q&A pairs from real broker queries before shipping anything.

## Question 4: What Happens When It's Wrong?

Every system will be wrong sometimes. The relevant design question is: what's the blast radius?

In a recipe recommendation app, a wrong answer is mildly annoying. In insurance, a wrong answer can affect a claim decision, expose the company to regulatory risk, and damage a customer relationship.

Design your error handling before you're in production. This means:

→ Explicitly deciding which use cases the system should decline to answer (and returning a graceful "I don't know" rather than a confident wrong answer)
→ Building a human review loop for answers above a certain risk threshold
→ Logging not just system errors but answer quality signals so you can identify degradation over time
→ Defining a rollback strategy if the system's quality drops below your threshold

These aren't advanced features. They're table stakes for production deployment in any domain where errors have consequences.

## Question 5: What Metric Are You Actually Optimizing?

RAG systems have multiple quality dimensions that don't all move in the same direction:

→ Retrieval precision (are the right documents being retrieved?)
→ Answer faithfulness (is the answer grounded in what was retrieved?)
→ Answer relevance (does the answer address the question?)
→ Latency (how long does it take?)
→ Cost (how much does each query cost at scale?)
→ Compliance constraints (GDPR, data residency, audit logs, explainability)

You cannot optimize all of these at once, especially in your first iteration. Pick one. Usually it's answer faithfulness — the most important signal that your system is grounded and not hallucinating.

Be explicit about what you're optimizing and what tradeoffs you're accepting. Write it down. Put it in your project brief. Refer back to it when you're tempted to add complexity.

In regulated industries, compliance isn't optional. Data residency, GDPR explainability requirements, and audit trail requirements need to be baked into the architecture on day one — not retrofitted later when a regulator asks.

## The Meta-Lesson

These five questions don't slow you down. They change what you build. The teams that skip them build fast and then rebuild slowly — because what they shipped isn't solving the right problem or isn't trustworthy enough to use.

The teams that start with these questions build something narrower, simpler, and more useful on the first attempt. Then they expand from there.

Save this. Share it with the person who hands you a pile of documents and says "just make it searchable." These questions are the start of an honest conversation about what you're actually building — and what it will take to build it right.
