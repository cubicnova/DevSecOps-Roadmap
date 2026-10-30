# Taint Analysis — Solutions and Explanations

These are reference solutions. Exact scanner findings depend on the language, framework, tool version, and configured source/sink models.

## Solution 1 — Source and sink identification

| Scenario | Source | Sink | Main risk |
|---|---|---|---|
| Request parameter in SQL | HTTP query parameter | SQL execution API | SQL injection |
| Header written to logs | HTTP header | Logger | Sensitive data disclosure or log injection |
| Uploaded filename in file path | Upload metadata | File read/write | Path traversal |
| User URL passed to HTTP client | HTTP parameter | Outbound request | SSRF |
| Request value inserted into HTML | HTTP parameter | HTML/DOM rendering | XSS |

The value may pass through several variables and helper functions before reaching the sink.

## Solution 2 — SQL flow

Vulnerable pattern:
```python
username = request.args.get("username")
query = "SELECT * FROM users WHERE name = '" + username + "'"
cursor.execute(query)
```

Safer:
```python
username = request.args.get("username")
cursor.execute(
    "SELECT * FROM users WHERE name = ?",
    (username,)
)
```

Use the placeholder format required by the database driver. Do not interpolate values into SQL. For table or column names that cannot be bound as values, select from a strict server-side allowlist.

## Solution 3 — Interprocedural flow

Manual trace:
```text
request.args.get("name")
       |
       v
handler.name
       |
       v
build_query(name)
       |
       v
returned SQL string
       |
       v
cursor.execute(query)
```

A tool that only matches a dangerous API call may flag the sink without proving the source. A taint-aware engine can attempt to follow the value across the function boundary. Verify the path in the tool output.

## Solution 4 — Command injection

Safer direction:
```python
import subprocess

ALLOWED_ACTIONS = {
    "status": ["/usr/bin/service", "example", "status"],
}

def run_action(action):
    if action not in ALLOWED_ACTIONS:
        raise ValueError("Unsupported action")

    subprocess.run(ALLOWED_ACTIONS[action], check=True)
```

The user chooses a predefined action, not an arbitrary command. Avoid `shell=True`; validate all arguments and keep executable paths fixed.

## Solution 5 — XSS

For plain text:
```javascript
element.textContent = userInput;
```

For rich HTML, use a maintained sanitizer configured for the exact allowed HTML policy. The sanitizer should be tested and reviewed. HTML escaping is context-dependent; a control appropriate for HTML text may not be sufficient for JavaScript, CSS, or URL contexts.

## Solution 6 — Path traversal

A robust approach is to map a public document identifier to a fixed server-side file rather than accepting arbitrary paths:
```python
from pathlib import Path

DOCUMENTS = {
    "guide": Path("/srv/docs/guide.txt"),
    "policy": Path("/srv/docs/policy.txt"),
}

def read_document(document_id):
    path = DOCUMENTS.get(document_id)
    if path is None:
        raise ValueError("Unknown document")
    return path.read_text()
```

This avoids treating user input as a filesystem path. If paths must be constructed, canonicalize them and enforce containment under an approved base directory while accounting for symlinks and race conditions.

## Solution 7 — SSRF

A robust design:
- Accept a logical destination identifier rather than an arbitrary URL.
- Resolve it through a server-side allowlist.
- Restrict schemes and ports.
- Validate resolved IP addresses and re-check after DNS changes.
- Validate every redirect target.
- Block internal, loopback, link-local, and metadata ranges as appropriate.
- Enforce outbound firewall or proxy policy.

Do not rely on a string prefix test such as `url.startswith("https://trusted.example")`.

## Solution 8 — Sensitive logging

Avoid:
```python
logger.info("Authorization: %s", token)
```

Prefer:
```python
logger.info("Authorization header present: %s", bool(token))
```

If correlation is required, use a non-secret request ID. Do not log bearer tokens, passwords, session cookies, or private keys. Ensure test logs and retained artifacts are also checked.

## Solution 9 — Semgrep taint rule

Illustrative rule:
```yaml
rules:
  - id: training-request-to-sql
    mode: taint
    languages: [python]
    message: Request input may reach SQL execution.
    severity: ERROR
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: cursor.execute($QUERY)
```

Run:
```bash
semgrep scan --config rules/python-taint.yml samples/
```

A useful rule should include:
- Framework-specific source patterns.
- The correct database sink signatures.
- Appropriate sanitizer/parameterization handling.
- Positive vulnerable samples.
- Negative safe samples.
- Documentation of limitations.

Do not infer that every call to `cursor.execute` is vulnerable; parameterized queries are normally the correct defense for SQL values.

## Solution 10 — Sanitizers and validators

Evaluate the control against the exact sink:
- SQL: bound parameters, not HTML escaping.
- HTML: context-aware encoding or vetted HTML sanitization.
- Shell: avoid shell interpretation and use safe argument handling.
- Filesystem: allowlisted identifiers or canonicalized containment.
- SSRF: destination validation plus network-level egress controls.

A validator that checks a string is numeric may be useful for a numeric business rule, but it does not automatically make that value safe for HTML or shell use.

## Solution 11 — Static versus dynamic analysis

| Static taint analysis | Dynamic taint analysis |
|---|---|
| Examines code without executing it | Tracks data during execution |
| Can identify unexecuted paths | Observes only exercised paths |
| May report infeasible paths | Can provide runtime evidence |
| Depends on code and framework models | Depends on runtime instrumentation and test coverage |
| Useful early in development | Useful during integration and runtime testing |

Neither method replaces code review, threat modeling, or other security testing.

## Solution 12 — CI/CD and triage

A sensible pipeline policy:
1. Run taint analysis on merge requests or protected branches.
2. Publish machine-readable findings where supported.
3. Fail on high-confidence, high-impact findings according to agreed policy.
4. Route ambiguous findings to an AppSec review.
5. Require owner, rationale, and expiry for accepted exceptions.
6. Re-scan after remediation and preserve regression tests.

Never make the pipeline green by suppressing every finding. Track the source-to-sink path and document why a finding is or is not exploitable.

## Common mistakes

- Treating every sanitizer as universally safe.
- Ignoring indirect flows through helper functions or object fields.
- Assuming a finding proves exploitability.
- Assuming no finding proves the application is secure.
- Confusing a source with a sink.
- Forgetting sensitive-data flows where the source is confidential rather than attacker-controlled.
- Excluding large directories to reduce alert counts.
- Testing SSRF or injection against systems without authorization.

## Evaluation rubric

| Area | Marks |
|---|---:|
| Taint concepts and terminology | 15 |
| Source/sink identification | 15 |
| Propagation and interprocedural tracing | 15 |
| Vulnerability examples and remediation | 20 |
| Semgrep/CodeQL rule understanding | 15 |
| Static/dynamic comparison | 10 |
| CI/CD integration and triage report | 10 |
| **Total** | **100** |

A strong submission demonstrates at least three source-to-sink flows, context-appropriate remediation, positive and negative tests, and a clear explanation of tool limitations.
