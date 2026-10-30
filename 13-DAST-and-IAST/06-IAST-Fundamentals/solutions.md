# IAST Fundamentals — Solutions and Reference Answers

These are reference answers. Exact agent installation commands, configuration keys, supported runtimes, and report formats vary by vendor. Use the selected product's current documentation rather than copying settings from another agent.

## Solution 1 — SAST, DAST, and IAST

| Method | Example SQL injection detection |
|---|---|
| SAST | Finds risky query construction in source code, even if the path is not executed |
| DAST | Sends crafted input to a running endpoint and observes externally visible behavior |
| IAST | Observes request data flowing through the running code to a database execution sink |

Each method has blind spots. Use them together and validate findings in application context.

## Solution 2 — Sources and sinks

Example source list:
- HTTP query parameter.
- JSON request field.
- Cookie or header.
- Uploaded file content.
- Message queue payload.

Example sink list:
- SQL execution API.
- Shell/process execution.
- File read/write.
- HTML/JavaScript response output.
- Server-side URL fetch.

A source or sink is contextual. A tool's rule pack determines which APIs and framework hooks it recognizes.

## Solution 3 — Data-flow trace

A typical trace might look like:

```text
HTTP request
   |
   v
Query parameter parsed
   |
   v
Application controller
   |
   v
Service method
   |
   v
String concatenation
   |
   v
SQL execution sink
```

A remediation should address the dangerous operation. For SQL, use parameterized queries and safe database APIs. For output encoding, use contextual encoding appropriate to the output context. For file access, map identifiers to approved resources or enforce canonical path containment.

## Solution 4 — Java instrumentation

A generic JVM launch pattern:

```bash
java -javaagent:/opt/iast/agent.jar \
  -jar target/application.jar
```

The actual agent download, configuration file, collector endpoint, authentication values, and compatibility requirements are vendor-specific. Confirm:
- Java version support.
- Application server/framework support.
- Agent startup logs.
- Collector connectivity.
- Test traffic visibility.
- Findings mapped to the correct build.

Never place license keys or API secrets in a committed script.

## Solution 5 — .NET instrumentation

Some products use CLR profiler variables and a native profiler library. The correct profiler identifier and variable names are product-specific. Follow the vendor's setup guide and validate the agent with a minimal test service before enabling it in a larger environment.

## Solution 6 — Node.js or Python instrumentation

Possible integration styles include preload hooks, framework middleware, runtime packages, or wrappers. A successful process start does not necessarily prove that security instrumentation is active. Confirm that the agent reports initialization and observes requests or transactions.

Record any unsupported runtime, framework, native extension, asynchronous path, or library limitation.

## Solution 7 — Test coverage

Build a route matrix:

| Route | Anonymous | Basic user | Admin | Error path |
|---|---:|---:|---:|---:|
| `GET /health` | Yes | Yes | Yes | N/A |
| `GET /profile` | Denied | Yes | Yes | Yes |
| `POST /orders` | Denied | Yes | Yes | Yes |
| `GET /admin/audit` | Denied | Denied | Yes | Yes |

The values are illustrative. Replace them with the application's actual access policy. A route is covered only if the relevant request and code path execute while instrumentation is active.

## Solution 8 — Finding analysis

Use this triage sequence:

1. Verify application, environment, commit, and build.
2. Confirm the agent was active during the request.
3. Inspect the source, transformations, and sink.
4. Determine whether the source is attacker-controlled.
5. Confirm whether the sink operation is dangerous in context.
6. Review existing validation, encoding, parameterization, or access controls.
7. Reproduce in a safe test environment.
8. Record a confirmed, false-positive, accepted-risk, or needs-investigation status.

IAST can provide strong runtime evidence, but it does not automatically establish business impact or exploitability in every deployment context.

## Solution 9 — Performance overhead

Use the same workload and environment for both runs. Example table:

| Metric | Agent off | Agent on | Difference |
|---|---:|---:|---:|
| Startup time | Record | Record | Calculate |
| Median latency | Record | Record | Calculate |
| CPU average | Record | Record | Calculate |
| Memory peak | Record | Record | Calculate |

Calculate percentage change as:

```text
((instrumented_value - baseline_value) / baseline_value) * 100
```

Repeat measurements and compare with agreed thresholds. Do not treat one run as a reliable performance benchmark.

## Solution 10 — Privacy and hardening

Recommended controls:
- Redact authorization headers, cookies, passwords, and sensitive request fields.
- Restrict access to traces and dashboards.
- Use TLS and authenticated agent-to-collector communication.
- Keep API keys in a secret manager.
- Apply retention and deletion policies.
- Review vendor data processing and residency.
- Use least-privilege agent identities.
- Document rollback and agent disablement.

## Solution 11 — CI/CD integration

A generic pipeline should implement these stages:

```text
Build
  |
Start test application with agent
  |
Verify agent initialized
  |
Run integration/API tests
  |
Export findings
  |
Sanitize and retain reports
  |
Apply quality gate
  |
Cleanup
```

The build should be marked failed or inconclusive if:
- The application does not start.
- The agent fails to initialize.
- The test suite fails unexpectedly.
- Findings cannot be exported when export is mandatory.
- The security policy is violated.

Do not equate “no findings” with “agent was active and coverage was adequate.”

## Solution 12 — Correlation example

| Observation | SAST | DAST | IAST |
|---|---|---|---|
| Risky SQL construction in an unexecuted function | May detect | Usually not observed | Not observed |
| Runtime request reaches SQL sink | May detect code pattern | May show external behavior | Can show runtime flow |
| Missing response security header | Limited | Can observe | May observe response behavior depending on tool |
| Vulnerable dependency version | SCA is primary | May reveal behavior | May reveal runtime use, not full dependency inventory |

Use correlation to reduce duplicate triage while preserving each tool's evidence and limitations.

## Solution 13 — Maturity assessment

Example improvement path:

| Current state | Next step | Evidence |
|---|---|---|
| Level 0 | Evaluate one supported application in test | Agent compatibility and test report |
| Level 1 | Add agent to CI test startup | Repeatable pipeline run |
| Level 2 | Create issues automatically | Finding-to-ticket traceability |
| Level 3 | Measure coverage and performance | Periodic metrics review |
| Level 4 | Tune and correlate continuously | Improved coverage and remediation trends |

The maturity level should be based on evidence, not an aspirational target.

## Solution 14 — Capstone reference architecture

```text
Commit / Pull Request
        |
        v
      Build
        |
        v
Deploy isolated test app + IAST agent
        |
        v
Verify agent initialization
        |
        v
Functional / Integration / API tests
        |
        v
Collect IAST findings and coverage
        |
        +------> Correlate SAST / DAST
        |
        v
Sanitize reports and store securely
        |
        v
Apply security gate
        |
        v
Promote or block + cleanup
```

Track four independent outcomes:
- Application/test execution.
- Agent initialization and telemetry.
- Security findings and quality-gate status.
- Coverage and performance.

This prevents a failed or inactive agent from being misreported as a clean security run.

## Example quality-gate policy

For a training pipeline:
- Fail if the application or IAST agent fails to start.
- Fail if required instrumented tests do not execute.
- Fail on confirmed critical/high findings unless an approved exception exists.
- Require manual review for medium findings.
- Track lower-severity findings and remediation.
- Require owner, rationale, and expiry/review date for exceptions.
- Re-run the same tests after remediation.

Tune thresholds with application owners and the security team.

## Further reading

- [OWASP IAST Guideline](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-1-Interactive-Application-Security-Testing/)
- [OWASP DevSecOps Verification Standard — TEST-003](https://owasp.github.io/www-project-devsecops-verification-standard/document/TEST-003-Interactive-Application-Security-Testing-IAST.html)
- [AWS IAST DevOps Guidance](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/qa.st.8-improve-security-testing-accuracy-using-interactive-application-security-testing.html)
