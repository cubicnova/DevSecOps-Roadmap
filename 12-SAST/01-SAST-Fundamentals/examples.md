# SAST Fundamentals — Examples

These examples illustrate common insecure patterns and safer alternatives. Run them only in a local training repository. Exact scanner findings depend on language, analyzer, ruleset, and version.

## 1. SQL injection — Python

### Vulnerable pattern

```python
import sqlite3

def get_user(username: str):
    connection = sqlite3.connect("training.db")
    query = "SELECT id, username FROM users WHERE username = '" + username + "'"
    return connection.execute(query).fetchall()
```

**Issue:** User-controlled data is concatenated into SQL syntax.

### Safer pattern

```python
import sqlite3

def get_user(username: str):
    connection = sqlite3.connect("training.db")
    query = "SELECT id, username FROM users WHERE username = ?"
    return connection.execute(query, (username,)).fetchall()
```

**Why safer:** The database driver treats the value as data rather than SQL syntax.

## 2. Cross-site scripting — Flask

### Vulnerable pattern

```python
from flask import Flask, request, Response

app = Flask(__name__)

@app.get("/hello")
def hello():
    name = request.args.get("name", "")
    return Response(f"<h1>Hello {name}</h1>", mimetype="text/html")
```

### Safer pattern

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.get("/hello")
def hello():
    name = request.args.get("name", "")
    return render_template_string("<h1>Hello {{ name }}</h1>", name=name)
```

**Why safer:** The template engine applies context-appropriate escaping for normal variable interpolation. Avoid marking untrusted values as safe HTML.

## 3. Command injection

### Vulnerable pattern

```python
import os

def list_files(directory):
    os.system("ls " + directory)
```

### Safer pattern

```python
import subprocess

def list_files(directory):
    subprocess.run(
        ["ls", "--", directory],
        check=True,
        shell=False,
        text=True,
        capture_output=True,
    )
```

**Why safer:** Passing an argument list with `shell=False` avoids constructing a shell command string. Validate the directory against the application's intended allowed locations as well.

## 4. Path traversal

### Vulnerable pattern

```python
from pathlib import Path

def read_document(filename):
    return Path("uploads/" + filename).read_text()
```

### Safer pattern

```python
from pathlib import Path

UPLOAD_DIR = Path("uploads").resolve()

def read_document(filename):
    candidate = (UPLOAD_DIR / filename).resolve()
    if candidate != UPLOAD_DIR and UPLOAD_DIR not in candidate.parents:
        raise ValueError("Invalid file path")
    if not candidate.is_file():
        raise FileNotFoundError(candidate)
    return candidate.read_text(encoding="utf-8")
```

**Why safer:** The resolved path is checked to ensure it remains inside the intended directory. Also enforce file type, ownership, and authorization requirements.

## 5. Hard-coded secret

### Vulnerable pattern

```python
API_TOKEN = "TRAINING_FAKE_TOKEN_DO_NOT_USE"
```

### Safer pattern

```python
import os

API_TOKEN = os.environ["API_TOKEN"]
```

**Note:** The example token is deliberately fake. Environment variables are one option for runtime configuration; use an approved secret manager or protected CI/CD variables for real credentials. Never commit real secrets.

## 6. Insecure deserialization

### Vulnerable pattern

```python
import pickle

def load_user_data(raw_data):
    return pickle.loads(raw_data)
```

### Safer pattern

```python
import json

def load_user_data(raw_data):
    value = json.loads(raw_data)
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object")
    return value
```

**Why safer:** JSON does not execute arbitrary Python object reconstruction in the way unsafe pickle deserialization can. Validate schema, types, size, and authorization after parsing.

## 7. Weak hash usage

### Vulnerable pattern

```python
import hashlib

def store_password(password):
    return hashlib.md5(password.encode()).hexdigest()
```

### Safer pattern

```python
from werkzeug.security import generate_password_hash, check_password_hash

def store_password(password):
    return generate_password_hash(password)

def verify_password(stored_hash, password):
    return check_password_hash(stored_hash, password)
```

**Why safer:** Passwords require a dedicated password-hashing function with salt and configurable work factor, not a fast general-purpose hash.

## 8. GitLab SAST template

```yaml
stages:
  - build
  - test

include:
  - template: Jobs/SAST.gitlab-ci.yml

build:
  stage: build
  image: alpine:3.20
  script:
    - echo "Build placeholder"
```

The SAST template adds analyzer jobs based on supported source files and template rules. Check the merged pipeline configuration to see which jobs are included.

## 9. Exclude training fixtures from SAST

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml

variables:
  SAST_EXCLUDED_PATHS: "spec,test,tests,tmp,training/fixtures"
```

Exclusions should be narrow, documented, and reviewed. This variable can override defaults, so include default exclusions when preserving them is required.

## 10. Override a SAST analyzer job

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml

semgrep-sast:
  variables:
    SECURE_LOG_LEVEL: "info"
```

Override only documented job properties and test changes in a merge request. Job names and analyzer behavior may change across template versions.

## 11. Pin an analyzer version

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml

semgrep-sast:
  variables:
    SAST_ANALYZER_IMAGE_TAG: "3.7"
```

The example pins a minor version for illustration. Use a currently supported version from GitLab's analyzer documentation and update it through a reviewed process.

## 12. SAST report artifact
GitLab analyzer jobs generate structured SAST JSON reports as job artifacts. Inspect the job's artifacts and validate the report schema before integrating it with external tooling.

A generic JSON file is not automatically a valid SAST report. Custom integrations must follow GitLab's documented SAST report schema and declare it using the correct `artifacts:reports:sast` configuration.
