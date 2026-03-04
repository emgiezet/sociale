# Day 11 — Trenches: Vibecoding Won't Kill Developers
**Pillar:** Trenches | **Week:** 3 | **CTA:** Opinion/Comment

---

## LinkedIn Post

Vibecoding won't kill developers.
But it will kill developers who refuse to adapt.

I gave a talk about this. The room had strong opinions before I finished the first slide.

Here's what I actually think, after 20 years in software engineering and 18 months building AI systems:

Vibecoding — using AI to generate code by describing intent — is a productivity tool. A powerful one. But it's not engineering judgment.

Here's the difference:
→ A junior developer vibecoding generates code. A senior developer vibecoding generates code AND evaluates it, refactors it, and knows when to throw it away.
→ Vibecoding can produce working code. It rarely produces appropriate code — code that fits the team's conventions, the system's constraints, the product's requirements.
→ The more complex your system, the less vibecoding helps and the more it can hurt. Generating a 50-line utility function: great. Generating an architectural change to a multi-tenant insurance platform: dangerous.

What dies: the developer who treats programming as typing code. If your value was "I can produce syntax faster than others," AI already won.

What survives: the developer who treats programming as solving problems. Architecture, system design, code review, debugging, team coordination, domain knowledge — these are not vibecoded.

What grows: the developer who learns to pair their judgment with AI's speed. Code faster. Test faster. Iterate faster. Stay in the loop.

**The threat is not that AI writes code. The threat is that some developers will use AI as a reason to stop developing judgment.**

What do you think? Is vibecoding a productivity multiplier or a shortcut to technical debt?

#SoftwareEngineering #AIEngineering #DeveloperProductivity #Vibecoding #TechLeadership

---

## Blog Post

### Vibecoding: Productivity Multiplier or Judgment Atrophier?

I gave a talk recently that I titled "Is This the End of the Developer Era?" It was framed as a question, which I did intentionally — because I don't think the honest answer is simple.

The audience expected me to either celebrate AI coding tools as a revolution or dismiss them as hype. What I actually believe is more specific and, I think, more useful than either position.

#### What Vibecoding Is

"Vibecoding" is the practice of describing to an AI what you want code to do, in natural language or rough pseudocode, and having the AI generate it. The term originated as a somewhat tongue-in-cheek description of a real workflow that increasing numbers of developers use daily.

It's genuinely powerful. For writing boilerplate, generating test cases, implementing well-understood patterns, translating between languages, refactoring repetitive code — AI coding assistants have changed what a single developer can produce in a day. I use them. My team uses them. Anyone who tells you they don't is either in a particularly restricted environment or not being honest.

But "powerful for many tasks" is not the same as "changes what it means to be a good developer."

#### What Vibecoding Doesn't Do

Vibecoding generates code. It doesn't generate engineering judgment.

This distinction matters more in some contexts than others. In a side project with no users, no compliance requirements, and no team to maintain the code — vibecoding freely and accepting the generated output with light review is entirely reasonable. The stakes are low. The speed is valuable.

In a production system with 150,000 users, complex multi-tenant architecture, insurance compliance obligations, and an 11-person team who will maintain this code for the next five years — the calculation is very different.

I've seen vibecoded additions to our codebase that:
→ Work correctly in the happy path but break on edge cases specific to our business logic
→ Follow general best practices but violate our team's specific conventions and patterns
→ Solve the immediate problem in a way that creates a harder problem downstream
→ Generate technically correct SQL that ignores the multi-tenancy isolation constraints we've built

None of these are AI failures. They're predictable outputs from a tool that doesn't know our system. The developer using the tool needs to know the system and evaluate the output against that knowledge.

Senior developers do this naturally. They treat AI output the way they'd treat code from a competent-but-new team member: review it carefully, validate the assumptions, refactor where needed, and explain the context it missed.

The risk isn't with senior developers using AI tools. The risk is with two other groups.

#### The Two Failure Modes

**Failure mode 1: Juniors who substitute vibecoding for learning.**

There's a dangerous shortcut available to junior developers now: they can produce working code faster than they can understand it. This creates the illusion of competence while preventing the development of actual competence. If you spend two years generating code you don't fully understand, you develop very little ability to evaluate code, debug complex systems, or make architectural decisions.

I don't think this means junior developers shouldn't use AI tools. I think it means they need mentors who actively push them to understand what they're shipping, not just that it passes the tests.

**Failure mode 2: Organizations that mistake output volume for quality.**

Some teams have started measuring developer productivity by lines of code generated or features shipped per sprint. In a vibecoding world, both of these metrics can go up while quality goes down. A developer who ships five vibecoded features that each introduce technical debt is not five times as productive as the developer who ships one well-designed feature.

The measurement problem is real and unsolved. I don't have a clean answer. What I can say is that teams that measure outputs rather than outcomes will get the outputs they measure for — which may not be the systems they actually want to build.

#### What the Thriving Developer Looks Like

The developers who will thrive in an AI-augmented world are the ones who use AI to move faster while maintaining (and improving) their ability to move carefully.

→ They use AI to generate first drafts, then apply judgment to shape them into production quality.
→ They use AI to explore options quickly, then use domain knowledge to choose between them.
→ They use AI to automate the routine, then focus their attention on the genuinely complex.
→ They develop the meta-skill of knowing when to trust AI output and when to verify it carefully.

This isn't a threat to developers. It's an opportunity — for the ones who take it.

The threat is real, but it's not "AI will replace developers." The threat is that some developers will use AI as a reason to stop developing judgment. And judgment — about architecture, about trade-offs, about what the code actually needs to do in the real world — is what the job has always actually been about.

What's your experience with AI coding tools in production environments? I'm genuinely curious whether others are seeing the same patterns.
