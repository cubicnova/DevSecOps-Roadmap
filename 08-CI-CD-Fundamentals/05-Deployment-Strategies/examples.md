# Deployment Strategies — Examples

These examples demonstrate deployment logic locally and show how deployment gates fit into CI/CD. They do not connect to or modify a real production system.

## 1. Blue-green deployment simulation

Create `blue_green.py`:

```python
from dataclasses import dataclass


@dataclass
class Environment:
    name: str
    version: str
    healthy: bool = True


def select_target(active: str) -> str:
    """Return the inactive environment name."""
    if active == "blue":
        return "green"
    if active == "green":
        return "blue"
    raise ValueError("active must be 'blue' or 'green'")


def switch_traffic(target: Environment) -> str:
    """Switch only when the target passes its health check."""
    if not target.healthy:
        raise RuntimeError(f"{target.name} failed health checks")
    return target.name


if __name__ == "__main__":
    blue = Environment("blue", "1.0.0", healthy=True)
    green = Environment("green", "1.1.0", healthy=True)

    active = "blue"
    target_name = select_target(active)
    target = green if target_name == "green" else blue

    print(f"Active: {active} ({blue.version})")
    print(f"Candidate: {target.name} ({target.version})")
    active = switch_traffic(target)
    print(f"Traffic switched to: {active}")
```

Run:

```bash
python blue_green.py
```

Expected final line:

```text
Traffic switched to: green
```

This is only a logic simulation; it does not configure a load balancer or create infrastructure.

## 2. Test the blue-green logic

Create `test_blue_green.py`:

```python
import unittest
from blue_green import Environment, select_target, switch_traffic


class TestBlueGreen(unittest.TestCase):
    def test_select_inactive_environment(self):
        self.assertEqual(select_target("blue"), "green")
        self.assertEqual(select_target("green"), "blue")

    def test_reject_invalid_active_environment(self):
        with self.assertRaises(ValueError):
            select_target("yellow")

    def test_switch_to_healthy_target(self):
        target = Environment("green", "1.1.0", healthy=True)
        self.assertEqual(switch_traffic(target), "green")

    def test_do_not_switch_to_unhealthy_target(self):
        target = Environment("green", "1.1.0", healthy=False)
        with self.assertRaises(RuntimeError):
            switch_traffic(target)


if __name__ == "__main__":
    unittest.main()
```

Run:

```bash
python -m unittest -v
```

## 3. Canary rollout decision simulation

Create `canary.py`:

```python
def should_continue(error_rate: float, max_error_rate: float = 0.02) -> bool:
    """Return whether the rollout meets the configured error-rate gate."""
    if not 0 <= error_rate <= 1:
        raise ValueError("error_rate must be between 0 and 1")
    if not 0 <= max_error_rate <= 1:
        raise ValueError("max_error_rate must be between 0 and 1")
    return error_rate <= max_error_rate


if __name__ == "__main__":
    observed_error_rate = 0.01
    if should_continue(observed_error_rate):
        print("Gate passed: rollout may continue")
    else:
        print("Gate failed: pause rollout and investigate")
```

This simplified example illustrates a decision rule only. Real canary analysis should compare appropriate metrics against a baseline, use an observation window, consider traffic volume, and evaluate more than one signal.

## 4. GitHub Actions deployment gate example

A workflow can run tests on pushes and pull requests, while deployment is limited to a protected environment and a release event. This is a **template**; replace the placeholder deployment command with the deployment process for your platform.

```yaml
name: Test and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m unittest -v

  deploy:
    if: github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Deployment placeholder
        run: echo "Replace this with your approved deployment command"
```

Configure the `production` environment in repository settings with appropriate required reviewers and protection rules. A manual trigger alone is not a complete security boundary; enforce branch rules, environment protection, least privilege, and platform-specific access controls.

The example uses major-version action references for readability. For production, review and pin third-party actions to full commit SHAs.

## 5. Example rollout plan

For a low-risk web service:

1. Build and test one immutable artifact.
2. Deploy it to staging.
3. Run smoke tests and verify key application flows.
4. Start a canary at a small traffic percentage, if supported.
5. Monitor error rate, latency, resource saturation, and business-critical requests.
6. Expand traffic only when predefined gates pass.
7. Pause or roll back if a gate fails.
8. Record artifact digest, commit, deployment time, and outcome.

## 6. Rollback checklist

Before a release, answer:

- What metric or failure triggers a pause or rollback?
- Who can stop the rollout?
- Can traffic be returned to the previous version safely?
- Are database migrations backward-compatible?
- Are background workers and queues compatible with both versions?
- How will the team verify recovery?
- Where are deployment logs and artifact identifiers recorded?

## Security notes

- Do not place credentials in workflow YAML.
- Use repository/environment secrets or short-lived workload identity.
- Do not expose deployment secrets to untrusted pull requests.
- Avoid logging tokens or sensitive environment variables.
- Make sure the actual production environment is protected and that rollback has been tested.
