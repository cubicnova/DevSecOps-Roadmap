# SAST Fundamentals — Practical Exercises

## Lab requirements
- GitLab project with CI/CD enabled.
- An eligible Linux-based runner using Docker or Kubernetes executor, as required by the selected analyzer.
- A supported language repository (Python, JavaScript, Java, Go, PHP, or another currently supported language).
- A local training application and test database.
- Do not commit real secrets or deploy vulnerable examples to public or production environments.

## Exercise 1: Understand SAST
Write a short explanation of SAST and compare it with DAST, IAST, and SCA.

**Tasks**
1. Identify which SDLC phase SAST can be used in.
2. Explain why SAST does not need a running application.
3. List three limitations of static analysis.

**Deliverable:** One-page comparison.

## Exercise 2: Identify sources and sinks
Review a small web application and identify:
- Three untrusted input sources.
- Three sensitive sinks.
- Any validation, sanitization, or encoding between them.

Create a simple source-to-sink table.

## Exercise 3: Find SQL injection
1. Review the vulnerable SQL example in `examples.md`.
2. Identify the user-controlled source and SQL sink.
3. Explain how string concatenation changes query structure.
4. Replace concatenation with parameterized SQL.
5. Add a unit test verifying that an input is treated as data.

**Expected result:** SQL statements use parameters rather than concatenated user input.

## Exercise 4: Find XSS
1. Review the vulnerable Flask example.
2. Identify the untrusted input and HTML output sink.
3. Replace direct HTML construction with safe template interpolation.
4. Test with a harmless string containing HTML metacharacters.
5. Confirm the browser displays the input as text rather than executing it.

Do not use payloads against a live third-party application.

## Exercise 5: Find command injection risk
1. Review the `os.system` example.
2. Explain why concatenating input into a shell command is dangerous.
3. Replace it with `subprocess.run` using an argument list and `shell=False`.
4. Add validation to restrict allowed directories.
5. Test normal and invalid inputs.

## Exercise 6: Identify path traversal
1. Review the vulnerable file path example.
2. Identify how untrusted path segments can escape the intended directory.
3. Resolve the final path.
4. Confirm it remains within the trusted base directory.
5. Add tests for normal filenames and path escape attempts.

## Exercise 7: Enable GitLab SAST
1. Add the following to `.gitlab-ci.yml`:

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

2. Commit to a feature branch.
3. Open a merge request.
4. Inspect the pipeline and SAST jobs.
5. Confirm which analyzer runs for the repository language.
6. Download and inspect the SAST report artifact if available.

## Exercise 8: Analyze a SAST finding
For at least one finding, record:
- Rule name and CWE.
- File and line.
- Severity and confidence.
- Source and sink, if provided.
- Data flow path.
- Business impact.
- Recommended fix.

Explain whether the finding is confirmed, a false positive, or needs more investigation.

## Exercise 9: Fix and rescan
1. Fix the confirmed issue in a feature branch.
2. Add or update a regression test.
3. Run SAST again.
4. Compare the new report with the previous one.
5. Confirm the finding is resolved or explain why it remains.

## Exercise 10: Configure excluded paths carefully
1. Review the default excluded paths for your GitLab version.
2. Add one narrow training fixture path to `SAST_EXCLUDED_PATHS`.
3. Run a scan and compare results.
4. Document what is no longer scanned.
5. Remove the exclusion and verify coverage returns.

Do not exclude production source directories merely to hide findings.

## Exercise 11: False-positive triage
Choose one finding that may be a false positive or requires contextual review.

**Tasks**
- Trace the data flow.
- Inspect validation and encoding.
- Determine whether the source is attacker-controlled.
- Determine whether the sink is reachable.
- Document evidence and conclusion.
- If suppressing, document owner, rationale, scope, and review date.

## Exercise 12: Build a SAST workflow
Create a small workflow containing:
- A build or syntax-check job.
- GitLab SAST template.
- A merge-request pipeline.
- A documented triage process.
- A remediation commit and rescan.

**Deliverable:** Pipeline YAML, scan report, remediation diff, and short report.

## Submission checklist
- [ ] SAST compared with DAST, IAST, and SCA.
- [ ] Sources and sinks identified.
- [ ] SQL injection example fixed.
- [ ] XSS example fixed.
- [ ] Command injection example fixed.
- [ ] Path traversal example fixed.
- [ ] GitLab SAST enabled.
- [ ] At least one SAST finding analyzed.
- [ ] Finding fixed and rescanned.
- [ ] Excluded paths reviewed.
- [ ] False-positive assessment documented.
- [ ] Complete SAST workflow submitted.

## Viva questions
1. What is SAST?
2. What is the difference between SAST and DAST?
3. What is a source in taint analysis?
4. What is a sink?
5. What is taint analysis?
6. What is a false positive?
7. What is a false negative?
8. Name five common vulnerabilities SAST can identify.
9. Why are parameterized SQL queries recommended?
10. Why should untrusted input not be concatenated into shell commands?
11. What is CWE?
12. Does a clean SAST report prove that an application is secure?
