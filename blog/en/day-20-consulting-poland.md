---
day: 20
title: "Why the Best AI Consulting Advice Often Starts With 'Don't Build AI'"
pillar: Trenches
language: en
image: ../../images/day-20.jpg
image_unsplash_query: "consulting business strategy meeting"
---

# Why the Best AI Consulting Advice Often Starts With "Don't Build AI"

There's a paradox in technology consulting: the most valuable advice you can give a client is sometimes "don't build what you're planning to build."

This isn't a cynical position. It's the result of observing that pressure to adopt AI — internal pressure, market pressure, executive pressure — often precedes diagnosis of the actual problem.

## The Pattern I See Regularly

A company comes with a project proposal. The project is framed in terms of technology: "we want to deploy an AI chatbot," "we need a RAG system for our documents," "we want to automate X with AI." The technology is already chosen. The problem is implementation.

My first question: "What specific business decision is this system supposed to support?"

There's usually a moment of silence. Then one of two answers.

Either the answer is precise and reveals a well-prepared project: "We want our underwriters to find the relevant coverage clause within 30 seconds." That's a project you can build toward and measure.

Or the answer is general: "We want to be more innovative," "our competitors deployed AI," "leadership wants to see AI in our product." That's a project that can consume budget without solving a specific problem.

## The Financial Services Case

I recently worked with a financial services company in Poland. They came with a plan: an AI chatbot integrated into their existing CRM. Specific idea, budget, timeline. Ready to build.

After 45 minutes discussing their actual business processes, it became clear the chatbot was an answer to a different problem than the one that actually existed. The real problem: sales staff were spending 30–40% of their time manually searching for customer information across three unintegrated systems. A chatbot wouldn't solve that — because the problem wasn't about answering natural language questions. It was about fragmented operational data.

The solution: a dashboard aggregating data from three systems, with unified search and customer history view. Implementation time: three weeks. Cost: 30% of the planned budget. Outcome: sales staff reported 40% reduction in preparation time before customer conversations.

Here's what struck me: the technical complexity of the actual solution was far lower than what was originally planned. A dashboard with data aggregation is straightforward engineering. A document chatbot with compliance requirements, accurate retrieval, hallucination prevention, and user trust-building is months of work.

The diagnosis changed the outcome. Not the execution.

## The Three Mistakes I See Repeatedly

### Mistake 1: Starting with tools instead of problems

"We want to deploy RAG." "We want AI agents." "We want GPT integration."

When the technology is already chosen before the problem is defined, you're likely building the wrong thing. The right technology emerges from the right problem definition.

What drives this: executive pressure from someone who read an article about AI and wants to show progress before end of quarter. An IT team given the task "do something with AI" without a defined business problem. No one empowered to say "let's check if this makes sense first."

### Mistake 2: Ignoring GDPR and compliance at design time

Companies build a prototype with customer data before anyone asks: in which country are the servers? Who has access to the logs? What does the right to be forgotten look like in a system with embeddings?

Then they pay to redesign everything.

This is particularly acute in Poland and the EU, where GDPR enforcement has teeth. A chatbot that processes customer data through an LLM API needs to answer these questions before you write the first line of code, not after you've built a demo that legal has to shut down.

For regulated industries — insurance, finance, healthcare — the compliance questions aren't a post-launch concern. They're a pre-architecture concern.

### Mistake 3: Measuring success by "does it work" instead of "does it work better"

An AI system that answers 80% of questions worse than the old search engine isn't progress. It's a more expensive problem.

I've seen teams celebrate demo success and deploy systems that scored below the baseline they were meant to replace. The evaluation was done against "can it answer questions?" rather than "does it answer questions as well as what it's replacing?"

The measurement problem is compounded by the difficulty of AI evaluation. But "we haven't measured" is not a defense for shipping. It's a reason to build the evaluation infrastructure before you launch.

## What Good AI Projects Look Like

Good AI projects share a few characteristics:

**A specific decision to support.** Not "we want to be smart," but "our underwriter needs to assess risk for a given client in 30 seconds."

**A known definition of success.** "We'll reduce query handling time from 15 minutes to 3 minutes and measure this in the first 30 days."

**A defined fallback.** "If the AI is uncertain, it escalates to a human." A missing fallback is a project with undefined risk.

**An answer to: what happens when the system is wrong?** In regulated industries, this is a legal question, not just a UX consideration.

If a project meets these four criteria, it's worth building. If it doesn't — it's worth pausing to ask questions before investing the budget.

## The Question That Opens the Real Conversation

When companies hire me as a consultant, the question I always ask first surprises them.

I don't ask about their tech stack. I don't ask about their architecture.

I ask: "What specific business decision is this system supposed to support?"

That question — and the silence that follows — tells me almost everything I need to know about whether the project is going to succeed.

The AI projects that succeed are the ones built from this kind of clarity. The ones that fail are usually the ones that started with the technology choice rather than the problem definition.
