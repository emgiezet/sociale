---
day: 28
title: "Everything I've learned about shipping AI in a regulated industry, in one post."
pillar: Educator
format: Mega-list
language: English
scheduled_date: 2026-05-01
posting_time: "08:00 CET"
hashtags: ["#AI", "#InsurTech", "#RAG", "#SoftwareEngineering", "#EngineeringLeadership"]
image: ./images/day-28.jpg
image_unsplash_query: "knowledge lessons learned checklist"
cta: Repost this to your engineering team
---

Everything I've learned about shipping AI in a regulated industry, in one post.

20 years of production engineering. 12 months of building AI systems at Insly. 3 RAG systems, 2 expensive lessons, 1 in production 🫠 Here's the consolidated list.

**1. Start with data quality, not model selection.**
The model won't save bad data. We lost weeks before we accepted this 🤦 Audit your source documents before writing a single prompt.

**2. Retrieval is the most common failure point.**
Most RAG problems are retrieval problems dressed up as LLM problems. Evaluate your retriever in isolation before blaming the model.

**3. In regulated domains, auditability is a feature, not an afterthought.**
Log every retrieval, every prompt, every response. GDPR and insurance regulations will ask you to explain decisions. Have the trail.

**4. LLMs should not make deterministic decisions.**
Premium calculations, coverage determinations, legal interpretations: these stay in deterministic systems. AI assists humans. It doesn't replace auditable logic.

**5. Language matters more than people admit.**
Polish-language insurance documents require Polish-language models. We tested Bielik specifically because generic multilingual models degraded quality on domain-specific Polish text. Match the model to the language of your data.

**6. Evaluation is the gate, not the afterthought.**
Retrieval precision. Answer faithfulness. Hallucination red lines. Run these before every deployment. A RAG system without evaluation is a demo in production clothes.

**7. Vibecoding is a tool, not a strategy.**
AI coding assistants accelerate development in familiar domains. In regulated systems, generated code needs to be understood before it's trusted. Speed without comprehension is technical debt at scale.

**8. Teams that feel safe learn AI faster.**
Psychological safety is an AI adoption accelerator. Engineers who can say "I don't understand this output" without embarrassment iterate faster than engineers who pretend.

**9. Compliance patterns transfer across domains.**
PSD2, GDPR, insurance regulation. They share structure: auditability, data minimization, explicit consent, right to erasure. Learn one deeply and the others become faster.

**10. Build internal capability, not just vendor relationships.**
LLM providers will change their APIs, pricing, and capabilities. Teams that understand the fundamentals adapt. Teams that only know how to call an API get stuck.

**11. Architecture boundaries protect AI from itself.**
Define clearly where AI can operate and where deterministic systems take over. The boundary isn't a limitation. It's what makes the system trustworthy.

**12. The expensive lessons are the ones that make it to production.**
Both RAG systems that failed were informative. The one that works benefited from everything they taught us. Treat failures as part of the cost of building, not evidence that the approach is wrong.

**Shipping AI in a regulated industry isn't harder than other software. It just makes visible the discipline that was always required.**

Repost this to your engineering team. Especially the parts they won't enjoy hearing.

#AI #InsurTech #RAG #SoftwareEngineering #EngineeringLeadership
