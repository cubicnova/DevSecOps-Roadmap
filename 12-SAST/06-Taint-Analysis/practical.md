# Taint Analysis — Practical Exercises

Complete these labs in a local training application or an authorized repository. Use harmless test values and never test against production systems without explicit authorization.

## Lab 1 — Identify sources and sinks

For each code sample, identify:
- Source
- Tainted variable
- Propagation step
- Sink
- Potential security impact

Samples to inspect:
1. HTTP parameter used in SQL.
2. Header value written to logs.
3. Uploaded filename used in a file path.
4. User-supplied URL passed to an HTTP client.
5. Request value inserted into HTML.

**Deliverable:** A source-to-sink table with at least five flows.

## Lab 2 — Trace a direct SQL flow

1. Create a local Python function that reads a request parameter.
2. Concatenate the value into a SQL query in a mock or local test database.
3. Mark the source and sink in comments.
4. Draw the data-flow path.
5. Replace concatenation with parameterized SQL.
6. Add a regression test confirming the value is treated as data.

**Deliverable:** Vulnerable and fixed examples plus tests.

## Lab 3 — Trace an interprocedural flow

1. Move query construction into a helper function.
2. Pass the request value into the helper.
3. Return the generated query to the handler.
4. Identify every function boundary.
5. Compare manual tracing with a SAST tool's output.
6. Explain whether the tool followed the flow.

**Deliverable:** Call-flow diagram and tool results.

## Lab 4 — Command injection analysis

1. Create a local sample that passes user input into a shell command.
2. Identify the source, propagation, and sink.
3. Replace shell execution with a fixed executable and argument list.
4. Validate user choices against a strict allowlist.
5. Add tests for valid and invalid values.
6. Re-run the static analysis.

Do not execute destructive commands or use real system paths as targets.

## Lab 5 — XSS flow analysis

1. Create a JavaScript sample that assigns dynamic input to `innerHTML`.
2. Identify the untrusted source and browser interpretation sink.
3. Replace the operation with `textContent` for plain text.
4. If rich HTML is needed, document the sanitizer and configuration.
5. Add a test proving the intended text is rendered safely.

## Lab 6 — Path traversal flow

1. Create a local sample that accepts a filename from a request.
2. Trace the filename into the file read operation.
3. Demonstrate why checking only for the substring `../` is insufficient.
4. Implement a server-side allowlist or safe identifier mapping.
5. Resolve the final path and verify it remains under the approved directory.
6. Test normal, unknown, and traversal-like inputs.

## Lab 7 — SSRF flow

1. Identify a sample that passes a user-supplied URL to an HTTP client.
2. Mark the source and outbound request sink.
3. Design an allowlist-based destination policy.
4. Include redirect and DNS/IP resolution considerations.
5. Add network egress restrictions to the proposed architecture.
6. Write a short test plan using mock endpoints only.

Do not probe internal networks, metadata endpoints, or third-party systems.

## Lab 8 — Sensitive data leakage

1. Create a sample that logs an authorization header or access token.
2. Identify the sensitive source and logging sink.
3. Replace the log with a boolean or request identifier.
4. Search test logs for the dummy token.
5. Document log retention and access requirements.

## Lab 9 — Build a Semgrep taint rule

1. Create `rules/python-taint.yml`.
2. Define a source for the request API used by your sample.
3. Define a sink for the database API.
4. Run Semgrep against vulnerable and fixed examples.
5. Record false positives and missed flows.
6. Refine the rule and add comments explaining its limitations.

Use the official Semgrep syntax for the engine/version installed.

## Lab 10 — Model sanitizers and validators

1. Identify a real sanitizer or validator in your sample.
2. Read its implementation or trusted framework documentation.
3. Determine which output context it protects.
4. Test whether the analysis tool recognizes it.
5. Model it only for the appropriate sink.
6. Confirm that the same sanitizer is not incorrectly treated as safe for a different sink.

## Lab 11 — Compare static and dynamic taint analysis

1. Run a static taint scan on the sample.
2. Exercise the relevant route in a local test environment using dummy input.
3. Record the runtime-observed flow if your dynamic tool supports it.
4. Compare coverage, evidence, and limitations.
5. Explain why a dynamic test may miss an unexecuted path and why static analysis may report an infeasible path.

## Lab 12 — CI/CD integration and triage

1. Add a taint-focused scan to a sandbox CI pipeline.
2. Store any required credentials securely.
3. Run on a feature branch.
4. Introduce a controlled vulnerable training sample.
5. Verify the finding appears.
6. Fix the sample and rerun.
7. Define which findings block the pipeline and which require review.
8. Document exception ownership and expiry.

**Final deliverable:** Source samples, fixed versions, custom rules, scan outputs, CI configuration, and a triage report.

## Report template

For each flow, record:

| Field | Description |
|---|---|
| Finding ID | Tool rule or issue identifier |
| Source | Entry point of untrusted/sensitive data |
| Sink | Sensitive operation |
| Propagation | Variables/functions carrying the value |
| Control | Sanitizer, validator, parameterization, or none |
| Reachability | Can an attacker reach the path? |
| Impact | What could happen if exploited? |
| Remediation | Correct context-specific fix |
| Validation | Regression test and rescan result |
