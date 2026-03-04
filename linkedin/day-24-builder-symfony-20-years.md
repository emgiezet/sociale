# Day 24 — Builder: Symfony at 20 Years
**Pillar:** Builder | **Week:** 5 | **CTA:** Comment

---

## LinkedIn Post

Symfony is 20 years old.
Here's why it's still the backbone of enterprise PHP — and what AI developers can learn from it.

I've been writing Symfony applications since before some of my current team members started university. I've watched frameworks come and go. Symfony stayed because it got something right that most frameworks get wrong.

**What Symfony got right:**

→ **It's a set of components, not a monolith.** You can use Symfony's HTTP kernel without its form component. You can use its dependency injection container in a non-Symfony application. This composability is why Symfony components underpin half the PHP ecosystem — including Laravel, which uses several.

→ **Backwards compatibility as a first principle.** The deprecation lifecycle is clear: deprecate with warnings in version N, remove in version N+2. SonataAdminBundle, a project I contribute to with 18 million installs, survives precisely because the Symfony foundation doesn't break things under you.

→ **It rewarded learning the fundamentals.** Learning Symfony properly meant learning dependency injection, event systems, service containers, HTTP semantics. These concepts transferred everywhere.

**What AI developers can learn from this:**

The AI framework ecosystem is in its 2006 moment — proliferating, opinionated, changing fast. Most of today's AI frameworks will be deprecated or abandoned in five years.

The concepts — embeddings, retrieval, context management, tool use, evaluation — won't be. Learn them properly.

→ Understand how transformers produce embeddings before you pick an embedding library
→ Understand retrieval mathematics before you optimize your vector store
→ Understand evaluation methodology before you trust a benchmark

**Technology stacks change. Engineering fundamentals don't.**

What's the framework or technology that shaped how you think about software more than any other?

#Symfony #PHP #SoftwareEngineering #AIEngineering #OpenSource

---

## Blog Post

### Symfony at 20: What Its Longevity Teaches Us About Building Durable Software

Twenty years is a geological age in software. Most frameworks launched in 2005 are either dead or existing as legacy liabilities that someone is slowly migrating away from. Symfony is still actively developed, still widely deployed in enterprise PHP applications, and still architecturally relevant.

Understanding why Symfony survived and thrived when most of its contemporaries didn't reveals patterns that apply far beyond the PHP ecosystem — including to the AI framework landscape that's currently in its early proliferation phase.

#### The Composability Principle

The most consequential decision in Symfony's architecture is one that's easy to underappreciate: Symfony is a collection of independent components, not an integrated monolith.

You can use Symfony's HTTP Kernel without its Form component. You can use its DependencyInjection container in a non-Symfony application. You can use its EventDispatcher, its Console component, its Security component — each independently of the others. Each component has its own semantic versioning, its own documentation, its own install base.

This composability is why Symfony components underpin a much larger portion of the PHP ecosystem than the framework itself. Laravel, the most popular PHP framework, uses multiple Symfony components. Drupal is built on Symfony. Magento uses Symfony components. Projects that chose different frameworks still ended up depending on Symfony because specific components were the best available implementation of a specific capability.

The composability also means that Symfony has been able to evolve without forcing wholesale migration on every user. A project that uses only Symfony's HTTP kernel and DependencyInjection components can upgrade those components independently of the rest of the ecosystem.

Contrast this with frameworks that bundle everything — where a major version upgrade requires touching every part of the application that touches the framework. These frameworks create high upgrade friction, which means projects stay on old versions, which means security vulnerabilities accumulate, which means the framework acquires the reputation of being a legacy system even when it's actively maintained.

#### Backwards Compatibility as a Social Contract

Symfony's backwards compatibility promise is unusually explicit. The policy: deprecate in version N, maintain with deprecation warnings through version N+1, remove in version N+2. This two-major-version runway is specified in writing and enforced through code.

For SonataAdminBundle, a Symfony admin framework I contribute to that has over 18 million Packagist installs, this backwards compatibility contract is what makes ongoing maintenance sustainable. Symfony's core doesn't break SonataAdminBundle under us. We have time to prepare for changes. Our users have time to prepare for our changes.

The social and engineering discipline required to maintain this contract is significant. It means that design mistakes can't simply be corrected — they have to be deprecated, maintained in parallel with their replacements, and removed on a schedule. It means that the public API surface is carefully considered before it's exposed, because everything exposed becomes a commitment.

This discipline produces better API design. When you know you can't easily remove something, you think harder about whether it should exist in its current form.

#### Teaching Fundamentals, Not Just Usage

The best educational side effect of learning Symfony properly was that it required understanding concepts that weren't Symfony-specific: dependency injection, the service container pattern, event-driven architecture, HTTP semantics, middleware patterns.

Learning Symfony well in 2012 meant learning ideas that were directly applicable to building distributed systems in 2016, to microservice architecture in 2018, and to understanding how modern JavaScript frameworks manage component composition in 2020.

The frameworks that optimize for "get started in 5 minutes" without explaining the concepts behind their abstractions produce developers who are framework-dependent rather than conceptually fluent. Those developers struggle when the framework is deprecated or when they need to debug behavior that the framework's abstractions are hiding.

#### The Lesson for AI Framework Adoption

The AI developer tooling landscape in 2026 looks like the PHP framework landscape in 2007: multiple frameworks competing for mindshare, each with strong opinions, each with early adopters publishing enthusiastic comparisons, and most of them destined to be deprecated or absorbed by something else within five to seven years.

LangChain, LlamaIndex, AutoGPT, CrewAI, Swarm — these are today's CodeIgniter, CakePHP, and Yii. Some will survive and become foundational. Most will be legacy choices by 2030.

What won't be deprecated: the concepts. Embeddings and vector similarity search. Retrieval-augmented generation as a pattern. Context management in long-horizon reasoning. Tool use and function calling. Evaluation methodology for probabilistic systems.

The developer who learns LangChain deeply but doesn't understand how transformer-based embedding models actually work will be lost when LangChain is replaced. The developer who understands why embeddings encode semantic relationships, how cosine similarity works as a retrieval metric, and what the tradeoffs are between dense and sparse retrieval — that developer will adapt to whatever the next framework is.

Learn the frameworks. Ship with them. But learn the fundamentals first, and always keep your understanding grounded at the level of concepts, not just APIs.

Symfony's longevity is ultimately a lesson about building on stable foundations. The PHP language is a stable foundation. HTTP is a stable foundation. Dependency injection as a design principle is a stable foundation. The specific APIs Symfony provides are built on top of those stable foundations.

For AI development: transformer architectures, retrieval mathematics, evaluation methodology — these are the stable foundations. The APIs and frameworks will keep changing. The foundations are worth learning deeply.

What's the technical concept you've learned that has stayed relevant across the most technology changes? I'm curious what the longevity leaders are in different domains.
