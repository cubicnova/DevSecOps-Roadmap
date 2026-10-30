# CodeQL Examples

These examples are learning material. Validate language-library APIs and CLI options against the CodeQL version installed in your environment.

## 1. Check the CLI

```bash
codeql version
codeql resolve languages
codeql resolve packs
```

## 2. Create a Python database

Run from the root of a small Python project:

```bash
codeql database create db-python \
  --language=python \
  --source-root=.
```

Inspect the database:

```bash
codeql database info db-python
```

## 3. Analyze with standard Python queries

```bash
codeql database analyze db-python \
  codeql/python-queries \
  --format=sarif-latest \
  --output=python-results.sarif
```

## 4. Basic QL query: identify calls by name

Save as `FindDangerousCall.ql` in a Python query pack:

```ql
/**
 * @name Find calls to dangerous_function
 * @description Flags calls that require a security review.
 * @kind problem
 * @id cubicnova/find-dangerous-call
 */

import python

from Call call
where call.getFunc().toString() = "dangerous_function"
select call, "Review this call and its arguments."
```

This is a teaching query. A production query should use robust API identification and language-library abstractions rather than relying only on rendered text.

## 5. Example vulnerable Python code

```python
import sqlite3

def find_user(connection, username):
    sql = "SELECT * FROM users WHERE name = '" + username + "'"
    return connection.execute(sql).fetchall()
```

Safer parameterized version:

```python
def find_user(connection, username):
    return connection.execute(
        "SELECT * FROM users WHERE name = ?",
        (username,)
    ).fetchall()
```

## 6. Command execution review

Potentially unsafe:

```python
import os

def run_report(report_name):
    os.system("cat reports/" + report_name)
```

Safer design: avoid shell interpretation and validate the requested identifier against an allowlist. If a subprocess is necessary, pass an argument list and constrain the accessible file.

```python
import subprocess

ALLOWED_REPORTS = {"daily.txt", "monthly.txt"}

def run_report(report_name):
    if report_name not in ALLOWED_REPORTS:
        raise ValueError("Unknown report")
    return subprocess.run(
        ["cat", f"reports/{report_name}"],
        check=True,
        capture_output=True,
        text=True
    )
```

The allowlist and path design must still be reviewed for the application's operating system and directory layout.

## 7. Create a query pack

```bash
mkdir -p custom-codeql/queries
cd custom-codeql
```

Create `qlpack.yml`:

```yaml
name: cubicnova/security-queries
version: 1.0.0
dependencies:
  codeql/python-all: "*"
```

Create a query under `queries/`, then resolve dependencies and compile using the installed CLI:

```bash
codeql pack install
codeql pack compile .
```

## 8. Analyze using a custom pack

From a directory where the database is available:

```bash
codeql database analyze db-python \
  ./custom-codeql \
  --format=sarif-latest \
  --output=custom-results.sarif
```

Use the correct pack path and ensure its dependencies are installed.

## 9. Run a single query

```bash
codeql query run \
  custom-codeql/queries/FindDangerousCall.ql \
  --database=db-python \
  --output=results.bqrs
```

Decode the results:

```bash
codeql bqrs decode results.bqrs \
  --format=table \
  --output=results.txt
```

For a production reporting workflow, prefer `database analyze` when you need interpreted results and SARIF.

## 10. GitHub Actions CodeQL workflow outline

```yaml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
      actions: read
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: python
      - uses: github/codeql-action/analyze@v3
```

Use the official workflow generator/current documentation to select the correct build mode and action versions for your repository.

## 11. Review SARIF output

```bash
python -m json.tool python-results.sarif > python-results-pretty.json
```

Inspect `runs[].results[]` for rule IDs, messages, locations, and code flows. Do not publish SARIF artifacts publicly if they expose sensitive source details.

## 12. Secure coding comparison

| Weak pattern | Better direction |
|---|---|
| SQL string concatenation | Parameterized query |
| Shell command from user input | Avoid shell; use fixed executable and validated arguments |
| User-controlled filesystem path | Allowlist identifiers and enforce canonical directory boundaries |
| Hardcoded credentials | Secret manager or protected CI secret |
| Unsafe deserialization | Use safe formats and strict schemas |

## 13. Suggested repository layout

```text
03-CodeQL/
├── README.md
├── examples.md
├── practical.md
└── solution.md
```
