# Day 12 — Builder: 18 Million Installs
**Pillar:** Builder | **Week:** 3 | **CTA:** Follow

---

## LinkedIn Post

I've contributed to a project with 18 million installs.
Nobody knows my name. That's fine.

SonataAdminBundle is an open-source administration framework for Symfony PHP applications. I've been contributing to it for years. It has over 18 million Packagist installs.

Most of my contributions will never be mentioned in anyone's conference talk. Some are tiny bug fixes. Some are documentation clarifications. Some are API improvements that took hours to think through and five lines to implement.

Here's what contributing to a large OSS project taught me about software at scale:

→ **Backwards compatibility is a constraint that changes how you think.** When 18 million people might depend on your code, you can't just refactor because refactoring is elegant. Every public API is a promise.

→ **Code review at this scale is a different discipline.** Maintainers of major OSS projects review contributions from people whose full codebase they'll never see. You learn to evaluate a PR in isolation — does this solve the stated problem? Does it introduce edge cases? Is it consistent with the existing API design?

→ **Documentation is code.** An undocumented feature doesn't exist for most users. The work of making software legible — through docs, examples, error messages, and naming — is engineering work, not afterthought.

→ **The community is the product.** The reason SonataAdminBundle is useful isn't only the code. It's the ecosystem: the Stack Overflow answers, the blog posts, the Discord channels, the community-maintained extensions. Healthy communities compound.

I bring all of this into my work at Insly — especially the backwards compatibility discipline. When you have 150,000 users depending on your platform, every API change is a backwards compatibility problem.

**The best engineering education I never paid for was contributing to open source.**

What OSS projects have shaped how you think about software?

#OpenSource #Symfony #SonataAdminBundle #SoftwareEngineering #PHP

---

## Blog Post

### What 18 Million Installs Taught Me About Engineering at Scale

I won't be famous for my contributions to SonataAdminBundle. The project has 18 million installs on Packagist. My name appears in the contributors list alongside dozens of other engineers who've shaped the project over the years. Nobody is going to write a blog post about my specific changes.

This is exactly as it should be, and it's exactly why contributing to large open-source projects is one of the best engineering educations available.

#### What SonataAdminBundle Is

SonataAdminBundle is an administration framework for Symfony — the PHP web framework I've used for most of my career. It provides a feature-rich, configurable admin interface for CRUD operations on Doctrine entities. It's widely used in enterprise PHP applications across Europe and beyond.

I started contributing after using it extensively in production at several companies. The "I see how I'd improve this" impulse is, I think, what draws most OSS contributors in. You hit a limitation, you understand the codebase well enough to see a solution, and you decide to contribute the fix rather than maintain a local patch.

#### Lesson 1: Backwards Compatibility Changes How You Think

The first major lesson from contributing to a widely-used project: when your code is running in production at tens of thousands of installations, backwards compatibility isn't a nice-to-have. It's a first-class constraint that shapes every decision.

In my own projects, when I want to rename a method or change an API signature, I just do it. I find all the call sites, update them, done. In SonataAdminBundle, a method rename means every user who has extended that class or called that method is affected. Their code breaks. Their admin panel breaks. They have to spend time investigating and updating.

The discipline of writing for backwards compatibility changes how you think about API design from the start. You think harder about naming before you name it, because renaming later is expensive. You think harder about the interface surface you're exposing, because every public method is a commitment. You think harder about deprecation paths — how do you evolve an API over time in a way that gives users a migration path rather than a breaking change?

At Insly, this discipline directly improves how we design our internal APIs and our integrations with third-party systems. When 150,000 users depend on your platform, your API changes are their breaking changes.

#### Lesson 2: Code Review at Scale Is a Different Discipline

As a contributor, your pull request will be reviewed by maintainers who don't know your full codebase, don't know your use case in detail, and are reviewing your change in isolation. This is a clarifying constraint.

Good PRs for major OSS projects need to be self-contained arguments. The description explains the problem, why the current behavior is wrong or incomplete, and why the proposed solution is the right approach. The code changes are minimal, focused, and don't introduce side changes that obscure the intent. The tests demonstrate that the fix works and doesn't break existing behavior.

Writing PRs to this standard has made me better at code review in my own team's work. I've started applying the same standard to my team's code review culture at Insly: each PR should be a complete argument for a specific change, with enough context that a reviewer who doesn't know the feature can evaluate it correctly.

#### Lesson 3: Documentation Is Code

A feature that exists in the code but not in the documentation effectively doesn't exist for most users. This sounds obvious. It wasn't obvious to me early in my career.

In SonataAdminBundle, I've made contributions specifically to documentation — explaining features that existed but weren't clearly documented, adding examples for configuration options that were described only in abstract terms. These contributions have high leverage: they help every user who encounters the documented feature, not just the ones sophisticated enough to read the source code.

This lesson carries into how I run engineering at Insly. Internal documentation — ADRs (Architecture Decision Records), runbooks, API documentation — is treated as engineering work, scheduled in sprints, and reviewed as rigorously as code. An undocumented decision is a future debugging session waiting to happen.

#### Lesson 4: The Community Is the Product

The last and most counterintuitive lesson: for an OSS project, the community is as important as the code.

SonataAdminBundle's value comes not just from what the code does but from the ecosystem around it: the Stack Overflow answers, the blog tutorials, the Discord community, the third-party extensions, the companies that have adopted it as a standard. A library with identical features but no community would be far less useful than SonataAdminBundle.

This maps to any technical platform. At Insly, we have an ecosystem of integration partners, resellers, and power users who extend and distribute our platform. The health of that ecosystem — the documentation, the developer experience, the responsiveness to questions — is as important to our business as the features we ship.

The codebase is what runs. The community is what compounds.

#### Why You Should Contribute

If you've been thinking about contributing to open source but haven't started: start small. Find a project you use. Find an issue tagged "good first issue." Fix a documentation error. The meta-skills — writing clear PR descriptions, understanding API design constraints, working with strangers on a shared codebase — are worth developing regardless of whether your contribution is famous.

The best engineering education I never paid for was contributing to open source. The skills transferred directly to my production work. And occasionally, knowing that code you wrote is running in 18 million production environments is its own quiet satisfaction.
