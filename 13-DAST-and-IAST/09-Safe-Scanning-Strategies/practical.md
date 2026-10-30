# Safe Scanning Strategies - Practical Exercises

## Lab safety
Use a disposable local application or a target with written authorization. Never test a public or production system merely because it is reachable. Begin with passive analysis and a narrow scope.

## Exercise 1 - Risk classification
Classify each activity as lower, moderate, or higher operational risk for a typical application:
- Passive analysis of manually browsed traffic.
- Traditional spidering.
- AJAX/browser spidering.
- Active scan.
- Fuzzing a file-upload endpoint.
- Testing account deletion.

Explain what application-specific facts could change your classification.

**Deliverable:** Risk assessment table.

## Exercise 2 - Write rules of engagement
Complete `templates/rules-of-engagement.md` for a local training application. Include target, authorization, window, scope, allowed techniques, exclusions, request limits, contacts, and stop conditions.

**Deliverable:** Signed-off rules-of-engagement record (simulated sign-off is acceptable for a lab).

## Exercise 3 - Configure ZAP Safe mode
1. Start ZAP and select Safe mode.
2. Browse a local lab through the proxy.
3. Observe which operations are restricted.
4. Record what Safe mode allows and prevents.
5. Explain why it is not a substitute for authorization.

**Deliverable:** Mode test notes.

## Exercise 4 - Configure Protected mode
1. Create a Context for the local lab.
2. Define a narrow include pattern.
3. Add a test exclusion.
4. Switch to Protected mode.
5. Confirm potentially dangerous operations are limited to in-scope URLs.

**Deliverable:** Context and scope validation evidence.

## Exercise 5 - Identify state-changing routes
Browse the lab and identify routes that can log out, create, update, delete, publish, send notifications, or trigger payments/webhooks.

**Deliverable:** State-changing route inventory with proposed controls.

## Exercise 6 - Passive-first assessment
1. Run a passive baseline against the local lab.
2. Record URLs and passive alerts.
3. Review whether the crawl interacted with state-changing routes.
4. Document any unexpected side effects.
5. Explain what passive analysis cannot detect.

**Deliverable:** Passive scan report and risk notes.

## Exercise 7 - Rate and resource limits
Design conservative limits for a small staging application. Include duration, request rate, concurrency, crawl depth, timeouts, and monitoring thresholds. Justify each setting with an application-owner perspective.

**Deliverable:** Completed `templates/scan-safety-plan.md`.

## Exercise 8 - Stop-condition drill
Simulate one of these conditions in a local lab:
- Health check fails.
- Error rate rises.
- Unexpected test record is deleted.
- Request reaches an out-of-scope hostname.

Write the stop procedure and the notifications that should occur.

**Deliverable:** Stop-event record.

## Exercise 9 - External integration safety
Identify email, SMS, payment, webhook, cloud storage, and third-party API integrations in a sample application. Propose how to sandbox or disable them during DAST.

**Deliverable:** Integration safety matrix.

## Exercise 10 - Staged scan strategy
Design a staged plan from authorization through passive baseline, limited crawl, authenticated discovery, targeted active scan, retest, and cleanup. Define the approval gate between each stage.

**Deliverable:** Staged scan plan.

## Exercise 11 - Recovery and cleanup
Create a checklist for test data reset, credential revocation, environment teardown, report retention, and incident notification. Explain who is authorized to restore data.

**Deliverable:** Cleanup and recovery checklist.

## Exercise 12 - Final assessment
Prepare a safe scanning strategy for an authorized staging application. Include:
- Rules of engagement.
- Scope and exclusions.
- ZAP mode and scan profile.
- Passive-first sequence.
- Active scan approval and limits.
- Monitoring and stop conditions.
- Recovery and cleanup.
- Coverage limitations and residual risk.

### Evaluation rubric (100 points)
| Area | Points |
|---|---:|
| Authorization and rules of engagement | 15 |
| Risk classification | 10 |
| Scope and ZAP mode | 15 |
| State-changing route controls | 15 |
| Rate limits and monitoring | 10 |
| Stop and incident procedure | 15 |
| Recovery and cleanup | 10 |
| Reporting and residual risk | 10 |
