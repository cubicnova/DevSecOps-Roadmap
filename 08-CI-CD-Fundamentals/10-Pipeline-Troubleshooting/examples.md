# Pipeline Troubleshooting — Examples

These examples are intentionally small and safe to adapt. Treat error messages as clues; confirm the root cause from logs and configuration.

## Example 1: Workflow does not run

**Symptom:** A push to `feature/docs-update` creates no workflow run.

```yaml
name: CI
on:
  push:
    branches:
      - main
```

**Diagnosis:** The workflow only listens for pushes to `main`. A push to another branch is filtered out.

**Possible fix:** If feature branches should be tested, widen the branch filter:

```yaml
name: CI
on:
  push:
    branches:
      - main
      - "feature/**"
  pull_request:
    branches:
      - main
```

Check the intended trigger policy before changing it.

## Example 2: YAML indentation error

**Symptom:** Workflow configuration is rejected before a job starts.

Incorrect:

```yaml
jobs:
  test:
  runs-on: ubuntu-latest
    steps:
      - run: echo "test"
```

Correct:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "test"
```

**Lesson:** Validate YAML and inspect indentation before debugging application code.

## Example 3: Dependency installation fails

**Symptom:** A Python pipeline fails while installing packages.

Potential causes:
- The Python version differs from the version expected by the project.
- A package version is unavailable for the runner's Python version or operating system.
- The package index is temporarily unreachable.
- A lockfile or requirements file contains an invalid pin.

Diagnostic commands:

```bash
python --version
python -m pip --version
python -m pip install -r requirements.txt -v
```

**Lesson:** Use verbose output temporarily and distinguish package-resolution errors from network errors.

## Example 4: Test step fails because of missing configuration

```python
import os

api_url = os.environ.get("API_URL")
if not api_url:
    raise RuntimeError("Required configuration missing: API_URL")
```

**Symptom:** Tests pass locally but fail in CI with `Required configuration missing: API_URL`.

**Diagnosis:** The CI job has not supplied the expected non-secret variable.

**Possible fix:** Configure `API_URL` at the appropriate repository, organization, or environment level. For sensitive values, use the platform's secret store. Do not hard-code credentials into the workflow.

## Example 5: Artifact name mismatch

Upload step:

```yaml
- name: Upload build
  uses: actions/upload-artifact@v4
  with:
    name: app-build
    path: dist/
```

Download step:

```yaml
- name: Download build
  uses: actions/download-artifact@v4
  with:
    name: release-build
    path: dist/
```

**Symptom:** The deployment job cannot locate the artifact.

**Diagnosis:** The upload name is `app-build`, while the download expects `release-build`.

**Fix:** Use the same name in both steps, and verify that the upload step actually ran and produced files.

## Example 6: Permission denied during deployment

**Symptom:** A deploy command returns HTTP 403 or an access-denied message.

Checklist:
1. Confirm which identity the job uses.
2. Check the minimum permissions required for the requested operation.
3. Verify that the secret or token is available to this event and environment.
4. Check environment protection rules and approval gates.
5. Avoid granting broad administrator permissions as a quick fix.

**Lesson:** A successful authentication does not guarantee authorization.

## Example 7: Intermittent network timeout

**Symptom:** Dependency download sometimes times out but succeeds on rerun.

Diagnostic commands (where installed and permitted):

```bash
getent hosts packages.example.invalid
curl -I --max-time 10 https://packages.example.invalid/
```

`packages.example.invalid` is a placeholder domain and will not resolve.

**Diagnosis approach:** Check DNS, TLS certificates, proxy/firewall policy, registry health, and rate limits. Retry only when the operation is safe and the failure appears transient.

## Example 8: Container build fails because a file is missing

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
CMD ["python", "-m", "src"]
```

**Symptom:** Docker reports that `requirements.txt` or `src/` cannot be found.

**Checks:**
- Is the build command using the expected build context?
- Are the files committed?
- Does `.dockerignore` exclude the required files?
- Is the capitalization correct? Linux paths are case-sensitive.

Example:

```bash
docker build -f Dockerfile .
```

Run from the directory intended to be the build context.

## Example 9: Job is unexpectedly skipped

**Symptom:** A deploy job shows as skipped even though tests passed.

```yaml
deploy:
  needs: test
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  steps:
    - run: echo "Deploying"
```

**Diagnosis:** The condition permits deployment only for `main`. Inspect the event and ref for the run before changing the condition. Also check upstream job results and any other conditions.

## Example 10: A practical root-cause note

```text
Incident: CI failed on commit abc1234
Impact: Build could not be promoted to staging
Detection: Unit-test job failed
Root cause: API_URL was not configured in the staging test environment
Resolution: Added the non-secret API_URL variable to the correct environment
Validation: Re-ran tests and the full pipeline successfully
Prevention: Added an early configuration validation step
Secrets exposed: No
```

## Example 11: Safe shell diagnostics

```yaml
- name: Check required configuration
  shell: bash
  run: |
    set -euo pipefail
    test -n "${API_URL:-}" || {
      echo "API_URL is missing"
      exit 1
    }
    echo "API_URL is configured"
```

This checks presence without printing the value. Use `set -x` cautiously because shell tracing may expose sensitive values.
