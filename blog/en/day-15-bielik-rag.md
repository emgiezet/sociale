---
day: 15
title: "Building Native Polish-Language RAG: Architecture Decisions and Results"
pillar: Builder
language: en
image: ../../images/day-15.jpg
image_unsplash_query: "Polish technology innovation architecture"
---

# Building Native Polish-Language RAG: Architecture Decisions and Results

When we started building RAG systems at Insly, we faced a question most Polish tech companies skip: do we actually need to translate everything to English first?

The standard approach for Polish-language documents follows this pipeline: Polish source document → machine translation to English → English embedding → English retrieval → English generation → translated answer back to Polish. This works. But it has concrete costs.

## The Translation Problem

Polish insurance terminology is precise in ways that matter legally. Terms like "ubezpieczenie odpowiedzialności cywilnej" (civil liability insurance) or "franszyza redukcyjna" (deductible clause) have specific legal meanings that machine translation handles with variable accuracy.

When documents pass through translation before embedding, we lose semantic signal specific to Polish legal and insurance language. Retrieval operates on the translated version, not the original. Small translation errors compound across pipeline stages.

We ran an experiment to test whether native Polish models could outperform the translate-first approach.

## What We Tested

We tested Bielik — an open-source family of Polish LLMs trained on large Polish-language corpora — in two roles in our RAG pipeline:

1. As the embedding model, replacing Amazon Titan Embeddings or Cohere Embed
2. As the generation model, replacing Claude for producing final answers

Our evaluation set: 150 questions about Polish insurance policy documents, with expected answers validated by Polish-speaking insurance experts. This was the most labor-intensive part of the experiment, and the most important.

## Embedding Results: Significant Win

For the embedding step, Bielik demonstrated clear advantages for Polish insurance content.

Retrieval precision on our evaluation set increased by approximately 12 percentage points compared to the translate-to-English-then-embed approach. The gains were most pronounced for queries using insurance-specific terminology — exactly the queries where translation errors or approximations are most consequential.

The hypothesis: models trained primarily on Polish text learn the semantic relationships between Polish legal and business terms more accurately than models trained primarily on English, even when those English models perform well on general Polish text.

This result was robust across different query types and document categories. We're confident enough in it that Bielik embeddings are now the default for Polish document processing in our production pipeline.

## Generation Results: More Nuanced

The generation results were more nuanced. For straightforward queries — factual lookups, specific value extraction, simple clause identification — Bielik-generated answers were accurate and naturally expressed.

For complex multi-step queries — "how does this clause interact with the general insurance conditions given this type of incident?" — Claude 3.5 Sonnet on Bedrock, even with translated context, outperformed Bielik. This makes sense given the model size difference and the complexity of the reasoning required.

We adopted a hybrid approach: Bielik for embedding and retrieval, Claude for complex generation. We eliminated full document translation but retained query and response translation for the generation layer where needed.

## Practical Architecture

The resulting pipeline:

1. Documents embedded using Bielik — no translation required
2. User queries embedded using Bielik — in original Polish
3. Retrieval against Polish embedding index
4. Retrieved Polish chunks passed to Claude with Polish-aware system prompt
5. Claude generates response in Polish (it handles Polish well)
6. Optional translation to English for non-Polish-speaking users

Cost impact: elimination of translation API calls for the embedding stage (our largest document volume) reduced pipeline costs by approximately 20%. Latency improved proportionally.

## The GDPR Consideration

One dimension the English-language literature rarely discusses: for Polish enterprise companies, data residency and processing location matters under GDPR. Running a translate-first pipeline means your raw document content passes through a third-party translation API before any other processing.

Bielik can run on your own infrastructure — on-premises or in a dedicated cloud environment within the EU. For insurance documents containing sensitive policyholder data, this is not a minor point. It significantly simplifies the data processing agreement requirements and the "data stays where it should" story for legal and compliance teams.

This is particularly relevant in regulated sectors like insurance (where Polish KNF supervision applies), healthcare, and legal.

## Challenges We Didn't Expect

The experiment also surfaced challenges that weren't obvious before we ran it.

**Evaluation dataset quality.** Building a Polish evaluation set required Polish-speaking insurance domain experts — not just Polish speakers, but people who understood insurance policy semantics deeply enough to validate answers. This was harder to resource than expected.

**Benchmark gaps.** There are far fewer standard Polish NLP benchmarks than English ones. Measuring "is this better?" requires building your own gold standard rather than relying on published benchmarks.

**Documentation lag.** Bielik's documentation has improved significantly, but there are still areas where you're reading source code rather than docs. Experimentation is required. Budget time for it.

## What This Means for Polish Enterprise AI

Building native Polish-language AI systems without the translation crutch is a viable path. It requires:

→ Investment in Polish embedding and generation models
→ Polish-language evaluation datasets validated by domain experts
→ Engineering patience with models that are smaller and require more careful prompting

The Polish AI ecosystem is building these capabilities. Bielik is proof that native Polish language AI is not an academic project — it's a production tool. For organizations operating primarily in Polish markets, building on native Polish models is worth evaluating seriously.

If you're working with Polish-language documents in an AI context and want to compare notes on architecture, reach out. This is a domain where shared learning moves faster than independent experimentation.
