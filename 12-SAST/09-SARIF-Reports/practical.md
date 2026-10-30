# SARIF Reports — Practical Exercises

## Lab requirements

- Python 3 installed.
- A text editor and terminal.
- CodeQL CLI or another SARIF-compatible scanner (optional for early exercises).
- A GitHub repository with code scanning access for upload exercises.

Use a training repository and do not upload reports containing sensitive source details to public locations.

## Exercise 1: Understand SARIF

1. Explain what SARIF stands for.
2. Identify the purpose of `version`, `$schema`, and `runs`.
3. Explain the difference between a rule definition and a result.
4. Identify three benefits of a common reporting format.

**Deliverable:** short explanation.

## Exercise 2: Inspect the sample report

1. Open `samples/minimal.sarif`.
2. Identify the tool name and version.
3. Find the rule ID.
4. Identify the finding level and message.
5. Find the file path and starting line.

**Deliverable:** annotated SARIF field map.

## Exercise 3: Validate JSON

1. Run `python -m json.tool` against the sample.
2. Intentionally remove a comma.
3. Run validation again.
4. Record the error.
5. Restore the valid JSON.

**Deliverable:** validation output and explanation.

## Exercise 4: Parse results with Python

1. Use the Python example in `examples.md`.
2. Print tool name, rule ID, level, message, file, and line.
3. Modify the script to count results by level.
4. Handle a report with no results.

**Deliverable:** working parser script.

## Exercise 5: Add a new result

1. Add a second rule definition.
2. Add a result referencing that rule.
3. Use a different source file and line.
4. Parse the report again.
5. Confirm both results appear.

**Deliverable:** updated SARIF sample.

## Exercise 6: Understand locations

1. Change the artifact URI.
2. Add a start column and end line.
3. Explain why repository-relative paths are useful.
4. Identify what can happen when paths do not match the checked-out repository.

**Deliverable:** location analysis.

## Exercise 7: Understand code flows

1. Inspect the code-flow example.
2. Identify the source and sink messages.
3. Explain how a reviewer uses the path.
4. Add one intermediate location.
5. Explain why a code flow is not required for every finding.

**Deliverable:** annotated code-flow example.

## Exercise 8: Generate SARIF with CodeQL

1. Create a CodeQL database for a supported training project.
2. Run a query suite.
3. Export using `--format=sarif-latest`.
4. Inspect the output.
5. Record the CLI version and command.

**Deliverable:** SARIF file and run notes.

## Exercise 9: Compare two scan reports

1. Generate or prepare two reports from different commits.
2. Compare tool name, rule IDs, result counts, locations, and fingerprints.
3. Identify new, resolved, and persistent findings.
4. Explain how unstable fingerprints can affect alert tracking.

**Deliverable:** comparison report.

## Exercise 10: Upload third-party SARIF

1. Confirm repository code-scanning availability.
2. Generate a compatible SARIF file.
3. Add an upload workflow using `upload-sarif`.
4. Grant only the required permissions.
5. Use a distinct category for a separate analysis stream.
6. Run the workflow and review the uploaded alerts.

**Deliverable:** workflow and upload evidence.

## Exercise 11: Troubleshoot an upload

Investigate a simulated upload failure caused by one of the following:

- Invalid JSON.
- Unsupported SARIF properties/version.
- Incorrect source path.
- Missing permission.
- Duplicate category.
- File-size limit.

**Deliverable:** root-cause notes and corrected report/workflow.

## Exercise 12: Protect SARIF artifacts

1. Identify sensitive information that may appear in SARIF.
2. Set an appropriate artifact retention period.
3. Restrict artifact access.
4. Explain how to share a sanitized report without breaking the original audit evidence.
5. Document credential-handling controls.

**Deliverable:** SARIF handling policy.

## Exercise 13: Final mini-project

Create a small reporting pipeline that:

1. Runs a SAST scanner or CodeQL.
2. Exports SARIF.
3. Validates JSON and SARIF structure.
4. Summarizes findings by rule and level.
5. Uploads the report to GitHub code scanning or stores it securely as an artifact.
6. Documents limitations and troubleshooting steps.

**Deliverable:** working pipeline, sample report, and documentation.

## Assessment rubric

| Area | Marks |
|---|---:|
| SARIF concepts and structure | 10 |
| Field inspection and locations | 15 |
| JSON parsing and validation | 15 |
| CodeQL/SAST report generation | 15 |
| Code-flow and fingerprint understanding | 15 |
| GitHub upload integration | 15 |
| Security, privacy, and troubleshooting | 15 |
| **Total** | **100** |
