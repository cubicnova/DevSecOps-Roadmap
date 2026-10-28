# Pipeline Troubleshooting — Suggested Solutions

Solutions are examples, not the only valid answers. Learners should explain the evidence supporting their diagnosis.

## Lab 1: Failure triage

A useful triage record includes:
- Workflow/run ID, commit SHA, branch, job, and failing step.
- Exact error with enough surrounding context.
- Category such as dependency resolution, DNS, authentication, or test failure.
- Hypotheses with checks that can confirm or reject each one.
- A minimal next step, such as checking the runtime version or retrying a registry request once after verifying service status.

Do not assume every install failure is a network problem.

## Lab 2: Missing trigger

One corrected workflow:

```yaml
name: Basic CI
on:
  push:
    branches:
      - main
      - "feature/**"
  pull_request:
    branches:
      - main
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - run: echo "CI started"
```

The original workflow only subscribed to `push` events for `main`, so pushes to feature branches did not match its filter.

## Lab 3: Malformed workflow

Corrected version:

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

`runs-on` and `steps` must be children of the job ID (`unit-tests`). Each step is an item in the `steps` list.

## Lab 4: Artifact mismatch

The artifact name must match between upload and download. For example:

```yaml
- name: Upload build
  uses: actions/upload-artifact@v4
  with:
    name: web-dist
    path: dist/
```

```yaml
- name: Download build
  uses: actions/download-artifact@v4
  with:
    name: web-dist
    path: dist/
```

Before deployment, verify expected files exist. For example, on a Linux runner:

```yaml
- name: Verify artifact
  run: |
    test -d dist
    find dist -type f -print -quit | grep -q .
```

If the download step uses a different name or path, the deploy job may not receive the files that the build job produced.

## Lab 5: Missing environment variable

Local test:

```bash
SERVICE_URL="https://example.test" python app_check.py
```

A safe shell check:

```yaml
- name: Validate service configuration
  shell: bash
  run: |
    set -euo pipefail
    if [[ -z "${SERVICE_URL:-}" ]]; then
      echo "SERVICE_URL is missing"
      exit 1
    fi
    echo "SERVICE_URL is configured"
```

Use plain variables for non-sensitive configuration. Store passwords, API tokens, and other credentials in the CI platform's secret store. Avoid printing values.

## Lab 6: Authorization failure

Authentication answers “who are you?” Authorization answers “what are you allowed to do?”

Suggested checks:
1. Verify the expected identity is used.
2. Verify the token is valid and available to this workflow event.
3. Review the minimum required token or cloud-role permissions.
4. Confirm the deployment environment's protection/approval rules.
5. Confirm target resource policy and repository/environment configuration.

Grant only the missing permission needed for the operation. Broad permissions increase the impact of token theft or workflow compromise.

## Lab 7: Intermittent timeout

Possible causes include transient registry outage, DNS instability, rate limiting, proxy/firewall interruption, TLS problems, runner network congestion, or an overloaded service.

Gather evidence before changing configuration. A bounded retry with backoff may be suitable for idempotent network requests that fail transiently. It is not a substitute for correcting invalid URLs, bad credentials, deterministic test failures, or broken configuration.

## Lab 8: Docker build failure

Useful checks:

```bash
pwd
ls -la
find . -maxdepth 2 -type d -print
cat .dockerignore
```

If `src/` is in the current directory and the Dockerfile is there, a typical command is:

```bash
docker build -f Dockerfile .
```

The final `.` defines the build context. Docker cannot copy files outside that context. Ensure `.dockerignore` does not exclude required paths and use the exact case-sensitive path.

## Lab 9: Diagnostic logging

For GitHub Actions, set `ACTIONS_STEP_DEBUG` to `true` as a repository secret or variable using the appropriate permissions. Set `ACTIONS_RUNNER_DEBUG` to `true` when runner diagnostic logs are needed. Rerun the workflow, inspect the logs, then remove or set the diagnostic values back to disabled. Do not print secrets or use shell tracing indiscriminately.

## Lab 10: Incident simulation

Resolve in order, validating after each change:

1. **Trigger:** Update branch/event filters according to the team's intended policy.
2. **Dependencies:** Read the first install error; verify runtime, lockfile, package versions, and registry/network access.
3. **Configuration:** Add `SERVICE_URL` to the correct workflow/environment as a non-secret variable if safe; use a secret store for credentials.
4. **Artifact:** Align upload/download names and paths, and verify the expected files exist before deployment.
5. **Validation:** Run the relevant job, then the complete pipeline. Confirm that the intended artifact is deployed to the intended test environment.

Example incident entry:

```text
Issue: CI/CD pipeline failed on feature branch
Root causes:
- Trigger filter did not include feature branches
- Dependency installation had an invalid version pin
- SERVICE_URL was absent from the test environment
- Artifact upload and download names differed
Resolution: Corrected each issue and validated after each change
Prevention: Trigger tests, dependency lockfile validation, early config checks,
            and artifact verification before deployment
Validation: Full pipeline passed in a non-production environment
Secrets exposed: No
```

## Additional references

- [Troubleshooting workflows](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows)
- [Using workflow run logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs)
- [Enabling debug logging](https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging)
