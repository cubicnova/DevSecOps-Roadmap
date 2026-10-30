# CodeQL Practical Solutions

These are reference solutions and expected reasoning. CLI output and findings vary by CodeQL release, language, query suite, and sample code.

## 1. Verify the environment

```bash
codeql version
codeql resolve languages
codeql resolve packs
```

A successful version command confirms the executable is available. The language list indicates which extractors are present in the installed bundle; it does not guarantee that every framework or build configuration is supported.

## 2. Create a Python database

```bash
codeql database create db-python \
  --language=python \
  --source-root=.

codeql database info db-python
```

If creation fails, check the source root, permissions, extractor availability, and database path. Use a clean output directory if the target database already exists.

## 3. Run standard queries

```bash
codeql database analyze db-python \
  codeql/python-queries \
  --format=sarif-latest \
  --output=python-results.sarif
```

The result count is project-dependent. A clean scan does not prove the application is secure; query coverage, supported frameworks, reachable code, and analysis limitations matter.

## 4. Sources and sinks

Example reasoning:

- Source: HTTP request parameter, route parameter, uploaded filename, or other externally controlled value.
- Sink: SQL execution, shell execution, file access, HTML output, or another security-sensitive operation.
- Sanitizer/validator: parameterized query, context-aware output encoding, strict allowlist, or safe API.
- Path: the sequence of assignments, calls, and transformations between source and sink.

Validation must match the sink's security context. Generic string filtering is not a universal sanitizer.

## 5. SQL injection remediation

Unsafe:

```python
sql = "SELECT * FROM users WHERE name = '" + username + "'"
connection.execute(sql)
```

Safer:

```python
connection.execute(
    "SELECT * FROM users WHERE name = ?",
    (username,)
)
```

The database driver treats the supplied value as data rather than SQL syntax. Keep table and column identifiers fixed or select them from strict allowlists because bind parameters generally represent values, not arbitrary SQL identifiers.

## 6. Command injection remediation

Avoid constructing shell command strings from user-controlled data. Prefer a fixed executable with an argument array:

```python
subprocess.run(
    ["tool-name", "--report", validated_report],
    check=True,
    shell=False
)
```

Validate `validated_report` against a known set and enforce filesystem boundaries. `shell=False` reduces shell interpretation risk but does not automatically make arbitrary arguments safe for the invoked program.

## 7. Basic query pack

Example structure:

```text
custom-codeql/
├── qlpack.yml
└── queries/
    └── FindDangerousCall.ql
```

Example pack metadata:

```yaml
name: cubicnova/security-queries
version: 1.0.0
dependencies:
  codeql/python-all: "*"
```

Then:

```bash
cd custom-codeql
codeql pack install
codeql pack compile .
```

For a maintained pack, pin or constrain dependencies deliberately and test compatibility when upgrading the CLI.

## 8. Basic query review

Illustrative query:

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

This is a beginner demonstration, not a robust production detector. String rendering may not uniquely identify a target. Improve it by using the language library's semantic call-target model, then add positive and negative tests.

## 9. Analyze with a custom pack

```bash
codeql database analyze db-python \
  ./custom-codeql \
  --format=sarif-latest \
  --output=custom-results.sarif
```

Run from a location where both the database and pack path resolve. If the pack is not found, check the path, `qlpack.yml`, and dependency installation.

## 10. GitHub Actions integration

A minimal learning outline:

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

For production, use the current official CodeQL workflow guidance. Compiled projects may require build steps or an explicit build mode. Review action pinning, repository feature availability, permissions, and pull-request trust boundaries.

## 11. Finding triage template

Record:

| Field | Example of what to capture |
|---|---|
| Rule ID | Exact identifier from the alert |
| Location | File and line |
| Source | Whether input is externally controlled |
| Sink | Sensitive API or operation |
| Flow | Relevant assignments and calls |
| Controls | Validation, encoding, authorization, or parameterization |
| Impact | Confidentiality, integrity, availability |
| Verdict | True positive, false positive, or needs investigation |
| Remediation | Root-cause fix |
| Verification | Regression test and rescan |

Do not close a finding solely because the reported line appears harmless. Review the full data path and application context.

## 12. SARIF inspection

```bash
python -m json.tool python-results.sarif > pretty-results.json
```

Inspect `runs`, `tool.driver.rules`, and `results`. A result may include a `ruleId`, message, physical location, and code flows. Treat paths and snippets in SARIF as potentially sensitive.

## 13. Regression testing

A complete remediation should include:

1. A test for the unsafe input or behavior.
2. A fix at the correct trust boundary.
3. A passing test demonstrating expected safe behavior.
4. A new CodeQL analysis using the same query suite.
5. A record of any remaining alert and its explanation.

A finding disappearing is useful evidence, but it should be combined with code review and tests.

## 14. Secure pipeline design checklist

- Trigger on pull requests and protected-branch pushes.
- Include scheduled analysis.
- Grant only required workflow permissions.
- Do not expose privileged secrets to untrusted fork code.
- Select the correct language and build mode.
- Keep action versions current and consider full-SHA pinning.
- Upload SARIF using the supported action.
- Assign alert owners and define triage SLAs.
- Store scan artifacts with appropriate access controls.

## 15. Common troubleshooting

| Symptom | Checks |
|---|---|
| `codeql: command not found` | PATH and installation |
| Unsupported language | CLI bundle and supported language list |
| Database creation fails | Source root, build command, extractor logs |
| Build cannot be traced | Build mode and build command |
| Pack dependency error | `qlpack.yml`, network/authentication, compatible versions |
| Query compilation error | Imports, metadata, QL API and pack version |
| No results | Query suite, language coverage, code path, database content |
| SARIF upload fails | Workflow permissions, action configuration, repository feature availability |

## Key lesson

CodeQL is most effective when standard analysis is integrated into development, custom queries are tested and maintained, and findings are triaged by understanding the actual source-to-sink path. It complements—not replaces—secure design, code review, dependency scanning, and dynamic testing.
