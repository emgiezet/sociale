---
day: 25
title: "What I'm Presenting at DevAI and Why It's Not a Typical AI Talk"
pillar: Educator
language: en
image: ../../images/day-25.jpg
image_unsplash_query: "conference speaker stage technology"
---

# What I'm Presenting at DevAI and Why It's Not a Typical AI Talk

When I accept a speaking invitation at a technical conference, I ask myself one question first: "What can I say that the audience can't find in any Medium article?"

AI presentations tend to fall into two categories. Too academic: elegant theory without production context, papers that explain how things should work without acknowledging how they actually work. Or too demo-centric: impressive demos that show the happy path, zero information about what happens after you leave the stage when real users start using the system in unexpected ways.

I try to find a third path: a detailed field report. This is what we actually built. Here is what broke. Here is what we changed and why. Here is what works in production with 150,000 documents per month processed by AI and full compliance obligations, and what only worked in staging.

## What I'll Be Covering at DevAI by DSS

At DevAI by DSS, I'll present the evolution of our RAG architecture at Insly — not as a success story, but as a sequence of production problems and the architectural decisions that followed from each of them.

**Stage 1: AWS Bedrock Knowledge Bases**

We started with AWS Bedrock Knowledge Bases because it was the fastest path to something working. The demo looked good. The retrieval quality on our production data set: approximately 60% on our evaluation test set.

60% sounds OK until you think about what it means in practice. Forty percent of the time, the system retrieved passages that weren't the most relevant to the question. When you're building something for insurance document retrieval — where the difference between the right clause and the wrong clause can have real implications — 60% is not a production number.

**Stage 2: Hybrid Search**

We added BM25 keyword search alongside semantic search. The combination improved quality to approximately 72%. Better. Still not enough for our use case.

The problem: retrieval was still flat. It treated every document as an independent unit and retrieved based on similarity to the query. But insurance documents have relationships — a policy clause references an exclusion that references a definition that references a regulatory standard. Flat retrieval doesn't see these relationships. It retrieves fragments without context about how they connect.

**Stage 3: LightRAG**

We modeled documents as a graph of entities and relationships. Each policy clause, each definition, each cross-reference became a node or an edge in the graph. Retrieval became traversal of this graph, not just similarity search.

Retrieval quality on questions that required understanding cross-document relationships: approximately 89%. The cost: significantly higher operational overhead. Graph construction, maintenance, and query processing are more complex than vector similarity search.

**The lesson that connects all three stages:** Every architectural change was driven by measurement. We built our evaluation framework first, established a quality baseline, and only changed the architecture when measurements showed we'd hit a quality ceiling. This is evolution driven by measurement, not speculation — and it's the central message I'll deliver at DevAI.

## Why Insurance Is an Important Context

AI presentations often treat domain as interchangeable or ignore it entirely. "Here's our RAG system — it works for any kind of document." This is understandable in an academic context. It's misleading in a practical one.

In insurance, domain is not interchangeable. It shapes every architectural decision.

An error in a product recommendation system produces poor UX. An error in interpreting an insurance clause could produce a wrongful claims decision. This changes everything: the required accuracy level (89% isn't sufficient in all contexts — some claims decisions require 99%+ confidence or human review), the fallback architecture (we need human escalation paths, not just "try again"), the audit trail requirements (we need to log what was retrieved, what context was provided, what the model produced), and the human oversight criteria (which decisions can AI support, and which require underwriter sign-off).

I believe regulated industries — insurance, finance, law, healthcare — are the best training ground for production AI. If something works here, it works anywhere. If it only works in an environment without compliance obligations, it's not production AI. It's a demo.

## The Human Dimension Nobody Talks About

Technical presentations about AI rarely address the organizational and human dimensions of AI transformation. At DevAI, I'll spend explicit time on this.

Leading a 15-person team through 18 months of AI transformation has taught me things that no paper or tutorial covers.

How experienced engineers respond to being beginners again. Senior developers who have been expert in their domain for years don't enjoy suddenly being the least-knowledgeable person in the room. AI transformation creates that situation repeatedly. The engineers who had the most Symfony and PHP experience were suddenly in learning mode alongside engineers who were newer to the team but more comfortable with Python and ML tooling. Managing this dynamic — building psychological safety for "I don't know yet," rewarding learning behaviors as much as shipping behaviors — was as much of the job as any technical architecture decision.

How to build shared context in a domain that changes weekly. The AI tooling landscape changes fast. LightRAG wasn't our initial plan — it emerged as the right answer after we'd learned enough from the previous stages. Building shared context in a fast-changing domain requires different practices than building shared context in a stable domain.

This is part of the story of building production AI that nobody talks about. At DevAI, I'll talk about it.

## The Three Questions I'll Ask the Audience

Before I present our architecture evolution, I'm going to ask the audience three questions. I want to know where people actually are, not where they think they should be.

**Question 1: Is vibecoding a tool or a substitute for understanding?**

My position: AI-assisted coding is powerful, and dangerous precisely when the generated code looks correct and you don't understand why it works. In regulated industries, "looks correct" is not sufficient. I want to hear from engineers who have navigated this already.

**Question 2: How many RAG systems in your organization are genuinely in production versus PoC renamed as production?**

I've built 3 RAG systems. Two were expensive lessons. One is in production with real users today. The gap between PoC and production is larger than most teams admit publicly.

**Question 3: When did your team last say "we won't deploy this because we don't yet know how to evaluate it"?**

Evaluation is the most frequently skipped step in AI projects. I ask this because I want to know whether this is just my problem or an industry standard.

## For Whom

This talk is for developers who've built their first RAG demo and are wondering what comes next — what the gap is between a demo that works and a system that's production-ready for real users with real consequences.

For tech leads guiding their teams through AI transformation and looking for someone who understands the organizational side, not just the technical architecture.

For engineers in regulated industries — banking, healthcare, legal, insurance — who think AI "can't work in their domain." I want to show them it can, and what it actually takes.

If you'll be at DevAI, find me before or after the talk. I'd love to compare notes and hear what you're building.

If you won't be there, the content from this talk will be incorporated into the "Agentic AI Developer" course launching this spring. Leave a comment below or send me a message if you want to be on the waitlist.
