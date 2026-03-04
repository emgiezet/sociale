# Day 13 — Educator: RAG Pipeline with AWS Bedrock
**Pillar:** Educator | **Week:** 3 | **CTA:** Save

---

## LinkedIn Post

How to set up your first RAG pipeline with AWS Bedrock — in plain English.

No fluff, no paid course required. This is what I wish I'd had when I started.

**What you're building:** A system that retrieves relevant information from your documents and uses an LLM to answer questions based on that information. AWS Bedrock provides both the embedding model and the generation model.

**Step 1: Prepare your documents**
→ Extract text from your source files (PDF, DOCX, HTML)
→ Clean and normalize: remove headers/footers, fix encoding issues, handle tables
→ Chunk into segments of 300–800 tokens with 50–100 token overlap
→ Store chunks with metadata: source file, section, date, whatever you'll want to filter by

**Step 2: Create embeddings with Bedrock**
→ Use the Amazon Titan Embeddings model (or Cohere Embed if your use case benefits)
→ Embed each chunk — this turns text into a vector representation
→ Store vectors in a vector store (OpenSearch Serverless, which Bedrock Knowledge Bases uses natively, or pgvector on RDS if you're already on PostgreSQL)

**Step 3: Build the retrieval layer**
→ On each user query, embed the query with the same embedding model
→ Run similarity search against your vector store — retrieve top k chunks
→ Filter by metadata if you have relevant constraints (date range, document type)
→ Optionally: add a re-ranker to improve precision

**Step 4: Generate with Claude**
→ Build a prompt: system prompt (role + instructions) + retrieved context + user question
→ Call Bedrock's Claude 3.5 Sonnet (or Haiku for lower latency/cost)
→ Return the generated answer to your user

**Step 5: Evaluate**
→ Build a test set of 50–100 question/answer pairs, validated by a domain expert
→ Measure retrieval precision and answer faithfulness
→ Iterate on chunking, retrieval, and prompting based on measurement

**The mistake most people make: they go from Step 4 to production without doing Step 5.**

Save this. Start with Step 1. Step 5 is what separates demos from systems.

#AWSBedrock #RAG #AIEngineering #Claude #LLM

---

## Blog Post

### Building Your First RAG Pipeline on AWS Bedrock: A Practical Walkthrough

This is the guide I wish I'd had when I started building RAG systems at Insly. Most tutorials either skip the production considerations or bury them in complexity. This one is designed to be practical, sequential, and honest about where the hard parts are.

By the end, you'll understand the full RAG pipeline on AWS Bedrock — from raw documents to generated answers — with enough context to build and evaluate your first system.

#### What We're Building

RAG — Retrieval-Augmented Generation — is the dominant pattern for enterprise AI that answers questions based on your own documents and data. The core idea: instead of relying on an LLM's trained knowledge (which doesn't include your data), you retrieve relevant content from your document store and include it in the prompt context.

AWS Bedrock provides a managed environment for both the retrieval infrastructure (via Bedrock Knowledge Bases) and the generation models (Claude, Titan, Llama, and others). You can use Bedrock Knowledge Bases for an integrated approach, or you can build a custom pipeline using Bedrock's individual APIs.

For learning purposes, I'll describe the custom pipeline approach — it gives you more visibility into each step and more control over the components.

#### Step 1: Document Preparation

The quality of your RAG system is largely determined before you write a single line of retrieval code. Document preparation — extraction, cleaning, chunking — is where quality is made or lost.

**Extraction:** Pull text from your source documents. PDF extraction is well-handled by libraries like `pypdf` or `pdfplumber`. DOCX by `python-docx`. HTML by `beautifulsoup4`. For scanned documents, you'll need OCR — Amazon Textract (available via AWS) handles this well and integrates naturally with Bedrock pipelines.

**Cleaning:** Remove artifacts from extraction: page headers and footers, watermarks, repeated navigation text, encoding errors. Normalize whitespace. Identify and handle tables specially — tabular data often needs to be extracted and formatted as text rather than preserved as layout.

**Chunking:** Split your documents into segments that will be individually embedded and retrieved. The key parameters:
- Chunk size: typically 300–800 tokens for most use cases
- Overlap: 50–100 tokens of overlap between adjacent chunks, so context isn't lost at boundaries
- Splitting strategy: fixed-size or semantic (splitting on paragraph or sentence boundaries)

Store each chunk with metadata: at minimum, the source document identifier and section/position. Add domain-specific metadata you'll want to filter on — dates, document types, categories, whatever is relevant to your use case.

#### Step 2: Creating Embeddings

Embeddings are numerical vector representations of text that capture semantic meaning. Similar text will have similar vectors, which is what allows similarity-based retrieval.

In AWS Bedrock, you have two primary embedding model options:
- **Amazon Titan Embeddings G1 – Text**: AWS's own embedding model, well-integrated with Bedrock Knowledge Bases
- **Cohere Embed**: Strong multilingual performance if you're working with non-English documents

To create an embedding for a chunk:

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def embed_text(text: str) -> list[float]:
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body=json.dumps({'inputText': text})
    )
    body = json.loads(response['body'].read())
    return body['embedding']
```

Do this for every chunk in your corpus. Store the resulting vectors alongside the chunk text and metadata in your vector store.

#### Step 3: The Vector Store

Your vector store is where embeddings live and where similarity search runs. AWS Bedrock Knowledge Bases uses Amazon OpenSearch Serverless as its native vector store, which is a good choice for production RAG systems.

If you're already running PostgreSQL on AWS RDS, `pgvector` is a practical alternative — it adds vector similarity search to your existing database without introducing a new data store.

For your first system, Bedrock Knowledge Bases is the fastest path to a working retrieval pipeline. Create a knowledge base, connect it to an S3 bucket containing your documents, and Bedrock handles chunking, embedding, and indexing automatically. You trade control for convenience — which is the right trade for a first iteration.

#### Step 4: Retrieval

When a user asks a question, the retrieval step finds the chunks most relevant to that question.

```python
def retrieve(query: str, k: int = 5) -> list[dict]:
    query_embedding = embed_text(query)
    # Run similarity search against your vector store
    # Return top-k chunks with their source metadata
    ...
```

If you're using Bedrock Knowledge Bases, the retrieval API handles this:

```python
bedrock_agent = boto3.client('bedrock-agent-runtime')

response = bedrock_agent.retrieve(
    knowledgeBaseId='YOUR_KB_ID',
    retrievalQuery={'text': query},
    retrievalConfiguration={
        'vectorSearchConfiguration': {'numberOfResults': 5}
    }
)
chunks = response['retrievalResults']
```

Add metadata filtering to constrain retrieval to relevant documents when you have that context.

#### Step 5: Generation

With retrieved chunks in hand, construct a prompt for your generation model and call it:

```python
def generate_answer(query: str, chunks: list[dict]) -> str:
    context = '\n\n'.join([c['content']['text'] for c in chunks])

    prompt = f"""You are a helpful assistant. Answer the question based only on the provided context.
If the context doesn't contain enough information to answer the question, say so.

Context:
{context}

Question: {query}

Answer:"""

    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body=json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 1024
        })
    )
    body = json.loads(response['body'].read())
    return body['content'][0]['text']
```

#### Step 6: Evaluation (The Step Most People Skip)

Building a retrieval and generation pipeline is maybe 40% of the work. The other 60% is making it trustworthy — which requires evaluation.

Build a test set of 50–100 question/answer pairs. Have a domain expert validate the expected answers. Measure:

- **Retrieval recall**: for each test question, are the relevant chunks being retrieved?
- **Answer faithfulness**: is the generated answer supported by the retrieved context, or is it hallucinating?
- **Answer relevance**: does the answer address the question that was asked?

Frameworks like RAGAS can automate some of these measurements using LLM-as-judge approaches. They're imperfect but useful for tracking trends.

Without evaluation, you have a system you hope works. With evaluation, you have a system you know works — and you know in which ways it doesn't, so you can improve them.

#### Next Steps

This pipeline gives you a functional RAG system. From here, the improvements that typically have the highest impact:

→ Add a cross-encoder re-ranker between retrieval and generation
→ Improve chunking strategy based on evaluation results
→ Add hybrid search (vector + BM25) for better recall on exact terminology
→ Implement query decomposition for complex multi-part questions

Start with Step 1. Evaluate at Step 6. Iterate based on what you measure. That's the path from demo to production.
