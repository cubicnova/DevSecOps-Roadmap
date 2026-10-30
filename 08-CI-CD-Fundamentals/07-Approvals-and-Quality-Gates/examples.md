# Approvals and Quality Gates — Examples

These examples are for learning in a test repository. The workflow uses a harmless placeholder and does not deploy to production.

## 1. Python quality-gate function

Create `quality_gate.py`:

```python
from dataclasses import dataclass


@dataclass
class GateResult:
    name: str
    passed: bool
    reason: str


def evaluate_release(
    tests_passed: bool,
    security_gate_passed: bool,
    artifact_traceable: bool,
) -> GateResult:
    """Allow a release only when all required checks pass."""
    checks = {
        "tests": tests_passed,
        "security": security_gate_passed,
        "artifact_traceability": artifact_traceable,
    }

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        return GateResult(
            name="release-readiness",
            passed=False,
            reason="Failed checks: " + ", ".join(failed),
        )

    return GateResult(
        name="release-readiness",
        passed=True,
        reason="All required automated checks passed",
    )


if __name__ == "__main__":
    result = evaluate_release(True, True, True)
    print(f"Passed: {result.passed}")
    print(result.reason)
```

Run:

```bash
python quality_gate.py
```

Expected output:

```text
Passed: True
All required automated checks passed
```

This is a policy simulation, not a security scanner or an actual approval system.

## 2. Unit tests

Create `test_quality_gate.py`:

```python
import unittest
from quality_gate import evaluate_release


class TestReleaseGate(unittest.TestCase):
    def test_all_checks_pass(self):
        result = evaluate_release(True, True, True)
        self.assertTrue(result.passed)

    def test_failed_tests_block_release(self):
        result = evaluate_release(False, True, True)
        self.assertFalse(result.passed)
        self.assertIn("tests", result.reason)

    def test_security_failure_blocks_release(self):
        result = evaluate_release(True, False, True)
        self.assertFalse(result.passed)
        self.assertIn("security", result.reason)

    def test_missing_traceability_blocks_release(self):
        result = evaluate_release(True, True, False)
        self.assertFalse(result.passed)
        self.assertIn("artifact_traceability", result.reason)


if __name__ == "__main__":
    unittest.main()
```

Run:

```bash
python -m unittest -v
```

All four tests should pass.

## 3. GitHub Actions workflow with an approval gate

Create `.github/workflows/quality-gates.yml` at the repository root:

```yaml
name: Quality Gates and Approval

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  quality:
    name: Automated quality checks
    runs-on: ubuntu-latest
    steps:
      - name: Check out source
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Run unit tests
        run: python -m unittest -v
      - name: Validate syntax
        run: python -m compileall -q .

  production-approval:
    name: Protected production gate
    if: github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main'
    needs: quality
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
    steps:
      - name: Confirm approval gate passed
        run: echo "Environment protection rules passed; deployment step would run here."
```

### Configure the environment

1. Open **Settings → Environments** in your test repository.
2. Create an environment named `production`.
3. If your plan and repository visibility support it, configure required reviewers and prevent self-review.
4. Restrict deployment branches/tags to the intended release source where supported.
5. Add environment secrets only if a real deployment needs them; this lab does not need secrets.
6. Save the rules.

When the workflow is manually started from `main`, the `production-approval` job waits for configured environment protection rules. The command after approval is only a message, not a deployment.

**Important:** Plan and repository visibility affect feature availability. Confirm your repository's actual Settings. A workflow condition is not a substitute for environment protection, branch rules, or least-privilege credentials.

For production, review and pin third-party actions to full commit SHAs rather than relying only on major-version references.

## 4. Branch protection checklist

A typical protected branch policy may require:
- Pull requests before merging.
- Required approving reviews.
- Required CI status checks.
- Code-owner review for sensitive files.
- Conversation resolution.
- Restrictions on force pushes and branch deletion.

Set the exact checks reported by your repository's workflows.

## 5. Example release approval record

```yaml
release:
  service: sample-api
  version: "1.4.2"
  commit_sha: "REPLACE_WITH_FULL_COMMIT_SHA"
  artifact_digest: "sha256:REPLACE_WITH_REAL_DIGEST"
  target_environment: production
  automated_gates:
    tests: passed
    security_scan: passed
    staging_smoke_tests: passed
  approval:
    status: pending
    reviewer: "REPLACE_WITH_AUTHORIZED_REVIEWER"
    rationale: "Review release notes, risk, and verification evidence before approval."
  rollback_plan: "Restore the last known-good artifact if health checks fail."
```

This is illustrative YAML. Replace placeholders with real release metadata in an approved system; never fabricate approval evidence.

## 6. Example time-bound exception record

```yaml
exception:
  id: SEC-EXCEPTION-001
  finding: "REPLACE_WITH_FINDING_ID"
  service: sample-api
  release: "1.4.2"
  risk: "Document impact and likelihood"
  compensating_controls:
    - "Document temporary mitigation"
  owner: "REPLACE_WITH_ACCOUNTABLE_OWNER"
  approved_by: "REPLACE_WITH_AUTHORIZED_APPROVER"
  expires_on: "YYYY-MM-DD"
  remediation_issue: "REPLACE_WITH_TRACKING_ISSUE"
```

A real exception should have a valid owner, approver, expiry, and remediation record.

## 7. Anti-patterns

| Anti-pattern | Safer alternative |
|---|---|
| Deploy even if tests fail | Make tests a required job dependency |
| Approval by the initiator of a sensitive deployment | Enable self-review prevention where available |
| Everyone has production credentials | Scope credentials to the protected deployment job |
| Scan failures ignored indefinitely | Define severity policy, owner, expiry, and exception process |
| Workflow file can be modified without review | Protect workflow and policy files with code review |
| `approved=true` input authorizes production | Use platform-enforced protection and authorized reviewers |
