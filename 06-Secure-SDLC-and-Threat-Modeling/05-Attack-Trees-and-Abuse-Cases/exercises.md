# Attack Trees and Abuse Cases — Exercises

Use fictional applications and authorized test environments only. Explain assumptions where the scenario lacks details.

## Exercise 1 — Draw an attack tree

Root goal: **Access another user's private document.**

Tasks:
1. Create at least three alternative branches.
2. Include at least one AND relationship and one OR relationship.
3. Add prerequisites to each meaningful path.
4. Identify the asset and trust boundaries involved.
5. Select three mitigations and explain which paths they break.

## Exercise 2 — Write an abuse case

Feature: Password reset for a public web application.

Tasks:
1. Describe the legitimate use case.
2. Identify at least two possible abuse scenarios.
3. State attacker prerequisites and likely impact.
4. Define secure expected behavior.
5. Write at least four negative security tests.

## Exercise 3 — Find missing logic

A draft attack tree says:

```text
Goal: Perform an admin action
|
+-- Get an admin session
+-- Call the admin API
+-- API lacks authorization checks
```

Tasks:
1. Explain why the relationships are unclear.
2. Reorganize the tree using explicit AND/OR logic.
3. Add an alternative path involving a normal account and weak authorization.
4. Add one mitigation and one test for each path.

## Exercise 4 — Prioritize attack paths

For this training exercise, use risk score = likelihood × impact, each rated 1–5. Bands: 1–5 Low, 6–12 Medium, 13–25 High.

| Path | Likelihood | Impact |
|---|---:|---:|
| A: Public endpoint accepts a client-controlled price | 4 | 5 |
| B: Internal report has verbose error details | 3 | 2 |
| C: Revoked share link still works | 2 | 5 |
| D: Low-impact action lacks an audit event | 4 | 2 |

Tasks:
1. Calculate scores and bands.
2. Recommend an initial remediation order.
3. Explain why the score alone may be insufficient.
4. List what evidence you would collect before finalizing priorities.

## Exercise 5 — Turn vague controls into acceptance criteria

Rewrite each statement so it is specific and testable:

- “Secure the admin API.”
- “Prevent account enumeration.”
- “Make share links safe.”
- “Stop duplicate orders.”
- “Improve audit logging.”

For each, include a positive test and a negative test where applicable.

## Exercise 6 — Abuse-case review: document sharing

A new feature lets users create public links to documents. The product draft says links never expire, anyone with the URL can view the document, and revocation will be added later.

Tasks:
1. Identify at least five abuse cases or harmful outcomes.
2. Identify the assumptions that need confirmation.
3. Propose safer defaults and lifecycle controls.
4. Define tests for expiry, revocation, scope, and unauthorized access.
5. Identify the stakeholders who should approve residual risk.

## Exercise 7 — AND/OR practice

For each goal below, propose a small attack tree and label each relationship:
1. Create a duplicate order.
2. Read a confidential report.
3. Perform an action after an administrator's access is revoked.

Include prerequisites and defensive controls.

## Exercise 8 — Complete a mini deliverable

Choose a fictional system: online checkout, document sharing, account recovery, or an internal admin portal.

Create:
- One clearly scoped root attacker goal
- An attack tree with at least eight nodes
- Two abuse cases with preconditions and outcomes
- A risk rationale for at least three paths
- Four security requirements
- Four negative security tests
- Owners and review triggers

## Review checklist

- [ ] Root goal is precise and attacker-centered.
- [ ] AND/OR relationships are explicit.
- [ ] Prerequisites and assumptions are recorded.
- [ ] Abuse cases describe concrete steps and outcomes.
- [ ] Risks are assessed in business and technical context.
- [ ] Mitigations are mapped to specific paths.
- [ ] Tests verify both allowed and forbidden behavior.
- [ ] The model is updated when the feature or architecture changes.
