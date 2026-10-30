# GitLab CI/CD Variables and Secrets — Practical Exercises

## Prerequisites
- A GitLab project with CI/CD enabled and a working runner.
- Permission to manage project CI/CD variables.
- A sample repository and `.gitlab-ci.yml`.
- Dummy values only; do not use production credentials.

## Lab 1: Define YAML variables
1. Define `APP_NAME` and `APP_ENV` at the top level of `.gitlab-ci.yml`.
2. Add a job-level `LOG_LEVEL`.
3. Print the non-sensitive values.
4. Record which jobs can access each variable.

**Expected result:** You understand global and job-level variable scope.

## Lab 2: Inspect predefined variables
1. Create a job that prints `CI_PROJECT_PATH`, `CI_COMMIT_REF_NAME`, `CI_COMMIT_SHORT_SHA`, and `CI_PIPELINE_SOURCE`.
2. Run it from a branch and a merge request pipeline.
3. Compare the values.
4. Consult GitLab's predefined variable reference.

**Expected result:** You can identify useful pipeline metadata without hardcoding it.

## Lab 3: Add a project-level variable
1. Open **Settings → CI/CD → Variables**.
2. Add a non-sensitive variable named `DEPLOY_REGION`.
3. Use it in a job.
4. Change the value in settings and rerun the pipeline.
5. Confirm the pipeline uses the updated value.

**Expected result:** Project settings can supply configuration without editing YAML.

## Lab 4: Configure masked and hidden values
1. Create a dummy token of at least eight characters, meeting GitLab's current masked-value requirements.
2. Add it as `LAB_TOKEN`.
3. Select masked visibility and hidden visibility if available.
4. Run a job that checks whether it is set without printing it.
5. Review the settings UI and job log.

**Expected result:** You can distinguish masking from hiding. Neither prevents malicious job code from exfiltrating a secret.

## Lab 5: Protect a variable
1. Protect the default branch in repository settings.
2. Mark `LAB_TOKEN` as protected.
3. Run a pipeline on the protected branch.
4. Run a pipeline on an unprotected feature branch.
5. Compare availability without printing the token.

**Expected result:** You understand protected-variable availability and the importance of ref protection.

## Lab 6: File-type variable
1. Generate a disposable test file containing non-sensitive sample text.
2. Add its contents as a variable named `LAB_CONFIG` with **Type: File**.
3. Create a job that checks `test -f "$LAB_CONFIG"`.
4. Read only a harmless marker from the file.
5. Remove the test variable when finished.

**Expected result:** The variable contains a temporary file path rather than the file contents.

## Lab 7: Environment scope
1. Create `staging` and `production` environments.
2. Add two different dummy `DEPLOY_TOKEN` values with matching environment scopes.
3. Create one job for each environment.
4. Check whether the token is present, but do not print it.
5. Explain why different environments should use different credentials.

**Expected result:** You can scope values to deployment targets.

## Lab 8: Variable precedence
1. Define a harmless `APP_MODE` in YAML.
2. Define the same key in project settings.
3. If permitted, supply a pipeline variable with the same key.
4. Observe which value is used.
5. Read the current GitLab precedence documentation and write down the relevant order.

**Expected result:** You understand that higher-precedence sources can override lower-precedence values and that this can create security risks.

## Lab 9: External secrets concept
1. Read GitLab's external secrets documentation.
2. Draw the flow: GitLab job → ID token → provider authentication → secret retrieval → job.
3. Identify the provider role, audience, secret path, and job permissions required.
4. If you have a lab provider and supported GitLab tier, configure a test secret.
5. Verify retrieval without displaying the secret.

**Expected result:** You can explain why external secret managers reduce long-lived credential storage in CI settings.

## Lab 10: Secret-leak review
Review a sample pipeline for these unsafe patterns:
- `echo "$API_TOKEN"`
- `env` or `printenv`
- `set -x` while secrets are present
- `curl` sending secret values to unknown destinations
- artifacts containing credential files
- untrusted merge-request code running with protected credentials

For each issue, document the impact and a safe remediation.

**Expected result:** You can identify common secret-exposure paths.

## Lab 11: Rotate a dummy credential
1. Create a disposable dummy token.
2. Configure it as a project variable.
3. Replace it with a new dummy value.
4. Rerun a validation job.
5. Document the rotation process and ownership.

**Expected result:** You understand how to update credentials without committing them to source control.

## Lab 12: Build a secure deployment configuration
1. Use non-sensitive YAML variables for application name and region.
2. Store a dummy deployment credential in GitLab settings.
3. Mark it masked and protected where appropriate.
4. Scope it to the staging environment.
5. Use a file variable for a sample configuration file.
6. Add a manual deployment job and configure protected environment rules where supported.
7. Review the logs and artifacts for accidental disclosure.

**Expected result:** A pipeline separates ordinary configuration from sensitive credentials and applies appropriate deployment controls.

## Lab deliverables
- `.gitlab-ci.yml` with safe variable usage.
- Screenshots of variable settings with all values obscured.
- Results from protected-ref and environment-scope tests.
- A variable-precedence note.
- A diagram or explanation of external secret retrieval.
- A secret-leak review with remediation actions.
