# SAST Remediation — Reference Solutions

These are reference approaches. Adapt the code to the actual framework, database driver, deployment model, and threat environment. A code sample alone does not prove a production system is secure.

## 1. Prioritize findings

Use scanner severity as a starting point. Add context such as reachability, internet exposure, privileges, data sensitivity, and exploitability. Assign an owner and due date according to the organization's remediation policy.

Do not automatically treat every critical label as equally exploitable, and do not downgrade a real issue only because it is inconvenient to fix.

## 2. SQL injection

Unsafe string concatenation should be replaced with the database driver's parameterized query API:

```python
cursor.execute(
    "SELECT * FROM users WHERE email = ?",
    (email,)
)
```

Verify the driver's placeholder syntax. Add a regression test with quotes and SQL metacharacters. Use allowlists for dynamic identifiers because query parameters generally bind values, not table or column names.

## 3. XSS

Use framework templates with autoescaping enabled or a context-aware encoding API. Verify the output context. Do not use a generic HTML escaping function for JavaScript, CSS, or URL contexts, and do not mark untrusted input as safe.

Test payloads containing HTML metacharacters and confirm they are rendered as text rather than interpreted markup.

## 4. Command injection

Prefer a fixed executable and an argument list:

```python
subprocess.run(
    ["tool", validated_value],
    shell=False,
    check=True
)
```

Validate `validated_value` against a business allowlist. Review the target program's argument semantics, process privileges, filesystem access, and environment. `shell=False` is not a complete input validation strategy.

## 5. Path traversal

Prefer server-side identifiers mapped to known files. If paths must be accepted, resolve the target and enforce containment within an approved base directory. Consider symlinks, race conditions, platform-specific path rules, and file permissions. Add tests for traversal sequences and unexpected encodings.

## 6. Hardcoded secrets

Recommended steps:

1. Remove the credential from active source.
2. Rotate or revoke it immediately.
3. Store the replacement in an approved secret manager.
4. Inject it securely at runtime.
5. Check logs, artifacts, and repository history for exposure.
6. Add secret scanning and access monitoring.

Deleting a token from the latest file does not invalidate the exposed token.

## 7. Password hashing

Use a dedicated password-hashing library such as a maintained Argon2id, scrypt, or bcrypt implementation. Configure work factors according to current guidance and performance testing. Store the encoded hash output and use the library's verification function.

For existing weak hashes, design a migration strategy. Common approaches include forced password reset or rehashing after successful authentication when the plaintext password is available. Do not attempt to reverse a one-way hash.

## 8. IDOR / authorization

Apply authorization on the server for every object operation. A query scoped to the current user's permitted objects is one common pattern:

```python
document = Document.query.filter_by(
    id=document_id,
    owner_id=current_user.id
).first_or_404()
```

Adapt this to role-based, tenant-based, shared-resource, or delegated access requirements. Test owner, non-owner, and unauthenticated cases for read, update, and delete operations.

## 9. SSRF

A robust defense is layered:

- Avoid arbitrary URLs when a business identifier can select an approved destination.
- Allowlist schemes, hostnames, and ports.
- Resolve and validate destination addresses.
- Revalidate redirects and DNS results.
- Block loopback, private, link-local, and metadata networks as required.
- Enforce outbound network restrictions independently of application checks.
- Set timeouts and response-size limits.

A simple regex or hostname suffix check is insufficient on its own.

## 10. Pull request template

```markdown
## Security finding
- Alert / ticket:
- Rule / CWE:
- Severity:

## Root cause
Describe the vulnerable data flow or missing control.

## Remediation
Explain the code change and why it addresses the root cause.

## Verification
- [ ] Regression test added
- [ ] Unit/integration tests pass
- [ ] SAST rerun
- [ ] Relevant dynamic/security tests completed
- [ ] Reviewer approval

## Residual risk
Document remaining limitations, if any.
```

Keep the pull request focused. Include enough evidence for reviewers to understand why the fix is secure.

## 11. Verification matrix

| Control | What it verifies |
|---|---|
| Unit test | Secure helper behavior and edge cases |
| Integration test | Framework, database, and service interactions |
| Regression test | Original vulnerability scenario is addressed |
| SAST rescan | Static rule no longer reports the fixed path, or remaining report is understood |
| DAST/manual test | Relevant runtime behavior is safe |
| Code review | Root cause, scope, and side effects are addressed |

A finding disappearing from SAST is not sufficient by itself. Check that the scanner still analyzes the relevant files and paths.

## 12. Risk exception

A valid exception should include:

- The issue is real and clearly described.
- A named business/security risk owner approves it.
- Compensating controls are documented and tested.
- The exception has a narrow scope.
- An expiry and review date are set.
- A remediation plan and owner are assigned.

Do not label an accepted risk as a false positive.

## 13. Final project report structure

1. Executive summary.
2. Scope and application description.
3. Original SAST findings and prioritization.
4. Root-cause analysis.
5. Remediation changes.
6. Regression and integration tests.
7. Before/after SAST results.
8. Residual risk and exceptions.
9. Lessons learned and preventive controls.

## Common mistakes to avoid

- Parameterizing SQL but leaving unsafe dynamic identifiers.
- Encoding output for the wrong context.
- Assuming `shell=False` makes every command argument safe.
- Validating a path without resolving it or considering symlinks.
- Removing a secret without rotating it.
- Checking authorization only in the frontend.
- Accepting automated fixes without review and tests.
- Closing alerts before verifying the intended branch and analysis configuration.

## Key lesson

Effective SAST remediation fixes the underlying weakness, protects the relevant trust boundary, preserves application behavior, and proves the result through tests, code review, and a fresh security scan.
