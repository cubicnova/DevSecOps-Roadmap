# Semgrep — Static Application Security Testing

Semgrep is a fast, code-aware static analysis tool used to find security issues, bugs, and enforce secure coding patterns. It can run locally, in pre-commit workflows, and in CI/CD pipelines.

This module focuses on the Semgrep CLI, rule syntax, secure coding detections, custom rules, GitLab CI integration, triage, and practical remediation.

## Learning objectives

After completing this module, you should be able to:

- Explain SAST and how Semgrep differs from plain text search.
- Install and run the Semgrep CLI.
- Select rule packs and scan specific paths.
- Interpret JSON, text, and SARIF output.
- Write custom YAML rules using metavariables and pattern operators.
- Detect common Python and JavaScript security weaknesses.
- Integrate Semgrep into GitLab CI/CD.
- Triage findings, reduce false positives, and manage suppressions responsibly.
- Understand the limits of static analysis and validate findings safely.

## 1. SAST fundamentals

Static Application Security Testing analyzes source code without executing the application. Semgrep parses code and matches structural patterns, so rules can recognize code constructs rather than only matching raw text.

Examples of issues suitable for static analysis include:
- SQL queries assembled using untrusted input.
- Dangerous shell execution.
- Weak cryptographic algorithms.
- Hard-coded credentials.
- Unsafe deserialization patterns.
- Missing security controls around framework APIs.

Static analysis is not proof that an application is exploitable. Validate the data flow, runtime context, reachability, and applicable mitigations.

## 2. Installation

Use an isolated Python environment or an approved package manager. Example using `pipx`:

```bash
pipx install semgrep
semgrep --version
```

Alternative with Python pip in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install semgrep
semgrep --version
```

On Windows, activate the environment with:
```powershell
.venv\Scripts\Activate.ps1
python -m pip install semgrep
semgrep --version
```

Use the official installation guide for supported platforms and current installation methods.

## 3. First scan

From the root of a project:

```bash
semgrep scan --config auto .
```

For a local ruleset:
```bash
semgrep scan --config rules/ .
```

For a registry ruleset:
```bash
semgrep scan --config p/security-audit .
```

The exact rules available from a registry may evolve. Review the rule pack and licensing/feature requirements before adopting it in a production pipeline.

Useful options:
```bash
semgrep scan --help
semgrep scan --config auto --json -o semgrep-results.json .
semgrep scan --config auto --sarif -o semgrep-results.sarif .
semgrep scan --config auto --verbose .
```

## 4. Semgrep rule structure

Rules are YAML documents. A simple rule:

```yaml
rules:
  - id: python-dangerous-eval
    languages:
      - python
    message: Avoid eval() on data that may be influenced by users.
    severity: ERROR
    metadata:
      category: security
      technology:
        - python
    pattern: eval($INPUT)
```

Important fields:
- `id`: stable unique identifier.
- `languages`: language targets.
- `message`: explanation shown with the finding.
- `severity`: `ERROR`, `WARNING`, or `INFO`.
- `metadata`: optional categorization and references.
- `pattern`, `patterns`, `pattern-either`, `pattern-regex`: matching logic.

Run a custom rules file:
```bash
semgrep scan --config rules/python-security.yml .
```

## 5. Pattern operators

### Metavariables

`$X` matches an expression or syntax node:
```yaml
pattern: eval($X)
```

### Multiple conditions with `patterns`

All patterns must match:
```yaml
patterns:
  - pattern: cursor.execute($QUERY)
  - pattern-not: cursor.execute("SELECT ...")
```

This is only a simplified demonstration. A real SQL injection rule needs to model the framework and query construction accurately.

### Alternatives with `pattern-either`

Any branch can match:
```yaml
pattern-either:
  - pattern: os.system($CMD)
  - pattern: subprocess.call($CMD, shell=True)
```

### Negative patterns

Use `pattern-not` and related operators carefully. Overly broad exclusions can hide genuine findings.

### Taint analysis

Taint-mode rules identify sources, propagation, and sinks. They are useful for data-flow checks such as untrusted request data reaching SQL execution or command execution. Engine capabilities vary by edition and configuration; validate which engine supports the rule features you intend to use.

## 6. Example custom rules

Create `rules/python-security.yml`:

```yaml
rules:
  - id: python-eval-use
    languages: [python]
    message: Avoid eval() on untrusted or dynamic input.
    severity: ERROR
    metadata:
      category: security
      cwe: "CWE-95"
    pattern: eval($EXPR)

  - id: python-shell-true
    languages: [python]
    message: Review shell=True when command arguments can be influenced by users.
    severity: WARNING
    metadata:
      category: security
      cwe: "CWE-78"
    pattern: subprocess.$FUNC(..., shell=True, ...)
```

Run:
```bash
semgrep scan --config rules/python-security.yml .
```

These examples are intentionally introductory. Production rules should account for safe wrappers, framework-specific APIs, and context to avoid noisy results.

## 7. GitLab CI integration

### Semgrep CLI job

```yaml
stages:
  - test
  - security

semgrep:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep scan --config auto --error .
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH'
```

For AppSec Platform-managed CI features, Semgrep documents the `semgrep ci` workflow and token configuration. Keep tokens in protected CI/CD variables and never print them.

### GitLab-managed SAST template

GitLab also provides a SAST template that includes a Semgrep-based analyzer for supported languages/configurations:

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

Do not assume the standalone Semgrep CLI job and GitLab's Semgrep-based analyzer produce identical findings or reports. Choose one integration model or deliberately manage overlap.

## 8. Finding triage

For every finding:
1. Read the rule ID and matched code.
2. Understand the source, sink, and relevant data flow.
3. Check whether input is attacker-controlled.
4. Identify validation, encoding, parameterization, or other mitigations.
5. Reproduce safely in a local test environment if needed.
6. Fix the underlying weakness.
7. Add a regression test.
8. Document any accepted risk with owner, rationale, and review date.

Prioritize by exploitability, impact, reachability, exposure, and confidence—not severity label alone.

## 9. False positives and suppressions

Prefer fixing the code or refining a custom rule over suppressing a result. When suppressing:
- Use the narrowest possible scope.
- Suppress a specific rule ID rather than every rule.
- Add a short reason and link to the issue where appropriate.
- Require review and periodic expiry/revalidation.

Example:
```python
safe_internal_expression = validated_value  # nosemgrep: python-eval-use
```

Do not use a suppression unless the code has been reviewed and the risk is understood. Confirm the supported syntax for the Semgrep version and language.

## 10. Limitations

- Semgrep is not a substitute for dynamic testing, threat modeling, code review, or penetration testing.
- Community/OSS and platform engines can differ in cross-file and cross-function analysis capabilities.
- A rule can miss a vulnerability if the pattern or modeled data flow is incomplete.
- A finding may be a false positive when context or sanitization is not understood.
- Generated, minified, or unsupported code may need special handling.
- Results depend on the ruleset, engine, language support, and scan configuration.

## 11. Suggested project structure

```text
12-SAST/
└── 02-Semgrep/
    ├── README.md
    ├── examples.md
    ├── practical.md
    ├── solutions.md
    └── rules/
        ├── python-security.yml
        └── javascript-security.yml
```

## 12. Further reading

- [Semgrep documentation](https://semgrep.dev/docs/)
- [Semgrep CLI usage](https://semgrep.dev/docs/cli-usage/)
- [Semgrep rule syntax](https://semgrep.dev/docs/writing-rules/overview/)
- [Semgrep GitLab CI examples](https://semgrep.dev/docs/semgrep-ci/sample-ci-configs/)
- [GitLab SAST documentation](https://docs.gitlab.com/user/application_security/sast/)
- [GitLab SAST rulesets](https://docs.gitlab.com/user/application_security/sast/customize_rulesets/)

Use Semgrep only on code you own or are authorized to assess.
