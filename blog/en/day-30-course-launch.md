---
day: 30
title: "30 Days, 30 Posts: What I Learned From Sharing Everything I Know About AI in Production"
pillar: Educator
language: en
image: ../../images/day-30.jpg
image_unsplash_query: "online course learning developer laptop"
---

# 30 Days, 30 Posts: What I Learned From Sharing Everything I Know About AI in Production

A month ago, I made a commitment: share something real about building AI in production every weekday for 30 days. Not recycled industry commentary. Not tutorial content that ignores real-world complexity. Actual accounts from the work I do at Insly — the architecture decisions, the team dynamics, the production failures, the things that actually worked.

This is the retrospective. And the announcement of what's next.

## Why I Started

The immediate reason: I'd been following practitioners in other domains who shared openly about their work, and found it far more valuable than academic content or vendor marketing. I wanted to contribute that kind of content for the specific intersection I inhabit: experienced software engineering, AI systems in production, regulated industries, and the Polish tech market.

The deeper reason: I genuinely believe that the knowledge needed to deploy AI responsibly in regulated industries is concentrated in too few places. The academic literature is rigorous but disconnected from production concerns. The vendor marketing is glossy and misleading. The practitioner voice — this is what we actually built, here's what broke, here's what we learned — is underrepresented.

If I know things that would help teams avoid expensive mistakes, not sharing them is a form of hoarding. This 30-day project was my attempt to stop hoarding.

## What I Covered

Looking back at 30 posts across three pillars, certain themes emerged:

**The technical architecture thread.** RAG from fundamentals to production. The progression from Bedrock Knowledge Bases (60% quality) to hybrid search (72%) to LightRAG (89%). Evaluation frameworks. Bielik for Polish-language documents — a 12 percentage point precision improvement over the translation approach. AWS RDS cost investigation. Insly's four-system architecture and where AI fits within it.

These posts established technical credibility and were the clearest differentiation from generic AI content. Engineers who've read these posts have specific, applicable frameworks they can use.

**The leadership and team thread.** 360-degree feedback. The emotional cost of leading through AI transformation. What makes a team exceptional and why it's infrastructure, not talent. Vibecoding and developer judgment. Managing competence anxiety in experienced engineers.

These posts got more engagement than I expected. The human side of technical leadership is underrepresented in tech content. People are hungry for it. Several posts in this thread led to direct messages from tech leads who said they'd been looking for exactly this kind of content.

**The domain and career thread.** PHP to AI career evolution. Open source contribution and what 18 million Packagist installs taught me about sustainable architecture. The Polish AI ecosystem. The insurance AI future and why companies need to start building now.

These posts built context and community in ways that pure technical content doesn't. They connected me with people thinking about similar problems in different contexts.

## What I Got Right

**Posting in Polish for Polish audiences.** The engagement rate on Polish posts with the Polish tech community was significantly higher than on English posts. Smaller absolute numbers, but exactly the audience that matters most for the work I'm doing. The Polish tech community is underserved by English-only technical content, and filling that gap is worth doing intentionally.

**The comment-first mindset.** Several posts were designed to generate comments — asking for reactions, posing genuine questions, framing contentious positions. The comment threads were often better than the posts. I learned more from the pushback and additions than from writing the original. Two posts led to direct conversations that may turn into consulting relationships.

**Including failure stories.** The posts where I described what didn't work — the first RAG prototype's 60% quality, the team challenges during AI transformation, the architecture decisions we regretted — got more engagement and more personal messages than the success stories. People trust practitioners who are honest about failure.

## What I Got Wrong

**Underestimating how much "boring" topics resonate.** I almost didn't write the post about the emotional cost of AI transformation because I thought it was "not technical enough." It became one of the most-shared posts of the 30 days. The human dimension of technical leadership is a gap in the content ecosystem, and I should have leaned into it earlier.

**Not building community infrastructure earlier.** By Day 25, I was having direct messages with people across the European insurance tech and Polish AI communities. I should have pointed to existing community spaces or created one earlier. Connections formed over 30 days are worth preserving in a structured way.

## The Evaluation Framework, Applied to This Project

It would be inconsistent to spend 30 days advocating for evaluation infrastructure and then not evaluate my own project.

Measurement before the project: 0 (no baseline).

Measurement after: followers increased, reach significantly higher, direct messages from potential consulting clients, course waitlist interest from a meaningful number of developers.

The most important outcome isn't in those numbers: I have a clearer understanding of what content serves which audience. The architecture content serves developers who are building AI systems. The leadership content serves tech leads and people managers. The career and domain content serves people who are trying to understand where they fit in the AI shift. All three audiences are relevant to the courses and community I'm building.

## What's Next

**"Agentic AI Developer" course** — For software engineers who want to go from "I understand RAG theoretically" to "I can ship production AI systems responsibly." This is the course that addresses the gap between tutorial-quality content and production-quality engineering.

The curriculum:

- **Production RAG architecture**: Beyond the tutorial, into evaluation and iteration. Chunking strategies, retrieval evaluation, hallucination detection, the mistakes that cost us weeks. The progression from basic vector search to hybrid retrieval to graph-based retrieval — and when to use each.

- **Agentic system design**: How to build systems where AI takes meaningful actions without going off-script. Multi-step reasoning, tool use, orchestration, debugging when things go wrong in probabilistic systems.

- **Evaluation and observability**: Building the infrastructure to know whether your system works. Test set construction, LLM-as-judge evaluation, trend tracking, failure diagnosis. The framework I use at Insly to gate every deployment.

- **Regulated industry AI**: Compliance design, audit trails, human oversight, stakeholder management. GDPR, the EU AI Act, and industry-specific requirements. How to build systems that survive a regulatory review.

- **Working with domain-specific data**: What changes when your documents are legal, medical, or insurance-specific. Language considerations (including Polish-language models like Bielik). Domain expert partnership.

- **Team adoption**: How to bring engineers along when the tooling changes every three months. Managing competence anxiety. Building shared context in a fast-moving domain.

Target audience: backend developers with 3+ years of experience, tech leads evaluating AI projects, engineers in regulated industries (insurance, finance, healthcare, legal) who want production-ready approaches.

Launch: spring 2026. The waitlist is open — comment below, message me, or DM "COURSE" for early access and founder pricing.

**Continued presence here** — Dropping from 5x/week to 3x/week. The format stays: specific, practitioner, no generic AI takes. Builder posts, Trenches posts, Educator posts. Polish posts for the Polish community.

## Thank You

Thirty days of conversations with people who are building, leading, and thinking seriously about AI — across Poland, across Europe, and beyond — have been genuinely valuable. The comment sections, the direct messages, the pushback that sharpened my thinking: this is what the "Educator" pillar was always meant to be about.

If you've been following along: thank you. If you've been lurking and this is the first post you're reading: start from Day 1 — there are 29 more posts worth reading.

If you want to continue the conversation: follow, comment, join the course waitlist. The next 30 days will be different, but the commitment to sharing what I actually know from production AI work continues.

See you on Day 31.
