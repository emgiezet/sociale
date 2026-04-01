---
day: 33
title: "The Legacy Code Problem Isn't Technical. It's Psychological."
pillar: Trenches
language: en
image: ../../images/day-33.jpg
image_unsplash_query: "legacy code old software developer debugging"
---

# The Legacy Code Problem Isn't Technical. It's Psychological.

I want to tell you about a moment from the workshops.

One of the engineers — several years at Insly, responsible for one of our older Symfony modules — sat with his arms crossed at the start of the legacy code session. Before we'd even begun, he said: "This won't work for our code. Our code is too complicated. Nobody understands it — not humans, not AI."

I asked him to show me the hardest piece he could find.

He pasted a class. Around three hundred lines, no comments, several layers of inheritance, business logic mixed with infrastructure code. The kind of thing that makes new developers quietly panic when it's assigned to them.

I asked Claude: "Explain what this class does, step by step, as if you were describing it to someone seeing it for the first time."

The answer came back in about ten seconds. It was a good answer. Not perfect — the engineer corrected two specific details where the model had misread the intention. But the skeleton was accurate. The core logic was legible. The explanation named the responsibility the class was carrying in terms that matched how the engineer himself would have described it if pressed.

He stared at the screen for a moment. Then he said: "Okay. I didn't expect that."

And then the session changed.

## What Was Really Happening

I've thought about that moment a lot since the workshops. The engineer wasn't wrong that the code was complex. He was wrong about what that complexity meant for AI.

The specific belief he held — and I've heard versions of it from developers at several different companies — goes something like this: "Legacy code is special. It's so old, so underdocumented, so idiosyncratically structured that modern AI tools, trained on clean examples and sensible patterns, won't be able to make sense of it. Our situation is the exception."

This belief is understandable. It feels protective. If the tools can't work with your code, then the tools can't judge your code, and the code that you've been maintaining for years and have become expert at reading can remain the territory where your expertise is sovereign.

But it's also wrong, in a specific and important way. Legacy code is not too strange for AI — it's just strange in the same ways all code is strange at scale. Too many responsibilities per class. Unclear naming. Business logic that's accumulated in unexpected places. Implicit dependencies. These are patterns AI has seen in enormous quantities in training data. The code isn't special. It's just old.

The breakthrough in that session wasn't that AI did something technically impressive. It was that it demolished a belief that was blocking an experienced engineer from even trying.

## The Psychology of Legacy Code Developers

Developers who work on legacy systems for years develop a specific relationship with that code. It becomes known territory — not comfortable exactly, but navigated. They know where the buried mines are. They know which classes are safe to touch and which will explode if you look at them wrong. They know the history: why this function does this strange thing, why this service calls that other service, what incident in 2017 led to this particular hack that has never been cleaned up.

This knowledge is genuine and valuable. It's also, occasionally, a cage.

The same expertise that makes someone effective at maintaining legacy code can create resistance to change — because change is how you lose the reliable map you've built. A new tool, a new approach, a new colleague who doesn't know the history: all of these are threats to the navigational advantage that expertise provides.

AI is a particularly interesting version of this threat, because AI can read code without any of the accumulated context that makes legacy expertise feel valuable. It can explain a function without knowing the 2017 incident. It can suggest a refactoring without knowing about the buried mine.

For some developers, that's liberating. For others — including, at first, the engineer in that workshop — it's threatening. If a machine can explain your code to a newcomer in ten seconds, what is the value of ten years of accumulated expertise?

I want to give a direct answer to that question, because I think the fear deserves one: the value is judgment. AI can describe what code does. It cannot tell you whether what it does is correct. It cannot tell you whether the approach taken in 2015 should be preserved or replaced in 2026. It cannot make architectural decisions. It cannot weigh business risk against technical debt. Those judgments require context, responsibility, and domain knowledge that only the humans who work with this system every day possess.

AI doesn't make legacy expertise obsolete. It makes certain parts of legacy work less tedious — so the expertise can be spent on the parts that actually require it.

## Specific Techniques That Worked

Let me be concrete about what we actually did in the legacy track, and what produced results.

### Code explanation as a first step

The first application is the simplest and the most broadly useful: ask AI to explain code you don't fully understand, before you touch it.

This works for onboarding. It works when you're handed a ticket for a module you've never seen. It works when you're debugging and need to understand a function you didn't write.

The technique that matters: don't just paste the function. Give context. Include the interface it implements. Include the type of the object it receives. Include any exception types it catches or raises. The model's explanation is only as good as the context it has.

And evaluate the explanation critically. Look for hedging language ("this appears to," "it seems like") — these are signals that the model is inferring rather than reading. Cross-check specific claims against the code. Use the explanation as a starting hypothesis, not a final answer.

### Characterization tests before refactoring

This is one of the most valuable applications of AI in legacy work, and the most underused.

If you have code with no tests and you want to refactor it, you face a standard problem: how do you know that your refactoring didn't break anything, when you have no tests to fail?

The answer is characterization tests: tests that document what the code currently does, not what it should do. They capture actual behavior as it exists — including bugs, if there are bugs — and create a baseline that will alert you if refactoring changes behavior in unexpected ways.

Writing characterization tests manually is tedious. AI makes it fast.

Give the model the function you want to characterize. Give it sample inputs if you have them. Ask it to write tests that capture the current behavior, including edge cases. Then review the tests against the code — not to validate that the behavior is correct, but to validate that the tests accurately reflect what the code actually does.

In the workshop, we applied this to a legacy billing calculation module that had never had tests. We generated characterization tests in about twenty minutes. Before AI, this would have taken most of a day. The tests weren't beautiful. They weren't architecturally ideal. But they existed, which meant we could start refactoring with a safety net we hadn't had before.

### Safe incremental refactoring

With characterization tests in place, refactoring with AI becomes much more practical.

The technique: refactor in small increments. Make one change at a time. Run the characterization tests after each change. If a test fails, you know exactly what changed behavior and can decide whether that change was intentional.

AI is useful here as a refactoring partner, not a refactoring agent. Describe the change you want to make. Ask the model to show you how to make it. Review the proposed change before applying it. Run the tests. Repeat.

The important discipline: never apply AI-suggested refactoring without reading it carefully. Legacy code has subtle dependencies that AI doesn't know about. A refactoring that looks safe from the code alone may break something that the tests don't cover. This is where the engineer's contextual knowledge remains indispensable — the AI proposes, the engineer decides.

### Bug hunting through structured dialogue

The most useful bug-hunting application of AI isn't "tell me what's wrong with this code." It's a structured dialogue.

Here's the format that worked: describe the symptom in precise terms. Describe the code path you've traced. List the hypotheses you've already ruled out and why. Then ask the model: given this symptom and this evidence, what am I missing?

This is useful for two reasons. First, articulating the problem clearly to AI forces the kind of systematic thinking that often surfaces the answer before AI says anything. Second, AI occasionally sees something you've looked past — a variable name that doesn't match its use, an off-by-one that becomes visible when the pattern is stated explicitly.

One engineer in the workshop spent forty minutes on a bug before the session. During the session, he described it to Claude in structured terms and got the answer in the first response. The bug was an incorrect null check in a specific condition — something he'd looked at several times and not seen. The model saw it because he'd described the symptom precisely enough that the check was the only plausible explanation.

### Naming and comments as low-cost readability improvement

This is the cheapest improvement you can make to a legacy codebase and one of the most valuable.

Give AI a function or variable with a bad name and ask for better alternatives. Give it an undocumented function and ask for a comment that explains its purpose and parameters. These are operations that take seconds and make the next person who opens the file measurably faster.

This is also safe: changing names and adding comments doesn't change behavior. It's the lowest-risk category of improvement, and AI can do it faster and more consistently than a developer manually writing documentation.

## The "Aha" Moment

The moment that changed the legacy track wasn't a technical breakthrough. It was watching the engineer who had said "this won't work" start to use AI systematically, without being prompted, on a ticket he'd been avoiding for two weeks.

He had a complex filtering function that combined several business rules in ways that had grown unclear over time. He'd been putting off touching it because he wasn't sure he understood it well enough to modify it safely.

He asked Claude to explain the function. He got a clear explanation. He asked Claude to suggest where he might add a new filtering condition without breaking the existing logic. He got a concrete proposal. He reviewed the proposal carefully, modified it based on his knowledge of the business rules, and applied it.

The ticket that had been sitting for two weeks was done in about forty minutes.

What changed wasn't the code. What changed was that he had a way to approach the uncertainty that had been blocking him. AI didn't replace his expertise — it gave him a starting point so his expertise didn't have to do all the work of orientation from zero.

## A Practical Framework: How to Use AI with Legacy Without Breaking Things

Based on what worked and what didn't, here's the framework I'd give to any team starting AI use with a legacy codebase:

**1. Start with reading, not writing.** Use AI to understand existing code before using it to modify code. Build confidence in the explanation quality before trusting the change suggestions.

**2. Generate characterization tests before refactoring anything.** This is non-negotiable. Without a safety net, AI-assisted refactoring is too risky in systems you don't fully understand.

**3. Refactor in the smallest possible increments.** AI makes it tempting to make large changes because large changes are easy to generate. Resist this. Small increments are safer and easier to verify.

**4. Maintain the discipline of reading every change.** Don't apply AI-generated code without reading it. Legacy codebases have implicit contracts and dependencies that AI doesn't know about.

**5. Use AI for the tedious parts, human judgment for the consequential parts.** AI generates characterization tests, explains unfamiliar code, and suggests names. Humans decide which behavior is correct, which refactoring is safe given the business context, and which technical debt to pay down in what order.

## What Actually Changed vs. What Didn't

After the workshops, something shifted in how the legacy track developers worked. The change was real but specific.

**What changed:** The tendency to avoid unfamiliar code decreased. Developers who would have spent hours being confused by a module now started with an AI explanation, got oriented quickly, and spent those hours on the actual problem. The backlog of "I need to understand this before I touch it" items started moving.

**What didn't change:** The need for engineering judgment. AI can't decide whether a legacy architecture should be preserved or migrated. It can't set priorities. It can't make the call on which technical debt matters enough to address now. Those decisions still require the same expertise they always required.

The most honest summary: AI made the tedious parts of legacy work faster, which freed up time and cognitive energy for the parts that actually require a skilled engineer. It didn't make legacy work easy. It made parts of it less hard.

For a team maintaining a system that's been running in production for over a decade, that's not a small thing.

---

*Next in this series: what the workshop participants said two weeks after — the honest retrospective on what stuck and what didn't.*
