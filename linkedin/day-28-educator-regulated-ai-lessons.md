# Day 28 — Educator: Everything I've Learned About Shipping AI in Regulated Industries
**Pillar:** Educator | **Week:** 6 | **CTA:** Save

---

## LinkedIn Post

Everything I've learned about shipping AI in a regulated industry — in one post.

18 months. 3 RAG prototypes. 150,000 users. Insurance. Here's the condensed version.

**On architecture:**
→ Retrieval quality is determined by data preparation and retrieval architecture, not model choice. Same model, different retrieval: 60% quality vs 89%.
→ Build evaluation infrastructure before you build features. You cannot improve what you cannot measure.
→ Additive AI layers (independent, toggleable, with fallbacks) beat rearchitecting from scratch.
→ In complex document domains, graph-based retrieval (LightRAG) outperforms semantic similarity search.

**On compliance:**
→ "AI made the decision" is not an acceptable explanation in regulated industries. Design for human oversight and audit trails from day one.
→ GDPR and insurance regulations interact. Data minimization principles constrain what you can put in a vector store.
→ Get your compliance team involved before you build, not after. The conversations that happen after are more expensive.

**On teams:**
→ AI transformation creates competence anxiety in experienced engineers. Name it, make space for it.
→ Domain experts (underwriters, brokers) are your most important evaluation resource. They know what "correct" looks like.
→ Evaluation datasets validated by humans outperform automated benchmarks for domain-specific quality.

**On process:**
→ Build narrow, prove it, expand. The teams that try to boil the ocean with AI usually produce impressive demos and unreliable systems.
→ Weekly demos to real users are worth more than monthly stakeholder reviews.
→ Failed payment logic, failed AI logic, failed anything — design the error path before you design the happy path.

**On expectations:**
→ AI is not a shortcut. It's a different kind of hard.
→ The first prototype teaches you what the real problem is. Budget for it.
→ Your biggest competitor in AI adoption is not the technology. It's the process of changing how your organization makes decisions.

Save this. Share it with your team before they start.

#AIEngineering #InsurTech #RAG #ProductionAI #RegulatedIndustries

---

## Blog Post

### Everything I've Learned in 18 Months of Shipping AI in Insurance

In March 2024, I stood in front of my engineering team and said we were going to build a production RAG system for insurance document retrieval. I had confidence in the technology direction, moderate confidence in our technical approach, and almost no idea how much I didn't know.

Eighteen months later, we have production AI systems serving real users, an evaluation framework that tracks quality over time, and a set of hard-won lessons that I wish I'd had at the start.

This post is everything I'd tell myself at the beginning.

#### Architecture Lessons

**The model is not the variable.** This was the most expensive lesson to learn and the most important. When our first RAG prototype returned 60% quality and our third returned 89%, the model was the same: Claude 3.5 Sonnet on AWS Bedrock. The variable was retrieval architecture. The same LLM on different data infrastructure produced radically different outcomes.

The implication: when your AI system's quality is poor, the answer is almost never "use a better model." The answer is almost always "improve your data or your retrieval."

**Evaluation before optimization.** We didn't build our evaluation framework until six weeks into our first prototype. The time spent before we had evaluation infrastructure was largely wasted — we were making architectural changes without knowing whether they helped.

The right order: define your evaluation test set with domain expert validation, build the measurement infrastructure, establish your baseline, then optimize. Any iteration before baseline measurement is speculation.

**Build additive, not transformative.** The safest architectural pattern for AI in a production system: AI capabilities as independent, optional layers with fallback paths. Feature flags that allow individual capabilities to be enabled or disabled. Separate services for ML workloads that can be deployed and scaled independently.

This costs some engineering overhead but buys enormous operational safety. We have never had a production incident where an AI service failure affected core insurance transaction functionality, because the core functionality doesn't depend on the AI services.

**Graph-based retrieval for complex document structures.** Semantic similarity search has a ceiling in domains where documents cross-reference each other. Insurance policies, legal contracts, medical guidelines, regulatory frameworks — these are all domains where a clause or rule only makes full sense in the context of other clauses and rules. LightRAG's graph-based retrieval captures these relationships. Standard vector search doesn't.

#### Compliance Lessons

**Design for human oversight from day one.** In regulated industries, the question "how was this decision made?" needs an answer that's more satisfying than "the AI said so." Design your AI systems with visible reasoning, clear evidence surfacing, and human confirmation for high-stakes outputs from the beginning.

Retrofitting human oversight into a system designed around AI autonomy is expensive and often architecturally painful.

**GDPR constrains what goes in your vector store.** This sounds obvious in retrospect. It wasn't obvious when we were building. Personal data — policyholder names, addresses, financial information — has specific handling requirements under GDPR that apply when that data is embedded and stored in a vector index. We had to redesign our indexing approach to ensure that personal data was handled in accordance with data minimization principles.

Involve your Data Protection Officer or compliance counsel before you build your document ingestion and embedding pipeline. The conversation before building costs hours. The conversation after you've built and deployed costs weeks.

**Get compliance involved early.** In general, the most expensive compliance conversations are the ones that happen after you've built something. Every "that's not compliant" raised post-deployment requires design changes, possibly data remediation, and potentially user communication. The same conversation raised before design costs a meeting.

This requires building a relationship with your compliance function that isn't adversarial. Frame it as: "Help me understand the constraints so I can design within them from the start." Most compliance professionals appreciate being involved early far more than being called to fix problems after the fact.

#### Team Lessons

**Competence anxiety is a real force.** Experienced engineers who have been expert in their domains for years don't enjoy being beginners. AI transformation creates situations where seniority doesn't help — where a developer with 15 years of PHP experience is learning alongside developers with 3 years of total experience. That's disorienting and potentially demotivating.

Naming this explicitly, creating psychological safety for "I don't know yet," and valuing learning behaviors as much as shipping behaviors are all things I wish I'd done more explicitly from the start.

**Domain experts are your most valuable evaluation resource.** The engineers on my team are excellent software engineers. They are not insurance experts. The difference between a correct answer about an insurance clause and a plausible-sounding wrong answer about an insurance clause is a distinction that underwriters make instantly and that engineers make only after being trained.

For every domain-specific AI application, the evaluation quality is bounded by your access to domain expertise. Building relationships with underwriters, brokers, and claims adjusters who would participate in evaluation sessions was one of the highest-leverage investments we made.

**Team composition for AI projects.** The AI project team that produces the best outcomes isn't the team with the strongest ML background. It's the team with the strongest engineering discipline plus sufficient ML fluency to make good architectural choices. In most organizations, this means cross-training excellent engineers in AI concepts rather than hiring ML specialists who don't have production engineering experience.

#### Process Lessons

**Start narrow.** The teams that try to build comprehensive AI systems fail more often than the teams that start with one narrow, well-defined use case, prove it works, and expand from there.

Our first production RAG feature answered one specific type of query for one specific user role. That limited scope let us build evaluation infrastructure, iterate on quality, and build organizational trust in the technology before we expanded.

**Weekly demos with real users.** Monthly stakeholder reviews are too slow for AI development feedback cycles. We moved to weekly demos with actual underwriters using the system for real queries. The feedback from these sessions — what confused them, what they trusted, what they doubted — shaped our development more than any metric.

**Design the error path first.** For every AI feature: what happens when it's wrong? What happens when it's uncertain? What happens when it's completely unavailable? These questions should be answered before you design the happy path. In regulated industries, the error handling is often subject to the same compliance requirements as the successful outputs.

#### Expectation Lessons

**AI is not a shortcut.** It's a different kind of hard. The people who come to AI work expecting it to be easier than traditional software engineering are consistently surprised by the evaluation complexity, the data preparation requirements, and the operational overhead.

The people who come to AI work expecting it to be hard — just hard in a different way than what they've done before — adapt faster and produce more reliable systems.

**The first prototype is curriculum.** Budget for it. Plan for what you learn from it, not what you ship with it. The prototype that teaches you what the real problem is has done its job. The real problem is usually more specific and more tractable than the problem you started with.

**The biggest competition is process change, not technology.** AI adoption in an organization isn't primarily a technology challenge. It's a challenge of changing how the organization makes decisions — which decisions can be supported by AI, which need human verification, what "good enough" means for AI-assisted outputs, how failure is handled. Getting clarity on these questions requires change management, not engineering.

Start with the technology second. Start with the decision architecture first.

---

Save this for your next AI project kickoff. And if you're starting this journey now: you're making the right call. The learning curve is steep but the competence on the other side is genuinely rare and genuinely valuable.
