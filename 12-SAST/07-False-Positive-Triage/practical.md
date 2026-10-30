# False Positive Triage — Practical Exercises

## Lab requirements

- A test repository with intentionally vulnerable and safe code.
- A SAST scanner or CodeQL-enabled repository.
- Permission to view and manage the relevant alerts.
- A triage record template.

Do not dismiss real security issues simply to reduce alert counts.

## Exercise 1: Learn the terminology

Define false positive, false negative, true positive, accepted risk, precision, and recall. Give one example of each using a web application.

**Deliverable:** glossary and examples.

## Exercise 2: Review an alert

Choose a SAST alert and record:

1. Rule ID and title.
2. Severity and precision/confidence information.
3. File, line, and affected branch.
4. Relevant source and sink.
5. Rule help and remediation.

**Deliverable:** initial alert summary.

## Exercise 3: Trace a SQL injection path

1. Identify the input source.
2. Follow assignments and function calls.
3. Identify the SQL sink.
4. Determine whether parameter binding or another valid control is used.
5. Classify the alert with evidence.

**Deliverable:** source-to-sink trace.

## Exercise 4: Validate a sanitizer

1. Find the sanitizer or validation helper.
2. Read its implementation.
3. Confirm it is appropriate for the output/sink context.
4. Check whether every path passes through it.
5. Create a positive and negative test.

**Deliverable:** sanitizer assessment.

## Exercise 5: Review XSS context

Compare HTML text, HTML attribute, JavaScript, and URL contexts. Determine which encoding or safe API is required for each. Explain why one generic escaping function may not protect every context.

**Deliverable:** context-specific remediation table.

## Exercise 6: Distinguish false positive from accepted risk

Review two sample alerts: one protected by a verified safe API and one that is real but temporarily tolerated. Classify them separately and document the required approval for the accepted risk.

**Deliverable:** two triage records.

## Exercise 7: Review test and generated code

1. Identify an alert in test or generated code.
2. Determine whether it is shipped or executed in production.
3. Trace generated code to its template or generator.
4. Decide whether to fix, exclude, or escalate.
5. Document the reason.

**Deliverable:** scope assessment.

## Exercise 8: Write a dismissal comment

Write an evidence-based comment for a verified false positive. Include the exact control, relevant code path, and test evidence. Avoid unsupported claims.

**Deliverable:** dismissal comment.

## Exercise 9: Improve a noisy rule

1. Reproduce a false positive.
2. Identify the query's incorrect assumption.
3. Propose semantic matching or an additional library model.
4. Add a negative regression test.
5. Add a positive test to ensure true positives remain detected.

**Deliverable:** rule-improvement proposal and tests.

## Exercise 10: Calculate precision

Given 40 reviewed alerts, 30 are true positives and 10 are false positives.

1. Calculate precision.
2. Explain why recall cannot be calculated from these alert counts alone.
3. Identify what additional labeled data is needed.

**Deliverable:** calculation and explanation.

## Exercise 11: Audit dismissed findings

1. Sample 10 previously dismissed alerts.
2. Check the classification and evidence.
3. Identify unsupported dismissals.
4. Reopen or escalate any incorrectly closed issue according to policy.
5. Recommend process improvements.

**Deliverable:** dismissal quality report.

## Exercise 12: Final triage case study

For a small training application:

1. Review at least five findings.
2. Trace each relevant data flow.
3. Classify each finding.
4. Record evidence and remediation.
5. Add a regression test for at least one issue.
6. Produce a summary of trends and rule improvements.

**Deliverable:** triage report and evidence log.

## Assessment rubric

| Area | Marks |
|---|---:|
| Terminology and metrics | 10 |
| Alert investigation | 15 |
| Source-to-sink reasoning | 20 |
| Sanitizer/context validation | 15 |
| Correct classification and evidence | 15 |
| Rule improvement and regression tests | 15 |
| Reporting and governance | 10 |
| **Total** | **100** |
