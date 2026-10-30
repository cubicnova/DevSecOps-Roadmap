# STRIDE Examples

These examples are illustrative. Confirm applicability against the real architecture, trust boundaries, attacker capabilities, and business impact.

## 1. Spoofing — fake identity

**Scenario:** An API trusts a client-supplied `user_id` header without verifying it against the authenticated principal. An attacker changes the header to impersonate another user.

**Potential impact:** Unauthorized access or actions attributed to the wrong identity.

**Mitigations:**
- Derive identity from a validated authentication context, not arbitrary client fields.
- Validate token signature, issuer, audience, expiry, and relevant claims.
- Use strong service-to-service authentication where required.
- Test with separate accounts and forged identity fields.

## 2. Tampering — unauthorized modification

**Scenario:** A client changes an order's price or role field in a request, and the server accepts the value without authoritative validation.

**Potential impact:** Fraud, data-integrity loss, or privilege changes.

**Mitigations:**
- Calculate prices and sensitive business values on the server.
- Enforce server-side authorization and schema validation.
- Use integrity protection for relevant inter-service messages.
- Test altered parameters, fields, and replayed requests.

## 3. Repudiation — insufficient evidence

**Scenario:** An administrator changes permissions, but the application records neither the actor nor the target or outcome.

**Potential impact:** Investigators cannot reliably reconstruct the action or determine accountability.

**Mitigations:**
- Record relevant actor, target, action, outcome, timestamp, and correlation ID.
- Protect logs against unauthorized alteration and deletion.
- Synchronize clocks and restrict log access.
- Test that the event is emitted and reaches the central collector.

Logs support accountability but do not automatically provide legal non-repudiation.

## 4. Information Disclosure — sensitive data leak

**Scenario:** An API returns full customer records when a user only needs a limited profile, or verbose errors expose internal paths and tokens.

**Potential impact:** Privacy breach, credential compromise, or exposure of business-sensitive information.

**Mitigations:**
- Enforce object- and field-level authorization.
- Minimize returned data and redact secrets from errors and logs.
- Protect data in transit and at rest according to approved requirements.
- Test unauthorized access and inspect error responses.

## 5. Denial of Service — resource exhaustion

**Scenario:** An unauthenticated endpoint performs expensive searches with no request, concurrency, or query limits.

**Potential impact:** Service degradation, increased cost, or outage for legitimate users.

**Mitigations:**
- Set request/body limits, rate limits, timeouts, and concurrency controls.
- Apply pagination and bounded query complexity.
- Use capacity monitoring and graceful degradation.
- Load-test within an authorized environment and verify limits.

## 6. Elevation of Privilege — gaining excessive authority

**Scenario:** A standard user can call an administrator endpoint because the endpoint checks authentication but not the user's role or permission.

**Potential impact:** Unauthorized administrative actions or broader compromise.

**Mitigations:**
- Enforce server-side authorization for every privileged action.
- Apply least privilege and separation of duties.
- Test direct endpoint access with low-privilege accounts.
- Alert on unusual role changes and privileged actions.

## Worked example: customer portal

**System scope:** Customers view invoices; support staff can help customers; an API accesses a database; security events go to a central log service.

| ID | STRIDE | Threat scenario | Candidate mitigation | Verification |
|---|---|---|---|---|
| TM-01 | Spoofing | Forged or stolen session used as another customer | Secure session lifecycle, MFA where appropriate, re-authentication for sensitive actions | Session and authentication tests |
| TM-02 | Tampering | Invoice ID or amount changed in a request | Server-side business rules and input validation | Negative API tests |
| TM-03 | Repudiation | Support agent denies viewing a customer record | Protected audit event with actor, target, action, outcome | Integration test and log review |
| TM-04 | Information Disclosure | Customer retrieves another customer's invoice | Object-level authorization and data minimization | Two-account access tests |
| TM-05 | Denial of Service | Repeated expensive report requests exhaust capacity | Rate limits, query bounds, timeouts, monitoring | Controlled load test |
| TM-06 | Elevation of Privilege | Customer invokes support-only endpoint | Server-side role/permission checks | Low-privilege negative tests |

## Distinguish related categories

- **Spoofing vs. Elevation of Privilege:** spoofing is pretending to be another identity; elevation is obtaining authority beyond what the current identity should have.
- **Tampering vs. Information Disclosure:** tampering violates integrity; disclosure violates confidentiality. One scenario can involve both.
- **Repudiation vs. Logging generally:** a log record is useful only if its source, integrity, context, and access are trustworthy.
- **Denial of Service vs. normal load:** assess whether a plausible actor can exhaust a constrained resource and affect legitimate availability.

## Risk notes

Do not assign severity from the STRIDE label alone. Consider exploitability, exposure, affected assets, impact, existing controls, and uncertainty using the team's documented risk method.
