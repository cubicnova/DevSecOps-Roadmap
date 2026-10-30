# DAST in CI/CD - Practical Exercises

## Lab safety
- Use an isolated local training application or an authorized ephemeral preview environment.
- Use synthetic data and dedicated test accounts.
- Begin with passive baseline scans.
- Never run active scans against production or public targets without explicit written authorization.
- Protect reports and credentials.
- Ensure cleanup executes even when earlier steps fail.

## Exercise 1 - Map the pipeline
Draw the pipeline from commit to build, deploy, readiness check, DAST, report, gate, and cleanup.

**Deliverable:** CI/CD flow diagram with trust boundaries.

## Exercise 2 - Deploy an ephemeral target
1. Create a test Docker Compose configuration.
2. Bind the target to localhost or an isolated network.
3. Add a health check.
4. Start the application and verify readiness.
5. Tear it down and confirm resources are removed.

**Deliverable:** Compose file and execution notes.

## Exercise 3 - Run a local ZAP baseline
1. Start the lab application.
2. Run the ZAP baseline scan from a container.
3. Save HTML and JSON reports.
4. Record scan duration, discovered URLs, warnings, and errors.
5. Tear down the target.

**Deliverable:** Baseline report and scan summary.

## Exercise 4 - Build a readiness script
Implement a bounded health-check loop with timeout and useful failure output. Demonstrate that the pipeline stops before scanning if the application never becomes ready.

**Deliverable:** Readiness script and test output.

## Exercise 5 - Create a GitHub Actions workflow
Use `workflows/dast-github-actions.yml` as a starting point. Configure:
- Pull request and main-branch triggers.
- Isolated app deployment.
- Health check.
- ZAP passive baseline.
- Report upload.
- Unconditional cleanup.

Review third-party action pinning and permissions.

**Deliverable:** Workflow YAML and security review.

## Exercise 6 - Create a GitLab CI job
Adapt `workflows/dast-gitlab-ci.yml` for a runner you control. Confirm the scanner container can resolve and reach the target. Publish the report as an artifact.

**Deliverable:** `.gitlab-ci.yml` and successful job log.

## Exercise 7 - Report-only versus blocking gate
1. Run the baseline in report-only mode.
2. Review and validate findings.
3. Define which validated findings should block.
4. Document exception ownership and expiry.
5. Test the gate with a controlled fixture or mock report.

**Deliverable:** Gate policy and test evidence.

## Exercise 8 - Add API DAST
1. Create or locate an OpenAPI definition for the local lab API.
2. Run a ZAP API scan in the isolated environment.
3. Compare imported endpoints with crawler-discovered routes.
4. Record endpoints requiring authentication.

**Deliverable:** API scan report and coverage comparison.

## Exercise 9 - Separate active scanning
Design a scheduled active-scan job for a disposable staging environment. Include approval, scope, rate limits, monitoring, stop conditions, synthetic data, and cleanup.

**Deliverable:** Active-scan job design. Execute only after explicit authorization of the lab.

## Exercise 10 - Secure the pipeline
Review the workflow for:
- Untrusted fork pull requests receiving secrets.
- Overly broad token permissions.
- Mutable third-party action references.
- Unrestricted report artifacts.
- Exposed ZAP API ports.
- Missing cleanup.
- Unbounded scanner duration.

**Deliverable:** Threat model and remediation checklist.

## Exercise 11 - Failure injection
Test at least three conditions:
- Application fails health check.
- Scanner cannot reach target.
- Scan returns findings that violate the gate.

Verify that each condition produces the expected pipeline status and that cleanup still runs.

**Deliverable:** Failure matrix with logs.

## Exercise 12 - Final assessment
Deliver a working DAST CI pipeline with:
- Isolated test deployment.
- Readiness verification.
- Passive baseline scan.
- Report artifacts.
- Explicit gate policy.
- Secure secrets and permissions.
- Unconditional cleanup.
- Documented limitations and scan versions.

### Evaluation rubric (100 points)
| Area | Points |
|---|---:|
| Pipeline design and trust boundaries | 10 |
| Ephemeral environment and health check | 15 |
| ZAP baseline integration | 15 |
| Report and gate handling | 15 |
| API/active scan design | 10 |
| Secret and runner security | 15 |
| Failure handling and cleanup | 10 |
| Documentation and reproducibility | 10 |
