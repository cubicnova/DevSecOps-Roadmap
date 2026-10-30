# Semgrep — Examples

These examples are intended for a local training repository. Some rules are deliberately simplified to teach syntax; review and test them before production use.

## 1. Scan a project

```bash
semgrep scan --config auto .
```

Scan a directory:
```bash
semgrep scan --config auto src/
```

Scan with a local rules directory:
```bash
semgrep scan --config rules/ .
```

## 2. Output formats

Text output:
```bash
semgrep scan --config auto .
```

JSON:
```bash
semgrep scan --config auto --json -o results.json .
```

SARIF:
```bash
semgrep scan --config auto --sarif -o results.sarif .
```

## 3. Python: dynamic evaluation

Vulnerable training code:
```python
def calculate(expression):
    return eval(expression)
```

Introductory rule:
```yaml
rules:
  - id: training-python-eval
    languages: [python]
    message: Avoid eval() on untrusted input.
    severity: ERROR
    pattern: eval($EXPR)
```

## 4. Python: shell command execution

Training code:
```python
import subprocess

def run_command(user_value):
    subprocess.run(user_value, shell=True)
```

Rule:
```yaml
rules:
  - id: training-python-shell-true
    languages: [python]
    message: Review shell=True with dynamically constructed commands.
    severity: WARNING
    pattern: subprocess.run(..., shell=True, ...)
```

Safer direction: pass an argument list and avoid invoking a shell when it is unnecessary:
```python
subprocess.run(["/usr/bin/tool", "--", validated_value], check=True)
```
Validate arguments against an allowlist appropriate to the application.

## 5. Python: hard-coded credential pattern

Training code:
```python
API_KEY = "training-example-not-a-real-secret"
```

Rule:
```yaml
rules:
  - id: training-hardcoded-api-key
    languages: [python]
    message: Possible hard-coded API key. Use a secret manager or environment injection.
    severity: WARNING
    pattern-regex: (?i)(api[_-]?key|secret|token)\s*=\s*["'][^"']{8,}["']
```

Regex rules can be noisy. Use a dedicated secret scanner for comprehensive credential detection.

## 6. Python: weak hash algorithm

Training code:
```python
import hashlib
digest = hashlib.md5(data).hexdigest()
```

Rule:
```yaml
rules:
  - id: training-python-md5
    languages: [python]
    message: MD5 is unsuitable for security-sensitive hashing.
    severity: WARNING
    pattern: hashlib.md5(...)
```

For password storage, use a purpose-built password hashing function such as Argon2id, scrypt, or bcrypt rather than a fast general-purpose hash.

## 7. JavaScript: dangerous HTML insertion

Training code:
```javascript
function renderProfile(userInput) {
  document.querySelector("#profile").innerHTML = userInput;
}
```

Rule:
```yaml
rules:
  - id: training-js-innerhtml
    languages: [javascript, typescript]
    message: Avoid assigning untrusted data to innerHTML.
    severity: WARNING
    pattern: $EL.innerHTML = $DATA
```

Prefer safe DOM APIs such as `textContent` when rendering text. If rich HTML is required, use a vetted sanitizer and context-appropriate controls.

## 8. JavaScript: dynamic code evaluation

Training code:
```javascript
function runExpression(value) {
  return eval(value);
}
```

Rule:
```yaml
rules:
  - id: training-js-eval
    languages: [javascript, typescript]
    message: Avoid eval() with dynamic input.
    severity: ERROR
    pattern: eval($VALUE)
```

## 9. Multiple alternatives

```yaml
rules:
  - id: training-dangerous-process-api
    languages: [python]
    message: Review dynamic process execution.
    severity: WARNING
    pattern-either:
      - pattern: os.system($CMD)
      - pattern: os.popen($CMD)
      - pattern: subprocess.call($CMD, shell=True, ...)
```

## 10. Taint-mode concept (illustrative)

Taint rules describe a source, a sink, and optional sanitizers. This conceptual example should be validated against the exact Semgrep engine and syntax version used by your team.

```yaml
rules:
  - id: training-python-request-to-sql
    mode: taint
    languages: [python]
    message: Untrusted request data may reach SQL execution.
    severity: ERROR
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: cursor.execute($QUERY)
```

This simplified rule may require framework-specific source patterns, propagation modeling, and sink refinement for a useful production detector.

## 11. GitLab CI: standalone Semgrep scan

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

Pin the image to a reviewed version or digest in production rather than relying on a floating tag.

## 12. GitLab CI: Semgrep AppSec Platform

```yaml
semgrep:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep ci
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

Configure the required platform token as a protected CI/CD variable. Confirm merge-request trust boundaries before exposing any token to pipelines from forks or untrusted branches.

## 13. GitLab-managed SAST template

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

GitLab manages the analyzer job and its ruleset. Review GitLab's current supported-language and analyzer documentation for your GitLab version and tier.

## 14. Exclude generated files

Create `.semgrepignore`:
```text
node_modules/
.venv/
build/
dist/
coverage/
generated/
```

Review exclusions carefully. Do not exclude source folders merely to reduce finding counts. GitLab's Semgrep-based analyzer has its own ignore behavior; consult the current GitLab documentation when using that analyzer.

## 15. Test a custom rule against a sample

```bash
semgrep scan --config rules/python-security.yml samples/
```

Use a small controlled sample containing both vulnerable and safe examples. Confirm that the rule detects the intended pattern and does not flag the safe example unexpectedly.
