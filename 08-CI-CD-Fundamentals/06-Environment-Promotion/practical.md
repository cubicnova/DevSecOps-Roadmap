# Practical Exercises — Environment Promotion

**Level:** Beginner to intermediate  
**Environment:** A test Git repository and optional GitHub Actions workflow. Use only non-production targets unless you have explicit authorization.

## Exercise 1 — Map your environments

Design an environment flow for a small web API. Include development, test, staging, and production—or justify a smaller set.

For each environment, document:

- Purpose and owner
- Infrastructure or service target
- Data classification
- Configuration source
- Secrets and identity
- Tests performed
- Promotion criteria

**Deliverable:** An environment matrix and a diagram.

## Exercise 2 — Distinguish build, deployment, and release

Classify each event as primarily a build, deployment, or release action. Explain any overlap.

1. Compile the application from a commit.
2. Upload a container image to a registry.
3. Install the image into staging.
4. Enable the feature for all users.
5. Deploy a new version but leave a feature flag disabled.
6. Move an approved artifact digest from staging to production.

## Exercise 3 — Define promotion gates

Create a promotion policy for staging-to-production. Include at least:

- Required tests
- Vulnerability thresholds
- Artifact identity/digest verification
- Staging health checks
- Change approval requirements
- Rollback readiness
- Exception owner and expiry

**Deliverable:** A checklist or policy document that a reviewer could use consistently.

## Exercise 4 — Configure GitHub Actions environments

In a test repository you control:

1. Open **Settings → Environments**.
2. Create `staging` and `production`.
3. Configure branch/tag restrictions where supported.
4. Add a non-sensitive environment variable to staging.
5. If your repository plan and visibility support it, configure required reviewers for production.
6. Create a small workflow that references each environment.
7. Observe whether environment protection rules block the relevant job until satisfied.

**Important:** Feature availability depends on repository visibility and plan. Never put a real production secret into this exercise.

**Deliverable:** Screenshots or notes showing environment configuration and workflow behavior.

## Exercise 5 — Use a promotion workflow

Start from the workflow in `examples.md`.

1. Run the manual workflow in a test repository.
2. Confirm that validation runs before staging.
3. Replace placeholder commands only when you have a safe test deployment target.
4. Add a real staging smoke test.
5. Configure the production environment gate.
6. Confirm production cannot proceed when staging fails or approval is missing.

**Deliverable:** Workflow file and evidence of at least one successful and one blocked run.

## Exercise 6 — Build once, promote many

**Scenario:** Your current pipeline builds separate images for staging and production.

Design a replacement that:

1. Builds one image from a reviewed commit.
2. Publishes it to a registry.
3. Records its digest.
4. Deploys that digest to staging.
5. Runs validation.
6. Promotes the same digest to production after approval.

**Questions:** How will the pipeline prove that staging and production use the same artifact? What configuration can differ between environments?

## Exercise 7 — Create an environment configuration matrix

Document at least eight settings for development, staging, and production. Include endpoints, database settings, debug mode, credentials/identity, logging, feature flags, and monitoring.

Mark each setting as:

- Same across environments
- Environment-specific non-secret configuration
- Secret or credential
- Restricted production-only configuration

Never enter actual credentials into the deliverable.

## Exercise 8 — Design an approval model

Define who may approve production promotion and who may execute it.

Address:

- Separation of duties
- Self-approval restrictions where required
- Change ticket or release notes
- Emergency release procedure
- Audit trail
- Exception expiry and post-release review

Explain why a manual approval is not a substitute for automated tests.

## Exercise 9 — Plan rollback

Assume a release passes staging but production error rates rise after deployment.

Write a rollback plan that includes:

- Signal and threshold
- Alert recipient
- Rollback decision authority
- Previous known-good artifact digest
- Traffic/deployment reversal
- Database migration compatibility
- Verification after rollback
- Communication and incident records

## Exercise 10 — Find promotion risks

Review this hypothetical design:

- Production is rebuilt from the source branch after staging succeeds.
- All environments share the same administrator credential.
- Staging uses production customer data without approval.
- The production deployment job has no approval gate.
- The release tag can be overwritten.
- No health check runs after deployment.
- The prior release artifact is deleted immediately.

Identify at least six risks and propose a mitigation for each.

## Exercise 11 — Write a release record

Create a sample release record with:

- Application name
- Source commit
- Artifact repository and digest
- Staging test result
- Security gate result
- Approver or policy decision
- Change reference, if used
- Production deployment time
- Health verification result
- Rollback version

Use placeholders or sample values only. Do not include secrets.

## Exercise 12 — Mini project: environment promotion pipeline

Design a promotion pipeline for a sample Flask API or static website.

Required deliverables:

- `environment-promotion.md` with architecture diagram
- Environment matrix
- CI workflow and promotion workflow
- Artifact identity strategy
- Promotion gates and approval model
- Configuration/secrets plan
- Failure and rollback matrix
- Release record template

**Evaluation rubric (100 points):**

| Area | Points |
|---|---:|
| Environment model and architecture | 15 |
| Build-once artifact promotion | 20 |
| Automated quality and security gates | 15 |
| Secrets and identity isolation | 15 |
| Approval and audit trail | 10 |
| Health checks and rollback | 20 |
| Documentation clarity | 5 |

## Submission checklist

- [ ] Environments have clear purposes and owners.
- [ ] Promotion gates are explicit and testable.
- [ ] The same artifact is promoted between environments.
- [ ] Environment secrets are scoped and not committed.
- [ ] Production approval rules are documented.
- [ ] Health checks and rollback are defined.
- [ ] Release records capture the artifact identity and decision.
