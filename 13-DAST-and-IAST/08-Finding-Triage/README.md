# Finding Triage

## Learning objectives

By completing this module, you will be able to:

- Explain the purpose of security finding triage in a DevSecOps program.
- Normalize findings from SAST, DAST, IAST, SCA, container, IaC, API, and manual testing.
- Distinguish true positives, false positives, duplicates, accepted risks, and findings requiring investigation.
- Validate findings using evidence, reachability, exploitability, and application context.
- Prioritize issues using severity, likelihood, impact, exposure, and asset criticality.
- Assign owners, remediation targets, and exception expiry dates.
- Track remediation and verify fixes through retesting.
- Integrate triage into CI/CD and vulnerability management workflows.

## 1. What is finding triage?

Finding triage is the structured process of reviewing security tool output to determine what is real, what matters, who should act, and what happens next. Scanners produce alerts, not final risk decisions. A good triage process prevents teams from wasting time on duplicates and false positives while ensuring real vulnerabilities are not ignored.

Triage is a continuous workflow:

1. Collect findings from approved security testing sources.
2. Normalize fields and preserve original evidence.
3. Deduplicate related alerts.
4. Validate whether the issue exists and is reachable.
5. Assess technical and business risk.
6. Decide the disposition.
7. Assign an owner and due date.
8. Remediate or formally accept risk.
9. Retest and close only after verification.
10. Report trends and improve detection quality.

## 2. Sources of findings

| Source | Example output |
|---|---|
| SAST | Hardcoded secrets, injection patterns, insecure APIs |
| DAST | Missing headers, injection indicators, exposed endpoints |
| IAST | Runtime source-to-sink flows |
| SCA | Vulnerable direct or transitive dependencies |
| Container scanning | OS/package vulnerabilities in images |
| IaC scanning | Public storage, broad IAM permissions |
| API testing | BOLA, BFLA, excessive data exposure |
| Penetration testing | Validated exploit paths and business logic flaws |
| Cloud posture tools | Misconfigurations and exposed resources |
| Manual review | Design and authorization weaknesses |

Each source may use different identifiers, severity scales, confidence levels, and evidence formats. Preserve the source-specific fields while mapping common fields into a normalized record.

## 3. Standard finding lifecycle

A recommended lifecycle:

```text
New
 |
 v
Needs Triage
 |
 +--> Confirmed --> Prioritized --> Assigned --> In Progress
 |                                  |              |
 |                                  |              v
 |                                  |          Remediated
 |                                  |              |
 |                                  |              v
 |                                  +----------> Retest
 |                                                 |
 |                                      +----------+---------+
 |                                      |                    |
 |                                    Passed                Failed
 |                                      |                    |
 |                                      v                    v
 |                                    Closed              Reopened
 |
 +--> False Positive --> Documented / Suppressed
 |
 +--> Duplicate -------> Linked to Canonical Finding
 |
 +--> Accepted Risk --> Approved, Time-Bounded Exception
 |
 +--> Needs Investigation --> Evidence Collection
```

Use statuses that are understandable to developers, security teams, auditors, and service owners. “Accepted risk” is not the same as “false positive”; the former is a real or potential issue whose residual risk has been formally accepted.

## 4. Finding validation

Before classifying an alert, answer:

- Does the affected asset, repository, endpoint, or package exist?
- Is the scanner result tied to the correct branch, commit, build, and environment?
- Can the issue be reproduced?
- Is the vulnerable code or endpoint reachable?
- Is the source attacker-controlled?
- Does the suspected sink or unsafe operation actually occur?
- Are effective mitigations present?
- Does the finding expose sensitive data or enable unauthorized action?
- Is the issue already tracked under another finding?

Use evidence rather than intuition. A low-confidence alert should be investigated, not automatically dismissed. A high-severity label should not be accepted without checking its context.

## 5. Disposition categories

### Confirmed true positive

The vulnerability exists and is supported by sufficient evidence. Record impact, affected component, reproduction steps, and remediation.

### False positive

The alert does not represent a vulnerability in the stated context. Record the technical reason, evidence, reviewer, date, and scope of the decision. Avoid blanket suppression of a rule if only one instance is invalid.

### Duplicate

The same root cause or remediation is already tracked. Link the duplicate to the canonical issue and retain affected locations/assets.

### Accepted risk

The issue is real or reasonably possible, but an authorized risk owner formally accepts the residual risk for a defined period. Record compensating controls, rationale, approver, expiry, and review date.

### Needs investigation

Evidence is insufficient to make a reliable decision. This must be a temporary status with an owner, next action, and target review date.

### Not applicable / out of scope

The asset or behavior is not in the approved scope or is not relevant to the product. Record why; do not use this as a shortcut for avoiding remediation.

## 6. Severity, risk, and priority

These terms are related but different:

- **Severity:** technical seriousness of the vulnerability under a scoring model or tool scale.
- **Likelihood:** probability that the weakness can be exploited in the actual environment.
- **Impact:** expected harm if exploited.
- **Risk:** combination of likelihood and impact in organizational context.
- **Priority:** order and urgency for action, considering risk, exposure, deadlines, and dependencies.

CVSS is useful for communicating technical severity, but it should not be the only prioritization signal. Consider:
- Internet exposure and reachable attack paths.
- Authentication requirements and privilege needed.
- Exploit availability and evidence of active exploitation.
- Sensitive data and business function affected.
- Asset criticality and blast radius.
- Existing mitigations and compensating controls.
- Whether the vulnerable code path is used at runtime.

For CVEs, enrichment may include EPSS and CISA KEV status. Do not apply CVE-specific signals to unrelated application findings such as business-logic flaws.

## 7. Example risk prioritization model

The following is a training model, not a universal standard. Adapt it to your organization's risk appetite.

| Factor | Example values |
|---|---|
| Technical severity | Critical / High / Medium / Low |
| Exposure | Internet-facing / Internal / Isolated |
| Reachability | Confirmed / Possible / Not observed |
| Exploit evidence | Active exploitation / Public PoC / None known |
| Asset criticality | Tier 1 / Tier 2 / Tier 3 |
| Data sensitivity | Regulated / Confidential / Public |
| Mitigations | None / Partial / Strong |

A practical decision rule:
1. Prioritize known exploited vulnerabilities and confirmed active attacks.
2. Elevate reachable vulnerabilities on internet-facing critical assets.
3. Consider data sensitivity and business impact.
4. Lower urgency only when evidence supports reduced exposure or effective mitigation.
5. Record why a lower priority is justified.

Do not invent a numeric risk score unless its calculation and calibration are documented.

## 8. CVSS, EPSS, and CISA KEV

- **CVSS** describes the technical characteristics and severity of a vulnerability. Record the version and vector where available.
- **EPSS** estimates the probability that a published CVE will be exploited in the wild over the next 30 days. It is a prioritization signal, not proof of exploitation.
- **CISA KEV** identifies vulnerabilities known to have been exploited in the wild. KEV inclusion is a strong urgency signal.
- **Reachability** determines whether affected code or a vulnerable component is actually accessible in the application's context.
- **Asset context** captures internet exposure, business criticality, and sensitive data.

Always record the source and date of enrichment. Scores and catalogs change.

## 9. Deduplication and normalization

Multiple tools may report the same root cause. Deduplicate carefully:

- Compare rule/CWE/CVE identifiers.
- Compare file, line, method, endpoint, package, and affected version.
- Compare root cause and required remediation.
- Preserve all tool references and evidence.
- Use a canonical finding ID with linked instances.
- Avoid merging distinct vulnerabilities just because they share a category.

Normalization should standardize severity, status, timestamps, repository/asset identity, ownership, and remediation fields without discarding the original scanner data.

## 10. False-positive management

A good false-positive record contains:
- Original tool and rule.
- Affected location or asset.
- Reason the alert is incorrect.
- Evidence supporting the decision.
- Scope of suppression (instance, path, rule, or asset).
- Reviewer and approval where required.
- Date and review/expiry date.

Prefer narrow, reviewable suppressions. Revisit them when code, framework, threat model, or scanner rules change. Do not suppress a true positive because remediation is inconvenient.

## 11. Ownership and remediation SLAs

Every confirmed finding should have:
- A named engineering owner or accountable team.
- A security contact where needed.
- A target remediation date.
- A ticket or tracking reference.
- An agreed mitigation if a full fix is delayed.
- Escalation for overdue high-risk findings.

Example training SLAs (adjust to policy):

| Priority | Example target |
|---|---|
| Critical | Immediate containment; fix target within 7 days |
| High | 14 days |
| Medium | 30–60 days |
| Low | 90 days or planned maintenance |
| Informational | Track or address as appropriate |

These are illustrative targets, not mandated timelines. Regulatory, contractual, or organizational requirements may be stricter.

## 12. Risk acceptance

Risk acceptance should be formal, time-bounded, and approved by an authorized risk owner. Record:
- Finding and affected asset.
- Residual risk and business rationale.
- Compensating controls.
- Why remediation is delayed or not planned.
- Approver and approval date.
- Expiry and review date.
- Conditions that trigger earlier reassessment.

Do not allow indefinite exceptions without review. Security teams should not accept business risk on behalf of the accountable owner.

## 13. Remediation verification

A finding is not closed merely because a developer says it is fixed or a ticket is complete.

Verification should:
1. Identify the exact fixed commit/build/version.
2. Repeat the original reproduction steps.
3. Run the relevant scanner or test again.
4. Confirm the vulnerable behavior is no longer present.
5. Check for regressions or alternate paths.
6. Attach retest evidence.
7. Close or reopen based on the result.

## 14. CI/CD integration

A mature pipeline can:
- Ingest scanner output such as SARIF, JSON, or XML.
- Normalize and deduplicate findings.
- Apply a policy to new or changed findings.
- Fail builds for defined blocking conditions.
- Create tickets for accepted non-blocking findings.
- Preserve reports and test metadata.
- Avoid treating scanner failure as a clean result.

Prefer gating on actionable new findings and clear policy conditions rather than blindly failing every build on every legacy alert.

## 15. Metrics and reporting

Useful metrics include:
- New findings by severity and source.
- Confirmed true-positive rate.
- False-positive rate and suppression age.
- Mean time to triage and remediate.
- SLA compliance and overdue backlog.
- Reopened findings after failed retest.
- Accepted-risk count and expiry status.
- Duplicate rate and tool noise.
- Findings by application, team, and asset criticality.

Metrics should encourage remediation and quality, not reward teams for hiding or suppressing findings.

## 16. Knowledge check

1. What is the difference between severity and risk?
2. Why should scanner output be manually validated?
3. How is accepted risk different from a false positive?
4. Why is “needs investigation” a temporary state?
5. What signals can supplement CVSS?
6. How should duplicate findings be handled?
7. What evidence belongs in a false-positive record?
8. Who should approve risk acceptance?
9. What is required before closing a remediated finding?
10. Why should CI distinguish scanner failure from zero findings?

## References

- [OWASP DevSecOps Guideline — Vulnerability Management](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-7-Operate/2-7-4-Vulnerability-Management/)
- [NCSC — Carry out assessments by triaging and prioritising](https://www.ncsc.gov.uk/collection/vulnerability-management/guidance/carry-out-assessments)
- [OWASP DSOMM — Simple false positive treatment](https://dsomm.owasp.org/activity-description?activityName=Simple+false+positive+treatment&dimension=Test+and+Verification&level=1&subDimension=Consolidation)
- [FIRST — CVSS](https://www.first.org/cvss/)
- [FIRST — EPSS](https://www.first.org/epss/)
- [CISA — Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [OWASP Web Security Testing Guide — Reporting](https://owasp.org/www-project-web-security-testing-guide/)
