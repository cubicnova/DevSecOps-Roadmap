# Custom Security Rules — Examples

Examples demonstrate how to define and implement custom security checks. The CodeQL query snippets are teaching patterns; verify APIs against the CodeQL version and language libraries used by your project.

## 1. Rule specification example

**Rule ID:** `PY-CUST-001`

**Title:** Prohibit legacy HTTP client

**Objective:** Ensure application code uses the organization's approved HTTP client with configured TLS and timeout behavior.

**Detection:** Identify calls to the prohibited client API.

**Severity:** Medium

**Confidence:** High only after semantic call-target matching and test coverage.

**Remediation:** Use the approved client wrapper.

## 2. CodeQL teaching query: prohibited API call

```ql
/**
 * @name Review calls to a prohibited API
 * @description Flags calls to an API that requires security review.
 * @kind problem
 * @id py/prohibited-api-review
 * @problem.severity warning
 * @security-severity 5.0
 * @precision medium
 * @tags security
 */

import python

from Call call
where call.getFunc().toString() = "legacy_request"
select call, "Review this call and use the approved secure client."
```

The `toString()` comparison is deliberately simple for teaching. It may miss aliases and may match unrelated names. Replace it with a semantic API identification strategy for production use.

## 3. Vulnerable and approved HTTP client patterns

Potentially prohibited pattern:

```python
import requests

def get_profile(url):
    return requests.get(url)
```

Approved wrapper example:

```python
from company_security.http import secure_get

def get_profile(url):
    return secure_get(url, timeout=5)
```

A real rule should distinguish the exact prohibited call from the approved wrapper, including import aliases and qualified names.

## 4. Weak hash usage rule concept

Policy: password storage must use an approved password-hashing function.

Potentially unsafe:

```python
import hashlib

def store_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

Preferred direction:

```python
from werkzeug.security import generate_password_hash

def store_password(password):
    return generate_password_hash(password)
```

A production detector should identify password-storage context and approved password-hashing APIs. A generic search for `sha256` is too broad because SHA-256 is appropriate for many non-password uses.

## 5. Insecure TLS verification rule concept

Potentially unsafe:

```python
import requests

response = requests.get(
    "https://service.example",
    verify=False
)
```

Safer direction:

```python
response = requests.get(
    "https://service.example",
    timeout=5
)
```

Use the default certificate verification or a correctly configured trust store. A production rule should inspect the relevant call argument and account for wrapper APIs.

## 6. Dangerous deserialization rule concept

Potentially unsafe:

```python
import pickle

def load_user_data(blob):
    return pickle.loads(blob)
```

Safer direction: use a data format with a constrained schema, such as JSON, when the data model permits it.

```python
import json

def load_user_data(blob):
    return json.loads(blob)
```

JSON parsing alone does not validate business rules; validate the resulting structure and types.

## 7. Rule pack layout

```text
custom-security-rules/
├── qlpack.yml
├── queries/
│   └── python/
│       ├── ProhibitedApi.ql
│       └── ProhibitedApi.md
└── tests/
    └── python/
        ├── ProhibitedApi.ql
        ├── ProhibitedApi.expected
        └── test.py
```

`qlpack.yml`:

```yaml
name: cubicnova/custom-security-rules
version: 1.0.0
dependencies:
  codeql/python-all: "*"
```

## 8. Query help Markdown example

Save beside `ProhibitedApi.ql` as `ProhibitedApi.md`:

```markdown
# Prohibited API call

This query identifies calls to an API that is not approved for application use.

## Recommendation

Use the centrally maintained secure client wrapper. Confirm that TLS
verification, timeouts, redirect behavior, and error handling are configured.
```

## 9. CLI workflow

From the query pack directory:

```bash
codeql pack install
codeql pack compile .
```

Run a custom pack against a database:

```bash
codeql database analyze ../db-python \
  . \
  --format=sarif-latest \
  --output=custom-security-results.sarif \
  --sarif-add-query-help
```

Use a database built for the same language and compatible query libraries. Confirm the installed CLI supports the selected options.

## 10. Rule test design

| Test case | Expected |
|---|---|
| Direct prohibited API call | Alert |
| Approved secure wrapper | No alert |
| Alias import of prohibited API | Alert if semantically equivalent |
| Unrelated function with same short name | No alert |
| Safe call with required timeout | No alert if policy requires timeout |
| Missing timeout | Alert if within the rule's defined scope |

## 11. CI policy example

A simple conceptual pipeline step:

```yaml
- name: Run custom CodeQL rules
  run: |
    codeql database analyze db-python \
      ./custom-security-rules \
      --format=sarif-latest \
      --output=custom-security-results.sarif
```

In a real workflow, create the database first, install the correct CLI and packs, upload SARIF using the supported integration, and set appropriate permissions.

## 12. Exception record example

```yaml
rule_id: PY-CUST-001
path: src/legacy/integration.py
owner: application-team
reason: "Temporary compatibility with a vendor SDK"
compensating_control: "Outbound destination allowlist and monitored egress"
approved_by: security-team
expires_on: 2026-12-31
```

This is an illustrative internal record format, not a CodeQL suppression file. Store approvals in the organization's designated risk or exception system.
