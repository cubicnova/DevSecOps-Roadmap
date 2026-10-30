# SAST Remediation — Practical Exercises

## Lab requirements

- A local training application with intentionally vulnerable code.
- Python and the required framework/database dependencies.
- A SAST scanner such as CodeQL or another approved tool.
- Git and a separate remediation branch.

Perform these exercises only on code you own or are authorized to test.

## Exercise 1: Review and prioritize findings

1. Run SAST against the training application.
2. Record at least five findings.
3. Identify rule ID, CWE (if available), severity, file, and line.
4. Assess exposure, reachability, attacker prerequisites, and impact.
5. Assign a remediation priority using a documented policy.

**Deliverable:** prioritized vulnerability backlog.

## Exercise 2: Trace a SQL injection

1. Identify the input source.
2. Follow the value to the SQL execution sink.
3. Inspect the database driver and query construction.
4. Replace string concatenation with parameter binding.
5. Add a regression test.
6. Rerun SAST and review the alert.

**Deliverable:** secure code, test, and scan evidence.

## Exercise 3: Remediate XSS

1. Identify the untrusted value and output context.
2. Determine whether the framework autoescapes by default.
3. Replace unsafe string construction with safe templating or context-aware encoding.
4. Test HTML metacharacters.
5. Check that no unsafe rendering bypass remains.

**Deliverable:** remediation diff and test results.

## Exercise 4: Remediate command injection

1. Identify user-controlled command input.
2. Remove shell command string construction.
3. Use a fixed executable and argument list.
4. Validate arguments against an allowlist.
5. Review file and process permissions.
6. Add tests for spaces, separators, and unexpected values.

**Deliverable:** secure implementation and regression tests.

## Exercise 5: Remediate path traversal

1. Identify user-controlled path segments.
2. Replace arbitrary paths with allowlisted identifiers where possible.
3. Resolve the target path and enforce directory containment.
4. Consider symlinks and race conditions.
5. Test traversal sequences and valid filenames.

**Deliverable:** secure file-access function and tests.

## Exercise 6: Remove and rotate a hardcoded secret

1. Identify the hardcoded credential.
2. Move it to a secret manager or protected runtime configuration.
3. Rotate the exposed credential.
4. Review logs and access history.
5. Consider repository history cleanup according to organizational policy.
6. Add secret scanning to CI.

**Deliverable:** remediation record and verification evidence.

## Exercise 7: Fix weak password storage

1. Identify the password hashing function.
2. Replace fast general-purpose hashing with an approved password-hashing library.
3. Verify that salts and work factors are handled by the library.
4. Add tests for hash generation and verification.
5. Plan a safe migration for existing password hashes.

**Deliverable:** implementation and migration note.

## Exercise 8: Fix IDOR

1. Identify an endpoint that accepts an object ID.
2. Determine the authenticated user's identity and authorization model.
3. Add server-side ownership or permission checks.
4. Test access as the owner, another user, and an unauthenticated user.
5. Verify read, update, and delete paths.

**Deliverable:** authorization fix and test matrix.

## Exercise 9: Review SSRF remediation

1. Identify arbitrary URL input.
2. Determine whether the application actually needs arbitrary destinations.
3. Prefer an identifier-to-destination mapping if feasible.
4. Design hostname/IP/redirect validation and egress restrictions.
5. Document DNS rebinding and metadata endpoint considerations.

**Deliverable:** SSRF remediation design.

## Exercise 10: Build a remediation pull request

1. Create a feature branch.
2. Fix one confirmed finding.
3. Add tests and update relevant documentation.
4. Run the project's test suite.
5. Run SAST and record the result.
6. Submit a focused pull request with the template in `examples.md`.

**Deliverable:** pull request or local PR-style report.

## Exercise 11: Validate with multiple controls

For one fixed vulnerability:

1. Run unit and integration tests.
2. Run SAST.
3. Run a relevant DAST or manual security test where appropriate.
4. Review the code diff.
5. Confirm no new security weakness was introduced.

**Deliverable:** verification matrix.

## Exercise 12: Manage a remediation exception

1. Select a real issue that cannot be fixed immediately in the lab scenario.
2. Document why it remains.
3. Identify compensating controls.
4. Assign owner and approver.
5. Set an expiry/review date.
6. Define the follow-up remediation plan.

**Deliverable:** time-bound risk acceptance record.

## Exercise 13: Final mini-project

Remediate at least three different vulnerability classes in a small application. Include:

- Original findings and prioritization.
- Root-cause analysis.
- Secure code changes.
- Regression tests.
- SAST before/after evidence.
- Pull request summary.
- Residual risk and lessons learned.

**Deliverable:** complete remediation report and code.

## Assessment rubric

| Area | Marks |
|---|---:|
| Finding review and prioritization | 10 |
| Root-cause and data-flow analysis | 15 |
| Secure coding remediation | 25 |
| Regression and integration testing | 15 |
| SAST rescan and verification | 15 |
| Pull request and documentation | 10 |
| Risk and exception management | 10 |
| **Total** | **100** |
