---
day: 38
title: "RAG Data Chunking: Why 60% of Your Work Is Before the LLM Sees Anything"
pillar: Educator
language: en
image: ../../images/day-38.jpg
image_unsplash_query: "document parsing pipeline data engineering processing"
---

# RAG Data Chunking: Why 60% of Your Work Is Before the LLM Sees Anything

Here's a debugging story that cost us two weeks.

Our RAG system was producing inconsistent answers. Sometimes sharp and precise. Sometimes incomplete, sometimes plainly wrong. The model was Claude Sonnet — good model, well-configured. The prompt had been iterated a dozen times. The embeddings were from a high-quality model.

And then someone on the team looked at what was actually landing in the context window.

The retriever was returning the middle of an insurance clause. No section heading. No paragraph number. No reference to the definition it was citing. The chunk started with "...in accordance with the provisions of paragraph 4, subsection 2..." and contained no indication of what those provisions said or where to find them.

The model didn't have a chance. You can't generate a correct answer from an incomplete fragment, regardless of how smart the model is.

That was the day we understood: RAG is mostly a data preparation problem.

## Garbage In, Garbage Out

The pipeline failure mode I see most often in RAG systems isn't prompt engineering. It isn't model selection. It's retrieval returning content that is technically relevant but contextually incomplete.

Chunking is why.

The way you divide a document into searchable pieces determines what the model sees when a user asks a question. Do it wrong, and you'll spend months improving every other component while the fundamental problem stays in place.

Our documents at Insly are the difficult kind: insurance policies from ten European markets, some in Word formats from 2009 and 2012, some as OCR-scanned PDFs with artifacts, some with tables embedded as images. Before we could think about chunking strategy, we had a significant data extraction problem to solve.

Let's work through both.

## Step 1: Cleaning the Source Documents

Getting clean text from real-world documents is harder than it looks. Here's what we encounter at each stage.

**PDF extraction.** Standard PDF libraries (PyMuPDF, pdfminer) handle well-structured PDFs reasonably. They fail on scanned documents, PDFs with two-column layouts, and PDFs where tables are rendered as images. For our insurance policies:

- Text-based PDFs: PyMuPDF works well, preserves layout information
- Scanned PDFs: We run AWS Textract, which handles OCR and returns structured output including table detection
- Multi-column PDFs: custom post-processing to detect and re-order columns

**Word documents.** Legacy .doc and .docx files from 2009–2013 are inconsistently structured. Headings may be bolded paragraphs rather than Word heading styles. Lists may be manually numbered. We use python-docx for extraction with custom heuristics to detect structural elements.

**OCR artifacts.** The character substitution errors OCR introduces are specific: "0" for "O", "l" for "1", "rn" for "m". In insurance documents, "§ 4 ust. 2" might come out as "§ 4 ust 2" or "§4ust.2". This breaks downstream text matching. We run a custom cleanup pass that normalizes Polish legal citation patterns.

**Metadata extraction.** During extraction, we capture: document title, date, policy type, issuing market, language, section structure (if recoverable). This metadata becomes chunk metadata and is critical for filtering at retrieval time.

## Step 2: The Four Chunking Strategies

Once you have clean text, you face the chunking decision. Here's how each strategy behaves — using a concrete example from our data.

**Source clause:**
> "The insurer is liable for damages arising from flooding, excluding cases specified in §4 section 2 of this agreement, provided that the policyholder has given written consent to extend the scope of coverage under the terms of §8."

### Strategy 1: Fixed-Size Chunking

Divide the text into chunks of N tokens (typically 256–512) with some overlap (typically 10–20%).

**What happens to our clause:** At 256 tokens, the clause might split mid-sentence if the surrounding context is dense. More likely, it lands in the middle of a chunk alongside unrelated content from adjacent paragraphs. The phrase "written consent to extend scope of coverage" appears in the chunk, but "flooding" might be in the previous chunk.

**Retrieval result for query "does the policy cover flood damage":** The system may return a chunk that contains the definition of "flooding" from a different section, or the exclusion list from §4 section 2, but not the primary liability clause.

**When to use it:** Homogeneous text where section boundaries don't matter much. FAQ databases. Short-document corpora. Never for structured legal or policy documents.

### Strategy 2: Semantic Chunking

Split on natural semantic boundaries: sentences, paragraphs, or using a sliding-window approach with sentence-level embedding comparison to detect topic shifts.

**What happens to our clause:** The clause typically becomes its own chunk — it's syntactically complete. But it's isolated from the definition of §4 section 2 that it references. When the model sees "excluding cases specified in §4 section 2" without the content of §4 section 2 being in context, it can't answer a question about exclusions.

**Retrieval result:** Better than fixed-size, but the cross-reference problem remains. The user asking "is flood damage excluded if I didn't sign the extension?" gets an incomplete answer.

**When to use it:** Generally structured text with reasonable paragraph boundaries. Better than fixed-size for most cases. Still not great for heavily cross-referenced documents.

### Strategy 3: Section-Based Chunking

Extract logical document sections as single chunks — a section heading and all its content.

**What happens to our clause:** The entire "Scope of Coverage" section becomes one chunk, including our flooding clause, the definition of flooding, and the list of exclusions. This is exactly what we need — except the section might be 2,000 tokens long.

**The dilution problem:** Embedding a 2,000-token chunk produces a dense representation that averages over many concepts. When searching for "flood coverage", this chunk competes with shorter, more focused chunks from other documents. The similarity score is diluted by the non-flooding content in the same section.

**Retrieval result:** Better context when retrieved, but lower retrieval recall — you find it less often.

**When to use it:** Documents with clear, bounded sections where the entire section is relevant to a user's question. Works well for FAQ-style documents.

### Strategy 4: Parent-Child Chunking with Metadata

This is the approach we use in production for insurance policy documents.

**Structure:** Each clause or paragraph becomes a "child" chunk with precise metadata: section heading, paragraph number, document title, policy type, market, date. Parent chunks are sections or subsections — larger units that provide broader context.

**What happens to our clause:** The flooding liability clause becomes a child chunk tagged with:
```
section: "Scope of Coverage"
subsection: "Event-Specific Liability"
paragraph: "§3.2"
references: ["§4.2", "§8"]
document: "Comprehensive Home Insurance v2.3"
market: "PL"
```

The child chunk is short and dense enough for effective embedding. When retrieved, the system can optionally fetch the parent chunk for broader context.

**Retrieval result for "is flood damage covered":** The flooding clause is retrieved as a child chunk. The §4.2 exclusions are retrieved as a separate child chunk, pulled in because "§4.2" appears in the metadata as a reference. The model sees both, answers completely.

**When to use it:** Complex structured documents with cross-references. Legal texts, insurance policies, regulatory documents. Worth the setup cost.

## Step 3: Overlap, Sliding Windows, and RAPTOR

A few additional techniques that complement the above.

**Overlap.** Even with semantic or section-based chunking, adding 50–100 token overlap between adjacent chunks ensures that a sentence split across a chunk boundary doesn't disappear. Simple and effective.

**Sliding window.** For narrative text without strong structural markers, a sliding window (chunk of 256 tokens, advance by 128 tokens) ensures every sentence appears in at least two chunks. Helps retrieval but increases index size.

**RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval).** A more sophisticated approach: embed chunks, cluster them, generate summaries of each cluster, embed the summaries, and build a hierarchy. Retrieval can happen at any level of the hierarchy. I'll cover this in depth in day 41 — it solves problems that the strategies above can't.

## The Pipeline in Full

Here's the sequence we run for every new document corpus at Insly:

1. **Format detection:** Is this a well-structured PDF, a scanned PDF, a Word document?
2. **Extraction:** PyMuPDF / AWS Textract / python-docx depending on format
3. **Normalization:** OCR artifact cleanup, encoding normalization, citation pattern standardization
4. **Structure detection:** Identify headings, sections, numbered clauses using regex patterns tuned for each document type
5. **Metadata extraction:** Capture document-level and section-level metadata
6. **Chunking strategy selection:** Based on document type and structure quality
7. **Chunk generation:** With metadata attached to every chunk
8. **Quality check:** Sample 50 chunks manually, verify metadata accuracy and completeness
9. **Embedding:** Run embedding model on chunks
10. **Index update:** Upsert to vector store with metadata filters

Steps 1–8 typically take longer than the rest of the RAG system combined, when you're doing it properly. That's why I call it 60% of the work.

## What This Looks Like at Insly

We process policy documents from 10+ European markets. Each market has its own document formats, legal traditions, and structural conventions. A Polish policy from 2022 looks structurally different from a UK policy from 2015.

We maintain market-specific extraction profiles: different structure detection heuristics, different metadata schemas, different citation normalization patterns. This sounds like overhead — and it is. But the alternative is a system that works well on one corpus and badly on everything else.

The outcome: our retrieval recall on our golden test set improved from 0.61 with naive fixed-size chunking to 0.87 with parent-child chunking plus metadata filtering. That 26-point improvement didn't come from model upgrades or prompt changes. It came from better data preparation.

That's the lesson. If your RAG system isn't performing well, look at what the retriever is actually returning before you touch the prompt.

---

*Day 38 of the RAG Deep Dive series. Tomorrow: the real costs of running RAG in production — three case studies and a break-even analysis.*
