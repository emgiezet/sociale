---
day: 9
title: "How We Cut AWS RDS Costs by 35%: A Story About Visibility, Not Just Optimization"
pillar: Builder
language: en
image: ../../images/day-09.jpg
image_unsplash_query: "cloud database optimization"
---

# How We Cut AWS RDS Costs by 35%: A Story About Visibility, Not Just Optimization

When your cloud bill grows 40% year over year while your user base grows 30%, you have a problem. The problem might be that your infrastructure is expensive. Or it might be that your infrastructure costs have become invisible.

For us at Insly, it was both — but mostly the second one.

This post is about how we identified and addressed the actual cost drivers in our AWS RDS setup, and what we learned about the difference between optimization and visibility.

## The Setup

Insly runs on PostgreSQL, managed through AWS RDS. At the time we started this investigation, we were serving 150,000+ users across European markets, with a multi-tenant architecture where each broker organization's data is isolated within the same database cluster.

Our RDS setup had grown organically over several years. We had multiple read replicas, automated snapshots, a handful of different instance classes for different environments, and a mix of configurations. The bill was large and growing. But more than the size, what concerned me was that nobody on the team could precisely explain what was driving the growth.

## Phase 1: Building Visibility Before Touching Anything

The first thing we did was not optimization. It was instrumentation.

We spent two weeks just building visibility into what our RDS infrastructure was actually doing:

→ AWS Cost Explorer by resource, not just by service — identifying which specific RDS instances were responsible for what fraction of cost
→ CloudWatch metrics for CPU utilization, I/O, and connection counts on each instance, mapped to time of day and day of week
→ Query performance data from Performance Insights, showing us which queries consumed the most database time
→ `pg_stat_statements` to capture query patterns across a full week — insurance workloads are not uniform, and a week of data showed us patterns we'd have missed in a 2-hour profiling window
→ Storage breakdown: data storage vs. backup storage vs. snapshot storage

This visibility work was humbling. We found things we hadn't known were true.

## What We Found

**Finding 1: Always-on read replicas for bursty workloads**

We had read replicas sized for our peak load, running 24/7. Our actual load pattern was highly bursty — Monday morning and end-of-month reporting periods were 5–10x the baseline load. Outside those periods, the replicas were 20–30% utilized.

Modern RDS Aurora supports automatic scaling for Aurora Serverless, but we were on standard RDS. The solution: Aurora replica auto-scaling, which allows replica instances to scale out during peak and scale in during off-peak. Implementation took a day. The cost impact was immediate.

**Finding 2: Analytical queries running on primary**

Several internal reporting jobs were running against the primary database instance. This had originally been set up because "the read replica sometimes has replication lag and we need current data." The reporting jobs had eventually been scheduled for nights and weekends to reduce impact. But "nights and weekends" meant they competed with end-of-timezone-day transaction traffic.

We moved them to a dedicated reporting replica and accepted the minor replication lag. For analytical reports, lag of a few seconds doesn't matter. The reduction in load on the primary instance improved transactional performance and reduced the instance class requirement.

**Finding 3: Storage inflation**

Automated snapshots were being retained for 35 days by default. We had old development and staging environments that had been partially decommissioned — the instances were deleted but the snapshots remained. We had manual snapshots taken for specific debugging sessions years ago.

Total snapshot storage: substantially more than our active data storage.

Implementing a snapshot retention policy and cleaning up old snapshots took a few hours and had no operational downside.

**Finding 4: One catastrophic query**

The most impactful single finding was a query in our multi-tenant data access layer that was, in the words of the engineer who eventually fixed it, "a query that made perfect sense at 10,000 rows and absolute nonsense at 10 million."

The query was joining across several tables without an index on the join key. The column had been added via a migration that neglected the index creation. At our current scale, this query was executing on every request to a frequently-used part of the application.

Adding the missing index reduced query execution time from ~800ms to ~12ms. The I/O reduction was visible immediately in CloudWatch metrics.

Three of our top-10 most expensive queries accounted for over 60% of CPU load. Two of those three had no indexes on filtered columns. Legacy code, added years ago, never revisited.

## The Results

Across these interventions, our RDS costs dropped approximately 35% within 90 days, with no reduction in performance or reliability.

But the real lesson isn't "optimize your database queries" or "review your snapshot retention."

## The Real Lesson

**Costs grow silently until you build visibility.**

None of the problems we found were new. The always-on read replicas had been that way for over a year. The analytical queries on primary had been there for two years. The orphaned snapshots had been accumulating since we started using RDS. The bad query was introduced in a migration eighteen months earlier.

We didn't find them because we weren't looking. And we weren't looking because we didn't have the dashboards, the alerts, or the regular review process that would have surfaced them.

The change that will have the most lasting impact isn't any of the specific optimizations. It's adding AWS cost visibility to our weekly engineering review. Not as a compliance exercise, but as a signal: when costs deviate from expectations, something in our system changed, and we want to understand what.

That visibility mindset — instrument first, understand before you optimize — is the lesson I'd carry into any infrastructure challenge.

What are the cost drivers in your AWS setup that you haven't looked at recently? The answer might surprise you.
