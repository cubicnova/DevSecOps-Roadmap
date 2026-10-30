# Suggested Solutions and Assessment Notes

These are sample reasoning paths. Your exact scores may differ if you document credible evidence and consistently apply your organization's criteria.

## Lab 1 — Risk statement
Example: “Because the invoice API does not enforce object-level authorization, an authenticated customer may retrieve invoices belonging to other customers by changing the invoice identifier, causing unauthorized disclosure of confidential financial and personal information.”

This statement identifies a weakness, event, affected asset, and consequence.

## Lab 2 — Rating rationale
For an exposed sensitive-data scenario, a learner might choose likelihood 3 (Possible) and impact 4 (Major), score 12 (High). The important part is explaining assumptions: internet exposure, exploit complexity, authentication, existing controls, data sensitivity, affected population, and evidence. A different score can be valid with a stronger rationale.

## Lab 3 — Compare two risks
- Risk A: 2 × 5 = 10.
- Risk B: 4 × 3 = 12.

The matrix makes Risk B numerically higher, but Risk A may still need urgent attention if it affects a critical system, has a legal reporting obligation, is actively exploited, or could cause irreversible harm. Use the score with context, not as the only decision rule.

## Lab 4 — Residual risk
Possible controls: gateway rate limits, per-user quotas, timeouts, query-cost ceilings, caching where appropriate, autoscaling/capacity safeguards, and alerting. Verification can include controlled load tests, bypass attempts, configuration review, and alert validation. Rate likelihood and impact separately after testing; document assumptions and remaining failure modes.

## Lab 5 — Treatment choices
1. Avoid or redesign the feature if its risk cannot be reduced to an acceptable level.
2. Mitigate by fixing and validating the code.
3. Accept only if the risk is within the approver's authority, rationale is recorded, compensating controls exist, and the exception expires.
4. Transfer/share selected financial consequences where appropriate, while retaining operational accountability and applying suitable security controls.

## Lab 6 — Risk register
A strong register includes distinct scenarios, evidence-based ratings, current control status, actions with owners and dates, and residual-risk review. Example categories:
- Confidentiality: unauthorized record access.
- Integrity: unauthorized order modification.
- Availability: API resource exhaustion.
- Privilege: compromised developer identity can deploy unreviewed code.
Other valid risks may include exposed storage, secrets in logs, weak backup recovery, or vulnerable dependencies.

## Lab 7 — Acceptance record
A suitable record includes the exact scope, risk scenario, rating and rationale, business need, alternatives, compensating controls, named risk owner and approver, start and expiry dates, remediation owner/milestone, monitoring, and triggers for early reassessment. The approval must come from an authority permitted by policy.

## Lab 8 — Reassessment
Public exposure changes the threat surface and may increase likelihood; the new integration adds data flows, trust boundaries, credentials, and third-party dependencies. Revisit asset sensitivity, reachability, authentication, authorization, logging, and business impact. Record the changed assumptions and evidence.

## Lab 9 — Peer review rubric (20 points)
- Clear risk scenario: 0–4
- Evidence-based likelihood and impact: 0–4
- Consistent scoring: 0–3
- Practical treatment with owner/date: 0–4
- Residual-risk verification: 0–3
- Acceptance governance and review: 0–2

A high-quality assessment explains uncertainty and supports decisions rather than merely producing a number.
