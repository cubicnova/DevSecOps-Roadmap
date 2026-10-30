# False Positive Triage — Reference Solutions

## 1. Terminology

- **True positive:** the rule correctly identifies a real issue.
- **False positive:** the rule reports an issue that is not present in the reviewed context.
- **False negative:** a real issue is missed.
- **Accepted risk:** a real issue is formally accepted by an authorized risk owner.
- **Precision:** `TP / (TP + FP)`.
- **Recall:** `TP / (TP + FN)`.

A scanner's own alert list cannot reveal all false negatives. Recall requires a labeled set that includes known issues the scanner did not report.

## 2. Alert review

A useful initial record includes the exact rule ID, alert location, affected branch, severity, query help, source/sink details, and the commit that introduced the code. Do not decide based only on the alert title.

## 3. SQL injection trace

For a query such as:

```python
cursor.execute(
    "SELECT * FROM users WHERE name = ?",
    (username,)
)
```

the value is supplied separately from the SQL statement. If the specific database driver implements parameter binding as expected, the value is treated as data rather than SQL syntax. Verify the driver and call semantics before dismissing an alert.

For string concatenation into a query, the input may alter SQL syntax. If attacker-controlled data reaches that query without an effective control, classify it as a likely true positive.

## 4. Sanitizer validation

A sanitizer is valid only for its intended context. Check:

1. The exact implementation.
2. The data type and encoding assumptions.
3. Whether it is applied on every path.
4. Whether later code can undo the protection.
5. Whether the sink expects the same context.

For example, HTML escaping is not a SQL sanitizer and is not automatically safe for JavaScript or CSS contexts.

## 5. XSS context

| Output context | Appropriate approach |
|---|---|
| HTML text | Context-aware HTML text encoding |
| HTML attribute | Attribute encoding and safe attribute handling |
| JavaScript | Avoid string construction; use safe serialization and context-aware encoding |
| URL | Validate allowed schemes/hosts and encode URL components |

Prefer framework APIs that safely encode output by default. Verify whether the framework's escaping is disabled or bypassed.

## 6. False positive versus accepted risk

- If a supported parameterized API protects the value at the sink, the alert may be a false positive if the query fails to model that API.
- If an unsafe operation is genuinely present but an owner approves temporary use with compensating controls, it is an accepted risk—not a false positive.

Accepted risks need an owner, approver, rationale, controls, and expiry/review date.

## 7. Test or generated code

Do not assume test code is harmless. Confirm whether it is packaged, deployed, or executed in production. For generated code, locate the source template or generator and fix the root cause where possible. Any exclusion should be narrow and documented.

## 8. Example dismissal comment

```text
Reviewed the reported SQL injection path in this function.
The value is passed as a separate parameter to the verified database
driver API; it is not concatenated into the SQL statement.
The regression test supplies quote and SQL metacharacters and confirms
they are treated as a bound value. The query appears not to model this
parameter-binding API. Recommend updating the query model and retaining
the regression case.
```

Only use this comment when the evidence has actually been verified.

## 9. Rule improvement

A sound improvement process:

1. Save a minimal reproducer.
2. Identify the missing model or incorrect query assumption.
3. Update semantic API matching or source/sink/sanitizer modeling.
4. Add a negative test for the false positive.
5. Add a positive test for the real vulnerability.
6. Run the full query test suite.
7. Test on representative codebases and measure performance.

Do not suppress all alerts from a directory to remove one false positive.

## 10. Precision calculation

Given:

- True positives = 30
- False positives = 10

\[
Precision = \frac{30}{30+10} = 0.75 = 75\%
\]

Recall cannot be calculated because the number of false negatives is unknown. You need a labeled evaluation set containing known vulnerable cases, including cases the scanner failed to report.

## 11. Dismissal audit

For each sampled alert, verify:

- The reason matches the actual classification.
- Evidence is specific and reproducible.
- The control is appropriate for the sink.
- The finding is not merely accepted risk.
- The dismissal is scoped correctly.
- Any needed rule improvement is tracked.

Reopen or escalate findings that were incorrectly dismissed, following the repository's process.

## 12. Final case-study report

Suggested summary:

| Alert | Classification | Evidence | Action |
|---|---|---|---|
| A | True positive | Untrusted input reaches SQL concatenation | Fix and test |
| B | False positive | Verified parameter binding | Dismiss with evidence; improve model |
| C | Accepted risk | Unsafe behavior remains; approved exception | Track expiry and controls |
| D | Inconclusive | Framework wrapper not understood | Escalate and investigate |
| E | Duplicate | Same root issue tracked elsewhere | Link canonical issue |

Use real evidence from the lab rather than copying these example classifications.

## GitHub alert handling notes

GitHub code scanning supports resolving alerts by fixing the code or dismissing an alert with a reason. Dismissal comments can preserve context for audit and review. For a CodeQL false positive caused by an unmodeled sanitizer, consider improving the query/model rather than repeatedly dismissing equivalent findings.

## Key lesson

False-positive triage is evidence-based security analysis. The goal is not to make the alert count smaller; it is to preserve real vulnerabilities, remove incorrect findings responsibly, and improve the quality of detection over time.
