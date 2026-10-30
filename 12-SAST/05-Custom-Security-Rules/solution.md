# Custom Security Rules — Reference Solutions

These are model answers and implementation guidance. Exact query APIs and test commands depend on the CodeQL language library and CLI version.

## 1. Identify a policy gap

Example policy: application code must use the centrally approved outbound HTTP client so that TLS verification, timeouts, and egress controls are applied consistently.

Why this is a good candidate:

- It is specific to the organization's architecture.
- The insecure behavior is identifiable in source code.
- A safe alternative exists.
- A rule can be tested against direct calls and approved wrappers.

If the policy is only about formatting or a simple local syntax pattern, a linter may be more maintainable than CodeQL.

## 2. Example rule specification

| Field | Example |
|---|---|
| Rule ID | `PY-CUST-001` |
| Title | Prohibited legacy HTTP client |
| Objective | Require approved outbound HTTP wrapper |
| Risk | Missing TLS/timeouts/egress controls |
| Scope | Python application source |
| Detection | Calls to specified legacy client APIs |
| Severity | Medium, adjusted to context |
| Confidence | High only after semantic matching and tests |
| False positives | Test doubles, vendor adapters, approved compatibility modules |
| Remediation | Use `company_security.http.secure_get` |
| Tests | Direct call, alias, wrapper, unrelated same-name function |
| Owner | Application Security |
| Exception | Scoped approval with expiry |

## 3. Pack creation

```bash
mkdir -p custom-security-rules/queries/python
cd custom-security-rules
```

`qlpack.yml`:

```yaml
name: cubicnova/custom-security-rules
version: 1.0.0
dependencies:
  codeql/python-all: "*"
```

Then:

```bash
codeql pack install
codeql pack compile .
```

If compilation fails, verify the CLI version, dependency compatibility, pack location, and query imports.

## 4. Introductory query

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

This query demonstrates the shape of a basic alert query. It should not be treated as production-ready because string rendering does not reliably distinguish APIs, aliases, and shadowed functions.

## 5. Semantic matching strategy

A production-quality implementation should:

1. Identify the actual imported module and callable.
2. Resolve aliases and qualified references.
3. Distinguish the prohibited library from unrelated functions with the same name.
4. Model approved wrappers and test doubles explicitly.
5. Add negative tests for safe code.

Consult the Python CodeQL library documentation and existing standard queries for the exact predicates supported by the installed pack. Do not invent a predicate name without verifying it against that version.

## 6. Weak password hashing rule

Avoid a global rule that flags every SHA-256 call. SHA-256 is appropriate for integrity checks and content identifiers, but it is not suitable as a standalone password-storage function.

A better rule specification focuses on password-storage flows:

- Source: password input or password field.
- Sink: persistent credential storage.
- Unsafe operation: general-purpose fast hash without password-specific work factor and salt management.
- Approved alternatives: organization-approved password hashing APIs.
- Tests: password storage with fast hash, non-password SHA-256 use, approved password hash, wrapper function.

A complete CodeQL implementation may require data-flow modeling to establish that a hash result reaches credential storage.

## 7. TLS verification rule

A useful rule targets explicit disabling of certificate verification, such as `verify=False` for a known HTTP client API.

Tests should include:

- Insecure explicit disablement: expected alert.
- Default verification: no alert.
- Explicit secure verification: no alert.
- Unrelated function with an argument named `verify`: no alert.
- Approved wrapper that enforces verification: no alert.

The query should identify the actual API and argument semantics, not merely search for the text `verify=False`.

## 8. Test quality

Example test matrix:

| Case | Expected |
|---|---|
| Direct call to prohibited API | Alert |
| Alias import to prohibited API | Alert |
| Unrelated function with same short name | No alert |
| Approved wrapper | No alert |
| Test mock with prohibited name | Depends on explicit policy; document it |
| Prohibited call in supported wrapper | Alert |
| Safe configuration | No alert |
| Previously reported false positive | No alert after fix |

A rule should not be promoted to blocking mode until its expected behavior is stable on representative repositories.

## 9. Query help

Place `ProhibitedApi.md` beside `ProhibitedApi.ql`. Include:

- What the rule detects.
- Why the behavior is risky.
- How to remediate it.
- Any important limitations.

For CLI SARIF output:

```bash
codeql database analyze db-python \
  ./custom-security-rules \
  --format=sarif-latest \
  --output=results.sarif \
  --sarif-add-query-help
```

The query help option requires a sufficiently recent CodeQL CLI; check the installed CLI documentation.

## 10. CI integration

A conceptual command step:

```yaml
- name: Analyze with custom security rules
  run: |
    codeql database analyze db-python \
      ./custom-security-rules \
      --format=sarif-latest \
      --output=custom-results.sarif
```

A complete workflow must also create the database, install compatible query dependencies, and upload SARIF using the supported GitHub integration. Use least-privilege permissions and protect secrets from untrusted pull-request code.

## 11. False-positive tuning

For every false positive:

1. Capture the smallest reproducible example.
2. Determine which assumption in the query was wrong.
3. Improve semantic identification or model approved behavior.
4. Add a negative regression test.
5. Run all existing tests to prevent regressions.

Do not add broad path exclusions unless the exception is intentional, documented, and reviewed.

## 12. Exception record

```yaml
rule_id: PY-CUST-001
path: src/legacy/integration.py
owner: application-team
reason: "Temporary compatibility with a vendor SDK"
compensating_control: "Outbound destination allowlist and monitored egress"
approved_by: security-team
expires_on: 2026-12-31
```

This is an illustrative governance record, not a native CodeQL suppression format. Store exceptions in the organization's approved risk-management system.

## 13. Effectiveness metrics

Example calculations:

- Precision = true positives / (true positives + false positives).
- False-positive rate among alerts = false positives / total alerts.
- Mean time to triage = average time from alert creation to initial disposition.
- Mean time to remediate = average time from confirmed finding to verified fix.
- Coverage = repositories scanned / repositories in scope.

Report denominators and time windows so metrics are interpretable. Avoid comparing rule precision across teams without considering codebase and scope differences.

## 14. Production-readiness checklist

- [ ] Policy and threat model are approved.
- [ ] Rule ID is stable and unique.
- [ ] Query metadata is valid for the target analysis mode.
- [ ] Positive and negative tests pass.
- [ ] Aliases and wrappers are considered.
- [ ] Query help explains risk and remediation.
- [ ] Performance is acceptable on representative repositories.
- [ ] CI permissions and trust boundaries are reviewed.
- [ ] Exceptions have owners and expiry dates.
- [ ] Rule has a maintainer and review schedule.

## Key lesson

A custom security rule is an engineered control, not merely a pattern match. Its value depends on a precise policy, reliable detection, representative tests, useful remediation, safe CI integration, and ongoing ownership.
