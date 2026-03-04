# Day 1 — Builder: Leading an AI Team in Insurance
**Pillar:** Builder | **Week:** 1 | **CTA:** Follow

---

## LinkedIn Post

I lead 11 engineers building AI for insurance.
Nobody told us it would be this hard.

We're not building demos. We're shipping RAG systems that process real insurance documents, where mistakes have legal consequences and your CI/CD pipeline is one misconfiguration away from a compliance violation.

Here's what nobody tells you before you start:

→ Insurance data is messy in ways that break your retrieval precision fast. Policy documents, endorsements, claims forms — the structure varies by broker, by country, by year. Your chunking strategy will fail on real data even when it worked fine on PDFs from the internet.

→ The business doesn't care about your RAG architecture. They care whether the underwriter can find the right clause in 3 seconds instead of 3 minutes. Everything else is noise.

→ AI in a regulated industry isn't slower because people are risk-averse. It's slower because you're accountable. There's a difference. Embrace it.

I've been leading engineering teams for over a decade. I've shipped Symfony monoliths, microservices, mobile payment apps, integrations with 150,000 users. None of it prepared me for what it means to have an LLM be part of your production system.

Not because AI is magic. Because the failure modes are different.

When a traditional API fails, you get an error. When a RAG system degrades, you get a confident-sounding wrong answer. That's a harder bug to catch and a harder story to tell your product team.

**The teams that win with AI aren't the ones who move fastest. They're the ones who build the right feedback loops.**

I'm going to be sharing what I'm learning here every day for the next 30 days — real stories, real mistakes, real architecture decisions.

If you're building AI in a production environment (or trying to figure out where to start), follow along.

#AIEngineering #InsurTech #RAG #TechLeadership #ProductionAI

---

## Blog Post

### What I Wish Someone Had Told Me Before Leading an AI Team in Insurance

Eighteen months ago, I stood in front of my 11-person engineering team and said something I'd never said before: "I don't fully know what we're building yet."

We were six months into experimenting with AI at Insly — a European insurance software platform serving over 150,000 users — and I was starting to understand that the challenges ahead weren't technical in the way I expected. They were different. Stranger. Harder to quantify.

I've been building software for 20 years. I've led teams through Symfony migrations, microservice transitions, and a zero-downtime SSO integration for 150,000 users. I know what hard looks like in traditional engineering. AI-in-production is hard in a different register.

This post is what I wish someone had told me at the start.

#### The Data Problem Nobody Warns You About

When you read RAG tutorials, you get clean PDFs. Well-structured documents. Sensible chunk sizes. Everything retrieves nicely.

Insurance data isn't like that.

At Insly, we process documents from dozens of brokers across multiple European markets. Policy documents that were formatted in Word 2003. Endorsements scanned from paper and OCR'd by a system that's been running since 2011. Clause libraries that use different terminology depending on which country they were written for.

Our first RAG prototype worked beautifully on our test dataset. It fell apart immediately on production data. Not catastrophically — it just started returning the wrong clause, with full confidence, for edge cases that showed up constantly in real use.

We spent two months rebuilding our chunking and retrieval strategy. What we learned: your data preparation is 60% of the work. The model is the easy part.

#### The Compliance Asymmetry

In most software, a bug produces an error. An exception is thrown. The system fails visibly. You fix it.

In a RAG system deployed in insurance, the failure mode is different: the system produces a confident, fluent, syntactically perfect wrong answer. No error log. No exception. Just an underwriter trusting a recommendation that was built on a retrieval miss.

This asymmetry shapes everything about how you build. You can't just measure "does it return an answer." You have to measure "is the answer grounded in what we actually gave it." That requires evaluation infrastructure, human review loops, and a feedback mechanism that most tutorials don't cover.

We built ours on AWS Bedrock, combining Bedrock Knowledge Bases for baseline retrieval with custom LightRAG integration for more complex document relationships. The evaluation layer took longer to build than the retrieval layer.

That's the right order of priorities. It just doesn't feel that way at the start.

#### What the Business Actually Cares About

Early in our AI work, I spent a lot of time talking about embedding models, retrieval precision, context window sizes. The product managers I worked with had a very simple question: "Can the underwriter find the right clause faster?"

That's it. That's the metric.

Everything else — the architecture, the model choices, the chunking strategy — is invisible infrastructure. The business sees outcomes. You measure outcomes. You build toward outcomes.

This sounds obvious. It isn't. When you're deep in the technical work, it's easy to optimize for the wrong thing. I've caught myself spending a week tuning retrieval precision when the actual user complaint was about UI — how the result was presented, not what was retrieved.

The feedback loop between "what we built" and "what the user experiences" needs to be short, explicit, and regular. We run weekly demos with actual underwriters. Not product managers interpreting what underwriters want — actual underwriters, clicking through the system, narrating their experience.

It changed how we built faster than anything else.

#### The Team Dimension

There's a leadership challenge specific to AI projects that I haven't seen written about much: your team is learning the technology at the same time they're building with it.

In traditional engineering, when I assign a task to a senior developer, I have a good mental model of how long it will take and what the risks are. With AI work, there's a research layer that's genuinely unpredictable. "How does LightRAG handle this document structure?" isn't a question with a known answer. You have to try it.

This changes how you plan sprints, how you set expectations with stakeholders, and how you protect your team from the pressure of deadlines on exploratory work.

The teams that win with AI aren't the ones who move fastest. They're the ones who build the right feedback loops — between engineers and users, between experiments and decisions, between what the model can do and what the business actually needs.

#### Starting Here

Over the next 30 days, I'm sharing what I'm learning — architecture decisions, team dynamics, specific tools, production war stories. Real accounts from the trenches of deploying AI in a regulated industry.

If you're a developer trying to figure out where AI fits in your career, a tech lead trying to move your team in this direction, or a builder in a highly regulated industry wondering if this is even possible: follow along. This is the content I wish I'd had 18 months ago.

You can find me on LinkedIn where I post every weekday. The conversation in the comments is often better than the post — bring your questions.
