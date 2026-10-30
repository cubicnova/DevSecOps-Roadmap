# GitLab Protected Environments — Practical Exercises

## Prerequisites
- A GitLab project with CI/CD enabled.
- A working GitLab Runner.
- Maintainer permissions for configuring protected environments, or an instructor who can configure them.
- A test project and harmless deployment commands.
- Check your GitLab plan: protected environments and deployment approvals are tier-dependent.

## Lab 1: Create staging and production environments
1. Add a staging deployment job to `.gitlab-ci.yml`.
2. Add a production deployment job.
3. Run the pipeline.
4. Open **Operate → Environments**.
5. Confirm both environments appear.

**Expected result:** GitLab records the two deployment targets.

## Lab 2: Protect production
1. Open **Settings → CI/CD**.
2. Expand **Protected environments**.
3. Select **Protect an environment**.
4. Choose `production`.
5. Set **Allowed to deploy** to a restricted role, user, or group.
6. Save the configuration.

**Expected result:** Production is protected and only configured principals can deploy.

## Lab 3: Compare deployment permissions
1. Use test accounts with different project roles, if available.
2. Attempt a production deployment as an authorized deployer.
3. Attempt it as a user not in the allowed list.
4. Record the result and relevant error message.
5. Do not grant broad access just to make the test pass.

**Expected result:** You can explain how the Allowed to deploy policy is enforced.

## Lab 4: Configure deployment approvals
1. Open the protected production environment settings.
2. Add an approver or approver group.
3. Configure the required number of approvals.
4. Trigger a deployment.
5. Inspect its status in **Operate → Environments**.
6. Have an authorized approver approve or reject it.
7. If approved, manually run the deployment job if GitLab requires it.

**Expected result:** A deployment remains blocked until the configured approval requirements are met.

## Lab 5: Test separation of duties
1. Use one account to trigger the pipeline.
2. Configure another account as an approver.
3. Verify the triggerer cannot self-approve by default.
4. Record the approval identity and status.
5. Discuss when, if ever, self-approval should be permitted.

**Expected result:** You understand separation between deployment initiation and approval.

## Lab 6: Add a branch guard
1. Protect the default branch in repository settings.
2. Add a `rules` condition allowing production only from the default branch.
3. Trigger a pipeline from the default branch.
4. Test a feature branch using a non-production environment.
5. Explain why the YAML rule and environment policy are separate controls.

**Expected result:** Production deployments are restricted through both pipeline logic and GitLab settings.

## Lab 7: Scope production credentials
1. Create a dummy `DEPLOY_TOKEN`.
2. Mark it protected and scope it to `production`, where supported.
3. Add a job that checks only whether the variable is present.
4. Run from an eligible protected ref and a non-protected ref.
5. Never print the token value.

**Expected result:** You understand the relationship between protected refs, environment scopes, and secret availability.

## Lab 8: Test deployment-only access
1. Create or identify a group intended for release operators.
2. Invite it to the project using the minimum supported role.
3. Add the group to the protected environment's Allowed to deploy list.
4. Test whether members can deploy without receiving unnecessary repository write access.
5. Document any role or membership prerequisites.

**Expected result:** You can describe deployment-only access and its limitations.

## Lab 9: Add deployment tier metadata
1. Add `deployment_tier: staging` to the staging job.
2. Add `deployment_tier: production` to the production job.
3. Run both jobs.
4. Inspect environment details.
5. Explain how tier metadata can support group-level protection policies.

**Expected result:** Environments are classified with appropriate deployment tiers.

## Lab 10: Troubleshoot a protected trigger job
1. Create a downstream deployment trigger job.
2. Configure it to target a protected environment.
3. Test deployment-only access.
4. If the job fails authorization unexpectedly, verify whether the trigger job has the `environment` keyword.
5. Correct the configuration and retest.

**Expected result:** You understand how the environment association affects protected-environment authorization for trigger jobs.

## Lab 11: Build a release approval flow
1. Add automated validation before deployment.
2. Configure production approval rules.
3. Restrict deploy permissions to the release/operator group.
4. Ensure the triggerer is not an approver unless policy explicitly allows it.
5. Document the sequence from validation to approval to deployment.

**Expected result:** A controlled production release workflow with distinct technical and human gates.

## Lab 12: Security review
Review:
- [ ] Production environment is protected.
- [ ] Allowed-to-deploy list is least-privilege.
- [ ] Approver rules are documented.
- [ ] Self-approval policy is intentional.
- [ ] Release branches/tags are protected.
- [ ] Production variables are protected and scoped.
- [ ] Deployment runners are trusted and isolated.
- [ ] Untrusted merge-request pipelines cannot access production secrets.
- [ ] Trigger jobs declare their target environment.
- [ ] Deployment history and approval evidence are retained.

## Lab deliverables
1. `.gitlab-ci.yml` with staging and production jobs.
2. Screenshots of protected environment settings (hide sensitive details).
3. Evidence of approval and deployment status.
4. Branch and variable access test results.
5. A short separation-of-duties diagram.
6. Security review with gaps and remediation recommendations.
