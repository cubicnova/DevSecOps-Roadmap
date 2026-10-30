# Environment Protection — Solutions and Explanations

These are reference solutions. Adapt names and deployment commands to your repository.

## Solution 1: Create environments
Create `development`, `staging`, and `production` under **Settings → Environments**. Configure each independently. Verify the settings in the repository UI; do not assume that a newly referenced environment has the protection configuration you intended.

## Solution 2: Staging workflow

Create `.github/workflows/staging.yml`:

```yaml
name: Staging environment test
on: workflow_dispatch
permissions:
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Confirm target
        run: echo "Target environment is staging"
```

## Solution 3: Required reviewer gate
In **Settings → Environments → production**, configure required reviewers and, where available, enable **Prevent self-review**. Trigger a job referencing production. It should remain pending until an authorized reviewer approves it. A rejected deployment does not proceed.

Required reviewer availability depends on repository visibility and plan. Check current GitHub plan documentation before relying on it for a private repository.

## Solution 4: Branch restriction
Configure the production environment's deployment branch policy to allow `main` only. Add a workflow-level condition as defense in depth:

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "Deploying from main"
```

The `if` condition does not replace the environment's branch policy. Configure both where appropriate.

## Solution 5: Environment secret and variable

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Validate configuration
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
          DEPLOY_REGION: ${{ vars.DEPLOY_REGION }}
        run: |
          if [ -z "$DEPLOY_TOKEN" ]; then
            echo "DEPLOY_TOKEN is unavailable"
            exit 1
          fi
          if [ -z "$DEPLOY_REGION" ]; then
            echo "DEPLOY_REGION is unavailable"
            exit 1
          fi
          echo "Deployment configuration is present"
          echo "Region: $DEPLOY_REGION"
```

Create the secret and variable in staging settings. Never print the secret.

## Solution 6: Separate credentials
Store a different dummy credential in each environment. The same secret name can be used because the values are independently scoped:

```yaml
jobs:
  staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - env:
          TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: test -n "$TOKEN"

  production:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - env:
          TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: test -n "$TOKEN"
```

Do not reuse the same credential value across environments.

## Solution 7: Concurrency

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    concurrency:
      group: production-deployment
      cancel-in-progress: false
    steps:
      - run: echo "Deploying"
```

All workflows that should share this deployment lock must use the same concurrency group. Environment protection does not automatically create a concurrency lock.

## Solution 8: Validate before production

```yaml
name: Validate and deploy
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run validation
        run: |
          test -f README.md
          echo "Replace with unit tests and security scans"

  production:
    needs: validate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    concurrency:
      group: production-deployment
      cancel-in-progress: false
    steps:
      - name: Deploy
        run: echo "Replace with the production deployment command"
```

If validation fails, the dependent production job will not run. Environment protection adds another gate after the job is eligible to start.

## Solution 9: Environment secret troubleshooting
A job must reference the correct environment:

```yaml
jobs:
  check:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - env:
          TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: |
          if [ -z "$TOKEN" ]; then
            echo "Secret is unavailable"
            exit 1
          fi
          echo "Secret is available"
```

Check:
1. The environment exists and spelling matches.
2. The secret is stored under that environment.
3. The job references that environment.
4. Required approvals and other protection rules have passed.
5. The secret name is exact.
6. The repository plan and visibility support the feature.

## Solution 10: Sample security review

| Finding | Risk | Recommended remediation |
|---|---|---|
| Production accepts all branches | Unreviewed code may deploy | Restrict deployment refs |
| No approval gate | Accidental release risk | Add reviewers where supported |
| Shared staging/production credential | Staging compromise may affect production | Use separate least-privilege credentials |
| Secret printed in logs | Credential disclosure | Remove logging and rotate exposed secret |
| No concurrency group | Releases may conflict | Add a shared production group |
| Broadly accessible self-hosted runner | Runner compromise can expose deployment assets | Isolate, patch, and restrict runner access |

## Additional notes
- A job referencing an environment waits for its protection rules before starting.
- Environment secrets are available only after applicable protection rules pass.
- Environment variables are accessed through the `vars` context.
- Required reviewers, wait timers, branch policies, and environment secrets can have plan and repository-visibility limitations.
- Self-hosted runners are not isolated merely because a job uses an environment.
- Deleting an environment also deletes its associated secrets and protection rules; verify dependencies before deletion.

## Official documentation
- [Managing environments for deployment](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
- [Deployments and environments reference](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- [Deploying with GitHub Actions](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments)
