---
day: 4
title: "What 20 Years of Stacking Languages Taught Me About Learning AI"
pillar: Trenches
language: en
image: ../../images/day-04.jpg
image_unsplash_query: "programming code learning career"
---

# What 20 Years of Stacking Languages Taught Me About Learning AI

I wrote my first production PHP application in 2007. I deployed my first production RAG system in 2024. The distance between those two points isn't a straight line, and the things I learned in the detours are exactly what made the destination possible.

This is the story of a non-linear path from enterprise PHP to production AI — and what each stop taught me that I couldn't have learned any other way.

## PHP: The Foundation That Actually Holds

Let me get the elephant out of the room. PHP gets mocked. It deserves some of that. Early PHP was a mess. But for developers who went deep enough, PHP in the Symfony era was an extraordinary education in software engineering principles.

I spent 15 years writing Symfony applications. In that time, I learned dependency injection not as a pattern to memorize but as a solution to a problem I'd hit repeatedly. I learned that clean architecture isn't about following rules — it's about making the right changes easy. I contributed to SonataAdminBundle, an open-source Symfony project that now has over 18 million installs. Working on a project at that scale teaches you things about backwards compatibility, API design, and community maintenance that no course can replicate.

The most important thing PHP taught me: the language is not the point. The engineering thinking is the point. When people ask me if I regret the PHP years, I say no. They made me an engineer. Everything after was specialization.

I also learned that "boring" technology that ships reliably beats "exciting" technology that doesn't. Symfony isn't glamorous. But it's predictable, well-tested, and has a community that has collectively solved the same problems you're about to face. I still believe that principle applies everywhere.

## Python: The Value of Fast Feedback

When I moved into ML-adjacent work, Python was the obvious choice. The ecosystem for machine learning, data processing, and AI research is built there. But Python taught me something less obvious than "use PyTorch."

It taught me about feedback loop speed.

The combination of interactive notebooks, dynamic typing, and a package ecosystem that covers almost everything means that in Python, you can go from idea to running experiment in minutes rather than hours. That changes how you think about exploration. You prototype more. You discard more. You find the right approach faster.

This mental shift — prototype aggressively, evaluate ruthlessly, commit only when you know what you're building — became central to how I approach AI work. The architecture of our first RAG prototype at Insly went through three complete redesigns in two months. That would have been paralyzingly slow in a compiled language. In Python on Jupyter, it was fast enough to actually teach us something.

I didn't switch to Python because it was better in some abstract sense. I switched because the libraries I needed — for embedding models, vector operations, ML experimentation — didn't exist elsewhere in a useful form. Lesson: follow the ecosystem that solves your actual problem, not the one that wins Twitter arguments.

## Go: The Discipline of Constraints

Go was a side education in constraints. The language deliberately removes options. No generics (for a long time), no class-based inheritance, limited exception handling. When I first wrote Go, it felt limiting. Two years later, I understood what the designers were doing.

Constraints force deliberate design. When you can't reach for a framework to solve every problem, you think harder about the problem. Go services I've built are smaller, simpler, and more maintainable than their Python equivalents — not because Go is better, but because Go's constraints wouldn't let me add complexity I didn't need.

Go also changed how I think about error handling. In Go, errors are explicit return values. You can't ignore them without deliberately writing code to do so. That discipline — acknowledge every failure path, handle it explicitly or consciously decide not to — is exactly the mental model needed for production AI systems, where failures are probabilistic and often silent.

This mindset carried into AI systems design directly. The temptation in AI projects is to add complexity — more agents, more vector stores, more retrieval strategies — because the tooling makes it easy. The discipline is to ask whether the complexity is solving a real problem or just making the demo more impressive.

## AI: A Paradigm Shift, Not Another Language

When I started building AI systems in earnest, I quickly learned that the transition wasn't primarily about learning new tools. It was about learning new failure modes.

Traditional software fails in ways you can test for. Given input X, expect output Y. If Y is wrong, your test suite tells you. If the system crashes, you have an error log.

AI systems fail differently. They fail probabilistically. They fail in ways that look like success at first glance — a confident, fluent, syntactically perfect answer that happens to be wrong. These failures don't show up in your error logs. They show up in user complaints, in quality reviews, in the slowly building realization that your system has a blind spot you didn't know about.

Everything I'd learned about building robust software — defensive design, evaluation infrastructure, observability, feedback loops — became more important in AI work, not less. The developers I've seen struggle most with the transition are the ones who thought "I just need to learn the new APIs." The ones who succeed are the ones who brought their full engineering experience and applied it to the new paradigm.

The engineers who stay relevant aren't the ones who picked the right language. They're the ones who kept moving when the problem changed.

## The Career Lesson

Your path doesn't need to be linear. The detours are curriculum.

If you're a PHP developer wondering whether your background is enough to work in AI: it is. The Symfony principles — dependency injection, SOLID design, testable interfaces — map cleanly to building production AI systems. The engineering discipline you've built up is exactly what AI development needs more of.

If you're earlier in your career and optimizing for the "right" language or the "right" stack: stop. Learn the fundamentals. Build things. Ship them. The specific technologies will change every five years. The engineering thinking transfers forever.

I'm still learning. Every day in AI work, I encounter something I don't know. But I have 20 years of context for how to learn it — and that, more than any specific skill, is the real return on a non-linear career path.
