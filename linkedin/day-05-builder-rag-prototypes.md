# Day 5 — Builder: 3 RAG Prototypes in 12 Months
**Pillar:** Builder | **Week:** 1 | **CTA:** Follow

---

## LinkedIn Post

We built 3 RAG prototypes in 12 months.
Here's what actually worked.

Prototype 1: Standard vector search on AWS Bedrock Knowledge Bases. Embedded our insurance documents, ran semantic search, passed results to Claude. Impressive demo. Retrieval quality in production: about 60% on our test set.

Why it failed: Insurance policies have complex cross-references. A clause in section 4 might only make sense in the context of the exclusion in section 12. Naive vector search retrieves the chunk. It misses the relationship.

Prototype 2: Hybrid search — dense vector retrieval plus BM25 keyword matching. Better. Retrieval quality: ~72%. But we were hitting context limits and the answers were verbose and imprecise.

Why it improved but still wasn't enough: Hybrid search helps with terminology matching but doesn't solve the structural problem. Insurance documents are hierarchical. Our retrieval was flat.

Prototype 3: LightRAG for document relationship mapping + AWS Bedrock for generation. We modeled document structure as a graph — entities, relationships, clauses that reference each other. Retrieval quality on our test set: ~89%.

What actually worked:
→ Treating documents as structured information, not flat text
→ Building evaluation infrastructure BEFORE optimizing retrieval
→ Involving actual underwriters in quality testing (not just engineers)
→ Starting with a narrow use case and proving it before expanding

The thing I'd tell myself at the start: **the retrieval architecture matters more than the model.**

AWS Bedrock Claude 3.5 Sonnet on prototype 1 returned 60% quality. The same model on prototype 3 returned 89%. Same model. Different data infrastructure.

If you're building RAG and hitting quality problems, the answer is almost never "use a better model."

Follow for more specific architecture decisions from the trenches of production AI.

#RAG #LightRAG #AWSBedrock #InsurTech #AIEngineering

---

## Blog Post

### Three RAG Prototypes, Three Lessons, One System That Works

Building a production RAG system is not a single decision. It's a sequence of experiments, each one revealing a problem the previous prototype couldn't solve.

At Insly, we spent twelve months iterating through three substantively different RAG architectures before we had a system we trusted enough to put in front of real users. Here's what each prototype taught us — and the single most important lesson that connects all three.

#### Prototype 1: The Standard Approach (and Why It Wasn't Enough)

The canonical RAG tutorial suggests a straightforward architecture: embed your documents into a vector store, embed the user query, retrieve the top-k most similar chunks, and pass them to your LLM for generation.

We built this on AWS Bedrock Knowledge Bases. The setup was genuinely fast — days rather than weeks. The demo was impressive. An underwriter could ask a question in natural language and get a relevant-sounding answer drawn from real policy documents.

The production numbers told a different story. On our evaluation set — a collection of 200 question/answer pairs reviewed and validated by experienced underwriters — retrieval quality was around 60%. Meaning four out of ten questions returned an answer based on the wrong document section, or retrieved relevant text but missed the critical context that would have changed the answer.

The root cause: insurance policy documents are hierarchically structured and cross-referenced. A clause about water damage coverage might say "subject to the exclusions listed in section 12.3." A semantic similarity search retrieves the relevant clause. It doesn't retrieve section 12.3 unless it's also semantically similar to the query. Which it often isn't — exclusions are written in different language than coverage descriptions.

Flat vector search doesn't understand document structure. In a domain where structure carries meaning, that's a fundamental limitation.

#### Prototype 2: Hybrid Search (Better, But Not Enough)

The natural evolution was hybrid search: combining dense vector retrieval (semantic similarity) with sparse BM25 retrieval (keyword matching). The intuition is that the two approaches complement each other — dense retrieval catches semantic relationships that differ in wording, sparse retrieval catches exact terminology matches.

This improved our retrieval quality to approximately 72%. Meaningful progress. But two new problems emerged.

First, keyword matching helped with terminology but didn't solve the structural problem. We were still retrieving semantically relevant chunks that lacked the relational context needed for accurate answers.

Second, we were hitting context limits. With hybrid retrieval returning more candidate chunks, we were passing more text to the LLM, which made answers longer, more expensive, and in some cases less focused. We were solving the retrieval problem by throwing more at the model, which is the wrong direction.

The lesson from prototype 2: quantity of retrieved context is not quality of retrieved context. More text doesn't help if it's still the wrong text.

#### Prototype 3: Graph-Based Retrieval with LightRAG

The insight that drove our third prototype came from an underwriter, not an engineer. During a review session, she walked through a question where the system had returned a plausible but incorrect answer. "The system found the right clause," she said, "but it didn't know that this clause was invalidated by this endorsement added last year."

Documents reference documents. Clauses reference clauses. A policy amendment from six months ago might override a condition in the base policy. We were treating documents as independent collections of text when they were actually a network of connected information.

LightRAG builds a knowledge graph from your documents — extracting entities and the relationships between them, not just the raw text. When you query the system, you're not searching for similar text; you're traversing a graph to find connected information.

Integrating LightRAG with AWS Bedrock for generation raised our retrieval quality to approximately 89% on our evaluation set — an improvement of nearly 30 percentage points over the baseline.

The additional work required:
→ Document relationship extraction (understanding how documents reference each other)
→ Entity normalization (ensuring that "coverage exclusion" and "policy exclusion" resolve to the same concept)
→ Graph indexing and maintenance as documents are added or updated
→ Evaluation infrastructure that could test relationship-aware retrieval

That last point deserves emphasis. The 89% quality number only means something because we built the evaluation framework early — before we started optimizing. Without evaluation infrastructure, you're guessing about quality rather than measuring it.

#### The Single Most Important Lesson

Here's the sentence I wish I'd read before we started: **the retrieval architecture matters more than the model.**

We used Claude 3.5 Sonnet on Bedrock for generation in all three prototypes. Same model. The quality went from 60% to 89% based entirely on what we fed it. The model didn't get better. Our understanding of our data structure got better.

This matters because the obvious temptation when your RAG system underperforms is to swap the model. Try a different LLM. Try a bigger context window. Try fine-tuning. These are expensive experiments with uncertain returns.

The higher-leverage intervention is almost always: understand your data structure better, and build a retrieval architecture that respects it.

For our insurance documents, the structure was hierarchical and relational. For your use case, the structure might be different. The question to ask is: what relationships in my data are not captured by semantic similarity? And then: how do I build a retrieval architecture that captures those relationships?

That question, asked early, would have saved us months.

If you're building RAG systems and hitting quality ceilings — especially in structured domains like legal, medical, financial, or insurance — I'd be glad to share more about the LightRAG architecture in detail. Follow along and drop a comment with your specific challenge.
