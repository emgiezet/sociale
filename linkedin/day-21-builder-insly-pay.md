# Day 21 — Builder: InslyPay Mobile Payment App
**Pillar:** Builder | **Week:** 5 | **CTA:** Follow

---

## LinkedIn Post

We built InslyPay — a mobile payment app for insurance.
Insurance payments are not like regular payments. Here's what makes them different.

InslyPay lets policyholders pay their insurance premiums directly from their phone. Sounds simple. The complexity is in the domain.

**What makes insurance payments uniquely hard:**

→ **Policy lifecycle awareness.** A payment isn't just a money transfer — it's associated with a specific policy, a specific coverage period, and potentially multiple installments. The payment infrastructure has to understand insurance business logic, not just payment processing.

→ **Multi-party accounting.** In insurance, money flows between policyholders, brokers, and insurers. A single premium payment might need to be split, tracked, and reconciled across multiple entities with different accounting systems.

→ **Regulatory requirements.** Insurance premium handling is regulated differently than e-commerce payments in most jurisdictions. In Europe, this intersects with both PSD2 (payment services directive) and insurance-specific regulations.

→ **Failed payment logic.** When a payment fails in e-commerce, you retry and send a reminder. When an insurance payment fails, the policy might lapse. The business logic for handling failed payments is significantly more complex.

What we built:
→ Mobile app with real-time payment processing
→ Policy state awareness (know which policy and period the payment covers)
→ Integration with our existing broker accounting workflows
→ Retry and recovery flows designed for insurance lapse prevention

The hardest part wasn't the payment integration. It was modeling the insurance business logic correctly underneath the payment flow.

**Domain knowledge beats technical cleverness every time.**

What's the most domain-specific complexity you've had to model in a software system?

#InsurTech #MobilePayments #SoftwareEngineering #ProductDevelopment #Insurance

---

## Blog Post

### Building InslyPay: What Insurance Payments Taught Us About Domain Modeling

Payments seem simple from the outside. You transfer money from one place to another. The technology for this is mature, well-documented, and API-accessible. What could be hard?

The hard part, as with most software projects, is not the technology. It's the domain.

Insurance payments are not like e-commerce payments. They're not like bank transfers. They sit at the intersection of financial services, insurance regulation, multi-party accounting, and policy lifecycle management — each of which has its own rules, edge cases, and failure modes.

Building InslyPay taught us that any time you're building a "payment feature" in a specialized domain, you're actually building domain logic that happens to involve payments.

#### The Problem with Insurance Premiums

When you pay for a product online, the payment model is simple: you owe a price, you pay the price, you receive the product.

Insurance premiums don't work this way.

A premium is associated with a specific policy, a specific period of coverage, and often a specific installment schedule. "Paying your insurance" might mean paying the third installment of an annual premium on a policy that covers two buildings and a commercial vehicle, issued to a company with four named drivers, through a broker who handles the client relationship and earns commission on the transaction.

The money doesn't just go somewhere — it goes to a specific accounting entry in the insurer's system, minus a commission that goes to a specific broker account, with a payment status that updates the policy state in the policy management system.

All of this needs to be reflected accurately, in real time, in InslyPay.

#### Multi-Party Accounting

The multi-party accounting dimension is the one that most surprised people who reviewed our architecture from outside the insurance domain.

In most payment scenarios, there are two parties: the payer and the payee. In insurance broker markets, there are typically three: the policyholder (who pays), the broker (who handled the sale and earns commission), and the insurer (who provides the coverage and receives the net premium).

A single payment event in InslyPay needs to:
→ Record the gross premium received
→ Calculate and split the broker commission
→ Post to the insurer's accounting system
→ Update the policy payment status
→ Trigger the appropriate receipts and documentation for all parties

This sounds like accounting. It is accounting. But it's accounting that has to happen automatically, in response to a payment event, with the correctness guarantees that financial transactions require.

#### The Failed Payment Problem

E-commerce has a fairly standard failed payment playbook: retry with exponential backoff, notify the user, offer alternative payment methods. If payment ultimately fails, the order is cancelled.

Insurance has a materially different business logic for failed payments, because the consequence is not a cancelled order — it's a lapsed policy. A lapsed policy means the policyholder is uninsured, which is a serious outcome both for them and for the broker's client relationship.

Our failed payment logic needed to understand:
→ How many days of grace period the specific policy had (this varies by policy type and insurer)
→ Whether the policy should be put in a "grace period" state (still covered but in arrears) or immediately suspended
→ What notifications needed to go to the policyholder, the broker, and potentially the insurer
→ What the reinstatement path looked like if the payment was eventually recovered

This logic was not something we could derive from general payment infrastructure. It came from our domain knowledge of how insurance policy lifecycle management works — and from many conversations with insurance professionals who knew the edge cases we hadn't thought of.

#### What Made This Project Succeed

Two things stand out.

**First: domain expertise before technical design.** We spent three weeks talking to brokers, underwriters, and accounting staff before we wrote significant application code. We built a mental model of the domain that was detailed enough to catch the edge cases early — the multi-party accounting, the failed payment grace periods, the regulatory requirements — before they became bugs in production.

**Second: incremental rollout with real feedback.** We deployed InslyPay to a small set of pilot clients before broader release, with active monitoring and direct feedback channels. Several domain edge cases that we hadn't modeled correctly surfaced in this period — not as critical failures, but as things that "worked but confused the users." The user confusion was a signal about domain model gaps, not just UX problems.

The technical architecture — the mobile app, the payment gateway integration, the webhook handling — was relatively straightforward once the domain model was correct. The domain model took most of the project time.

#### The General Lesson

Any time you're building a "standard" feature (payments, notifications, search, reporting) in a specialized domain (insurance, healthcare, legal, financial services), you're actually building a domain-specific system that happens to use standard technology.

The temptation is to lead with the technology — find a payment library, integrate it, done. The approach that works is to lead with the domain — understand the business logic deeply enough that the technology choices follow naturally.

Domain knowledge beats technical cleverness every time. Not because technical cleverness doesn't matter, but because the hardest problems in domain software are domain problems, not technical ones.
