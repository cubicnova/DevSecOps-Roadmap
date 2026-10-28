# Runner and Agent Security — Examples

These examples focus on safe configuration and threat modeling. They do not attack a runner, access real credentials, or modify production systems.

## 1. Minimal-permission GitHub Actions workflow

Create `.github/workflows/runner-security.yml` at the repository root:

```yaml
name: Runner Security Basics

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  validate:
    name: Safe validation job
    runs-on: ubuntu-latest
    steps:
      - name: Check out source
        uses: actions/checkout@v4

      - name: Show execution context
        run: |
          python --version
          git --version

      - name: Run tests
        run: python -m unittest -v
```

This is a basic example. It gives the workflow read-only repository contents access and does not configure deployment credentials. For production, review and pin third-party actions to full commit SHAs. Keep the test code and dependencies trustworthy, and treat pull-request content as untrusted.

## 2. A safe runner-risk model

Create `runner_risk.py`:

```python
from dataclasses import dataclass


@dataclass
class RunnerContext:
    untrusted_code: bool
    has_production_secret: bool
    persistent_host: bool
    private_network_access: bool


def assess_runner(context: RunnerContext) -> list[str]:
    """Return risk observations; this is a teaching model, not a scanner."""
    risks = []

    if context.untrusted_code and context.has_production_secret:
        risks.append("Untrusted code can access a production secret")

    if context.untrusted_code and context.persistent_host:
        risks.append("Untrusted code may leave persistent host changes")

    if context.untrusted_code and context.private_network_access:
        risks.append("Untrusted code may reach private network services")

    if not risks:
        risks.append("No modeled high-risk combination detected; review other controls")

    return risks


if __name__ == "__main__":
    example = RunnerContext(
        untrusted_code=True,
        has_production_secret=True,
        persistent_host=True,
        private_network_access=True,
    )

    for risk in assess_runner(example):
        print(f"RISK: {risk}")
```

Run:

```bash
python runner_risk.py
```

The script should identify the modeled risks. This simple exercise is not a comprehensive risk assessment.

## 3. Unit tests for the risk model

Create `test_runner_risk.py`:

```python
import unittest
from runner_risk import RunnerContext, assess_runner


class TestRunnerRisk(unittest.TestCase):
    def test_untrusted_code_with_secret_is_flagged(self):
        context = RunnerContext(True, True, False, False)
        self.assertTrue(any("production secret" in r for r in assess_runner(context)))

    def test_persistent_host_is_flagged_for_untrusted_code(self):
        context = RunnerContext(True, False, True, False)
        self.assertTrue(any("persistent host" in r for r in assess_runner(context)))

    def test_private_network_is_flagged_for_untrusted_code(self):
        context = RunnerContext(True, False, False, True)
        self.assertTrue(any("private network" in r for r in assess_runner(context)))

    def test_low_risk_combination_returns_review_message(self):
        context = RunnerContext(False, False, False, False)
        self.assertTrue(assess_runner(context))


if __name__ == "__main__":
    unittest.main()
```

Run:

```bash
python -m unittest -v
```

## 4. Safer job separation

A useful design separates untrusted validation from privileged deployment. This illustration shows only the validation side:

```yaml
name: Pull Request Validation

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
      - name: Run safe checks
        run: python -m unittest -v
```

Do not add production secrets to this job. Put deployment in a separate trusted workflow or job with protected environment rules, restricted triggers, minimal permissions, and a narrowly scoped identity. Review the trust boundary carefully before passing artifacts between workflows.

## 5. Workflow review checklist

When reviewing a pipeline, ask:

- Does any job run code from an untrusted pull request?
- Could that job access deployment secrets or a cloud identity?
- Is the runner reused across unrelated trust levels?
- Does the runner have unnecessary access to internal networks?
- Are workflow token permissions broader than required?
- Are third-party actions and dependencies reviewed and pinned?
- Can untrusted code alter or poison a cache consumed by a privileged job?
- Are logs or artifacts likely to contain sensitive information?
- Are build outputs traceable to a commit and workflow run?
- Can a compromised runner be isolated and rebuilt quickly?

## 6. Example runner policy

```yaml
runner_policy:
  untrusted_pull_requests:
    use_isolated_runner: true
    production_secrets: false
    private_network_access: false
  release_jobs:
    use_protected_workflow: true
    require_approved_source: true
    use_short_lived_identity: true
  all_jobs:
    minimal_token_permissions: true
    retain_security_logs: true
    record_artifact_digest: true
```

This is illustrative policy data, not a native GitHub configuration file.

## Security notes

- Do not echo environment variables or print credentials for debugging.
- Never store tokens in the repository or test fixtures.
- Avoid running untrusted code on privileged self-hosted runners.
- Prefer disposable runners for untrusted workloads.
- If a credential was exposed, revoke or rotate it; deleting the visible string is not sufficient.
