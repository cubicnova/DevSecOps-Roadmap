# CodeQL Practical Exercises

## Lab requirements

- A test repository containing code you are authorized to analyze.
- CodeQL CLI installed from an official source.
- Git and a supported runtime/build tool for the selected language.
- Optional: a GitHub repository where code scanning is enabled.

Do not run analysis against repositories or code you do not have permission to inspect. Use intentionally vulnerable training code, not production systems.

## Exercise 1: Verify the environment

1. Install the CodeQL CLI.
2. Run `codeql version`.
3. Run `codeql resolve languages`.
4. Record the CLI version and languages available.

**Deliverable:** environment notes.

## Exercise 2: Create a database

1. Clone or create a small Python training project.
2. Navigate to the project root.
3. Create a database named `db-python`.
4. Inspect the database metadata.
5. Record any warnings.

**Deliverable:** command history and database information.

## Exercise 3: Run a standard query suite

1. Analyze `db-python` with `codeql/python-queries`.
2. Export SARIF.
3. Identify at least three results or explain why the sample project produced none.
4. Record rule IDs and locations.

**Deliverable:** sanitized SARIF review notes.

## Exercise 4: Understand sources and sinks

Given a web endpoint that reads a request parameter and passes it to a database operation:

1. Identify the possible source.
2. Identify the sensitive sink.
3. Identify validation or parameterization steps.
4. Draw the data path.

**Deliverable:** source-to-sink diagram or written trace.

## Exercise 5: Compare vulnerable and fixed SQL

1. Inspect the vulnerable function in `examples.md`.
2. Explain why concatenation is unsafe.
3. Replace it with a parameterized query.
4. Run the same CodeQL analysis before and after.
5. Compare findings and explain any change.

**Deliverable:** before/after code and scan notes.

## Exercise 6: Review command execution

1. Inspect the `os.system` example.
2. Identify attacker-controlled input.
3. Explain shell metacharacter risk.
4. Implement a safer argument-list approach and input allowlist.
5. Discuss why path restrictions are still needed.

**Deliverable:** remediation explanation and test cases.

## Exercise 7: Write a basic QL query

1. Create a query pack.
2. Add the `FindDangerousCall.ql` teaching query from `examples.md`.
3. Compile the pack.
4. Run the query against the database.
5. Review the results.

**Deliverable:** query source, compile output, and result summary.

## Exercise 8: Improve a query

1. Identify a weakness in matching a function using `toString()`.
2. Research the language library's API for identifying the call target.
3. Update the query to use a more robust semantic predicate.
4. Test positive and negative examples.

**Deliverable:** improved query and test notes.

## Exercise 9: Build a custom query pack

1. Create `qlpack.yml`.
2. Add a query and a README.
3. Install dependencies.
4. Compile the pack.
5. Run `database analyze` with the pack.

**Deliverable:** complete pack directory.

## Exercise 10: Configure GitHub code scanning

1. Use the repository's Security or Code Security settings to check feature availability.
2. Add or generate a CodeQL workflow.
3. Configure the language matrix.
4. Configure the build mode if the project requires compilation.
5. Run the workflow on a test branch.
6. Review the code scanning alerts.

**Deliverable:** workflow file and a screenshot or text summary of the run.

## Exercise 11: Triage a finding

For one alert:

1. Read the rule description and query help.
2. Inspect the complete code path.
3. Determine whether the input is attacker-controlled.
4. Assess reachability and impact.
5. Decide whether it is a true positive, false positive, or needs more investigation.
6. Record the evidence.

**Deliverable:** finding triage record.

## Exercise 12: Export and inspect SARIF

1. Export a scan in `sarif-latest` format.
2. Validate that the file is valid JSON.
3. Locate the rule ID, message, and physical location for a result.
4. Identify whether code-flow information is included.
5. Store the artifact securely.

**Deliverable:** annotated SARIF excerpt with sensitive details removed.

## Exercise 13: Add a regression test

1. Fix one confirmed vulnerability.
2. Add a test that exercises the expected safe behavior.
3. Rerun the query suite.
4. Confirm the alert is resolved or explain why the query still reports it.
5. Document residual risk.

**Deliverable:** test, remediation, and rescan notes.

## Exercise 14: Design a secure scanning pipeline

Design a CI workflow that:

- Runs on pull requests and pushes to the protected branch.
- Uses least-privilege permissions.
- Uses a supported language and build mode.
- Uploads SARIF through the supported CodeQL action.
- Avoids exposing secrets to untrusted pull-request code.
- Runs scheduled analysis.
- Defines ownership and triage expectations.

**Deliverable:** workflow YAML and a short security design note.

## Assessment rubric

| Area | Marks |
|---|---:|
| CLI setup and database creation | 10 |
| Built-in query analysis | 15 |
| Source/sink reasoning | 15 |
| Custom query and pack | 20 |
| GitHub Actions integration | 15 |
| Finding triage and remediation | 15 |
| Documentation and reproducibility | 10 |
| **Total** | **100** |
