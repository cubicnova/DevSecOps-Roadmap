# Approvals and Quality Gates — Suggested Solutions

These are sample answers. Adapt policies to the project's risk, compliance obligations, and repository capabilities.

## Solution 1 — Gate or approval?

| Item | Classification | Why |
|---|---|---|
| Unit tests pass | Automated quality gate | Test runner returns a pass/fail result |
| Release manager approves production | Human approval | Authorized person accepts release risk |
| Dependency scan meets policy | Automated quality gate | Findings are evaluated against thresholds |
| Service owner reviews risky migration | Human approval plus automated checks | Human reviews impact; migration tests can also gate progress |
| Staging smoke tests pass | Automated quality gate | Critical paths are verified by executable checks |

## Solution 2 — Run the quality gate

Run:

```bash
python quality_gate.py
python -m unittest -v
```

The script should print `Passed: True` and state that all required checks passed. The test suite should report four passing tests.

## Solution 3 — Simulate a blocked release

For example:

```python
result = evaluate_release(
    tests_passed=True,
    security_gate_passed=False,
    artifact_traceable=True,
)
```

The gate returns `passed=False` and names `security` as a failed check. Required gates should fail closed: missing, failed, or unknown evidence should not be treated as success unless an explicitly governed policy says otherwise.

## Solution 4 — Add a new quality check

Update the function signature and checks dictionary:

```python
def evaluate_release(
    tests_passed: bool,
    security_gate_passed: bool,
    artifact_traceable: bool,
    staging_smoke_tests_passed: bool,
) -> GateResult:
    checks = {
        "tests": tests_passed,
        "security": security_gate_passed,
        "artifact_traceability": artifact_traceable,
        "staging_smoke_tests": staging_smoke_tests_passed,
    }
    # Keep the same failed-check handling below.
```

Update all calls and add tests for both `True` and `False`.

## Solution 5 — GitHub Actions workflow

Store the workflow at:

```text
.github/workflows/quality-gates.yml
```

Commit and push:

```bash
git add quality_gate.py test_quality_gate.py .github/workflows/quality-gates.yml
git commit -m "Add approval and quality gate examples"
git remote -v
git push origin main
```

If no remote exists, add your test repository URL first. Update branch filters if the default branch is not `main`.

## Solution 6 — Protected environment

In repository **Settings → Environments**, create `production` and configure required reviewers and self-review prevention if the plan and repository visibility support those controls. Restrict deployment branches/tags where appropriate.

A job referencing `environment: production` must satisfy the configured protection rules before it proceeds. Environment secrets are not available to that job until those rules pass. See [GitHub's deployment and environment documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

## Solution 7 — Branch protection

A suitable default-branch policy can require:
- Pull requests before merge.
- One or more independent approving reviews.
- Required CI status checks.
- Code-owner review for sensitive files.
- Conversation resolution.
- No force pushes or deletion.

Require the exact check names reported by Actions. Test settings in a practice repository and limit emergency bypass permissions.

## Solution 8 — Separate permissions

| Job | Example permission | Reason |
|---|---|---|
| Test | `contents: read` | Checkout and test source |
| Deploy | Only the exact permissions needed | Publish or deploy artifact |
| Approval | Environment protection rules | Enforce authorized approval before protected job proceeds |

Do not grant broad write permissions to every job. Use environment-scoped secrets or short-lived identity, and never expose deployment credentials to untrusted pull-request code.

## Solution 9 — Design security gates

A sample policy might include:
- Secret scanning: block newly introduced credentials and rotate exposed secrets.
- Dependency scanning: block vulnerabilities meeting the project's release-blocking severity policy.
- Static analysis: fail on defined high-confidence, high-severity findings.
- Container scanning: block images that violate release policy.
- Infrastructure-as-code scanning: block unsafe public exposure or excessive privileges.

Thresholds should be documented and owned. A clean scan does not prove software is secure.

## Solution 10 — Production reviewer checklist

The reviewer should confirm:
1. Change summary and intended impact are clear.
2. Required CI checks passed.
3. Security results meet policy or have approved, time-bound exceptions.
4. Artifact digest and source commit are recorded.
5. Staging and smoke tests passed.
6. Data migrations and backward compatibility were reviewed.
7. Monitoring and alert ownership are known.
8. Rollback or roll-forward procedures are feasible.
9. Target environment and release window are correct.
10. The reviewer has authority to approve the release.

## Solution 11 — Exception record

Use fictional identifiers only in a lab. A real exception must identify the finding, affected service/release, risk, compensating controls, accountable owner, authorized approver, expiry date, and remediation ticket. It should be reviewed at expiry rather than silently becoming permanent.

## Solution 12 — Approval bypass scenario

An input such as `approved=true` is user-supplied workflow data, not proof that an authorized reviewer accepted the risk. A person who can start a workflow may be able to set the input.

Use platform-enforced environment protection, authorized reviewers, branch restrictions, least-privilege credentials, and audit logs. Prevent self-review where supported. Protect workflow definitions so a change cannot simply remove the gate.

## Solution 13 — Audit trail

Record:
- Full source commit SHA.
- Artifact version and digest.
- Workflow run ID and link.
- Target environment.
- Approval decision, reviewer identity, and timestamp.
- Automated gate results and report references.
- Deployment time and outcome.
- Rollback event or incident reference, if applicable.

Keep records in an approved system with appropriate access controls and retention.

## Stretch challenge guidance

- **Mandatory gate policy:** explicitly list required gates and test that omission causes failure.
- **Environment-specific policy:** use stricter controls for production than development, with documented rationale.
- **CODEOWNERS:** require relevant owners to review workflow and policy changes.
- **Break-glass:** require restricted access, documented reason, incident/ticket reference, audit evidence, and post-event review.
- **Plan limitations:** verify available GitHub settings directly; do not assume every protection feature is available for every plan and repository visibility.

## Final review

Good approval and quality-gate design combines measurable automated checks, independent human judgment for meaningful risks, least privilege, protected workflow configuration, and a complete audit trail.
