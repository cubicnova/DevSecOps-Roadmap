# GitLab CI/CD Variables and Secrets

## Overview
GitLab CI/CD variables pass configuration into pipeline jobs. They can be defined in `.gitlab-ci.yml`, project settings, group settings, instance settings, or supplied by supported integrations. Sensitive values such as API tokens, passwords, private keys, and cloud credentials require stronger handling than ordinary configuration.

**Important:** Masking helps prevent accidental disclosure in job logs, but it does not stop malicious pipeline code from reading or exfiltrating a secret. Review pipeline changes and use external secret managers for high-value credentials where possible.

## Learning objectives
- Understand variable scopes and precedence.
- Define YAML-level, project, group, and instance variables.
- Use predefined variables and variable expansion safely.
- Configure masked, hidden, protected, and file-type variables.
- Scope variables to environments.
- Pass variables to jobs without exposing values.
- Use external secrets with supported providers and ID tokens.
- Avoid variable injection and secret leakage.

## 1. Variable types and scopes

### Common variable sources
- **Predefined variables:** supplied by GitLab, such as `CI_PROJECT_PATH`, `CI_COMMIT_REF_NAME`, and `CI_PIPELINE_SOURCE`.
- **YAML variables:** defined at the top level or under a job in `.gitlab-ci.yml`.
- **Project variables:** configured in project Settings → CI/CD → Variables.
- **Group variables:** shared with projects in a group, subject to inheritance and overrides.
- **Instance variables:** configured by administrators for an instance.
- **Pipeline and trigger variables:** supplied when creating or triggering a pipeline.
- **External secrets:** retrieved at job runtime from a supported secrets provider.

### YAML example

```yaml
variables:
  APP_ENV: "test"
  LOG_LEVEL: "info"

unit_tests:
  stage: test
  variables:
    TEST_MODE: "fast"
  script:
    - echo "Environment: $APP_ENV"
    - echo "Log level: $LOG_LEVEL"
    - echo "Mode: $TEST_MODE"
```

Use YAML variables for non-sensitive configuration. Do not commit secrets to the repository.

## 2. Variable precedence

GitLab has a defined precedence order for variables from different sources. Higher-precedence variables can override lower-precedence ones. The full order is version- and feature-sensitive, so consult the current documentation before relying on a particular override behavior.

Security implications:
- A user-supplied pipeline variable can override a lower-precedence variable in some configurations.
- A predefined variable may be overridden by a higher-precedence variable.
- Untrusted users may influence pipeline behavior if they can supply variables or modify CI configuration.
- Prefer pipeline inputs for typed pipeline parameters where supported, and restrict who can supply pipeline variables.

Do not design security decisions around a variable value that an untrusted caller can freely override.

## 3. Add project CI/CD variables

Typical UI workflow:
1. Open the GitLab project.
2. Go to **Settings → CI/CD**.
3. Expand **Variables**.
4. Select **Add variable**.
5. Enter a key and value.
6. Choose the type, environment scope, and visibility/protection flags.
7. Save the variable.

Use group variables for approved shared configuration. Use project-level variables when a value should be limited to one project.

## 4. Masked, hidden, and protected variables

| Setting | Purpose | Important limitation |
|---|---|---|
| Masked | Replaces matching secret text in job logs | Does not stop malicious code from reading or sending the value elsewhere |
| Hidden | Prevents the saved value from being revealed in settings after creation | Must be selected when creating a new variable; does not prevent job access |
| Protected | Limits availability to pipelines on protected branches/tags, subject to MR pipeline settings | Protection depends on ref and project configuration |
| Environment scope | Limits a variable to matching deployment environments | Ensure the job's environment name matches the scope |

GitLab's current masked-variable requirements include a single-line value of at least eight characters and character restrictions. Disable variable expansion when appropriate, especially for secrets containing special characters. Check current docs for exact validation requirements.

## 5. File-type variables

A file-type variable stores the value in a temporary file and exposes the file path as the environment variable. This is useful for certificates, SSH keys, and configuration files.

Example job:

```yaml
deploy:
  stage: deploy
  script:
    - test -f "$SSH_PRIVATE_KEY"
    - chmod 600 "$SSH_PRIVATE_KEY"
    - ssh -i "$SSH_PRIVATE_KEY" user@example.invalid "echo connected"
```

Configure `SSH_PRIVATE_KEY` in GitLab settings with **Type: File**. Use a safe test host in a lab; do not connect to an unauthorized system. Avoid printing the file contents.

## 6. Environment-scoped variables

Environment scopes let a variable be available only to jobs targeting a matching environment.

Example:

```yaml
deploy_staging:
  stage: deploy
  environment:
    name: staging
  script:
    - echo "Staging configuration is available"

deploy_production:
  stage: deploy
  environment:
    name: production
  script:
    - echo "Production configuration is available"
```

Create separate variables such as `DEPLOY_TOKEN` with scopes `staging` and `production`, and use distinct credential values. Do not reuse production credentials in test environments.

## 7. Safely use variables in scripts

Prefer passing values through the job environment and quote shell expansions:

```yaml
deploy:
  script:
    - 'test -n "$DEPLOY_TOKEN"'
    - 'printf "%s\n" "Deployment credential is configured"'
```

Avoid:
- `echo "$SECRET"` or `printenv` in jobs with secrets.
- `set -x` / shell tracing around secret use.
- Putting secrets in command-line arguments when tools can read them from environment or files.
- Constructing shell commands with untrusted variable contents.
- Uploading secret-containing files as artifacts or caches.

## 8. External secrets

GitLab supports integrations with external secret providers such as HashiCorp Vault, Google Cloud Secret Manager, Azure Key Vault, and AWS Secrets Manager. Jobs explicitly request secrets, and supported integrations use ID tokens for authentication. Availability depends on GitLab tier and provider configuration.

Illustrative Vault example (configure a compatible provider and authentication first):

```yaml
deploy:
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.example.com
  secrets:
    DB_PASSWORD:
      vault: production/database/password@ops
      token: $VAULT_ID_TOKEN
  script:
    - test -n "$DB_PASSWORD"
    - echo "Database secret retrieved"
```

By default, an external secret is commonly provided as a file-type variable: the variable contains a path to a file holding the secret. Use the `file: false` option only when the consuming tool requires the value directly and the provider syntax supports it.

## 9. Protect pipelines from secret exfiltration

- Review changes to `.gitlab-ci.yml`, included files, and scripts before running pipelines with protected secrets.
- Treat fork merge requests and untrusted branches carefully.
- Do not run untrusted pipeline code in a privileged parent-project context with access to secrets.
- Restrict who can create pipelines with arbitrary variables.
- Use protected branches/tags and protected environments for deployments.
- Prefer external secret managers for high-value credentials.
- Use trusted, isolated runners for jobs with sensitive credentials.
- Rotate a credential immediately if it may have been exposed.

## 10. Troubleshooting

| Symptom | Possible cause | Checks |
|---|---|---|
| Variable is empty | Scope mismatch, protected ref restriction, or variable not available to pipeline | Check environment scope, protected ref, key spelling |
| Masked value is rejected | Value violates masking requirements | Check length, single-line requirement, and allowed characters |
| Wrong value used | Higher-precedence variable overrides it | Inspect all variable sources and restrict pipeline variable overrides |
| File variable path missing | Variable configured as ordinary variable or unavailable to job | Confirm Type: File and variable scope |
| External secret fails | Provider auth, ID token audience, role, or secret path mismatch | Check provider configuration and job logs without printing secret |
| Secret appears in logs | Script printed it or transformed it so masking did not match | Stop pipeline, rotate secret, remove exposure, audit logs |

## Security checklist
- [ ] No secrets are committed to `.gitlab-ci.yml` or repository files.
- [ ] Sensitive variables are masked and hidden where supported.
- [ ] Production credentials are protected and environment-scoped.
- [ ] Different environments use different credentials.
- [ ] Pipeline-variable permissions and precedence are understood.
- [ ] Untrusted merge requests cannot access privileged secrets.
- [ ] File variables are used for certificates/keys when suitable.
- [ ] External secret managers are considered for high-value credentials.
- [ ] Logs, artifacts, caches, and debug traces are checked for leakage.
- [ ] Exposed credentials are rotated and incidents are reviewed.

## Official documentation
- [CI/CD variables](https://docs.gitlab.com/ci/variables/)
- [Use external secrets in CI/CD](https://docs.gitlab.com/ci/secrets/)
- [Pipeline security](https://docs.gitlab.com/ci/pipeline_security/)
- [CI/CD YAML syntax reference](https://docs.gitlab.com/ci/yaml/)
