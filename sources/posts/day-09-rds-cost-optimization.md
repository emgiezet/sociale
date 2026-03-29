---
day: 9
title: "Our AWS RDS bill was growing 40% year over year. Here's what we did about it."
pillar: Builder
format: Technical
language: English
scheduled_date: 2026-04-02
posting_time: "07:30 CET"
hashtags: ["#AWS", "#DatabaseOptimization", "#CloudCosts", "#SoftwareEngineering"]
image: ./images/day-09.jpg
image_unsplash_query: "cloud database optimization"
cta: "What's your biggest AWS cost surprise? Comment below."
---

Our AWS RDS bill was growing 40% year over year. Here's what we did about it.

At Insly, we run multi-tenant insurance software across European markets. Data volume grows. That's expected. But 40% YoY growth in RDS costs without proportional user growth meant something was wrong. And it wasn't the database.

**Step 1: Diagnosis**
We started with AWS Cost Explorer and RDS Performance Insights. Within two hours we identified the top 10 most expensive queries by cumulative execution time 🕵️ Three of them accounted for over 60% of the CPU load. Two of those three had no indexes on the filtered columns.

Legacy code. Added years ago. Never revisited 😐

**Step 2: Query analysis**
We used `pg_stat_statements` to capture query patterns across a full week. This was more useful than point-in-time profiling. Insurance workloads are not uniform: broker activity peaks at certain hours, quarter-end reporting creates spikes. A week of data showed us patterns we'd have missed in a 2-hour window.

**Step 3: Targeted indexing**
We didn't add indexes blindly. Each candidate went through the same check:
→ How often does this query run per day?
→ What's the write-to-read ratio on this table?
→ What's the actual selectivity of the proposed index?

Over-indexing on high-write tables can make things worse. We added 6 indexes, removed 3 that were unused and adding write overhead.

**Step 4: Instance right-sizing**
Performance Insights showed our peak CPU utilization was 35%. We were on an instance sized for 70%+ headroom. Dropped one instance tier on two non-critical replicas. Kept headroom where it mattered.

**Result: RDS costs stopped growing. Year-over-year bill is flat while data volume continues to increase.**

This wasn't clever architecture. It was measurement, then action. In that order.

What's your biggest AWS cost surprise? Comment below.

#AWS #DatabaseOptimization #CloudCosts #SoftwareEngineering
