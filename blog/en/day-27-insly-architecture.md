---
day: 27
title: "The Architecture Behind Insly: Building a Multi-Tenant Insurance Platform at Scale"
pillar: Builder
language: en
image: ../../images/day-27.jpg
image_unsplash_query: "system architecture diagram enterprise"
---

# The Architecture Behind Insly: Building a Multi-Tenant Insurance Platform at Scale

Most architecture posts describe the ideal system. This one describes the system we actually have — how it evolved, the decisions that shaped it, and what we'd do differently starting from scratch today.

Insly is insurance management software serving 150,000+ users across European markets. It's not a single application — it's a platform that connects insurance brokers with insurers, policy management systems, payment processors, and policyholders. The architecture reflects that complexity.

## The Four Systems

Insly's platform has four major components. Understanding how they connect explains where the hardest problems live.

**QMT: Quote Management Tool**

The core broker workflow: request quotes, compare products, issue policies. This is where broker time is spent. It integrates with insurer systems — some modern REST APIs, some SOAP from 2008 that will remain SOAP until the insurer decides to rebuild their core system, which is not happening anytime soon.

The complexity here is integration heterogeneity. Every insurer speaks a slightly different dialect. Same conceptual operation — "give me a quote for this risk" — maps to different data schemas, different authentication approaches, different error handling conventions, different SLA expectations. The integration layer in QMT is one of the most maintenance-intensive parts of the platform precisely because it's adapting a uniform interface to a heterogeneous external world.

**Calcly: Calculation Engine**

Insurance premiums are calculated, not fetched. Calcly holds the calculation logic: tariff tables, rating factors, discount rules, country-specific adjustments.

This is deterministic, versioned, and auditable. A calculation run for a specific input at a specific time must produce the same result forever — because the policyholder is billed based on it, regulators may audit it, and disputes are resolved with reference to it.

Calcly is also the part of the system that AI does not touch. Premium calculations, coverage determinations, and regulatory interpretations are not probabilistic operations. They require exact, auditable logic. LLMs should not be asked to make these calculations. This boundary is explicit and enforced at the architecture level.

**Insly3: Core Platform**

Policy lifecycle management, document generation, claims tracking, client records. The system of record.

Insly3 is the oldest layer, carries the most domain logic, and is where data quality challenges are most visible. It's also where GDPR obligations are heaviest: data retention, right to erasure, access logs, data minimization requirements. Every piece of personal data in the system — policyholder names, addresses, financial information, health declarations — has specific handling obligations that are managed here.

For AI workloads, Insly3 is the primary data source. Our RAG systems query policy documents stored in Insly3. Our AI extraction features work with policy data. This creates a compliance intersection: the AI systems must handle Insly3 data according to the same GDPR constraints that apply to Insly3 itself.

**InslyPay: Payment Layer**

Mobile payment processing for insurance premiums. PSD2-compliant. Connects to payment gateways, handles reconciliation, ties payments back to policy records.

InslyPay is built to be modular because payment regulations change faster than policy regulations. The business logic for failed payments — grace periods, lapse prevention, reinstatement paths — is insurance-domain logic that had to be built explicitly, not inherited from generic payment infrastructure.

## The Multi-Tenancy Foundation

Multi-tenancy is the first architectural decision that shapes everything else. At Insly, each insurance broker organization operates as a completely isolated tenant.

This isn't just a security requirement. It's a business trust requirement. Insurance brokers are often direct competitors. A broker's book of business — their client relationships, their portfolio, their pricing strategies — is their core competitive asset. The system's credibility depends on the guarantee that this data is genuinely isolated.

We implement multi-tenancy primarily through row-level security on PostgreSQL, with tenant identification propagated through the application service layer. Each database query is automatically scoped to the authenticated tenant. There are no code paths that can access cross-tenant data without explicitly bypassing the tenant context — which we've made architecturally difficult and procedurally forbidden.

For AI workloads, multi-tenancy adds complexity. Vector indexes are either per-tenant (complete isolation, higher storage cost) or shared with metadata filtering (lower cost, more complex isolation verification). We use per-tenant indexes for sensitive insurance documents and shared-with-filtering for non-sensitive reference data.

## Event-Driven Integration

Early in the platform's history, integrations were implemented as synchronous calls from the core application. A policy binding event would trigger a sequential chain: notify the insurer, generate the document, post to accounting, send the confirmation email. When any step failed, the whole chain failed.

We migrated to event-driven integration over several years. The current architecture: when a significant business event occurs — policy bound, payment received, claim filed — an event is published to our event bus. Downstream systems consume events independently, with their own retry logic and failure handling.

The benefits are significant. Integration failures are isolated: if document generation fails, the policy is still bound and the accounting entry is still posted. New integrations can be added without modifying the core policy management workflow. Processing can be scaled independently based on volume.

The costs are real. Eventual consistency requires accepting that downstream systems might briefly be out of sync with the core database state. Event schema evolution requires careful versioning. Debugging cross-system issues requires tracing events across multiple service logs rather than reading a single stack trace.

For most of our integration use cases, the benefits strongly outweigh the costs.

## The AI Layer: Additive, Not Transformative

When we started adding AI capabilities, we made a deliberate architectural choice: AI would be additive rather than transformative. We would not replace existing architecture with AI. We would add AI capabilities as optional layers with fallback paths.

This decision came from operational risk awareness. A production system with 150,000 documents per month processed by AI cannot afford a failed AI integration to affect core functionality. By keeping AI capabilities in separate, independently deployable services, we can:

- Roll AI features out gradually to specific user segments
- Roll them back quickly if they perform poorly
- Evaluate them against specific use cases rather than globally
- Ensure that AI service failures never affect core insurance transaction functionality

The architecture: separate Python services for ML workloads, connected to the core Symfony application through internal APIs. Feature flags at the application layer determine when AI capabilities are used versus fallback to non-AI paths. Each AI feature has a corresponding non-AI fallback.

This costs some performance — additional service hops for AI-assisted operations — but buys enormous operational safety. We have never had a production incident where an AI service failure affected core insurance transaction functionality.

## What We'd Do Differently

Starting from scratch with current knowledge:

**Earlier investment in event sourcing.** Our current architecture captures events for integration purposes but not for full audit trail reconstruction. In an insurance context, being able to reconstruct the exact state of a policy at any historical point in time would be valuable for compliance and dispute resolution. Retrofitting event sourcing is expensive.

**More aggressive API-first from day one.** We spent years with a web application as a special case that bypassed the API layer. Building everything as an API consumer from the start would have saved multiple refactoring projects.

**Earlier multi-tenant testing infrastructure.** Testing multi-tenant isolation is hard, and we didn't invest in dedicated testing infrastructure for it early enough. Several tenant isolation bugs in the first years would have been caught earlier with better test tooling.

The things we got right: the event-driven integration architecture, the Symfony foundation — its stability and composability have served us well for over a decade — and the additive approach to AI capabilities.

Architecture is a sequence of decisions, not a design that was right from the start. The most useful thing I can share is the reasoning behind the decisions, not just the decisions themselves. The reasoning is what transfers to new contexts.
