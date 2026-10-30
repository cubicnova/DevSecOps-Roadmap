# 05 - Scan Configuration

## Learning objectives
By the end of this module, learners will be able to:
- Define scan scope, context, exclusions, and target boundaries.
- Configure passive and active scan behavior for an authorized environment.
- Explain scan policy thresholds, strength, rule status, and technology selection.
- Tune crawling, request limits, timeouts, and scan duration.
- Design separate baseline, API, and active scan profiles.
- Version-control scan configuration and document exceptions.
- Interpret coverage, performance, and false-positive trade-offs.

## 1. Why scan configuration matters
A scanner's output depends on what it can reach, which requests it sends, which rules are enabled, and how aggressively those rules run. A scan that is too broad can affect unrelated systems; one that is too restrictive may miss important behavior. A good configuration is explicit, reviewable, repeatable, and appropriate to the environment.

## 2. Configuration building blocks

| Building block | Purpose | Example |
|---|---|---|
| Target | Application being assessed | `http://127.0.0.1:8080` |
| Context / scope | URLs considered part of the application | Approved host and paths |
| Include/exclude rules | Boundaries inside the context | Include `/app/.*`, exclude `/logout` |
| Scan policy | Rules and their settings | Selected active rules |
| Threshold | Likelihood required to raise an alert | Higher threshold reduces noise |
| Strength | Amount of testing per rule | Low, Medium, High |
| Technology | Technologies believed to be present | Java, PHP, JavaScript |
| Crawl settings | How the app is explored | Depth, duration, browser spider |
| Resource limits | Bound scan impact | Duration, concurrency, request rate |
| Authentication | Identity used during discovery/testing | Dedicated test user |

## 3. Scope and Context
A ZAP Context groups URLs belonging to an application. Context include/exclude patterns are regular expressions that match the whole URL, so validate them against representative URLs before scanning.

Example scope pattern for a local lab:
```regex
^http://127\.0\.0\.1:8080/.*$
```

Do not add a broad wildcard that can include unrelated hosts. Define explicit exclusions for logout, account deletion, payment, email dispatch, destructive administrative actions, and external integrations unless the test plan explicitly authorizes them.

## 4. Passive versus active configuration
- **Passive scanning** analyzes requests and responses observed during browsing/crawling. It is generally safer but can still generate load and sensitive reports.
- **Active scanning** sends attack payloads and may change data, trigger workflows, or affect availability. It is an attack against the target and must only be used on systems you own or are explicitly authorized to test.

Recommended progression:
1. Validate scope and reachability.
2. Run a passive baseline.
3. Review coverage and findings.
4. Configure a bounded active policy in an isolated test environment.
5. Retest and compare results.

## 5. Scan policy: threshold and strength
A scan policy controls which active rules run and how they behave.

### Threshold
Controls how likely a rule is to report a potential issue:
- Lower threshold: more potential alerts, potentially more false positives.
- Higher threshold: fewer alerts, but some real issues may be missed.
- Off: rule is not run.

### Strength
Controls how much testing a rule performs:
- Low: fewer requests, faster, potentially less coverage.
- Medium: balanced starting point for many test labs.
- High: more requests and time, potentially more findings.
- Insane: can generate a very large number of attacks; reserve for small, carefully controlled areas.

Do not assume the same threshold/strength is appropriate for every application. Record the rationale for changes.

## 6. Scanner rules and add-ons
ZAP rules are provided by add-ons and can have different statuses, such as Release, Beta, or Alpha. Rule availability can change as add-ons are updated. Before comparing scans, record the ZAP version, add-on versions, enabled rules, and policy settings.

A locked policy can prevent additional/new rules from being used inadvertently. This improves repeatability, but it also means policy updates must be deliberate and reviewed.

## 7. Crawl configuration
Crawl coverage depends on:
- Traditional spider and AJAX/browser spider selection.
- Authentication and session verification.
- Application state and workflow sequence.
- Crawl depth, duration, and maximum children.
- JavaScript routing and dynamically loaded content.
- API definition imports and recorded workflows.

A crawler's discovered URL count is not proof that every endpoint or business rule was tested.

## 8. Performance and safety controls
Set and document:
- Maximum scan duration.
- Maximum duration per rule.
- Maximum concurrent hosts.
- Request rate or delay where supported.
- Crawl depth and time limits.
- Excluded destructive endpoints.
- Stop conditions and monitoring.
- Cleanup and test-data reset procedure.

Start conservatively and tune based on the isolated lab's observed behavior. Do not increase concurrency or strength to compensate for poor scope or missing authentication.

## 9. Example ZAP Automation Framework plan
This is an illustrative passive-first plan. Automation Framework job names and schema can evolve; validate it against the installed ZAP release and add-ons before use.

```yaml
env:
  contexts:
    - name: local-training-app
      urls:
        - http://127.0.0.1:8080
      includePaths:
        - "http://127\\.0\\.0\\.1:8080/.*"
      excludePaths:
        - "http://127\\.0\\.0\\.1:8080/logout.*"
        - "http://127\\.0\\.0\\.1:8080/admin/delete.*"

jobs:
  - type: spider
    parameters:
      context: local-training-app
      maxDuration: 2

  - type: passiveScan-wait
    parameters:
      maxDuration: 2

  - type: report
    parameters:
      template: traditional-html
      reportDir: /zap/wrk
      reportFile: dast-baseline.html
```
The example intentionally does not start an active scan. Review the current Automation Framework documentation for exact job parameters and report template availability.

## 10. Version-control and governance
Store configuration in the repository, for example:
```text
.zap/
  plan.yaml
  README.md
  policies/
    baseline-policy-notes.md
  exclusions/
    exclusions.md
```
Use pull requests to review scope, exclusions, rule changes, and suppression rationale. Never commit real credentials, session cookies, private keys, or production tokens.

## 11. Baseline, API, and active profiles
- **Baseline profile:** passive-only, bounded crawling, suitable for frequent feedback.
- **API profile:** imports OpenAPI/GraphQL definitions and tests only approved API hosts.
- **Active profile:** explicitly approved rules and strength, used against disposable/staging targets.
- **Authenticated profile:** dedicated user(s), session verification, and role-specific coverage.

Keep profiles separate so that a fast pull-request scan does not accidentally inherit a high-impact active policy.

## 12. Common configuration mistakes
- Scope regex does not match the full URL.
- Context includes multiple unrelated hosts.
- Logout or destructive paths are crawled.
- Active scan runs against production without approval.
- Excessive strength/concurrency creates unnecessary load.
- New scanner rules silently alter results between versions.
- Suppressions have no owner, rationale, or expiry.
- Scan passes but crawler never authenticated or reached protected pages.

## Knowledge check
1. What is the difference between scope and scan policy?
2. How do threshold and strength differ?
3. Why should active scanning be isolated and authorized?
4. Why record scanner and add-on versions?
5. What does a locked policy help prevent?
6. Why is URL count not a sufficient coverage metric?

## Further reading
- ZAP Scan Policy: https://www.zaproxy.org/docs/desktop/start/features/scanpolicy/
- ZAP Scanner Rules: https://www.zaproxy.org/docs/desktop/start/checks/
- ZAP Contexts: https://www.zaproxy.org/docs/desktop/start/features/contexts/
- ZAP API: https://www.zaproxy.org/docs/api/
- OWASP DevSecOps DAST: https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-2-Dynamic-Application-Security-Testing/
