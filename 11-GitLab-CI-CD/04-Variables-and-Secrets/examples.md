# GitLab CI/CD Variables and Secrets — Examples

> Use dummy values for exercises. Never commit real passwords, API tokens, private keys, or cloud credentials.

## 1. Global and job-level variables

```yaml
variables:
  APP_NAME: "demo-app"
  LOG_LEVEL: "info"

test:
  stage: test
  variables:
    TEST_MODE: "unit"
  script:
    - echo "Application: $APP_NAME"
    - echo "Log level: $LOG_LEVEL"
    - echo "Test mode: $TEST_MODE"
```

## 2. Use predefined variables

```yaml
pipeline_info:
  stage: test
  script:
    - echo "Project: $CI_PROJECT_PATH"
    - echo "Commit: $CI_COMMIT_SHORT_SHA"
    - echo "Ref: $CI_COMMIT_REF_NAME"
    - echo "Pipeline source: $CI_PIPELINE_SOURCE"
```

Predefined variables provide pipeline metadata. Check the official list for availability and expansion timing.

## 3. Consume a project secret safely

Create `DEPLOY_TOKEN` in project Settings → CI/CD → Variables. Mark it masked and protected as appropriate.

```yaml
deploy:
  stage: deploy
  script:
    - |
      if [ -z "${DEPLOY_TOKEN:-}" ]; then
        echo "DEPLOY_TOKEN is unavailable"
        exit 1
      fi
      echo "Deployment credential is configured"
```

Do not print the value.

## 4. File-type SSH key

Configure `SSH_PRIVATE_KEY` as a File variable in GitLab settings.

```yaml
ssh_check:
  stage: test
  script:
    - test -f "$SSH_PRIVATE_KEY"
    - chmod 600 "$SSH_PRIVATE_KEY"
    - echo "Private key file is present"
```

This example does not print or use the key. Add a real SSH command only for a host you own or are authorized to access.

## 5. Environment-scoped deployment variables

Configure `DEPLOY_TOKEN` twice in GitLab settings:
- One value with environment scope `staging`.
- A different value with environment scope `production`.

```yaml
deploy_staging:
  stage: deploy
  environment:
    name: staging
  script:
    - test -n "${DEPLOY_TOKEN:-}"
    - echo "Staging credential is available"

deploy_production:
  stage: deploy
  environment:
    name: production
  when: manual
  script:
    - test -n "${DEPLOY_TOKEN:-}"
    - echo "Production credential is available"
```

Configure protected environments and protected refs separately. A manual job alone is not a full authorization policy.

## 6. Validate required configuration

```yaml
validate_config:
  stage: test
  script:
    - |
      required_vars="APP_NAME DEPLOY_REGION"
      for name in $required_vars; do
        eval "value=\${$name-}"
        if [ -z "$value" ]; then
          echo "Missing required variable: $name"
          exit 1
        fi
      done
      echo "Required non-secret configuration is present"
```

This example validates names from a fixed allowlist. Do not use `eval` with untrusted variable names or user input; in ordinary workflows, direct checks are safer.

Safer direct alternative:

```yaml
validate_config:
  stage: test
  script:
    - test -n "${APP_NAME:-}"
    - test -n "${DEPLOY_REGION:-}"
```

## 7. Use a secret without exposing it

```yaml
api_check:
  stage: test
  script:
    - |
      if [ -z "${API_TOKEN:-}" ]; then
        echo "API_TOKEN is not configured"
        exit 1
      fi
      # Pass the token through the environment to a trusted client.
      ./scripts/check-api.sh
```

The script should read the token from its environment and must not log it.

## 8. External Vault secret with ID token

Provider configuration, Vault role, JWT auth method, audience, and secret path must be prepared first. This is a template:

```yaml
vault_read:
  stage: test
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.example.com
  secrets:
    DB_PASSWORD:
      vault: production/database/password@ops
      token: $VAULT_ID_TOKEN
  script:
    - test -n "$DB_PASSWORD"
    - echo "External secret was retrieved"
```

The secret is normally provided as a file-type variable; `$DB_PASSWORD` can therefore be a file path. Read the provider-specific GitLab documentation for the exact path syntax.

## 9. Environment variables and non-secret values

```yaml
variables:
  APP_PORT: "8080"
  DEPLOY_REGION: "ap-south-1"

show_config:
  stage: test
  script:
    - echo "Port: $APP_PORT"
    - echo "Region: $DEPLOY_REGION"
```

Non-sensitive configuration can be stored in YAML. Keep credentials out of source control.

## 10. Avoid accidental secret output

```yaml
safe_diagnostic:
  stage: test
  script:
    - |
      if [ -n "${DEPLOY_TOKEN:-}" ]; then
        echo "DEPLOY_TOKEN is set"
      else
        echo "DEPLOY_TOKEN is missing"
        exit 1
      fi
```

Avoid `env`, `printenv`, `set -x`, and commands that dump process environments when secrets are present.

## 11. Restrict a job to protected refs

```yaml
deploy_production:
  stage: deploy
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
    - when: never
  environment:
    name: production
  script:
    - test -n "${DEPLOY_TOKEN:-}"
    - echo "Ready for controlled production deployment"
```

Also configure the variable as protected and the environment as protected in GitLab settings where available.

## 12. Pass a variable to a container safely

```yaml
container_task:
  image: alpine:3.20
  stage: test
  variables:
    APP_MODE: "test"
  script:
    - 'printf "Mode: %s\n" "$APP_MODE"'
```

For credentials, prefer environment variables or file variables supported by the tool; never bake secrets into an image or image build arguments that may persist in layers.
