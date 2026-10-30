# GitHub Actions Environment Protection

## Overview
GitHub Actions environments represent deployment targets such as `development`, `staging`, and `production`. They let teams apply deployment gates, restrict eligible branches and tags, and scope secrets and variables to jobs targeting a particular environment. A job must pass the environment's protection rules before it starts; environment secrets become available only after those rules pass.

## Learning objectives
- Explain GitHub Actions environments and deployment targets.
- Create and configure development, staging, and production environments.
- Reference environments from workflow jobs.
- Configure required reviewers, wait timers, and deployment branch policies.
- Use environment-scoped secrets and variables safely.
- Prevent overlapping deployments with concurrency.
- Troubleshoot blocked deployments and missing secrets.

## 1. Environment fundamentals
An environment is a named deployment target configured in repository settings. Common names include `development`, `staging`, and `production`.

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "Deploying to production"
```

You can attach a URL to deployment metadata:

```yaml
environment:
  name: staging
  url: https://staging.example.com
```

## 2. Create an environment
1. Open the repository on GitHub.
2. Select **Settings → Environments**.
3. Select **New environment** and enter a name.
4. Configure protection rules and deployment branch/tag restrictions.
5. Add environment secrets and variables when needed.

Environment names referenced in workflow YAML should match the configured names.

## 3. Deployment protection rules

### Required reviewers
Require an authorized user or team to approve a deployment before its job proceeds. Up to six reviewers can be configured; only one needs to approve. Where available, enable **Prevent self-review** so the person who initiated the deployment cannot approve it.

### Wait timer
Delay a job for a configured number of minutes. The documented range is 1 to 43,200 minutes. A timer is a release-control mechanism, not a substitute for monitoring or approval.

### Deployment branches and tags
Choose:
- **No restriction** — any branch or tag can target the environment.
- **Protected branches only** — eligible protected branches can deploy.
- **Selected branches and tags** — allow explicit patterns such as `main` or `release/*`.

Branch and tag patterns are configured separately. Review GitHub's matching behavior before relying on wildcard rules.

### Custom deployment protection rules
GitHub Apps can provide custom protection rules that consult external systems such as change-management or observability services. Feature availability and preview status may change; verify current documentation and plan requirements.

## 4. Environment secrets and variables
Environment secrets are scoped to jobs that reference that environment. If protection rules are configured, the job must pass them before accessing environment secrets.

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
          DEPLOY_REGION: ${{ vars.DEPLOY_REGION }}
        run: ./scripts/deploy.sh
```

Security practices:
- Never print secret values or place them in artifacts.
- Do not hardcode credentials in workflow YAML.
- Use separate least-privilege credentials for staging and production.
- Rotate credentials and remove unused secrets.
- Treat self-hosted runners as sensitive infrastructure; environment scoping does not isolate a self-hosted runner.

## 5. Multi-environment workflow

```yaml
name: Deploy application
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m compileall .

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    concurrency:
      group: deploy-staging
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: ./scripts/deploy.sh staging

  deploy-production:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    concurrency:
      group: deploy-production
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: ./scripts/deploy.sh production
```

Create and configure both environments in repository settings. A protected production job waits until its rules are satisfied.

## 6. Protection versus concurrency
Environment protection determines whether a deployment job may proceed. Concurrency controls how many jobs in a concurrency group run at once. These are separate controls; explicitly configure a stable group such as `production-deployment` in every workflow that should share the deployment lock.

## 7. Security checklist
- [ ] Production is a dedicated environment.
- [ ] Production deployments are restricted to approved branches/tags.
- [ ] Required reviewers and self-review prevention are configured where supported.
- [ ] Production secrets are stored only in the production environment.
- [ ] Staging and production use different credentials.
- [ ] Workflow permissions are least-privilege.
- [ ] Deployment concurrency is configured.
- [ ] Logs and artifacts do not expose credentials.
- [ ] Self-hosted runners are hardened and access-controlled.
- [ ] Emergency bypasses are restricted and audited.

## 8. Troubleshooting

| Symptom | Likely cause | Check |
|---|---|---|
| Job waits for approval | Required reviewer rule | Review the pending deployment |
| Branch cannot deploy | Environment branch/tag policy | Check allowed refs and `github.ref` |
| Secret is empty | Wrong/missing environment or approval pending | Check `jobs.<job_id>.environment` and secret name |
| Protection seems absent | Environment not configured or name mismatch | Check repository Settings |
| Deployments overlap | No shared concurrency group | Add a stable group |
| Feature unavailable | Plan/visibility limitation | Check current GitHub plan requirements |

## 9. Plan and availability notes
Environment features differ by repository visibility and plan. Required reviewers, wait timers, deployment branch policies, and environment secrets may have restrictions for private repositories. Confirm current GitHub documentation before making a control mandatory in a production design.

## Further reading
- [Managing environments for deployment](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
- [Deployments and environments reference](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- [Deploying with GitHub Actions](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments)
- [Reviewing deployments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/review-deployments)
