# Sample CI/CD Pipeline Examples

These examples use GitHub Actions YAML. Save workflow files under `.github/workflows/` in a test repository before running them. Replace placeholder commands with commands supported by your application.

## Example 1: Pull request validation

File: `.github/workflows/ci.yml`

```yaml
name: Pull Request CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Check out source
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run unit tests
        run: |
          if [ -d tests ]; then python -m unittest discover -s tests; else echo "No tests directory found"; fi
```

**Discuss:** This is a starter pattern, not a production-pinned workflow. For production, review and pin actions to verified full commit SHAs and make the test command fail if tests are required but missing.

## Example 2: Build and package an artifact

File: `.github/workflows/package.yml`

```yaml
name: Package Application

on:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  package:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create distributable archive
        run: |
          mkdir -p dist
          tar --exclude=.git --exclude=dist -czf dist/source-bundle.tar.gz .

      - name: Calculate checksum
        run: sha256sum dist/source-bundle.tar.gz > dist/source-bundle.tar.gz.sha256

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: source-bundle
          path: dist/
          if-no-files-found: error
```

**Discuss:** A source archive is not the same as a compiled or containerized production artifact. For real projects, build the actual deployable output and include only required files.

## Example 3: Reusable test workflow

File: `.github/workflows/reusable-tests.yml`

```yaml
name: Reusable Python Tests

on:
  workflow_call:
    inputs:
      python-version:
        description: Python version to test
        required: false
        type: string
        default: "3.12"

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
      - name: Install test tooling
        run: python -m pip install --upgrade pip
      - name: Run tests
        run: python -m unittest discover -s tests
```

Caller workflow:

```yaml
name: Application CI

on:
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    uses: ./.github/workflows/reusable-tests.yml
    with:
      python-version: "3.12"
```

Reusable workflows are called at the job level. A called workflow cannot elevate token permissions beyond what the caller grants; permissions can remain the same or become more restrictive.

## Example 4: Deployment gate (illustrative)

File: `.github/workflows/deploy-staging.yml`

```yaml
name: Deploy to Staging

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Explain deployment placeholder
        run: |
          echo "Add your approved deployment command here."
          echo "Use environment-scoped credentials and a previously built artifact."
```

Configure the `staging` environment in repository settings and add appropriate protection rules and secrets. Do not paste credentials directly into YAML or command-line arguments.

## Example 5: Quality gate using a test result

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: python -m unittest discover -s tests

  publish:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Publish placeholder
        run: echo "Publish only after the test job succeeds."
```

The `needs: test` dependency ensures the publish job does not proceed when the required test job fails or is skipped.

## Review checklist

- [ ] Triggers are limited to intended branches and events.
- [ ] Token permissions are explicitly minimized.
- [ ] Required tests fail the workflow when they fail.
- [ ] Secrets are not available to untrusted pull-request code.
- [ ] Build outputs are separated from source and logs.
- [ ] Deployment uses a protected environment.
- [ ] Third-party actions and reusable workflows are reviewed and pinned appropriately.
