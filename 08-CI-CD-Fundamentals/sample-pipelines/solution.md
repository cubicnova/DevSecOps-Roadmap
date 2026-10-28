# Solutions and Guidance: Sample CI/CD Pipelines

These are reference answers. Equivalent implementations are acceptable if they satisfy the requirements and preserve security boundaries.

## Lab 1: Map a pipeline

A typical flow is:

```text
Checkout
   |
   +--> Lint --------+
   |                 |
   +--> Unit tests --+--> Build --> Package/upload --> Approval --> Deploy --> Smoke test
```

Lint and unit tests can often run in parallel. Build should depend on required validation. Deployment should use a verified artifact and protected environment. A smoke test should run after deployment and should block promotion if it detects a critical failure.

## Lab 2: Pull-request validation

A minimal workflow outline:

```yaml
name: CI

on:
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: python -m pip install -r requirements.txt
      - name: Lint
        run: python -m compileall -q .
      - name: Unit tests
        run: python -m unittest discover -s tests
```

Replace the lint command and dependency installation with the project's real tools. If `requirements.txt` or `tests/` is required, fail clearly when it is missing rather than silently skipping checks.

## Lab 3: Build stage

Make the build job depend on validation with `needs: validate`. Package only the required deployable output, exclude `.git`, local configuration, secrets, caches, and test-only data, and give the artifact a traceable name such as `app-${{ github.sha }}`.

## Lab 4: Checksum

Create a checksum after packaging:

```bash
sha256sum dist/application.tar.gz > dist/application.tar.gz.sha256
sha256sum --check dist/application.tar.gz.sha256
```

A checksum helps detect accidental or malicious modification when the checksum itself is obtained from a trusted channel. It does not prove authenticity if an attacker can replace both the artifact and checksum.

## Lab 5: Reusable workflow

The called workflow declares `on: workflow_call` and an optional typed input. The caller invokes it at the job level with `uses: ./.github/workflows/reusable-tests.yml` and supplies `with:` values. A reusable workflow is useful for sharing whole jobs or multi-job processes; a composite action is useful for packaging a sequence of steps within a job.

## Lab 6: Quality gate

Use a job dependency:

```yaml
publish:
  needs: test
  runs-on: ubuntu-latest
  permissions:
    contents: read
  steps:
    - run: echo "Publish approved artifact here"
```

If publishing requires write access, grant only the specific permission at the narrowest possible job scope. Do not give every job write permissions by default.

## Lab 7: Protected staging

Configure the environment in repository settings, add reviewers and branch restrictions where available, and store deployment credentials as environment secrets. Environment protection controls when a job can access environment-scoped secrets. Repository secrets are broader in scope and may be accessible to other workflows that reference them.

## Lab 8: Build once, promote many

1. Build from a known commit.
2. Run tests and security checks.
3. Store an immutable artifact and record its checksum or digest.
4. Deploy that same artifact to staging.
5. Run smoke and acceptance tests.
6. Require approval before production.
7. Deploy the same artifact digest to production.
8. Keep a known-good prior version available for rollback.

Rebuilding separately in each environment can produce different bits and weakens traceability.

## Lab 9: Secure untrusted pull requests

Do not expose deployment secrets or write-capable tokens to code from untrusted forks. Run pull-request validation with minimal read permissions and no privileged secrets. If a workflow needs to comment on or modify pull requests, separate that privileged operation from execution of untrusted code and carefully validate all inputs. Review privileged triggers such as `pull_request_target` against current platform guidance.

## Lab 10: Smoke test

A simple pattern using `curl`:

```bash
curl --fail --silent --show-error --max-time 10 "$HEALTHCHECK_URL" \
  --output /dev/null
```

Store `HEALTHCHECK_URL` as a non-secret variable appropriate to the environment. Do not put credentials in the URL. For stronger checks, validate expected response fields without logging sensitive data.

## Lab 11: Troubleshooting

| Symptom | Possible cause | Next step |
|---|---|---|
| Workflow does not start | Trigger, branch filter, or Actions policy mismatch | Inspect `on:` filters and repository Actions settings |
| Job is skipped | Failed `if` condition or unmet `needs` dependency | Review conditions and upstream job results |
| Artifact not found | Incorrect path or build did not produce output | Inspect build logs and verify the artifact path |
| Deployment waiting | Environment reviewer or protection rule | Check environment protection settings and pending approvals |
| Local test passes, CI fails | Different runtime, dependencies, OS, or environment variables | Compare versions, lockfiles, test data, and CI logs |

## Lab 12: Risk register examples

| Finding | Impact | Likelihood | Remediation |
|---|---|---|---|
| Broad token write permissions | Unauthorized repository changes | Medium | Set explicit minimal permissions |
| Unpinned third-party actions | Unexpected code changes in CI | Medium | Review and pin to full commit SHAs |
| Secrets exposed to untrusted pull requests | Credential theft | High | Remove secret access from untrusted jobs |
| Artifact contains local configuration | Secret leakage | Medium | Use an allowlist and inspect package contents |
| No protected deployment environment | Unreviewed production changes | Medium | Add environment protections and approvals |
| No artifact integrity metadata | Difficult tamper detection | Medium | Record digest/checksum and provenance |

## Evaluation rubric

- Pipeline stages and dependencies: 20%
- Correct triggers and quality gates: 20%
- Artifact packaging and traceability: 20%
- Least privilege and secret safety: 25%
- Troubleshooting and documentation: 15%

## Official references

- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
