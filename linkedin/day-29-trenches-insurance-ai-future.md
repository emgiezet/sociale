# Day 29 — Trenches: Every Insurance Company Will Need an AI Team
**Pillar:** Trenches | **Week:** 6 | **CTA:** Comment

---

## LinkedIn Post

In 2 years, every insurance company will need an AI team.
Most of them don't know it yet.

This isn't a prediction about AI replacing underwriters. It's an observation about how competitive dynamics in insurance are shifting — faster than most of the industry has processed.

Here's what I'm watching:

→ **Underwriting speed is becoming a differentiator.** Brokers route business to insurers who respond fastest. AI-assisted underwriting that can evaluate a submission in minutes rather than hours changes the competitive calculus.

→ **Claims processing is the most visible AI use case — and it's maturing fast.** FNOL (first notice of loss) automation, document extraction, coverage matching — these are in production at forward-looking insurers now. The gap between them and the laggards is widening.

→ **Policyholder expectations are shifting.** When you can file a car insurance claim by video and get a response in hours, waiting three weeks for a response to a commercial policy query feels broken. The consumer experience bar is being set by a few leaders and applied to the whole industry.

→ **Regulatory reporting is fertile ground for AI.** The documentation burden in insurance is enormous. AI that can summarize, extract, and format for regulatory requirements isn't exciting, but it's high value and relatively low risk.

What "AI team" means in this context: probably not a team of ML researchers. Probably a team of engineers who understand the AI tooling stack, can evaluate and deploy RAG and classification systems, can work closely with domain experts, and can build the evaluation infrastructure to know whether things are working.

That's the skill set. It already exists in software engineering teams that have upskilled intentionally.

**The question for insurance companies isn't "do we need AI?" It's "do we build this internally or fall behind while competitors do?"**

What are you seeing in your industry? Is the AI capability gap widening?

#InsurTech #AIEngineering #Insurance #DigitalTransformation #TechLeadership

---

## Blog Post

### Why Insurance's AI Transformation Is Moving Faster Than the Industry Realizes

I spend my days building AI systems for insurance. I also spend time talking to people across the insurance industry — brokers, underwriters, executives at carriers, technology vendors. The gap between what I see being built in forward-looking organizations and what most of the industry is doing with AI is significant and growing.

This post isn't a prediction that AI will "disrupt" insurance in the Silicon Valley sense. Insurance is a regulated, relationship-driven, actuarial business that will remain fundamentally human for the foreseeable future. But the competitive dynamics within insurance are shifting, and the organizations that understand this shift are building advantages that will be hard to close.

#### The Underwriting Speed Dynamic

Insurance brokers route business to insurers. How they choose is influenced by price, relationship, and increasingly: speed.

An insurer who can evaluate a commercial submission, provide a quote, and bind coverage in two hours has a different competitive position than one who takes two weeks. The two-week insurer may have the more accurate pricing, the better coverage, the stronger relationship — but they lose business to the faster competitor for the subset of brokers who need speed.

AI-assisted underwriting doesn't replace the underwriter's judgment. It speeds up the information gathering and preliminary analysis: extracting relevant information from submission documents, matching against historical claims data, flagging the specific questions the underwriter needs to ask. The underwriter makes the final judgment faster because the preparation happened automatically.

The insurers building this capability aren't advertising it. They're just binding more business.

#### Claims: The Most Mature Use Case

If you want to see where insurance AI is furthest along, look at claims processing.

First Notice of Loss (FNOL) automation — capturing initial claim details from various channels (phone, app, web) and populating claim records — is operational at multiple carriers. AI-powered document extraction for supporting documentation (medical records, repair estimates, police reports) is widespread. Coverage matching — given this claim description, which policy provision applies? — is exactly the RAG use case we've been building at Insly.

The maturity here is relative. The best implementations are genuinely impressive. The average implementation is still rough. But the gap between the leaders and the average is visible and widening.

The interesting next frontier in claims: multi-step agentic systems that can manage a claim through multiple stages of the workflow — requesting additional documentation, coordinating with repair networks, calculating settlement estimates — with appropriate human review at key decision points.

#### The Policyholder Experience Gap

Consumer expectations for insurance interactions are being reset by a handful of innovators, then applied to the whole industry.

When Lemonade can handle a simple renters insurance claim in under a minute, and a major carrier takes three weeks to respond to a similar inquiry, the carrier isn't being evaluated against a 1990 baseline. It's being evaluated against the best experience the customer has seen — which may have come from a competitor or from a completely different industry.

This applies to commercial insurance as well, though the dynamics are different. Brokers who advise commercial clients have their own set of technology expectations, driven partly by the consumer tools they use personally and partly by the competitive pressure to serve clients more efficiently.

AI in the customer-facing layer of insurance — not replacing the relationship, but making information access and process management faster and more transparent — is the area where policyholder experience improvements will come most visibly.

#### The Regulatory Documentation Burden

This is the least glamorous and most consistently high-value AI use case in insurance.

Insurance companies operate under regulatory regimes that require extensive documentation: rate filings, reserve justification, market conduct examinations, solvency reporting. The documentation burden is enormous and largely handled by skilled professionals doing fundamentally mechanical work — gathering information from multiple systems, formatting it according to specific requirements, checking for completeness and consistency.

AI can't replace actuarial judgment in reserve setting. But AI can extract and format the supporting data that goes into reserve documentation. AI can check draft regulatory filings for completeness against filing requirements. AI can summarize large document sets for preliminary regulatory review.

This is high value (regulatory compliance is not optional), relatively low risk (AI is assisting professionals who verify the output), and technically tractable (the document processing and extraction capabilities are mature).

It's also the use case that almost never appears in AI conference talks, because it's not exciting. It's valuable.

#### What "AI Team" Actually Means

When I say every insurance company will need an AI team within two years, I don't mean a team of ML researchers building models from scratch. The foundation models and MLaaS platforms that exist today mean that most insurance AI use cases don't require model training.

What's needed: software engineers who understand the AI tooling stack (RAG, classification, extraction, agentic frameworks), can evaluate and deploy AI components against insurance-specific quality requirements, can work closely with actuaries, underwriters, and compliance professionals, and can build the evaluation and observability infrastructure to ensure systems continue to work as data and requirements evolve.

This is a skill set that exists in software engineering teams that have upskilled intentionally. It's also a skill set that the organizations who don't build it internally will struggle to acquire externally, because demand is growing faster than supply.

The question for insurance companies in 2026 isn't "do we need AI?" It's "do we start building the capability now, while the competitive gap is still closeable, or do we wait until we're playing catch-up against competitors who've had two years of compounding learning?"

The answer seems obvious to me. But I'm aware that most of the industry hasn't reached that conclusion yet.

What are you seeing in your own organization or industry? Is the AI capability gap beginning to create visible competitive differentiation? I'm genuinely curious how people across different parts of the industry perceive this.
