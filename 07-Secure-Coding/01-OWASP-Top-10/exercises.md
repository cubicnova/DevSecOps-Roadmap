# OWASP Top 10:2025 — Exercises

Complete these exercises using a local training application, sample code, or an environment you are explicitly authorized to test.

## Exercise 1: Learn the categories

For each scenario, identify the most relevant OWASP Top 10:2025 category and explain why:

1. A customer retrieves another customer's invoice by changing an identifier.
2. A production service exposes detailed stack traces.
3. A CI job uses an untrusted dependency source and a token with release privileges.
4. An encryption key is committed to a public repository.
5. A database query concatenates request input into SQL.
6. A password-reset workflow has no abuse controls or clear security requirements.
7. A session remains valid after a sensitive account change when it should be rotated or revoked.
8. A release artifact can be modified after testing without verification.
9. Privilege changes are not logged and no alert is generated.
10. A policy service timeout causes a protected action to be allowed.

## Exercise 2: Access-control test plan

A multi-tenant application has `GET /projects/{id}`, `PUT /projects/{id}`, and `DELETE /projects/{id}`.

Write at least six tests that cover:
- Access by the resource owner
- Cross-tenant access
- Read-only users
- Direct requests that bypass the user interface
- Invalid or expired credentials
- Authorization-service failure

State the expected result and evidence for each test.

## Exercise 3: Fix injection

Review this conceptual code:

```python
email = request.args.get("email", "")
query = "SELECT id, email FROM users WHERE email = '" + email + "'"
db.execute(query)
```

1. Explain the vulnerability.
2. Rewrite it using the database driver's parameterized-query syntax.
3. Name two additional defense-in-depth controls.
4. Describe a safe regression test strategy.

## Exercise 4: Secure configuration review

Create a checklist for a production web service covering:
- Debug settings
- Default accounts and sample endpoints
- TLS and security headers
- CORS
- Cloud storage permissions
- Secrets and environment configuration
- Management ports and network exposure
- Dependency and framework versions

For each item, explain how it can be verified automatically or manually.

## Exercise 5: Supply-chain threat model

A project builds a web application in CI and publishes a container image.

Identify:
- Assets and trust boundaries
- Threats to source, dependencies, CI credentials, build runners, registry, and deployment
- At least six controls
- Negative tests and evidence
- An owner for each control

Include a plan for handling dependency findings and urgent credential revocation.

## Exercise 6: Cryptography and data protection

A service stores passwords, customer contact details, and API credentials.

Propose a design that addresses:
- Data minimization and retention
- Transport protection
- Password hashing
- Encryption keys
- Secret storage and rotation
- Log redaction
- Backup protection

Explain why encryption alone does not solve access-control problems.

## Exercise 7: Authentication and session review

Review a login flow with the following properties:
- Unlimited login attempts
- Session ID is not changed after login
- Session cookie lacks `Secure` and `HttpOnly`
- Password reset tokens never expire
- Responses reveal whether an email address is registered

Prioritize fixes and create tests for each issue.

## Exercise 8: Logging and alerting

Design an event and alert plan for:
- Repeated authentication failures
- Authorization denials across many resources
- Privilege changes
- Sensitive data exports
- Unexpected deployment activity
- Security-control dependency failures

Define the minimum event fields, who owns alerts, what should not be logged, and how to verify that alerts reach the responder.

## Exercise 9: Exceptional conditions

A report-export endpoint calls an authorization service, a database, and a file-generation service. Dependencies can time out or return errors.

For each failure, define:
- Expected user-facing response
- Whether the operation may proceed
- Retry and timeout behavior
- Transaction or idempotency considerations
- Logging and alerting
- Recovery and test evidence

## Exercise 10: DevSecOps mapping

Create a table mapping all ten OWASP Top 10:2025 categories to:
- A preventive control
- A CI/CD or deployment check
- A runtime detection signal
- A regression test
- A responsible team

## Exercise 11: Finding write-up

Write a professional finding for a confirmed cross-tenant object access issue in an authorized test environment. Include title, category, scope, impact, evidence, remediation, and retest steps. Use synthetic data and do not include real secrets.

## Exercise 12: Mini project

Build or select a deliberately vulnerable local application and choose at least three categories. For each category:
1. Describe the vulnerable behavior.
2. Reproduce it safely.
3. Fix the root cause.
4. Add a regression test.
5. Run relevant static analysis or configuration checks.
6. Document evidence and remaining risk.

## Submission checklist

- [ ] Correct 2025 category names are used.
- [ ] Each finding has a root cause and impact.
- [ ] Fixes address root causes, not only symptoms.
- [ ] Negative tests include unauthorized and failure paths.
- [ ] Secrets and personal data are redacted from evidence.
- [ ] Controls have verification evidence and owners.
