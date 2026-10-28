# 10 - Pipeline Troubleshooting

A practical learning module for diagnosing, fixing, and preventing failures in CI/CD pipelines.

## Learning objectives

By the end of this module, learners should be able to:

- Read pipeline logs and identify the first meaningful failure.
- Separate trigger, configuration, dependency, test, artifact, deployment, runner, and permission problems.
- Reproduce a pipeline failure locally where possible.
- Use safe, temporary diagnostic logging without exposing secrets.
- Apply a fix, verify it, and document the root cause.

## Troubleshooting workflow

1. **Confirm the symptom** — identify the workflow, run ID, branch, commit, stage, and expected behavior.
2. **Find the first failure** — inspect the earliest failing step, not just the final summary.
3. **Classify the failure** — trigger/configuration, environment, dependency, test, artifact, network, permissions, or deployment.
4. **Form a hypothesis** — change one variable at a time.
5. **Reproduce safely** — use the same runtime version and relevant configuration locally or in a test branch.
6. **Fix and validate** — run the narrowest useful test, then rerun the full pipeline.
7. **Prevent recurrence** — add validation, pin versions, improve messages, or add a regression test.
8. **Record the incident** — capture impact, root cause, resolution, and preventive action.

## Common failure categories

| Category | Common symptoms | First checks |
|---|---|---|
| Workflow not triggered | No run appears | `on:` events, branch/path filters, disabled workflow, skip annotations |
| Invalid configuration | Workflow fails before steps run | YAML syntax, required fields, action inputs, indentation |
| Dependency install | Package not found, lockfile mismatch | Runtime version, registry, lockfile, cache |
| Tests/build | Unit test or compilation failure | First stack trace, test data, environment variables |
| Artifact handoff | Deploy stage cannot find package | Artifact name, upload/download paths, retention |
| Runner/environment | Tool missing, job queued, disk full | Runner labels, image, installed tools, capacity |
| Permissions/authentication | 401/403, denied operation | Token scope, job permissions, secret availability |
| Network/service | Timeout, DNS, TLS error | Endpoint status, DNS, firewall/proxy, certificate chain |
| Deployment | Health check fails, wrong version deployed | Target environment, config, rollout logs, health endpoint |

## GitHub Actions: inspect a failed run

1. Open the repository's **Actions** tab.
2. Select the workflow and failed run.
3. Open the failed job and expand the failed step.
4. Read a little before the first error and follow the error to its cause.
5. Compare the failed run with the most recent successful run.
6. Download logs if needed; share a permalink to the relevant log lines with teammates.

Useful GitHub CLI commands:

```bash
# List recent workflow runs
gh run list --limit 10

# Inspect a particular run
gh run view RUN_ID

# Print logs for a run
gh run view RUN_ID --log

# Print failed-step logs
gh run view RUN_ID --log-failed

# Re-run failed jobs after investigating
gh run rerun RUN_ID --failed
```

Replace `RUN_ID` with the actual run identifier. Do not rerun repeatedly without learning something from the previous attempt.

## Debug logging

If ordinary logs are insufficient, enable additional diagnostic logging temporarily. For GitHub Actions, repository secrets or variables named `ACTIONS_STEP_DEBUG` and `ACTIONS_RUNNER_DEBUG` can be set to `true` where permitted. Remove or disable them after troubleshooting.

Do not print access tokens, passwords, private keys, `.env` files, or full environment dumps. Mask sensitive values and prefer logging whether a variable is set rather than printing its contents.

## Useful local checks

```bash
# Validate YAML with a tool available in your environment
yamllint .github/workflows/

# Inspect recent commits
git log --oneline -8

# Check local working-tree changes
git status --short

# Run project tests (example for Python)
python -m pytest -q

# Check installed runtime versions
python --version
node --version
docker --version
```

Run only commands relevant to the project and installed tools.

## Lab structure

- [`examples.md`](examples.md) — common failure scenarios and diagnostic patterns.
- [`practical.md`](practical.md) — hands-on troubleshooting tasks.
- [`solutions.md`](solutions.md) — suggested answers and corrected configurations.

## Completion checklist

- [ ] I can identify the first failing step in a run.
- [ ] I can classify the failure and test a specific hypothesis.
- [ ] I can distinguish transient failures from reproducible defects.
- [ ] I can troubleshoot artifacts, secrets, permissions, runners, and deployments.
- [ ] I can write a useful root-cause report without exposing secrets.

## Further reading

- [GitHub Docs: Troubleshooting workflows](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows)
- [GitHub Docs: Using workflow run logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs)
- [GitHub Docs: Enabling debug logging](https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging)

> These materials use GitHub Actions for examples, but the troubleshooting process also applies to GitLab CI, Jenkins, Azure Pipelines, and other CI/CD systems.
