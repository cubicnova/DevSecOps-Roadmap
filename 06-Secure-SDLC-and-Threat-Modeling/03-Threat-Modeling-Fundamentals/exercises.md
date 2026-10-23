# Threat Modeling Exercises

Use the fictional systems below. No real target testing is required. Write down assumptions where details are missing.

## Exercise 1 — Identify assets and trust boundaries

A web application lets users upload PDFs, stores them in cloud object storage, and records file ownership in a database. A background worker scans files before making them available for download.

Tasks:
1. List at least five assets.
2. Identify the actors and system components.
3. Identify at least three trust boundaries.
4. List the important data flows.
5. Name two assumptions you would confirm with the engineering team.

## Exercise 2 — Apply STRIDE

Use the file-upload system from Exercise 1.

Tasks:
1. Write one plausible threat scenario for each STRIDE category.
2. Identify the affected component or data flow.
3. Propose one specific mitigation for each scenario.
4. Define a validation test for each mitigation.
5. Explain which scenarios overlap and why.

## Exercise 3 — Prioritize risk

Use this training scale: likelihood 1–5, impact 1–5, score = likelihood × impact. For this exercise only, scores 1–5 are Low, 6–12 Medium, and 13–25 High.

| Threat | Likelihood | Impact |
|---|---:|---:|
| A | 4 | 5 |
| B | 2 | 3 |
| C | 5 | 2 |
| D | 1 | 5 |

Tasks:
1. Calculate each score.
2. Assign a training risk band.
3. Explain why score alone should not determine remediation order.
4. Select one risk for immediate action and justify your choice.

## Exercise 4 — Review an unsafe design

An API accepts this JSON body:

```json
{
  "user_id": "user-123",
  "role": "admin",
  "document_id": "doc-456"
}
```

The API uses `user_id` to decide whose document to return and trusts `role` to decide whether admin functions are allowed.

Tasks:
1. Identify at least three threats.
2. Map each threat to STRIDE where appropriate.
3. Describe the design flaw behind each threat.
4. Recommend server-side controls.
5. Write two negative security tests.

## Exercise 5 — Build an attack tree

Attacker goal: “Access a private document without permission.”

Tasks:
1. Put the goal at the root.
2. Add at least three alternative branches, such as abusing authorization, stealing a session, or exploiting a sharing-link design.
3. Add two or more steps beneath each branch.
4. Mark which branches require an account, privileged access, or another precondition.
5. Choose mitigations that break the most important paths.

## Exercise 6 — Write actionable mitigations

Rewrite each vague statement into a testable requirement:

- “Make uploads secure.”
- “Improve logging.”
- “Prevent brute force.”
- “Protect sensitive data.”
- “Validate users.”

Each requirement should identify the expected system behavior and at least one way to verify it.

## Exercise 7 — Threat-model change review

A service originally stores all documents privately. A product change introduces shareable links that work without sign-in.

Tasks:
1. Identify new assets, entry points, and assumptions.
2. Identify likely STRIDE threats and privacy concerns.
3. Define safe defaults and link lifecycle controls.
4. Decide which existing threats need to be reassessed.
5. List the tests and approvals required before release.

## Exercise 8 — Mini threat-model deliverable

Choose one fictional system: password reset, API key management, online checkout, or internal admin portal.

Create a one-page threat model containing:
- Scope and assumptions
- Assets and actors
- A small DFD or textual flow
- Trust boundaries
- At least six threat scenarios
- Risk ratings and rationale
- Mitigations, owners, and validation tests
- Residual-risk decisions and review triggers

## Self-review checklist

- [ ] Scope and assumptions are explicit.
- [ ] Actors, data stores, processes, flows, and trust boundaries are shown.
- [ ] Sensitive assets and privileged interfaces are included.
- [ ] Threats are scenarios, not just category names.
- [ ] Risk ratings include a rationale.
- [ ] Mitigations are specific and testable.
- [ ] Every accepted risk has an owner and review point.
- [ ] The model will be updated after relevant architecture changes.
