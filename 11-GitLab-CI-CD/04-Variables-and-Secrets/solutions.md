# GitLab CI/CD Variables and Secrets — Solutions

## Solution 1: YAML variables

```yaml
variables:
  APP_NAME: "sample-app"
  APP_ENV: "test"

check_config:
  stage: test
  variables:
    LOG_LEVEL: "debug"
  script:
    - echo "App: $APP_NAME"
    - echo "Environment: $APP_ENV"
    - echo "Log level: $LOG_LEVEL"
```

Top-level variables are available to jobs unless overridden. Job-level variables apply to that job.

## Solution 2: Predefined variables

```yaml
pipeline_metadata:
  stage: test
  script:
    - echo "Project: $CI_PROJECT_PATH"
    - echo "Branch/ref: $CI_COMMIT_REF_NAME"
    - echo "Commit: $CI_COMMIT_SHORT_SHA"
    - echo "Source: $CI_PIPELINE_SOURCE"
```

Use GitLab's predefined variable reference for the full list and availability timing.

## Solution 3: Project variable

Add `DEPLOY_REGION` in **Settings → CI/CD → Variables**. Then:

```yaml
show_region:
  stage: test
  script:
    - 'test -n "$DEPLOY_REGION"'
    - 'printf "Region is configured\n"'
```

If you need to display the non-sensitive region, print it explicitly. Do not print sensitive values.

## Solution 4: Masked and hidden variables

Create a dummy `LAB_TOKEN` in the UI and select masked/hidden visibility where available. Validate it without exposing it:

```yaml
check_token:
  stage: test
  script:
    - |
      if [ -z "${LAB_TOKEN:-}" ]; then
        echo "LAB_TOKEN is unavailable"
        exit 1
      fi
      echo "LAB_TOKEN is configured"
```

Masking is best-effort log protection. Hidden controls whether the saved value can be revealed in settings. Neither prevents malicious code from sending the value elsewhere.

## Solution 5: Protected variable

Mark the variable as protected and ensure the intended branch/tag is protected. Test with harmless validation only:

```yaml
check_protected_value:
  stage: test
  script:
    - |
      if [ -n "${LAB_TOKEN:-}" ]; then
        echo "Protected variable is available in this pipeline"
      else
        echo "Protected variable is not available"
      fi
```

Merge request pipeline access to protected variables has additional settings and restrictions. Verify the behavior for your GitLab version and project configuration.

## Solution 6: File-type variable

Configure `LAB_CONFIG` as a File variable. The environment variable contains the path to a temporary file:

```yaml
check_file_variable:
  stage: test
  script:
    - test -f "$LAB_CONFIG"
    - echo "File variable exists"
```

Do not `cat` real private keys or credentials. For the exercise, use harmless sample content.

## Solution 7: Environment scope

Create separate variables with the same key but different environment scopes and values:

```yaml
deploy_staging:
  stage: deploy
  environment:
    name: staging
  script:
    - test -n "${DEPLOY_TOKEN:-}"
    - echo "Staging credential is present"

deploy_production:
  stage: deploy
  environment:
    name: production
  when: manual
  script:
    - test -n "${DEPLOY_TOKEN:-}"
    - echo "Production credential is present"
```

Environment scope selects which variable value is available to a matching environment job. Use different credentials for each environment.

## Solution 8: Variable precedence

GitLab documents a precedence order for variable sources. The exact order includes pipeline execution policy variables, scan execution policy variables, pipeline variables, project/group/instance variables, dotenv variables, job/default YAML variables, and predefined variables, with details that can change by version and feature. Consult the current official precedence page rather than relying on memory.

Security lesson: do not let untrusted callers override variables that determine authorization, deployment destination, or secret selection. Restrict who can provide pipeline variables and prefer typed CI/CD inputs for parameters where supported.

## Solution 9: External secrets

Conceptual flow:

1. The job requests an ID token with an audience expected by the provider.
2. The external provider validates the token's issuer, audience, subject/claims, and configured role/trust policy.
3. The provider authorizes access to a specific secret path or resource.
4. GitLab's secrets integration retrieves the secret for that job.
5. The job consumes it without printing it.

Example shape for a Vault integration (provider setup and exact path are environment-specific):

```yaml
retrieve_secret:
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
    - echo "Secret retrieval succeeded"
```

External secret integrations have tier and provider prerequisites. Follow the provider-specific GitLab documentation.

## Solution 10: Secret-leak review

| Unsafe pattern | Risk | Remediation |
|---|---|---|
| `echo "$API_TOKEN"` | Secret in job trace | Remove output; rotate if exposed |
| `env` / `printenv` | Dumps environment values | Print only approved non-sensitive variables |
| `set -x` | Commands may expose expanded secrets | Disable tracing around secret use |
| Unknown `curl` destination | Exfiltration | Review destinations and pipeline changes |
| Secret file in artifacts | Credential persists and can be downloaded | Exclude it; use temporary files and cleanup |
| Untrusted MR with privileged secrets | Attacker-controlled code can steal secrets | Isolate fork/MR pipelines and restrict secret access |

## Solution 11: Rotation
1. Generate a new credential in the issuing service.
2. Update the GitLab variable through the settings UI or approved secret manager.
3. Run a safe validation job.
4. Revoke the old credential.
5. Review logs and audit events.
6. Record the owner and rotation date.

If a credential was exposed, revoke/rotate it immediately rather than only deleting the log line.

## Solution 12: Secure deployment example

```yaml
stages: [validate, deploy]

variables:
  APP_NAME: "sample-app"
  DEPLOY_REGION: "ap-south-1"

validate:
  stage: validate
  script:
    - test -n "$APP_NAME"
    - test -n "$DEPLOY_REGION"
    - echo "Non-sensitive configuration is valid"

deploy_staging:
  stage: deploy
  environment:
    name: staging
  when: manual
  script:
    - |
      if [ -z "${DEPLOY_TOKEN:-}" ]; then
        echo "Deployment credential is unavailable"
        exit 1
      fi
      echo "Deployment credential is configured"
      # Invoke a trusted deployment tool here. Do not print the token.
```

Store `DEPLOY_TOKEN` in GitLab settings with masked and protected options as appropriate, and use the `staging` environment scope. Add protected environment permissions and a trusted runner for real deployments.

## Common troubleshooting

| Problem | Likely cause | Action |
|---|---|---|
| Variable is empty | Protected ref or environment scope mismatch | Verify branch protection, environment name, and variable scope |
| Value unexpectedly changes | Higher-precedence source overrides it | Inspect all variable sources and restrict pipeline variables |
| Masking rejected | Value does not meet current masking rules | Check length, newline, spaces, and allowed characters |
| File variable is not a file | Variable type is `Variable`, not `File` | Change its type and verify the path |
| Secret provider denies access | Wrong issuer, audience, subject, role, or path | Inspect trust configuration without logging tokens |
| Secret is leaked | Pipeline printed or transmitted it | Stop the job, revoke/rotate, audit, and fix pipeline |

## Official documentation
- [CI/CD variables](https://docs.gitlab.com/ci/variables/)
- [Use external secrets in CI/CD](https://docs.gitlab.com/ci/secrets/)
- [Pipeline security](https://docs.gitlab.com/ci/pipeline_security/)
- [CI/CD YAML syntax](https://docs.gitlab.com/ci/yaml/)
