# SAST Remediation

## Learning objectives

By the end of this module, learners should be able to:

- Interpret SAST findings and prioritize remediation by risk.
- Trace vulnerabilities from input sources to sensitive sinks.
- Select secure coding fixes that address root causes.
- Validate remediation with unit tests, regression tests, and rescanning.
- Manage remediation through pull requests and CI quality gates.
- Document residual risk and verify that fixes do not introduce regressions.

## 1. What is SAST remediation?

SAST remediation is the process of correcting security weaknesses identified through static application security testing. The goal is not simply to silence a scanner alert. A good remediation removes or reduces the underlying weakness, preserves intended functionality, and is verified by testing and a subsequent scan.

A typical lifecycle is:

1. Detect and record a finding.
2. Understand the vulnerability and affected code path.
3. Assess severity, exploitability, exposure, and business impact.
4. Identify the root cause and appropriate control.
5. Implement the smallest safe change.
6. Add or update tests.
7. Review the code and security impact.
8. Run tests and SAST again.
9. Confirm the alert is resolved and document residual risk.

## 2. Prioritizing remediation

Prioritize based on more than the scanner's severity label. Consider:

- Exploitability and attacker prerequisites.
- Internet exposure and reachable code paths.
- Privileges required.
- Confidentiality, integrity, and availability impact.
- Sensitive data and business criticality.
- Existing compensating controls.
- Whether the issue is newly introduced or part of a backlog.

Example prioritization:

| Priority | Example | Response |
|---|---|---|
| P0 / Critical | Active, exploitable remote compromise path | Immediate escalation and containment |
| P1 / High | Reachable injection or authentication bypass | Expedite fix and release review |
| P2 / Medium | Context-dependent weakness with limited exposure | Planned remediation with owner and due date |
| P3 / Low | Low-impact hardening issue | Backlog and scheduled improvement |

Use the organization's approved severity and SLA policy. A scanner's severity is an input, not the complete risk decision.

## 3. Understand the vulnerability before fixing it

For each finding, identify:

- **Source:** Where untrusted or sensitive data enters the program.
- **Transformation:** How the data is assigned, parsed, encoded, validated, or passed between functions.
- **Sink:** Where the data reaches a sensitive operation.
- **Trust boundary:** Where data crosses from an untrusted context to a trusted one.
- **Existing controls:** Authentication, authorization, validation, parameterization, output encoding, or sandboxing.

For data-flow alerts, inspect the full path. Fixing only the highlighted line may leave another path vulnerable.

## 4. Remediation principles

- Fix the root cause at the correct trust boundary.
- Prefer safe APIs and framework protections.
- Use context-specific validation and encoding.
- Apply authorization on the server side for every protected operation.
- Keep secrets out of source code and logs.
- Avoid broad exception handling that hides security failures.
- Preserve business behavior and compatibility.
- Add regression tests for the original exploit scenario.
- Avoid scanner-specific workarounds that merely suppress alerts.

## 5. Common vulnerabilities and secure fixes

### SQL injection

Weak pattern:

```python
query = "SELECT * FROM users WHERE email = '" + email + "'"
cursor.execute(query)
```

Safer pattern:

```python
cursor.execute(
    "SELECT * FROM users WHERE email = ?",
    (email,)
)
```

Use the parameter syntax supported by the database driver. Bind values separately; use strict allowlists for dynamic identifiers such as table or column names.

### Cross-site scripting (XSS)

Weak pattern:

```python
return "<p>" + user_input + "</p>"
```

Safer direction: use a framework's context-aware output encoding or safe templating defaults. HTML text, attributes, JavaScript, CSS, and URL contexts require different handling. Avoid marking untrusted input as safe.

### Command injection

Weak pattern:

```python
os.system("tool " + user_value)
```

Safer direction: avoid shell execution, pass a fixed executable and argument list, validate allowed values, and constrain accessible resources.

```python
subprocess.run(
    ["tool", validated_value],
    shell=False,
    check=True
)
```

` shell=False` reduces shell parsing risk but does not make every argument safe for the invoked program.

### Path traversal

Weak pattern: joining an untrusted path to a storage directory without verifying the final resolved location.

Safer direction: use server-generated identifiers or allowlisted filenames, resolve the final path, and enforce that it remains inside the intended base directory. Account for symlinks and platform-specific path behavior.

### Hardcoded secrets

Move credentials to an approved secret manager or protected CI secret store. Rotate exposed credentials, review access logs, and remove the secret from repository history where required. Deleting it from the latest commit alone does not invalidate an exposed credential.

### Weak password storage

Use a dedicated password-hashing function with a unique salt and a configurable work factor, such as Argon2id, scrypt, or an approved bcrypt implementation. Do not use a fast general-purpose hash such as plain SHA-256 for password storage.

### Broken access control / IDOR

Enforce authorization on the server for every object access. Derive the user's identity from a trusted authentication context and verify ownership or permissions for the specific resource. Unpredictable IDs are not an authorization control.

### SSRF

Use allowlists for permitted destinations, restrict network egress, validate resolved addresses and redirects, and block access to sensitive internal networks and metadata endpoints. Defenses must account for DNS rebinding and redirect behavior.

## 6. Validate the fix

A remediation is not complete until it is verified.

Recommended checks:

1. Unit test the secure helper or function.
2. Add a regression test that exercises the original unsafe input.
3. Test boundary cases and expected business behavior.
4. Run integration tests where trust boundaries or framework behavior are involved.
5. Run SAST with the same or equivalent query suite.
6. Review whether the alert is resolved for the intended branch and configuration.
7. Check for similar vulnerable patterns elsewhere.

A clean scan is not proof of security. Combine scanner results with code review and testing.

## 7. Pull request remediation workflow

A good security fix pull request should include:

- Alert or issue reference.
- Vulnerability and root-cause summary.
- Before/after behavior.
- Secure coding change.
- Regression tests.
- SAST rescan result.
- Compatibility and performance considerations.
- Any residual risk or follow-up work.

Keep changes focused so reviewers can understand the security effect. Do not bundle unrelated refactoring with an urgent vulnerability fix unless necessary.

## 8. CI/CD quality gates

A practical policy is to:

- Scan pull requests and protected-branch pushes.
- Block new critical/high findings when confidence and policy justify it.
- Track existing backlog separately from newly introduced issues.
- Allow documented, time-bound exceptions through an approved process.
- Avoid failing every build for low-confidence or informational findings without a risk rationale.
- Re-run scans after remediation.

The exact check behavior and feature availability depend on the scanning platform, repository configuration, and product plan.

## 9. Using automated fix suggestions

Tools such as GitHub Copilot Autofix may provide a proposed change for supported code-scanning alerts. Treat suggestions as drafts:

1. Understand the original finding.
2. Review the suggested diff and its assumptions.
3. Confirm the fix addresses the root cause.
4. Check authorization, validation, error handling, and edge cases.
5. Run tests and SAST.
6. Have a developer/security reviewer approve the change.

Automated suggestions are not guaranteed to be available or correct for every alert.

## 10. Remediation tracking

Record:

| Field | Description |
|---|---|
| Finding ID | Scanner alert or ticket |
| Rule / CWE | Detection rule and weakness category |
| Severity | Scanner and business risk |
| Affected component | Service, module, file, and branch |
| Owner | Responsible developer/team |
| Due date | Based on remediation SLA |
| Root cause | Why the weakness exists |
| Fix | Change made |
| Tests | Regression and verification evidence |
| Rescan | Scanner, date, and result |
| Status | Open, in progress, fixed, verified, exception |
| Residual risk | Remaining exposure and owner |

## 11. Common remediation mistakes

- Escaping data for the wrong output context.
- Using validation as a substitute for parameterized SQL.
- Relying on client-side authorization.
- Treating UUIDs or hidden fields as access controls.
- Setting `shell=False` but allowing dangerous arguments.
- Suppressing a rule instead of fixing the code.
- Removing a secret without rotating it.
- Fixing one path while leaving equivalent paths exposed.
- Trusting an automated patch without tests.
- Closing the alert before the fix is analyzed on the target branch.

## 12. Best practices

- Establish severity-based remediation SLAs.
- Assign a clear owner to every confirmed finding.
- Fix root causes and reusable insecure helpers.
- Add regression tests for every meaningful security fix.
- Verify fixes with SAST and appropriate dynamic tests.
- Use peer review for security-sensitive changes.
- Track remediation age and recurrence.
- Document exceptions and compensating controls.
- Feed recurring patterns back into secure coding training and custom rules.

## References

- [GitHub code scanning alerts](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning-alerts)
- [Triaging code scanning alerts in pull requests](https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts/triage-alerts-in-pull-requests)
- [Resolving code scanning alerts](https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts/resolve-alerts)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
