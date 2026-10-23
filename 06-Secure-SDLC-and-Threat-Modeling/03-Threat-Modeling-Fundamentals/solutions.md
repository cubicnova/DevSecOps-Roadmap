# Threat Modeling Exercises — Sample Solutions

These are example answers, not the only valid answers. Threat modeling depends on architecture, assumptions, business context, and existing controls. Record uncertainty rather than presenting guesses as facts.

## Exercise 1 — Identify assets and trust boundaries

**Possible assets**
1. Uploaded PDF contents
2. User identity and session credentials
3. File ownership and sharing metadata
4. Scan results and file status
5. Cloud storage credentials and access policies
6. Database integrity and availability
7. Audit events

**Actors and components**
- Actors: uploader, recipient, administrator, identity provider
- Components: browser, API, object storage, metadata database, message queue, scanning worker

**Possible trust boundaries**
- User browser to public API
- API to database
- API to object storage
- Queue to scanning worker
- Worker to storage and metadata services

**Important flows**
- Upload request and file bytes
- Metadata creation and owner assignment
- Scan job and scan result
- Download request and authorization decision
- Security/audit events

**Assumptions to confirm**
- Are object-storage objects private by default?
- Does the worker process untrusted PDFs in a sandbox?
- Are download permissions checked for every request?

## Exercise 2 — Apply STRIDE

| Category | Example scenario | Mitigation | Validation |
|---|---|---|---|
| Spoofing | A forged identity field causes a file to be attributed to another user | Derive identity from validated server-side authentication | Send a request with a mismatched user ID and verify it cannot change the authenticated identity |
| Tampering | An attacker changes file metadata or scan status | Restrict write access; allow only trusted worker transitions | Attempt unauthorized status updates with a low-privilege account |
| Repudiation | A user denies uploading or sharing a document | Record authenticated actor, action, object, time, and result in protected logs | Verify required fields and access controls in audit events |
| Information disclosure | A user downloads another user's file by changing its identifier | Check ownership or explicit sharing permissions on each download | Automated cross-account access tests |
| Denial of service | Large or numerous uploads exhaust storage or scanning workers | Enforce size, rate, concurrency, quota, and timeout limits | Controlled tests confirm configured limits and safe failures |
| Elevation of privilege | A user sets a client-controlled role or status to gain access | Enforce authorization server-side; do not trust client role fields | Attempt privileged actions as a normal test user |

Overlap is expected. For example, a missing ownership check may enable both information disclosure and elevation of privilege. Use the categories to prompt analysis, but track the scenario and remediation clearly.

## Exercise 3 — Prioritize risk

| Threat | Calculation | Score | Training band |
|---|---:|---:|---|
| A | 4 × 5 | 20 | High |
| B | 2 × 3 | 6 | Medium |
| C | 5 × 2 | 10 | Medium |
| D | 1 × 5 | 5 | Low |

A reasonable first candidate is A because it combines high likelihood and critical impact. However, final order should consider exploitability, exposure, affected population, existing controls, business consequences, remediation effort, and confidence in the ratings. Threat D has critical impact despite a low score, so it may still deserve attention if its consequences are catastrophic or its likelihood estimate is uncertain.

## Exercise 4 — Review an unsafe design

**Threat 1: User-ID tampering**
- STRIDE: Elevation of privilege / Information disclosure
- Flaw: The API trusts a client-supplied identity.
- Control: Derive the actor from the validated session or token; check document ownership or explicit sharing permissions server-side.
- Test: Authenticate as User A and request User B's document ID; expect a consistent denial response.

**Threat 2: Role tampering**
- STRIDE: Elevation of privilege
- Flaw: Authorization is decided from a request-body field.
- Control: Obtain roles from a trusted server-side authorization source and check permission for every privileged operation.
- Test: Submit `role: admin` as a normal user; the request must not grant admin capabilities.

**Threat 3: Identifier enumeration**
- STRIDE: Information disclosure
- Flaw: Predictable identifiers plus missing object-level authorization may expose records.
- Control: Enforce authorization regardless of identifier complexity; rate-limit and monitor suspicious access patterns.
- Test: Use known and random document IDs across separate test accounts and confirm unauthorized access is denied.

**Example negative tests**
1. User A cannot retrieve, modify, or delete a document owned only by User B.
2. A normal user cannot invoke an admin endpoint by changing request JSON, headers, or query parameters.

Opaque identifiers are not a replacement for authorization.

## Exercise 5 — Build an attack tree

**Root goal:** Access a private document without permission.

Possible alternative branches:

- **Abuse authorization**
  - Obtain a valid low-privilege account (precondition: account available)
  - Change document ID in a request
  - Succeed only if object-level authorization is missing
- **Steal or reuse a session**
  - Obtain a session token through a separate compromise
  - Replay it while valid
  - Succeed if session protections and authorization allow the access
- **Abuse a sharing link**
  - Obtain or guess a link
  - Access it before expiration or revocation
  - Succeed if link scope, entropy, expiry, or revocation controls are inadequate

High-value mitigations include object-level authorization, secure session handling and revocation, high-entropy scoped sharing tokens, expiry and revocation, monitoring, and tests for cross-account access. Attack trees describe possible paths; they do not imply that each path is feasible in a particular system.

## Exercise 6 — Write actionable mitigations

Examples:

- **Uploads:** “The API rejects files exceeding the configured size limit, validates permitted file types using content inspection, stores files outside executable paths, and makes files downloadable only after the required scanning state is complete.” Verify with boundary-size tests, malformed-file tests, and status-transition tests.
- **Logging:** “For every document download, record the authenticated actor, document identifier, timestamp, outcome, and correlation ID in access-controlled logs without recording document contents or credentials.” Verify representative success and denial events.
- **Brute force:** “The authentication service applies documented rate limits and progressive defenses to repeated failures and emits an alert when the defined threshold is crossed.” Verify controlled tests and alert delivery.
- **Sensitive data:** “The service encrypts data in transit, restricts access by role and object ownership, and redacts secrets from logs.” Verify TLS configuration, authorization tests, and log inspection.
- **User validation:** “Every protected API operation validates the authentication context and performs server-side authorization for the requested action and resource.” Verify unauthenticated, wrong-role, and cross-user negative tests.

Set numerical thresholds and implementation specifics according to system requirements and abuse analysis rather than copying arbitrary values.

## Exercise 7 — Threat-model change review

New risks include link leakage through messages, browser history, referrer headers, analytics, screenshots, or logs; unauthorized forwarding; links remaining valid too long; and weak revocation behavior.

Possible controls:
- Private-by-default sharing
- High-entropy, scoped tokens
- Explicit expiry and revocation
- Least-privilege access to the shared object
- Avoid putting sensitive information in URLs
- Appropriate cache and referrer policies
- Audit creation, use, and revocation
- Rate limits and abuse monitoring
- Clear user experience explaining link permissions

Reassess authentication assumptions, authorization logic, logging, data exposure, incident response, and privacy requirements. Before release, test unauthorized access, expiry, revocation, forwarding, access logging, and cache behavior; obtain the required product, security, privacy, and risk approvals.

## Exercise 8 — Mini threat-model deliverable

A strong submission does not need a large diagram. It should show a clear scope, realistic trust boundaries, concrete threat scenarios, defensible risk reasoning, specific controls, validation tests, owners, and remaining uncertainties. A reviewer should be able to trace each important threat to a mitigation and evidence that the mitigation works.

## Further reading

- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [OWASP Threat Modeling Project](https://owasp.org/www-project-threat-model/)
- [Microsoft Threat Modeling Tool — getting started](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-getting-started)
- [Microsoft SDL threat modeling](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
