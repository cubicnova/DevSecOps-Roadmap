# CodeQL

## Learning objectives

By the end of this module, learners should be able to:

- Explain how CodeQL represents source code as a queryable database.
- Distinguish CodeQL from conventional pattern-matching SAST tools.
- Set up and use the CodeQL CLI and GitHub code scanning.
- Create databases, run built-in query suites, and interpret SARIF results.
- Read and write basic QL queries and understand data-flow analysis.
- Organize custom queries into CodeQL packs and validate them.

## 1. What is CodeQL?

CodeQL is a semantic code analysis technology. It extracts information from a supported codebase into a database and lets analysts query that database using the QL language. A query can identify code patterns, relationships, and potentially vulnerable flows.

Unlike a simple text search, CodeQL can reason about program structure and, with suitable libraries and models, follow data from a source through transformations to a sink.

Typical uses include:

- Finding security weaknesses such as injection and unsafe path handling.
- Detecting correctness and maintainability issues.
- Enforcing organization-specific secure coding rules.
- Tracking data flow through application code.

## 2. CodeQL workflow

A typical CLI workflow is:

1. Install a compatible CodeQL CLI bundle.
2. Create a CodeQL database from source code or a build.
3. Select built-in or custom query packs.
4. Analyze the database.
5. Review results and export SARIF.
6. Fix findings, rerun analysis, and validate the remediation.

Conceptual command sequence:

```bash
codeql database create db-python \
  --language=python \
  --source-root=.

codeql database analyze db-python \
  codeql/python-queries \
  --format=sarif-latest \
  --output=results.sarif
```

The exact database creation options depend on language and build requirements. Compiled languages may require a successful build during database creation. Use the CLI version and language support documented for the project.

## 3. Core concepts

| Concept | Meaning |
|---|---|
| Extractor | Converts source/build information into database facts |
| CodeQL database | Structured representation of a codebase |
| QL | Declarative query language used to analyze the database |
| Query (`.ql`) | A rule that selects code elements or flows of interest |
| Library (`.qll`) | Reusable QL predicates, classes, and logic |
| Query pack | A distributable collection of queries and dependencies |
| Query suite (`.qls`) | A selection of queries to run |
| SARIF | Standard JSON format for static-analysis results |

## 4. CodeQL versus other SAST approaches

Traditional SAST tools may combine syntax rules, semantic analysis, and data-flow analysis. CodeQL's distinctive approach is to make extracted program information queryable. This supports reusable, reviewable queries and custom analysis.

CodeQL is not a replacement for threat modeling, manual review, dynamic testing, dependency analysis, or secure design. It can miss issues when relevant framework behavior or data-flow models are unavailable, and it can produce false positives or false negatives.

## 5. Languages and support

CodeQL supports a defined set of languages and frameworks. Coverage and build modes evolve, so check the current official supported-language and framework documentation before choosing it for a repository. Do not assume that every language, framework, generated source file, or build configuration is supported equally.

## 6. Installing and checking the CLI

Download the CodeQL CLI bundle from the official CodeQL releases/documentation. Follow the installation instructions for your operating system, then verify:

```bash
codeql version
codeql resolve languages
codeql resolve packs
```

Keep the CLI and query packs compatible. Avoid downloading binaries from untrusted mirrors.

## 7. Creating a database

For an interpreted language such as Python, a simple example is:

```bash
codeql database create db-python \
  --language=python \
  --source-root=.
```

For a compiled language, database creation commonly needs a build command:

```bash
codeql database create db-java \
  --language=java \
  --source-root=. \
  --command="mvn clean package -DskipTests"
```

Use the build command appropriate to the repository. Do not run untrusted build scripts on a privileged workstation or runner.

## 8. Running built-in queries

Example:

```bash
codeql database analyze db-python \
  codeql/python-queries \
  --format=sarif-latest \
  --output=codeql-results.sarif
```

A query suite determines which queries are selected. Security-extended or security-and-quality suites may increase coverage and runtime. Review the selected suite and its expected scope.

## 9. Understanding QL queries

A basic query has a `from`, `where`, and `select` structure:

```ql
/**
 * @name Example query
 * @description Finds calls to a selected function.
 * @kind problem
 * @id example/find-selected-call
 */

import python

from Call call
where call.getFunc().toString() = "dangerous_function"
select call, "Review this call."
```

This is an introductory illustration. QL APIs differ by language and CodeQL library version. Confirm the relevant language library types and predicates in the official documentation before using a query in production.

A query's metadata helps the CLI and code-scanning interface interpret its results. For `database analyze`, use valid metadata and the appropriate query kind.

## 10. Sources, sinks, and data flow

A source is an origin of potentially untrusted data, such as an HTTP request parameter. A sink is a sensitive operation, such as a SQL execution call or shell command. A sanitizer or validator may reduce risk if it is appropriate and correctly applied.

A path query can show how data travels from source to sink. CodeQL provides language-specific data-flow libraries; do not assume that a simplified example is a complete production query.

## 11. Custom query packs

A query pack is rooted at a directory containing `qlpack.yml`. It can include `.ql` queries, `.qll` libraries, query suites, and dependencies.

Illustrative pack structure:

```text
custom-codeql/
├── qlpack.yml
├── queries/
│   └── FindDangerousCall.ql
└── README.md
```

Example `qlpack.yml`:

```yaml
name: cubicnova/security-queries
version: 1.0.0
dependencies:
  codeql/python-all: "*"
```

Use a compatible dependency version for a production pack and validate it with the installed CLI. Pack metadata and supported properties can change across CLI versions.

## 12. GitHub Actions integration

GitHub code scanning can run CodeQL as part of CI. A typical workflow uses the official CodeQL action, with initialization, build (where required), and analysis steps. Use the current official starter workflow as the source of truth for action versions and configuration.

Example outline:

```yaml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "23 4 * * 1"

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
      actions: read
    strategy:
      fail-fast: false
      matrix:
        language: ["python"]
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
      - uses: github/codeql-action/analyze@v3
```

This is a learning skeleton, not a universal workflow. Compiled projects may need an explicit build mode or build steps. Pin actions to full commit SHAs in high-assurance environments and review permissions, supported languages, and current GitHub guidance.

## 13. Reading SARIF results

SARIF records tool metadata, rules, result messages, locations, and optional code flows. Review:

- Rule ID and severity.
- File path and line range.
- Data-flow path, if supplied.
- Query help and remediation guidance.
- Whether the finding is reachable and exploitable in the application's context.

A scanner finding is a lead for investigation, not proof of exploitability.

## 14. Triage and remediation

1. Reproduce the finding in the relevant source context.
2. Identify attacker-controlled inputs and security-sensitive operations.
3. Trace validation, canonicalization, and authorization boundaries.
4. Determine exploitability and impact.
5. Fix the root cause, not just the reported line.
6. Add regression tests.
7. Rerun the same query suite and confirm the result is resolved.
8. Document accepted risks and time-bound exceptions.

## 15. Best practices

- Run scans on pull requests and on a scheduled basis.
- Use least-privilege workflow permissions.
- Avoid exposing secrets to untrusted pull-request code.
- Keep CodeQL CLI, actions, and query packs updated.
- Start with standard queries before adding custom rules.
- Test custom queries against positive and negative examples.
- Use narrowly scoped exclusions with an owner and expiry.
- Treat SARIF as potentially sensitive because it can contain source paths and code snippets.
- Combine SAST with SCA, secret scanning, DAST, code review, and threat modeling.

## 16. Troubleshooting checklist

- Confirm `codeql version` and supported language.
- Confirm the source root and database path.
- For compiled languages, verify the build succeeds.
- Inspect database creation logs for extractor errors.
- Confirm query pack dependencies are downloaded and compatible.
- Check query metadata and query kind.
- Confirm the SARIF output path is writable.
- Review GitHub workflow permissions and action logs.

## References

- [CodeQL documentation](https://codeql.github.com/docs/)
- [GitHub CodeQL CLI: command-line scanning](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/scan-from-the-command-line)
- [Custom CodeQL queries](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/custom-queries)
- [CodeQL query packs](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/query-packs)
- [About CodeQL queries](https://codeql.github.com/docs/writing-codeql-queries/about-codeql-queries/)
