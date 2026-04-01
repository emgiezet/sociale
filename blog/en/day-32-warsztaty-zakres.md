---
day: 32
title: "The Exact AI Workshop Agenda I Used for 15 Developers (And Why It Was Split in Two)"
pillar: Educator
language: en
image: ../../images/day-32.jpg
image_unsplash_query: "workshop agenda whiteboard developers team"
---

# The Exact AI Workshop Agenda I Used for 15 Developers (And Why It Was Split in Two)

When I decided to run AI workshops for fifteen developers at Insly, the first design decision was the one I think most people get wrong: I didn't try to run one unified workshop for everyone.

I ran two tracks.

This post is the full breakdown: what was on the agenda, why the split, how the sessions were structured, and the key decisions that shaped the curriculum.

## Why Two Tracks

The developers who showed up to these workshops were not a homogeneous group. Some were working on new greenfield projects — building new microservices, designing new APIs, writing code where they had full control over the architecture. Others were deep in legacy maintenance — Symfony applications dating back to 2012 and 2015, codebases with no tests, functions that nobody fully understood anymore, and an organizational risk profile that made "just rewrite it" an impossible answer.

These two groups have genuinely different problems, and a single workshop agenda would have served neither of them well.

A developer building a new Python service doesn't need a session on how to ask AI to explain unfamiliar code — they wrote the code, they understand it. Conversely, a developer maintaining a twelve-year-old PHP application doesn't need a session on greenfield architecture with AI — that's not their constraint.

Mixing them together would have produced either a workshop that's too basic for the legacy engineers (who need concrete techniques for specific hard problems) or too advanced for the new-project engineers (who need to build basic habits before tackling harder scenarios).

So: two tracks, running in parallel for certain sessions, with shared sessions on the topics that cross-cut both.

## Track 1: New Projects

This track was for developers building new systems — new services, new features, new codebases. The problems here are different: not "how do I understand this existing mess" but "how do I build faster, better, with AI as part of the workflow."

**Environment setup and tool selection**

We started here because skipping it leads to confusion. Cursor, GitHub Copilot, local models via Ollama, Claude in the browser — these are not interchangeable, and the decision of what to use when matters.

The criteria I walked through: latency and workflow integration (Cursor for in-editor work), privacy sensitivity (local Ollama for anything that shouldn't leave the machine), capability ceiling (when you need the full model, not the lite version), and cost. No single tool wins on all dimensions; the right answer depends on the task.

**Workflow integration — writing code that AI can help with**

This was one of the less obvious sessions. It turns out that how you structure your code significantly affects how well AI can assist with it. Small, well-named functions with clear inputs and outputs are easier for AI to work with than large, sprawling methods with side effects. This is good software engineering anyway — but framing it as "AI-friendly code" gave developers a practical reason to care about it in a new way.

We also covered prompt engineering for development specifically: not generic prompting, but how to give an AI model the right context — existing interfaces, type signatures, existing tests — so that what it generates fits into the actual codebase.

**AI-assisted code review**

Using an AI model as the first reviewer before human code review. This is one of the highest-value workflows I've found: run your diff through Claude or GPT-4 with a prompt that asks for logic errors, edge cases, and style inconsistencies before opening the PR. It doesn't replace human review — it removes the easily-catchable noise so the human review can focus on what matters.

**Test generation for new code**

Writing unit tests for new functions using AI. The promise: take a function you just wrote, paste it in, ask for a test suite, get 80% of your coverage in five minutes instead of forty-five. The reality: it works, with caveats. AI-generated tests need review — they'll often test the happy path and miss edge cases, and occasionally test implementation rather than behavior. We covered how to prompt for better tests and how to review AI-generated tests critically.

**Documentation generation**

OpenAPI specs from route handlers. README sections from code. Inline comments for non-obvious logic. This is the category of work that developers consistently put off because it's important but not urgent — AI makes it fast enough that there's no longer a good excuse.

**Prototyping speed**

Going from idea to working proof-of-concept in the time of a single planning meeting. I demonstrated building a small functional prototype during the session — it's genuinely different from writing code the traditional way, and seeing it changes how developers think about the early stages of feature work.

## Track 2: Legacy Systems and Existing Code

This track was for developers working with code they didn't write, in systems that have accrued years of complexity, with constraints that make sweeping changes risky.

**Understanding unfamiliar code**

The most immediately practical skill: "explain this class to me." Not as a one-time trick, but as a systematic approach to exploring an unknown codebase. I showed techniques for giving AI enough context to produce accurate explanations — not just pasting a function, but including the interface it implements, the service it calls, the exception it catches.

And critically: how to evaluate the explanation. AI can be confidently wrong about code. We covered specific signals that suggest the model is guessing versus understanding — inconsistencies, vague language about behavior, explanations that don't account for edge cases in the actual code.

**Safe refactoring with AI**

How to refactor legacy code without breaking it. The key insight: tests are the safety net that make AI-assisted refactoring possible. If you have tests, you can let AI make changes and verify with tests. If you don't have tests — which is common in legacy codebases — you need to generate them first.

This led naturally into the next session.

**Generating tests for untested code**

This is one of AI's highest-value applications in a legacy context. For code with no existing tests: characterization testing — write tests that document what the code currently does, not what it should do. These "golden tests" don't validate correctness; they create a baseline that lets you detect when refactoring changes behavior.

AI is genuinely good at generating characterization tests. The session showed how to use it systematically: give the model the function, give it sample inputs if available, ask it to write tests that capture the current behavior, review for completeness.

**Bug hunting as a pair**

Using AI as a second brain for difficult debugging. Not "tell me what's wrong with this code" but a more structured dialogue: here's the symptom, here's the code path I've traced, here's what I've ruled out, what am I missing? The value isn't that AI finds the bug — it's that articulating the problem to AI often surfaces the answer anyway, and occasionally AI sees something you've looked past.

**Migration and modernization planning**

Using AI to help plan larger-scale changes: migrating to a newer PHP version, extracting a service from a monolith, refactoring a data model. AI is useful here not as an implementer but as a thinking partner — helping map dependencies, identify risky changes, draft a migration sequence.

## Shared Sessions

Some topics applied to both tracks and were run together.

**Security and privacy**

What can you safely share with AI APIs? What can't you? Enterprise plans, data retention policies, self-hosted options. For a company handling insurance data, these aren't optional topics — they're mandatory. We also covered prompt injection and the specific security concerns of AI-generated code.

**Evaluating AI output**

The single most important cross-cutting skill: how do you know if what AI produced is correct? This isn't just code review — it's a different kind of critical reading. AI output has specific failure patterns: it's often syntactically correct and semantically wrong; it tends to produce plausible-sounding but incorrect explanations; it will complete a pattern it recognizes even if that pattern is wrong for the specific context.

We spent a full session on this, because the answer to "how do I trust AI-generated code" is not "don't" and not "trust it fully" — it's "develop specific judgment about where AI is reliable and where it isn't."

**Integration into daily workflow**

How to build habits rather than use AI only when you remember it exists. Which tasks benefit most from AI assistance (understanding, generation, transformation), which benefit least (complex system-level reasoning, novel problem-solving), and how to structure your day to use AI where it's strong.

## Structure: 30/70, Always on Real Code

Each day was roughly thirty percent structured presentation and seventy percent hands-on work.

Hands-on meant: your actual tasks, your actual codebase, your actual sprint items. Not exercises I designed. Not Hello World applications. Real work that needed to get done anyway, now done with AI assistance.

This mattered. The fastest way to build confidence with AI tools is to successfully use them on a real problem. The fastest way to build good judgment is to use them on problems you already understand, so you can evaluate the output accurately.

I also gave explicit time for "productive failure" — trying to use AI in ways that didn't work, understanding why, and learning the failure modes. This is deliberately designed into the schedule because AI failure modes are not intuitive, and you need to encounter them in a low-stakes context.

## Key Curriculum Decisions

**Not teaching tools — teaching judgment.** Every session was framed around a decision: when to use AI, how to evaluate AI output, what to verify. The specific tools will change. The judgment won't.

**Addressing the "is it safe" question directly, at the start.** Not at the end as an afterthought. This question was blocking some developers from engaging, and it needed a real answer before anything else could land.

**Including the failure cases.** I showed examples of AI being wrong, confidently. Of AI-generated code that looked right but had subtle bugs. Of AI explanations that sounded authoritative but missed important context. This made the workshops more useful and more honest than a workshop that only shows the technology at its best.

**Going slow on the first day.** The temptation in any workshop is to cover too much. Day one was deliberately slow: one tool, one workflow, enough time to actually try it and debrief. Speed came in days two and three, once the basic patterns were established.

## What Wasn't on the Agenda

A few things I considered and left out.

**Prompt engineering theory.** There are courses dedicated to this. For developers who need to get work done, learning the principles by doing is more useful than studying theory first.

**Comprehensive tool comparison.** Too many tools, too fast-moving a landscape. I made opinionated recommendations and explained the reasoning, rather than surveying everything.

**AI strategy and organizational change.** That's a different conversation for a different audience. This workshop was for individual contributors — the people who actually write the code. Getting them productive is the priority.

---

*Next in this series: the legacy code track in depth — the specific techniques, the psychological resistance, and the moment resistance turned to enthusiasm.*
