# Day 19 — Educator: 7 AI Dev Tools I Actually Use
**Pillar:** Educator | **Week:** 4 | **CTA:** Save/Comment

---

## LinkedIn Post

7 tools I actually use for AI development in 2026.
Not hype. Not sponsored. Just what's in my actual stack.

I manage an 11-person team building AI systems at Insly. These are the tools we've evaluated and kept:

**1. AWS Bedrock**
Foundation model API, Knowledge Bases for managed RAG, Claude 3.5 Sonnet for generation. We stay in the AWS ecosystem because we're already there and the compliance posture is familiar.

**2. LightRAG**
Graph-based retrieval for complex document sets. Not for every use case — but when your documents cross-reference each other, nothing else competes on retrieval quality.

**3. RAGAS**
RAG evaluation framework. Automated metrics for retrieval precision, answer faithfulness, and context relevance. Imperfect but essential for tracking quality over time.

**4. LangSmith**
Observability for LLM applications. Traces every LLM call — inputs, outputs, latency, cost. When something breaks in a multi-step pipeline, this is where I start debugging.

**5. pgvector on PostgreSQL**
For simpler use cases where we're already on RDS, pgvector adds vector search without introducing a new data store. Lower performance ceiling than OpenSearch, but zero additional infrastructure.

**6. Bielik**
Polish-language LLM. For Polish insurance documents, it outperforms translate-then-embed approaches on retrieval precision. Important for our EU market work.

**7. Claude Code / Cursor**
AI-assisted coding. Not a replacement for engineering judgment, but a meaningful productivity multiplier for boilerplate, test generation, and documentation.

What's not in this list:
→ Pinecone (too expensive for our scale; pgvector covers most needs)
→ LangChain (we use it in places, but we've removed it where we don't need the abstraction)
→ GPT-4 (Claude on Bedrock fits our compliance requirements better)

**The best AI dev stack is the one that matches your team's actual constraints.**

What's in yours? Disagree with any of these? Tell me in the comments.

#AIEngineering #AWSBedrock #LightRAG #RAG #DeveloperTools

---

## Blog Post

### The AI Development Stack We Actually Run in Production

Every few weeks, a new AI tool gets announced with the marketing copy "the last tool you'll need for AI development." Every few months, the tool that was going to replace everything quietly becomes one of six things in a complex stack.

This post is about the tools we actually use at Insly for building and operating AI systems in production. I'll share why we kept each one, what we evaluated and removed, and the decision logic behind the choices.

#### The Philosophy First

Our stack selection follows a few principles:

**AWS-native when possible.** We're already on AWS. Compliance, security review, IAM integration — these are solved problems in our existing infrastructure. Adding a new vendor means adding new compliance surface area. We only add non-AWS tools when the capability gap is significant.

**Prefer boring infrastructure for new capabilities.** We don't want to manage two new complex systems to ship one new feature. pgvector on existing PostgreSQL instead of a dedicated vector database, wherever the performance ceiling allows.

**Evaluate based on measured outcomes, not demos.** Every tool in our stack survived an evaluation against our actual use case, not a synthetic benchmark. We keep the things that improved measurable outcomes.

#### The Stack

**AWS Bedrock — Foundation Model API and Managed RAG**

Bedrock is the center of our AI infrastructure. It gives us access to Claude 3.5 Sonnet (our primary generation model), Amazon Titan Embeddings, and Bedrock Knowledge Bases for managed RAG.

The compliance case for Bedrock is significant in our industry: data stays in our AWS region, the service agreement fits our insurance-context requirements, and IAM integration means we don't manage separate API keys for model access. For companies in regulated industries, this matters as much as the model quality.

We use Claude 3.5 Sonnet as our primary generation model. For lower-stakes, lower-cost use cases (classification, entity extraction from short documents), we route to Claude Haiku.

**LightRAG — Graph-Based Retrieval**

LightRAG earns its place in our stack specifically for insurance document retrieval — complex, cross-referenced documents where semantic similarity search hits a quality ceiling. For 40% of our query types, LightRAG provides 20-30 percentage points better retrieval accuracy than standard vector search.

It comes with significant operational overhead, which is why we don't use it everywhere. But for the use cases where it matters, it's irreplaceable.

**RAGAS — Evaluation Framework**

RAG quality evaluation is the unglamorous infrastructure that determines whether your system is actually getting better or just feeling like it's getting better.

RAGAS provides automated metrics using LLM-as-judge approaches: context precision (is the retrieved content relevant?), context recall (are all relevant passages being retrieved?), faithfulness (is the answer supported by retrieved content?), and answer relevance (does the answer address the question?).

We run RAGAS evaluations on a weekly basis against our test set and track the metrics in our engineering dashboard. When metrics degrade, we investigate before deploying changes to production. This has caught quality regressions twice that would otherwise have shipped.

**LangSmith — LLM Observability**

Debugging multi-step LLM pipelines without observability is archaeology — you infer from artifacts rather than seeing what happened.

LangSmith traces every LLM call: inputs, outputs, intermediate steps, latency, and cost. For an agentic pipeline with five or six reasoning steps, this visibility is essential. We've used it to identify prompt issues, unexpected model behavior, and cost spikes from inefficient call patterns.

We evaluated alternatives including Weights & Biases and Arize. LangSmith won on developer experience and integration with LangChain components we were already using.

**pgvector on PostgreSQL — Vector Search for Simpler Use Cases**

pgvector adds vector similarity search to PostgreSQL. We use it for use cases that don't justify the operational complexity of OpenSearch Serverless or a dedicated vector database.

The performance ceiling is real — at millions of vectors with high query load, you'll want a dedicated vector store. But for internal tools, lower-query-volume features, and development environments, pgvector means we're querying vectors in the same database infrastructure we use for everything else. Fewer systems to operate. Simpler backup and restore. Familiar operational procedures.

**Bielik — Polish-Language LLM**

Bielik is an open-source Polish LLM trained on Polish-language data. We use it primarily for embedding Polish insurance documents, where it outperforms multilingual models on terminology precision.

This is a narrow but important use case for us. If your systems are primarily English-language, you won't need it. If you're processing Polish documents and care about terminology precision — insurance, legal, financial — it's worth evaluating.

**Claude Code / Cursor — AI-Assisted Development**

Both used for different purposes. Claude Code for terminal-based, codebase-aware assistance. Cursor for in-IDE code generation and editing.

The productivity case is real: boilerplate generation, test case writing, documentation drafting. The judgment case is also real: neither tool replaces the architectural thinking, code review discipline, or domain knowledge that makes production code trustworthy.

I wrote about this tension earlier in this series. Short version: use them, but understand what they're not doing for you.

#### What Didn't Make the Cut

**Pinecone**: We evaluated it seriously. Excellent managed vector database with strong performance. But the cost at our scale, combined with the additional vendor relationship and compliance review, didn't justify the performance advantage over pgvector for our current query volume.

**Weaviate**: Strong open-source option with excellent multi-tenancy support, which we needed. But the operational complexity of self-hosting exceeded the value for our use case when Bedrock Knowledge Bases covered most of our needs.

**LangChain as primary orchestration**: We use LangChain's components (document loaders, text splitters, some chains), but we've removed it as the primary orchestration layer in most of our pipelines. The abstraction was obscuring what was happening in ways that made debugging harder. We use it where it helps and bypass it where it doesn't.

#### The Bottom Line

The best AI dev stack is the one that matches your team's actual constraints — technical, operational, compliance, and cost. Optimizing for the benchmark stack or the conference talk stack instead of your constraints is how teams end up with complex infrastructure they can't maintain.

Start simple. Add complexity when you've measured a need for it. Remove things that aren't earning their place. And revisit the stack every six months, because the tool landscape changes fast enough that last year's best choice may not be this year's.

What's in your stack? I'm especially curious about tools in the evaluation and observability category — it's where I've seen the most variance in how teams approach the problem.
