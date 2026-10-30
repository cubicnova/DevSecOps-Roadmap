# Solutions — Matrix Strategies

These model answers illustrate the expected reasoning. Adjust runtime versions and action versions to your project and repository policy.

## Solution 1: Basic matrix
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: python --version
```
Expected: two jobs, one per Python version.

## Solution 2: Cross-platform job count
Two operating systems × two runtime versions = four combinations. If there are three operating systems and two versions, the matrix produces six combinations before `include` or `exclude`.

## Solution 3: Exclusion
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python: ['3.10', '3.11', '3.12']
    exclude:
      - os: windows-latest
        python: '3.10'
```
The original matrix has \(2 \times 3 = 6\) combinations. One exclusion leaves five.

## Solution 4: Include metadata
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: ['20', '22']
    include:
      - os: ubuntu-latest
        node: '22'
        coverage: true
```
The metadata can be read as `${{ matrix.coverage }}` for the matching combination. If a step expects the value in every combination, define a default or add the field to each relevant combination. `include` can augment matching combinations or create additional combinations depending on whether it would overwrite existing matrix values.

## Solution 5: Failure behavior
- With `fail-fast: true`, a failing matrix job causes queued and in-progress jobs in the matrix to be cancelled.
- With `fail-fast: false`, other combinations continue, making it easier to collect the full test picture.
- `continue-on-error` is per job; it can mark a particular experimental combination as allowed to fail.
Do not confuse a job allowed to fail with a matrix that stops early.

## Solution 6: Experimental version
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
```
The stable combinations remain required; the experimental combination is permitted to fail. Confirm the `include` expansion and resulting `matrix.experimental` value in the Actions run.

## Solution 7: Parallel limit
```yaml
strategy:
  max-parallel: 2
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    runtime: ['20', '22']
```
Six combinations are generated, with at most two matrix jobs running at once. Actual throughput also depends on available runner capacity and account limits.

## Solution 8: Unique artifact names
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: report-${{ matrix.os }}-${{ matrix.python }}
    path: reports/summary.txt
```
Including matrix values avoids jobs attempting to upload to the same artifact name. Ensure the artifact path exists and that every job produces its own report.

## Solution 9: Dynamic matrix
Producer:
```yaml
outputs:
  matrix: ${{ steps.set-matrix.outputs.matrix }}
steps:
  - id: set-matrix
    run: echo 'matrix={"python":["3.11","3.12"]}' >> "$GITHUB_OUTPUT"
```
Consumer:
```yaml
needs: define
strategy:
  matrix: ${{ fromJSON(needs.define.outputs.matrix) }}
```
For real dynamic data, validate allowed values, reject malformed JSON, and enforce a maximum number of combinations. Do not let untrusted input select privileged runners or change security policy.

## Solution 10: Matrix optimization
Suppose a matrix has 3 operating systems × 3 runtimes × 2 databases = 18 combinations. If two OS/runtime/database combinations are unsupported, use `exclude` to reduce the total to 16. Split slow integration tests from quick unit tests if they have different cadence or resource needs.

GitHub documents a maximum of 256 generated matrix jobs per workflow run. Keep cost, runtime, coverage, and maintainability in view when expanding matrices.

## Final review checklist
- Matrix size is calculated before adding dimensions.
- Exclusions represent real unsupported or unnecessary combinations.
- `include` metadata is defined where used.
- Failure semantics match the desired CI policy.
- Concurrency is bounded when resources are shared.
- Artifacts have unique names.
- Dynamic matrices are validated and constrained.
