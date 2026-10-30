# SAST CI/CD Integration — Practical Exercises

Complete these labs in a sandbox GitLab project and authorized repositories. Use dummy credentials and non-production code.

## Lab 1 — Map the pipeline

1. Draw your current CI/CD stages.
2. Identify build, test, SAST, artifact, and deployment jobs.
3. Identify which jobs receive credentials.
4. Mark untrusted merge-request and trusted release boundaries.
5. Propose where SAST should run.

**Deliverable:** Pipeline architecture diagram and trust-boundary notes.

## Lab 2 — Enable GitLab-managed SAST

1. Create a sandbox GitLab project.
2. Add the SAST template include.
3. Validate the pipeline configuration.
4. Run a branch pipeline.
5. Inspect the jobs created by the template.
6. Confirm whether the repository language is supported.
7. Review the resulting security findings.

**Deliverable:** Sanitized pipeline configuration and job evidence.

## Lab 3 — Integrate Semgrep

1. Add a Semgrep CLI job.
2. Run it against the repository.
3. Export JSON output as an artifact.
4. Review rule IDs, locations, and severities.
5. Add a harmless vulnerable training example.
6. Confirm that the scan detects it.
7. Fix the example and rescan.

**Deliverable:** Before/after scan outputs.

## Lab 4 — Integrate SonarQube

1. Create or select a SonarQube project.
2. Configure the project key and server URL.
3. Store the analysis token as a secure CI/CD variable.
4. Add a scanner job.
5. Run analysis on the default branch.
6. Enable Quality Gate waiting.
7. Review the dashboard and pipeline result.

**Deliverable:** Sanitized job log and Quality Gate screenshot.

## Lab 5 — Generate and publish coverage

1. Add unit tests to a small application.
2. Generate a coverage report.
3. Upload the report as a pipeline artifact.
4. Configure SonarQube to import the report.
5. Confirm coverage is visible in analysis.
6. Deliberately omit the report in a test branch and diagnose the result.

**Deliverable:** Test job, report artifact, and analysis evidence.

## Lab 6 — Explore CodeQL output

1. Select a supported language and a training repository.
2. Follow the official CodeQL setup for that language.
3. Create a database using the appropriate build mode.
4. Run a standard query suite.
5. Generate SARIF.
6. Inspect the SARIF structure and findings.
7. Determine how your chosen platform supports SARIF ingestion.

**Deliverable:** SARIF artifact and integration notes. Do not assume a generic artifact is automatically ingested.

## Lab 7 — Secure merge-request scanning

1. Configure SAST to run for merge requests.
2. Identify which variables are protected.
3. Create a test merge request from an untrusted branch or fork if your lab permits.
4. Verify production credentials are not available to that job.
5. Confirm the scan can still run without privileged credentials.
6. Review runner isolation and job-token access.

**Deliverable:** Trust-boundary test report.

## Lab 8 — Configure a staged quality gate

1. Start with scans in advisory mode.
2. Collect a baseline of existing findings.
3. Define which new findings should block merges.
4. Configure the selected scanner or Quality Gate accordingly.
5. Introduce a controlled training finding.
6. Verify the expected pipeline status.
7. Fix the issue and verify the result.

**Deliverable:** Written enforcement policy and pass/fail evidence.

## Lab 9 — Handle report formats

1. Generate Semgrep JSON.
2. Generate SARIF from a supported scanner.
3. Inspect each output format.
4. Identify which format your CI platform expects for native security-report ingestion.
5. If conversion is required, use a supported and validated converter.
6. Verify the uploaded report appears in the intended UI.

**Deliverable:** Format comparison and ingestion evidence.

## Lab 10 — Manage scanner versions and exclusions

1. Identify the scanner image and version used by each job.
2. Replace floating image tags with reviewed versions or digests.
3. Review excluded paths.
4. Remove unnecessary exclusions.
5. Confirm the scanner still analyzes the intended source files.
6. Document the update and review cadence.

**Deliverable:** Scanner inventory and exclusion review.

## Lab 11 — Improve performance

1. Record scan duration and runner resource use.
2. Identify dependency downloads and repeated setup.
3. Cache only safe dependencies or package-manager data.
4. Avoid sharing untrusted cache data with privileged release jobs.
5. Test parallel scanning only if runner capacity allows.
6. Compare duration and reliability before and after.

**Deliverable:** Performance comparison.

## Lab 12 — Build an end-to-end SAST pipeline

Create a sandbox repository with:
- Unit tests and coverage.
- One primary SAST scanner.
- Optional second scanner with a documented reason.
- Secure CI/CD variable configuration.
- Merge-request scan rules.
- Report artifacts or native security report ingestion.
- A quality gate or severity policy.
- A finding triage workflow.

Demonstrate a passing run and a controlled failing run. Include sanitized logs, report artifacts, and remediation evidence.

**Final deliverable:** Repository link or ZIP, pipeline diagram, CI configuration, scanner results, and a short security integration report.
