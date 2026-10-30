# IAST Fundamentals — Practical Labs

## Lab safety

Use a local training application or an explicitly authorized non-production environment. IAST agents can collect sensitive runtime context. Use synthetic accounts and data, restrict access to reports, and follow the selected vendor's privacy and deployment guidance.

## Lab 1 — Compare SAST, DAST, and IAST

**Tasks**

1. Select one example vulnerability such as SQL injection.
2. Describe how SAST might identify a risky query construction.
3. Describe how DAST might test the running endpoint.
4. Describe how IAST might observe request data reaching a database sink.
5. List what each method can miss.

**Deliverable:** comparison table.

## Lab 2 — Identify sources and sinks

Review a small application and identify at least five sources and five sinks.

Possible sources:
- HTTP query parameter.
- JSON request body.
- Cookie or header.
- Uploaded file.
- Message queue input.

Possible sinks:
- SQL execution.
- Shell command.
- File system access.
- HTML output.
- URL fetch or XML parser.

**Deliverable:** `sources-and-sinks.md` with file/function references.

## Lab 3 — Trace data flow

Use the examples in `examples.md`.

**Tasks**

1. Follow a user-controlled value from request parsing.
2. Track transformations and function calls.
3. Identify the operation where the value reaches a sensitive sink.
4. Propose a context-appropriate mitigation.
5. Explain how an IAST trace could help a developer.

**Deliverable:** source-to-sink flow diagram and remediation note.

## Lab 4 — Instrument a Java training application

**Tasks**

1. Create or use a small Java web application in a local test environment.
2. Check the selected IAST product's supported Java and framework versions.
3. Install the agent according to vendor instructions.
4. Attach it at application startup.
5. Confirm successful agent initialization.
6. Run a small functional test suite.
7. Review a sanitized trace or finding.

**Deliverable:** startup notes, compatibility matrix, and sample finding. Do not include license keys or API secrets.

## Lab 5 — Instrument a .NET application

**Tasks**

1. Select a supported .NET runtime and sample web API.
2. Review the vendor's CLR profiler requirements.
3. Configure the agent in a test container or VM.
4. Start the application and verify agent initialization.
5. Exercise two endpoints.
6. Review runtime telemetry and any IAST findings.
7. Compare performance with an uninstrumented baseline.

**Deliverable:** configuration checklist and comparison.

## Lab 6 — Instrument a Node.js or Python application

**Tasks**

1. Select a vendor-supported agent and framework.
2. Create an isolated environment.
3. Configure the agent bootstrap or middleware as documented.
4. Start the application.
5. Run tests against the application.
6. Confirm that requests are observed.
7. Record unsupported libraries or runtime limitations.

**Deliverable:** integration notes and compatibility gaps.

## Lab 7 — Exercise application paths

**Tasks**

1. List the application's main API routes.
2. Build a test suite that exercises anonymous, authenticated, and privileged paths.
3. Include positive and negative input cases.
4. Exercise error handling and file operations where relevant.
5. Run the suite with the IAST agent enabled.
6. Compare observed routes with the API inventory.

**Deliverable:** route coverage matrix.

## Lab 8 — Analyze an IAST finding

For each finding, capture:
- Rule/vulnerability name.
- Source and sink.
- File and line.
- Request/transaction context.
- Stack trace.
- Severity and confidence.
- Reproduction steps.
- Recommended fix.

**Tasks**

1. Confirm the finding belongs to the correct build.
2. Inspect the source and sink.
3. Verify whether data is actually controllable by an untrusted caller.
4. Determine whether a mitigation is present.
5. Reproduce safely.
6. Record the final triage status.

**Deliverable:** sanitized finding analysis.

## Lab 9 — Measure instrumentation overhead

**Tasks**

1. Run a representative test workload without IAST.
2. Record startup time, median response time, CPU, and memory.
3. Enable the IAST agent.
4. Repeat the same workload and test data.
5. Compare results.
6. Repeat enough times to avoid relying on one noisy measurement.
7. Agree performance thresholds with the application owner.

**Deliverable:** performance comparison report.

## Lab 10 — Privacy and agent hardening review

**Tasks**

1. Identify what request and runtime data the agent collects.
2. Check redaction rules for passwords, tokens, and personal data.
3. Review agent-to-collector network paths.
4. Check TLS and authentication configuration.
5. Review console roles and report retention.
6. Confirm agent secrets are stored outside source control.
7. Document a rollback and disablement process.

**Deliverable:** `iast-agent-security-review.md`.

## Lab 11 — CI/CD integration

**Tasks**

1. Add the agent to an isolated test deployment.
2. Start the application with instrumentation enabled.
3. Run integration and API tests.
4. Export findings using the selected product's supported interface.
5. Save sanitized reports as CI artifacts.
6. Fail or mark the build inconclusive if the agent does not initialize.
7. Apply a documented gate for confirmed high-risk findings.
8. Clean up test resources.

**Deliverable:** pipeline YAML, sanitized report, and quality-gate policy.

## Lab 12 — Correlate IAST with SAST and DAST

**Tasks**

1. Run SAST against the source code.
2. Run DAST against the test deployment.
3. Run IAST during functional/integration tests.
4. Compare findings by endpoint, rule, file, and vulnerability type.
5. Identify duplicate findings and complementary coverage.
6. Note issues visible to only one testing method.
7. Avoid treating an unobserved path as safe.

**Deliverable:** correlation matrix.

## Lab 13 — IAST maturity assessment

Assess the team against these stages:

- Level 0: no IAST.
- Level 1: manual/on-demand use.
- Level 2: automatic CI integration.
- Level 3: centralized issue tracking and periodic review.
- Level 4: continuous coverage, tuning, metrics, and correlation.

**Tasks**

1. Select the current level and provide evidence.
2. Identify the next practical maturity improvement.
3. Assign an owner and measurable outcome.
4. Define a review cadence.

**Deliverable:** IAST maturity plan.

## Lab 14 — Capstone: Instrumented DevSecOps workflow

Build an end-to-end workflow for a sample application.

Required elements:

1. Build the application.
2. Deploy it in an isolated test environment.
3. Attach a supported IAST agent.
4. Verify successful agent initialization.
5. Run functional, integration, and API tests.
6. Collect and sanitize findings.
7. Correlate with SAST and DAST output.
8. Apply a documented security gate.
9. Upload reports with restricted access and retention.
10. Clean up the test environment.
11. Measure coverage and performance overhead.
12. Document limitations and untested paths.

**Deliverables:**
- Architecture diagram.
- Agent configuration checklist.
- Test suite and coverage matrix.
- Sanitized IAST report.
- Correlation matrix.
- Quality-gate policy.
- Performance report.
- Retest and maturity summary.

## Submission checklist

- [ ] SAST, DAST, and IAST differences explained.
- [ ] Sources and sinks identified.
- [ ] Data flow traced.
- [ ] Runtime compatibility checked.
- [ ] Agent initialization verified.
- [ ] Functional/API tests exercised relevant paths.
- [ ] Findings manually reviewed.
- [ ] Performance overhead measured.
- [ ] Sensitive data redaction reviewed.
- [ ] CI integration and failure behavior documented.
- [ ] SAST/DAST/IAST correlation completed.
- [ ] Untested paths and limitations documented.
