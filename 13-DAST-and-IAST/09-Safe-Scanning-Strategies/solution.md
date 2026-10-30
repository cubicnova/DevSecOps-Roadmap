# Safe Scanning Strategies - Solutions and Guidance

## Exercise 1 - Risk classification
A typical relative classification:
- Passive analysis of manually browsed traffic: lower operational risk, but reports may expose sensitive data.
- Traditional spidering: moderate risk because it follows links and may submit forms depending on configuration.
- AJAX/browser spidering: moderate risk because it can interact with client-side workflows.
- Active scan: higher risk because it sends attack payloads.
- Fuzzing file upload: higher risk due to storage, processing, and resource impacts.
- Account deletion: high impact and should be excluded unless specifically authorized and safely simulated.

The application's workflow, data sensitivity, external integrations, and environment can change these ratings.

## Exercise 2 - Rules of engagement
A complete record identifies the owner, authorization reference, exact targets, allowed techniques, prohibited actions, scan window, rate/concurrency limits, contacts, report handling, and stop conditions. Scope must be explicit and unambiguous.

## Exercise 3 - Safe mode
Safe mode prevents potentially dangerous operations. It is useful for low-risk exploration, but it does not prove that the target is authorized or that all remaining traffic is harmless. Review application behavior and data handling.

## Exercise 4 - Protected mode
Protected mode permits potentially dangerous operations only for URLs in scope. It relies on accurate Context patterns. Test the patterns with in-scope and out-of-scope URLs before scanning. A broad or incorrect pattern can defeat the intended boundary.

## Exercise 5 - State-changing routes
Common candidates include logout, account deletion, user invitations, password reset, payment, refunds, file uploads, content publishing, and administrative mutations. Exclude or sandbox them as appropriate. Avoid broad exclusions that hide unrelated read-only functionality.

## Exercise 6 - Passive-first assessment
Passive scanning analyzes observed requests/responses without injecting attack payloads. The crawler still sends requests and may trigger application behavior. Record coverage and side effects. Passive scanning cannot reliably detect issues that require malicious payloads or complex business-logic reasoning.

## Exercise 7 - Rate and resource limits
A good plan starts with low concurrency and a short bounded duration, then increases only with approval and monitoring. Record request rate, timeout, crawl depth, maximum scan duration, error rate, latency, and system resource thresholds. Choose actual values based on a measured baseline, not generic defaults.

## Exercise 8 - Stop-condition drill
On a stop condition:
1. Stop the scan through the supported ZAP UI/API control.
2. Confirm no scan remains active.
3. Record timestamp, target, scan ID, last action, and impact.
4. Notify the designated owner and incident contact.
5. Preserve logs and evidence securely.
6. Follow the approved recovery plan; do not restore data without authorization.

## Exercise 9 - External integration safety
Use sandbox credentials and endpoints, disable outbound production integrations, route email to a test mail sink, use payment-provider test mode, and block unnecessary egress at the network layer. Verify the controls before scanning.

## Exercise 10 - Staged scan strategy
Proceed only when each gate is satisfied:
- Authorization and scope approved.
- Passive baseline completes without unexpected impact.
- Crawl coverage and exclusions reviewed.
- Authentication and test identities validated.
- Active policy and rate limits approved.
- Monitoring and rollback confirmed.
- Findings triaged and cleanup completed.

## Exercise 11 - Recovery and cleanup
The application owner or designated operations team should approve restoration. Revoke temporary accounts/tokens, stop scanner processes, remove ephemeral environments, reset synthetic data, and store/delete reports according to retention policy.

## Exercise 12 - Final assessment checklist
The final strategy should show that safety is engineered into the process: authorization, scope, safe mode, staged scanning, monitoring, stop conditions, recovery, and residual-risk communication. A clean scan must not be represented as proof that the application has no vulnerabilities.

## Sample conclusion
> The assessment used a documented rules-of-engagement record and a narrowly scoped staging Context. Testing began with Safe mode and passive analysis, followed by a limited crawl after state-changing routes were reviewed. Active scanning was separately approved for an isolated target with conservative limits and monitoring. Stop conditions, incident contacts, and recovery steps were defined in advance. Results are limited to the tested roles, routes, and scan techniques; manual testing remains necessary for business-logic and other coverage gaps.
