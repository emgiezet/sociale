# Day 2 — Trenches: "Just Add AI" Is the New "Just Add a Database"
**Pillar:** Trenches | **Week:** 1 | **CTA:** Comment/Opinion

---

## LinkedIn Post

"Just add AI" is the new "just add a database."

Same energy. Same magical thinking. Same rude awakening at 2 AM.

In 2008, the answer to every product problem was "just add a database and query it." Non-technical stakeholders thought data storage was the hard part. Once you had the data, the insights would just… appear.

We learned, slowly and painfully, that databases don't think. They store. And structuring your data, querying it intelligently, and surfacing insights through an interface is the actual work.

We're in the same moment with AI. But the hype cycle is faster and the expectations are more unreasonable.

I've had three conversations in the past two months that went like this:

→ "We have all this data. Can we just put it in an AI and ask it questions?"
→ "We want to automate this process. How long to add AI?"
→ "The competitor just launched an AI feature. We need one too."

None of these are wrong questions. They're understandable questions. But "just add AI" treats a hard problem as a solved one.

Here's what "adding AI" actually involves at minimum:
→ Data preparation and chunking strategy
→ Retrieval architecture and evaluation
→ Prompt engineering and output validation
→ Integration with existing systems and workflows
→ Monitoring, feedback loops, and iteration

The analogy I use: a database query returns deterministic results. An LLM returns probabilistic ones. You can test for the first. The second requires a completely different approach to quality assurance.

**The teams who succeed with AI treat it like any other engineering problem: hard, learnable, and worth the work.**

What's your experience with "just add AI" requests from stakeholders? I want to hear the good and the painful.

#AIEngineering #ProductionAI #TechLeadership #SoftwareEngineering #LLM

---

## Blog Post

### "Just Add AI" Is the Worst Advice in Tech Right Now

I've heard it in product meetings, in Slack messages from executives, in conference Q&As. The phrase that's become the 2026 equivalent of "we just need to put it on the blockchain."

"Can't we just add AI to this?"

Let me be direct: this framing is causing real damage to real projects. And having built AI systems in production at Insly — an insurance platform with 150,000+ users and serious compliance obligations — I've seen how this mindset plays out when it meets reality.

#### The Historical Pattern

"Just add AI" has predecessors. In the early database era, non-technical stakeholders believed that once you had a database, insight would follow automatically. The data was the hard part. Storing it would unlock the value.

What we learned: the database was the easy part. Schema design, query optimization, reporting layers, data quality — that was the work.

The same pattern played out with microservices ("just split it into services"), with NoSQL ("just use MongoDB"), and with cloud migration ("just move it to AWS"). Each time, a genuinely powerful technology got sold as a simple addition when it was actually a deep architectural commitment.

AI is following the same arc, but faster. The hype cycle has compressed. The expectations have gotten further from reality. And the "just add" crowd is louder than ever because the demos are genuinely impressive.

#### What "Just Add AI" Actually Requires

When someone asks me "how long to add AI to X," here's the real answer they need to hear:

**Data preparation takes longer than you think.** LLMs are powerful, but they're only as good as what you give them. If your data is unstructured, inconsistently formatted, multilingual, or scattered across legacy systems — which describes most enterprise data — preparation can take weeks before you write a single line of AI code.

At Insly, our insurance documents are stored in multiple formats, written in multiple languages, with varying structure by broker and country. Before we could build anything useful, we spent weeks just on chunking strategies and normalization.

**Retrieval quality requires its own engineering discipline.** RAG (Retrieval-Augmented Generation) is the dominant pattern for enterprise AI right now, and it has a deceptive surface simplicity: you embed your documents, embed your query, and find the closest match. In practice, retrieval quality at production scale requires careful attention to embedding models, chunk overlap strategies, metadata filtering, hybrid search approaches, and re-ranking logic. Each of these is its own optimization problem.

**Evaluation infrastructure is not optional.** This is the one that kills projects most often. Traditional software has deterministic tests: given input X, expect output Y. AI systems produce probabilistic outputs. You need evaluation frameworks that can measure whether outputs are grounded, accurate, helpful, and consistent. Building this infrastructure isn't glamorous, but skipping it means you'll never know when your system is degrading.

**Integration is the real complexity.** Dropping an API call to an LLM into your codebase isn't the same as integrating AI into your product. The real work is in workflow integration: how does the AI output connect to downstream systems? How do users give feedback? How do errors surface and get corrected? How do you handle the cases where the model confidently returns wrong information?

#### The Right Question

"Just add AI" is the wrong frame. The right question is: "What specific problem do we want AI to solve, for which users, at what quality bar, and how will we know when it's working?"

That question is harder to ask in a product meeting. But it's the only one that leads to a system worth building.

The teams I've seen succeed with AI treat it exactly like they'd treat any other hard engineering problem: they start small, they measure obsessively, they iterate based on real user feedback, and they resist the urge to rebuild everything before proving value on something narrow.

The failure mode is starting big, skipping evaluation, and shipping something that looks impressive in a demo and falls apart in production.

#### What This Means for You

If you're a developer being asked to "just add AI": push back on the framing. Ask for clarity on the specific use case. Ask who will define what "good" looks like. Build the evaluation infrastructure before you build the feature.

If you're a leader asking your team to "just add AI": understand that you're asking them to navigate a new engineering discipline with production stakes. Give them time for the invisible work — data prep, evaluation, iteration — that won't show up in a demo but will determine whether the system actually works.

The technology is genuinely powerful. It can do remarkable things. But it doesn't add itself. And pretending otherwise is how good teams end up building impressive demos that fail their users.

What's your experience with this? Have you been on the receiving end of "just add AI" requests? I'd genuinely like to know how teams are handling this — the comment section is where the real conversation happens.
