# Practical Labs: CVSS and Risk Rating

Use authorized lab systems, sample records, or public advisories. Do not exploit production assets as part of these exercises.

## Lab 1 — Read a CVSS vector

1. Open the official FIRST CVSS v4.0 specification and calculator.
2. Review the illustrative vector in `examples.md`.
3. Identify each Base metric and explain its meaning.
4. Use the calculator to obtain the actual score for the vector.
5. Record the score, severity, and exact vector together.

**Deliverable:** A short vector interpretation table.

## Lab 2 — Compare CVSS and business risk

Create two hypothetical deployments of the same vulnerability:
- A public-facing production service holding sensitive information.
- An isolated test service with no sensitive data.

For each, document reachability, asset criticality, exploit evidence, likely impact, controls, and remediation priority. Explain why CVSS Base alone may not express the full difference in local risk.

**Deliverable:** A two-environment comparison.

## Lab 3 — Score likelihood and impact

Use the training model in `README.md`. Rate each factor from 1 to 5 and multiply Likelihood × Impact.

Scenario A: An internet-facing service has a public exploit and supports a critical business process.

Scenario B: A medium-severity issue affects an internal development VM with no sensitive data and restricted access.

Scenario C: A vulnerability has no known exploit, but affects a critical system that is reachable from several internal networks.

Explain your assumptions. If evidence is unknown, mark it as unknown and state how you would verify it.

## Lab 4 — Triage a mini backlog

Use these fictional findings:

| ID | Finding | Context |
|---|---|---|
| V-101 | Remote code execution | Internet-facing server; exploitation reported; critical service |
| V-102 | Weak TLS configuration | Public web server; no sensitive admin interface; supported remediation available |
| V-103 | Local privilege escalation | Developer workstation; user access required; endpoint controls enabled |
| V-104 | SQL injection | Internal application; contains customer records; reachable by many employees |
| V-105 | Unsupported library | Test-only service; not externally reachable; replacement planned |

Rank the findings for initial triage. Your ranking must explain the effect of exposure, exploit evidence, asset importance, and impact. Do not invent CVSS scores where none are provided.

**Deliverable:** A prioritized table with evidence, owner, action, and review date.

## Lab 5 — Use the risk register

1. Open `risk-register-template.csv` in a spreadsheet editor.
2. Add three fictional findings from your lab.
3. Populate CVSS version, score, severity, and vector only when you have verified them.
4. Fill in likelihood, impact, risk score, rationale, owner, and target date.
5. Use `Unknown` where evidence is missing; do not silently assume a favorable value.
6. Record the source of each published score.

## Lab 6 — Risk exception review

A product team asks to defer a Critical finding for 90 days because a release is approaching.

Write an exception review containing:
- Business justification and accountable risk owner.
- Exploitability, exposure, asset criticality, and impact evidence.
- Temporary mitigations and how their effectiveness will be validated.
- Expiration date, monitoring, rollback/containment triggers, and remediation plan.
- Required approval under the organization's policy.

A delivery deadline by itself is not a security control.

## Lab 7 — Reassessment after remediation

Choose a fictional finding and describe how you would validate the fix. Include retesting, version/configuration evidence, exposure checks, regression testing, and updating the register. Explain why a closed ticket is not enough to prove remediation.

## Completion checklist

- [ ] I can explain CVSS Base vs. Threat vs. Environmental metrics.
- [ ] I can identify the CVSS v4.0 severity bands.
- [ ] I can read the major fields in a CVSS v4.0 vector.
- [ ] I can distinguish a CVSS score from a local business-risk rating.
- [ ] I can prioritize using evidence, exposure, exploit activity, and business impact.
- [ ] I can document assumptions, uncertainty, owner, due date, and exception approvals.
