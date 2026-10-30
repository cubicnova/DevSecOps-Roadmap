# SAST Remediation — Examples

Examples use Python for clarity. Adapt APIs and validation to the actual framework, database driver, and operating system.

## 1. SQL injection

**Vulnerable:**

```python
def get_user(cursor, email):
    query = "SELECT * FROM users WHERE email = '" + email + "'"
    cursor.execute(query)
    return cursor.fetchall()
```

**Remediated:**

```python
def get_user(cursor, email):
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )
    return cursor.fetchall()
```

Use the placeholder syntax required by the database driver. Add a test containing quotes and SQL metacharacters and verify they are treated as data.

## 2. Cross-site scripting

**Vulnerable:**

```python
from flask import request

@app.get("/hello")
def hello():
    name = request.args.get("name", "")
    return "<h1>Hello " + name + "</h1>"
```

**Remediated with template autoescaping:**

```python
from flask import render_template, request

@app.get("/hello")
def hello():
    name = request.args.get("name", "")
    return render_template("hello.html", name=name)
```

`hello.html`:

```html
<h1>Hello {{ name }}</h1>
```

Keep autoescaping enabled and avoid marking untrusted values as safe. Use context-appropriate APIs for non-HTML-text contexts.

## 3. Command injection

**Vulnerable:**

```python
import os

def show_file(filename):
    os.system("cat " + filename)
```

**Remediated direction:**

```python
import subprocess
from pathlib import Path

BASE = Path("/srv/reports").resolve()
ALLOWED = {"daily.txt", "monthly.txt"}

def show_file(filename):
    if filename not in ALLOWED:
        raise ValueError("Invalid report")
    target = (BASE / filename).resolve()
    if target.parent != BASE:
        raise ValueError("Invalid path")
    return subprocess.run(
        ["cat", str(target)],
        shell=False,
        check=True,
        capture_output=True,
        text=True
    ).stdout
```

This example assumes the allowed files are direct children of `BASE`. A production design must also consider symlinks, file replacement races, permissions, and platform-specific behavior.

## 4. Path traversal

**Vulnerable:**

```python
from pathlib import Path

def read_document(filename):
    return Path("/srv/docs", filename).read_text()
```

**Safer pattern:**

```python
from pathlib import Path

BASE = Path("/srv/docs").resolve()
ALLOWED = {"guide.txt", "policy.txt"}

def read_document(filename):
    if filename not in ALLOWED:
        raise ValueError("Unknown document")
    target = (BASE / filename).resolve()
    if target.parent != BASE:
        raise ValueError("Invalid document path")
    return target.read_text(encoding="utf-8")
```

For more complex directory structures, use a carefully designed containment check and address symlink/race conditions. Server-generated identifiers are often preferable to accepting paths from users.

## 5. Hardcoded secret

**Vulnerable:**

```python
API_TOKEN = "replace-with-real-secret"
```

**Remediated direction:**

```python
import os

API_TOKEN = os.environ["SERVICE_API_TOKEN"]
```

In production, inject the value from a secret manager or protected deployment configuration. Rotate any credential that was committed or exposed. Do not log the secret.

## 6. Weak password hashing

**Vulnerable:**

```python
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

**Remediated using Werkzeug:**

```python
from werkzeug.security import generate_password_hash, check_password_hash

def store_password(password):
    return generate_password_hash(password, method="scrypt")

def verify_password(stored_hash, candidate):
    return check_password_hash(stored_hash, candidate)
```

Use a supported, maintained password-hashing implementation and tune parameters for the deployment environment. Never store plaintext passwords.

## 7. IDOR / broken object authorization

**Vulnerable:**

```python
@app.get("/documents/<int:document_id>")
def get_document(document_id):
    return Document.query.get_or_404(document_id).content
```

**Remediated direction:**

```python
@app.get("/documents/<int:document_id>")
@login_required
def get_document(document_id):
    document = Document.query.filter_by(
        id=document_id,
        owner_id=current_user.id
    ).first_or_404()
    return document.content
```

The authorization condition must match the application's sharing, role, and tenancy model. Apply it to every read, update, and delete operation.

## 8. SSRF

**Risky pattern:**

```python
import requests

def fetch_url(url):
    return requests.get(url, timeout=5)
```

**Safer design direction:**

- Accept a business identifier instead of an arbitrary URL when possible.
- Map identifiers to fixed, approved destinations.
- Restrict outbound network access at the network layer.
- Validate destination addresses and redirects.
- Block loopback, private, link-local, and metadata ranges as appropriate.
- Account for DNS rebinding and redirect chains.

A simple hostname check alone is not a complete SSRF defense.

## 9. Remediation regression test example

```python
def test_get_user_uses_parameter_binding(fake_cursor):
    get_user(fake_cursor, "alice' OR '1'='1")
    sql, params = fake_cursor.executed
    assert "?" in sql
    assert params == ("alice' OR '1'='1",)
```

This test assumes a fake cursor that records the SQL and parameter tuple. It verifies the application calls the parameterized API; integration tests should also verify the actual database driver behavior.

## 10. Remediation pull request template

```markdown
## Security finding
- Alert / ticket:
- Rule / CWE:
- Severity:

## Root cause
Describe the vulnerable data flow or missing control.

## Remediation
Explain the code change and why it addresses the root cause.

## Verification
- [ ] Regression test added
- [ ] Unit/integration tests pass
- [ ] SAST rerun
- [ ] Relevant dynamic/security tests completed
- [ ] Reviewer approval

## Residual risk
Document remaining limitations, if any.
```
