# Practical Exercises — Security Scanning Pipeline

## Lab prerequisites
- A disposable Jenkins controller and a dedicated agent labelled `security-scanner`.
- A test repository with a small application and dependency manifest.
- Approved installations of the scanners selected for the lab.
- Jenkins permissions to create jobs and archive build artifacts.
- No production secrets or real customer data in the test repository.

## Exercise 1: Map security checks to the SDLC
Choose at least four scan types: secret scanning, SAST, SCA, IaC, container, and DAST. Decide which pipeline stage runs each check, what artifact it examines, and who owns remediation.

**Deliverable:** A table containing scan type, stage, input, output, owner, and blocking policy.

## Exercise 2: Run a secret scan
1. Run Gitleaks against a test repository.
2. Save the JSON report as a build artifact.
3. Use only synthetic test values for demonstrations.
4. Confirm the report is not exposed to unauthorized users.
5. Explain what to do if a genuine credential is discovered.

**Deliverable:** Jenkins build log excerpt with sensitive values redacted and report-presence evidence.

## Exercise 3: Add SAST and SCA stages
Add Semgrep and Trivy filesystem scanning to a Jenkinsfile. Run each in a separate stage and archive the reports even when a scan stage fails, where your pipeline design permits.

**Deliverable:** Jenkinsfile and a successful test run showing stage-level results.

## Exercise 4: Scan Infrastructure as Code
Run Checkov against a test directory containing Terraform or Kubernetes configuration. Review at least three findings or checks and explain which are actionable in your scenario.

**Deliverable:** Report and remediation notes. Do not copy production infrastructure secrets into the lab.

## Exercise 5: Define a quality gate
Write a policy for critical/high/medium/low findings. Specify:
- Which findings block a build
- How scanner execution errors differ from policy failures
- How false positives are documented
- Who can approve an exception
- When exceptions expire

**Deliverable:** A one-page security gate policy.

## Exercise 6: Add credential handling
Create a dummy or restricted scanner token in Jenkins Credentials, then bind it only in the stage that requires it. Verify that the token does not appear in the Jenkinsfile or logs.

**Deliverable:** A screenshot or redacted log proving safe binding. Never paste a real token into the report.

## Exercise 7: Test failure behavior
Run a clean sample and a controlled sample with a known test finding. Confirm:
- Scanner execution completes.
- The report is created.
- The quality gate evaluates findings as expected.
- Pipeline status reflects policy.
- The logs distinguish scanner failure from a security finding.

**Deliverable:** A two-case test matrix with expected and actual outcomes.

## Exercise 8: Troubleshoot a missing report
Cause a safe failure in a lab, such as specifying an invalid output path. Diagnose the result using the console log, workspace, exit code, and artifact archive configuration. Restore the working configuration.

**Deliverable:** Root cause, fix, and preventive action.

## Exercise 9: Add a container scan
Build a test image, scan the image with Trivy, archive the JSON report, and define how an image digest is associated with the report. Do not push an image to a public registry unless explicitly intended and approved.

**Deliverable:** Jenkins stage and report with image tag/digest recorded.

## Exercise 10: Threat-model the pipeline
Review where untrusted pull-request code runs, which credentials it can access, what network access it has, and whether the agent is reused between trust levels. Propose isolation and least-privilege improvements.

**Deliverable:** At least five findings or design decisions with risk and mitigation.

## Completion checklist
- [ ] At least three scan types run in separate stages.
- [ ] Reports are archived and access-controlled.
- [ ] Exit-code and quality-gate behavior is tested.
- [ ] Credentials are stored and bound securely.
- [ ] Exceptions have an owner and expiry.
- [ ] Untrusted build inputs are isolated from privileged secrets.
