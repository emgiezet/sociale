---
day: 23
title: "RAG Quality Evaluation for Teams Without ML Engineers"
pillar: Educator
language: en
image: ../../images/day-22.jpg
image_unsplash_query: "data quality metrics dashboard"
---

# RAG Quality Evaluation for Teams Without ML Engineers

The most common failure mode I see in RAG development teams that aren't doing well: they deployed a system, it "seems to work," and they have no idea whether it's actually working.

This isn't a problem of technical sophistication. It's a problem of evaluation discipline. And unlike many aspects of machine learning, building good evaluation infrastructure for RAG systems doesn't require an ML background.

After building 3 RAG systems in production — two of which were expensive learning experiences — this is the evaluation framework I wish I'd had on day one.

## Why Evaluation Is Non-Negotiable

A RAG system that "seems to work" is generating confident-sounding answers of unknown quality. Without evaluation, you have no way to:

- Know when a code change improved or degraded quality
- Identify which types of questions your system handles poorly
- Distinguish retrieval failures (wrong documents retrieved) from generation failures (right documents, wrong answer)
- Build a case for continued investment or course correction

Teams that skip evaluation end up in a position I've seen too many times: months into a project, confident the system is good, and then a user demonstrates a systematic failure that's been present since deployment. We wasted two weeks optimizing prompts on our first RAG system before we ran proper retrieval evaluation and discovered that the retriever was the bottleneck all along. The prompts weren't the problem. The problem was earlier in the pipeline.

Build evaluation infrastructure before you build your first production feature. If you've already shipped without it, build it now.

## Step 1: Build Your Test Set

Your evaluation framework is only as good as your test set. A test set for RAG consists of three things:

**Questions**: Realistic queries that real users will ask, or as close to realistic as you can get. Pull them from your support tickets, user interviews, or usage logs. If you're pre-launch, create them with a domain expert who can simulate realistic queries.

**Expected source passages**: The specific passages from your document corpus that should be retrieved to answer each question. This requires domain expertise — someone who actually understands the subject matter well enough to know which sections of which documents are relevant.

**Expected answers**: What a correct, high-quality answer looks like for each question.

The validation work is labor-intensive. Plan for 30-60 minutes per question for thorough validation. For a 50-question test set, that's 25-50 hours of expert time. Budget this explicitly. It's the most leveraged investment you'll make in the project.

In insurance at Insly, our test set questions come from real underwriters and brokers. The expected answers are validated by people who handle insurance queries professionally. We can't fake this step. The quality of our evaluation is bounded by the quality of our domain expertise access.

Store your test set in version control. Update it as you discover new failure modes. A test set that doesn't evolve isn't capturing the full picture.

## Step 2: Measure Retrieval Quality

Retrieval quality measures whether your system is finding the right content before the LLM gets involved. This is the most commonly underrated measurement step.

**Precision**: Of the passages retrieved, what fraction are relevant? If you retrieved 5 passages and 3 were relevant, precision is 0.6.

**Recall**: Of the relevant passages in your corpus, what fraction were retrieved? If there are 5 relevant passages and you retrieved 3, recall is 0.6.

You can measure these manually with a spreadsheet: for each test question, list the passages that should have been retrieved, run your retrieval, and check which expected passages appear in the results.

For our production systems, we target >80% retrieval precision before spending time optimizing the generation layer. If retrieval precision is below that threshold, no amount of prompt engineering will fix the system. The LLM can't generate a good answer when the right information isn't in its context.

The automation path: RAGAS and similar tools provide these measurements using LLM-as-judge approaches — a separate LLM call evaluates whether each retrieved passage is relevant to the query. This scales better than manual review and is accurate enough for tracking trends.

## Step 3: Measure Answer Quality with LLM-as-Judge

Once you have retrieved passages, the generation step produces answers. Measuring answer quality has three critical dimensions:

**Faithfulness**: Is the answer supported by the retrieved passages, or is the LLM introducing information not present in the context? An unfaithful answer indicates hallucination — the model is generating plausible-sounding content that isn't grounded in what was retrieved.

**Relevance**: Does the answer actually address the question that was asked? An answer that's technically accurate but doesn't address the question is still a failure.

**Completeness**: Does the answer cover all important aspects of the question, or does it address only part of it?

For each of these, you write evaluation prompts that use an LLM to judge the generated answer. Here's the faithfulness eval prompt we use:

```
System: You are an evaluation judge. Assess whether the provided answer 
is faithful to the provided context.

Context: {retrieved_passages}
Question: {question}
Answer: {generated_answer}

Rate faithfulness on a 0.0 to 1.0 scale, where 1.0 means the answer is 
entirely supported by the context and introduces no information beyond it.
Provide a brief explanation, then provide your numerical rating.
```

This "LLM-as-judge" approach isn't perfect. LLMs can make evaluation errors. But it's accurate enough for tracking trends at scale and identifying systematic failures. We run these evaluations via AWS Bedrock, which keeps our insurance data within our existing compliance boundary.

For insurance specifically, we maintain what we call "hallucination red lines" — about 30 canary questions where any hallucination is a deployment blocker. Wrong coverage amounts, incorrect policy terms, fabricated legal references. These run on every deployment. One failure here stops the release.

## Step 4: Track Trends Over Time

Single-point evaluation is minimally useful. What you want is a trend: is quality improving, stable, or degrading?

Set up a weekly evaluation run that:

1. Runs your full retrieval and generation pipeline against the test set
2. Calculates all your metrics automatically
3. Records results in a dashboard or spreadsheet
4. Alerts you when any metric drops below a threshold

This gives you signal when changes affect quality — in either direction. When you deploy a new chunking strategy, you want to know immediately whether it helped or hurt. When you switch embedding models, you want to see the quality impact before it reaches users.

We require net improvement across all four metrics before merging significant retrieval or generation changes. Not just improvement on the metric you optimized for — net improvement across the board. Changes that improve faithfulness while degrading retrieval recall get blocked until both are addressed.

Make the evaluation dashboard visible to your whole team. Quality metrics visible only to engineers get optimized for engineering concerns. Quality metrics visible to product stakeholders get treated as the product feature they are.

## Step 5: Diagnose Failures Systematically

When evaluation reveals poor quality on specific questions, the next step is systematic diagnosis. The critical distinction:

**Retrieval failure**: The system retrieved passages that didn't include the relevant content. The generation model had no way to produce a good answer because the right information wasn't in its context. Fix: improve chunking, indexing, retrieval architecture.

**Generation failure**: The system retrieved relevant passages but the generated answer was still wrong or unfaithful. The model had the right information but didn't use it correctly. Fix: improve prompting, context formatting, or model selection.

These require different interventions. Conflating them leads to trying to fix generation problems with retrieval changes, or vice versa — which is exactly the mistake we made with our first RAG prototype before we built proper evaluation.

For each failing question, review: what did the system retrieve? Were those passages actually relevant? If not, retrieval failure. If yes, generation failure. Keep a categorized log of failures. Patterns in failure types will guide your most important optimization work.

## The Tooling We Actually Use

Our evaluation stack at Insly is intentionally simple:

- **Custom Python scripts** for running the test set and calculating metrics
- **LLM-as-judge via AWS Bedrock** for automated faithfulness and relevance scoring
- **A versioned test set** stored in our code repository alongside the application code
- **A simple spreadsheet dashboard** for tracking metric trends over time

We evaluated RAGAS as a complete solution. It's good. But we found that implementing the evaluation logic ourselves gave us better control over the specific metrics that matter for insurance — particularly the hallucination red lines that are specific to our domain. Start with RAGAS if you want faster initial setup. Build custom logic when you understand your domain-specific failure modes.

## Starting Today

If you have a RAG system in production without evaluation infrastructure, here's the minimum viable starting point:

1. Identify 20 representative questions from your actual use case
2. Have a domain expert validate expected answers for each
3. Run your system against all 20 questions
4. Manually score each answer: correct, partially correct, or incorrect
5. Calculate your overall quality score

A crude baseline is infinitely better than no baseline. From there, build the automation to track the trend.

The RAG systems that survive into genuine production usefulness are the ones that were evaluated from the start. The ones that aren't get quietly deprecated after users lose trust in them.

Your RAG system deserves to be evaluated, not just hoped at.
