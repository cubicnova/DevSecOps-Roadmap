# Risk Assessment for Secure SDLC and Threat Modeling

## Overview
Risk assessment helps a team understand which security risks matter most, why they matter, and what action is justified. It connects a threat scenario or vulnerability to its likelihood, impact, existing controls, and treatment decision.

Risk scores are decision aids, not precise predictions. Use a consistent method, document assumptions, and involve the people accountable for business impact and risk acceptance.

## Learning objectives
- Distinguish an asset, threat, vulnerability, risk, control, and residual risk.
- Identify and describe security risk scenarios.
- Estimate likelihood and impact using a documented scale.
- Calculate and interpret a qualitative risk rating.
- Select and track risk treatment actions.
- Explain inherent versus residual risk and risk acceptance.
- Maintain a useful risk register.

## Key terms
| Term | Meaning | Example |
|---|---|---|
| Asset | Something valuable that needs protection | Customer records |
| Threat | A potential cause of harm | Attacker abuses an exposed endpoint |
| Vulnerability | A weakness that can be exploited | Missing object-level authorization |
| Risk scenario | How a threat could exploit a weakness and cause harm | A user accesses another customer's invoice |
| Likelihood | Estimated chance the scenario will occur within the defined context/timeframe | Possible |
| Impact | Consequence if the scenario occurs | Major privacy and financial impact |
| Control | A measure that reduces likelihood or impact | Server-side authorization checks |
| Inherent risk | Risk before considering relevant controls | High |
| Residual risk | Risk remaining after controls are applied | Medium |
| Risk owner | Person accountable for the risk decision and treatment | Product or service owner |

## A practical risk assessment workflow
1. **Set scope and context.** Identify the system, business process, assessment date, assumptions, and risk criteria.
2. **Identify assets and objectives.** Consider confidentiality, integrity, availability, privacy, safety, compliance, and business continuity.
3. **Describe risk scenarios.** State the threat actor/event, weakness or predisposing condition, affected asset, and potential consequence.
4. **Identify existing controls.** Record controls that are implemented and verified—not only planned.
5. **Estimate likelihood.** Consider exposure, attacker capability and motivation, exploitability, existing controls, and available evidence.
6. **Estimate impact.** Consider data sensitivity, scale, operational disruption, financial loss, privacy, legal/regulatory obligations, and reputation.
7. **Determine risk level.** Apply the agreed matrix consistently.
8. **Choose a treatment.** Mitigate, avoid, transfer/share, or accept within delegated authority.
9. **Assign ownership and deadlines.** Actions need a named owner, due date, and verification criteria.
10. **Reassess residual risk.** Rate the risk after implemented controls are tested.
11. **Review and monitor.** Reassess after significant architecture changes, new vulnerabilities, incidents, or changes in business context.

## Example 5 × 5 scoring method
Use this illustrative matrix only if it fits your organization's policy. Define the scale before rating real risks.

### Likelihood
1. Rare — exceptional circumstances
2. Unlikely — not expected, but possible
3. Possible — could occur
4. Likely — expected in many circumstances
5. Almost certain — expected frequently

### Impact
1. Insignificant — negligible disruption or loss
2. Minor — limited, recoverable effect
3. Moderate — meaningful service, data, or business impact
4. Major — substantial disruption, sensitive-data exposure, or material loss
5. Severe — critical business interruption, extensive exposure, or major harm

**Risk score = Likelihood × Impact** (range 1–25).

| Score | Example level | Typical response |
|---:|---|---|
| 1–4 | Low | Track or handle through routine controls |
| 5–9 | Medium | Plan treatment and monitor |
| 10–16 | High | Prioritized treatment and explicit owner review |
| 17–25 | Critical | Prompt escalation and urgent risk decision |

These bands are illustrative and are not universal. Use the organization's approved risk matrix if one exists. A low numeric score must not override legal obligations, safety concerns, or mandatory controls.

## Risk treatment choices
- **Mitigate:** implement or improve controls.
- **Avoid:** stop or redesign the activity that creates the risk.
- **Transfer/share:** allocate some financial or operational consequences contractually or through insurance; accountability is not automatically eliminated.
- **Accept:** explicitly retain the risk with informed approval by the authorized risk owner.

## Risk register minimum fields
Risk ID, system/asset, scenario, threat, weakness, existing controls, likelihood, impact, score, rating, treatment, action owner, due date, evidence, residual likelihood/impact/rating, risk owner, acceptance decision, review date, and status.

## Good assessment habits
- Use evidence and explain uncertainty; avoid false precision.
- Rate a clearly described scenario, not a vague label like “security issue.”
- Separate vulnerability severity from business risk.
- Do not count planned controls as implemented controls.
- Keep treatment actions measurable and testable.
- Record who accepted residual risk, why, and when it expires or is reviewed.
- Revisit ratings when conditions change.

## Suggested learning path
1. Read `examples.md`.
2. Complete the exercises in `practical.md`.
3. Compare your reasoning with `solutions.md`.
4. Use `risk-assessment-template.csv` for practice.
5. Run the `risk-review-checklist.md` before a review meeting.

## References
- NIST SP 800-30 Rev. 1, Guide for Conducting Risk Assessments: https://csrc.nist.gov/pubs/sp/800/30/r1/final
- OWASP Risk Rating Methodology: https://owasp.org/www-community/OWASP_Risk_Rating_Methodology
- OWASP Threat Model Library: https://owasp.org/projects/threat-model-library/
