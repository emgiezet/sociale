---
day: 21
title: "Building InslyPay: What FinTech Compliance Taught Me About Building AI"
pillar: Builder
language: en
image: ../../images/day-21.jpg
image_unsplash_query: "mobile payment app fintech"
---

# Building InslyPay: What FinTech Compliance Taught Me About Building AI

Payments seem simple from the outside. You move money from one place to another. The technology is mature, well-documented, and API-accessible. What could be hard?

The hard part — as with almost every software project that touches a specialized domain — is not the technology. It's the domain. And then, in a regulated domain, it's the compliance layer stacked on top of the domain complexity.

We built InslyPay: a mobile payment application for insurance policyholders. It lets them pay their insurance premiums directly from their phone. At the time, navigating the compliance requirements felt brutal. In hindsight, it was the best possible preparation for the AI systems work I'm doing now.

Here's what the experience actually taught me.

## What Makes Insurance Payments Uniquely Hard

Insurance premiums don't work like e-commerce payments. When you buy something online, the payment model is clean: you owe a price, you pay the price, you receive the product.

A premium payment is associated with a specific policy, a specific coverage period, and often a specific installment schedule. "Paying your insurance" might mean paying the third installment of an annual premium on a policy that covers two buildings and a commercial vehicle, issued to a company with four named drivers, through a broker who handles the client relationship and earns commission on the transaction.

The money doesn't just go somewhere — it goes to a specific accounting entry in the insurer's system, minus a commission that flows to a specific broker account, with a payment status that updates the policy state in the policy management system. All of this needs to be reflected accurately and in real time.

### Multi-Party Accounting

In most payment scenarios, there are two parties: the payer and the payee. In insurance broker markets, there are typically three: the policyholder who pays, the broker who handled the sale and earns commission, and the insurer who provides coverage and receives the net premium.

A single payment event in InslyPay needs to record the gross premium received, calculate and split the broker commission, post to the insurer's accounting system, update the policy payment status, and trigger receipts and documentation for all parties.

This is accounting. But it's accounting that has to happen automatically, in response to a payment event, with the correctness guarantees that financial transactions require.

### The Failed Payment Problem

E-commerce has a standard failed payment playbook: retry with exponential backoff, notify the user, offer alternative payment methods, cancel the order if payment ultimately fails.

Insurance has materially different business logic for failed payments. The consequence is not a cancelled order — it's a lapsed policy. A lapsed policy means the policyholder is uninsured, which is serious both for them and for the broker's client relationship.

Our failed payment logic needed to understand how many days of grace period the specific policy had (this varies by policy type and insurer), whether the policy should enter a "grace period" state or be immediately suspended, what notifications needed to go to which parties, and what the reinstatement path looked like.

None of this came from general payment infrastructure knowledge. It came from deep domain expertise about how insurance policy lifecycle management works.

## The Compliance Landscape: PSD2, GDPR, and Insurance Regulation

Building a payment application in Europe in the current regulatory environment means managing multiple overlapping compliance frameworks simultaneously.

**PSD2** governs payment services in the EU. It requires strong customer authentication, mandates open banking access for third-party payment providers, and demands audit trails for every payment transaction. Every payment flow in InslyPay had to be designed with PSD2 requirements built in — not added afterward.

**GDPR** applies to every piece of personal data we handle. Payment data is particularly sensitive under GDPR. We needed to design data minimization into our architecture, implement appropriate retention policies, and ensure that the right-to-erasure requirements could be fulfilled without breaking the audit trails that PSD2 and insurance regulation require simultaneously.

**Insurance-specific payment regulation** adds a third layer. In many European jurisdictions, the handling of insurance premiums is regulated separately from general payment processing — there are requirements around client money handling, escrow arrangements, and the timing of premium posting to policy records.

Managing these three frameworks simultaneously, ensuring they didn't conflict with each other, and building architecture that could evolve as any of them changed — that was the actual challenge of InslyPay.

## What FinTech Compliance Taught Me About AI Compliance

When I started building AI systems at Insly 18 months ago, I noticed something immediately: the compliance patterns I'd learned building InslyPay mapped almost directly onto the requirements for AI in regulated industries.

**Auditability as a first principle.** PSD2 demands a paper trail for every transaction. AI in insurance demands a trace for every decision. If a claim is denied or a coverage question is answered incorrectly, I need to be able to explain exactly what documents were retrieved, what context was provided to the model, and what the model's response was. The same discipline that built InslyPay's payment audit trail built our AI decision audit trail.

**You cannot ship first and fix later.** A buggy payment flow can void transactions and trigger regulatory consequences. A hallucinating AI can produce incorrect coverage interpretations with real legal implications. In regulated environments, moving fast and breaking things is a strategy for a different industry. Both InslyPay and our AI systems required getting the compliance design right before launching, not as a post-launch cleanup exercise.

**Third-party integrations multiply your risk surface.** Every payment gateway we connected to InslyPay was another compliance boundary to manage — their data handling, their security certifications, their API reliability became our responsibility to verify. Every LLM provider in our AI stack carries the same weight. AWS Bedrock's data handling practices, their model training policies, their audit logging capabilities — these are things we had to verify and document before we could use the service with insurance data.

**The rules change, and your architecture needs to handle it.** PSD2 has been updated multiple times since we built InslyPay. The EU AI Act is being implemented in stages. Insurance regulation in specific markets changes with legislative cycles. Architecture that required rewrites every time a regulation changed would be impossible to maintain. Both systems needed to be designed with regulatory evolution in mind — capability to update compliance logic without rebuilding core functionality.

## The Pattern That Transfers

The most transferable lesson from InslyPay to AI work is this: regulated environments have specific, recurring patterns — auditability, human oversight requirements, data minimization, explicit consent, right to erasure or explanation — and once you've internalized one regulatory framework deeply, the others become much faster to learn.

Engineers who've shipped production software in one regulated environment adapt to new regulated environments significantly faster than engineers coming from unregulated domains. The mental model — thinking about what needs to be audited, what requires human sign-off, what data can and can't be retained — transfers.

I built InslyPay before I built RAG systems. That sequence wasn't accidental luck. It was training that I'm still drawing on every time we make an AI architecture decision at Insly.

Domain knowledge beats technical cleverness every time. Not because technical cleverness doesn't matter, but because the hardest problems in domain software are domain problems — and in regulated domains, compliance problems. Learn the domain. Learn the regulation. The technology will follow.
