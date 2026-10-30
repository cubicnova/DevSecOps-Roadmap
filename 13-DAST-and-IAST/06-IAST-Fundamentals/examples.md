# IAST Fundamentals — Examples

These examples explain IAST concepts and show generic runtime integration patterns. They are not installation instructions for a particular vendor. Always use the current vendor documentation for exact agent options and configuration keys.

## 1. Source-to-sink example: SQL injection risk

Unsafe Python illustration:

```python
def get_account(request, database):
    account_id = request.args.get("id")       # Source
    sql = "SELECT * FROM accounts WHERE id=" + account_id
    return database.execute(sql)              # Sink
```

An IAST sensor may observe request-controlled data flowing into a SQL execution call.

Safer parameterized version:

```python
def get_account(request, database):
    account_id = request.args.get("id")
    return database.execute(
        "SELECT * FROM accounts WHERE id = ?",
        (account_id,)
    )
```

The parameterized query separates data from SQL syntax. Confirm that the driver uses parameter binding correctly.

## 2. Source-to-sink example: command execution

Unsafe pattern:

```python
import subprocess

def lookup_host(request):
    hostname = request.args.get("host")       # Source
    return subprocess.check_output(
        "nslookup " + hostname,
        shell=True                             # Dangerous sink
    )
```

Safer design: avoid shell parsing and validate the hostname according to the application's business rules.

```python
import subprocess

def lookup_host(hostname):
    # Apply strict allowlist validation before this function.
    return subprocess.run(
        ["nslookup", hostname],
        check=True,
        capture_output=True,
        text=True,
        shell=False
    )
```

A tool's taint rules determine which transformations or validations it recognizes. A syntactic change alone does not prove all command-injection risks are removed.

## 3. Source-to-sink example: path traversal

Unsafe pattern:

```python
from pathlib import Path

def read_document(request):
    filename = request.args.get("file")      # Source
    return Path("/srv/docs/" + filename).read_text()
```

Safer design: map a server-side identifier to an approved file rather than accepting an arbitrary path. If paths must be accepted, canonicalize and verify that the resolved path remains under the permitted directory.

## 4. Source-to-sink example: reflected output

Unsafe pattern:

```python
from flask import request

def greeting():
    name = request.args.get("name")          # Source
    return "<h1>Hello " + name + "</h1>"      # HTML output sink
```

Safer design: use a template engine with contextual output encoding enabled, and avoid marking untrusted input as safe HTML.

## 5. Generic Java agent startup pattern

A JVM IAST agent is commonly attached with the Java agent mechanism:

```bash
java \
  -javaagent:/opt/iast/agent.jar \
  -jar target/application.jar
```

The agent path and any additional options are vendor-specific. Confirm compatibility with the Java version and application server.

## 6. Generic .NET profiler deployment pattern

Some .NET IAST products use CLR profiling environment variables to load an instrumentation component. A generic deployment checklist:

```text
1. Install the vendor-supported agent package.
2. Configure the profiler identifier and agent path using vendor instructions.
3. Set the application/service identity and collector endpoint.
4. Inject credentials from a secret manager.
5. Start the service in a test environment.
6. Confirm agent initialization in sanitized logs.
7. Run the automated test suite.
8. Review findings and runtime metrics.
```

Do not copy profiler GUIDs or environment variable values from an unrelated product.

## 7. Generic Node.js integration pattern

Depending on the product, a Node.js agent may be loaded before application modules using a preload mechanism:

```bash
NODE_OPTIONS="--require /opt/iast/agent-bootstrap.js" \
  node server.js
```

This is illustrative only. Confirm the vendor's documented bootstrap package, Node.js version support, and required configuration.

## 8. Generic Python middleware or agent pattern

Some Python IAST integrations use an agent package, framework middleware, or startup wrapper. The exact installation and launch syntax is product-specific.

A safe evaluation sequence:

```text
1. Create an isolated virtual environment.
2. Install the vendor-supported agent version.
3. Configure collector URL and application identity.
4. Inject API keys using environment secrets.
5. Start the application under instrumentation.
6. Send test requests.
7. Confirm the expected request and trace appear.
8. Compare response time and resource use with an uninstrumented run.
```

## 9. CI pipeline lifecycle example

```yaml
name: Instrumented Integration Tests

on:
  pull_request:

permissions:
  contents: read

jobs:
  iast-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build application
        run: ./mvnw -B package

      # Replace with your approved agent setup and secure secret injection.
      - name: Start instrumented test application
        run: |
          echo "Configure the vendor IAST agent here"
          echo "Start the application with instrumentation enabled"

      - name: Run integration tests
        run: ./mvnw -B verify

      - name: Collect IAST results
        if: always()
        run: |
          echo "Export results using the vendor-supported API or CLI"

      - name: Upload sanitized reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: iast-test-results
          path: reports/
          if-no-files-found: warn
```

This is a lifecycle template, not a working vendor integration. Add actual agent installation, startup, test execution, export, and quality-gate commands for the selected product. Pin actions to reviewed full commit SHAs in production.

## 10. Example finding record

```yaml
id: IAST-TRAIN-001
title: Untrusted request data reaches SQL execution
application: training-api
environment: isolated-test
severity: high
confidence: high
source:
  type: HTTP query parameter
  endpoint: /api/search
sink:
  type: SQL execution
  component: database-driver
location:
  file: src/search.py
  line: 24
evidence:
  trace_id: redacted-training-trace
status: needs-review
```

This is a training record format, not a standard IAST export schema. Do not include real credentials, personal data, or raw production request bodies.

## 11. Coverage comparison example

| Test suite | Routes exercised | IAST findings | Interpretation |
|---|---:|---:|---|
| Unit tests only | 2 | 0 | May not exercise HTTP/runtime integration |
| API integration tests | 12 | 2 | More request paths were executed |
| End-to-end tests | 18 | 3 | Broader workflow coverage |
| Full regression | 25 | 3 | More coverage, not proof of complete security |

A higher finding count may result from greater coverage rather than a less secure build. Track coverage and findings separately.

## 12. IAST vs. DAST example

A DAST scanner may report that a request to an endpoint produces a suspicious response. An IAST agent may add evidence that the request parameter reached a particular SQL execution call and identify the relevant code location.

Neither result alone replaces developer review, threat modeling, or a test of the complete business impact.

## 13. Example sanitized metrics

```json
{
  "application": "training-api",
  "build": "example-commit-123",
  "agent_status": "active",
  "instrumented_test_runs": 1,
  "requests_observed": 145,
  "routes_exercised": 18,
  "findings": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 1
  },
  "runtime_overhead_percent": 4.2
}
```

Values are illustrative. Establish a repeatable baseline before comparing performance overhead or coverage.

## 14. Secure agent configuration checklist

- Keep API keys and license values out of source control.
- Use a dedicated low-privilege agent identity.
- Restrict collector network access.
- Use TLS for agent-to-platform communication.
- Redact request data and secrets.
- Pin and periodically update agent versions.
- Test startup and shutdown behavior.
- Measure performance overhead.
- Define retention and access policies for traces.
