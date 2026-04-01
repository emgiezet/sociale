---
day: 22
title: "What Makes a Team 10x? The Infrastructure Under High-Performance Engineering Teams"
pillar: Trenches
language: en
image: ../../images/day-22.jpg
image_unsplash_query: "engineering team collaboration whiteboard"
---

# What Makes a Team 10x? The Infrastructure Under High-Performance Engineering Teams

The "10x developer" concept has generated years of debate. Is it real? Is it harmful? I've come to a specific view: the debate is pointing at the wrong unit of analysis.

In over a decade of leading engineering teams, I've never observed a developer who was 10x more productive than their peers in any sustained, meaningful way. I've seen 2x, maybe 3x for specific task types and specific domains. But 10x? No.

What I have observed are teams that were dramatically more effective than other teams working on similar problems. Not because of individual talent levels, but because of the infrastructure those teams had built for themselves. That's the thing nobody talks about: the 10x team is built, not hired.

## Psychological Safety as the Foundation

The single highest-leverage thing I've done to improve team performance at Insly has nothing to do with technical decisions. It's building an environment where engineers can say "I don't understand this" or "I tried this and it failed" without it feeling risky.

This sounds soft. The engineering impact is concrete.

AI work requires experimentation by definition. When you're building RAG systems, tuning retrieval parameters, or evaluating whether LightRAG's graph-based approach outperforms Bedrock's semantic search for your use case — you don't know what will work. You have hypotheses. Some are wrong. The engineers who are afraid to be wrong stop experimenting, which means they stop learning.

I explicitly reward "I tried this and it failed, here's what I learned" in our retrospectives. It took months to normalize this behavior. But once it was normalized, the velocity of learning in the team changed noticeably. Our second RAG system benefited enormously from lessons that only existed because someone had run an experiment that didn't work and talked about it openly.

## Shared Context: The Invisible Multiplier

The most effective teams I've worked with have shared context at a depth that allows them to make good decisions quickly — without extensive explanation, without escalation, without miscommunication.

Shared context means everyone understands the domain (the actual business problem the software is solving), the system (how the current architecture works and why it looks that way), the constraints (what's fast, what's expensive, what's fragile), and the current state (what's in progress, what's changed recently, what's uncertain).

At Insly, with a 15-person team building AI systems in a complex insurance domain, shared context is particularly critical. The business logic is non-trivial. Insurance policies, coverage periods, premium calculations, claims workflows — these aren't concepts that map directly to how software engineers naturally think about data. Engineers who don't understand the insurance domain context produce code that works technically but fails on domain edge cases.

We invest explicitly in shared context: weekly team-level architecture reviews, a living document of domain model decisions, and a team practice of explaining the "why" not just the "what" in code reviews. The return on this investment shows up in the speed of decision-making — people can make good calls without consulting me because they understand the context well enough.

## Low Coordination Overhead

Coordination overhead is the friction between when a decision is needed and when it gets made. High coordination overhead means small decisions require meetings, meetings require scheduling, and by the time the decision is made, the engineer waiting for it has context-switched twice.

The failure mode in many teams is either too much process (everything goes through a committee) or too little (no shared understanding of what decisions should be escalated). Both create overhead.

High-performing teams are better at right-sizing their decision-making process. Small, reversible decisions are made immediately by whoever is doing the work. Medium decisions are made by small groups with fast communication. Large, hard-to-reverse decisions involve the right stakeholders and are documented.

I've reduced coordination overhead on my team primarily through context-sharing (so people can make good decisions with less consultation) and explicit decision documentation (so decisions don't need to be relitigated every time someone wasn't in the original conversation).

When we adopted LightRAG for our second RAG system, the whole team was productive in it within two sprints. Not because the technology was simple, but because we had built the habit of shared learning and low-friction knowledge transfer.

## Quality Infrastructure

Quality infrastructure — tests, CI/CD pipelines, observability, documentation — has compound returns. Bad infrastructure creates drag on every subsequent task. Every bug takes longer to diagnose. Every deployment carries more risk. Every onboarding takes longer.

The teams that fail at sustained productivity often share a specific pattern: they shipped fast early by skipping infrastructure investment, and then slowed down continuously as the technical debt compounded. The initial speed advantage reversed within a few months.

For AI-specific work at Insly, quality infrastructure means evaluation datasets maintained and versioned, LLM call logging and tracing, automated quality regression detection, and clear rollback procedures for model and retrieval changes. Without this infrastructure, we couldn't confidently iterate on our RAG systems — any change might have improved one metric while degrading another, and we'd have no way to know.

## Short, Honest Feedback Loops

Monthly performance reviews catch problems in the third month that could have been caught in the first week. I run quick weekly check-ins: what's blocked, what's confusing, what's frustrating. Not "how are you," but specific questions designed to surface problems early.

This serves two purposes. Engineers feel heard, which builds psychological safety. And problems that would have compounded over a quarter get addressed while they're still small.

The questions I actually ask: "What's the thing you're most uncertain about right now?" "Is there anything you've been waiting for that's blocked your work?" "What's the most frustrating part of your current task?"

These surface the actual friction points — unclear requirements, technical blockers, confusion about priorities — much more reliably than open-ended wellbeing questions.

## Senior Engineers as Uncertainty Reducers

In a team going through AI transformation, the role of senior engineers changes significantly. Their value is no longer primarily in their own output — it's in reducing uncertainty for everyone else on the team.

When we adopted AI tooling and new frameworks, I had the experienced engineers go first: learn the new technology, document what worked and what didn't, identify the pitfalls, build the first internal examples. Then they taught it. Nobody was left to figure it out alone.

This is how you get a whole team productive in a new technology within two sprints. Not by sending everyone to a training course, but by having your most experienced engineers create the internal knowledge transfer path.

## Hiring for Learning Speed

I've hired engineers who didn't know Python and became productive with AI tooling in weeks. I've hired engineers who knew Python but resisted learning new approaches — and their resistance compounded over time.

The skill that matters most for AI work isn't current technical skills. It's learning speed and willingness to be a beginner again. The tooling changes every few months. The engineer who can rapidly learn and adapt outperforms the engineer who's expert in the current stack but rigid about it.

In interviews, I evaluate this directly: "Tell me about the last time you had to learn something genuinely unfamiliar. How did you approach it? What was the hardest part?"

The answers are revealing. Engineers who have a systematic approach to learning new things — who can describe their process for building mental models in unfamiliar domains — are the ones who thrive when the technology shifts.

## The Bottleneck Is Infrastructure, Not Talent

If you're leading a team that's underperforming relative to what the individual talent suggests should be possible — look at the infrastructure first. Is context shared deeply enough? Is coordination overhead right-sized? Is quality infrastructure maintained? Does trust exist at the level that enables open communication and learning from failure?

In my experience, improving team infrastructure has higher leverage than hiring. A 10x team isn't composed of 10x developers. It's composed of ordinary developers who have built extraordinary infrastructure for their collective capacity to compound.

The good news: this is almost entirely within the team lead's control. You don't need to hire different people. You need to build the environment where your current people can do their best work.

That's the opportunity. Start there.
