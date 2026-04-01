---
day: 34
title: "AI-First From Day Zero: What I Showed My Team in the Workshops"
pillar: Trenches
language: en
image: ../../images/day-34.jpg
image_unsplash_query: "developer laptop coding workflow team"
---

# AI-First From Day Zero: What I Showed My Team in the Workshops

"AI-first" is one of those phrases that sounds decisive in a slide deck and means almost nothing in a standup. When I ran AI workshops for 15 developers at Insly, the first thing I had to do was replace the phrase with actual behaviour — specific things you do, in a specific order, that are different from what you did before.

This post is about that. What AI-first actually looks like when you're starting a new project from day zero.

## What "AI-First" Doesn't Mean

It doesn't mean adding a chatbot to your product.

It doesn't mean running GitHub Copilot and calling it done.

It doesn't mean outsourcing decisions to a model and hoping for the best.

Those are easy misreadings, and I've seen teams do all three. "AI-first" for a development workflow means something more specific: you involve AI at every stage of the work, from requirements to review, in ways that change what you produce and how fast you produce it. You're not decorating an existing workflow. You're rebuilding the workflow with AI as a first-class participant.

Here's what that looks like in practice, stage by stage.

## Stage 1: Requirements — AI as a Stress-Tester

Most teams write requirements and then hand them off. Or review them with another human. I now do a third thing first: I paste the problem statement into Claude and ask it to poke holes.

Not "write me a spec." Rather: "Here's the problem I'm solving. What am I not accounting for? What edge cases am I ignoring? What's ambiguous enough that two engineers would build different things?"

The results are consistently uncomfortable in useful ways. In the workshops, I did a live demo of this with a fictional insurance claims processing service — a domain the team knew well. Within two minutes, Claude identified three requirements conflicts that would have caused integration problems downstream.

The team's reaction was not "wow, AI is smart." It was: "wait, we do this with real specs all the time and catch it way later." That was the point.

AI doesn't write your requirements. It challenges them while it's still cheap to change them.

## Stage 2: Architecture — Compressed Exploration, Not Outsourced Decisions

When I start a new project, I used to spend the first several hours in a private thinking loop — sketching options, rejecting them for reasons I'd only articulate later, eventually landing on something. That loop is valuable. AI doesn't replace it. But it compresses it.

What I showed the team: describe your context (domain, constraints, team size, existing stack, non-negotiables) and ask for three different architecture approaches with their tradeoffs explicitly stated. You don't accept any of them. You use them as starting points for real thinking.

This isn't abdication. It's like pairing with a very well-read engineer who has no ego about their suggestions. The suggestions are often wrong in ways that clarify what you actually need.

At Insly we run Go and Python backends on AWS, with Symfony still in parts of the legacy system. Whenever I'm designing something new in that context, I can get from "blank page" to "three real options with named tradeoffs" in 30 minutes instead of three hours. The decision is still mine. The exploration is shared.

## Stage 3: Implementation — Short Loops With Cursor

I want to be direct about how I actually use AI-assisted coding, because the naive version wastes time.

The naive version: paste a large prompt, get a large code block, try to run it, debug for an hour.

The version I showed: tight loops. Write a function signature and a docstring. Ask for an implementation. Read it. If it's wrong, figure out why your prompt was wrong, not why the model is wrong. Revise. Get a test. Verify the test is testing what you think it's testing. Move on.

The discipline is in the loop size. Long prompts to AI, trying to generate entire services at once — that's vibecoding, and it produces code nobody fully understands. Short loops, frequent verification, staying in the driver's seat — that produces code you own.

I walked the workshop through this on real Go code: a simple HTTP handler with some business logic. The first attempt from the model had a subtle error in the error handling. That error was a teaching moment — not "AI is bad" but "this is why you read every line."

One thing that surprised the team: once you're running tight loops, development speed for the parts that aren't novel — the infrastructure, the scaffolding, the boilerplate — increases dramatically. The creative, hard parts still take the same time. But there's less of the grinding stuff in the way.

## Stage 4: Code Review — AI Before Humans

Before a pull request goes to a human reviewer, I now run it through an AI review with a specific prompt template:

- What security issues do you see in this code, specifically around [domain concern — e.g., user data handling, authentication]?
- Which of the existing patterns in this codebase does this violate or ignore?
- What edge cases are not covered by the current tests?
- What would a senior engineer ask about this in review?

The goal isn't to replace human review. It's to raise the floor. By the time a human reviewer sees the PR, the obvious things are already addressed. Human review can focus on architecture, domain logic, and things AI genuinely misses — like "this works but it's going to be a nightmare to maintain in 18 months because of how this module is structured."

In the workshops, I showed before and after: the same piece of code, two PR descriptions — one without AI pre-review, one after. The difference in what was caught before human eyes touched it was significant. One participant said: "I've been sending my reviewers the homework I should have done myself."

## Stage 5: Test Generation — Thinking, Not Typing

This is where I saw the biggest mindset shift in the workshops.

The traditional pain of writing unit tests: you know what you need to test, you just have to write out all the cases. It's tedious. And because it's tedious, you skip edge cases, or you write tests that technically pass but don't cover the failure modes that matter.

AI changes this. You describe the behaviour you want to test — in plain language, ideally with some domain context. You get a set of test cases back. Then you review them, not for whether they're syntactically correct, but for whether they're testing the right things. You add the ones you would have missed. You delete the ones that don't make sense.

The writing is no longer the bottleneck. The thinking is. And thinking about what you're testing — what could go wrong, what your invariants are — is the part that actually makes tests valuable.

I ran this exercise with a piece of Python code from a hypothetical insurance calculation module. The generated tests covered seven cases. I would have written five. Two of those seven were genuinely useful tests I wouldn't have thought of. The other two weren't valid for our domain. That ratio — find more, discard some — is the normal mode.

## Before and After: A Sprint With and Without This Workflow

Here's a rough comparison from what I observed at Insly in my own team's work before the workshops and what I saw in teams that adopted AI-first approaches:

**Greenfield feature, traditional sprint:**
- Day 1–2: Requirements discussion, back-and-forth clarification
- Day 3: Architecture sketching, async feedback
- Day 4–7: Implementation, hitting unexpected edge cases mid-sprint
- Day 8: Writing tests, rushing because deadline
- Day 9: Review, several rounds of comments
- Day 10: Ship

**Greenfield feature, AI-first sprint:**
- Day 1: Requirements with AI stress-test, conflicts caught same day
- Day 1 afternoon: Architecture options explored, direction chosen
- Day 2–5: Implementation with tight AI loops, tests generated alongside
- Day 6: AI pre-review, PR raised with edge cases already addressed
- Day 7: Human review focused on what matters
- Day 8: Ship

The time difference varies by project and team. What doesn't vary: the reduction in back-and-forth late in the sprint. The stuff that creates crunch — discovering requirements gaps in implementation, catching edge cases in review — moves earlier, when it's cheaper.

## What Doesn't Work for Greenfield

AI-first doesn't solve every problem in new projects, and I'd rather say that plainly than let teams learn it the hard way.

**AI isn't good at novel domain logic.** If you're solving a problem nobody has solved before in quite the same way — unusual regulatory logic, complex multi-party calculations, domain-specific optimisation problems — AI will generate plausible-looking code that is subtly wrong in domain-specific ways. You need deep domain expertise to catch those errors. The tool isn't a substitute for understanding your domain.

**Context decay is real.** In a long session working on a large codebase, AI assistants lose track of earlier context. The tight-loop discipline helps here — smaller units of work mean less context to maintain — but it doesn't eliminate the problem. You have to stay the architect.

**Team inconsistency.** If half your team adopts AI-first and half doesn't, you get inconsistent code quality and frustrated reviewers. The discipline has to be shared, and that takes deliberate adoption — not mandates, but shared practice.

## The Honest Summary

What I showed the team isn't magic. It's a set of habits — concrete things you do at each stage of a project — that make the work faster and catch problems earlier. The mindset shift is smaller than it sounds: you're not becoming a "prompt engineer." You're becoming an engineer who uses a powerful tool thoughtfully.

The team at Insly was sceptical going in. By the end of the first day of workshops, they weren't believers in AI — they were users of specific techniques that had already produced results they could see. That's the right way for adoption to happen: not through inspiration, through demonstration.

If you're starting a new project next week, you can apply one of these stages immediately. Start with requirements. Run your problem statement through Claude before your next planning session. See what comes back.

It'll either find something you missed, or confirm you've thought it through. Either way, you're ahead.
