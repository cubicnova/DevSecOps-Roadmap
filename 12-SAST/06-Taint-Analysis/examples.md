# Taint Analysis — Examples

The examples demonstrate common source-to-sink paths. They are intentionally small and should be used only in a local training environment.

## 1. Direct SQL injection flow

Vulnerable:
```python
def find_user(request, cursor):
    username = request.args.get("username")  # source
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return cursor.execute(query)             # sink
```

Safer:
```python
def find_user(request, cursor):
    username = request.args.get("username")
    return cursor.execute(
        "SELECT * FROM users WHERE name = ?",
        (username,)
    )
```

Use the parameter binding syntax supported by the database driver. Parameterization protects values; dynamic table or column identifiers require a separate allowlist strategy.

## 2. SQL flow through a helper

```python
def make_query(value):
    return "SELECT * FROM accounts WHERE owner = '" + value + "'"

def handler(request, cursor):
    owner = request.args.get("owner")
    sql = make_query(owner)
    cursor.execute(sql)
```

A basic pattern rule may miss this relationship. A taint engine that follows function returns can model the source-to-sink path.

## 3. Command injection

Vulnerable:
```python
import subprocess

def convert(request):
    filename = request.args.get("file")
    command = "convert " + filename
    subprocess.run(command, shell=True)
```

Safer direction:
```python
import subprocess

ALLOWED_FORMATS = {"png", "jpg"}

def convert(format_name):
    if format_name not in ALLOWED_FORMATS:
        raise ValueError("Unsupported format")

    subprocess.run(
        ["/usr/bin/convert", "input.png", f"output.{format_name}"],
        check=True
    )
```

Use fixed executable paths and argument arrays. Validate every user-controlled argument; do not allow a user to choose arbitrary executable paths or options.

## 4. XSS through unsafe HTML output

Vulnerable:
```javascript
function showMessage(element, message) {
  element.innerHTML = message;
}
```

Safer for plain text:
```javascript
function showMessage(element, message) {
  element.textContent = message;
}
```

For rich HTML, use a maintained sanitizer configured for the intended content. Output encoding must match the context.

## 5. Path traversal

Vulnerable:
```python
from pathlib import Path

def read_document(request):
    name = request.args.get("name")
    return Path("/srv/docs/" + name).read_text()
```

Safer direction:
```python
from pathlib import Path

BASE = Path("/srv/docs").resolve()

def read_document(name):
    allowed = {"guide.txt", "policy.txt"}
    if name not in allowed:
        raise ValueError("Unknown document")

    target = (BASE / name).resolve()
    if target.parent != BASE:
        raise ValueError("Invalid path")

    return target.read_text()
```

A server-side identifier-to-file mapping is often safer than accepting arbitrary paths. Account for symlinks and platform-specific path behavior.

## 6. SSRF

Risky pattern:
```python
import requests

def fetch(request):
    url = request.args.get("url")
    return requests.get(url, timeout=5)
```

Safer design:
- Accept an identifier rather than an arbitrary URL.
- Map identifiers to approved destinations.
- Validate scheme, hostname, resolved IP, and redirects.
- Block loopback, link-local, private, and cloud metadata destinations as appropriate.
- Restrict outbound network access at the infrastructure layer.

A simple string-prefix check is not a reliable SSRF defense.

## 7. Sensitive data to log sink

Risky:
```python
def authenticate(request, logger):
    token = request.headers.get("Authorization")
    logger.info("request authorization=%s", token)
```

Safer:
```python
def authenticate(request, logger):
    token = request.headers.get("Authorization")
    logger.info("authorization header received: %s", bool(token))
```

Do not log passwords, access tokens, session identifiers, private keys, or unnecessary personal data.

## 8. Semgrep taint-mode example

Illustrative Python rule:
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

This is a starting point, not a complete production detector. Add framework-specific source patterns, accurate sinks, sanitizer models, and positive/negative tests.

## 9. Semgrep sanitizer concept

A sanitizer must be appropriate for the sink. In a rule, a team can model a function as a sanitizer when it truly makes the data safe for the specific operation. Do not declare a generic `clean()` function safe without reviewing its implementation.

Conceptual configuration:
```yaml
pattern-sanitizers:
  - pattern: escape_html($VALUE)
```

Use the exact syntax supported by the Semgrep engine and version. HTML escaping should not be modeled as a sanitizer for SQL or shell sinks.

## 10. CodeQL conceptual model

A CodeQL taint-tracking query generally:
1. Defines a source representing attacker-controlled data.
2. Defines a sink representing a dangerous operation.
3. Uses a taint-tracking configuration.
4. Optionally models sanitizers or additional propagation.
5. Produces a path query result showing how the source reaches the sink.

Use CodeQL's language-specific libraries and query help for the actual implementation.

## 11. Direct and indirect propagation

Direct:
```python
value = request.args.get("q")
query = value
execute(query)
```

Through a helper:
```python
def identity(value):
    return value

value = request.args.get("q")
query = identity(value)
execute(query)
```

A taint engine may follow both flows depending on language, engine, and interprocedural analysis configuration.

## 12. Safe versus unsafe control examples

| Control | SQL sink | HTML sink | Shell sink |
|---|---|---|---|
| Parameterized query | Appropriate | Not sufficient | Not sufficient |
| HTML escaping | Not sufficient | Appropriate for matching context | Not sufficient |
| Shell argument array | Not sufficient | Not sufficient | Safer command construction |
| Strict allowlist | Useful for identifiers | Useful for constrained content | Useful for arguments |
| Generic string replace | Unreliable | Unreliable | Unreliable |

The correct control is determined by the interpretation performed at the sink.
