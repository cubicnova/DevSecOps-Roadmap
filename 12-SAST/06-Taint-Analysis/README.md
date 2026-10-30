# Taint Analysis — Data-Flow Security Testing

Taint analysis is a program-analysis technique that tracks data from an origin to a security-sensitive operation. It is especially useful for finding injection flaws and sensitive-data leaks where untrusted input reaches a dangerous sink without an appropriate control.

This module covers the fundamentals, sources and sinks, taint propagation, sanitizers, static and dynamic analysis, vulnerability patterns, custom Semgrep rules, CodeQL concepts, practical exercises, and CI/CD integration.

## Learning objectives

By completing this module, you should be able to:

- Explain taint analysis and its relationship to static data-flow analysis.
- Identify sources, sinks, propagators, sanitizers, and validators.
- Trace data across variables, functions, and application layers.
- Recognize SQL injection, command injection, XSS, path traversal, SSRF, and data-leak flows.
- Distinguish validation, encoding, parameterization, and sanitization.
- Understand context-sensitive and context-insensitive analysis.
- Write and test basic Semgrep taint-mode rules.
- Understand CodeQL source, sink, and taint-tracking concepts.
- Triage findings and reduce false positives without hiding real issues.
- Integrate taint-focused checks into a secure development pipeline.

## 1. What is taint analysis?

Taint analysis marks data from an untrusted or sensitive origin and follows it as the program transforms, stores, and passes that data. A finding is produced when the data reaches a sensitive operation in a way that violates the security policy.

A common model is:

```text
Untrusted input
     |
     v
  SOURCE
     |
     v
Propagation through variables / functions
     |
     v
  SANITIZER or VALIDATOR
     |
     v
   SINK
```

The absence of an appropriate control between source and sink may indicate a vulnerability. Whether a sanitizer is appropriate depends on the sink and context: HTML escaping does not make a value safe for a SQL query, and SQL parameterization does not make a value safe for a shell command.

## 2. Core terminology

| Term | Meaning | Example |
|---|---|---|
| Source | Where untrusted or sensitive data enters | HTTP query parameter |
| Tainted value | Data currently marked as untrusted/sensitive | `username` from request |
| Propagator | Moves taint to another value | Assignment, concatenation, function return |
| Sink | Security-sensitive operation | SQL execution, shell command |
| Sanitizer | Context-appropriate transformation recognized by the analysis | HTML escaping for HTML text |
| Validator | Checks data against an allowed format or set | Numeric range or allowlist check |
| Sanitization model | Tool configuration describing safe transformations | Framework-specific sanitizer |
| Flow | Path from source to sink | Request parameter → helper → SQL API |

A sanitizer is not a universal “make safe” operation. It must be appropriate for the exact output context and correctly modeled by the analysis tool.

## 3. Vulnerability classes detected through taint flows

### SQL injection

```text
HTTP parameter → string concatenation → SQL execution
```

Preferred defense: parameterized queries with bound values. Do not attempt to secure SQL by HTML-escaping or generic string replacement.

### Command injection

```text
HTTP parameter → command construction → shell execution
```

Preferred defense: avoid invoking a shell; use fixed executable paths and argument arrays, and validate arguments against strict allowlists.

### Cross-site scripting (XSS)

```text
Request parameter → template or DOM update → browser HTML interpretation
```

Preferred defense: context-aware output encoding, safe DOM APIs, and a vetted HTML sanitizer when rich HTML is required.

### Path traversal

```text
User-supplied file name → path construction → file read/write
```

Preferred defense: map user choices to server-side identifiers or enforce canonicalized paths within an allowed base directory. Avoid relying only on string checks for `../`.

### Server-side request forgery (SSRF)

```text
User-supplied URL → HTTP client → outbound request
```

Preferred defense: allowlist destinations, restrict network egress, validate DNS/IP resolution and redirects, and block access to sensitive internal address ranges.

### Sensitive data leakage

```text
Secret or personal data → logging / analytics / external transmission
```

Here the source may be sensitive data rather than untrusted input. The sink is a location where the data should not be disclosed.

## 4. Taint analysis approaches

### Static taint analysis

Examines source code, bytecode, or another program representation without running the application. It can explore paths that were not exercised in tests, but it must approximate runtime behavior.

### Dynamic taint analysis

Tracks taint while the application executes. It can provide runtime evidence for exercised paths, but it cannot report paths that were never triggered in the observed tests.

### Interactive Application Security Testing (IAST)

Combines runtime instrumentation with taint tracking during tests or application use. It can report observed source-to-sink paths and stack traces, depending on the agent and platform.

### Pattern matching versus data-flow analysis

Pattern matching detects a code shape, such as `eval(x)`. Taint analysis asks whether attacker-controlled data can flow into `eval`. Data-flow analysis can reduce noise, but its results depend on the accuracy and coverage of sources, sinks, propagators, sanitizers, framework models, and call graphs.

## 5. Data-flow concepts

### Direct flow

```python
user_input = request.args.get("name")  # source
query = user_input                     # propagation
cursor.execute(query)                  # sink
```

### Flow through a helper function

```python
def build_query(value):
    return "SELECT * FROM users WHERE name = '" + value + "'"

def handler(request, cursor):
    name = request.args.get("name")
    query = build_query(name)
    cursor.execute(query)
```

An analyzer needs to follow the value through the helper function to identify the path.

### Control flow and data flow

- **Control flow** describes which statements may execute and in what order.
- **Data flow** describes how values are defined, transformed, and used.
- **Interprocedural analysis** follows values across function boundaries.
- **Intraprocedural analysis** stays within a function or procedure.
- **Path sensitivity** distinguishes values or conditions on different execution paths.
- **Context sensitivity** distinguishes calls to the same function from different callers.

These capabilities vary substantially between tools and configurations.

## 6. Sanitization and validation

Choose controls based on the sink:

| Sink/context | Preferred control |
|---|---|
| SQL query values | Parameterized queries |
| HTML text | Context-aware HTML output encoding |
| JavaScript string context | Context-specific encoding; avoid unsafe inline script construction |
| Shell command | Avoid shell; fixed executable plus argument array and allowlist |
| File path | Server-side mapping or canonicalized containment check |
| URL fetch | Destination allowlist and network egress restrictions |
| Log output | Structured logging and sensitive-data redaction |

Validation checks whether input is acceptable. Encoding changes representation for a specific output context. Parameterization separates SQL code from data. These controls are related but not interchangeable.

## 7. Semgrep taint mode

Semgrep rules can describe sources and sinks using taint mode. The basic structure is:

```yaml
rules:
  - id: example-taint-flow
    mode: taint
    languages: [python]
    message: Untrusted data may reach a sensitive operation.
    severity: ERROR
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: cursor.execute($QUERY)
```

This is a teaching example. Real rules should define framework-accurate sources, sinks, sanitizers, propagators, and safe query patterns. Confirm the syntax and capabilities of the Semgrep engine/version used by your team.

## 8. CodeQL taint-tracking concepts

CodeQL models data flow through source and sink definitions and taint-tracking configurations. A query identifies paths between a source and a sink, optionally accounting for sanitizers and additional flow steps.

Conceptual components:
- Source: a user-controlled input API.
- Sink: a security-sensitive API.
- Taint tracking configuration: defines how to find relevant flows.
- Path query: displays the flow path to support review.

CodeQL libraries and query APIs are language-specific. Use the official query help and language library documentation rather than copying a query between languages.

## 9. Triage workflow

For each reported flow:
1. Identify the source and whether an attacker can control it.
2. Follow every propagation step to the sink.
3. Confirm that the sink is security-sensitive in this context.
4. Check whether a suitable sanitizer, validator, parameterization, or allowlist is applied.
5. Verify that the tool understands the control correctly.
6. Assess reachability, authorization, and deployment context.
7. Fix the root cause and add a regression test.
8. Record any accepted exception with an owner and review date.

Do not mark a finding safe merely because a variable name suggests validation. Inspect the actual validation behavior.

## 10. Limitations

Taint analysis can produce false positives when it misses a sanitizer or cannot understand a framework. It can produce false negatives when sources, sinks, propagation paths, reflection, generated code, dynamic behavior, or external libraries are not modeled.

Static analysis also cannot always determine runtime configuration, deployment topology, authorization state, or whether a path is practically exploitable. Validate important findings with code review and appropriate testing.

## 11. Suggested lab structure

```text
06-Taint-Analysis/
├── README.md
├── examples.md
├── practical.md
├── solutions.md
├── samples/
│   ├── vulnerable/
│   └── fixed/
└── rules/
    └── python-taint.yml
```

## 12. Further reading

- [OWASP Static Application Security Testing](https://devguide.owasp.org/en/05-implementation/05-static-analysis/)
- [OWASP Static Code Analysis](https://community.owasp.org/controls/Static_Code_Analysis)
- [OWASP DevSecOps SAST guidance](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-3-Build/2-3-1-Static-Analysis/2-3-1-1-Static-Application-Security-Testing/)
- [Semgrep rule syntax](https://semgrep.dev/docs/writing-rules/overview/)
- [CodeQL documentation](https://codeql.github.com/docs/)
- [OWASP Mobile Application Security — Taint Analysis](https://mas.owasp.org/MASTG/techniques/android/MASTG-TECH-0108/)

Use these techniques only on applications and repositories you own or are authorized to assess.
