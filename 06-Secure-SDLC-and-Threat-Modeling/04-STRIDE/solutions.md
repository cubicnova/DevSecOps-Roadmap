# STRIDE Solutions and Reference Answers

Answers below are examples, not a substitute for analyzing the actual system.

## Lab 1 — Category mapping

1. Changing an invoice amount: **Tampering**; may also enable fraud or elevation if permissions are bypassed.
2. Forged identity header: **Spoofing**.
3. Unlimited expensive jobs: **Denial of Service**.
4. Missing admin audit trail: **Repudiation**.
5. Reading another customer's record: **Information Disclosure**; often caused by broken object-level authorization.
6. Normal user invoking admin operation: **Elevation of Privilege**.

## Lab 2 — DFD outline

A possible flow:

`Customer Browser → Public Web/API → Application Database`

Supporting flows:
- Browser ↔ Identity Provider: authentication redirect/tokens.
- API ↔ Identity Provider: token validation or identity metadata.
- API → Central Logging Service: security audit events.
- API ↔ Database: queries and updates.

Trust boundaries may include the public internet to the application, application to identity provider, application to database, and application to central logging. Label actual data and protocols in your own diagram; do not assume that network location alone makes a component trusted.

## Lab 3 — Example threats

- Browser/API: stolen session is reused (**Spoofing**).
- Browser/API: request fields are modified (**Tampering**).
- API/log service: admin actions are not recorded reliably (**Repudiation**).
- API/database: cross-customer data is returned (**Information Disclosure**).
- Public API: repeated costly requests exhaust capacity (**Denial of Service**).
- API/admin functions: low-privilege user invokes privileged operation (**Elevation of Privilege**).
- API/database: application service account has excessive write privileges (**Elevation of Privilege**).
- API/log service: log transport failure creates an investigation gap (**Repudiation**, and potentially availability/integrity concerns depending on the design).

Threat classification can overlap; state the reasoning.

## Lab 4 — Register fields

Use stable threat IDs such as `TM-001`. Include the affected component/flow, concrete scenario, impact, existing controls, likelihood, impact score, proposed mitigation, owner, verification evidence, status, and residual risk. Keep the scoring method documented; do not treat the STRIDE category itself as a severity score.

## Lab 5 — Mitigation examples

### Cross-customer invoice access
- Prevent: server-side object-level authorization on every request.
- Detect: alert on repeated denied cross-account access attempts.
- Recover: incident response workflow to revoke sessions and assess exposed records.
- Verify: automated tests using two separate test accounts.

### Missing administrative audit evidence
- Prevent: require privileged operations to emit audit events through a controlled logging interface.
- Detect: alert on missing event volume or collector gaps.
- Recover: preserve alternate platform audit records and investigate the gap.
- Verify: integration test plus simulated collector outage.

### Expensive report endpoint
- Prevent: rate limits, bounded query complexity, pagination, and timeouts.
- Detect: latency, queue depth, and resource saturation alerts.
- Recover: graceful degradation and capacity recovery procedures.
- Verify: authorized load tests with documented thresholds.

## Lab 6 — Upload feature

| Category | Example threat | Mitigation |
|---|---|---|
| Spoofing | Attacker submits an upload as another user | Authenticate request and bind ownership server-side |
| Tampering | File or metadata changes between validation and processing | Verify integrity where needed; validate metadata and processing state |
| Repudiation | Uploader denies submitting a file | Record actor, file ID/hash, timestamp, and outcome in protected audit logs |
| Information Disclosure | Uploaded file becomes publicly accessible | Private storage, object-level authorization, short-lived access links if appropriate |
| Denial of Service | Huge or numerous uploads exhaust storage/worker capacity | Size/type limits, quotas, rate limits, bounded queues, timeouts |
| Elevation of Privilege | Worker processes files with unnecessary administrative permissions | Isolate workers, least-privilege service identity, sandbox processing |

Use safe file-processing practices and avoid executing uploaded content.

## Lab 7 — Assumptions

Example: “The log collector is always available.” If false, audit events may be delayed or lost. Define bounded buffering, delivery retries, health monitoring, and alerting for gaps. Record the residual risk and test the failure behavior.

Other assumptions might concern identity-provider availability, administrator behavior, internal network trust, third-party security, backup integrity, and dependency integrity.

## Lab 8 — Change review

A new payment provider adds an external entity and trust boundary. Assess spoofing of provider callbacks, tampering with payment amounts/status, repudiation of transactions, disclosure of payment/customer data, denial of service or provider outage, and privilege misuse in callback processing. Validate signed/authenticated callbacks, server-side amount verification, idempotency, audit trails, least privilege, and outage handling as appropriate.

## Common mistakes

- Writing category labels without concrete scenarios.
- Treating every STRIDE category as equally relevant to every component.
- Assuming a mitigation is effective without verification.
- Assigning severity from the category name alone.
- Ignoring trust boundaries and third-party dependencies.
- Leaving threat owners, due dates, and residual risk undocumented.
- Failing to update the model when architecture changes.
