# Solutions and Reference Answers

These are example answers. Final requirements should be adapted to the actual architecture, risk assessment, policies, and user needs.

## Lab 1 — Example rewrites

### “The application must be secure.”
**Improved:** Each release shall pass the security verification activities defined for its risk tier before production deployment. Any failed mandatory control shall block release unless an authorized, time-bound exception is approved.

**Evidence:** Pipeline results, test report, and exception record.

### “Passwords must be strong.”
**Improved:** The identity component shall enforce the organization's approved password policy and store passwords using a maintained adaptive password-hashing implementation. Plaintext passwords and raw password values shall not be logged.

**Evidence:** Identity configuration review, code review, and negative tests. Specify the exact policy values in the requirements baseline.

### “Logs should be good.”
**Improved:** Authentication, authorization-denial, privilege-change, and administrative events shall be recorded with UTC timestamp, event type, outcome, and correlation ID, without logging credentials or session secrets.

**Evidence:** Integration tests and log sample review.

### “The API should be protected from abuse.”
**Improved:** The API shall enforce documented rate limits for authentication and resource-intensive operations, and shall return the specified response when a limit is exceeded.

**Evidence:** Automated boundary tests and configuration review. Define threshold, time window, and identity dimensions before acceptance.

### “Data must be encrypted.”
**Improved:** Sensitive data in transit and at rest shall be protected according to the approved cryptographic baseline, with keys managed separately and access restricted.

**Evidence:** TLS/configuration review, data-store configuration evidence, and key-access review.

## Lab 2 — Example requirements

- Customer users shall access only invoices and statements belonging to their authorized customer account.
- The server shall enforce authorization on every invoice read, download, update, and delete operation.
- Sessions shall expire according to approved idle and absolute timeout values.
- Logout shall invalidate the active session.
- Support staff shall receive only the permissions required for their assigned duties.
- Support-staff access to customer records shall be logged with actor, target, action, outcome, timestamp, and correlation ID.
- Sensitive data shall be protected in transit and at rest according to the approved baseline.
- Statement downloads shall require authorization at the time of each download.
- Authentication endpoints shall enforce approved rate limits and monitoring.
- Logs shall not include passwords, bearer tokens, session cookies, or full statement contents.

## Lab 3 — Acceptance criteria examples

- Account A can read its own invoice.
- Account A cannot read Account B's invoice by changing an invoice ID.
- Account A cannot download or delete Account B's invoice.
- Authorization is enforced server-side for every relevant endpoint and HTTP method.
- Unauthorized responses contain no invoice data or sensitive metadata.
- Automated tests cover both positive and negative cases.

## Lab 4 — Traceability matrix

Example columns:

`Requirement ID, Version, Requirement, Threat/Risk, Design Component, Owner, Verification Method, Test ID, Evidence, Status, Release Gate`

Traceability should allow a reviewer to move from a threat to a requirement, then to the implementation and verification evidence.

## Lab 5 — Prioritization

A reasonable approach is to prioritize controls that mitigate severe, plausible threats to exposed or critical assets, while accounting for dependencies. Document the scoring scale and assumptions. Do not present a local priority score as a CVSS score.

## Lab 6 — Requirement review

Replace subjective terms with measurable values. Examples:
- “regularly” → a specified interval and event trigger.
- “strong TLS” → approved TLS baseline/version/cipher policy.
- “logs are retained” → a defined retention period and deletion rule.
- “rate limiting” → threshold, time window, keying dimensions, and response.
- “quick recovery” → approved RTO/RPO plus restoration test evidence.
- “authorized exception” → named role, documented approval, scope, and expiry.

## Lab 7 — Exception request

A complete request identifies the requirement and reason for deferral, affected threats, exposure, compensating controls, validation evidence, accountable risk owner, approval, expiry, monitoring, rollback/containment trigger, and committed remediation date. A launch deadline alone does not reduce risk.

## Lab 8 — Verification mapping

- Input validation: unit tests plus integration tests.
- Object-level authorization: automated negative integration tests and targeted security testing.
- TLS baseline: configuration scan and deployment review.
- Security logging: integration tests and sample-log inspection.
- Backup restoration: operational recovery exercise with recorded RTO/RPO evidence.

Use more than one method when the risk warrants it.

## Common mistakes

- Requirements that say “secure,” “strong,” or “appropriate” without measurable criteria.
- Requirements with no owner, rationale, or verification plan.
- Treating a policy reference as proof that a control works.
- Writing implementation detail that unnecessarily constrains the architecture.
- Missing negative tests and abuse cases.
- Exceptions without expiry, monitoring, or accountable risk acceptance.
