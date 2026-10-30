# GitLab Pipeline Hardening — Practical Exercises

Complete these exercises in a sandbox GitLab project. Use dummy secrets only. Record the control, expected result, and evidence for each task.

## Lab 1 — Build a pipeline asset inventory

**Goal:** Identify what an attacker could target.

1. Create a table of secrets, runners, artifacts, caches, deployment environments, and pipeline configuration.
2. For each item, record its owner, access path, and impact if compromised.
3. Identify which jobs receive credentials.
4. Mark all untrusted execution paths.

**Deliverable:** `pipeline-asset-inventory.md` with at least eight assets and a risk rating.

## Lab 2 — Protect the pipeline definition

1. Protect the default branch.
2. Add `CODEOWNERS` entries for `.gitlab-ci.yml` and `/ci/`.
3. Configure merge-request approvals for pipeline configuration changes.
4. Create a harmless change to `.gitlab-ci.yml` in a feature branch.
5. Verify the change cannot reach the protected branch without required review.

**Evidence:** Screenshot or exported settings and the merge-request approval history.

## Lab 3 — Configure safe CI/CD variables

1. Create a dummy variable named `STAGING_DEPLOY_TOKEN`.
2. Set it to masked and hidden where supported.
3. Protect it and scope it to `staging`.
4. Create a job targeting an unprotected feature branch and verify the protected variable is unavailable.
5. Run the same test from an authorized protected ref and verify only that the variable is present.
6. Do not print the value in either job.

**Expected result:** The secret is not exposed to unprotected refs and never appears in logs.

## Lab 4 — Test log hygiene

Create two jobs: one safe diagnostic job and one intentionally unsafe job using a dummy token only.

1. In the unsafe job, demonstrate why printing all environment variables is dangerous.
2. Remove the unsafe commands.
3. Replace them with presence checks and non-sensitive metadata.
4. Review the final logs for dummy secret disclosure.
5. Document the remediation.

**Never use a real credential in this exercise.**

## Lab 5 — Pin build dependencies

1. Identify all container images used in `.gitlab-ci.yml`.
2. Replace `latest` references with fixed versions.
3. For a production-grade example, resolve and verify image digests from the trusted registry.
4. Commit lockfiles for application dependencies.
5. Use `npm ci`, hash-verified Python requirements, or the equivalent for your language.
6. Record how updates will be reviewed.

**Deliverable:** A dependency pinning report.

## Lab 6 — Restrict job-token access

1. Open the target project's CI/CD job-token permissions.
2. Review inbound access from other projects.
3. Remove unnecessary allowlist entries in a test project.
4. Add only the consumer project required for the lab.
5. Verify the intended access succeeds and an unrelated project is denied.

**Deliverable:** Allowlist table containing consumer, target, permission need, and owner.

## Lab 7 — Separate runner trust levels

1. Create or identify an isolated runner for untrusted validation jobs.
2. Create or identify a protected runner for release jobs.
3. Mark the release runner protected and scope it to the required project/group.
4. Ensure untrusted merge-request jobs cannot select the protected runner.
5. Confirm executor isolation and that no privileged mode is enabled without a documented reason.

**Deliverable:** Runner trust-boundary diagram and configuration notes.

## Lab 8 — Protect production deployment

1. Create a `production` environment.
2. Configure it as a protected environment.
3. Restrict deploy permissions to a release group.
4. Add deployment approvals if available in your GitLab tier.
5. Add a manual deployment job with `resource_group: production`.
6. Verify an unauthorized user cannot deploy.

## Lab 9 — Review artifacts and caches

1. List artifacts and caches produced by the pipeline.
2. Check whether any contain `.env`, credentials, private keys, or unnecessary source data.
3. Set suitable artifact retention.
4. Restrict artifact access where supported.
5. Ensure protected and unprotected refs do not share sensitive caches.
6. Remove sensitive data from caches and artifacts.

## Lab 10 — Validate external communication

1. List external services contacted by pipeline jobs.
2. Verify HTTPS/TLS certificate validation.
3. Identify any insecure HTTP endpoints.
4. Restrict outbound traffic where feasible.
5. Document required endpoints and business reasons.

## Lab 11 — Pin included pipeline configuration

1. Search `.gitlab-ci.yml` for `include`.
2. Identify project, remote, and component includes.
3. Pin trusted project includes to a reviewed SHA or protected version tag.
4. Remove unused remote includes.
5. Test the pipeline after pinning.

## Lab 12 — Final hardening review

Score each control as `Implemented`, `Partial`, or `Missing`:

- Branch and tag protection
- Pipeline configuration ownership and approvals
- Secret protection and external secret storage
- Job-token allowlist
- Runner isolation
- Immutable image and dependency references
- Protected production environment
- Artifact and cache hygiene
- Log hygiene
- Security scanning
- Audit and incident response readiness

**Final deliverable:** A prioritized remediation plan with owner, due date, risk, and validation evidence for every missing control.
