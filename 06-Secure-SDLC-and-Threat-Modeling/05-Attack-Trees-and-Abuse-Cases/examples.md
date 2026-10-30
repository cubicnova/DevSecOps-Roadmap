# Attack Trees and Abuse Cases — Examples

All systems and scenarios below are fictional. Each example focuses on how to move from an attacker goal to actionable controls and tests.

## Example 1 — Attack tree for unauthorized invoice access

**Root goal:** Read an invoice that belongs to another customer.

```text
Read another customer's invoice
|
+-- OR: Abuse the API
|   +-- Obtain a valid low-privilege account
|   +-- Submit a different invoice identifier
|   +-- Succeed if the API omits ownership authorization
|
+-- OR: Abuse a sharing feature
|   +-- Obtain a link
|   +-- Access it outside the intended scope or after it should expire
|
+-- OR: Reuse an authorized session
    +-- Obtain a session token through a separate compromise
    +-- Use the session while it remains valid
```

### Analysis

| Path | Key prerequisite | Defensive control | Validation |
|---|---|---|---|
| API authorization | API accepts a caller-controlled invoice ID | Check invoice ownership or explicit permission on every request | Cross-account negative tests |
| Sharing link | Link can be obtained and remains valid | High-entropy scoped token, expiry, revocation, careful handling in logs and referrers | Test expiry, revocation, and scope |
| Session reuse | A valid session token is exposed | Secure session handling, appropriate expiry, revocation, reauthentication for sensitive actions | Verify revoked sessions cannot access protected invoices |

A random invoice ID can reduce guessing but cannot replace authorization checks.

## Example 2 — Abuse case: password-reset endpoint

**ID:** AC-AUTH-01  
**Feature:** Account recovery  
**Legitimate actor:** Account owner  
**Potential abuser:** Unauthenticated remote actor

**Legitimate flow**
1. User requests a password-reset link.
2. Service responds without unnecessarily disclosing account existence.
3. Service sends a single-use reset token through the configured recovery channel.
4. User sets a new password.
5. Service invalidates the used token and follows its session-revocation policy.

**Abuse scenario**
1. Actor submits many reset requests.
2. Requests consume service resources or flood a victim's recovery channel.
3. If responses differ by account existence, the actor may infer which accounts are registered.

**Impact:** Availability disruption, user harassment, account enumeration, and possible recovery-workflow compromise if token controls are weak.

**Controls**
- Apply rate limits and abuse monitoring.
- Keep responses consistent where practical.
- Use unpredictable, time-limited, single-use reset tokens.
- Avoid placing reset tokens in analytics, logs, or third-party referrers.
- Notify users appropriately without revealing sensitive account state to the requester.

**Tests**
- Compare responses for existing and nonexistent test accounts.
- Verify throttling behavior with a controlled request rate.
- Verify expired and previously used tokens are rejected.
- Inspect application logs to confirm tokens are not recorded.

## Example 3 — Abuse case: discount and checkout workflow

**Legitimate use case:** A customer applies a valid discount and completes an order.

**Abuse case:** A customer attempts to manipulate the checkout process to receive an unintended price or create inconsistent order state.

| Step / failure mode | Risk | Requirement | Test |
|---|---|---|---|
| Client submits a modified item price | Revenue loss, data integrity | Server calculates prices from trusted catalog and promotion data | Send a modified price in a test request |
| Discount is applied repeatedly | Unauthorized discount | Enforce promotion eligibility, limits, and atomic redemption | Attempt repeated redemption with test accounts |
| Client repeats a checkout request | Duplicate orders or charges | Use idempotent order creation and safe payment-state transitions | Replay the same test request |
| Forged payment status is accepted | Fraud, incorrect fulfillment | Verify provider events and reconcile trusted transaction state | Submit an invalid-signature test event |

**Risk note:** Apply controls to the actual business rules. A rate limit alone does not fix incorrect price calculation or duplicate-order logic.

## Example 4 — Attack tree for privileged account takeover

**Root goal:** Perform an administrative action without proper authorization.

```text
Perform an unauthorized administrative action
|
+-- OR: Abuse identity or session controls
|   +-- Reuse a compromised administrator session
|   +-- Session remains active after required revocation
|
+-- OR: Abuse authorization logic
|   +-- Call an admin API as a normal user
|   +-- Server trusts a client-supplied role or permission
|
+-- OR: Abuse recovery or approval workflow
    +-- Trigger a weak recovery path
    +-- Bypass a required second-person approval
```

**Mitigations:** Server-side permission checks, least privilege, secure session management, MFA for privileged access, protected recovery workflows, approval enforcement, and audit monitoring.

**Validation:** Use test identities for each role; attempt forbidden admin operations; test session revocation; verify recovery and approval requirements cannot be skipped.

## Example 5 — AND versus OR logic

Suppose an attacker goal is “use a private share link after revocation.”

```text
Access object using a revoked link
AND
+-- Possess the old link
+-- Revocation is not enforced by the download service
```

Both conditions are required for this particular path, so it is an AND relationship. A separate path might be “access the object through an authorized account with permission,” which is an alternative OR branch.

Be explicit about the logic. If the tree is ambiguous, reviewers may misunderstand what a mitigation must prevent.

## Example 6 — Convert an abuse case into a user story

**Security user story**

As the owner of a private document, I want the service to authorize every download against the authenticated identity and document permissions so that changing an object identifier does not expose another user's data.

**Acceptance criteria**
- An authenticated owner can download their own permitted document.
- A different user cannot download the document without explicit permission.
- Unauthenticated requests cannot download private documents.
- Authorization is enforced server-side on every request.
- Automated tests cover allowed, denied, and revoked-access cases.
- Logs record the result without storing document contents or session secrets.

## Example 7 — Abuse-case register

| ID | Feature | Abuse scenario | Priority rationale | Owner | Status |
|---|---|---|---|---|---|
| AC-01 | Password reset | Repeated requests flood a user's recovery channel | High user impact; public endpoint | Identity team | Open |
| AC-02 | File sharing | Revoked link still grants access | Confidentiality impact; control failure | API team | In progress |
| AC-03 | Checkout | Client-controlled price is accepted | Direct financial impact | Commerce team | Open |
| AC-04 | Admin portal | Normal user invokes privileged endpoint | High privilege and business impact | Platform team | Open |

Priority and status are illustrative. A real register should include evidence, due dates, risk decisions, and links to implementation issues.
