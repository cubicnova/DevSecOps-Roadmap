# IAST Fundamentals

## Learning objectives

By completing this module, you should be able to:

- Explain Interactive Application Security Testing (IAST) and its place in DevSecOps.
- Compare IAST with SAST, DAST, RASP, and traditional runtime monitoring.
- Describe runtime instrumentation, sensors, sources, sinks, taint propagation, and execution traces.
- Understand agent deployment models and common runtime integrations.
- Plan IAST coverage using functional, integration, and API tests.
- Interpret IAST findings and assess their evidence, severity, and confidence.
- Integrate IAST into CI/CD and vulnerability management workflows.
- Identify performance, privacy, compatibility, and operational risks.

## 1. What is IAST?

Interactive Application Security Testing (IAST) analyzes an application while it is running and being exercised by tests or user interactions. An IAST sensor or agent is attached to the application runtime. It observes relevant operations and data flow, then reports security issues when tested code paths exhibit unsafe behavior.

IAST combines aspects of static and dynamic analysis:

- Like SAST, it can provide insight into application code and identify the source location of a problem.
- Like DAST, it observes a running application and real requests.
- Unlike a conventional black-box DAST scanner, it can often see internal execution context, method calls, and data flow.

IAST is not a guarantee that all vulnerabilities will be found. It generally reports only behavior reached during instrumented execution, and its coverage depends on the application, runtime, agent, rules, and test suite.

## 2. IAST in the application security testing landscape

| Method | Where it analyzes | Typical strength | Main limitation |
|---|---|---|---|
| SAST | Source code/build artifacts | Broad code coverage without running the app | May lack runtime reachability context |
| DAST | Running application from outside | Tests externally observable behavior | Limited internal code and data-flow visibility |
| IAST | Running application from inside | Runtime context and code-level evidence | Only observes instrumented and exercised paths |
| RASP | Running application | Runtime attack detection/blocking | Operational protection focus; not a complete SDLC testing strategy |
| SCA | Dependencies and packages | Known vulnerable components and license risk | Does not prove exploitability in application context |

Use complementary methods. IAST does not replace SAST, DAST, SCA, threat modeling, or manual security review.

## 3. How IAST works

A typical agent-based IAST workflow:

1. The agent is attached to a supported application runtime.
2. The application starts with instrumentation enabled.
3. Functional, integration, API, or manual tests exercise the application.
4. The agent observes selected framework and library operations.
5. It tracks untrusted data from sources through transformations.
6. It detects when that data reaches a potentially dangerous sink without adequate protection.
7. It records evidence such as request context, stack trace, source and sink, and code location.
8. Findings are sent to a local collector or vendor platform for triage.

The exact implementation varies by product and language. Some tools use bytecode instrumentation, runtime profilers, middleware, hooks, or a combination.

## 4. Core concepts

### Agent or sensor

A component loaded into or alongside the application to observe runtime behavior. It may instrument methods, framework hooks, database calls, file operations, or HTTP processing.

### Source

A point where untrusted or externally controlled data enters the application. Examples include:
- HTTP query and path parameters.
- Request body fields.
- Headers and cookies.
- Uploaded files.
- Message queues and external service responses.
- Environment variables or files, depending on the rule model.

### Sink

An operation where unsafe data can cause harm. Examples include:
- SQL query execution.
- OS command execution.
- File path or file write operations.
- HTML or JavaScript output.
- URL fetching or network access.
- XML parsing or deserialization.

### Taint propagation

Tracking how data from a source moves through variables, functions, and transformations toward a sink. A sanitizer or validator may change the analysis depending on the context and tool's rules.

### Execution trace

Evidence describing the runtime path, such as the source, call stack, sink, request, and relevant code location. It helps developers reproduce and fix the issue.

## 5. Example: source-to-sink flow

Consider an application that reads a request parameter and concatenates it into a SQL statement.

```python
def search_users(request, db):
    username = request.args.get("name")       # Source
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return db.execute(query)                  # Sink
```

An IAST sensor may observe request data flowing into the SQL execution operation. A safe implementation uses parameterized queries:

```python
def search_users(request, db):
    username = request.args.get("name")
    return db.execute(
        "SELECT * FROM users WHERE name = ?",
        (username,)
    )
```

This is a simplified illustration. Actual detection depends on the language, framework, database driver, agent instrumentation, and configured rules.

## 6. Instrumentation models

Common approaches include:

- JVM agents attached using `-javaagent`.
- .NET profilers and runtime instrumentation.
- Node.js hooks or module instrumentation.
- Python middleware, tracing, or runtime hooks.
- Language-specific sensors and framework integrations.
- Proxy-assisted or hybrid models in some products.

Support differs substantially between vendors. Validate the exact runtime version, framework, application server, container base image, and dependency set before selecting an IAST tool.

## 7. Typical deployment workflow

For a Java application, a vendor agent may be attached at startup:

```bash
java -javaagent:/opt/iast/agent.jar \
  -jar application.jar
```

For a .NET service, a vendor may use CLR profiler environment variables. For Node.js or Python, setup may involve an agent package, preload hook, middleware, or framework integration.

Always follow the vendor's current installation guide. Do not invent or reuse environment variable names from another product. Keep license keys and API credentials in a secret manager.

## 8. IAST test coverage

IAST only observes code paths that execute while the agent is active. Test quality is therefore central to IAST effectiveness.

Improve coverage by exercising:
- Authenticated and unauthenticated routes.
- Different user roles and tenants.
- Positive and negative input cases.
- Error and exception paths.
- API endpoints and background jobs.
- File upload and download workflows.
- Database and external-service integrations.
- Administrative and sensitive business workflows.

A low finding count may mean the application is secure, but it may also mean the test suite did not exercise important code. Measure coverage and test completeness separately from vulnerability count.

## 9. Findings and triage

An IAST finding may include:
- Vulnerability type and rule.
- Severity and confidence.
- Application, environment, and endpoint.
- Source and sink details.
- Stack trace and file/line location.
- Request or transaction context.
- Remediation guidance.

Triage should confirm:
1. The finding came from the expected application and build.
2. The trace shows a real executed path.
3. The source is attacker- or user-controllable as described.
4. The sink operation and security impact are understood.
5. The proposed mitigation fits the actual code path.
6. Evidence does not contain secrets or sensitive personal data.

Do not assume every IAST alert is automatically exploitable. Runtime context improves accuracy but does not eliminate the need for validation.

## 10. IAST in CI/CD

A common workflow:

```text
Build application
      |
Deploy to isolated test environment with IAST agent
      |
Run functional / integration / API tests
      |
Collect IAST findings and coverage data
      |
Normalize, triage, and apply security policy
      |
Store reports / create issues
      |
Promote or block release
```

Recommended practices:
- Instrument ephemeral or staging environments first.
- Pin and update agent versions through a controlled process.
- Use CI-managed secrets.
- Preserve test and agent logs securely.
- Distinguish agent startup failures from zero findings.
- Define quality gates based on confirmed findings and risk.
- Retain enough metadata to map a finding to the exact commit and build.
- Run complementary SAST and DAST checks.

## 11. Performance and operational considerations

Instrumentation can add CPU, memory, startup, and request latency overhead. Measure the impact with representative tests. Start with a non-production environment and a small application subset.

Consider:
- Runtime and framework compatibility.
- Container and Kubernetes deployment behavior.
- Agent startup and shutdown lifecycle.
- Threading and asynchronous execution.
- Sampling or rule configuration.
- Network connectivity to the collector.
- Agent updates and rollback.
- Performance thresholds and safe failure behavior.

Do not silently disable the agent when it fails to initialize if the pipeline expects IAST coverage. Mark the run inconclusive or failed.

## 12. Privacy and data protection

IAST traces may capture request metadata, payload fragments, stack traces, database statements, identifiers, or other sensitive values.

Controls should include:
- Redaction and masking of credentials, tokens, and personal data.
- Least-privilege access to the IAST console.
- Encryption in transit and at rest.
- Retention limits for traces and reports.
- Secure handling of agent configuration and API keys.
- Review of vendor data residency and processing terms.
- No production customer data in training labs.

## 13. Common limitations

- Untested paths remain unobserved.
- Agent compatibility varies by language and framework.
- Instrumentation can affect performance.
- Some native, asynchronous, or third-party code may not be fully visible.
- A finding may require manual validation and business context.
- Agent and collector connectivity can fail.
- Proprietary platforms may have licensing and data-handling constraints.

## 14. IAST maturity progression

| Level | Capability |
|---|---|
| 0 — Initial | No IAST agent or runtime security analysis |
| 1 — Basic | Agent used manually during selected tests |
| 2 — Integrated | Agent starts automatically in CI and reports build status |
| 3 — Managed | Findings flow into a central issue tracker and effectiveness is reviewed |
| 4 — Optimized | Coverage, performance, deduplication, and remediation metrics are continuously improved |

## 15. Useful metrics

- Percentage of relevant test runs with the agent active.
- Application and runtime compatibility coverage.
- Endpoint and code-path coverage during instrumented tests.
- Confirmed findings by severity and release.
- Mean time to triage and remediate.
- Agent startup success rate.
- Runtime overhead against an agreed baseline.
- Percentage of findings linked to tickets and retested.

Do not use a low alert count as a standalone security KPI.

## 16. Knowledge check

1. What does IAST observe while an application runs?
2. How does IAST differ from DAST?
3. Define source, sink, and taint propagation.
4. Why does IAST depend on functional test coverage?
5. What is the purpose of an execution trace?
6. Why should the agent be tested for runtime compatibility?
7. What operational risks can instrumentation introduce?
8. Why must secrets be redacted from traces?
9. What is the difference between IAST and RASP?
10. Why should IAST complement rather than replace SAST and DAST?

## References

- [OWASP DevSecOps Guideline — IAST](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-1-Interactive-Application-Security-Testing/)
- [OWASP DevSecOps Verification Standard — TEST-003 IAST](https://owasp.github.io/www-project-devsecops-verification-standard/document/TEST-003-Interactive-Application-Security-Testing-IAST.html)
- [AWS DevOps Guidance — Interactive Application Security Testing](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/qa.st.8-improve-security-testing-accuracy-using-interactive-application-security-testing.html)
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
