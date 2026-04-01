---
day: 44
title: "RAG is a Product, Not a Chatbot on Documents"
pillar: Educator
language: en
image: ../../images/day-44.jpg
image_unsplash_query: "product design blueprint planning framework user journey"
---

# RAG Is a Product, Not a Chatbot on Documents

"We want to add a chatbot to our documents." I've heard this sentence at the start of every RAG project that later struggled. Not because the idea is wrong, but because it's not a product spec. It's an architecture suggestion dressed up as a requirement.

What happens next is predictable: three months of building, then another three months of "why isn't the quality better?" without any shared definition of what "better" means or for whom.

I've built three RAG systems. The one that works well in production was the first one where we started with product thinking before writing a single line of code.

---

## What "Chatbot on Documents" Misses

A product spec answers five questions:
1. Who uses this?
2. What do they ask?
3. What does "good" look like, and how will we measure it?
4. What happens when the system doesn't know?
5. How do we learn and improve over time?

"Chatbot on documents" answers none of these. It describes an interface metaphor, not a product.

The consequence: every team member fills in the blanks with their own assumptions. Engineering builds for the questions they think users ask. Product evaluates against their intuition of "feels right." Users arrive with completely different mental models. Everyone is disappointed, and nobody agrees on why.

The technical architecture follows the product spec. If you don't have a product spec, you don't know what architecture you need.

---

## Step 1: User Personas and Their Actual Questions

The first thing we did for our insurance broker RAG was spend two weeks not building anything. We interviewed six brokers, read three months of support email logs, and watched brokers navigate existing policy documentation.

From that research, we extracted eleven distinct query intents:

1. **Fact lookup**: "What exactly does the policy say about X?" — single-source, precision-critical
2. **Product comparison**: "How does variant A differ from variant B?" — multi-source, completeness-critical
3. **Procedure walkthrough**: "How do I register a claim step by step?" — sequential, format-critical
4. **Exclusion check**: "Is X excluded from coverage?" — precision-critical, false negative is unacceptable
5. **Premium estimation**: "Approximately what would this cost for a client with profile Y?" — calculation-adjacent, requires explicit uncertainty communication
6. **Clause interpretation**: "What does term Z specifically mean in this policy?" — legal language, requires verbatim quotation
7. **Historical comparison**: "Has this condition changed from the previous policy version?" — version-aware, requires document metadata
8. **Multi-document synthesis**: "Compare coverage across A, B, and C for scenario X" — complex retrieval, high latency acceptable
9. **Edge case analysis**: "What happens if Y and Z occur simultaneously?" — low retrieval confidence expected, escalation path critical
10. **Out-of-scope refusal**: "Should I recommend this product to my client?" — not a knowledge question, requires hard boundary
11. **Human escalation**: "I need to speak with an underwriter about this case" — routing, not answering

These eleven intents are not equivalent. Each has a different answer format, different acceptable latency, different precision requirement, and a different acceptable failure mode.

---

## Step 2: The Quality Contract

Once you have intents, you need to define what "working correctly" means for each one. I call this the quality contract — the explicit, agreed-upon targets that govern what you build and how you evaluate it.

For each intent, the quality contract specifies:

| Dimension | Example for Fact Lookup | Example for Multi-doc Synthesis |
|---|---|---|
| Precision target | > 0.95 | > 0.82 |
| Recall target | > 0.80 | > 0.75 |
| Latency (p95) | < 2s | < 8s |
| Format | Short answer + exact quote | Structured table + citations |
| Failure mode | Hard block + "I don't have this" | Partial answer + "coverage incomplete" |
| Review required? | No (if precision gate passes) | Human review for high-stakes queries |

Without this table, every quality discussion is a negotiation with no reference point. With it, you can look at production metrics and say: "Fact lookup is at 0.91 precision, below contract. Here's the specific failure cluster."

The quality contract also forces conversations that engineers avoid and product managers don't know to ask:
- What is an acceptable false negative rate for exclusion checks? (Answer in insurance: 0. Every missed exclusion is a potential legal liability.)
- Is a 6-second response acceptable for multi-document synthesis? (Answer from brokers: yes, they'll wait if the comparison is complete. They won't wait 6 seconds for a simple fact.)
- What exactly does the system say when it doesn't know? (Not "I don't know" — the actual wording matters for user trust.)

---

## Step 3: Failure Modes — Refuse, Escalate, or Hedge

Every RAG system will encounter questions it can't answer well. The question is what it does then.

Three options:
1. **Refuse**: "I don't have information on this. Please contact [X]."
2. **Escalate**: "This question requires specialist input. I'm connecting you with an underwriter."
3. **Hedge**: "Based on available documentation, it appears that X — but this interpretation should be confirmed with a specialist."

The right answer depends on the intent and the stakes.

For fact lookups with low retrieval confidence: refuse. Don't guess at coverage limits.

For edge case analysis: hedge, with an explicit confidence indicator and escalation path.

For out-of-scope questions (our intent 10): refuse immediately, before retrieval even runs. These are architectural decisions that bypass the LLM entirely.

For human escalation requests (intent 11): routing function, not a generation function. We detect this intent and route to the broker support queue.

**The failure mode design is a product decision, not an engineering one.** Engineers implement it; product must define it. What the system does when it doesn't know is as important as what it does when it does.

---

## Step 4: How Intent-Based Routing Changed the Architecture

We started with one pipeline. We shipped to production with four pipeline paths, routing eleven intents.

**Path A: Precision retrieval** (intents 1, 4, 6)
- Scoped retrieval with high similarity threshold (0.78)
- Retrieval gate at 0.78 — hard block if not met
- LLM-as-judge faithfulness check
- Short answer format with verbatim quotation

**Path B: Synthesis** (intents 2, 5, 8)
- Multi-chunk retrieval with explicit source separation
- Cross-document consistency check
- Structured output with per-source citations
- Higher latency budget (up to 8s)

**Path C: Sequential procedure** (intent 3)
- Metadata-filtered retrieval for procedure documents specifically
- Forced numbered list output format
- No faithfulness check (format is the main quality signal)

**Path D: Routing and refusal** (intents 7, 9, 10, 11)
- No LLM generation (or minimal)
- Intent classification → pre-defined response template or external routing
- Intent 7 (historical comparison): specialized pipeline with version-aware retrieval
- Intent 9 (edge case): hedge with explicit confidence level

The single pipeline would have been a compromise for all eleven intents. Path A's strict precision threshold would have killed usability for intent 8 (multi-document synthesis regularly comes in below 0.78 because cross-document queries are inherently harder). Path B's synthesis approach would have introduced unnecessary complexity and latency for simple fact lookups.

The architecture followed the product requirements. Without the intent taxonomy and quality contract, we would have built a general-purpose pipeline and tuned it until everyone was equally dissatisfied.

---

## Step 5: Feedback Loop — Collecting User Signals

Evaluation sets tell you what happened in the past. User signals tell you what's happening now.

We collect three types of signals:

**Explicit feedback**: After each answer, a thumbs up/down. Low friction, low signal quality — but volume compensates. We track thumbs-down rate by intent as a leading indicator of quality drift.

**Implicit feedback**: Did the user ask a follow-up question immediately? Did they copy the answer or abandon the conversation? These behavioral signals correlate with answer quality without requiring active user input.

**Escalation rate by intent**: If brokers increasingly escalate edge case queries (intent 9) to human support, that tells us the system's confidence calibration for that intent is off — either it's refusing too much (and users escalate as a workaround) or it's answering when it shouldn't and users escalate to verify.

Feedback data feeds quarterly recalibration of quality contracts and annual reassessment of the intent taxonomy.

---

## Step 6: Evaluation as Product Metric

The final shift in thinking: RAG evaluation is not a technical metric. It's a product KPI.

Precision on the canary test set is not "a number your ML team tracks." It's the equivalent of uptime — a metric that tells you whether the product is delivering on its promise.

The quality contract targets from Step 2 are your SLAs. Breach them, and you have a product incident, not an engineering issue.

This framing changes conversations. When precision on fact lookups drops from 0.95 to 0.91, it's not "the model is underperforming." It's "we're below SLA on the most critical use case, and we need to understand the cause and fix it within [timeline]."

Product owns this. Engineering implements it. The numbers exist in shared dashboards, not just ML experiment logs.

---

## The RAG Product Canvas

The template I use at the start of every RAG project:

**Section 1: Users**
- Primary persona, secondary persona
- Top 10 questions each asks (from actual research, not assumptions)
- Frequency distribution across intents

**Section 2: Quality Contract**
- Table: intent × (precision, recall, latency, format, failure mode)
- Explicit "this must never happen" list (for insurance: wrong coverage amounts, missed exclusions)

**Section 3: Architecture Constraints**
- Compliance requirements (data residency, PII, audit trail)
- Integration points with existing systems
- Operational constraints (team size for maintenance, budget envelope)

**Section 4: Evaluation Plan**
- Canary test set composition and update cadence
- User signal collection mechanism
- Review and recalibration schedule

**Section 5: Open Questions**
- Things the spec leaves ambiguous, with owner and deadline

DM me "RAG CANVAS" on LinkedIn if you'd like the template.

---

## Summary

"Chatbot on documents" is not a product spec. It's a starting wish.

The path from wish to working product runs through:
1. Real user research → intent taxonomy
2. Intent taxonomy → quality contract
3. Quality contract → architecture decisions
4. Architecture + deployment → feedback loops
5. Feedback loops → continuous recalibration

The one RAG system we built with this approach has been in production for eight months with measurable quality targets and a shared team understanding of what success means. The others were rebuilt more than once because nobody agreed on what we were building in the first place.

Start with the product canvas. Build the architecture second.
