# Threat Modeling Examples

These examples demonstrate how to turn architecture details into concrete threat scenarios and testable mitigations. The systems are illustrative.

## Example 1: Online store checkout

### Scope and assets

- Customer account and session
- Address and order data
- Payment-provider integration
- Inventory and order status
- Service availability

### Simplified data flow

```text
Customer Browser --HTTPS--> Store API --query/update--> Order Database
                                  |
                                  +--payment request--> Payment Provider
```

Trust boundaries exist between the browser and API, the application and database, and the store and payment provider.

### Threat register

| ID | Scenario | STRIDE | Impact | Mitigation | Validation |
|---|---|---|---|---|---|
| TM-01 | A customer changes an order ID and views another customer's order | Elevation of privilege / Information disclosure | High | Enforce server-side object-level authorization | Test access using two separate test accounts |
| TM-02 | A client changes the submitted price | Tampering | High | Calculate price and discounts server-side from trusted catalog data | Submit modified prices in a test environment |
| TM-03 | Repeated checkout requests create duplicate orders | Tampering / Availability | Medium–High | Use idempotency keys and transaction-safe order creation | Replay the same test request |
| TM-04 | Payment callback is forged | Spoofing / Tampering | High | Verify provider signatures and transaction state; reject untrusted callback fields | Test invalid signatures and replayed callbacks |
| TM-05 | Error messages expose internal details | Information disclosure | Medium | Return generic client errors and log details securely server-side | Trigger controlled invalid requests |

### Design questions

- Is the order owner derived from the authenticated server-side identity?
- Is the payment callback authenticated independently of the browser?
- Can a retry safely repeat a checkout operation?
- Which actions need audit events?

## Example 2: Internal employee portal

### Assets and actors

Assets: employee records, payroll data, access tokens, audit logs.
Actors: employee, HR administrator, identity provider, portal service, database.

| Threat | STRIDE | Candidate control |
|---|---|---|
| Attacker reuses a stolen session token | Spoofing | Secure session handling, short appropriate session lifetime, revocation, MFA for sensitive actions |
| Employee changes a payroll field through a crafted request | Tampering / Elevation of privilege | Server-side authorization and field-level validation |
| Administrator denies changing a salary | Repudiation | Protected audit trail with actor, timestamp, target, and outcome |
| Portal reveals payroll records through search results | Information disclosure | Enforce authorization before returning search results; minimize response fields |
| Expensive search exhausts the database | Denial of service | Query limits, pagination, rate limits, timeouts, monitoring |

A control should be tied to a specific threat and verified with a test. “Improve security” is not a testable mitigation.

## Example 3: STRIDE applied to a login service

| STRIDE | Threat question | Example scenario | Possible mitigation |
|---|---|---|---|
| Spoofing | Can an attacker impersonate a user? | Stolen session cookie is reused | Secure cookie attributes, session rotation, revocation |
| Tampering | Can authentication state be changed? | Client-supplied role is trusted | Keep authorization decisions server-side |
| Repudiation | Can a sensitive login or reset action be denied? | No record of password reset | Record appropriately protected security events |
| Information disclosure | Can credentials or recovery tokens leak? | Token appears in application logs | Redact secrets; use secure token delivery and storage |
| Denial of service | Can login capacity be exhausted? | High-volume login attempts consume resources | Rate limits, progressive defenses, capacity controls |
| Elevation of privilege | Can a basic account gain admin access? | API trusts a role field in request JSON | Check permissions on every privileged server-side operation |

STRIDE categories can overlap. Record the core scenario clearly, and avoid duplicating one scenario merely to fill every row.

## Example 4: Build a data-flow diagram (DFD)

For a document-sharing service, identify:

- External entities: uploader, recipient, identity provider
- Processes: web/API service, malware scanning worker
- Data stores: object storage, metadata database
- Flows: upload, scan result, sharing link, download
- Trust boundaries: internet-to-service, service-to-storage, worker-to-queue

A diagram should show enough detail to support threat discovery, not every implementation detail. Mark sensitive flows and privileged interfaces.

## Example 5: Threat record template

```text
ID: TM-006
Title: Unauthorized access to another user's document
Component / flow: Download API -> Object Storage
Asset: Confidential document
Threat category: Elevation of privilege / Information disclosure
Preconditions: Attacker has a valid low-privilege account
Scenario: Attacker changes a document identifier and the API fails to verify ownership
Impact: Confidentiality breach; possible contractual or regulatory consequences
Likelihood: 4/5 (illustrative)
Impact rating: 5/5 (illustrative)
Existing controls: Authenticated sessions
Mitigation: Verify document-level authorization on every read and download
Owner: API team
Validation: Automated cross-user access-control tests
Status: Open
Residual risk / rationale: Reassess after validation
```

## Example 6: Risk response choices

- **Mitigate:** Add object-level authorization and tests.
- **Eliminate:** Remove public sharing if the product does not need it.
- **Transfer:** Use contractual arrangements to allocate certain responsibilities, while retaining oversight of the remaining risk.
- **Accept:** A named risk owner documents the rationale, expiry/review date, and residual risk according to policy.

Acceptance is not the same as ignoring a threat. Follow organizational approval requirements.
