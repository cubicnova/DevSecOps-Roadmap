# 07 - DAST in CI/CD

## Learning objectives
By the end of this module, learners will be able to:
- Explain where DAST fits in a CI/CD pipeline.
- Deploy a disposable test target and wait for application readiness.
- Run an automated passive baseline scan with OWASP ZAP.
- Understand when active and API scans are appropriate.
- Publish and protect scan reports as pipeline artifacts.
- Design security gates using reviewed thresholds and triage rules.
- Secure scanner credentials, runner permissions, and pipeline execution.
- Ensure cleanup occurs even when deployment or scanning fails.

## 1. What is CI/CD DAST?
DAST in CI/CD automatically tests a running application during development or delivery. A typical workflow deploys a preview or staging instance, scans it, evaluates the results, publishes evidence, and tears down temporary resources.

DAST is complementary to SAST, SCA, unit tests, integration tests, and manual penetration testing. A passing scan does not prove that an application is secure; coverage depends on scope, authentication, crawling, API definitions, and scan policy.

## 2. Recommended pipeline stages

1. **Build:** compile/package the application.
2. **Test:** run unit and integration tests.
3. **Deploy preview:** deploy an isolated environment with synthetic data.
4. **Health check:** wait until the target is actually ready.
5. **DAST baseline:** run passive checks and bounded discovery.
6. **Evaluate:** apply a reviewed policy to new or selected findings.
7. **Publish:** upload reports as access-controlled artifacts.
8. **Cleanup:** remove preview resources and revoke temporary credentials.

For a first implementation, start with a passive baseline. Introduce active scanning only in an isolated, explicitly authorized environment.

## 3. ZAP scan options

| Option | Typical use | Behavior |
|---|---|---|
| Baseline scan | Frequent CI feedback | Spider + passive checks; no active attack payloads |
| Full scan | Scheduled/deeper testing | Spider and active scan; can affect target |
| API scan | API-focused testing | Uses OpenAPI/Swagger or GraphQL definition |
| Automation Framework | Custom pipelines | YAML-driven jobs, contexts, auth, scan and reports |

The ZAP baseline scan is designed for CI and runs passive analysis. The full scan includes active testing and should be limited to isolated targets. The Automation Framework is useful when authentication or custom sequencing is required.

## 4. GitHub Actions example
A workflow is provided in `workflows/dast-github-actions.yml`. It demonstrates:
- Starting a local test application with Docker Compose.
- Waiting for a health endpoint.
- Running a ZAP baseline scan.
- Uploading the report.
- Cleaning up with an unconditional step.

The example uses a placeholder ZAP action tag. Before adopting it, check the current official action release and pin the action to a reviewed immutable commit SHA. Do not assume a mutable version tag is a supply-chain control.

## 5. GitLab CI example
`workflows/dast-gitlab-ci.yml` demonstrates a container-based baseline scan and report artifact. Adapt the runner, image, service networking, and target URL to your GitLab environment. Do not copy legacy image names without checking the current ZAP Docker documentation.

## 6. Health checks and networking
A scanner must be able to reach the deployed target from its execution environment. `localhost` inside a container refers to that container, not necessarily the CI host or application container.

Prefer:
- A shared isolated Docker network with service DNS.
- A platform-specific service hostname.
- A verified preview URL.

Use a readiness loop against a health endpoint rather than a fixed `sleep`. A successful TCP connection alone may not mean migrations, dependencies, or application initialization are complete.

## 7. Security gates
Do not fail builds on every scanner warning without review. A practical approach:
- Start in report-only mode to establish a baseline.
- Validate findings and remove false positives with documented evidence.
- Define severity/confidence criteria for blocking.
- Fail on selected new, validated findings.
- Keep exceptions time-bound, owned, and reviewable.
- Track scan errors separately from vulnerability findings.

Avoid blanket suppression. A scan that fails to start, cannot reach the target, or never authenticates must not be treated as a clean result.

## 8. Active scanning safety
Active scans send attack payloads. They may modify records, trigger external integrations, send email, create accounts, or degrade availability. Run them only:
- Against disposable preview or dedicated staging environments.
- With written authorization and explicit scope.
- With synthetic data and destructive routes excluded where possible.
- With monitoring, rate limits, stop conditions, and cleanup.
- In a scheduled or gated pipeline rather than every untrusted pull request.

## 9. Secrets and pipeline hardening
- Use dedicated low-privilege test accounts.
- Store credentials in protected CI secret stores.
- Do not expose secrets to untrusted fork pull requests.
- Do not print tokens, cookies, or authenticated request bodies.
- Pin third-party actions and scanner images to reviewed versions/digests.
- Restrict runner permissions to the minimum needed.
- Protect artifact access and retention.
- Avoid privileged Docker-in-Docker unless required and reviewed.
- Do not expose the ZAP API port to untrusted networks.

## 10. Report handling
Useful artifacts include HTML, JSON, XML, or Markdown reports, scan logs, and a small metadata summary containing:
- Target and environment.
- Scanner/action/image version.
- Start/end time.
- Scan profile and scope.
- Discovered URLs and roles covered.
- Findings and dispositions.
- Errors and known limitations.

Reports may include internal URLs, response snippets, and sensitive metadata. Restrict access and retention accordingly.

## 11. CI/CD troubleshooting

| Symptom | Likely cause | First check |
|---|---|---|
| Connection refused | App not ready or wrong network | Health endpoint and service DNS |
| Target resolves on runner but not scanner | Container network mismatch | Shared Docker network |
| Empty report | Scope mismatch or no crawl coverage | Target URL, context and logs |
| Login page only | Authentication failed | Context, credentials and verification |
| Job passes despite scan errors | Exit handling masks errors | Exit code and log evaluation |
| Cleanup did not run | Missing unconditional cleanup | `if: always()` / `when: always` |
| Secrets unavailable | Untrusted PR or protected variable policy | Trigger and secret protections |

## Knowledge check
1. Why should a preview environment be ephemeral?
2. What is the difference between baseline and full scan?
3. Why is a readiness check better than a fixed sleep?
4. Why must active scanning be isolated?
5. What should happen if the scanner cannot reach the target?
6. Why should reports be access-controlled?

## Further reading
- OWASP DevSecOps DAST guideline: https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-2-Dynamic-Application-Security-Testing/
- ZAP Docker documentation: https://www.zaproxy.org/docs/docker/
- ZAP Baseline Scan: https://www.zaproxy.org/docs/docker/baseline-scan/
- ZAP Automation Framework: https://www.zaproxy.org/docs/automate/
- ZAP automation options: https://www.zaproxy.org/docs/getting-further/automation/automation-options/
