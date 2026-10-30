# GitLab Security Scanning — Practical Exercises

## Lab safety and prerequisites
- A GitLab test project with CI/CD enabled.
- An eligible runner and access to required scanner images.
- A disposable application and test container image.
- A staging target you own or have explicit authorization to test.
- Never use real credentials as test data. Never scan third-party or production systems without written authorization.

## Exercise 1: Enable SAST
1. Add the SAST template to `.gitlab-ci.yml`.
2. Push a branch and inspect the pipeline.
3. Identify the SAST job and analyzer image.
4. Review its artifacts and report.
5. Record which languages and files are supported in your project.

**Expected result:** A SAST job is created when the repository contains supported files and template rules allow it.

## Exercise 2: Create a safe SAST finding
1. Use a deliberately vulnerable training application or a small local code sample.
2. Add a known insecure pattern appropriate to the language.
3. Run SAST.
4. Record the finding type, file, line, severity, and suggested remediation.
5. Fix the issue and rerun the scan.

Do not deploy the vulnerable example to a public or production environment.

## Exercise 3: Enable secret detection safely
1. Include the secret detection template.
2. Add an obviously fake marker string such as `TRAINING_TOKEN_NOT_REAL_1234567890`.
3. Run the pipeline.
4. Inspect whether the marker is detected by the configured analyzer and coverage mode.
5. Remove the marker from the training branch.

**Important:** Do not use a real credential. If one is accidentally committed, revoke/rotate it immediately and follow your incident process. Removing it from the latest commit is not sufficient.

## Exercise 4: Historic secret detection research
1. Read the current GitLab documentation about pipeline and historic secret detection.
2. Explain the difference between scanning the current state/future commits and scanning earlier Git history.
3. In a disposable repository, plan a historic scan using the documented supported method.
4. Document coverage limitations.

## Exercise 5: Dependency scanning
1. Add a supported dependency manifest and lockfile to a test application.
2. Include the dependency scanning template.
3. Run the pipeline.
4. Inspect package name, installed version, vulnerability identifier, severity, and fixed version where available.
5. Update the dependency to a supported fixed version and rerun.

Use a test dependency selected from an official advisory or training dataset. Do not add a vulnerable dependency to a real production service.

## Exercise 6: Container scanning
1. Build a small test container image.
2. Push it to a test registry or make it available using a documented supported workflow.
3. Include the container scanning template.
4. Configure the image reference.
5. Run the scan and inspect the report.
6. Rebuild with updated base packages and compare findings.

Avoid enabling privileged Docker-in-Docker on shared runners without a security review.

## Exercise 7: DAST in staging
1. Deploy a deliberately vulnerable training app to an isolated local or staging environment.
2. Confirm the target is owned by you and reachable from the runner.
3. Include the DAST template and set the target URL using the documented variable.
4. Run a scan with safe scope and test accounts.
5. Review findings and remediation guidance.
6. Stop the test environment when complete.

Never direct DAST at an arbitrary public website.

## Exercise 8: IaC scanning
1. Add a sample Terraform or Kubernetes configuration file.
2. Include the current GitLab IaC scanning template.
3. Add one deliberately insecure training configuration.
4. Run the scan and inspect the finding.
5. Apply the recommended secure configuration and rescan.

Use non-deployable lab files; do not apply insecure infrastructure to a real cloud account.

## Exercise 9: Security reports and artifacts
1. Open a successful scanner job.
2. Locate its report artifact.
3. Identify the report type and format.
4. Explain why a generic JSON artifact is not automatically a GitLab security report.
5. Document where the findings are presented in your GitLab instance.

## Exercise 10: Configure a security stage
1. Create a `security` stage.
2. Move the supported scanner jobs into it using the documented job overrides or template inputs.
3. Validate the configuration with CI Lint.
4. Run a pipeline and confirm stage ordering.
5. Check that every template job's stage exists.

## Exercise 11: Triage findings
For at least three findings from your lab:
- Identify severity and confidence.
- Determine affected asset and exposure.
- Check whether a fix is available.
- Assign an owner and remediation action.
- Record any accepted risk with rationale and review date.
- Rescan after remediation.

## Exercise 12: Troubleshooting
Diagnose the following:
1. No scanner job appears.
2. Pipeline fails because a scanner stage is missing.
3. Container scanner cannot pull the image.
4. DAST cannot reach the target.
5. Secret detection does not find an older leaked secret.
6. Scanner job succeeds but no finding appears.
7. A report artifact exists but the Security UI does not show it.

For each, record symptom, likely cause, evidence, and correction.

## Submission checklist
- [ ] SAST enabled and finding documented.
- [ ] SAST issue fixed and rescanned.
- [ ] Secret detection run with fake training data only.
- [ ] Historic secret scanning behavior researched.
- [ ] Dependency scan completed and dependency remediated.
- [ ] Test container image scanned.
- [ ] DAST performed only against an authorized staging target.
- [ ] IaC scan completed.
- [ ] Security report artifact inspected.
- [ ] Security stage validated.
- [ ] Findings triaged and remediation documented.
- [ ] Troubleshooting report submitted.

## Viva questions
1. What is the purpose of security scanning in CI/CD?
2. Differentiate SAST and DAST.
3. What does dependency scanning identify?
4. Why is secret detection important?
5. What is IaC scanning?
6. What does container scanning examine?
7. What is a GitLab security report artifact?
8. Why might a scanner job not appear?
9. Why should DAST run against an authorized staging target?
10. What should you do if a real secret is committed?
11. Does a successful scan guarantee that an application is secure?
12. How should security findings be prioritized?
