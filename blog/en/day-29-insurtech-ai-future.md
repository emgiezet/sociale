---
day: 29
title: "Why Insurance's AI Transformation Is Moving Faster Than the Industry Realizes"
pillar: Trenches
language: en
image: ../../images/day-29.jpg
image_unsplash_query: "insurance future technology strategy"
---

# Why Insurance's AI Transformation Is Moving Faster Than the Industry Realizes

I spend my days building InsurTech SaaS. I also spend time talking to people across the insurance industry — brokers, underwriters, executives at carriers, technology vendors. The gap between what I see being built in forward-looking organizations and what most of the industry is doing with AI is significant and growing.

This post isn't a prediction that AI will "disrupt" insurance in the Silicon Valley sense. Insurance is a regulated, relationship-driven, actuarial business that will remain fundamentally human for the foreseeable future. But the competitive dynamics within insurance are shifting, and the organizations that understand this shift are building advantages that will be hard to close.

## The Underwriting Speed Dynamic

Insurance brokers route business to insurers. How they choose is influenced by price, relationship, and increasingly: speed.

An insurer who can evaluate a commercial submission, provide a quote, and bind coverage in two hours has a different competitive position than one who takes two weeks. The two-week insurer may have the more accurate pricing, the better coverage, the stronger relationship — but they lose business to the faster competitor for the subset of brokers who value speed above all.

AI-assisted underwriting doesn't replace the underwriter's judgment. It speeds up the information gathering and preliminary analysis: extracting relevant information from submission documents, matching against historical claims data, flagging the specific questions the underwriter needs to ask. The underwriter makes the final judgment faster because the preparation happened automatically.

This is happening now. The insurers building this capability aren't advertising it loudly. They're just binding more business.

## Claims: The Most Mature Use Case

If you want to see where insurance AI is furthest along, look at claims processing.

First Notice of Loss (FNOL) automation — capturing initial claim details from various channels and populating claim records — is operational at multiple carriers. AI-powered document extraction for supporting documentation (medical records, repair estimates, police reports) is widespread. Coverage matching — given this claim description, which policy provision applies? — is exactly the RAG use case we've been building at Insly for the past 18 months.

The maturity here is relative. The best implementations are genuinely impressive. The average implementation is still rough. But the gap between the leaders and the average is visible and widening.

The interesting next frontier in claims: multi-step agentic systems that can manage a claim through multiple stages of the workflow — requesting additional documentation, coordinating with repair networks, calculating settlement estimates — with appropriate human review at key decision points. This is not science fiction. It's being designed and piloted now.

## The Policyholder Experience Gap

Consumer expectations for insurance interactions are being reset by a handful of innovators, then applied to the whole industry.

When a digital-native insurer can handle a simple claim in under a minute, and a major carrier takes three weeks to respond to a similar inquiry, the carrier isn't being evaluated against a 1990 baseline. It's being evaluated against the best experience the customer has seen — which may have come from a competitor in a completely different industry.

AI in the customer-facing layer of insurance — not replacing the relationship, but making information access and process management faster and more transparent — is where policyholder experience improvements will come most visibly.

For brokers serving commercial clients, this dynamic plays out in broker-carrier interactions. Brokers who advise commercial clients have their own technology expectations, driven partly by the consumer tools they use personally and partly by competitive pressure to serve clients more efficiently.

## The Regulatory Documentation Burden

This is the least glamorous and most consistently high-value AI use case in insurance.

Insurance companies operate under regulatory regimes that require extensive documentation: rate filings, reserve justification, market conduct examinations, solvency reporting. The documentation burden is enormous and largely handled by skilled professionals doing fundamentally mechanical work — gathering information from multiple systems, formatting it according to specific requirements, checking for completeness and consistency.

AI can't replace actuarial judgment in reserve setting. But AI can extract and format the supporting data that goes into reserve documentation. AI can check draft regulatory filings for completeness against filing requirements. AI can summarize large document sets for preliminary regulatory review.

This is high value (regulatory compliance is not optional), relatively low risk (AI is assisting professionals who verify the output), and technically tractable (document processing and extraction capabilities are mature).

It's also the use case that almost never appears in AI conference talks, because it's not exciting. It's valuable.

## What "AI Team" Actually Means

When I say every insurance company will need an AI team within two years, I don't mean a team of ML researchers building models from scratch. The foundation models and MLaaS platforms that exist today mean that most insurance AI use cases don't require model training.

What's needed: software engineers who understand the AI tooling stack (RAG, classification, extraction, agentic frameworks), can evaluate and deploy AI components against insurance-specific quality requirements, can work closely with actuaries, underwriters, and compliance professionals, and can build the evaluation and observability infrastructure to ensure systems continue to work as data and requirements evolve.

This is a skill set that exists in software engineering teams that have upskilled intentionally. It's also a skill set that organizations who don't build it internally will struggle to acquire externally, because demand is growing faster than supply.

## The Trap: Vendor Solutions Instead of Internal Capability

The most common strategic mistake I see in insurance companies approaching AI: signing enterprise contracts with AI vendors instead of building internal capability.

Vendor solutions are appropriate for getting started, for specific well-defined use cases, and for capabilities that genuinely don't need to be differentiated. They become a liability when:

- The vendor changes pricing or deprecates features you depend on
- Your regulatory environment has edge cases the vendor didn't design for
- You need to modify the system to fit your specific domain logic
- You need to explain the system's behavior to regulators or auditors

Insurance is too domain-specific to fully outsource the core. The understanding of your data, your compliance obligations, your specific use cases, and your users' actual needs lives inside your organization. Vendors can provide infrastructure. They can't provide domain intelligence.

## The 5-Step Playbook

For insurance companies that haven't yet built meaningful AI capability:

**1. Hire for domain fluency plus AI fundamentals.** Not AI generalists who will need to learn the domain. Engineers who will learn your data, understand your compliance obligations, and build systems that fit your specific context.

**2. Start narrow and prove it.** Policy search, broker FAQ assistance, regulatory document summarization — pick one specific use case with measurable value. Ship something real to real users in under six months.

**3. Build evaluation infrastructure before scaling.** Define what good looks like for your use case. Build the measurement infrastructure to track quality over time. This is the foundation everything else depends on.

**4. Treat compliance as architecture, not a review step.** RODO, KNF requirements, the EU AI Act, insurance-specific regulation — these need to be designed in from day one. Retrofitting compliance to a system that wasn't designed for it is three times the work of building it correctly from the start.

**5. Iterate in production, not in staging.** The feedback loop from real users in a regulated environment is where you learn what actually matters. PoC-to-production is a larger gap than most teams estimate. Take it seriously.

## The Compounding Advantage

We are ahead on this at Insly because we started before it was obvious we needed to. Eighteen months of production experience with real users, a working evaluation framework, a team that knows how to iterate on AI systems, and hard-won lessons about what works in insurance — that's a compounding advantage.

The insurance companies that will lead in 2028 are the ones building internal AI capability in 2026. The ones that wait until 2027 or 2028 will be buying vendor solutions and hoping the compliance story holds.

The competitive landscape is not static. Every quarter that forward-looking organizations build experience and infrastructure, the gap to catch up widens. The window to build from a reasonable starting position isn't indefinite.

That's the strategic reality from where I sit. What are you seeing in your organization?
