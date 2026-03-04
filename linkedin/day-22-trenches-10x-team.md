# Day 22 — Trenches: The 10x Team
**Pillar:** Trenches | **Week:** 5 | **CTA:** Comment

---

## LinkedIn Post

The "10x developer" doesn't exist.
But the 10x team does.

I've managed engineers for over a decade. I've never met a developer who was 10x more productive than their peers in any meaningful, sustained way.

But I've seen teams that were 10x more effective than other teams working on the same problem.

Here's what those teams had in common — from what I've observed at Insly and elsewhere:

→ **They had shared context.** Everybody understood the domain, the system, and why the current architecture looked the way it did. Onboarding new features didn't require explaining the whole system from scratch.

→ **They had low coordination overhead.** Decisions were made at the right level. Small decisions happened fast, without escalation. Big decisions happened with the right people in the room.

→ **They built and maintained quality infrastructure.** Good tests, good documentation, good deployment pipelines. Not as a bureaucratic exercise but because bad infrastructure compounds — every task takes longer than it should.

→ **They trusted each other.** Not naively. But enough that a code review was a technical conversation rather than an interrogation. Enough that someone could say "I don't know" without it feeling risky.

→ **They had a clear north star.** They knew what success looked like — not in abstract terms but specifically enough to make tradeoff decisions without asking for permission every time.

With my 11-person team, building this has been more important than hiring. The team's collective capacity exceeds what any individual could produce, and the quality of that team dynamic determines how much of that capacity actually gets used.

**The bottleneck in most teams isn't talent. It's the infrastructure for talent to compound.**

What do you think makes a team genuinely exceptional? I'm curious what's in your list.

#TechLeadership #EngineeringManagement #SoftwareEngineering #TeamDevelopment

---

## Blog Post

### What Makes a Team 10x? The Infrastructure Under High-Performance Engineering Teams

The "10x developer" concept has generated years of debate. Is it real? Is it harmful? I've come to a specific view: the debate is pointing at the wrong unit of analysis.

In ten-plus years of leading engineering teams, I've never observed a developer who was 10x more productive than their peers in any sustained, meaningful way. I've seen 2x, maybe 3x for specific task types. But 10x? No.

I have observed teams that were dramatically more effective than other teams working on similar problems. The difference wasn't the individual talent level. It was the quality of the infrastructure those teams had built for themselves.

#### Shared Context: The Invisible Multiplier

The most effective teams I've worked with or observed have shared context at a depth that allows them to make good decisions quickly — without extensive explanation, without escalation, without miscommunication.

Shared context means: everybody understands the domain (the actual business problem the software is solving), the system (how the current architecture works and why), the constraints (what's fast, what's expensive, what's fragile), and the current state (what's in progress, what's changed recently, what's uncertain).

Building this shared context requires investment: good documentation of architectural decisions (ADRs), regular team-level technical discussions, onboarding processes that transfer context explicitly rather than hoping it will be absorbed. Most teams under-invest here because the investment has no immediately visible return.

The return shows up in speed of decision-making, quality of code review, and the number of cross-team conversations that don't need to happen because the answer is already in the team's shared model.

At Insly, with an 11-person team building AI systems in a complex insurance domain, shared context is particularly critical. The business logic is non-trivial. The AI components interact with each other in ways that require whole-system understanding. Engineers who don't understand the insurance domain context produce code that works technically but fails in domain edge cases.

We invest explicitly in shared context: weekly team-level architecture reviews, a living document of domain model decisions, and a team practice of explaining the "why" not just the "what" in code reviews.

#### Low Coordination Overhead

Coordination overhead is the friction that exists between when a decision is needed and when it gets made. High coordination overhead means that small decisions require meetings, meetings require scheduling, and by the time the decision is made, the engineer waiting for it has context-switched twice.

High-performing teams are almost uniformly better at right-sizing their decision-making process. Small, reversible decisions are made immediately by whoever is doing the work. Medium decisions are made by small groups with fast communication. Large, hard-to-reverse decisions involve the right stakeholders and are documented.

The failure mode in many teams is either too much process (everything goes through a committee) or too little (no shared understanding of what decisions should be escalated). Both create overhead. The optimum is team-specific and requires calibration over time.

We've reduced coordination overhead on my team primarily through context-sharing (so people can make good decisions with less consultation) and explicit decision documentation (so decisions don't need to be relitigated every time someone wasn't in the original conversation).

#### Quality Infrastructure

Quality infrastructure — tests, CI/CD, observability, documentation — has compound returns. Bad infrastructure creates drag on every subsequent task. Every bug takes longer to diagnose. Every deployment carries more risk. Every onboarding takes longer because the system is harder to understand.

The teams I've seen fail at sustained productivity often have a specific pattern: they shipped fast early by skipping infrastructure, and then slowed down continuously as the technical debt compounded.

High-performing teams treat infrastructure investment as non-negotiable. Not as bureaucracy — as the foundation that makes everything else possible.

For AI-specific work at Insly, quality infrastructure means: evaluation datasets maintained and versioned, LLM call logging and tracing (via LangSmith), automated quality regression detection, and clear rollback procedures for model and retrieval changes.

#### Trust and Psychological Safety

Teams where people are afraid to say "I don't know" or "I made a mistake" spend enormous energy on self-protection that could be spent on solving problems.

Trust at the engineering team level means: code reviews are technical conversations, not performance evaluations. Failures are investigated for systemic causes, not attributed to individuals. Questions are welcomed, not treated as evidence of incompetence.

This sounds soft. The engineering impact is concrete: faster debugging (people share relevant context without worrying about blame), better code review (reviewers give honest feedback), faster knowledge transfer (people ask questions instead of guessing).

Building this culture is leadership work, not HR work. It happens through how the team lead handles mistakes in public, how code reviews are modeled, and what behavior is visibly rewarded versus what's punished.

#### The Bottleneck Is Infrastructure, Not Talent

If you're leading a team that's underperforming relative to what the individual talent suggests should be possible — look first at the infrastructure. Is context shared deeply enough? Is coordination overhead right-sized? Is quality infrastructure maintained? Does trust exist at the level that enables open communication?

In my experience, improving team infrastructure has higher leverage than hiring. A 10x team isn't composed of 10x developers. It's composed of ordinary developers who have built extraordinary infrastructure for their collective capacity to compound.

That's the opportunity. And it's almost entirely within the team lead's control.
