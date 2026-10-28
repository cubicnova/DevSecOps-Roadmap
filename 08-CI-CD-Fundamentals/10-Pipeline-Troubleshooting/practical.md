# Pipeline Troubleshooting — Practical Exercises

Complete the exercises in a test repository or disposable branch. Do not use production credentials or intentionally break a production pipeline.

## Lab 1: Build a failure triage record

A CI run fails on the `test` job after a dependency-install step.

Tasks:
1. Record the workflow name, run ID, commit SHA, branch, job, and failing step.
2. Copy the first relevant error and a few lines of context.
3. Classify the failure.
4. Write two possible causes and the evidence needed to distinguish them.
5. Propose the smallest safe next test.

**Deliverable:** A short triage note.

## Lab 2: Diagnose a missing trigger

Use this workflow:

```yaml
name: Basic CI
on:
  push:
    branches: [main]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - run: echo "CI started"
```

Tasks:
1. Explain why a push to a branch named `feature/logging` does not trigger this workflow.
2. Edit the workflow so pushes to `main` and `feature/**` run CI.
3. Add a `pull_request` trigger targeting `main`.
4. Validate YAML and inspect the workflow's trigger settings.

**Deliverable:** Corrected YAML and a one-paragraph explanation.

## Lab 3: Fix a malformed workflow

Find the indentation and structure problem:

```yaml
name: Test
on:
  push:
jobs:
  unit-tests:
  runs-on: ubuntu-latest
    steps:
    - name: Print message
      run: echo "running"
```

Tasks:
1. Correct the YAML.
2. Explain how indentation affects the `jobs`, job ID, `runs-on`, and `steps` hierarchy.
3. Use a YAML linter if available.

**Deliverable:** Corrected workflow file.

## Lab 4: Resolve an artifact mismatch

Pipeline stages:
- Build uploads an artifact named `web-dist`.
- Deploy downloads an artifact named `website-dist`.

Tasks:
1. Identify the mismatch.
2. Correct the name in one stage.
3. Add a check that the expected output directory contains files before deployment.
4. Explain why a green build does not always mean the deploy stage has the right artifact.

**Deliverable:** Corrected upload/download steps.

## Lab 5: Diagnose a missing environment variable

Use this script in a test project:

```python
import os
print("Starting tests")
if not os.getenv("SERVICE_URL"):
    raise SystemExit("SERVICE_URL is required")
print("Configuration check passed")
```

Tasks:
1. Run it without `SERVICE_URL` and capture the expected failure.
2. Set a harmless local test URL and rerun.
3. Add a pipeline step that checks whether `SERVICE_URL` is present without printing its value.
4. Explain when a variable should be stored as a secret rather than a plain variable.

**Deliverable:** Script output and a safe CI check.

## Lab 6: Analyze an authorization failure

A deployment request returns `403 Forbidden`.

Tasks:
1. Explain the difference between authentication and authorization.
2. Check identity, token permissions, environment protection rules, and target resource permissions.
3. Write a least-privilege remediation.
4. Explain why giving the token all available permissions is not a good first response.

**Deliverable:** Troubleshooting checklist and remediation plan.

## Lab 7: Investigate an intermittent timeout

A dependency registry request times out once, then succeeds on retry.

Tasks:
1. List at least four possible causes.
2. Check DNS, TLS, registry status, proxy/firewall, and rate limiting where applicable.
3. Decide whether a bounded retry is appropriate.
4. Describe when retrying could hide a deterministic defect.

**Deliverable:** Evidence-based root-cause hypothesis.

## Lab 8: Inspect a Docker build failure

A Docker build fails at `COPY src/ ./src/`.

Tasks:
1. Check the current directory and Docker build context.
2. Confirm that `src/` exists and is committed.
3. Inspect `.dockerignore`.
4. Check path capitalization.
5. Fix the problem and rebuild.

**Deliverable:** Root cause and corrected command or file.

## Lab 9: Enable diagnostic logging safely

Tasks:
1. Explain when standard logs are insufficient.
2. In a test GitHub repository, enable step debug logging using the supported repository secret or variable setting.
3. Re-run a test workflow and inspect the added output.
4. Disable debug logging when done.
5. Confirm no secrets or sensitive environment values appear in logs.

**Deliverable:** Short before/after note.

## Lab 10: Full incident simulation

Scenario: The pipeline did not run on a feature branch. After changing the trigger, dependency installation failed. Once dependencies were installed, tests failed because `SERVICE_URL` was missing. The build then succeeded, but deployment could not find the artifact.

Tasks:
1. Diagnose each issue independently.
2. Fix the trigger, dependency problem, configuration, and artifact naming.
3. Re-run after each change rather than changing everything at once.
4. Document root cause, fix, validation, and preventive action for each issue.

**Deliverable:** A troubleshooting report and a successful test pipeline.

## Evaluation rubric

| Criterion | Points |
|---|---:|
| Identifies the earliest useful error | 20 |
| Uses evidence rather than guesswork | 20 |
| Chooses a minimal, safe fix | 20 |
| Validates the fix with a rerun/test | 20 |
| Documents cause and prevention | 20 |
| **Total** | **100** |

## Safety rules

- Use test branches and non-production environments.
- Never paste secrets into logs, issues, screenshots, or reports.
- Do not disable security checks just to make a pipeline green.
- Do not make repeated blind reruns; each retry should test a hypothesis.
- Revert intentional faults after completing the lab.
