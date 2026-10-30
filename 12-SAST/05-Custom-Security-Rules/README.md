# Custom Security Rules

## Learning objectives

By the end of this module, learners should be able to:

- Explain when an organization needs custom security rules.
- Translate a secure-coding requirement into a precise detection rule.
- Design rules with clear scope, severity, confidence, and remediation guidance.
- Write and organize basic CodeQL queries and custom rule patterns.
- Test rules against positive, negative, and edge-case examples.
- Integrate rules into CI and manage exceptions safely.

## 1. What are custom security rules?

Custom security rules detect security weaknesses or policy violations that are specific to an application, framework, architecture, or organization. They supplement built-in SAST rules rather than replace them.

Examples include:

- Preventing use of an internally prohibited cryptographic algorithm.
- Detecting direct access to a sensitive database wrapper instead of an approved safe wrapper.
- Enforcing a project-specific authorization check before a sensitive operation.
- Finding use of insecure internal HTTP clients.
- Detecting unsafe logging of selected sensitive fields.

A useful rule must describe a meaningful risk, identify the relevant code pattern, and provide actionable remediation.

## 2. Rule engineering lifecycle

1. **Define the policy:** State the required secure behavior in one sentence.
2. **Model the risk:** Identify threat, attacker control, impact, and trust boundary.
3. **Choose the enforcement layer:** SAST query, linter, secret scanner, dependency policy, IaC policy, or CI check.
4. **Define scope:** Languages, frameworks, repositories, directories, and exclusions.
5. **Implement detection:** Use syntax-aware or semantic analysis where possible.
6. **Test:** Include positive, negative, boundary, and regression cases.
7. **Tune:** Reduce false positives without hiding real vulnerabilities.
8. **Deploy:** Run in report-only mode before enforcing a blocking gate.
9. **Maintain:** Assign ownership, version rules, review exceptions, and measure effectiveness.

## 3. Rule specification

Before implementation, document:

| Field | Description |
|---|---|
| Rule ID | Stable unique identifier |
| Title | Short human-readable name |
| Objective | Secure behavior the rule enforces |
| Risk | Threat and possible impact |
| Scope | Languages, frameworks, repositories |
| Detection | Exact pattern or source-to-sink condition |
| Severity | Impact-based priority |
| Confidence | Expected true-positive rate |
| False positives | Known benign patterns |
| Remediation | Specific safe alternative |
| Tests | Positive, negative, and edge cases |
| Owner | Team responsible for maintenance |
| Exception | Approval, rationale, expiry, and scope |

Do not use severity as a substitute for confidence. A high-impact issue can still have uncertain detection.

## 4. Select the right enforcement layer

| Requirement | Suitable mechanism |
|---|---|
| Unsafe data flow in application code | CodeQL or semantic SAST |
| Simple prohibited syntax/API usage | Linter or AST rule |
| Credential accidentally committed | Secret scanning |
| Vulnerable third-party package | SCA/dependency scanning |
| Cloud/IaC misconfiguration | IaC policy scanner |
| Deployment approval or branch policy | CI/CD platform controls |
| Runtime abuse or exploit behavior | DAST, runtime monitoring, or detection engineering |

Use CodeQL when relationships across program elements or data flow matter. For simple formatting or local patterns, a lightweight linter may be easier to maintain.

## 5. Custom CodeQL rule anatomy

A CodeQL query is saved in a `.ql` file. Queries used with `database analyze` need valid metadata, including `@id` and `@kind`. Alert queries commonly also define name, description, tags, severity, and precision.

Example teaching query:

```ql
/**
 * @name Review calls to a prohibited API
 * @description Flags calls to an API that requires security review.
 * @kind problem
 * @id py/prohibited-api-review
 * @problem.severity warning
 * @security-severity 5.0
 * @precision medium
 * @tags security
 */

import python

from Call call
where call.getFunc().toString() = "legacy_request"
select call, "Review this call and use the approved secure client."
```

This is an introductory pattern only. Matching by rendered text can be imprecise. Production rules should use the language library's semantic API/call-target model and test aliases, imports, wrappers, and shadowed names.

## 6. Example custom rule pack structure

```text
custom-security-rules/
├── qlpack.yml
├── README.md
├── queries/
│   └── python/
│       ├── ProhibitedApi.ql
│       └── ProhibitedApi.md
└── tests/
    └── python/
        ├── ProhibitedApi.ql
        └── ProhibitedApi.expected
```

Example `qlpack.yml`:

```yaml
name: cubicnova/custom-security-rules
version: 1.0.0
dependencies:
  codeql/python-all: "*"
```

Use a compatible dependency version for your CodeQL CLI and language libraries. Pin versions deliberately in a maintained pack.

## 7. Test-driven rule development

A robust test set should contain:

- **Positive case:** The insecure pattern must be detected.
- **Negative case:** A safe implementation must not be reported.
- **Boundary case:** Similar-looking but safe code must be handled correctly.
- **Alias/import case:** Alternate imports or qualified names.
- **Wrapper case:** Approved wrappers and prohibited wrappers.
- **Regression case:** A previously fixed false positive or false negative.

For CodeQL query tests, use the standard CodeQL test workflow and expected result files. Run the tests whenever the query or its library dependencies change.

## 8. False positives and false negatives

False positive: a rule reports code that does not violate the intended policy.

False negative: a rule misses code that does violate the policy.

Reduce false positives by improving semantic matching, modeling approved APIs, narrowing scope, and adding negative tests. Reduce false negatives by testing aliases, indirect calls, wrappers, alternate data paths, and framework-specific behavior.

Do not silence a noisy rule with broad exclusions before understanding why it reports.

## 9. Severity and confidence

A practical internal scale:

| Severity | Typical handling |
|---|---|
| Critical | Immediate security escalation and release review |
| High | Prioritized remediation and owner assignment |
| Medium | Planned remediation with defined SLA |
| Low | Backlog or improvement work |

Define severity based on impact and exploitability in context. Confidence describes how reliably the rule identifies the issue. Keep these dimensions separate.

For CodeQL code-scanning queries, follow the supported metadata conventions for the target query type and destination. Security queries use `@tags security`; metadata and severity fields should follow the current CodeQL guidance.

## 10. CI integration strategy

Recommended rollout:

1. Run the new rule locally against representative repositories.
2. Run in CI without blocking merges.
3. Review findings with application owners.
4. Fix query logic and document approved exceptions.
5. Enable blocking only for high-confidence, actionable rules.
6. Reassess after framework or codebase changes.

Keep CI permissions minimal. Avoid exposing privileged secrets to untrusted pull-request code. Preserve scan logs and SARIF artifacts with appropriate access controls.

## 11. Exception management

Every exception should include:

- Exact rule ID and affected path or code location.
- Business/technical reason.
- Risk assessment and compensating control.
- Named approver and owner.
- Expiry date and review date.
- Narrow scope; avoid repository-wide suppression.

Exceptions are temporary risk decisions, not permanent fixes.

## 12. Metrics

Track:

- Findings by rule and severity.
- True-positive rate and false-positive rate.
- Time to triage and remediate.
- Reopened or recurring findings.
- Rule execution time.
- Exception count and age.
- Coverage across repositories and languages.

Do not optimize for the number of alerts alone. A smaller set of high-quality, actionable rules is usually more useful.

## 13. References

- [CodeQL custom queries](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/custom-queries)
- [Writing custom queries for the CodeQL CLI](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/scan-from-the-command-line/write-custom-queries)
- [CodeQL query metadata](https://codeql.github.com/docs/writing-codeql-queries/metadata-for-codeql-queries/)
- [About CodeQL queries](https://codeql.github.com/docs/writing-codeql-queries/about-codeql-queries/)
- [CodeQL query metadata style guide](https://github.com/github/codeql/blob/main/docs/query-metadata-style-guide.md)
