# DAST in CI/CD - Solutions and Guidance

## Exercise 1 - Map the pipeline
A good design has distinct build, test, deploy, readiness, scan, report/gate, and cleanup stages. The scanner should reach only the intended test application. CI credentials, deployment credentials, scanner secrets, and report artifacts should be separated by least privilege.

## Exercise 2 - Deploy an ephemeral target
The target should be isolated, use synthetic data, and expose only the required port. A health check should verify application readiness. Use immutable image references for repeatability and remove volumes/containers after the run when safe.

## Exercise 3 - Run a local ZAP baseline
A successful baseline run records the target, scanner image/version, duration, URLs discovered, report paths, and exit status. Baseline scans perform passive checks rather than active attack payload testing. Protect the report and do not treat a scan with zero discovered URLs as a clean security result.

## Exercise 4 - Build a readiness script
Use a bounded retry loop and non-zero exit on timeout. The readiness URL should verify that the application can serve requests. Do not use an unbounded wait or a fixed sleep as the only readiness mechanism.

## Exercise 5 - GitHub Actions workflow
A robust workflow:
- Uses least-privilege `permissions`.
- Does not expose secrets to untrusted fork pull requests.
- Deploys an ephemeral app.
- Waits for health.
- Runs a passive baseline.
- Uploads reports with restricted access and retention.
- Cleans up in an unconditional step.
- Pins third-party actions to reviewed immutable SHAs.

## Exercise 6 - GitLab CI job
The scanner job must reach the target from its own network namespace. `localhost` inside a job container is the job container itself. Use a service alias or shared network and verify reachability before scanning. Store reports as restricted artifacts and set an appropriate expiry.

## Exercise 7 - Report-only versus blocking gate
Begin with report-only mode to learn the scanner's behavior. Validate candidate findings and define explicit criteria for blocking, such as confirmed high-impact findings. Keep an exception record with a ticket, owner, justification, compensating control, and expiry. Avoid broad suppression rules.

## Exercise 8 - API DAST
An API scan should import an accurate API definition and remain scoped to the authorized API host. Compare imported paths with crawler routes. Configure authentication where required and record methods/operations that were not tested. An OpenAPI document improves discovery but does not test every business rule.

## Exercise 9 - Separate active scanning
A safe active-scan design uses a disposable environment, approval, exact scope, test identities, synthetic data, rate limits, monitoring, stop conditions, and unconditional cleanup. It should not run automatically against production or an untrusted pull-request deployment.

## Exercise 10 - Secure the pipeline
Recommended controls:
- Minimal CI token permissions.
- No secrets for untrusted forks.
- Immutable action/image references.
- Restricted artifacts and retention.
- No public ZAP API exposure.
- Bounded scan duration and request volume.
- Cleanup with `always()` / `when: always`.
- Protected branches/environments for privileged jobs.

## Exercise 11 - Failure injection
Expected outcomes:
- Health check timeout: fail before scan; cleanup still executes.
- Scanner cannot reach target: fail or mark scan as errored; never report clean.
- Gate violation: publish the report and fail according to the reviewed policy.
- Cleanup failure: surface the failure and alert the environment owner.

## Exercise 12 - Final assessment checklist
A complete submission includes workflow files, application deployment configuration, readiness script, scan report, gate policy, action/image pinning evidence, permissions review, cleanup proof, and documented limitations.

## Sample pipeline summary
> The pipeline deploys a disposable application instance with synthetic data, waits for a readiness endpoint, and runs a bounded ZAP passive baseline scan. Reports are stored as restricted artifacts and evaluated against a reviewed gate policy. Active scanning is maintained as a separate approved workflow for isolated staging. Scanner failures are not treated as clean results, and cleanup runs regardless of job outcome.
