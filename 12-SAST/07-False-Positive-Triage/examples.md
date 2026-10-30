# False Positive Triage — Examples

## 1. SQL injection: likely true positive

Vulnerable code:

```python
def get_user(cursor, username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
```

Triage:

- Source: `username`, potentially supplied by a request.
- Sink: SQL execution.
- Control: no parameterization is visible.
- Classification: likely true positive if the value is attacker-controlled and the code is reachable.
- Action: use a parameterized query and add a regression test.

Safer version:

```python
def get_user(cursor, username):
    cursor.execute(
        "SELECT * FROM users WHERE name = ?",
        (username,)
    )
```

## 2. SQL injection: finding may be a false positive

```python
def get_user(cursor, username):
    cursor.execute(
        "SELECT * FROM users WHERE name = ?",
        (username,)
    )
```

If a rule reports this as SQL injection, inspect whether it recognizes the database API's parameter binding. Confirm the driver and API semantics. If parameterization is effective, document the evidence and consider improving the query model.

Do not assume every API that accepts a second argument binds values safely; verify the specific library.

## 3. XSS: context-specific encoding

Potentially unsafe:

```python
return "<h1>" + user_input + "</h1>"
```

Potentially safe for HTML text context:

```python
from markupsafe import escape

return "<h1>" + escape(user_input) + "</h1>"
```

Triage should verify that the output is truly an HTML text context and that the escaping library is used correctly. HTML escaping is not a universal defense for JavaScript, CSS, URL, or attribute contexts.

## 4. Command injection: inspect the actual API

Potentially unsafe:

```python
import os

def run_task(value):
    os.system("tool " + value)
```

Safer direction:

```python
import subprocess

def run_task(validated_value):
    subprocess.run(
        ["tool", validated_value],
        shell=False,
        check=True
    )
```

Triage must still inspect argument validation and the behavior of `tool`. `shell=False` prevents shell parsing but does not make every argument safe.

## 5. Custom sanitizer not recognized

```python
def normalize_identifier(value):
    if not value.isalnum():
        raise ValueError("Invalid identifier")
    return value

def lookup_user(db, user_id):
    safe_id = normalize_identifier(user_id)
    return db.execute(
        "SELECT * FROM users WHERE id = ?",
        (safe_id,)
    )
```

A query may not understand `normalize_identifier`. Inspect the helper implementation, all call paths, and the actual sink. Here parameter binding is the primary SQL control; the allowlist adds input constraints. If a custom model is needed, add it only after verifying semantics and testing both safe and unsafe cases.

## 6. Test-only code

```python
def test_sql_builder():
    # Test fixture uses a deliberately unsafe string to verify rejection.
    return "SELECT * FROM users WHERE name = '" + "sample" + "'"
```

A finding in a test fixture may have lower practical exposure, but it is not automatically a false positive. Determine whether test code is shipped, executed in production, or copied into application code. Use a test-code classification or scoped exclusion only when policy permits and the rationale is documented.

## 7. Generated code

A finding in generated code may be caused by a template or generator. Trace the generated file back to its source template. Fix the template when possible; excluding the generated output alone may leave the root cause intact.

## 8. Example triage record

```yaml
alert_id: "example-alert-123"
rule_id: "python/sql-injection"
location: "app/repository.py:42"
classification: "false-positive"
reason: "The query uses the database driver's parameter-binding API."
evidence:
  - "The SQL statement contains a placeholder."
  - "The untrusted value is supplied as a separate bound parameter."
  - "A regression test verifies special characters are treated as data."
reviewer: "AppSec reviewer"
review_date: "2026-10-30"
follow_up: "Add a regression test to the custom query model."
```

This is an illustrative internal record, not a GitHub API payload.

## 9. Accepted risk is not a false positive

```yaml
alert_id: "example-alert-456"
rule_id: "python/unsafe-operation"
classification: "accepted-risk"
reason: "The issue is real but temporarily required for vendor compatibility."
owner: "Application team"
compensating_controls:
  - "Restricted network egress"
  - "Input allowlist"
approved_by: "Security risk owner"
expires_on: "2026-12-31"
```

A real vulnerability remains a real vulnerability even when an authorized owner accepts the risk.

## 10. CodeQL precision metadata

Illustrative metadata:

```ql
/**
 * @name Example security query
 * @description Identifies a security-sensitive pattern.
 * @kind problem
 * @id py/example-security-pattern
 * @problem.severity warning
 * @security-severity 5.0
 * @precision medium
 * @tags security
 */
```

`@precision` is a query-level estimate based on the observed proportion of true-positive results and their relevance. It is not a per-alert confidence score. Set it using representative testing and follow the current CodeQL metadata guidance.

## 11. Suggested triage checklist

```text
[ ] Read the rule description and query help
[ ] Confirm exact file, line, and branch
[ ] Identify source and sink
[ ] Trace transformations and controls
[ ] Verify sanitizer/API semantics
[ ] Check reachability and attacker control
[ ] Assess impact and exploitability
[ ] Classify with evidence
[ ] Fix, dismiss, escalate, or document risk
[ ] Add regression test or rule improvement
```
