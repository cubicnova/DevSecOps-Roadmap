# Risk Assessment Examples

All ratings below are fictional examples using the illustrative 5 × 5 matrix in `README.md`. Adapt ratings and thresholds to the organization's approved policy.

## Example 1 — Broken object-level authorization in an invoice API
**Scenario:** An authenticated customer changes an invoice ID and receives another customer's invoice because the API does not verify object ownership.

- Asset: invoices and customer personal data
- Threat event: authenticated user enumerates invoice identifiers
- Weakness: missing server-side object-level authorization
- Existing controls: authentication is required, but authorization testing is incomplete
- Likelihood: 4 — Likely
- Impact: 4 — Major
- Score: 4 × 4 = 16 (High under the example bands)
- Treatment: mitigate
- Actions: enforce authorization on every object access; add negative authorization tests; review logs for prior access; retest affected endpoints
- Residual rating: determine only after the controls are implemented and verified

## Example 2 — Public object storage
**Scenario:** A storage bucket containing internal reports is publicly readable due to a misconfiguration.

- Asset: internal reports and potentially confidential data
- Likelihood: 3 — Possible, based on current exposure and discoverability
- Impact: 4 — Major, assuming the reports contain sensitive business data
- Score: 12 (High)
- Treatment: mitigate
- Actions: remove public access, apply least-privilege policy, scan for other exposed stores, enable configuration monitoring, and assess whether data was accessed
- Evidence: effective access policy, exposure test, and monitoring results

## Example 3 — Denial of service against a public API
**Scenario:** An unauthenticated endpoint allows expensive queries and has no effective rate limiting.

- Asset: API availability and dependent business operations
- Likelihood: 4 — Likely
- Impact: 3 — Moderate
- Score: 12 (High)
- Treatment: mitigate
- Actions: add request limits, timeouts, query-cost limits, capacity protections, and alerting; test graceful degradation
- Residual risk depends on service criticality, abuse patterns, and verified protections.

## Example 4 — Stolen developer credentials
**Scenario:** A developer account without phishing-resistant MFA is compromised and used to change a production deployment.

- Asset: source code, CI/CD pipeline, production environment
- Likelihood: 3 — Possible
- Impact: 5 — Severe
- Score: 15 (High)
- Treatment: mitigate
- Actions: enforce strong MFA, short-lived credentials, least privilege, protected branches, peer review, and deployment audit trails; test account recovery and emergency access.

## Example 5 — Unsupported dependency in an internal tool
**Scenario:** An unmaintained library contains a known exploitable vulnerability, but the application is reachable only by a small group.

- Asset: internal tool and connected data
- Likelihood: 2 — Unlikely (assumption: restricted access and no known exploitation path)
- Impact: 3 — Moderate
- Score: 6 (Medium)
- Treatment: mitigate or time-bound acceptance while upgrading is scheduled
- Actions: verify reachability and exploitability, identify a maintained replacement, isolate where appropriate, and set an upgrade deadline.
- Note: “internal” does not mean safe. Re-rate if the service is reachable through compromised accounts or adjacent systems.

## Example 6 — Residual risk after remediation
Initial scenario: missing authorization on a sensitive endpoint.
- Inherent likelihood: 4
- Inherent impact: 4
- Inherent score: 16
- Control: server-side ownership checks, centralized authorization, automated negative tests, and security regression testing
- Verification: code review, test evidence, and retest against representative roles and object IDs
- Illustrative residual likelihood: 2
- Residual impact: 4
- Residual score: 8 (Medium)

Impact may remain high even when likelihood is reduced. Do not lower impact just because a control was implemented; reassess each dimension based on evidence.

## Example 7 — Risk acceptance
A service owner requests a temporary exception for a medium-risk issue while a vendor patch is pending.

A defensible acceptance record should include:
- Exact risk scenario and affected systems
- Business rationale and alternatives considered
- Existing compensating controls
- Potential impact and uncertainty
- Named authorized approver
- Expiry date and remediation milestone
- Monitoring or trigger that forces earlier reassessment

Acceptance should not be used to bypass mandatory legal, contractual, or safety requirements.
