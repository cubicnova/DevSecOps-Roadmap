# Practical Labs: Security Risk Assessment

Use a fictional environment or systems you are authorized to assess. Do not include real secrets or sensitive personal data in the exercises.

## Lab 1 — Write a risk scenario
Scenario: A customer portal stores invoices and exposes an API endpoint `/api/invoices/{id}`.

Tasks:
1. Identify the asset and business objective.
2. Write a concise threat event.
3. Identify the weakness or missing control.
4. Describe the possible consequence.
5. Rewrite the risk as one complete cause–event–impact statement.

**Deliverable:** one risk statement and supporting assumptions.

## Lab 2 — Rate likelihood and impact
Use the illustrative 1–5 scales in `README.md`.

Tasks:
- Rate a scenario involving exposed sensitive data.
- Explain the evidence for likelihood.
- Explain business and technical impact separately.
- Calculate the score.
- Identify what new evidence could change the rating.

**Deliverable:** one scored risk with rationale.

## Lab 3 — Compare two risks
Compare:
- Risk A: low likelihood, severe impact (2 × 5).
- Risk B: likely occurrence, moderate impact (4 × 3).

Tasks:
1. Calculate both scores.
2. Explain why equal or similar scores do not necessarily mean equal urgency.
3. Consider mandatory controls, affected population, exploit evidence, and reversibility.
4. Recommend an order for treatment and justify it.

## Lab 4 — Inherent versus residual risk
Scenario: A public API lacks effective rate limiting. The team implements gateway limits, per-account quotas, timeouts, and alerting.

Tasks:
- Record the initial rating.
- Identify controls and how each reduces likelihood or impact.
- Define test evidence needed to verify controls.
- Estimate residual likelihood and impact separately.
- Explain remaining uncertainty.

## Lab 5 — Choose a treatment
For each fictional case, choose mitigate, avoid, transfer/share, or accept:
1. A critical feature creates unacceptable exposure and can be redesigned.
2. A known issue can be fixed with a validated code change.
3. A low-impact risk is explicitly accepted by an authorized owner for a short period.
4. Financial losses from some residual risk may be insured, but security controls are still needed.

Explain why the selected treatment is suitable and name an accountable owner.

## Lab 6 — Build a risk register
Use `risk-assessment-template.csv`.

Tasks:
- Add at least five distinct risk scenarios.
- Include at least one confidentiality, integrity, availability, and privilege/access-control scenario.
- Record existing controls, evidence, likelihood, impact, treatment, owner, due date, and status.
- Mark estimates and assumptions clearly.
- Do not rate every issue as “High” without justification.

## Lab 7 — Risk acceptance review
Create a one-page decision record for a hypothetical medium risk with a remediation date 30 days away.

Include:
- Scope and scenario
- Business rationale
- Compensating controls
- Risk owner and approving authority
- Expiry date
- Monitoring plan
- Conditions that revoke acceptance

## Lab 8 — Reassessment after a change
A service moves from private network access to a public endpoint, and a new integration is added.

Tasks:
- Identify which assumptions are no longer valid.
- Reassess likelihood and impact.
- Review new threat paths and dependencies.
- Update treatment actions and due dates.
- Record the reason and date for the rating change.

## Lab 9 — Peer review
Review another learner's register using `risk-review-checklist.md`.

Look for:
- Vague risk statements
- Ratings with no rationale
- Planned controls counted as existing controls
- Missing owner or due date
- No residual risk or verification evidence
- Acceptance without an authorized approver or expiry

## Submission checklist
- [ ] Each risk has a unique ID.
- [ ] Scenarios connect a threat event, weakness, asset, and impact.
- [ ] Ratings follow a stated scale and include rationale.
- [ ] Treatment actions are measurable and owned.
- [ ] Residual ratings are evidence-based.
- [ ] Exceptions have an authorized approver and review/expiry date.
