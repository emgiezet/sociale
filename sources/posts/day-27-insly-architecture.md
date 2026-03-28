---
day: 27
title: "Here's a rare look inside the architecture of a real InsurTech platform."
pillar: Builder
format: Technical
language: English
scheduled_date: 2026-04-30
posting_time: "07:30 CET"
hashtags: ["#InsurTech", "#SoftwareArchitecture", "#AI", "#SystemDesign", "#EnterpriseEngineering"]
image: ./images/day-27.jpg
image_unsplash_query: "system architecture diagram enterprise"
cta: Save for InsurTech architecture inspiration
---

Here's a rare look inside the architecture of a real InsurTech platform.

Most InsurTech architecture discussions are theoretical. Here's what it actually looks like when you're building software for insurance brokers across Europe, with GDPR constraints, multi-country regulatory requirements, and AI systems layered on top of legacy domain logic.

Insly's platform has four major systems. They're distinct but connected, and understanding how they connect explains where the hard problems live.

**QMT — Quote Management Tool**

The core broker workflow: request quotes, compare products, issue policies. This is where broker time is spent. It integrates with insurer APIs, some of which are modern REST, some of which are SOAP from 2008 and will remain SOAP until the insurer rebuilds their core system (which they will not do anytime soon). The complexity here is integration heterogeneity — every insurer speaks a slightly different dialect.

**Calcly — Calculation Engine**

Insurance premiums are calculated, not fetched. Calcly holds the calculation logic: tariff tables, rating factors, discount rules, country-specific adjustments. This is deterministic, versioned, and has to be auditable — changing a calculation rule has regulatory implications. This is not a place for AI to improvise.

**Insly3 — Core Platform**

Policy lifecycle management, document generation, claims tracking, client records. This is the system of record. It's the oldest layer, carries the most domain logic, and is where data quality challenges are most visible. Also where GDPR obligations are heaviest — data retention, right to erasure, access logs.

**InslyPay — Payment Layer**

Mobile payment processing for premiums. PSD2 compliant. Connects to payment gateways, handles reconciliation, ties payments back to policy records. Built to be modular because payment regulations change faster than policy regulations.

**Where AI fits:**

AI is not rewriting any of these systems. AI sits alongside them. Our RAG systems query policy documents stored in Insly3. Our AI features surface information from QMT data to assist brokers in workflows. Calcly stays deterministic — we don't ask LLMs to calculate premiums.

The principle: AI augments the human layer. The systems of record stay clean, versioned, and auditable.

**The hardest architectural problems in InsurTech aren't technical — they're about knowing which parts of the system should never be touched by AI.**

Save for InsurTech architecture inspiration — and if you're building something similar, I'm happy to compare notes.

#InsurTech #SoftwareArchitecture #AI #SystemDesign #EnterpriseEngineering
