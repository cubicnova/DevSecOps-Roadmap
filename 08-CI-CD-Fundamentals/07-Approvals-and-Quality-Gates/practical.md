# Approvals and Quality Gates — Practical Exercises

Use a personal test repository. Keep deployment commands harmless and do not use production credentials.

## Lab setup

Requirements: Python 3.10+, Git, and GitHub for the optional workflow exercise.

Create `quality_gate.py` and `test_quality_gate.py` using `examples.md`.

## Exercises

### Exercise 1 — Gate or approval?
Classify each as an automated quality gate, human approval, or both:
- Unit tests pass.
- A release manager approves production.
- Dependency scan meets policy.
- A service owner reviews a risky database migration.
- Staging smoke tests pass.

**Deliverable:** A table with classification and rationale.

### Exercise 2 — Run the quality gate
Run:

```bash
python quality_gate.py
python -m unittest -v
```

Record the outputs and explain what each required check represents.

### Exercise 3 — Simulate a blocked release
Change one argument passed to `evaluate_release()` to `False`.

**Deliverable:** Show which failed condition blocks the release and why required checks should fail closed.

### Exercise 4 — Add a new quality check
Extend `evaluate_release()` with `staging_smoke_tests_passed`.

**Deliverable:** Add tests for both pass and fail cases.

### Exercise 5 — Add the GitHub Actions workflow
Create `.github/workflows/quality-gates.yml` from `examples.md` and push it to a test repository.

**Deliverable:** A successful automated quality job.

### Exercise 6 — Configure a protected environment
Create a `production` environment. Where supported, add a required reviewer and enable prevention of self-review.

**Deliverable:** Explain what happens while approval is pending. If the feature is unavailable on your plan/repository visibility, document the limitation rather than claiming it is enabled.

### Exercise 7 — Protect the default branch
Configure branch protection or repository rules for pull requests, required reviews, and required status checks.

**Deliverable:** List the policy settings and exact required status-check names.

### Exercise 8 — Separate build and deployment permissions
Design separate jobs for tests and production deployment. Give the test job read-only source access and only the deployment job the permissions it needs.

**Deliverable:** A permissions table and justification.

### Exercise 9 — Design security gates
Choose appropriate source, dependency, secret, container, or infrastructure checks for a sample application.

**Deliverable:** Purpose, severity threshold, owner, and failure behavior for each check.

### Exercise 10 — Create an approval checklist
Write a checklist for a production reviewer covering change summary, test results, scan results, artifact digest, staging verification, impact, monitoring, and rollback.

### Exercise 11 — Document an exception
Use the example exception record and fill it with clearly fictional data.

**Deliverable:** A time-bound exception with risk, compensating controls, owner, approver role, expiry, and remediation issue. Do not represent fictional data as a real approval.

### Exercise 12 — Review a bypass scenario
A workflow accepts `approved=true` and deploys if the input is true.

**Deliverable:** Explain why this is not reliable authorization and describe how to use protected environments and access controls instead.

### Exercise 13 — Audit trail
Design a release record that connects approval to the exact version deployed.

**Deliverable:** Include commit SHA, artifact digest, environment, approver, timestamp, workflow run, outcome, and rollback reference.

## Stretch challenges

- Add a policy test that fails when a mandatory gate is missing.
- Define different gate thresholds for development, staging, and production.
- Add CODEOWNERS rules for workflow and security-policy files.
- Design a break-glass process with restricted access, incident ticket, audit evidence, and post-event review.
- Research how your repository plan supports environments and required reviewers.

## Submission checklist

- [ ] Quality gate logic and tests work.
- [ ] Required checks block later stages when they fail.
- [ ] Protected environment is configured where available.
- [ ] Branch protection requires intended reviews and checks.
- [ ] Deployment permissions are limited.
- [ ] Approval and exception evidence is auditable.
- [ ] No real secrets or production changes were used in the lab.
