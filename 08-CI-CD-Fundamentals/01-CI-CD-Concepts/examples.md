# CI/CD Concepts — Examples

These examples are designed for a learning repository. Start with the local Python example, then try the GitHub Actions workflow.

## 1. Minimal Python application

Create `app.py`:

```python
def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


if __name__ == "__main__":
    print(add(2, 3))
```

Create `test_app.py`:

```python
import unittest
from app import add


class TestAdd(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative_number(self):
        self.assertEqual(add(-2, 2), 0)

    def test_zero(self):
        self.assertEqual(add(0, 0), 0)


if __name__ == "__main__":
    unittest.main()
```

Run locally:

```bash
python app.py
python -m unittest -v
```

Expected application output: `5`. All three tests should pass.

## 2. Basic GitHub Actions CI workflow

Create `.github/workflows/ci.yml` at the **repository root**:

```yaml
name: Python CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    name: Run Python tests
    runs-on: ubuntu-latest
    steps:
      - name: Check out source
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Run unit tests
        run: python -m unittest -v
```

**Security note:** Major-version action references are used here for readability. For production, review and pin third-party actions to full commit SHAs, then update them through a controlled process.

What happens:

1. A push to `main`, a pull request targeting `main`, or a manual run triggers the workflow.
2. GitHub creates a runner and checks out the repository.
3. Python 3.12 is configured.
4. Unit tests run. A failing test makes the job fail.

## 3. Add linting as a quality gate

For a project that uses Ruff, add these steps after setting up Python:

```yaml
      - name: Install Ruff
        run: python -m pip install ruff

      - name: Lint source and tests
        run: ruff check .
```

For reproducible builds, pin development tools in a requirements or project lock file instead of installing an unconstrained latest version during each run.

## 4. Illustrative multi-job pipeline

This example demonstrates job dependencies. It is not a full deployment pipeline.

```yaml
name: Build and test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m unittest -v

  package:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create source archive
        run: |
          mkdir -p dist
          tar --exclude=.git --exclude=dist -czf dist/source.tar.gz .
      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: source-package
          path: dist/source.tar.gz
          if-no-files-found: error
```

The `package` job starts only after `test` succeeds because of `needs: test`. For a real application, package the actual build output rather than blindly archiving the entire repository.

## 5. Environment promotion concept

```text
Build once -> Test artifact -> Deploy same artifact to staging
           -> Smoke test -> Approval -> Deploy same artifact to production
```

Avoid rebuilding from a moving branch separately for staging and production. Promote the same immutable artifact or image digest so the tested bits are the released bits.

## 6. Common trigger examples

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

- `push`: runs after matching branch pushes.
- `pull_request`: validates proposed changes.
- `workflow_dispatch`: allows a user to start the workflow manually.

Use event filters thoughtfully. Ensure important validation cannot be skipped merely by pushing to an unprotected branch.

## 7. Safer workflow permissions

Start with minimal permissions and grant more only to jobs that need them:

```yaml
permissions:
  contents: read
```

A workflow that only checks out source and runs tests usually does not need repository write permissions.

## 8. Anti-patterns and improvements

| Anti-pattern | Better practice |
|---|---|
| API key committed in YAML | Use a secret store or short-lived identity |
| Deploy on every branch push | Separate validation from protected release/deploy events |
| One job runs every task | Split stages where dependencies and permissions benefit |
| Tests fail but pipeline remains green | Fail the job on required-check failure |
| Build different artifacts for staging and production | Promote one immutable artifact |
| Untrusted PR runs on privileged self-hosted runner | Use isolated, ephemeral runners with no sensitive access |
| Floating action references in production without review | Pin reviewed action SHAs and maintain an update process |
| Print all environment variables while debugging | Print only non-sensitive diagnostic information |

## 9. Verify a workflow run

1. Commit the files and push to GitHub.
2. Open the repository's **Actions** tab.
3. Select the `Python CI` workflow.
4. Open the latest run and inspect each step's logs.
5. Intentionally introduce a failing assertion in a test branch.
6. Push the branch and verify that the job fails.
7. Revert the assertion and verify that the job passes.

Never put real credentials into a test workflow or commit them to the repository.
