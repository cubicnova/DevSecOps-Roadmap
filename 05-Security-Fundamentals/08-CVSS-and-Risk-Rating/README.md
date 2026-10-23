# CVSS and Risk Rating

Learn to assess vulnerability severity, use CVSS v4.0 consistently, and prioritize remediation using business context.

## Learning objectives

By the end of this module, you should be able to:

- Explain the difference between vulnerability severity, likelihood, impact, and business risk.
- Identify the CVSS v4.0 Base, Threat, Environmental, and Supplemental metric groups.
- Interpret CVSS severity bands and vector strings.
- Build a risk rating using asset criticality, exposure, exploit evidence, and business impact.
- Document assumptions, remediation priority, owners, and due dates.
- Avoid common scoring errors such as treating CVSS as the complete business-risk decision.

## Contents

- [`examples.md`](examples.md) — worked scenarios, sample vectors, and scoring examples.
- [`practical.md`](practical.md) — guided exercises and case studies.
- [`solutions.md`](solutions.md) — sample answers and rationale.
- [`risk-register-template.csv`](risk-register-template.csv) — reusable vulnerability/risk register.
- [`risk-rating-checklist.md`](risk-rating-checklist.md) — assessment and remediation checklist.

## Core concepts

### CVSS vs. risk rating

CVSS communicates the technical severity of a vulnerability using a standardized method. Organizational risk rating combines relevant technical evidence with local context, such as asset criticality, internet exposure, exploit activity, compensating controls, data sensitivity, and business consequences.

A high CVSS score is a strong signal, but it does not automatically determine the order of every remediation task. A medium-scored issue on an exposed identity provider or a critical production system may deserve faster action than a higher-scored issue on an isolated lab asset. Document why a priority differs from the raw score.

### CVSS v4.0 metric groups

- **Base:** intrinsic vulnerability characteristics and impacts.
- **Threat:** current threat conditions, including exploit maturity.
- **Environmental:** how the organization's environment changes the assessment.
- **Supplemental:** extra context; these metrics do not change the final CVSS score.

CVSS v4.0 scores range from 0.0 to 10.0. Qualitative bands are:

| Rating | Score |
|---|---:|
| None | 0.0 |
| Low | 0.1–3.9 |
| Medium | 4.0–6.9 |
| High | 7.0–8.9 |
| Critical | 9.0–10.0 |

Always state the CVSS version and score type when reporting results. A Base score is not the same as a Threat- or Environmental-adjusted score.

### A practical organizational risk model

Use the organization's approved methodology if one exists. For training, this module uses a simple qualitative model:

**Risk = Likelihood × Impact**

Rate each dimension from 1 (Low) to 5 (Very High), then multiply them:

| Score | Training label |
|---:|---|
| 1–4 | Low |
| 5–9 | Moderate |
| 10–16 | High |
| 17–25 | Critical |

This is a teaching model, not a universal standard. Organizations should define their own thresholds, escalation rules, and remediation SLAs. CVSS scores should not be mechanically converted to these numbers.

### Evidence to collect

- Vulnerability identifier and affected product/version.
- CVSS version, score, vector, and source.
- Reachability and exposure (internet-facing, internal, isolated).
- Exploit maturity and evidence of active exploitation.
- Asset/business criticality and data sensitivity.
- Existing controls and their tested effectiveness.
- Potential confidentiality, integrity, availability, safety, and regulatory impacts.
- Remediation owner, target date, mitigation, and exception approval.

## Recommended workflow

1. Validate the finding and identify the affected asset.
2. Record the published CVSS score and vector, where available.
3. Assess threat and environmental context using reliable evidence.
4. Rate likelihood and impact under the organization's risk method.
5. Set a priority and due date using policy, exposure, exploit evidence, and business criticality.
6. Record rationale and uncertainty; do not fabricate missing evidence.
7. Reassess after remediation, changes in exposure, or new exploit intelligence.

## Official references

- FIRST CVSS v4.0 specification: https://www.first.org/cvss/v4.0/specification-document
- FIRST CVSS v4.0 resources and calculator: https://www.first.org/cvss/v4-0
- NIST National Vulnerability Database: https://nvd.nist.gov/
- NIST SP 800-30, Guide for Conducting Risk Assessments: https://csrc.nist.gov/pubs/sp/800/30/r1/final
