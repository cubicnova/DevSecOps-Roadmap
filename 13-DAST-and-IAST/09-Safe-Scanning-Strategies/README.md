# 09 - Safe Scanning Strategies

## Learning objectives
By the end of this module, learners should be able to:
- Select a safe DAST approach based on authorization, environment, and business impact.
- Distinguish passive scanning, crawling, active scanning, fuzzing, and manual testing.
- Use ZAP Safe and Protected modes appropriately.
- Define scope, exclusions, scan windows, rate limits, and stop conditions.
- Reduce operational risk from destructive requests, external integrations, and shared data.
- Plan staged scans with monitoring, rollback, and cleanup.
- Document residual risk and communicate scan safety decisions.

## 1. Why safe scanning matters
A DAST scanner interacts with a running application. Discovery and testing can generate many requests, submit forms, follow links, and send attack payloads. Depending on application behavior, this may create records, trigger emails, modify data, invalidate sessions, or affect availability.

A safe strategy is not simply “use fewer requests.” It is a documented plan that ensures the tester is authorized, the target is correct, the scan is proportionate, and unexpected behavior can be stopped and recovered.

## 2. Understand the activity risk

| Activity | Typical behavior | Risk considerations |
|---|---|---|
| Passive analysis | Reviews traffic already observed | Usually low impact; reports may contain sensitive data |
| Traditional spider | Follows links and may submit forms depending on settings | Can trigger application workflows |
| AJAX/browser spider | Drives a browser through client-side behavior | May interact with state-changing UI controls |
| Active scan | Sends attack payloads | Can create, modify, or delete data; may affect availability |
| Fuzzing | Sends many altered inputs | Can cause load, errors, or unexpected state changes |
| Manual validation | Human-controlled reproduction | Still requires authorization and safe test data |

Do not treat crawling as automatically harmless. Review the application's links, forms, and state-changing operations before discovery.

## 3. Authorization and rules of engagement
Before testing anything beyond your own local lab:
- Obtain written authorization from the system owner.
- Identify the exact hostnames, IP ranges, ports, paths, and APIs in scope.
- Define allowed techniques, scan dates, time zone, request rate, and concurrency.
- Name technical contacts and an emergency stop contact.
- Agree on data handling, report recipients, and retention.
- Define prohibited actions, including denial-of-service, destructive operations, and testing third-party integrations unless explicitly approved.

Authorization for one hostname or environment does not automatically authorize sibling domains, production, cloud accounts, or third-party services.

## 4. Choose the right ZAP mode
ZAP provides modes with different restrictions:
- **Safe:** prevents potentially dangerous operations.
- **Protected:** allows potentially dangerous operations only for URLs in scope.
- **Standard:** does not impose those restrictions.
- **Attack:** actively scans in-scope nodes as they are discovered.

For controlled assessments, Protected mode is a useful guardrail after carefully defining scope. Safe mode is useful when you want to avoid potentially dangerous operations. Neither mode replaces authorization, application-specific exclusions, monitoring, or good judgment.

## 5. Passive-first strategy
A conservative sequence:
1. Validate the target and authorization.
2. Configure a narrow Context and scope.
3. Set ZAP to Safe mode for initial inspection.
4. Browse representative pages and review passive alerts.
5. Assess whether spidering is safe for the application's workflows.
6. Review coverage and authentication.
7. Plan any active scan separately with explicit approval.

Passive analysis does not inject attack payloads and does not change requests/responses. However, crawling still sends requests, and storing traffic/report data can create privacy and confidentiality risks.

## 6. Control destructive behavior
Identify routes and controls that may:
- Log out a user or invalidate a session.
- Delete accounts, records, or files.
- Submit payments, orders, or refunds.
- Send email, SMS, or push notifications.
- Publish content or invite users.
- Trigger external webhooks, cloud functions, or third-party APIs.
- Modify shared tenant or customer data.

Use dedicated test accounts, synthetic records, and narrow exclusions. Prefer disabling external integrations in a test environment. Exclusions should be specific and documented; broad exclusions can hide real attack surface.

## 7. Rate limits and resource controls
Set a conservative initial request rate and concurrency. Bound:
- Total scan duration.
- Per-rule duration.
- Concurrent hosts and threads.
- Crawl depth and duration.
- Requests per second where supported.
- Retry behavior and timeouts.

Monitor application health, latency, error rates, CPU/memory, database load, queue depth, and external service activity. Increase intensity only when the environment owner approves and monitoring shows the target can tolerate it.

## 8. Staged scan plan
A practical staged approach:

| Stage | Activity | Gate to proceed |
|---|---|---|
| 0 | Authorization and scope review | Written approval |
| 1 | Reachability and passive observation | Correct target and no unexpected traffic |
| 2 | Limited crawl | State-changing routes controlled |
| 3 | Authenticated discovery | Test identity and session verification |
| 4 | Targeted active tests | Isolated target, policy approved |
| 5 | Broader active scan | Monitoring, rate limits, rollback ready |
| 6 | Retest and cleanup | Findings recorded, credentials revoked |

Do not jump directly to a high-strength full scan because a previous scan completed quickly.

## 9. Stop conditions and incident response
Stop the scan immediately if:
- The target is outside the approved scope.
- Application health or availability degrades beyond agreed thresholds.
- Unexpected data changes or external messages occur.
- Scanner traffic reaches a third-party or production system.
- Authentication behaves unexpectedly or a privileged account is used unintentionally.
- The owner or incident contact requests a stop.

Record the time, scan ID, target, last action, observed impact, and steps taken. Notify the owner and follow the agreed incident process. Do not attempt unapproved cleanup or data restoration.

## 10. Recovery and cleanup
Before scanning:
- Snapshot or seed disposable test data.
- Confirm backup and rollback procedures.
- Disable or sandbox outbound integrations.
- Prepare a test reset procedure.
- Record emergency contacts.

After scanning:
- Stop remaining jobs and verify no scanner process continues.
- Reset synthetic data if required.
- Revoke temporary credentials and tokens.
- Remove ephemeral environments.
- Securely retain or delete reports according to policy.
- Record deviations, incidents, and lessons learned.

## 11. Example ZAP safety configuration
A local lab can be started in Safe mode from the ZAP UI or command line. The exact command-line options depend on the installed ZAP version; consult current documentation.

For a scoped assessment, Protected mode restricts potentially dangerous actions to URLs in scope. Define and test Context include/exclude patterns before changing to Protected mode.

A sample planning record is provided in `templates/rules-of-engagement.md`. This is a documentation template, not an executable ZAP configuration file.

## 12. What automation cannot guarantee
Automated DAST cannot reliably identify every business-logic flaw, chained exploit, authorization weakness, or workflow abuse. ZAP's own documentation notes that active scanning finds only certain vulnerability types; manual penetration testing is still needed.

A safe scan report should state:
- What was tested and what was not.
- Which roles and workflows were covered.
- Scan mode, rules, intensity, and limits.
- Any exclusions or interruptions.
- Application health during testing.
- Findings requiring manual validation.
- Residual risk and recommended next steps.

## Knowledge check
1. Why can spidering create risk even without active scan payloads?
2. What is the difference between Safe and Protected mode?
3. Why is authorization for staging not authorization for production?
4. Name five conditions that should stop a scan.
5. Why should outbound integrations be disabled or sandboxed?
6. Why does a clean DAST report not prove that business logic is secure?

## Further reading
- ZAP Modes: https://www.zaproxy.org/docs/desktop/start/features/modes/
- ZAP Scan Policy: https://www.zaproxy.org/docs/desktop/start/features/scanpolicy/
- ZAP FAQ - scanning risks: https://www.zaproxy.org/faq/
- ZAP API and scan controls: https://www.zaproxy.org/docs/api/
- OWASP DevSecOps DAST Guideline: https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-2-Dynamic-Application-Security-Testing/
