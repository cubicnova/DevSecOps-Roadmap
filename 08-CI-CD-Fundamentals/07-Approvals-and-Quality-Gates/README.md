# 07 — Approvals and Quality Gates

This module explains how CI/CD pipelines use automated quality gates and human approvals to prevent unsafe or non-compliant changes from progressing to release or production.

## Learning objectives

- Explain the difference between automated quality gates and human approvals.
- Define release checks for source, tests, security, artifacts, and deployments.
- Configure a GitHub Actions job that references a protected environment.
- Explain branch protection, least privilege, and separation of duties.
- Design auditable release criteria and exception handling.
- Avoid common ways that pipeline gates can be bypassed.

## 1. What is a quality gate?

A **quality gate** is a condition that must be satisfied before the pipeline can progress. It is often automated and produces a pass/fail result.

Examples:
- Unit and integration tests pass.
- Linting and static analysis meet the project's policy.
- Dependency and secret scans meet the release threshold.
- The build artifact is created and traceable to a source commit.
- Staging smoke tests pass.
- Required status checks are successful before a pull request can merge.

A gate should be measurable, relevant to risk, and consistently enforced. Avoid checks that have no clear owner or remediation path.

## 2. What is an approval gate?

An **approval gate** requires a person or authorized process to review a proposed change or release before a protected action continues.

Examples include pull-request review, production deployment approval, security exception review, or service-owner approval of a high-impact migration.

Approvals should confirm readiness against clear criteria, not merely serve as a routine click-through.

## 3. Automated gates vs. human approvals

| Aspect | Quality gate | Approval gate |
|---|---|---|
| Typical evaluator | Automated check or policy engine | Authorized person or process |
| Example | Required tests pass | Release owner approves production |
| Main benefit | Consistency and fast feedback | Context, accountability, risk judgment |
| Evidence | Test report, scan result, status check | Reviewer identity, decision, timestamp, rationale |
| Common weakness | Poorly tuned or bypassable checks | Rubber-stamping or unclear ownership |

Use both when appropriate. Human approval does not replace automated tests or security checks.

## 4. Example release policy

A production release may require:
1. Changes arrive through a pull request.
2. Required reviewers approve the change.
3. Required CI checks pass.
4. Security findings meet the defined release policy.
5. The artifact is immutable and linked to a commit SHA.
6. Staging smoke tests pass.
7. An authorized reviewer approves the production environment.
8. Deployment health checks pass and the outcome is recorded.

Security exceptions should be time-bound, documented, approved by the appropriate owner, and accompanied by compensating controls.

## 5. GitHub Actions environments

GitHub Actions jobs can reference an environment such as `production`. The job must satisfy that environment's configured protection rules before proceeding. Depending on repository plan and visibility, rules can include required reviewers, wait timers, and allowed deployment branches or tags. Environment secrets are made available only to jobs that reference that environment and, when protection rules apply, after those rules pass.

Official documentation:
- [Deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- [Manage deployment environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
- [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

**Plan note:** GitHub feature availability varies by plan and repository visibility. Verify the options available in your repository's Settings before relying on a protection rule.

## 6. Branch protection and required checks

For a protected default branch, consider requiring:
- Pull requests instead of direct pushes.
- Independent approvals appropriate to risk.
- Required CI status checks.
- Resolution of review conversations.
- Code-owner review for sensitive paths.
- Restrictions on force pushes and branch deletion.
- No bypass except for explicitly defined, audited emergency procedures.

The required status-check names must match the checks reported by your workflows.

## 7. Security and separation of duties

- Use least-privilege `GITHUB_TOKEN` permissions.
- Keep deployment credentials out of general test jobs.
- Use environment-scoped secrets or short-lived identity where supported.
- Separate untrusted pull-request validation from privileged deployment workflows.
- Do not authorize production solely from a user-supplied workflow input.
- Prevent self-approval for sensitive releases where the platform supports it.
- Protect workflow files and policy configuration with code review.
- Record approval, commit SHA, artifact digest, target, and outcome.
- Make emergency bypasses rare, time-limited, and auditable.

## 8. Handling exceptions

An exception record should include the finding ID, affected service and release, risk assessment, compensating controls, accountable owner, authorized approver, expiry date, remediation issue, and audit evidence. Never silently ignore a failed check just to make a pipeline green.

## 9. Hands-on lab

`examples.md` includes a Python quality-gate simulation, unit tests, a GitHub Actions workflow referencing a protected `production` environment, and example review/exception records. The workflow command is a harmless placeholder; it does not deploy to a real service.

## Module files

- `README.md` — principles, policy, and security controls.
- `examples.md` — code, tests, and GitHub Actions workflow.
- `practical.md` — hands-on exercises.
- `solution.md` — suggested answers and verification steps.

## Completion checklist

- [ ] I can distinguish quality gates from approval gates.
- [ ] I can define measurable release criteria.
- [ ] I understand required status checks and branch protection.
- [ ] I can explain protected environments.
- [ ] I can document and govern a security exception.
- [ ] I can design least-privilege and auditable release approvals.
