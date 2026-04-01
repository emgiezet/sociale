---
day: 35
title: "Three Weeks After the Workshops: What Actually Changed"
pillar: Trenches
language: en
image: ../../images/day-35.jpg
image_unsplash_query: "team meeting developers collaboration office"
---

# Three Weeks After the Workshops: What Actually Changed

Three weeks after running AI workshops for 15 developers at Insly, I want to write the honest account. Not the inflated one. Not the disappointing one. The one that's actually true.

Here's the honest answer: a lot changed, some things didn't, and the things that changed aren't the things that show up in productivity dashboards.

## The Change I Was Watching For — and Didn't Get

Let me start with what I was hoping to see but can't claim: measurable productivity gains. I didn't run a controlled study. I have no before/after velocity numbers. Anyone who tells you they ran a 3-day AI workshop and measured a 40% productivity increase is either measuring the wrong thing or telling you what you want to hear.

What I have is something more useful: observations of behavioural change. Specific things people do differently now versus three weeks ago. Those matter more than post-workshop surveys, which measure enthusiasm, not change.

## The Curve Nobody Tells You About

There's a curve to team AI adoption that I've watched happen both in my own engineering team at Insly and now in a different group of developers:

**Skepticism.** Before the workshops, the dominant mode was avoidance with a vague sense of guilt. "I should be using this." But the tools felt overwhelming, the learning curve felt steep, and the risk of looking incompetent by doing it wrong felt real. Experienced engineers are particularly vulnerable to this — someone with 10 years of instincts doesn't want to be a beginner again.

**Curiosity.** The first day of workshops cracked this open. Not because I showed them magic, but because I showed them boring things — specific, practical, reproducible things they could do the next morning. Curiosity is not inspiration. It's "I wonder if this works for my thing too."

**First wins.** The first win is disproportionately important. One developer told me, about a week after the workshops: "I was stuck on a weird Symfony edge case and just described it to Claude. It got me unstuck in five minutes. I would have spent an hour on it." That's not a productivity number. It's a data point that resets the default assumption from "probably won't help" to "might as well try."

**Habit.** This is where we are at three weeks. Partial habit formation. Some people are solidly in it. Some are dipping in occasionally. A few are still in "I need to get around to that." That's normal. Habits don't form uniformly across a team.

## What I Observed — Specifically

I want to be specific because vague reports of "people are using AI more" are useless. Here's what I actually saw:

**One senior developer started adding an "AI review" note to his PRs.** Before submitting for human review, he runs the diff through Claude with a specific prompt and includes a section in the PR description: what the AI flagged, and how he addressed it (or why he didn't). His reviewers told me they noticed a drop in small review comments — the stuff that used to clog the thread.

**One developer who had been avoiding test writing started writing tests.** Her explanation: "I've been putting off covering this old module for months. I described it to Claude and got a first set of test cases I could actually work with. I ended up writing tests for three modules last week." She didn't suddenly love writing tests. The activation energy dropped enough that she did it.

**The questions in the team chat changed.** Before: "How do I do X in Go?" (asked to other humans, answered by other humans). After, increasingly: "I asked Claude about X, it suggested Y, does that look right to anyone?" That's a different pattern — the AI becomes the first-pass tool, humans become the validators. For the humans, that's a better use of time.

**One mid-level developer started using AI for debugging.** Describing a confusing stack trace to Claude and asking "what might cause this?" as a first step before posting to the team. This is exactly the kind of thing that reduces "interrupt costs" on senior developers — the constant tap on the shoulder that fragments focused time.

## What Didn't Change

I want to be honest about this, because the "after workshop" story is usually over-polished.

**Legacy code adoption is slower.** This was predictable but still worth naming. The developers working primarily with the older Symfony codebase reported more friction. "I don't know how to give Claude enough context about the system to get useful answers." That's a real problem. Working with legacy code with AI requires different techniques — architectural summarisation, targeted context provision, working with smaller slices — and that's more advanced than what we covered in three days. It's a separate workshop.

**The sceptics are still sceptical.** Not hostile, but two or three people in the group are in "I'll believe it when I see the results consistently" mode. That's a legitimate position. They're not blocking anyone else. They're just not believers yet. I've learned not to treat scepticism as a problem to solve immediately — give it time, let the first wins from colleagues be the persuasion.

**Code quality review habits are inconsistent.** The AI pre-review workflow I showed in the workshops requires discipline to maintain. It adds a few minutes to the PR preparation process. Some people are doing it consistently. Some are doing it when they remember. That's the normal adoption pattern for anything that adds small upfront cost for downstream benefit.

## The Psychological Safety Factor

This is the thing I didn't anticipate fully, and I now think it's the most important variable in team AI adoption.

The barrier to trying AI in front of your colleagues isn't technical. It's social. There's a fear of looking naive — of asking a stupid question, of generating something bad, of having colleagues see that you don't know how to use a tool that you "should" know how to use.

The workshops helped with this by making the exploration collective. Everyone was learning together, including the most senior people. When a director-level developer publicly struggled with a prompt in the workshop and laughed about it, something shifted. The space for not-knowing-yet opened up.

Three weeks later, the developers who made the most progress are the ones who used the workshop to "have permission" to try AI in front of their team. Not alone, in private, with no witnesses. In the normal work context, where their colleagues could see them experimenting.

That permission — the social normalisation of "I'm trying something and I don't know if it'll work" — is not something you can get from a YouTube tutorial. It requires a shared experience.

## What I'd Do Differently

If I ran these workshops again — and I will — I'd add a two-week check-in structure. Not a meeting. A lightweight async format: one message per person per week, sharing one thing they tried, one thing that worked, one thing that didn't. The purpose isn't accountability. It's continued social normalisation of experimentation.

The workshops create a moment of shared vocabulary and shared experience. The check-ins would extend that window before the momentum dissipates into normal work patterns.

I'd also spend more time on legacy code workflows. It came up too many times in the three weeks after for me to keep treating it as an edge case. It's central to what most working engineers actually face.

## The Honest Summary

Three weeks out: partial adoption, meaningful behavioural change in a subset of developers, slower change in others, honest gaps that I'd address differently next time.

Is that enough to call the workshops a success? I think so — not because the numbers are good, but because the change is real and sustainable. The developers who changed their habits didn't do it out of enthusiasm that will fade. They did it because they tried something specific, it worked, and they kept doing it.

That's how lasting change happens. Not with inspiration. With evidence.

If you're thinking about running something similar for your team — or having someone run it for you — the next post is the practical answer to that question.
