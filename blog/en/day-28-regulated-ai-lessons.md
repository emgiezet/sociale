---
day: 28
title: "Everything I've Learned in 18 Months of Shipping AI in Insurance"
pillar: Educator
language: en
image: ../../images/day-28.jpg
image_unsplash_query: "knowledge lessons learned checklist"
---

# Everything I've Learned in 18 Months of Shipping AI in Insurance

Eighteen months ago, I stood in front of my engineering team and said we were going to build a production RAG system for insurance document retrieval. I had confidence in the technology direction, moderate confidence in our technical approach, and almost no idea how much I didn't know.

Eighteen months later, we have production AI systems serving real users, an evaluation framework that tracks quality over time, and a set of hard-won lessons that I wish I'd had at the start.

This post is everything I'd tell myself at the beginning.

## Architecture Lessons

**The model is not the variable.** This was the most expensive lesson to learn and the most important. When our first RAG prototype returned 60% quality and our third returned 89%, the model was the same: Claude 3.5 Sonnet on AWS Bedrock. The variable was retrieval architecture. The same LLM on different data infrastructure produced radically different outcomes.

The implication: when your AI system's quality is poor, the answer is almost never "use a better model." The answer is almost always "improve your data or your retrieval." We lost weeks before we accepted this.

**Evaluation before optimization.** We didn't build our evaluation framework until six weeks into our first prototype. The time spent before we had evaluation infrastructure was largely wasted — we were making architectural changes without knowing whether they helped.

The right order: define your evaluation test set with domain expert validation, build the measurement infrastructure, establish your baseline, then optimize. Any iteration before baseline measurement is speculation.

**Build additive, not transformative.** The safest architectural pattern for AI in a production system: AI capabilities as independent, optional layers with fallback paths. Feature flags that allow individual capabilities to be enabled or disabled. Separate services for ML workloads that can be deployed and scaled independently.

This costs some engineering overhead but buys enormous operational safety. We have never had a production incident where an AI service failure affected core insurance transaction functionality, because the core functionality doesn't depend on the AI services.

**Graph-based retrieval for complex document structures.** Semantic similarity search has a ceiling in domains where documents cross-reference each other. Insurance policies, legal contracts, medical guidelines, regulatory frameworks — these are domains where a clause only makes full sense in the context of other clauses. LightRAG's graph-based retrieval captures these relationships. Standard vector search doesn't.

**Language matters more than people admit.** Polish-language insurance documents require Polish-language models. We tested Bielik, the Polish LLM, specifically because generic multilingual models degraded quality on domain-specific Polish text. Our evaluation showed a 12 percentage point precision improvement over the translation approach. Match the model to the language of your data.

## Compliance Lessons

**Design for human oversight from day one.** In regulated industries, "the AI said so" is not an acceptable explanation. Design your AI systems with visible reasoning, clear evidence surfacing, and human confirmation for high-stakes outputs from the beginning.

Retrofitting human oversight into a system designed around AI autonomy is expensive and often architecturally painful. The conversation about oversight requirements before you design costs one meeting. The conversation after you've built costs weeks.

**GDPR constrains what goes in your vector store.** This sounds obvious in retrospect. It wasn't obvious when we were building. Personal data — policyholder names, addresses, financial information — has specific handling requirements under GDPR that apply when that data is embedded and stored in a vector index. We had to redesign our indexing approach to ensure data minimization principles were respected.

Involve your Data Protection Officer or compliance counsel before you build your document ingestion and embedding pipeline. In Poland, working within KNF (Polish Financial Supervision Authority) requirements adds another layer — these need to be understood before architectural decisions are made, not after.

**Get compliance involved early.** Every "that's not compliant" raised post-deployment requires design changes, possibly data remediation, and potentially user communication. The same conversation raised before design costs a meeting.

This requires building a relationship with your compliance function that isn't adversarial. Frame it as: "Help me understand the constraints so I can design within them from the start." Most compliance professionals appreciate being involved early far more than being called to fix problems after the fact.

**LLMs should not make deterministic decisions.** Premium calculations, coverage determinations, legal interpretations: these stay in deterministic systems. AI assists humans. It doesn't replace auditable logic. This boundary is not a technical constraint — it's a compliance requirement and a trust requirement. Define it explicitly in your architecture documentation.

## Team Lessons

**Competence anxiety is a real force.** Experienced engineers who have been expert in their domains for years don't enjoy being beginners. AI transformation creates situations where seniority doesn't help — where a developer with 15 years of PHP experience is learning alongside developers with 3 years of total experience.

Naming this explicitly, creating psychological safety for "I don't know yet," and valuing learning behaviors as much as shipping behaviors are all things I wish I'd done more explicitly from the start. Engineers who feel safe to say "I don't understand this output" iterate faster than engineers who pretend to understand.

**Domain experts are your most valuable evaluation resource.** The engineers on my team are excellent software engineers. They are not insurance experts. The difference between a correct answer about an insurance clause and a plausible-sounding wrong answer is a distinction that underwriters make instantly and that engineers make only after being trained.

For every domain-specific AI application, the evaluation quality is bounded by your access to domain expertise. Building relationships with underwriters, brokers, and claims adjusters who participated in evaluation sessions was one of the highest-leverage investments we made.

**Team composition for AI projects.** The AI project team that produces the best outcomes isn't the team with the strongest ML background. It's the team with the strongest engineering discipline plus sufficient ML fluency to make good architectural choices. Cross-training excellent engineers in AI concepts almost always outperforms hiring ML specialists who don't have production engineering experience.

## Process Lessons

**Start narrow.** The teams that try to build comprehensive AI systems fail more often than the teams that start with one narrow, well-defined use case, prove it works, and expand. Our first production RAG feature answered one specific type of query for one specific user role. That limited scope let us build evaluation infrastructure, iterate on quality, and build organizational trust before expanding.

**Weekly demos with real users.** Monthly stakeholder reviews are too slow for AI development feedback cycles. We moved to weekly demos with actual underwriters using the system for real queries. The feedback from these sessions shaped our development more than any metric.

**Design the error path first.** For every AI feature: what happens when it's wrong? What happens when it's uncertain? What happens when it's completely unavailable? These questions should be answered before you design the happy path. In regulated industries, the error handling is often subject to the same compliance requirements as the successful outputs.

**Vibecoding is a tool, not a strategy.** AI coding assistants accelerate development in familiar domains. In regulated systems, generated code needs to be understood before it's trusted. Speed without comprehension is technical debt at scale. The developers who get the most from AI assistance are the ones who can immediately evaluate whether the generated code is correct, not just whether it runs.

## Expectation Lessons

**AI is not a shortcut.** It's a different kind of hard. The evaluation complexity, the data preparation requirements, and the operational overhead are all real. The people who come to AI work expecting it to be hard — just hard in a different way — adapt faster and produce more reliable systems.

**The first prototype is curriculum.** Budget for it. Plan for what you learn from it, not what you ship with it. The prototype that teaches you what the real problem is has done its job.

**The biggest competition is process change, not technology.** AI adoption in an organization isn't primarily a technology challenge. It's a challenge of changing how the organization makes decisions — which decisions can be supported by AI, what "good enough" means for AI-assisted outputs, how failure is handled. Getting clarity on these questions requires change management, not engineering.

**Compliance patterns transfer across domains.** PSD2, GDPR, insurance regulation, the EU AI Act — these frameworks share structure: auditability, data minimization, explicit consent, right to erasure. Learn one deeply and the others become significantly faster to understand. Engineers who've shipped in one regulated environment adapt to new regulated environments faster. This pattern transfers.

Start with the technology second. Start with the decision architecture first. The technology will follow.
