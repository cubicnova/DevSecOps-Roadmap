# 04 — Matrix Strategies

## Overview
GitHub Actions matrix strategies let one job definition run across multiple configurations, such as operating systems, language versions, database versions, or feature flags. A matrix reduces duplicated YAML and helps verify compatibility across supported environments.

This module explains matrix expansion, `include`, `exclude`, failure behavior, concurrency limits, and safe practical patterns.

## Learning objectives
By the end of this module, you should be able to:
- Create a matrix using one or more dimensions.
- Calculate how many jobs a matrix will create.
- Use `include` to add metadata or additional combinations.
- Use `exclude` to remove unsupported combinations.
- Control failure behavior with `fail-fast` and `continue-on-error`.
- Limit concurrent jobs using `max-parallel`.
- Use matrix values in runner selection and action inputs.
- Keep matrices manageable, reproducible, and secure.

## 1. Basic matrix

```yaml
name: Cross-platform tests

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [20, 22]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
```

Two operating systems × two Node.js versions produce four job combinations. Matrix variables are available through the `matrix` context, such as `${{ matrix.os }}` and `${{ matrix.node }}`.

## 2. Matrix expansion and job count
When dimensions are listed as arrays, GitHub creates the Cartesian product of those dimensions. For example:
- 3 operating systems
- 2 runtime versions
- 2 database versions

This produces \(3 \times 2 \times 2 = 12\) combinations before exclusions or extra configurations. GitHub documents a maximum of 256 generated jobs in a matrix for one workflow run, so avoid unbounded or excessively large matrices.

## 3. Excluding combinations
Use `exclude` for combinations that are unsupported, redundant, or too costly to test.

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python: ['3.11', '3.12']
    exclude:
      - os: windows-latest
        python: '3.11'
```

This starts with four combinations and removes one, leaving three. An exclusion can match a subset of the matrix fields.

## 4. Including metadata or combinations
`include` can attach extra values to matching combinations or add a new combination when it cannot be applied without overwriting an original matrix value.

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [20, 22]
    include:
      - os: ubuntu-latest
        node: 22
        coverage: true
      - os: ubuntu-latest
        node: 20
        coverage: false
```

A job can then read `${{ matrix.coverage }}`. Be precise about which combinations an `include` entry matches; it is not simply a universal append operation. Review the official docs when combining several `include` entries.

## 5. Failure behavior
- `strategy.fail-fast` defaults to `true`. If a matrix job fails, queued and in-progress matrix jobs may be cancelled.
- Set `fail-fast: false` when you want all combinations to finish and provide a fuller compatibility picture.
- `continue-on-error` applies to an individual job. It is useful for explicitly experimental configurations that are allowed to fail.

```yaml
strategy:
  fail-fast: false
  matrix:
    runtime: ['20', '22', '24']
    experimental: [false]
    include:
      - runtime: '24'
        experimental: true
continue-on-error: ${{ matrix.experimental }}
```

Use experimental allowances deliberately. Do not make required production configurations non-blocking just to obtain a green workflow.

## 6. Concurrency limits
`max-parallel` limits the number of matrix jobs that run at the same time.

```yaml
strategy:
  max-parallel: 2
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    runtime: ['20', '22']
```

The matrix defines six combinations, but no more than two of these matrix jobs run concurrently. This can control cost, rate limits, or contention for shared test infrastructure.

## 7. Dynamic matrices
A previous job can calculate a JSON matrix and expose it as a job output. A downstream job can parse that JSON with `fromJSON(...)`. Treat generated values as data from a trusted source, validate them, and keep the number of generated combinations bounded.

## 8. Security and reliability
- Use `permissions: contents: read` or another minimal permission set when possible.
- Do not let untrusted matrix values form shell commands without validation and safe quoting.
- Avoid passing secrets to jobs that do not need them.
- Pin action versions according to your repository's supply-chain policy.
- Be aware that each matrix combination can consume runner minutes and create artifacts with similar names.
- Include OS/runtime values in artifact names to prevent collisions.
- Avoid sharing mutable external test resources between parallel jobs unless the test is designed for concurrency.

## 9. Troubleshooting
- **More jobs than expected:** multiply the dimensions, then account for `include` and `exclude`.
- **A job gets cancelled after another fails:** check `fail-fast`.
- **Experimental job fails the workflow:** verify `continue-on-error` is set at the job level and driven by the intended matrix field.
- **Too much concurrency:** set `max-parallel`.
- **Wrong runtime or OS:** confirm the matrix context is referenced correctly.
- **Artifacts overwrite each other:** include matrix dimensions in artifact names.
- **Unexpected include behavior:** inspect whether each include object augments an original combination or creates a new one.

## Further reading
- [Running variations of jobs in a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
