# Examples — GitHub Actions Matrix Strategies

These examples are designed for a test repository. Adjust runtime versions and action versions to match your project and supply-chain policy.

## Example 1: Test multiple Node.js versions

```yaml
name: Node compatibility

on: [push, pull_request]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: ['20', '22']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
```

## Example 2: Cross-platform matrix

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python: ['3.11', '3.12']
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: python --version
      - run: python -m compileall .
```

This matrix creates six combinations before any exclusions.

## Example 3: Exclude an unsupported combination

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python: ['3.10', '3.11', '3.12']
    exclude:
      - os: windows-latest
        python: '3.10'
```

The original matrix contains six combinations. One exclusion leaves five.

## Example 4: Add matrix metadata with include

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: ['20', '22']
    include:
      - os: ubuntu-latest
        node: '22'
        run_coverage: true
      - os: windows-latest
        node: '22'
        run_coverage: false
```

Use the metadata in a step:

```yaml
- name: Show coverage selection
  env:
    RUN_COVERAGE: ${{ matrix.run_coverage }}
  run: echo "Coverage enabled: $RUN_COVERAGE"
```

Make sure the key is present for every combination that uses it, or define defaults intentionally.

## Example 5: Limit parallel execution

```yaml
strategy:
  max-parallel: 2
  matrix:
    database: [postgres, mysql, sqlite]
    python: ['3.11', '3.12']
```

This matrix contains six combinations and runs at most two simultaneously.

## Example 6: Let an experimental version fail

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    continue-on-error: ${{ matrix.experimental }}
    strategy:
      fail-fast: false
      matrix:
        runtime: ['20', '22']
        experimental: [false]
        include:
          - runtime: '24'
            experimental: true
    steps:
      - uses: actions/checkout@v4
      - name: Display runtime
        env:
          RUNTIME_VERSION: ${{ matrix.runtime }}
        run: echo "Testing runtime $RUNTIME_VERSION"
```

The experimental configuration is allowed to fail without failing the workflow. Keep stable, required combinations blocking.

## Example 7: Name artifacts by matrix values

```yaml
- name: Create sample report
  env:
    OS_NAME: ${{ matrix.os }}
    PYTHON_VERSION: ${{ matrix.python }}
  run: |
    mkdir -p reports
    printf 'OS=%s\nPython=%s\n' "$OS_NAME" "$PYTHON_VERSION" > reports/summary.txt

- uses: actions/upload-artifact@v4
  with:
    name: report-${{ matrix.os }}-python-${{ matrix.python }}
    path: reports/summary.txt
```

Distinct artifact names avoid collisions when several matrix jobs upload reports.

## Example 8: Dynamic matrix from a previous job

```yaml
name: Dynamic matrix example

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  define:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: echo 'matrix={"python":["3.11","3.12"]}' >> "$GITHUB_OUTPUT"

  test:
    needs: define
    runs-on: ubuntu-latest
    strategy:
      matrix: ${{ fromJSON(needs.define.outputs.matrix) }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: python --version
```

For dynamic matrices, only generate values from trusted, validated inputs. Bound the list size so the job count stays manageable.
