# Day 6 — Builder: 150,000 Users, 0 Downtime SSO Migration
**Pillar:** Builder | **Week:** 2 | **CTA:** Comment

---

## LinkedIn Post

150,000 users. 1 Microsoft SSO integration. 0 downtime during migration.

People always ask about the technical part. The technical part was the easy part.

Here's the story of Insly's Microsoft SSO migration — and what it actually taught me about engineering at scale.

**The context:**
Insly is insurance management software used by brokers across Europe. Many of our enterprise clients use Microsoft 365. The request: let their teams log in with their Microsoft credentials instead of maintaining a separate Insly password.

Straightforward feature. Right?

**What made it hard:**
→ 150,000+ active users, across different account types, with different auth flows
→ Enterprise clients with IT security teams who needed to approve every change
→ Some clients on older Microsoft tenant configurations with different OAuth behaviors
→ A multi-tenancy architecture where each broker operates in isolation

**The approach that kept us at 0 downtime:**
→ Feature flagged the entire migration — old auth and new auth running simultaneously
→ Per-client rollout: enabled SSO for one organization at a time, with their IT team on a call
→ Fallback always available: if SSO fails, the legacy auth path still works
→ 30-day monitoring period after each organization migrated before removing the fallback

The thing I'd tell any engineer planning a large-scale auth migration: **your migration isn't a technical problem. It's a coordination problem.**

We spent 20% of the project timeline on the integration code. We spent 80% on coordination: client communication, rollout sequencing, fallback testing, edge case discovery.

The engineering was solid. The coordination is what made it safe.

What's your experience with large-scale auth migrations? I'd love to hear how others have handled the non-technical complexity.

#SoftwareEngineering #MicrosoftSSO #EnterpriseEngineering #TechLeadership #InsurTech

---

## Blog Post

### Zero Downtime SSO Migration at Scale: What the Technical Post-Mortems Don't Tell You

When people ask about our Microsoft SSO migration at Insly, they want to know about the OAuth flows, the multi-tenancy architecture, the token handling. Those things matter. But the migration didn't succeed because we got the technical details right. It succeeded because we got the coordination right.

This post is about the part that technical case studies usually skip.

#### The Starting Point

Insly serves over 150,000 users — insurance brokers, underwriters, and administrative staff across European markets. Many of our enterprise clients operate on Microsoft 365, which means their employees are already authenticated through Microsoft's identity platform for everything else they do at work.

The request came from multiple large clients simultaneously: let our staff use their Microsoft credentials to log in to Insly. Don't make them maintain a separate password. Integrate with our existing Microsoft tenant.

This is a standard enterprise feature request. "Just add SSO" — to use a phrase I introduced on Day 2.

#### Why It's Actually Hard

The technical complexity was real. Our architecture is multi-tenant, with each broker organization operating in strict isolation. Adding SSO required mapping Microsoft tenant identities to Insly organization memberships without conflating them. Different Microsoft tenant configurations have different OAuth 2.0 behaviors. Enterprise clients often have security policies that restrict which external applications can participate in SSO flows.

But the technical problems had technical solutions. We've handled complex auth flows before. The library support for Microsoft MSAL is mature. AWS Cognito, which we use for identity management, integrates cleanly with external identity providers.

The harder problems were coordination problems.

#### The Coordination Problems

**Problem 1: Enterprise IT security review.** Every large client we migrated needed approval from their IT security team before enabling SSO. This meant providing documentation of our OAuth implementation, our token handling, our session management, and our incident response procedures. Some IT teams had review cycles of four to six weeks. Some had requirements we hadn't anticipated — specific token lifetimes, specific logout behavior, specific audit logging.

We started collecting these requirements three months before the first migration. We still encountered surprises.

**Problem 2: Account matching.** When a user's Microsoft account is linked to their Insly account for the first time, we need to match them. This sounds straightforward until you encounter: multiple Insly accounts with the same email address (it happens more than you'd think), email addresses that have changed since the Insly account was created, shared accounts that multiple people have been using under one email.

Each anomaly required a manual review and a decision. We developed a matching protocol and ran the full matching for each client before their migration window, flagging exceptions for human review.

**Problem 3: Rollout sequencing.** We couldn't migrate all clients at once. We had to sequence them — starting with smaller clients who could serve as a test population, moving to larger clients with more complex configurations. Each migration needed a dedicated window with the client's IT team available, a pre-migration checklist, and a post-migration monitoring period.

We migrated over 30 client organizations across a six-month period.

#### The Technical Approach That Made It Safe

Given the coordination complexity, we made two architectural decisions that were non-negotiable from the start:

**Feature flags, not big-bang migrations.** The SSO system was built alongside the existing authentication system, not replacing it. A per-organization feature flag determined which authentication path a given user would take. Enabling SSO for a client was a configuration change, not a deployment.

**Always-available fallback.** For a minimum of 30 days after SSO was enabled for a client, their users could still log in with legacy credentials if SSO failed for any reason. This wasn't about distrust of our implementation — it was about the reality that enterprise IT environments have their own dynamics. A Microsoft tenant configuration can change. An IT policy can be updated. Having a fallback meant that our migration was never a dependency for a client's ability to access their software.

These two decisions added complexity to the implementation but removed risk from every single migration event. The tradeoff was obviously correct in retrospect. It wasn't obvious before we made it.

#### What 0 Downtime Actually Means

We had 0 downtime during the migration period. But "downtime" is a narrow metric. We had:

→ Two SSO authentication failures for specific users during the first week (resolved by identity matching corrections)
→ One client where the fallback auth path was used for three days while their IT team resolved a tenant configuration issue
→ One client who requested a migration rollback after SSO revealed that their user list included 40 inactive accounts they hadn't known about

None of these were critical incidents. All of them would have been if we hadn't built the coordination infrastructure to detect and respond to them quickly.

The coordination infrastructure — shared Slack channels with client IT teams, daily check-in calls during active migration windows, a per-client migration status dashboard — was as important as the technical implementation.

#### The Lesson for Any Large-Scale Migration

If you're planning a migration that touches your auth system, your data model, or any other foundational layer — here is the heuristic I'd give you:

Estimate the engineering time. Then multiply it by three and budget that for coordination.

Not because engineering is easy. Because coordination is the thing that determines whether engineering effort leads to a safe, successful change or a high-risk event that puts your users at risk.

The best migration I've ever seen wasn't the one with the most elegant architecture. It was the one where every person who needed to know something knew it before they needed to know it.

I'd love to hear about your experiences with large-scale migrations — auth changes, database transformations, API versioning at scale. What was the coordination challenge that surprised you most?
