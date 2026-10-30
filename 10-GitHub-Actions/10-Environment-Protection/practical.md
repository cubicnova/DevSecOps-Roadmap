# Environment Protection — Practical Exercises

## Prerequisites
- A GitHub repository where you can edit workflows and repository settings.
- Basic YAML and GitHub Actions knowledge.
- A harmless sample application or `echo`-only deployment workflow.
- Never use production credentials in these labs.

> Feature availability for private repositories depends on the GitHub plan. If a protection option is unavailable, document the limitation and complete the conceptual exercise.

## Lab 1: Create environments
**Objective:** Create `development`, `staging`, and `production`.

1. Open **Settings → Environments**.
2. Create all three environments.
3. Record the intended purpose of each.
4. Verify exact spelling.

**Expected result:** Three distinct environment targets appear in repository settings.

## Lab 2: Attach a job to staging
1. Create `.github/workflows/staging.yml`.
2. Add a `workflow_dispatch` trigger.
3. Add a job with `environment: staging`.
4. Run the workflow manually.
5. Inspect the Actions run and deployment details.

**Expected result:** The job targets the configured staging environment.

## Lab 3: Configure production reviewers
1. Open production environment settings.
2. Add required reviewers where supported.
3. Enable prevention of self-review if available.
4. Save the protection rules.
5. Run a job targeting production.
6. Observe the pending approval state.
7. Have an authorized reviewer approve or reject it.

**Expected result:** The job waits until the required protection rule passes.

## Lab 4: Test branch restrictions
1. Configure production to allow only `main`.
2. Trigger a production-targeting workflow from `main`.
3. If safe and permitted, test a feature branch against a separate test environment.
4. Record accepted and rejected refs.

**Expected result:** Disallowed refs cannot deploy to the protected environment.

## Lab 5: Add environment secrets and variables
1. Add a dummy `DEPLOY_TOKEN` secret to staging.
2. Add `DEPLOY_REGION`, such as `ap-south-1`, as an environment variable.
3. Read them using `${{ secrets.DEPLOY_TOKEN }}` and `${{ vars.DEPLOY_REGION }}`.
4. Confirm the secret is present without printing it.
5. Do not use the dummy value with a real service.

**Expected result:** The job uses environment-scoped configuration without exposing the secret.

## Lab 6: Compare staging and production credentials
1. Create different dummy tokens for staging and production.
2. Store each token only in its matching environment.
3. Create jobs targeting each environment.
4. Check only whether each token is non-empty.
5. Explain why sharing a high-privilege credential increases risk.

**Expected result:** Each job receives the configuration intended for its target.

## Lab 7: Serialize production deployments
1. Add `concurrency.group: production-deployment`.
2. Set `cancel-in-progress: false`.
3. Start two workflow runs close together.
4. Observe how the concurrency group handles them.
5. Explain why concurrency is not automatically implied by `environment: production`.

**Expected result:** Jobs in the same concurrency group do not run simultaneously.

## Lab 8: Add pre-deployment validation
1. Add a job that runs tests and security checks.
2. Make production depend on it with `needs:`.
3. Configure production protection rules.
4. Confirm production does not run when validation fails.
5. Explain automated checks versus human approval.

**Expected result:** Failed validation blocks the dependent production job.

## Lab 9: Troubleshoot an unavailable secret
1. Run a test job without an `environment` key.
2. Check whether the environment secret is available.
3. Add `environment: staging` and rerun.
4. If approval is required, observe when the secret becomes available.
5. Record why the first job could not access the environment secret.

**Expected result:** You can explain the environment reference and protection requirements.

## Lab 10: Security review
- [ ] Production branch/tag restrictions are configured.
- [ ] Approval rules are enabled where available.
- [ ] Self-review is prevented where appropriate.
- [ ] Environment secrets are scoped and credentials are separate.
- [ ] Logs and artifacts contain no secret values.
- [ ] Workflow permissions are least-privilege.
- [ ] Production concurrency is configured.
- [ ] Self-hosted runners are treated as trusted infrastructure.
- [ ] Bypass permissions are understood and controlled.

## Lab deliverables
1. Screenshots of environments with secret values hidden.
2. Workflow YAML for staging and production.
3. A note explaining configured protection rules.
4. Results of branch restriction and concurrency tests.
5. A short security review listing gaps and remediation actions.
