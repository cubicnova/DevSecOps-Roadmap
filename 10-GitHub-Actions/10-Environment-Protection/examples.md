# Environment Protection — Examples

Replace sample URLs and deployment commands with your own application tooling. These examples use harmless commands and do not perform real deployments.

## 1. Basic environment target

```yaml
name: Staging deployment
on: workflow_dispatch
permissions:
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - run: echo "Deploying the staging build"
```

Create the `staging` environment in repository settings first.

## 2. Environment URL

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - run: echo "Target: staging"
```

The URL is deployment metadata; it does not authenticate or secure the destination.

## 3. Environment secret and variable

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Use deployment configuration
        env:
          TOKEN: ${{ secrets.DEPLOY_TOKEN }}
          REGION: ${{ vars.DEPLOY_REGION }}
        run: |
          test -n "$TOKEN"
          echo "Deploying to region: $REGION"
```

Add `DEPLOY_TOKEN` under staging **Environment secrets** and `DEPLOY_REGION` under **Environment variables**. Do not print the token.

## 4. Separate staging and production jobs

```yaml
name: Promote release
on: workflow_dispatch
permissions:
  contents: read
jobs:
  staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: echo "Deploy to staging"
  production:
    needs: staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "Deploy to production after environment rules pass"
```

Configure production with appropriate reviewer and branch restrictions.

## 5. Restrict production to main

```yaml
name: Production deployment
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "Production deployment"
```

The YAML condition is an extra guard. Also configure the environment's deployment branch policy in repository settings.

## 6. Prevent overlapping deployments

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    concurrency:
      group: production-deployment
      cancel-in-progress: false
    steps:
      - run: echo "Deploying one production release at a time"
```

Other workflows must use the same group to participate in the same concurrency control.

## 7. Example deployment script

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: |
          chmod +x scripts/deploy.sh
          ./scripts/deploy.sh staging
```

Example `scripts/deploy.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
target="${1:?Usage: deploy.sh <staging|production>}"
case "$target" in
  staging|production) ;;
  *) echo "Unsupported target" >&2; exit 2 ;;
esac
: "${DEPLOY_TOKEN:?DEPLOY_TOKEN is required}"
echo "Deployment command for ${target} goes here."
# Invoke your deployment CLI here. Never echo DEPLOY_TOKEN.
```

## 8. Manual release with validation

```yaml
name: Manual production release
on:
  workflow_dispatch:
    inputs:
      release_version:
        description: "Version to release"
        required: true
        type: string
permissions:
  contents: read
jobs:
  release:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Validate version
        env:
          RELEASE_VERSION: ${{ inputs.release_version }}
        run: |
          [[ "$RELEASE_VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]
      - name: Release
        run: echo "Replace with the real release command"
```

Validate user input before passing it to shell commands.

## 9. Regional environments

```yaml
jobs:
  deploy-eu:
    runs-on: ubuntu-latest
    environment: production-eu
    steps:
      - run: echo "Deploy to EU"
  deploy-us:
    runs-on: ubuntu-latest
    environment: production-us
    steps:
      - run: echo "Deploy to US"
```

Create and configure both environments separately. Use separate secrets when credentials or permissions differ.

## 10. Secret-safe diagnostic

```yaml
- name: Check deployment credential
  env:
    DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
  run: |
    if [ -z "$DEPLOY_TOKEN" ]; then
      echo "Deployment credential is missing"
      exit 1
    fi
    echo "Deployment credential is configured"
```

Never echo the token or enable shell tracing around commands that handle secrets.
