---
day: 10
title: "The 3-Question Framework That Keeps AI Projects From Failing Silently"
pillar: Educator
language: en
image: ../../images/day-10.jpg
image_unsplash_query: "decision framework whiteboard"
---

# The 3-Question Framework That Keeps AI Projects From Failing Silently

I've seen AI projects fail in two ways. The first is the obvious failure: the system doesn't work, quality is poor, the team abandons it. That's a painful outcome, but at least it's visible. You know it happened and you can learn from it.

The second is the silent failure: the system ships, it technically runs, it gets used occasionally, but it never actually solves the problem it was built for. This failure is harder to detect and more expensive in terms of wasted effort and misplaced trust.

In my experience leading AI work at Insly, the silent failures almost always trace back to the same root cause: the problem was never precisely defined at the start.

The 3-question framework I'm sharing here was developed from observing these failures — and from building three RAG systems myself, one of which failed expensively before we changed our process. It's not elegant or complicated. But teams that can answer all three questions before they start building almost always build the right thing. Teams that can't answer them need to do more discovery work first.

## Question 1: What Specific Decision Does This AI Need to Support?

The word "specific" is doing a lot of work in this question.

"We want AI to make our workflow smarter" is not a specific decision. Neither is "we want to use AI to analyze our documents" or "we want an AI assistant for our support team."

A specific decision looks like this: "When an underwriter receives a claim notification, they need to identify within 30 seconds which coverage clause applies and whether the claim falls within coverage limits." That's a decision you can build toward, evaluate against, and measure.

In practice, I've found that many AI project proposals can't pass this test on the first try. "We want AI to improve our customer service" becomes, after ten minutes of questioning, "we want to automatically categorize incoming support tickets so they route to the right team without manual triage." That's a different and much more buildable project.

The discipline of naming a specific decision has several effects. It forces a conversation about who is making the decision and what information they need. It reveals the quality bar — what does "correct" look like for this decision? It clarifies scope — you're not building an AI system, you're building support for this specific decision.

A separate but related question: is this a retrieval problem or a generation problem? Most AI requests turn out to be retrieval problems in disguise. A broker asking "what does this policy cover?" doesn't need a creative answer. They need the exact text from the right document. That's retrieval. Solving it with a generative model adds complexity, latency, and hallucination risk without adding value. Getting this wrong costs months.

## Question 2: What Does the Human Do When the AI Is Wrong?

This question is the most uncomfortable one in a project kickoff meeting. It implies that the AI will be wrong. In the early enthusiasm of an AI project, this feels like negativity. It's actually engineering discipline.

Every AI system is wrong sometimes. The question is whether you've designed for that reality.

The answer to this question defines your error handling architecture, your UI design, and your risk profile. If the answer is "the human will review the AI's output before acting on it," then your interface needs to make the AI's reasoning visible and easy to override. If the answer is "this is a decision support tool, not a decision tool — the human always makes the final call," then your system should never present its output as definitive.

In insurance, we think carefully about this for every feature. A RAG system that returns the wrong policy clause can affect a claims decision. Our response: the system surfaces evidence (the retrieved text, the source document) alongside the answer, and underwriters are trained to verify the source before acting on the recommendation. We log every case where a human overrides the AI's suggestion — that log is our most valuable quality signal.

In regulated industries, this question has teeth. Before you build anything AI-powered in insurance, finance, law, or healthcare, you need to map: what data does this system touch? Can it leave its jurisdiction? Do automated decisions using this system require explainability under EU law (GDPR/AI Act)? What's the audit trail requirement?

If you can't answer these before you start, your architecture will change under you halfway through. That's an expensive sprint review.

## Question 3: How Will We Know It's Working 3 Months From Now?

This question is about success criteria and measurement.

"It works" is not a success criterion. "Users seem to like it" is not a success criterion. A success criterion is a measurable outcome that can be observed at a defined future point in time.

Good success criteria for AI projects look like:
→ Time to complete decision X reduced from Y minutes to Z minutes
→ Volume of manual overrides of AI recommendations below N%
→ Retrieval precision on evaluation set above threshold T
→ Number of support tickets requiring manual escalation reduced by X%

For our production RAG system, "good enough" meant: >85% retrieval precision on our 200-question labeled test set, <2 seconds response time at p95, zero answers citing sources that don't exist. We run this evaluation on every major change. If accuracy drops more than 3%, we don't ship. No exceptions.

Defining success criteria in advance does two things. First, it aligns the team on what "done" looks like, which prevents the project from drifting forever in improvement cycles. Second, it gives you an honest basis for a post-launch review — this either worked or it didn't, here's the evidence, here's what we learned.

## Using the Framework

The next time you're in an AI project kickoff — whether you're leading it or participating in it — try asking these three questions explicitly:

1. What specific decision does this AI need to support?
2. What does the human do when the AI is wrong?
3. How will we know it's working 3 months from now?

If the room can answer all three clearly, you have a project worth building. If it can't, the most valuable thing you can do is spend more time on discovery before anyone writes a line of code.

The AI projects that fail usually don't fail because of a technical problem. They fail because the problem was never precisely defined. These three questions are a forcing function to make that definition happen before the failure can occur.

Save this. Use it in your next AI project kickoff.
