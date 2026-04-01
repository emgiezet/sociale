---
day: 2
title: "\"Just Add AI\" Is the Worst Advice in Tech Right Now"
pillar: Trenches
language: en
image: ../../images/day-02.jpg
image_unsplash_query: "warning sign database technology"
---

# "Just Add AI" Is the Worst Advice in Tech Right Now

I've heard it in product meetings, in Slack messages from executives, in conference Q&As. The phrase that's become the 2026 equivalent of "we just need to put it on the blockchain."

"Can't we just add AI to this?"

Let me be direct: this framing is causing real damage to real projects. And having built AI systems in production at Insly — an insurance platform with 150,000+ users and serious compliance obligations — I've seen how this mindset plays out when it meets reality.

## The Historical Pattern

"Just add AI" has predecessors. In the early database era, non-technical stakeholders believed that once you had a database, insight would follow automatically. The data was the hard part. Storing it would unlock the value.

What we learned: the database was the easy part. Schema design, query optimization, reporting layers, data quality — that was the work.

The same pattern played out with microservices ("just split it into services"), with NoSQL ("just use MongoDB"), and with cloud migration ("just move it to AWS"). Each time, a genuinely powerful technology got sold as a simple addition when it was actually a deep architectural commitment.

AI is following the same arc, but faster. The hype cycle has compressed. The expectations have gotten further from reality. And the "just add" crowd is louder than ever because the demos are genuinely impressive.

## What "Just Add AI" Actually Requires

When someone asks me "how long to add AI to X," here's the real answer they need to hear:

**Data preparation takes longer than you think.** LLMs are powerful, but they're only as good as what you give them. If your data is unstructured, inconsistently formatted, multilingual, or scattered across legacy systems — which describes most enterprise data — preparation can take weeks before you write a single line of AI code.

At Insly, our insurance documents are stored in multiple formats, written in multiple languages, with varying structure by broker and country. Before we could build anything useful, we spent weeks just on chunking strategies and normalization. Three months of data preparation before our first RAG system touched production. Not building. Not training. Cleaning, classifying, and auditing what we already had.

**Retrieval quality requires its own engineering discipline.** RAG is the dominant pattern for enterprise AI right now, and it has a deceptive surface simplicity: you embed your documents, embed your query, and find the closest match. In practice, retrieval quality at production scale requires careful attention to embedding models, chunk overlap strategies, metadata filtering, hybrid search approaches, and re-ranking logic. Each of these is its own optimization problem.

**Evaluation infrastructure is not optional.** This is the one that kills projects most often. Traditional software has deterministic tests: given input X, expect output Y. AI systems produce probabilistic outputs. You need evaluation frameworks that can measure whether outputs are grounded, accurate, helpful, and consistent. Building this infrastructure isn't glamorous, but skipping it means you'll never know when your system is degrading.

**Integration is the real complexity.** Dropping an API call to an LLM into your codebase isn't the same as integrating AI into your product. The real work is in workflow integration: how does the AI output connect to downstream systems? How do users give feedback? How do errors surface and get corrected? How do you handle the cases where the model confidently returns wrong information?

## In Regulated Industries, the Stakes Are Higher

In insurance, a broker asks our AI: "Is this client covered for flood damage?" A wrong answer, delivered confidently, doesn't just frustrate a user. It creates liability. It can affect a real claim. Regulators in the EU are not impressed by "the model said so."

Here's what "just add AI" ignores in regulated industries:

→ Your data reflects historical decisions, including wrong ones
→ GDPR requires you to explain automated decisions, and LLMs are not explainable by default
→ Legacy systems weren't designed for AI-readable data formats
→ Insurance products are jurisdiction-specific — a generic model doesn't know Polish insurance law
→ Evaluation is not optional. You need metrics before you ship, not after

## The Right Question

"Just add AI" is the wrong frame. The right question is: "What specific problem do we want AI to solve, for which users, at what quality bar, and how will we know when it's working?"

That question is harder to ask in a product meeting. But it's the only one that leads to a system worth building.

The teams I've seen succeed with AI treat it exactly like they'd treat any other hard engineering problem: they start small, they measure obsessively, they iterate based on real user feedback, and they resist the urge to rebuild everything before proving value on something narrow.

The failure mode is starting big, skipping evaluation, and shipping something that looks impressive in a demo and falls apart in production.

## What This Means for You

If you're a developer being asked to "just add AI": push back on the framing. Ask for clarity on the specific use case. Ask who will define what "good" looks like. Build the evaluation infrastructure before you build the feature.

If you're a leader asking your team to "just add AI": understand that you're asking them to navigate a new engineering discipline with production stakes. Give them time for the invisible work — data prep, evaluation, iteration — that won't show up in a demo but will determine whether the system actually works.

The technology is genuinely powerful. But it doesn't add itself. And pretending otherwise is how good teams end up building impressive demos that fail their users.

What's your experience with this? Have you been on the receiving end of "just add AI" requests? I'd genuinely like to know how teams are handling this.
