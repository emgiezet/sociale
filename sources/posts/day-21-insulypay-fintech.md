---
day: 21
title: "We built InslyPay, a mobile payment app for insurance. Here's what FinTech compliance taught me about building AI."
pillar: Builder
format: Case study
language: English
scheduled_date: 2026-04-22
posting_time: "07:30 CET"
hashtags: ["#InsurTech", "#FinTech", "#AI", "#SoftwareEngineering", "#Compliance"]
image: ./images/day-21.jpg
image_unsplash_query: "mobile payment app fintech"
cta: Repost if you build in FinTech or InsurTech
---

We built InslyPay, a mobile payment app for insurance. Here's what FinTech compliance taught me about building AI.

InslyPay lets insurance policyholders pay premiums on mobile. It sounds simple. It is not simple. PSD2, anti-fraud requirements, GDPR, insurance-specific payment regulations, cross-border rules. All landing on one product team.

At the time, I found it brutal. In hindsight, it was the best preparation for building AI systems I could have had.

Here's what payment compliance and AI compliance share:

→ Auditability is non-negotiable. PSD2 demands a paper trail for every transaction. AI in insurance demands a trace for every decision. Same principle: if something goes wrong, you need to explain exactly what happened and why.

→ You can't ship first and fix later. A buggy payment flow voids transactions. A hallucinating AI voids trust. In regulated environments, "move fast and break things" is a strategy for a different industry 🙃

→ Third-party integrations multiply your risk surface. Every payment gateway we connected was another compliance boundary to manage. Every LLM provider we use at Insly carries the same responsibility. Their data handling becomes your problem.

→ The rules change. PSD2 evolved. AI regulation is evolving now. You need architecture that handles rule changes without rewrites.

The pattern I keep seeing: engineers who have shipped in one regulated environment adapt to new regulated environments much faster. The mental model transfers.

I built InslyPay before I built RAG systems. That sequence was not accidental luck. It was training 🎯

**Regulated environments have patterns. Learn them once, apply them everywhere.**

Repost if you build in FinTech or InsurTech, let's keep this conversation going.

#InsurTech #FinTech #AI #SoftwareEngineering #Compliance
