# Build and Test Stages — Suggested Solutions

These are reference answers. Equivalent approaches are acceptable if they are correct, repeatable, and explained.

## Solution 1 — Identify the stages

| Stage | Purpose | Typical failure |
|---|---|---|
| Checkout | Obtain source at a specific revision | Repository access or checkout failure |
| Install | Install declared dependencies | Missing package, incompatible version, network issue |
| Lint/static checks | Detect style, type, or suspicious-code issues | Lint rule or type check fails |
| Build | Compile or transform source into output | Syntax, compilation, or bundling error |
| Unit test | Validate isolated behavior | Assertion fails |
| Integration test | Validate component interactions | Service or database interaction fails |
| Package | Create a distributable output | Packaging command or required file missing |
| Artifact upload | Preserve or transfer output | Incorrect path or upload failure |

## Solution 2 — Run unit tests

Run:

```bash
python -m unittest -v
```

The example should report four passing tests. A non-zero exit status indicates that the test command failed, which should normally make a required CI test step fail.

## Solution 3 — Add test cases

Example additional tests:

```python
def test_add_zero(self):
    self.assertEqual(add(0, 7), 7)

def test_add_decimals(self):
    self.assertAlmostEqual(add(0.1, 0.2), 0.3)

def test_divide_negative_numbers(self):
    self.assertEqual(divide(-10, 2), -5)
```

For floating-point results, `assertAlmostEqual` is generally more appropriate than direct equality because many decimal fractions cannot be represented exactly in binary floating-point.

## Solution 4 — Build validation

Run:

```bash
python -m compileall -q .
```

A successful result shows that Python source files compiled to bytecode without syntax errors. It does not guarantee correct logic, valid external service interactions, or expected application behavior. Automated tests are still necessary.

## Solution 5 — GitHub Actions workflow

Save the workflow as:

```text
.github/workflows/build-test.yml
```

Commit and push:

```bash
git add calculator.py test_calculator.py .github/workflows/build-test.yml
git commit -m "Add build and test workflow"
git remote -v
git push origin main
```

If no remote exists, add your own repository URL with `git remote add origin https://github.com/OWNER/REPOSITORY.git`. Replace the placeholder with your test repository. If your default branch is not `main`, update the workflow branch filters.

## Solution 6 — Intentional test failure

Change:

```python
self.assertEqual(add(2, 3), 6)
```

The test fails because the function returns `5`. CI should report the test step and job as failed. Restore the expected value before continuing.

## Solution 7 — Quality gate with `needs`

```yaml
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
      - run: echo "Packaging after tests pass"
```

The `needs: test` dependency prevents the package job from running after a failed or skipped prerequisite under normal conditions. A production pipeline should make all required checks explicit and avoid bypassing them.

## Solution 8 — Preserve test reports

Use an upload step with `if: always()` so it can run after a previous step fails. Ensure the report file is created before the test command runs, or use a test runner that always writes its report. If no file exists, configure the upload step's missing-file behavior intentionally.

For example:

```yaml
- name: Upload test report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: unittest-report
    path: test-reports/unittest-report.txt
    if-no-files-found: warn
```

This does not make the test pass; it only helps preserve diagnostic output.

## Solution 9 — Test matrix

Use a matrix only for versions the application claims to support:

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12"]
```

Set `python-version: ${{ matrix.python-version }}` in the Python setup step. Each matrix entry runs the job with that version, helping reveal compatibility issues.

## Solution 10 — Cache versus artifact

- **Cache:** package-manager downloads, reusable dependency data, or other expensive-to-recreate inputs.
- **Artifact:** built distribution, test report, coverage output, or diagnostic bundle from a particular run.

A cache is an optional performance optimization and may be evicted or missed. A release artifact should be explicitly produced, retained according to policy, and traceable to a source revision.

## Solution 11 — Security check

A suitable solution depends on the project. For Python, teams may use a linter/static analyzer and a dependency vulnerability scanner. Pin tool versions where practical, define severity thresholds, and document whether findings fail the build or create an advisory report. Avoid claiming a clean scan proves the application is secure.

## Solution 12 — Build-stage threat review

| Risk | Example mitigation |
|---|---|
| Malicious or compromised dependency | Lock versions, review changes, scan dependencies, use trusted registries |
| Secret leakage | Secret manager, minimal exposure, log redaction, credential rotation |
| Untrusted code on privileged runner | Isolated ephemeral runners and no production secrets for untrusted PRs |
| Artifact tampering or confusion | Restrict artifact write access, record commit and digest, promote immutable outputs |
| Sensitive test output | Use synthetic data, sanitize logs, restrict artifact access and retention |
| Excessive workflow permissions | Set minimum token permissions and elevate only where required |

## Solution 13 — Artifact traceability

Record the full source commit SHA, workflow run ID, package version/name, build timestamp, and a checksum or container image digest. Preserve this metadata with the artifact. Promote the same immutable artifact to later environments rather than rebuilding from a moving branch.

## Stretch challenge guidance

- **Coverage:** measure meaningful behavior coverage and avoid setting a threshold without a baseline.
- **Validation tests:** cover both valid inputs and invalid/error cases.
- **Separate jobs:** use dependencies where one stage must wait for another; parallelize independent checks where sensible.
- **Concurrency:** avoid canceling a deployment that is already modifying a live environment.
- **Build metadata:** include commit and version information without secrets.
- **Lockfiles:** pin transitive dependency versions where the package ecosystem supports it and review updates.

## Final review

A good build-and-test pipeline is repeatable, fails clearly when required checks fail, preserves useful diagnostic reports, limits permissions, and produces artifacts that can be traced to their source.
