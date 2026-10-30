# Build and Test Stages — Examples

The examples use Python's built-in `unittest` framework so the first lab does not require third-party test packages.

## 1. Create a small application

Create `calculator.py`:

```python
def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def divide(a: float, b: float) -> float:
    """Divide a by b; reject division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

Create `test_calculator.py`:

```python
import unittest
from calculator import add, divide


class TestCalculator(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_number(self):
        self.assertEqual(add(-2, 2), 0)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)


if __name__ == "__main__":
    unittest.main()
```

Run locally from the directory containing both files:

```bash
python -m unittest -v
```

All four tests should pass.

## 2. Basic build check

For this pure-Python example, a simple syntax/bytecode compilation check can act as a basic build validation:

```bash
python -m compileall -q .
```

This verifies that Python files compile. It does **not** prove that the application is functionally correct; tests are still required.

## 3. CI workflow with test report

Create `.github/workflows/build-test.yml` at the repository root:

```yaml
name: Build and Test

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
    name: Compile and test
    runs-on: ubuntu-latest
    steps:
      - name: Check out source
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Validate Python syntax
        run: python -m compileall -q .

      - name: Run tests and write test report
        run: |
          mkdir -p test-reports
          python -m unittest -v 2>&1 | tee test-reports/unittest-report.txt

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: unittest-report
          path: test-reports/unittest-report.txt
          if-no-files-found: warn
```

The `if: always()` upload step allows the report to be uploaded even if an earlier test step fails, provided the report file exists. The test command still fails the job if tests fail; `tee` returns the test command's status in the default GitHub Actions Bash shell.

## 4. Separate test and build jobs

This example shows job dependencies. It creates a zip archive only after the tests pass.

```yaml
name: Test and Package

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
      - run: python -m compileall -q .
      - run: python -m unittest -v

  package:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create source archive
        run: |
          mkdir -p dist
          zip -r dist/source.zip calculator.py test_calculator.py
      - name: Upload package
        uses: actions/upload-artifact@v4
        with:
          name: source-package
          path: dist/source.zip
          if-no-files-found: error
```

For a real project, package the actual release output and include only required files. This example packages source files for learning; it is not a production release process.

## 5. Testing a failure

Temporarily change this assertion:

```python
self.assertEqual(add(2, 3), 6)
```

Run:

```bash
python -m unittest -v
```

The test suite should fail because `add(2, 3)` returns `5`. Restore the correct expected value after confirming the failure.

## 6. Example test matrix

A matrix is useful when an application supports multiple Python versions:

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12"]
```

Use it inside a job and configure the Python setup step with:

```yaml
with:
  python-version: ${{ matrix.python-version }}
```

Only include versions that the project actually supports.

## 7. Build, cache, and artifact comparison

| Item | Example | Purpose |
|---|---|---|
| Build output | `dist/source.zip` | Output produced by a build command |
| Test report | `test-reports/unittest-report.txt` | Evidence of test results |
| Artifact upload | `actions/upload-artifact` | Retain or transfer files from a workflow run |
| Dependency cache | Cached package downloads | Reduce repeat download time |

Do not rely on a dependency cache as the only copy of a release artifact. Artifacts and caches solve different problems.

## 8. Security reminders

- The examples use major-version action references for readability. For production workflows, review and pin third-party actions to full commit SHAs.
- Keep `permissions` minimal.
- Do not store API keys or passwords in source code.
- Do not run untrusted pull-request code on a runner with production credentials.
- Use dependency lockfiles and review updates.
