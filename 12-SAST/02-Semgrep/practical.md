# Semgrep — Practical Exercises

Complete these labs in a local training repository or an authorized GitLab project. Use dummy data and non-production credentials.

## Lab 1 — Install and verify Semgrep

1. Create a Python virtual environment or use an approved package manager.
2. Install Semgrep.
3. Run `semgrep --version`.
4. Run `semgrep scan --help`.
5. Record the installed version and installation method.

**Deliverable:** Installation notes with terminal output.

## Lab 2 — Scan a sample project

1. Create `sample_app/`.
2. Add a Python file containing a training `eval()` call.
3. Run `semgrep scan --config auto sample_app/`.
4. Review the rule ID, severity, message, and source location.
5. Save JSON output to `semgrep-results.json`.

**Deliverable:** Scan output and a short explanation of one finding.

## Lab 3 — Create a custom Python rule

1. Create `rules/python-security.yml`.
2. Add a rule matching `eval($EXPR)`.
3. Set a unique rule ID, message, severity, and CWE metadata.
4. Run Semgrep with the local rule.
5. Add a safe example and confirm whether it is also matched.
6. Explain why a syntax match is not automatically proof of exploitability.

## Lab 4 — Detect risky process execution

1. Create a Python sample using `subprocess.run(..., shell=True)`.
2. Write a Semgrep rule for the pattern.
3. Run the rule against the sample.
4. Refactor the code to pass a list of arguments without a shell.
5. Re-run the scan and compare results.

**Deliverable:** Before/after source and findings.

## Lab 5 — Detect weak cryptographic usage

1. Create a sample using `hashlib.md5()`.
2. Write a rule that detects this call.
3. Run the scan and inspect the output.
4. Replace the use case with an appropriate secure design.
5. Explain the difference between password hashing and file-integrity hashing.

## Lab 6 — Detect unsafe JavaScript DOM updates

1. Create a JavaScript file assigning dynamic data to `innerHTML`.
2. Write a custom rule matching the assignment.
3. Run Semgrep.
4. Replace text rendering with `textContent`.
5. Explain when HTML sanitization is required.

## Lab 7 — Use pattern operators

Create one rules file that demonstrates:
- `pattern`
- `patterns`
- `pattern-either`
- `pattern-not`
- A metavariable such as `$VALUE`

Run each rule against at least two code samples. Record expected and actual matches.

## Lab 8 — Explore taint analysis

1. Review the concepts of sources, sinks, propagators, and sanitizers.
2. Create a deliberately vulnerable local example where request data is passed into a database query.
3. Draft a taint-mode rule for the framework used in your sample.
4. Test the rule with the engine and version available to you.
5. Document limitations or unsupported syntax encountered.

Do not use a real database or public endpoint for this exercise.

## Lab 9 — Export and review findings

1. Run a scan with JSON output.
2. Run a scan with SARIF output.
3. Compare the information available in both formats.
4. Record finding IDs, severity, file, line, and remediation.
5. Do not commit generated reports if they contain sensitive source excerpts or internal paths.

## Lab 10 — Integrate Semgrep into GitLab CI

1. Create a sandbox GitLab project.
2. Add a Semgrep job to `.gitlab-ci.yml`.
3. Run the pipeline on a feature branch.
4. Add an intentionally vulnerable training sample.
5. Confirm the job reports the finding.
6. Fix the sample and rerun the pipeline.
7. Configure the job to fail for findings according to your team's policy.

## Lab 11 — Triage and suppress responsibly

1. Select one finding from the training project.
2. Verify whether the code path is reachable and whether input is untrusted.
3. Fix the issue if it is valid.
4. If it is a false positive, document why.
5. Test a narrowly scoped rule-specific suppression in the sample.
6. Add an owner and review date to the exception record.

Do not suppress a finding simply to make the pipeline green.

## Lab 12 — Build a small team ruleset

Create at least three custom rules:
- One Python rule.
- One JavaScript/TypeScript rule.
- One organization-specific secure coding rule.

For each rule, provide:
- Unique ID.
- Language.
- Severity and message.
- CWE or relevant security reference where appropriate.
- Positive test case.
- Negative/safe test case.
- Known limitations.

**Final deliverable:** `rules/`, sample source files, test results, GitLab CI configuration, and a short triage report.
