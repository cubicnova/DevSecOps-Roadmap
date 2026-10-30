# GitLab CI/CD Protected Environments

## Overview

GitLab environments represent deployment targets such as `development`, `staging`, and `production`. A protected environment adds an authorization boundary around deployments: only users, roles, or groups permitted by the environment's **Allowed to deploy** configuration can deploy to it. Protected environments can also use deployment approval rules to require review before a deployment proceeds.

This module focuses on protecting critical deployment targets and separating the people who build software from those authorized to release it.

## Learning objectives

- Understand GitLab environments, deployments, and protected environments.
- Create deployment jobs that target named environments.
- Configure **Allowed to deploy** permissions.
- Configure deployment approval rules and approval workflows.
- Understand the difference between deploy permission and approval permission.
- Protect production using branch controls, protected variables, and trusted runners.
- Use deployment tiers and group-level protection where supported.
- Troubleshoot blocked or unauthorized deployments.

## 1. Environment fundamentals

An environment is a named target where code is deployed. Common examples:

| Environment | Purpose | Typical access |
|---|---|---|
| `development` | Frequent developer testing | Developers and maintainers |
| `staging` | Release candidate validation | QA, release team, maintainers |
| `production` | Live application | Restricted operators/release managers |

A job creates or updates an environment when it uses the `environment` keyword:

```yaml
stages:
  - deploy

deploy_staging:
  stage: deploy
  script:
    - echo "Deploying to ${CI_ENVIRONMENT_NAME}"
  environment:
    name: staging
    url: https://staging.example.com
```

The `environment` keyword is important: it associates the job with the deployment target so GitLab can apply environment permissions and record deployment activity.

## 2. What is a protected environment?

By default, environment access follows the project's general permissions. A protected environment lets a project explicitly define who may deploy to a sensitive target.

Protected environments can control:
- **Allowed to deploy:** users, roles, or groups permitted to deploy.
- **Approvers:** users, roles, or groups permitted to approve deployment requests.
- **Approval rules:** the number of approvals required from configured approvers.
- **Deployment-only access:** in supported configurations, users can be granted deployment permission without broad repository write access.

Protecting an environment does not automatically secure every part of the pipeline. Review source branch protections, CI/CD variables, runner access, job-token permissions, and included configuration too.

## 3. Protect an environment in GitLab

Typical UI workflow:

1. Open the project.
2. Go to **Settings → CI/CD**.
3. Expand **Protected environments**.
4. Select **Protect an environment**.
5. Choose an existing environment name.
6. Configure **Allowed to deploy** with the appropriate role, users, or invited groups.
7. Configure approvers and approval rules if available.
8. Save the protection configuration.

You generally need at least the Maintainer role to protect, update, or unprotect a project environment. Current feature availability is documented by GitLab and may depend on plan.

## 4. Allowed to deploy versus approvers

These controls serve different purposes:

| Control | Meaning |
|---|---|
| Allowed to deploy | Who is authorized to execute deployments to the environment |
| Approvers | Who can approve a deployment request |
| Approval rule | How many approvals are required from a configured approver set |

Do not assume that approval alone deploys the application. GitLab documents that after a deployment is approved, the corresponding deployment job must still be run manually. A user may need both the relevant approval and deployment permissions depending on the configured rules.

## 5. Deployment approval workflow

Deployment approvals are used for change management, QA, security, and compliance checks. A deployment to a protected environment can be blocked until all required approval rules are satisfied.

Example deployment job:

```yaml
stages:
  - test
  - deploy

test:
  stage: test
  script:
    - echo "Run automated validation"

deploy_production:
  stage: deploy
  script:
    - echo "Deploying to ${CI_ENVIRONMENT_NAME}"
  environment:
    name: production
    url: https://example.com
```

Configure approval rules in **Settings → CI/CD → Protected environments**. The approval feature is plan-gated; check current GitLab documentation for tier and instance requirements.

By default, the pipeline triggerer cannot approve their own deployment. GitLab provides an option to allow self-approval, but enabling it weakens separation of duties and should be a deliberate policy decision.

## 6. Manual jobs are not the same as protected environments

A manual job:

```yaml
deploy:
  stage: deploy
  when: manual
  script:
    - echo "Deploy"
```

requires a user to start it, but it does not by itself define who is authorized to deploy to production. Use protected environments for deployment authorization and approval rules where required.

## 7. Deployment tiers and group-level protection

Deployment jobs can declare a tier:

```yaml
deploy_production:
  stage: deploy
  script:
    - echo "Deploying"
  environment:
    name: production
    deployment_tier: production
```

GitLab supports environment tiers such as `development`, `testing`, `staging`, and `production`. Group-level protected environment controls can help organizations apply consistent protection to critical tiers across projects. Availability and exact behavior depend on GitLab offering and configuration.

## 8. Deployment branch and variable controls

A protected environment is one layer of a secure release process. Also consider:

- Protect the default and release branches.
- Restrict who can merge or push to release branches.
- Mark production credentials as protected variables.
- Scope variables to the `production` environment where appropriate.
- Use separate staging and production credentials.
- Use trusted runners for production deployments.
- Limit job-token permissions.
- Review merge-request pipeline behavior, especially for forks and untrusted code.

Example:

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
    - test -n "${DEPLOY_TOKEN:-}"
    - echo "Production credential is configured"
```

The YAML rule is an additional guard, not a replacement for protected branch and environment settings.

## 9. Deployment-only access

In some configurations, a user or invited group can receive permission to deploy to a protected environment without receiving broad project write access. This supports a separation between developers who change application code and operators who deploy approved releases.

Use least privilege:
- Developers can build and test in lower environments.
- Operators or release managers deploy to production.
- Approvers review release readiness.
- Maintainers administer the environment policy.

Check current role and group requirements in GitLab's documentation.

## 10. Troubleshooting

| Symptom | Likely cause | What to check |
|---|---|---|
| User cannot deploy | User is not in Allowed to deploy | Protected environment access list and group membership |
| Deployment blocked | Required approvals are incomplete | Approval rules and deployment status |
| Approval does not start job | Approval and job execution are separate steps | Run the approved deployment job |
| Trigger job cannot use deployment-only access | Trigger job lacks `environment` keyword | Add the correct environment to the trigger job |
| Environment not protected | Wrong environment name or protection not saved | Environment name in YAML and settings |
| Protected variable missing | Pipeline ref or environment scope mismatch | Protected branch/tag and variable scope |
| Feature not visible | Plan or permission limitation | GitLab tier and user role |

## Security checklist

- [ ] Production is a named environment in `.gitlab-ci.yml`.
- [ ] Production is protected in project settings.
- [ ] Allowed-to-deploy permissions are least-privilege.
- [ ] Approvers are separate from deployers where practical.
- [ ] Approval requirements reflect release risk.
- [ ] Self-approval is disabled unless explicitly justified.
- [ ] Release branches and tags are protected.
- [ ] Production secrets are protected and environment-scoped.
- [ ] Production jobs use trusted runners.
- [ ] Merge request pipelines cannot access privileged production secrets.
- [ ] Deployment activity and approval history are reviewed.
- [ ] Emergency access is limited and audited.

## Plan and availability notes

GitLab's current documentation lists protected environments and deployment approvals as Premium/Ultimate features for GitLab.com, Self-Managed, and Dedicated. Exact availability may differ by version and offering. Verify the current tier before designing a control that depends on it.

## Further reading

- [Protected environments](https://docs.gitlab.com/ci/environments/protected_environments/)
- [Deployment approvals](https://docs.gitlab.com/ci/environments/deployment_approvals/)
- [Deployment safety](https://docs.gitlab.com/ci/environments/deployment_safety/)
- [Environments and deployments](https://docs.gitlab.com/ci/environments/)
