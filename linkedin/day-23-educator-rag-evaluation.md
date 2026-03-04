# Day 23 — Educator: RAG Quality Evaluation Without ML Team
**Pillar:** Educator | **Week:** 5 | **CTA:** Save

---

## LinkedIn Post

How to evaluate your RAG system's quality without an ML team.

Most RAG tutorials end at "it generated an answer." That's not evaluation. That's hope.

Here's the practical framework I use — no ML background required:

**Step 1: Build a human-validated test set**
50–100 questions from real users (or realistic simulations). For each question, a domain expert manually writes the expected answer AND identifies the source passages that should be retrieved.
→ This is the most labor-intensive step and the most important

**Step 2: Measure retrieval quality**
For each test question, check:
→ Were the expected source passages retrieved?
→ What percentage of retrieved passages were actually relevant?

You don't need fancy tools. A spreadsheet works. Track precision (how much retrieved content was relevant?) and recall (how much relevant content was retrieved?).

**Step 3: Measure answer quality with LLM-as-judge**
Use a separate LLM call to evaluate each generated answer:
- Faithfulness: "Is this answer supported by the retrieved context?" (0–1)
- Relevance: "Does this answer address the question?" (0–1)
- Completeness: "Does this answer cover all important aspects?" (0–1)

RAGAS automates this. Or you can write the eval prompts yourself.

**Step 4: Track trends, not just numbers**
Single point-in-time evaluation isn't useful. Run evaluation weekly. Track whether quality is improving, stable, or degrading after changes.

**Step 5: Investigate failures**
For every question where quality is poor: was it a retrieval failure (wrong passages) or a generation failure (right passages, wrong answer)? Different failures need different fixes.

**This process costs time, not ML expertise.**

The hardest part is Step 1: getting domain experts to validate 50+ questions. The second hardest is Step 4: making evaluation a habit, not a one-time event.

Save this. Your RAG system deserves to be evaluated, not just hoped at.

#RAG #AIEngineering #LLMEvaluation #RAGAS #ProductionAI

---

## Blog Post

### RAG Quality Evaluation for Teams Without ML Engineers

The most common thing I see in RAG development teams that aren't doing well: they deployed a system, it "seems to work," and they have no idea whether it's actually working.

This is not a problem of technical sophistication. It's a problem of evaluation discipline. And unlike many aspects of ML, building good evaluation infrastructure for RAG systems doesn't require an ML background.

This post is a practical guide to evaluating your RAG system's quality — written for software engineers, not ML researchers.

#### Why Evaluation Is Non-Negotiable

Before the framework, the motivation.

A RAG system that "seems to work" is generating confident-sounding answers of unknown quality. Without evaluation, you have no way to:
- Know when a code change improved or degraded quality
- Identify which types of questions your system handles poorly
- Distinguish retrieval failures (wrong documents retrieved) from generation failures (right documents, wrong answer)
- Build a case for continued investment or course correction

Teams that skip evaluation end up in a position I've seen too many times: months into a project, confident the system is good, and then a user demonstrates a systematic failure that's been present since deployment.

Build evaluation infrastructure before you build your first production feature. If you've already shipped without it, build it now.

#### The Test Set: Foundation of Everything

Your evaluation framework is only as good as your test set. A test set for RAG consists of:

1. **Questions**: Realistic queries that real users will ask, or as close to realistic as you can get
2. **Expected source passages**: The specific passages from your document corpus that should be retrieved to answer each question
3. **Expected answers**: What a correct, high-quality answer looks like

The questions should come from real users if possible — pull them from your support tickets, user interviews, or usage logs. If you're building before you have users, create them with a domain expert who can simulate realistic queries.

The expected passages and expected answers must be validated by a domain expert — someone who actually knows the subject matter well enough to identify correct answers and the evidence that supports them.

This validation work is labor-intensive. Plan for 30-60 minutes per question for thorough validation. For a 50-question test set, that's 25-50 hours of expert time. This is worth budgeting explicitly because it's the most leveraged investment you'll make in the project.

Store your test set in version control. Update it over time as you discover new failure modes. A test set that doesn't evolve isn't capturing the full picture of where your system can fail.

#### Measuring Retrieval Quality

Retrieval quality measures whether your system is finding the right content before the LLM gets involved.

**Precision**: Of the passages retrieved, what fraction are relevant? If you retrieved 5 passages and 3 were relevant, precision is 0.6.

**Recall**: Of the relevant passages in your corpus, what fraction were retrieved? If there are 5 relevant passages and you retrieved 3, recall is 0.6.

**Context relevance**: A softer metric — rather than binary relevant/not-relevant, how relevant are the retrieved passages on a 0-1 scale?

You can measure these manually with a spreadsheet: for each test question, list the passages that should have been retrieved, run your retrieval, and check which expected passages appear in the results. Calculate precision and recall from the counts.

For automation, tools like RAGAS provide these measurements using LLM-as-judge approaches — a separate LLM call evaluates whether each retrieved passage is relevant to the query. This scales better than manual review and is accurate enough for tracking trends.

#### Measuring Answer Quality

Once you have retrieved passages, the generation step produces answers. Measuring answer quality has three dimensions:

**Faithfulness**: Is the answer supported by the retrieved passages, or is the LLM introducing information not present in the context? An unfaithful answer indicates the LLM is hallucinating rather than grounding its response in retrieved content.

**Relevance**: Does the answer actually address the question that was asked? An answer that's technically accurate but doesn't address the question is still a failure.

**Completeness**: Does the answer cover all important aspects of the question, or does it address only part of it?

For each of these, you can write evaluation prompts that use an LLM to judge the generated answer:

```
System: You are an evaluation judge. Assess whether the provided answer is faithful to the provided context.

Context: {retrieved_passages}
Question: {question}
Answer: {generated_answer}

Rate faithfulness on a 0.0 to 1.0 scale, where 1.0 means the answer is entirely supported by the context.
Provide a brief explanation, then provide your numerical rating.
```

This "LLM-as-judge" approach isn't perfect — LLMs can make evaluation errors — but it's accurate enough for tracking trends at scale and identifying systematic failures.

RAGAS implements these metrics as a library with a clean API. If you're starting from scratch, I'd recommend using it rather than implementing from scratch.

#### Tracking Trends Over Time

Single-point evaluation is minimally useful. What you want is a trend: is quality improving, stable, or degrading?

Set up a weekly evaluation run that:
1. Runs your full retrieval and generation pipeline against the test set
2. Calculates all your metrics automatically
3. Records results in a dashboard or spreadsheet
4. Alerts you when any metric drops below a threshold

This gives you signal when changes affect quality — in either direction. When you deploy a new chunking strategy, you want to know immediately whether it helped or hurt. When you switch embedding models, you want to see the quality impact before it reaches users.

Make the evaluation dashboard visible to your whole team. Quality metrics that are only visible to engineers tend to be optimized for engineers. Quality metrics that are visible to product managers and stakeholders get prioritized differently.

#### Diagnosing Failures

When evaluation reveals poor quality on specific questions, the next step is diagnosis. The critical distinction:

**Retrieval failure**: The system retrieved passages that didn't include the relevant content. The generation model had no way to produce a good answer because the right information wasn't in its context. Fix: improve chunking, indexing, retrieval architecture.

**Generation failure**: The system retrieved relevant passages but the generated answer was still wrong or unfaithful. The model had the right information but didn't use it correctly. Fix: improve prompting, context formatting, or model selection.

These failures require different interventions. Conflating them leads to trying to fix generation problems with retrieval changes, or vice versa. The evaluation framework helps you separate them.

For each question that fails evaluation, review: what did the system retrieve? Were those passages actually relevant? If not, retrieval failure. If yes, generation failure. Keep a categorized log of failures — patterns in failure types will guide your most important optimization work.

#### Starting Today

If you have a RAG system in production without evaluation infrastructure, here's the minimum viable starting point:

1. Identify 20 representative questions from your actual use case
2. Have a domain expert validate expected answers for each
3. Run your system against all 20 questions
4. Manually score each answer: correct, partially correct, or incorrect
5. Calculate your overall quality score

That's it. A crude baseline is infinitely better than no baseline. From there, build the automation to track the trend.

The RAG systems that survive into genuine production usefulness are the ones that were evaluated from the start. The ones that don't get quietly deprecated after users lose trust in them.

Your RAG system deserves to be evaluated, not just hoped at. Start today.
