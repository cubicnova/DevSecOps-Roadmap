# SonarQube — Practical Exercises

Perform these exercises in a local lab or authorized SonarQube project. Use dummy credentials and non-production code.

## Lab 1 — Set up a SonarQube environment

1. Choose SonarQube Community Build, Server, or Cloud for the lab.
2. Review the official system requirements.
3. Start or access the instance using an approved deployment method.
4. Sign in and verify the instance is reachable.
5. Record product type, version, URL, and deployment method.

**Deliverable:** Setup notes and a screenshot of the dashboard. Do not expose the instance publicly without proper security controls.

## Lab 2 — Create a project and analysis token

1. Create a project named `training-app`.
2. Record its project key.
3. Generate a project-scoped analysis token where supported.
4. Store the token in a local environment variable or secret store.
5. Verify that the token is not present in source files or Git history.

**Deliverable:** Project key and sanitized configuration notes. Never include the token value.

## Lab 3 — Run your first scanner analysis

1. Install the appropriate SonarScanner.
2. Create a small application with a `src/` directory.
3. Add `sonar-project.properties`.
4. Set the server URL and token securely.
5. Run `sonar-scanner`.
6. Open the project dashboard and inspect the analysis.

**Deliverable:** Scanner output with credentials redacted and a dashboard screenshot.

## Lab 4 — Import test coverage

For a Python project:
1. Install `pytest` and `coverage`.
2. Add at least three unit tests.
3. Run `coverage run -m pytest`.
4. Generate `coverage.xml`.
5. Configure the Python coverage report path.
6. Run analysis again.
7. Confirm the coverage measure is imported.

**Deliverable:** Test output, coverage report, and SonarQube coverage screenshot.

## Lab 5 — Explore rules and Quality Profiles

1. Open the project's Quality Profile.
2. Identify the active profile for the language.
3. Review at least five active rules.
4. Record each rule's purpose and an example finding.
5. Identify one rule that could be useful for secure coding.
6. Do not disable rules without documenting a reason and approval.

**Deliverable:** Rule review table.

## Lab 6 — Investigate issues and security hotspots

1. Add a small training code sample with a potential security weakness.
2. Run analysis.
3. Open the Issues and Security Hotspots views.
4. Inspect the highlighted code and rule description.
5. Decide whether the result is a confirmed issue, a hotspot needing review, or a false positive.
6. Document your reasoning.
7. Fix valid issues and rerun analysis.

**Deliverable:** Triage report with finding, impact, decision, and remediation.

## Lab 7 — Configure a Quality Gate

1. Review the default Quality Gate.
2. Identify the conditions applied to new code.
3. Create a custom gate only if your lab permissions and product support it.
4. Define realistic conditions for new issues, coverage, and duplication.
5. Associate the gate with the training project.
6. Run analysis and observe the gate result.

**Deliverable:** Quality Gate configuration and pass/fail evidence.

## Lab 8 — Integrate SonarQube with GitLab CI

1. Add `sonarqube-check` to `.gitlab-ci.yml`.
2. Configure `SONAR_HOST_URL`, `SONAR_TOKEN`, and `SONAR_PROJECT_KEY` as CI/CD variables.
3. Mark the token masked/hidden and protected as appropriate.
4. Run analysis from a protected branch.
5. Add `sonar.qualitygate.wait=true`.
6. Confirm that the pipeline reflects the Quality Gate result.
7. Ensure untrusted fork or merge-request pipelines do not receive protected secrets.

**Deliverable:** Sanitized pipeline configuration and successful job log.

## Lab 9 — Test a failing Quality Gate

1. In a disposable branch, introduce a known training issue or lower a coverage metric.
2. Run analysis.
3. Observe the Quality Gate status.
4. Confirm how the CI job responds.
5. Fix the issue or restore coverage.
6. Rerun analysis and verify the gate result changes.

Do not introduce real vulnerabilities into production code.

## Lab 10 — Configure analysis scope

1. Identify source, test, generated, and vendor directories.
2. Configure `sonar.sources` and `sonar.tests`.
3. Add narrowly scoped exclusions for generated/vendor files if justified.
4. Run analysis and inspect the analyzed file count.
5. Verify that important application code has not been excluded.

**Deliverable:** Scope configuration and rationale.

## Lab 11 — Troubleshoot scanner failures

Create or use a disposable lab and investigate:
- Incorrect project key.
- Invalid token.
- Unreachable server.
- Missing coverage report.
- Wrong source directory.
- Shallow Git clone.

For each, record the symptom, diagnostic step, root cause, and fix. Avoid sharing logs with secrets or sensitive infrastructure details.

## Lab 12 — Build a secure quality workflow

Create a small repository containing:
- Source code and unit tests.
- Coverage report generation.
- `sonar-project.properties`.
- GitLab CI scanner job.
- A documented Quality Gate policy.
- A finding triage report.

Demonstrate a passing run and a controlled failing run, then document the remediation.

**Final deliverable:** Repository link or archive, sanitized pipeline logs, screenshots, and a short report explaining the quality and security controls.
