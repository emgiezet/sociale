---
day: 13
title: "Building Your First RAG Pipeline on AWS Bedrock: A Practical Walkthrough"
pillar: Educator
language: en
image: ../../images/day-13.jpg
image_unsplash_query: "AWS cloud architecture diagram"
---

# Building Your First RAG Pipeline on AWS Bedrock: A Practical Walkthrough

This is the guide I wish I'd had when I started building RAG systems at Insly. Most tutorials either skip the production considerations or bury them in complexity. This one is designed to be practical, sequential, and honest about where the hard parts are.

I've built 3 RAG systems in production. By the end of this walkthrough, you'll understand the full RAG pipeline on AWS Bedrock — from raw documents to generated answers — with enough context to build and evaluate your first system.

## What We're Building

RAG — Retrieval-Augmented Generation — is the dominant pattern for enterprise AI that answers questions based on your own documents and data. The core idea: instead of relying on an LLM's trained knowledge (which doesn't include your data), you retrieve relevant content from your document store and include it in the prompt context.

AWS Bedrock provides a managed environment for both the retrieval infrastructure (via Bedrock Knowledge Bases) and the generation models (Claude, Titan, Llama, and others). You can use Bedrock Knowledge Bases for an integrated approach, or build a custom pipeline using Bedrock's individual APIs.

I'll describe both — starting with the managed approach for clarity, then showing where custom pipelines give you more control.

## Step 1: Document Preparation

The quality of your RAG system is largely determined before you write a single line of retrieval code. Document preparation — extraction, cleaning, chunking — is where quality is made or lost.

**Extraction.** Pull text from your source documents. PDF extraction is well-handled by libraries like `pypdf` or `pdfplumber`. DOCX by `python-docx`. HTML by `beautifulsoup4`. For scanned documents, you'll need OCR — Amazon Textract handles this well and integrates naturally with Bedrock pipelines.

**Cleaning.** Remove artifacts from extraction: page headers and footers, watermarks, repeated navigation text, encoding errors. Normalize whitespace. Identify and handle tables specially — tabular data often needs to be extracted and formatted as text rather than preserved as layout.

**Chunking.** Split your documents into segments that will be individually embedded and retrieved. The key parameters:
- Chunk size: typically 300–800 tokens for most use cases
- Overlap: 50–100 tokens of overlap between adjacent chunks, so context isn't lost at boundaries
- Splitting strategy: fixed-size or semantic (splitting on paragraph or sentence boundaries)

Store each chunk with metadata: at minimum, the source document identifier and section/position. Add domain-specific metadata you'll want to filter on — dates, document types, categories.

## Step 2: Creating Embeddings

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

## Step 3: The Vector Store

Your vector store is where embeddings live and where similarity search runs. AWS Bedrock Knowledge Bases uses Amazon OpenSearch Serverless as its native vector store, which is a good choice for production RAG systems.

If you're already running PostgreSQL on AWS RDS, `pgvector` is a practical alternative — it adds vector similarity search to your existing database without introducing a new data store.

For your first system, Bedrock Knowledge Bases is the fastest path to a working retrieval pipeline. Create a knowledge base, connect it to an S3 bucket containing your documents, and Bedrock handles chunking, embedding, and indexing automatically. You trade control for convenience — which is the right trade for a first iteration.

## Step 4: Retrieval

When a user asks a question, the retrieval step finds the chunks most relevant to that question.

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

Add metadata filtering to constrain retrieval to relevant documents when you have that context. This is particularly important for multi-tenant applications — you don't want to retrieve documents from tenant A for tenant B's queries.

## Step 5: Generation

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

The system prompt matters more than most tutorials acknowledge. Be explicit about what the model should do when the context doesn't have the answer. "Say so" is better than hallucinating a plausible-sounding response.

## Step 6: Evaluation (The Step Most People Skip)

Building a retrieval and generation pipeline is maybe 40% of the work. The other 60% is making it trustworthy — which requires evaluation.

This is where we learned the hard way at Insly. We shipped a system we were proud of. Then we built a proper evaluation set and discovered it was answering a meaningful percentage of questions incorrectly in ways that weren't obvious from casual testing.

Build a test set of 50–100 question/answer pairs. Have a domain expert validate the expected answers. Measure:

- **Retrieval recall**: for each test question, are the relevant chunks being retrieved?
- **Answer faithfulness**: is the generated answer supported by the retrieved context, or is it hallucinating?
- **Answer relevance**: does the answer address the question that was asked?

Frameworks like RAGAS can automate some of these measurements using LLM-as-judge approaches. They're imperfect but useful for tracking trends.

Without evaluation, you have a system you hope works. With evaluation, you have a system you know works — and you know in which ways it doesn't, so you can improve them.

## What Bedrock Gets Right (and What to Watch)

**Gets right:** Managed infrastructure, built-in IAM, reasonable compliance posture for EU workloads with the right region configuration. For regulated industries like insurance, the ability to keep data in your AWS account and region matters.

**Watch:** Chunking strategy matters more than people think. Default settings work for general text. Technical documents, policy clauses, and structured data often need custom chunking — which means using the custom pipeline approach rather than Bedrock Knowledge Bases' automatic processing.

**Watch:** Complex document relationships. If your documents reference each other — if understanding clause A requires knowing clause B — Bedrock Knowledge Bases doesn't model those relationships. It retrieves similar text. It doesn't reason about connections. For that, you'll need something like LightRAG (a different post, a different architecture decision).

## Next Steps After Your First System

This pipeline gives you a functional RAG system. From here, the improvements with the highest impact:

→ Add a cross-encoder re-ranker between retrieval and generation
→ Improve chunking strategy based on evaluation results
→ Add hybrid search (vector + BM25) for better recall on exact terminology
→ Implement query decomposition for complex multi-part questions

Start with Step 1. Evaluate at Step 6. Iterate based on what you measure. That's the path from demo to production.
