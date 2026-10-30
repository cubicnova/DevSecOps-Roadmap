# False Positive Triage

## Learning objectives

By the end of this module, learners should be able to:

- Explain false positives, false negatives, precision, and recall.
- Triage SAST and CodeQL alerts using source context and data-flow paths.
- Distinguish a true positive, false positive, accepted risk, and inconclusive result.
- Validate sanitizers, validators, authorization checks, and framework behavior.
- Document evidence and dismiss alerts with an auditable reason.
- Improve noisy rules without creating blind spots.

## 1. What is false-positive triage?

A false positive is a reported finding that does not represent the issue described by the rule in the context of the analyzed application. Triage is the structured process of reviewing a finding, collecting evidence, determining its validity and impact, and deciding the next action.

A false positive is not the same as an accepted risk. An accepted risk is a real issue for which an authorized owner has approved a documented exception. A false negative is a real issue that the scanner failed to report.

## 2. Key terms

| Term | Meaning |
|---|---|
| True positive | The finding correctly identifies a real issue |
| False positive | The finding does not represent the reported issue |
| False negative | A real issue was not detected |
| Precision | True positives / (true positives + false positives) |
| Recall | True positives / (true positives + false negatives) |
| Accepted risk | Real issue with a documented, approved exception |
| Inconclusive | Evidence is insufficient to make a reliable decision |

Precision and recall are measured against a defined evaluation set. Do not claim a scanner has perfect recall based only on the alerts it produced.

## 3. Triage workflow

1. **Read the alert:** Understand the rule, severity, confidence/precision, and remediation guidance.
2. **Confirm the location:** Open the exact code and surrounding call sites.
3. **Trace the data:** Identify source, transformations, validation/sanitization, and sink.
4. **Check reachability:** Determine whether the relevant code path can execute and whether input is attacker-controlled.
5. **Validate controls:** Confirm that protections are effective for the specific sink and context.
6. **Assess impact:** Consider exposure, privileges, data sensitivity, and exploitability.
7. **Classify:** True positive, false positive, accepted risk, duplicate, or inconclusive.
8. **Record evidence:** Document the reasoning and relevant code/test references.
9. **Take action:** Fix, improve the rule/model, dismiss with a supported reason, or escalate.
10. **Verify:** Rerun analysis and ensure the disposition remains correct.

## 4. Understanding source-to-sink paths

For data-flow findings, identify:

- **Source:** Where potentially untrusted or sensitive data enters the program.
- **Propagation:** Assignments, function calls, transformations, and wrappers.
- **Sanitizer/validator:** A control that changes or constrains the data.
- **Sink:** A security-sensitive operation such as SQL execution, shell execution, or HTML output.

A sanitizer is context-specific. HTML escaping does not make a value safe for SQL; SQL parameterization does not validate a filesystem path. Confirm the control's semantics and that it is applied on every relevant path.

## 5. Common causes of false positives

- The analyzer does not recognize a custom sanitizer or validation helper.
- A framework or wrapper provides protection not modeled by the query.
- The alert occurs in test code, generated code, or unreachable code.
- The rule matches a function name without resolving the actual call target.
- The source is trusted in the specific context, but the rule assumes it is attacker-controlled.
- The sink is used with a safe API or parameterized operation.
- The finding is duplicated by overlapping rules or analysis configurations.

## 6. Common causes of false negatives

- An unmodeled source, sink, sanitizer, or framework.
- Indirect calls, reflection, dynamic dispatch, or custom wrappers.
- Incomplete build or database extraction.
- Unsupported language/framework behavior.
- A rule that is too narrowly scoped or has broad exclusions.
- Incorrect assumptions about input validation or trust boundaries.

Triage must consider false negatives as well as false positives. Do not reduce alert counts by broadly suppressing paths or lowering coverage.

## 7. Classification decision

| Classification | Meaning | Typical action |
|---|---|---|
| True positive | Rule accurately identifies a real issue | Fix and verify |
| False positive | Rule does not apply to this code | Dismiss with evidence; improve rule/model if useful |
| Accepted risk | Real issue, formally accepted | Document approval, controls, and expiry |
| Duplicate | Same underlying issue already tracked | Link canonical issue and follow policy |
| Inconclusive | Not enough evidence | Escalate or request further analysis |

Do not classify an issue as a false positive merely because it is difficult to fix or the business accepts the risk.

## 8. GitHub code scanning alert review

For a GitHub code scanning alert:

1. Open the repository's Security and quality / Code scanning area.
2. Open the alert and review the description, location, rule ID, and related metadata.
3. For data-flow alerts, inspect the source-to-sink path and any sanitizer steps.
4. Review affected branches and the commit that introduced the alert.
5. If the issue is real, fix it and verify with a new scan.
6. If it is not applicable, choose the most accurate dismissal reason and add a clear comment where appropriate.

Dismissal choices and available UI may vary by platform version and permissions. A dismissal closes an alert; it does not prove the code is secure.

## 9. Evidence-based dismissal

A good dismissal record includes:

- Alert ID and rule ID.
- File, line, and affected branch.
- Classification and reason.
- Code path and relevant source/sink analysis.
- Sanitizer or control and why it is effective.
- Supporting tests, documentation, or code references.
- Reviewer and date.
- Follow-up action, if the rule needs improvement.

Avoid comments such as "not exploitable" or "false positive" without supporting evidence.

## 10. Improving noisy rules

If a query repeatedly reports safe code:

1. Reproduce the behavior with a minimal positive and negative example.
2. Determine whether the query's source, sink, or sanitizer model is incomplete.
3. Prefer semantic API matching over brittle string matching.
4. Add or correct framework and custom-library models.
5. Add regression tests for both the false positive and true positive.
6. Test against representative repositories.
7. Review query precision and performance before rollout.

For CodeQL, custom models and query changes should follow the supported modeling and testing workflow for the language pack. Do not modify a query merely to hide a finding without understanding the security semantics.

## 11. Metrics and quality controls

Track:

- Alert volume by rule, repository, and severity.
- True-positive and false-positive counts from reviewed findings.
- Precision on a defined, labeled evaluation set.
- Time to triage and time to remediate.
- Reopened alerts and repeated false positives.
- Inconclusive findings and escalation outcomes.
- Suppression/dismissal rate and age of exceptions.
- Rule execution time and scan coverage.

A low dismissal count is not automatically a sign of high quality; teams may be ignoring alerts or classifying them inconsistently.

## 12. Best practices

- Use a documented triage rubric.
- Require evidence for dismissals.
- Separate false positives from accepted risks.
- Apply least privilege to alert-management permissions.
- Review high-impact findings promptly.
- Keep exceptions narrow, owned, and time-bound.
- Add regression tests when query logic changes.
- Periodically sample dismissed alerts for quality review.
- Preserve audit history and avoid exposing sensitive source code in public tickets.

## References

- [Resolving code scanning alerts](https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts/resolve-alerts)
- [Triaging code scanning alerts in pull requests](https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts/triage-alerts-in-pull-requests)
- [CodeQL query metadata style guide](https://github.com/github/codeql/blob/main/docs/query-metadata-style-guide.md)
- [Supported CodeQL queries and libraries](https://github.com/github/codeql/blob/main/docs/supported-queries.md)
