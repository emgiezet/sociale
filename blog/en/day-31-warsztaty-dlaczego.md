---
day: 31
title: "Why Experienced Developers Fear AI (And Why I Ran Workshops to Fix It)"
pillar: Trenches
language: en
image: ../../images/day-31.jpg
image_unsplash_query: "developer team workshop coding discussion"
---

# Why Experienced Developers Fear AI (And Why I Ran Workshops to Fix It)

Fifteen developers. Twenty years of combined experience. And a palpable, honest fear of AI.

That's what I walked into when I proposed running AI workshops at Insly. I expected enthusiasm — or at least curiosity. What I got instead was something more valuable: candor.

One of the seniors — twelve years in the industry, genuinely one of the best engineers on the wider team — said it plainly: "I don't know where to start. And honestly, I'm a bit scared that if I try, I'll find out I can't do it."

That sentence stopped me. Not because it was surprising, but because it was so honest. And because I knew, from eighteen months of building AI systems in production, that his fear was rooted in something real.

This is the story of why I ran those workshops — and what I learned about experienced developers and AI before we'd even started.

## It's Not About Skill. It's About Uncertainty.

There's a specific kind of discomfort that comes when a tool appears that seems like it should rewrite your value proposition. Senior developers have spent years building expertise in a craft — architecture, debugging, code review, system design — and suddenly there's a technology that seems to threaten all of it.

The reaction isn't usually panic. It's something quieter and more paralyzing: not knowing where the threat is exactly, and therefore not knowing how to respond to it.

I work at Insly, a European InsurTech SaaS with 150,000+ users. My team of eleven engineers has been building AI systems in production for eighteen months — RAG pipelines, LLM integrations, AWS Bedrock, LightRAG. I see daily what works, what fails, and where the real complexity lives.

But the other fifteen developers at Insly? The engineers working with production code, legacy systems, daily feature work? For them, AI was somewhere in the distance. Something they'd heard about. Something they felt they "should learn" but had no concrete path toward.

The gap between those two realities — between people actively building AI and people uncertain where to begin — was the gap the workshops were designed to close.

## The Specific Fears I Heard

Before we started, I sat with several engineers informally and just listened. Three things came up repeatedly.

**"Our codebase is too old for AI."**

The Insly stack includes PHP/Symfony systems that go back to 2012 and 2015. Legacy in the most real sense: systems that work, that are mission-critical, and that no one fully understands end-to-end anymore. The fear was that AI tools were designed for greenfield projects — clean, well-typed, well-documented — and would be useless against decade-old enterprise code.

This fear is understandable. It's also wrong. But it requires demonstration, not argument, to overcome.

**"I don't know if it's safe to paste code into ChatGPT."**

This is a reasonable concern, and it reflects something important: these are engineers who care about their professional obligations. Insly handles sensitive insurance data. The instinct to be cautious before uploading proprietary code to a commercial AI API is the right instinct. The fear wasn't ignorance — it was responsibility.

The answer here isn't "just do it." It's: here's how to think about what's safe to share and what isn't. Here's what privacy settings and enterprise tiers mean. Here's how to use AI tools without violating your obligations.

**"If AI writes the PR, how do I know it's right?"**

This was the deepest fear, and the most interesting one. Underneath it was a question about judgment: if AI produces code, and I accept it without fully understanding it, have I done my job? Am I still the engineer, or have I become a reviewer of AI output — and what does that mean for my expertise?

This fear isn't irrational. It reflects a genuine tension in AI-assisted development: the tools are useful precisely because they're faster than thinking from scratch, and that speed creates the temptation to accept outputs without the scrutiny you'd apply to your own work.

The answer to this one takes longer to develop. It's about building the judgment to evaluate AI output — not accepting blindly, not rejecting on principle, but learning to see clearly.

## Why Ignoring It Isn't an Option Anymore

I'm not going to make grand claims about AI replacing developers. That conversation is tired and mostly unhelpful. But I am going to say something simpler: the developers who learn to use these tools well will be able to do more, debug faster, understand unfamiliar code more quickly, and write tests for systems they've never touched.

The gap between developers who use AI well and developers who don't is widening. It's not a crisis yet — but it will be in two years, and the time to learn is before you're behind.

For a team working on a product serving 150,000+ users in a regulated industry, that gap is also a business risk. If the people building the product don't understand the tools transforming their domain, they're less equipped to make good architectural decisions, less equipped to evaluate AI features in the product, and less equipped to lead the work well.

This isn't about replacing human judgment with AI. It's about giving experienced engineers better tools so their judgment has more leverage.

## What the Workshops Were Designed to Address

I designed the workshops around the specific fears and gaps I'd identified — not around a generic AI curriculum.

**Practical from minute one.** No hour-long slide decks. We opened IDEs in the first session and looked at real code. The goal was to move from abstract uncertainty ("I don't know how to use AI") to concrete experience ("I just watched AI explain this function, and I can see where it got it right and where it's uncertain") as fast as possible.

**Split into two tracks.** New projects and legacy systems have different challenges. Engineers working on greenfield features have one set of concerns; engineers maintaining Symfony code from 2013 have another. Merging these into one workshop would have served neither well.

**Covering safety and judgment, not just capability.** The question "is this safe?" deserved a real answer, not dismissal. And the question "how do I know if AI-generated code is good?" deserved a practical framework, not a philosophical answer.

**Built around the actual stack.** Specific tools for PHP/Symfony development. Specific techniques for understanding legacy code. Specific approaches for the kind of regulated-industry constraints that Insly operates under. Generic workshops about ChatGPT wouldn't have been useful — these needed to address the actual context.

## The Thing I Didn't Expect

The most important realization I had — before the workshops even started — was that the fear wasn't a sign of weakness. It was a sign of seriousness.

Experienced developers who are afraid of AI aren't afraid because they're incompetent. They're afraid because they understand that expertise is built carefully, and they don't want to shortcut it in ways they'll regret. They're afraid because they care about the quality of their work and are uncertain how AI fits into that care.

That's the right instinct. The right response isn't to push through the fear carelessly — it's to give it a proper answer.

The workshops were my attempt to provide that answer: here's what AI actually does well, here's where it will mislead you, here's how to use it in a way that extends your expertise rather than shortcutting it.

Whether that answer landed the way I hoped — that's what the rest of this series is about.

---

*This is the first post in a series about AI workshops I ran for fifteen developers at Insly. Follow along for the full breakdown: agenda, techniques, the legacy code breakthrough, what changed and what didn't.*
