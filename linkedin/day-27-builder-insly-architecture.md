# Day 27 — Builder: Insly Multi-System Architecture
**Pillar:** Builder | **Week:** 6 | **CTA:** Follow

---

## LinkedIn Post

The architecture behind Insly's multi-system platform.

We serve 150,000+ users across Europe. Here's how the system is actually structured — and why it looks the way it does.

Insly isn't one product. It's a platform that connects insurance brokers, insurers, and policyholders. Each has different needs, different data models, and different integration requirements.

The architectural decisions that shaped what we built:

**Multi-tenancy by design, not by accident**
Each broker organization operates in strict isolation. Data doesn't bleed between tenants. This wasn't just a security requirement — it was a business requirement. Brokers are competitors with each other. The data trust model depends on bulletproof isolation.

**Event-driven integration for cross-system workflows**
Insly integrates with insurer systems, payment processors, document management systems, and regulatory reporting. We use event-driven architecture to decouple these integrations. When a policy is bound, an event fires. Downstream systems — accounting, document generation, regulatory reporting — consume the event independently.

**API-first, always**
Everything that our internal systems can do, our API can also do. This wasn't a principle from day one — it became one after we had to build mobile apps and third-party integrations. Building everything as API first prevents the bifurcation of internal and external capabilities.

**Symfony as the foundation**
PHP on Symfony for the core platform, with specific services in Python for ML workloads and data pipelines. Symfony's event system, service container, and mature ORM underpin the whole thing.

**Incremental AI layer**
We didn't replace existing architecture with AI. We added AI capabilities as additional layers: RAG for document retrieval, classification for workflow routing, extraction for data capture. Each layer is independently toggleable and independently evaluatable.

**The hardest architectural decision: where to put the data.**
Multi-tenant PostgreSQL with row-level security for most data. Separate vector stores (pgvector for simpler use cases, OpenSearch for complex retrieval) for AI workloads. S3 for documents. Each storage choice reflects specific access patterns and isolation requirements.

**Complexity should live in data, not in code.**
Follow for more architecture decisions from the trenches.

#SoftwareArchitecture #InsurTech #Symfony #AWS #APIDesign

---

## Blog Post

### The Architecture Behind Insly: Building a Multi-Tenant Insurance Platform at Scale

Most architecture posts describe the ideal system. This one describes the system we actually have — how it evolved, the decisions that shaped it, and what we'd do differently if we were starting from scratch.

Insly is insurance management software serving 150,000+ users across European markets. It's not a single application — it's a platform that connects insurance brokers with insurers, policy management systems, payment processors, and policyholders. The architecture reflects that complexity.

#### The Multi-Tenancy Foundation

Multi-tenancy is the first architectural decision that shapes everything else. At Insly, each insurance broker organization operates as a completely isolated tenant. A broker's policies, clients, documents, and transaction history are not visible to any other broker's users.

This isn't just a security requirement. It's a business trust requirement. Insurance brokers are often direct competitors. A broker's book of business — their client relationships, their portfolio, their pricing strategies — is their core competitive asset. The system's credibility depends on the guarantee that this data is genuinely isolated.

We implement multi-tenancy primarily through row-level security on PostgreSQL, with tenant identification propagated through the application service layer. Each database query is automatically scoped to the authenticated tenant. There's no application-layer code path that can access cross-tenant data without explicitly bypassing the tenant context — which we've made architecturally difficult and procedurally forbidden.

For AI workloads, multi-tenancy adds complexity. Vector indexes are either per-tenant (complete isolation, higher storage cost) or shared with metadata filtering (lower cost, more complex isolation verification). We use per-tenant indexes for sensitive insurance documents and shared-with-filtering for non-sensitive reference data.

#### Event-Driven Integration

Insly integrates with a complex ecosystem: insurer back-office systems, payment processors, document management platforms, regulatory reporting systems, digital signature providers. Each integration has different protocols, different reliability characteristics, and different update frequencies.

Early in the platform's history, these integrations were implemented as synchronous calls from the core application. A policy binding event would trigger a sequential chain: notify the insurer, generate the document, post to accounting, send the confirmation email. When any step failed, the whole chain failed.

We migrated to event-driven integration over several years. The current architecture: when a significant business event occurs (policy bound, payment received, claim filed), an event is published to our event bus. Downstream systems consume events independently, with their own retry logic and failure handling.

The benefits: integration failures are isolated (if document generation fails, the policy is still bound and the accounting entry is still posted). New integrations can be added without modifying the core policy management workflow. Event processing can be scaled independently based on volume.

The costs: eventual consistency requires accepting that some downstream systems might briefly be out of sync with the core database state. Event schema evolution requires careful versioning. Debugging cross-system issues requires tracing events across multiple service logs rather than reading a single stack trace.

For most of our integration use cases, the benefits strongly outweigh the costs.

#### API-First Architecture

The API-first principle is one we arrived at the hard way, not one we started with.

Early in the platform's development, mobile apps and third-party integrations were treated as special cases that accessed the database through different code paths than the web application. This created a persistent split: features added to the web application weren't automatically available to API consumers. Mobile app development required reverse-engineering what the web application was doing.

We refactored to API-first: every capability of the system is exposed through the same API that external integrators use. The web application is an API consumer. Mobile apps are API consumers. Third-party integrations are API consumers. There are no special code paths that bypass the API layer.

This creates some constraints — the API must be versioned carefully, breaking changes require deprecation cycles — but it eliminates the bifurcation problem and means that anything we add to the platform is immediately available to all consumers.

#### The AI Layer: Additive, Not Transformative

When we started adding AI capabilities, we made a deliberate architectural choice: AI would be additive rather than transformative. We would not replace existing architecture with AI. We would add AI capabilities as optional layers that could be enabled, disabled, and evaluated independently.

This decision came from operational risk awareness. A production system with 150,000 users cannot afford a failed AI integration to take down core functionality. By keeping AI capabilities in separate, independently deployable services, we can roll AI features out gradually, roll them back quickly if they perform poorly, and evaluate them against specific use cases rather than globally.

The AI architecture: separate Python services for ML workloads (embeddings, retrieval, classification, extraction), connected to the core Symfony application through internal APIs. Feature flags at the application layer determine when AI capabilities are used versus fallback to non-AI code paths. Each AI feature has a corresponding non-AI fallback.

This architecture costs some performance (additional service hops) but buys significant operational safety and evaluation flexibility.

#### What We'd Do Differently

Starting from scratch with current knowledge:

**Earlier investment in event sourcing.** Our current architecture captures events for integration purposes but not for full audit trail reconstruction. In an insurance context, the ability to reconstruct the exact state of a policy at any historical point in time would be valuable for compliance and dispute resolution. Retrofitting event sourcing is hard.

**More aggressive API-first from day one.** The cost of the web-application-as-special-case period was years of debt and multiple refactoring projects.

**Earlier multi-tenant testing infrastructure.** Testing multi-tenant isolation is hard, and we didn't invest in dedicated testing infrastructure for it early enough. Several tenant isolation bugs in our first years would have been caught earlier with better test tooling.

The things we got right: the event-driven integration architecture, the Symfony foundation (its stability and composability have served us well for over a decade), and the additive approach to AI capabilities.

Architecture is a sequence of decisions, not a design that was right from the start. The most useful thing I can share is the reasoning behind the decisions, not just the decisions themselves.
