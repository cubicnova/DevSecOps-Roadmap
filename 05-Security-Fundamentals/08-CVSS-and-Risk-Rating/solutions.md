# Solutions and Reference Answers

These are example answers. Risk ratings depend on verified evidence and the organization's approved methodology.

## Lab 1 — Vector interpretation

For the illustrative vector:

```text
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H
```

- `AV:N`: network attack vector.
- `AC:L`: low attack complexity.
- `AT:N`: no attack requirements.
- `PR:N`: no privileges required.
- `UI:N`: no user interaction.
- `VC/VI/VA:H`: high confidentiality, integrity, and availability impacts on the vulnerable system.
- `SC/SI/SA:H`: high impacts on subsequent systems.

Use the official FIRST calculator to confirm the score. Always retain the exact vector and CVSS version.

## Lab 2 — CVSS vs. business risk

The Base score communicates intrinsic technical severity. Exposure, criticality, controls, threat intelligence, and business consequences can alter local urgency. If enough evidence exists, evaluate CVSS Threat and Environmental metrics. Keep the organizational risk rating as a separate, documented assessment.

## Lab 3 — Illustrative training-model answers

Using Likelihood × Impact, each rated 1–5:

| Scenario | Likelihood | Impact | Product | Training label |
|---|---:|---:|---:|---|
| A | 5 | 5 | 25 | Critical |
| B | 1 | 2 | 2 | Low |
| C | 3 | 5 | 15 | High |

These values are illustrative only. Scenario C's likelihood might increase if reachable paths or exploit evidence are found. The score should be updated when assumptions change.

## Lab 4 — Example triage reasoning

A plausible initial triage order is V-101, V-104, V-102, V-103, V-105, subject to validation.

- **V-101:** Highest urgency because exploitation is reported, exposure is public, and the service is critical. Validate affected versions, follow incident procedures, and consider immediate mitigation.
- **V-104:** Customer records and broad internal reachability can create major impact. Validate exploitability and access boundaries promptly.
- **V-102:** Public exposure and an available fix support planned remediation; urgency depends on the actual configuration and threat context.
- **V-103:** Local access requirement and existing controls may reduce likelihood, but privilege escalation on developer endpoints can still matter.
- **V-105:** Test-only and isolated context may reduce immediate risk, but verify the isolation and ensure the upgrade plan is completed.

Do not assign invented CVSS scores. If a published CVSS score is required, locate the advisory/CVE record and preserve its source and vector.

## Lab 5 — Risk register

Recommended practices:
- Separate CVSS score/severity from local likelihood, impact, and risk rating.
- Include the score source, version, and vector.
- Record `Unknown` for missing evidence.
- Use the same scoring criteria consistently across findings.
- Assign an accountable owner and a policy-aligned target date.

## Lab 6 — Exception review

A complete exception has a named accountable risk owner, documented evidence, explicit expiry, temporary mitigations, monitoring, containment triggers, and a funded remediation plan. Approval must follow organizational policy. Revisit the exception if exploit evidence, exposure, or impact changes.

## Lab 7 — Reassessment

Confirm the fix in the affected version/configuration, repeat the relevant security test, check adjacent versions and regression paths, and verify that exposure is reduced as intended. Update the register with evidence and closure date. If a mitigation is temporary rather than a full fix, keep the finding open or clearly mark it as mitigated according to policy.

## Common mistakes

- Reporting a CVSS Base score as the entire business risk.
- Mixing CVSS versions or using a vector that does not match the score.
- Guessing missing scores or claiming the calculator was used when it was not.
- Prioritizing only by numeric score and ignoring active exploitation or critical assets.
- Lowering risk based on unverified controls.
- Closing findings without evidence of retesting.
- Allowing risk exceptions to remain open indefinitely without an owner and expiry.
