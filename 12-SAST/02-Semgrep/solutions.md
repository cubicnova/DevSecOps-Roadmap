# Semgrep — Solutions and Explanations

Use these as reference answers. Exact findings depend on the Semgrep version, ruleset, engine, and language support.

## Solution 1 — Installation

Example:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install semgrep
semgrep --version
```

On Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
python -m pip install semgrep
semgrep --version
```

An isolated environment avoids modifying system-managed Python packages.

## Solution 2 — First scan

```bash
semgrep scan --config auto sample_app/
semgrep scan --config auto --json -o semgrep-results.json sample_app/
```

Review the rule ID, matched code, location, severity, and message. `--config auto` selects an appropriate configuration based on Semgrep's supported automatic configuration behavior; inspect the selected rules and scan output rather than assuming every possible rule ran.

## Solution 3 — Custom `eval()` rule

```yaml
rules:
  - id: training-python-eval
    languages: [python]
    message: Avoid eval() on untrusted or dynamic input.
    severity: ERROR
    metadata:
      category: security
      cwe: "CWE-95"
    pattern: eval($EXPR)
```

Run:
```bash
semgrep scan --config rules/python-security.yml sample_app/
```

This detects a syntax pattern. It does not prove that the argument is attacker-controlled or that the call is reachable.

## Solution 4 — Process execution

Rule:
```yaml
rules:
  - id: training-python-shell-true
    languages: [python]
    message: Review shell=True when command input can be influenced externally.
    severity: WARNING
    pattern: subprocess.run(..., shell=True, ...)
```

Safer design:
```python
import subprocess

def list_directory():
    subprocess.run(["/usr/bin/ls", "-la"], check=True)
```

When arguments must vary, validate each argument against an allowlist and avoid shell interpretation. The safest design may be to use a library API rather than spawning a process.

## Solution 5 — Weak hash

Rule:
```yaml
rules:
  - id: training-python-md5
    languages: [python]
    message: MD5 is not suitable for security-sensitive hashing.
    severity: WARNING
    pattern: hashlib.md5(...)
```

For password storage, use a dedicated password hashing scheme such as Argon2id, scrypt, or bcrypt with appropriate parameters and salts. For file-integrity checks, use a modern cryptographic hash such as SHA-256 where collision resistance is required. The correct choice depends on the security purpose.

## Solution 6 — DOM injection

Rule:
```yaml
rules:
  - id: training-js-innerhtml
    languages: [javascript, typescript]
    message: Avoid inserting untrusted data with innerHTML.
    severity: WARNING
    pattern: $EL.innerHTML = $DATA
```

For plain text:
```javascript
element.textContent = userInput;
```

If rich HTML is necessary, sanitize it with a vetted library and enforce the application's content security policy. `textContent` is not a replacement when intentionally rendering formatted HTML.

## Solution 7 — Pattern operators

Example:
```yaml
rules:
  - id: training-shell-api
    languages: [python]
    message: Review shell command execution.
    severity: WARNING
    pattern-either:
      - pattern: os.system($CMD)
      - pattern: subprocess.run($CMD, shell=True, ...)
```

Use `patterns` when all listed conditions must match. Use `pattern-not` to exclude a carefully defined safe form, but test exclusions against both positive and negative cases to avoid hiding findings.

## Solution 8 — Taint analysis

A taint rule generally needs:
- Source: untrusted request or input data.
- Sink: sensitive operation such as SQL execution.
- Propagation: transformations that preserve attacker influence.
- Sanitizer: a validated operation that makes the data safe for the specific sink.

Illustrative structure:
```yaml
rules:
  - id: training-request-to-sql
    mode: taint
    languages: [python]
    message: Untrusted request input may reach SQL execution.
    severity: ERROR
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: cursor.execute($QUERY)
```

This example is intentionally incomplete for production. Real rules should model the actual framework, database API, parameterized query behavior, and relevant engine capabilities. Verify syntax and test with positive and negative cases.

## Solution 9 — JSON and SARIF

```bash
semgrep scan --config auto --json -o results.json .
semgrep scan --config auto --sarif -o results.sarif .
```

JSON is useful for custom processing and automation. SARIF is a standardized static-analysis interchange format supported by many code-scanning systems. Review the output before uploading it to a service; reports can reveal file paths and code snippets.

## Solution 10 — GitLab CI

Standalone CLI example:
```yaml
stages:
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

For repeatable production builds, pin the container image to a reviewed version or digest. `--error` makes the command return a failing exit status when findings are reported, so decide carefully whether all findings should block the pipeline or whether a staged severity policy is more appropriate.

For Semgrep AppSec Platform integration, use the documented `semgrep ci` command and configure its token securely. Do not expose platform credentials to untrusted fork pipelines.

GitLab-managed SAST is a separate integration:
```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

Review GitLab's current analyzer support and avoid unintentionally running duplicate scans.

## Solution 11 — Triage and suppression

A good triage record includes:
- Rule ID and finding location.
- Data source and sink.
- Reachability and attacker control.
- Existing validation or mitigation.
- Reproduction or reasoning.
- Fix or suppression rationale.
- Owner and review date.

If suppressing a finding, scope it to the exact rule and line where possible. A broad file or directory exclusion can hide future vulnerabilities.

## Solution 12 — Team ruleset quality

A mature custom rule includes:
- A stable, descriptive rule ID.
- Clear security-focused message and remediation guidance.
- Narrow language and framework scope.
- Positive and negative tests.
- Severity calibrated to likely impact.
- References to CWE or internal standards.
- Documented limitations and an owner.

Example repository structure:
```text
02-Semgrep/
├── README.md
├── examples.md
├── practical.md
├── solutions.md
└── rules/
    ├── python-security.yml
    └── javascript-security.yml
```

## Evaluation rubric

| Area | Marks |
|---|---:|
| Installation and CLI scanning | 10 |
| Rule syntax and operators | 20 |
| Python and JavaScript security rules | 15 |
| Taint analysis understanding | 15 |
| GitLab CI integration | 15 |
| Finding triage and suppression | 15 |
| Evidence and documentation | 10 |
| **Total** | **100** |

A strong submission includes repeatable scans, tested custom rules, both positive and negative test cases, and documented remediation decisions.
