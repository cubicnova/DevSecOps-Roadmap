# GitLab Protected Environments — Examples

Use harmless placeholder commands in labs. Replace them only with deployment commands for systems you own or are authorized to administer.

## 1. Basic staging deployment

```yaml
stages: [deploy]

deploy_staging:
  stage: deploy
  script:
    - echo "Deploying to ${CI_ENVIRONMENT_NAME}"
  environment:
    name: staging
    url: https://staging.example.com
```

Create the environment by running a job that references it. Then protect it in **Settings → CI/CD → Protected environments** if required.

## 2. Production deployment with deployment tier

```yaml
deploy_production:
  stage: deploy
  script:
    - echo "Deploying production release"
  environment:
    name: production
    url: https://example.com
    deployment_tier: production
```

The tier helps GitLab classify the environment. It does not itself grant or restrict deploy access.

## 3. Manual production job

```yaml
deploy_production:
  stage: deploy
  when: manual
  allow_failure: false
  environment:
    name: production
  script:
    - echo "Run the approved production deployment command"
```

A manual job is a user interaction gate. Configure a protected environment to control who may deploy.

## 4. Branch guard plus protected environment

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
    - echo "Production deploy from default branch"
```

Also protect the default branch and configure Allowed to deploy in the GitLab UI. The YAML condition alone is not an authorization boundary.

## 5. Separate staging and production

```yaml
stages: [test, deploy]

test:
  stage: test
  script:
    - echo "Run tests"

deploy_staging:
  stage: deploy
  needs: [test]
  environment:
    name: staging
  script:
    - echo "Deploy staging"

deploy_production:
  stage: deploy
  needs: [test]
  when: manual
  environment:
    name: production
  script:
    - echo "Deploy production after approval and authorization"
```

Configure separate access policies for the two environments.

## 6. Use a protected production variable

Configure `DEPLOY_TOKEN` in GitLab CI/CD settings as a protected variable and scope it to `production` where appropriate.

```yaml
deploy_production:
  stage: deploy
  environment:
    name: production
  script:
    - |
      if [ -z "${DEPLOY_TOKEN:-}" ]; then
        echo "Production credential is unavailable"
        exit 1
      fi
      echo "Production credential is configured"
      # Invoke the deployment client here; never print the token.
```

## 7. Deployment approval demonstration

```yaml
stages: [deploy]

production:
  stage: deploy
  script:
    - echo "Deploying ${CI_ENVIRONMENT_NAME}"
  environment:
    name: production
    action: start
```

Configure approval rules for the protected `production` environment in GitLab settings. A deployment can be blocked pending approval. After approval, the job still needs to be run according to GitLab's deployment approval workflow.

## 8. Deployment-only access with a trigger job

```yaml
deploy_downstream:
  stage: deploy
  trigger:
    project: group/deployment-project
    branch: main
  environment:
    name: production
```

The `environment` keyword on the trigger job allows GitLab to associate it with the protected environment for access checks. Configure the downstream project and permissions carefully.

## 9. Lower and higher environment tiers

```yaml
deploy_dev:
  stage: deploy
  script: echo "Deploy development"
  environment:
    name: development
    deployment_tier: development

deploy_test:
  stage: deploy
  script: echo "Deploy testing"
  environment:
    name: testing
    deployment_tier: testing

deploy_staging:
  stage: deploy
  script: echo "Deploy staging"
  environment:
    name: staging
    deployment_tier: staging

deploy_prod:
  stage: deploy
  script: echo "Deploy production"
  environment:
    name: production
    deployment_tier: production
```

Use different access policies for lower and higher environments.

## 10. Record deployment URL and tier

```yaml
deploy_preview:
  stage: deploy
  script:
    - echo "Deploy preview"
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://preview.example.com
    deployment_tier: testing
    on_stop: stop_preview

stop_preview:
  stage: deploy
  script:
    - echo "Stop preview environment"
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  when: manual
```

Review app URLs and stop jobs are examples of dynamic environments. Do not expose sensitive preview instances publicly without appropriate access controls.
