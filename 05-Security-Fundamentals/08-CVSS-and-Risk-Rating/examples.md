# Examples: CVSS and Risk Rating

## Example 1 — Interpret a CVSS v4.0 score

Suppose a trusted vendor advisory reports **CVSS v4.0 Base Score: 9.2 (Critical)**.

Record:
- Version: CVSS v4.0
- Score type: Base
- Score: 9.2
- Severity: Critical
- Source: link to the vendor advisory or CVE record
- Vector: copy the exact vector supplied by the source

Do not infer the full vector from the score. Different metric combinations can produce the same or similar score. Use the FIRST calculator or the source's vector when you need to validate the calculation.

## Example 2 — Example vector anatomy

The following is an illustrative CVSS v4.0 Base vector format:

```text
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H
```

It describes a hypothetical issue with network attack vector, low attack complexity, no attack requirements, no privileges required, no user interaction, and high impacts to the vulnerable and subsequent systems. Use the official FIRST calculator to determine the score; do not rely on a hand-calculated estimate.

Metric abbreviations include:
- `AV`: Attack Vector
- `AC`: Attack Complexity
- `AT`: Attack Requirements
- `PR`: Privileges Required
- `UI`: User Interaction
- `VC`, `VI`, `VA`: Confidentiality, Integrity, Availability impact on the vulnerable system
- `SC`, `SI`, `SA`: impacts on subsequent systems

## Example 3 — Same vulnerability, different environments

A vulnerability in a network service is rated High by its published Base score.

**Environment A:** The service is internet-facing, handles sensitive customer data, and has evidence of exploitation. The affected asset supports a critical business process.

**Environment B:** The vulnerable component is not reachable from untrusted networks, is disabled by configuration, and is deployed only in a disposable test environment.

The technical vulnerability may be the same, but the urgency and business risk can differ. Validate the reachability and controls before reducing priority. Where appropriate, use CVSS Environmental metrics and document the separate organizational risk decision.

## Example 4 — Qualitative likelihood × impact

Training scenario: a vulnerable admin panel is reachable from the internet. A public exploit is available, and the panel manages a critical production system.

| Dimension | Rating | Rationale |
|---|---:|---|
| Likelihood | 5 — Very High | Internet exposure and public exploit evidence |
| Impact | 5 — Very High | Administrative compromise could disrupt a critical service |
| Result | 25/25 — Critical | Training model only |

This score is not a CVSS score. It is an example of a local risk model. Keep the two values in separate fields.

## Example 5 — A lower CVSS issue that still needs urgent work

A vulnerability has a Medium CVSS score, but it affects a publicly exposed authentication service. Threat intelligence confirms targeted exploitation and the system is a dependency for many applications.

A defensible risk decision may prioritize this above a higher-CVSS issue on an isolated, non-production asset. Record the supporting evidence, approver, and reason for the override.

## Example 6 — Sample prioritization table

| Finding | CVSS severity | Context | Suggested action |
|---|---|---|---|
| Internet-facing remote code execution with exploitation evidence | Critical/High depending on verified score | Broad exposure and severe impact | Emergency triage and rapid mitigation |
| Vulnerability in a critical identity platform | Any verified rating | High business dependency | Prioritize based on exposure and impact |
| Medium issue on isolated lab system | Medium | No sensitive data, limited reachability | Schedule according to policy |
| Unsupported software on an internet-facing server | May have multiple findings | Unknown future vulnerability exposure | Plan upgrade and reduce exposure |

These are decision examples, not universal SLAs. Follow your organization's incident and vulnerability management policies.

## Example 7 — Avoid misleading reporting

Prefer:

> CVSS v4.0 Base 7.4 (High), vendor-provided. Organizational risk: Critical due to confirmed exploitation, internet exposure, and impact to a critical payment service. Immediate mitigation owner: Platform Security.

Avoid:

> Risk is 7.4 out of 10.

The latter incorrectly treats a CVSS score as a complete business-risk assessment.
