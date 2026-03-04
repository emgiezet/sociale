# Day 9 — Builder: AWS RDS Cost Problem
**Pillar:** Builder | **Week:** 2 | **CTA:** Comment

---

## LinkedIn Post

Our AWS RDS bill was growing 40% year over year.
We fixed it. Here's what we actually did.

Insly runs on PostgreSQL on AWS RDS. As our user base and data volume grew, the cost grew faster. 40% YoY is the kind of number that eventually gets you into a room with finance asking uncomfortable questions.

The obvious answer: optimize queries, add indexes, move some workloads.

The real answer: we needed to understand what was actually driving costs before we could fix anything.

Here's what we found:

→ **Read replicas running 24/7 for workloads that were bursty.** We had replicas scaled for peak load running continuously. 70% of the time, they were underutilized.

→ **Reporting queries running on primary.** A handful of long-running analytical queries were hitting the primary instance, competing with transactional traffic. Nobody had moved them to a read replica because "it works fine."

→ **Snapshots and storage growing without housekeeping.** Automated snapshots accumulating. Old environments not cleaned up. Storage inflation invisible until you look for it.

→ **One multi-tenant query pattern that hit the database hard for every request.** A query that was perfectly reasonable at 10,000 users but brutal at 150,000.

What we did:
→ Moved reporting to read replica + added schedule-based scaling
→ Fixed the multi-tenant query (added proper index, restructured the ORM call)
→ Implemented storage housekeeping automation
→ Added RDS cost dashboards to our weekly engineering review

Result: 35% reduction in RDS costs within 90 days.

**The lesson isn't "optimize your database." The lesson is: costs grow silently until you build visibility.**

What's the most surprising cost driver you've found in your cloud infrastructure?

#AWS #PostgreSQL #CloudCosts #EngineeringLeadership #FinOps

---

## Blog Post

### How We Cut AWS RDS Costs by 35%: A Story About Visibility, Not Just Optimization

When your cloud bill grows 40% year over year while your user base grows 30%, you have a problem. The problem might be that your infrastructure is expensive. Or it might be that your infrastructure costs have become invisible.

For us at Insly, it was both — but mostly the second one.

This post is about how we identified and addressed the actual cost drivers in our AWS RDS setup, and what we learned about the difference between optimization and visibility.

#### The Setup: What We Were Running

Insly runs on PostgreSQL, managed through AWS RDS. At the time we started this investigation, we were serving 150,000+ users across European markets, with a multi-tenant architecture where each broker organization's data is isolated within the same database cluster.

Our RDS setup had grown organically over several years — the hallmark of a database that started small and scaled through a series of "good enough for now" decisions. We had multiple read replicas, automated snapshots, a handful of different instance classes for different environments, and a mix of PostgreSQL versions that we'd been meaning to consolidate.

The bill was large and growing. But more than the size, what concerned me was that nobody on the team could precisely explain what was driving the growth.

#### Phase 1: Building Visibility Before Touching Anything

The first thing we did was not optimization. It was instrumentation.

We spent two weeks just building visibility into what our RDS infrastructure was actually doing. This meant:

→ AWS Cost Explorer by resource, not just by service — identifying which specific RDS instances were responsible for what fraction of cost
→ CloudWatch metrics for CPU utilization, I/O, and connection counts on each instance, mapped to time of day and day of week
→ Query performance data from Performance Insights, showing us which queries consumed the most database time
→ Storage breakdown: data storage vs. backup storage vs. snapshot storage

This visibility work was humbling. We found things we hadn't known were true.

#### What We Found

**Finding 1: Always-on read replicas for bursty workloads**

We had read replicas sized for our peak load, running 24/7. Our actual load pattern was highly bursty — Monday morning and end-of-month reporting periods were 5–10x the baseline load. Outside those periods, the replicas were 20–30% utilized.

Modern RDS Aurora supports automatic scaling for Aurora Serverless, but we were on standard RDS. The solution: Aurora replica auto-scaling, which allows replica instances to scale out during peak and scale in during off-peak. Implementation took a day. The cost impact was immediate.

**Finding 2: Analytical queries running on primary**

Several internal reporting jobs were running against the primary database instance. This had originally been set up because "the read replica sometimes has replication lag and we need current data." The reporting jobs had eventually been scheduled for nights and weekends to reduce impact. But "nights and weekends" meant they competed with end-of-timezone-day transaction traffic.

We moved them to a dedicated reporting replica and accepted the minor replication lag. For analytical reports, lag of a few seconds doesn't matter. The reduction in load on the primary instance improved transactional performance and reduced the instance class requirement.

**Finding 3: Storage inflation**

This was the most embarrassing finding. Automated snapshots were being retained for 35 days by default. We had old development and staging environments that had been partially decommissioned — the instances were deleted but the snapshots remained. We had a handful of manual snapshots taken for specific debugging sessions years ago.

Total snapshot storage: substantially more than our active data storage.

Implementing a snapshot retention policy and cleaning up old snapshots took a few hours and had no operational downside.

**Finding 4: One catastrophic query**

The most impactful single finding was a query in our multi-tenant data access layer that was, in the words of the engineer who eventually fixed it, "a query that made perfect sense at 10,000 rows and absolute nonsense at 10 million."

The query was joining across several tables without an index on the join key, which had been added to the schema but never indexed because the column was added via a migration that neglected the index creation. At our current scale, this query was executing on every request to a frequently-used part of the application, generating significant I/O on every hit.

Adding the missing index reduced query execution time from ~800ms to ~12ms. The I/O reduction was visible immediately in CloudWatch metrics.

#### The Results and the Lesson

Across these interventions, our RDS costs dropped approximately 35% within 90 days, with no reduction in performance or reliability.

But the real lesson isn't "optimize your database queries" or "review your snapshot retention." Those are the specific interventions. The real lesson is:

**Costs grow silently until you build visibility.**

None of the problems we found were new. The always-on read replicas had been that way for over a year. The analytical queries on primary had been there for two years. The orphaned snapshots had been accumulating since we started using RDS. The bad query was introduced in a migration eighteen months earlier.

We didn't find them because we weren't looking. And we weren't looking because we didn't have the dashboards, the alerts, or the regular review process that would have surfaced them.

The change that will have the most lasting impact isn't any of the specific optimizations. It's adding AWS cost visibility to our weekly engineering review. Not as a compliance exercise, but as a signal: when costs deviate from expectations, something in our system changed, and we want to understand what.

That visibility mindset — instrument first, understand before you optimize — is the lesson I'd carry into any infrastructure challenge.

What are the cost drivers in your AWS setup that you haven't looked at recently? The answer might surprise you.
