# GitLab Protected Environments — Solutions and Explanations

## Solution 1: Define environments in YAML

```yaml
stages: [deploy]

deploy_staging:
  stage: deploy
  script:
    - echo "Deploying to ${CI_ENVIRONMENT_NAME}"
  environment:
    name: staging
    url: https://staging.example.com

deploy_production:
  stage: deploy
  script:
    - echo "Deploying to ${CI_ENVIRONMENT_NAME}"
  environment:
    name: production
    url: https://example.com
    deployment_tier: production
```

Running jobs that reference these environments creates or updates the environment records. Protect the production environment separately in project settings.

## Solution 2: Protect production

Go to **Settings → CI/CD → Protected environments** and protect `production`. Configure **Allowed to deploy** with only the roles, users, or groups that need production deployment access. You generally need Maintainer or Owner permissions to manage this configuration.

## Solution 3: Permission testing

A user who is not allowed to deploy should be blocked from deploying to the protected environment. Check:
- The exact environment name used in the job.
- The Allowed to deploy list.
- Whether the user is a direct or inherited member of an allowed group.
- The user's project and group role.
- Whether group membership is configured as required by the project.

Do not use a broader project role as a workaround when deployment-only access is sufficient.

## Solution 4: Deployment approvals

Configure approvers and approval rules in the protected environment settings. Trigger a deployment and inspect the deployment status in **Operate → Environments**. The deployment is blocked until all configured approval rules are satisfied.

After approval, the corresponding deployment job still needs to be run manually according to GitLab's documented workflow. Approval is not the same as job execution.

## Solution 5: Separation of duties

By default, the user who triggers the deployment pipeline cannot approve that deployment. This prevents one person from both initiating and approving the same release. GitLab provides an option to allow self-approval, but it should remain disabled unless a documented policy requires otherwise.

## Solution 6: Branch guard

```yaml
deploy_production:
  stage: deploy
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
    - when: never
  environment:
    name: production
    deployment_tier: production
  script:
    - echo "Deploying from the default branch"
```

Protect the default branch and configure the production environment in GitLab settings. The `rules` condition is a pipeline guard, not a substitute for the protected environment authorization policy.

## Solution 7: Protected production credential

Create `DEPLOY_TOKEN` in CI/CD variables, mark it protected, and scope it to `production` where supported. Then validate without printing it:

```yaml
deploy_production:
  stage: deploy
  environment:
    name: production
  script:
    - |
      if [ -z "${DEPLOY_TOKEN:-}" ]; then
        echo "Production token is unavailable"
        exit 1
      fi
      echo "Production token is configured"
```

Protected variables are only available in eligible protected-ref contexts, subject to merge request pipeline settings and the project's configuration.

## Solution 8: Deployment-only access

Where supported, invite a release-operator group to the project and grant the minimum role required for deployment-only access. Add the group to the protected environment's Allowed to deploy list. Verify the group's membership and direct/inherited membership requirements in current GitLab documentation.

The goal is to allow operators to deploy without granting unnecessary source-code modification privileges.

## Solution 9: Deployment tiers

```yaml
deploy_staging:
  stage: deploy
  script: echo "Deploy staging"
  environment:
    name: staging
    deployment_tier: staging

deploy_production:
  stage: deploy
  script: echo "Deploy production"
  environment:
    name: production
    deployment_tier: production
```

Deployment tiers classify environments. Group-level protected environment controls can use tiers to apply consistent restrictions to critical environments, subject to the GitLab offering and group configuration.

## Solution 10: Protected trigger job

```yaml
deploy_downstream:
  stage: deploy
  trigger:
    project: group/deployment-project
    branch: main
  environment:
    name: production
```

GitLab documents that a trigger job without an `environment` keyword may not be associated with the protected environment. Adding the environment lets GitLab apply the intended protected-environment access check. Ensure the downstream project also has appropriate permissions and protections.

## Solution 11: Example release approval flow

```yaml
stages: [validate, deploy]

validate:
  stage: validate
  script:
    - echo "Run tests and security scans"

deploy_production:
  stage: deploy
  needs: [validate]
  environment:
    name: production
    deployment_tier: production
  script:
    - |
      if [ -z "${DEPLOY_TOKEN:-}" ]; then
        echo "Deployment credential is unavailable"
        exit 1
      fi
      echo "Run the trusted deployment command here"
  when: manual
```

Configure the protected environment with:
1. An Allowed to deploy list containing the release/operator team.
2. Approvers and approval rules appropriate to the release risk.
3. A protected production variable scoped to the environment.
4. A trusted runner for deployment.
5. Protected release branches/tags.

The release flow is: automated validation → deployment approval → authorized job execution → deployment record.

## Solution 12: Sample security review

| Finding | Risk | Remediation |
|---|---|---|
| Production is not protected | Broad or unintended deploy access | Protect the environment and restrict deployers |
| Developers can deploy to production by default | Separation-of-duties weakness | Use a release/operator group |
| No approval rules | Unreviewed changes may reach production | Add approver rules where supported |
| Self-approval enabled | Reduced independent review | Disable unless policy requires it |
| Production secret available to untrusted refs | Secret theft | Protect variable and ref; review MR settings |
| Untrusted runner used for deployment | Credential or artifact compromise | Use isolated trusted runners |
| Trigger job omits environment | Protected access check may not apply as intended | Declare the environment on the trigger job |

## Common troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| Deployment denied | User not in Allowed to deploy | Verify user/group/role membership |
| Deployment blocked | Approval rule incomplete | Inspect approval status and eligible approvers |
| Approval completed but job pending | Approval does not automatically run the job | Manually start the deployment job |
| Trigger job denied | Missing `environment` keyword | Add the target environment to the trigger job |
| Environment policy not visible | GitLab plan or permission limitation | Check current tier and Maintainer/Owner access |
| Production variable missing | Protected ref or environment scope mismatch | Check branch protection and variable scope |

## Important notes
- Protected environments and deployment approvals are documented as Premium/Ultimate features; verify current availability for your GitLab offering.
- A protected environment does not replace protected branches, protected variables, runner isolation, or review of CI configuration.
- Approval rules and deployment permissions are distinct controls.
- Keep approval evidence and deployment history for audit requirements.

## Official documentation
- [Protected environments](https://docs.gitlab.com/ci/environments/protected_environments/)
- [Deployment approvals](https://docs.gitlab.com/ci/environments/deployment_approvals/)
- [Deployment safety](https://docs.gitlab.com/ci/environments/deployment_safety/)
