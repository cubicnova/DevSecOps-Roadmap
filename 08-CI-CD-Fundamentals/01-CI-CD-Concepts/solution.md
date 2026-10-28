# CI/CD Concepts — Suggested Solutions

These are sample answers, not the only acceptable answers. Explain the reasoning behind each design decision.

## Solution 1 — CI, Continuous Delivery, and Continuous Deployment

| Model | Expected behavior after tests pass |
|---|---|
| CI | Code is integrated and automated checks run; production deployment is not implied. |
| Continuous Delivery | A release-ready artifact is prepared and can be deployed; production may require manual approval or a release decision. |
| Continuous Deployment | Changes passing all required checks are automatically released to production. |

Continuous Deployment needs strong test coverage, observability, and safe recovery because successful automated checks trigger production release.

## Solution 2 — Example pipeline design

```text
Pull Request
   |
   v
Checkout -> Lint -> Unit Tests -> Dependency/SAST Checks
                                   |
                              All required checks pass?
                              /                  \
                            No                    Yes
                            |                      |
                       Block merge             Build artifact
                                                   |
                                             Deploy to staging
                                                   |
                                             Smoke/integration tests
                                                   |
                                              Approval gate
                                                   |
                                             Production deploy
                                                   |
                                           Health checks/monitoring
                                             /             \
                                           Good            Bad
                                            |               |
                                         Continue       Roll back
```

A production design should define who can approve, how the artifact is identified, which health checks are required, and how rollback is performed.

## Solution 3 — Local verification

Run:

```bash
python app.py
python -m unittest -v
```

Expected application output is `5`. The test runner should report three passing tests. If Python cannot import `app`, ensure both files are in the same directory and run the command from that directory.

## Solution 4 — GitHub Actions workflow

Use the `Python CI` workflow from `examples.md`. Confirm the file is located at:

```text
.github/workflows/ci.yml
```

Then commit and push:

```bash
git add app.py test_app.py .github/workflows/ci.yml
git commit -m "Add introductory CI workflow"
git branch -M main
git remote add origin https://github.com/OWNER/REPOSITORY.git
git push -u origin main
```

Replace `OWNER/REPOSITORY` with your own test repository. If a remote already exists, inspect it with `git remote -v` rather than adding it again.

## Solution 5 — Failed quality gate

Change an assertion, for example:

```python
self.assertEqual(add(2, 3), 6)
```

The test fails because `add(2, 3)` returns `5`. GitHub Actions marks the step and job as failed. Restore the correct assertion and push again. Configure branch protection or repository rules so required checks must pass before a pull request can merge.

## Solution 6 — Add linting

A simple learning workflow can install Ruff and run:

```yaml
- name: Install Ruff
  run: python -m pip install ruff

- name: Lint source and tests
  run: ruff check .
```

For repeatable CI, add Ruff to a development dependency file or project configuration and pin the intended version. A lint failure should return a non-zero exit code and fail the job if linting is a required quality gate.

## Solution 7 — Job dependencies

Set `needs: test` on the `package` job:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m unittest -v

  package:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Package only after tests pass"
```

The package command is illustrative. In a real project, build a proper package or container and store the resulting artifact.

## Solution 8 — Artifact traceability

Useful metadata includes:

- Full source commit SHA.
- CI workflow run ID and build timestamp.
- Application version or release tag.
- Artifact checksum or container image digest.
- Build toolchain and dependency lockfile version.

A strong process publishes an immutable artifact and promotes the same artifact from staging to production. Do not rely solely on a mutable tag such as `latest`.

## Solution 9 — Secrets handling

A hard-coded API key may be exposed through Git history, forks, logs, or copies of the repository. Removing it from the current file does not invalidate prior copies.

Recommended response:

1. Revoke or rotate the exposed credential immediately.
2. Review audit logs for unexpected use.
3. Store the replacement in an approved secret manager or GitHub Actions secret.
4. Pass it only to the job and step that need it.
5. Avoid printing it, enabling shell tracing around it, or including it in artifacts.
6. Consider history cleanup if appropriate, but do not treat history rewriting as a substitute for rotation.

For cloud deployments, prefer short-lived credentials and identity federation when supported.

## Solution 10 — Least privilege

For the introductory test workflow:

```yaml
permissions:
  contents: read
```

This permits read access to repository contents needed for checkout. A test-only workflow normally does not need to create releases, write packages, or modify repository settings. Grant additional permissions only to jobs that require them.

## Solution 11 — Pull request threat model

Risks include:

1. Untrusted code could read credentials available to the runner.
2. Malicious code could persist on a long-lived self-hosted runner.
3. A compromised runner could access internal network resources.
4. A workflow could exfiltrate tokens through logs or network requests.

Controls include:

- Use isolated, ephemeral runners for untrusted code.
- Do not expose deployment secrets to untrusted pull-request workflows.
- Separate validation from privileged deployment workflows.
- Restrict network access and runner permissions.
- Use minimal token permissions and review third-party actions.
- Do not use privileged `pull_request_target` workflows to check out and execute untrusted pull-request code without a carefully reviewed design.

## Solution 12 — Release and rollback

A reasonable Continuous Delivery process:

1. Build once from a specific commit.
2. Run automated tests and security/quality checks.
3. Publish the artifact with a version, commit SHA, and checksum or image digest.
4. Deploy that artifact to staging.
5. Run smoke and integration tests.
6. Require an authorized approval before production deployment.
7. Promote the same artifact to production.
8. Monitor error rates, latency, and key technical/business signals.
9. If health checks fail, stop rollout and roll back to the last known-good artifact.
10. Record the deployment, approval, verification results, and any incident.

For critical services, use a tested rollback or roll-forward procedure and verify database changes are backward-compatible.

## Stretch challenge hints

- **Python matrix:** use `strategy.matrix.python-version` and configure Python from the matrix value.
- **Dependency scanning:** choose a maintained scanner, pin its version, and define how findings affect the build.
- **Concurrency:** use a group derived from workflow and branch/ref; decide carefully whether cancellation is appropriate for deployment jobs.
- **Manual trigger:** add `workflow_dispatch` under `on`.
- **Permissions:** set restrictive workflow-level defaults and elevate permissions only at the job level where necessary.

## Final review

A sound introductory pipeline should be repeatable, observable, traceable, secure by default, and able to stop on failed checks. CI/CD is not merely automation: it is also the set of controls that make software releases dependable.
