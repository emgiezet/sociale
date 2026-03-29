---
day: 12
title: "I've contributed to a project with 18 million installs. Here's what open source taught me about production code."
pillar: Builder
format: Open source
language: English
scheduled_date: 2026-04-07
posting_time: "07:30 CET"
hashtags: ["#OpenSource", "#SoftwareEngineering", "#PHP", "#Symfony"]
image: ./images/day-12.jpg
image_unsplash_query: "open source code collaboration github"
cta: Follow if you believe in open source
---

I've contributed to a project with 18 million installs. Here's what open source taught me about production code.

The project is SonataAdminBundle, a Symfony/PHP admin interface used by developers across the world. I've been contributing for years. 18 million installs means your change runs in production environments you'll never see, on stacks you can't predict.

That kind of scale changes how you think about code.

The first lesson was backward compatibility. In a normal codebase, you can refactor and update callers. In open source with millions of installs, a breaking change creates real damage for real people. You learn to think about deprecation paths, migration notes, and the cost of convenience.

The second lesson was code review at scale. Contributors come with different backgrounds, different standards, different assumptions. Reviewing a PR stopped being about "is this correct" and started being about "can someone who doesn't know our history maintain this in two years."

The third lesson was ruthlessness about scope. A good open source maintainer says no more than yes. Every feature someone wants is a feature someone else will have to debug, document, and support for a decade 🫠

I brought all of this into my day job at Insly. When I design internal APIs for my team, I think about the developer using it at 11pm during an incident. When I merge code, I think about who reads this in six months.

**The best education in production-quality software is writing code that thousands of strangers depend on.** Nothing keeps you honest like a GitHub issue from someone in a timezone you've never heard of 🌍

Follow if you believe in open source, and what it teaches you beyond the commits.

#OpenSource #SoftwareEngineering #PHP #Symfony
