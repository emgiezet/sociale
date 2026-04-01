---
day: 36
title: "I Run AI Workshops for Dev Teams. Here's What's Included — and Who It's Not For."
pillar: Trenches
language: en
image: ../../images/day-36.jpg
image_unsplash_query: "workshop training developers team whiteboard"
---

# I Run AI Workshops for Dev Teams. Here's What's Included — and Who It's Not For.

This is the post where I describe what I actually offer. I'll try to make it useful whether or not you hire me — because if the description is specific enough to help you evaluate the offer, it's also specific enough to help you think about what your team actually needs.

## The Background

I'm a Tech Lead at Insly, a European InsurTech SaaS — our AI solutions process over 150,000 documents per month. My team of 15 engineers has been building AI systems in production for over a year — AWS Bedrock, LightRAG, Python, Go, integrating AI into a codebase that includes Symfony components going back to 2012. We've learned what works and what doesn't the hard way.

A few months ago, I ran AI workshops for 15 other developers at Insly — people working on the same codebase, but not on the AI team. Engineers dealing with legacy PHP, multi-year-old architecture, the standard problems of a growing SaaS product. I ran it because I watched good people losing time and confidence on things that AI could help with, once someone showed them how.

Three days of hands-on sessions. Two tracks: new projects and legacy code. No slides without code. No theory without practice.

Three weeks later, I wrote an honest account of what changed. Some things did. Some things didn't. The specifics are in the previous post.

Now I'm offering the same thing to other teams.

## What the Workshop Covers

### Track 1: AI-First in New Projects

This covers what your development workflow looks like when AI is a participant from day zero — not a tool you add at the end.

Specifically:

**Requirements under pressure.** How to use AI to stress-test requirements before you build — catching gaps, ambiguities, and conflicts while they're cheap to fix. This alone changes how planning conversations work.

**Architecture exploration.** How to go from blank page to three well-reasoned options with explicit tradeoffs in 30 minutes instead of three hours. How to stay in the driver's seat while the model generates the options. How to recognise when AI suggestions are subtly wrong for your domain.

**Implementation loops.** The specific discipline of AI-assisted coding that produces code you own and understand — not vibecoded output that works until it doesn't. How to tune loop size. How to use Cursor effectively for backend development (Go, Python, PHP — depends on your stack).

**AI code review as a floor-raiser.** A specific prompt template for pre-review before human reviewers see the code. What it catches consistently. What it consistently misses (and why human review remains necessary).

**Test generation without the tedium.** How to use AI to generate test cases you would have skipped — specifically the edge cases — and how to evaluate which generated tests are actually testing the right things.

### Track 2: AI in Legacy Code

This is the harder problem, and the one most workshops ignore. Most of your engineers are probably working with code that's 5-10 years old. The techniques for AI-assisted work in that context are different from greenfield development.

**Context provision strategies.** How to give an AI assistant enough context about a legacy system to get useful responses — when you can't just paste the whole codebase. Architectural summarisation, targeted context injection, working with smaller slices.

**Refactoring with AI.** How to use AI to propose refactoring approaches and identify the risks in each — without losing the institutional knowledge embedded in the existing code.

**Debugging with AI.** Describing error patterns, stack traces, and unexpected behaviour to AI as a first-pass diagnostic step. How to get useful signal even when the model doesn't know your system. How to reduce the interrupt cost on senior engineers from junior debugging questions.

**Safe incremental improvement.** How to add test coverage to untested legacy code using AI to generate tests, then use those tests to refactor safely.

**Where AI gets confused in legacy code.** The specific failure modes — outdated patterns, framework-specific behaviour, implicit domain assumptions — and how to work around them.

## What's Not Covered

I want to be explicit about this, because scope clarity avoids disappointment.

The workshop does not cover AI product features — building chatbots, implementing RAG, deploying AI models. That's a different skill set. What I cover is using AI in the software development process itself.

The workshop does not cover AI strategy or ROI analysis. I'm not a management consultant. If you need a business case built for AI investment, that's a different engagement.

The workshop does not give you a tool you install and forget. What it gives you is a set of practices your team knows how to run. The ongoing discipline is yours.

## Who Benefits Most

The developers who get the most from this kind of workshop share a few traits:

**Experienced engineers who've been avoiding AI.** The 5-10-year engineers who have strong instincts but haven't made AI a habit. They're the hardest to reach through self-directed learning because they're busy, because the learning curve feels like regression, and because the initial results from casual AI use are often underwhelming enough to confirm their scepticism. A structured, hands-on environment with a practitioner who understands their context changes this.

**Teams with mixed projects.** The workshop's two-track structure is specifically designed for teams that work on both new features and legacy maintenance. Most teams do both. Generic AI content doesn't address the legacy problem at all.

**Teams that need shared vocabulary.** One underrated benefit of a workshop over individual self-learning: everyone learns the same things. Code review conversations change when both the reviewer and the reviewee know what "AI pre-review" means and have used the same templates. Shared practice is more valuable than individual practice.

## Who This Is Not For

Being clear about who shouldn't hire me is more useful than persuading everyone.

**Teams without an existing software engineering foundation.** This isn't an intro to programming with AI. Your developers need to be able to evaluate generated code. If they can't yet, they'll use AI in ways that create technical debt they can't see.

**Teams looking for a one-hour keynote.** What I do is three days of hands-on work. If you want an inspirational talk about the future of AI, there are excellent speakers for that. What I offer is different.

**Teams that want AI decisions made for them.** The workshop transfers knowledge and practice — it doesn't come with a mandate about which tools to use or a roadmap to implement. Your team makes its own choices after. If you need someone to run your AI implementation, that's a consulting engagement, not a workshop.

**Teams where the decision-makers don't believe AI is relevant.** If the workshop is happening because someone above insisted on it and the team is being sent, the psychological safety conditions for real learning won't be there. The best results happen when at least the tech leads are genuinely curious.

## The Business Case

I'll make this concrete, because abstract ROI claims are useless.

A senior developer costs somewhere between 150,000 and 250,000 EUR per year in total cost, depending on location and seniority. If AI-assisted development workflows save two hours per week — a conservative estimate, based on what I observe in my own team — that's roughly 100 hours per year per developer. At full cost, that's 7,000-12,000 EUR per developer per year in recovered time.

For a team of 10 developers, that's 70,000-120,000 EUR per year if the habits hold.

The workshop doesn't guarantee those numbers. No responsible practitioner would. What it does is give your team the specific knowledge and shared practice to make those habits achievable — instead of leaving it to each developer to figure out on their own, some never getting there.

The investment in a workshop is a fraction of one developer's annual cost.

## What Happens Before and After

**Before:** A one-hour discovery conversation. I want to understand your stack, your team's current relationship with AI tools, your project mix (greenfield vs. legacy), and what you're most hoping to address. The workshop content gets adjusted based on this — I don't run the same three days for every team.

**During:** Three full days, on-site or remote (your preference). Hands-on from the start. Participants work in their own development environments, with their own code where possible. Small group exercises, live demos, Q&A built in throughout.

**After:** Optional two-week check-in. An async structure where participants share what they've tried, what's working, what's stuck. Based on what I observed after the Insly workshops, the check-in period is when a second wave of questions emerges — the ones that only arise after people have tried things in their real work context.

## FAQ

**Can this be done remotely?** Yes. I've run full workshops remotely. The hands-on work translates well to remote. The social/psychological dimension — the normalisation of experimenting in front of colleagues — requires more deliberate facilitation remotely, and I've adapted for that.

**What's the minimum team size?** I've found the sweet spot is 8-20 people. Fewer than 8 and the group dynamic that makes shared learning valuable doesn't fully emerge. More than 20 and the ability to give individual attention to what people are struggling with drops off.

**Do you work with non-Polish companies?** Yes. I'm based in Poland and most comfortable in Polish-language environments, but I run workshops in English and have done so across European markets.

**Our codebase is old and messy — is that a problem?** It's actually the more interesting case, and the one I've thought hardest about. The Track 2 content is specifically designed for that situation. "Our code is too old for AI" is a statement I've heard many times and found to be wrong in most cases.

**What tools do you assume?** Cursor for development, Claude for general AI assistance, specific tooling varies by stack. I'm not tool-agnostic in a "whatever works for you" way — I have opinions, and I share them. But I'll work with what your team already has where it makes sense.

## How to Get in Touch

If this sounds relevant to your team, the right first step is a 30-minute conversation — no pitch deck, no proposal, just a conversation about whether this makes sense for your situation.

Message me directly with the word **WORKSHOPS** (or **WARSZTATY** if you're in Poland). I'll reply and we'll schedule the call.

If you want to talk before committing to that step, leave a comment here or on the LinkedIn post. I read everything.
