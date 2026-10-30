# Custom Security Rules — Practical Exercises

## Lab requirements

- CodeQL CLI and a supported language query pack.
- A small training repository you are authorized to analyze.
- Git and a supported runtime.
- A custom query pack workspace.

Use intentionally vulnerable sample code. Do not test against codebases without permission.

## Exercise 1: Identify a policy gap

Choose one internal secure-coding requirement not adequately covered by your existing scanners.

1. Write the required secure behavior in one sentence.
2. Describe the threat and impact.
3. Identify the relevant language/framework.
4. Decide whether CodeQL, a linter, SCA, secret scanning, or a CI policy is the best fit.

**Deliverable:** one-page rule proposal.

## Exercise 2: Write a rule specification

Define:

- Rule ID and title.
- Objective and risk.
- Scope.
- Detection logic.
- Severity and confidence.
- Positive and negative examples.
- Remediation guidance.
- Rule owner and exception process.

**Deliverable:** completed rule specification.

## Exercise 3: Create a custom CodeQL pack

1. Create the directory structure from `examples.md`.
2. Add `qlpack.yml`.
3. Add a `queries/python` directory.
4. Install dependencies.
5. Compile the pack.

**Deliverable:** pack that compiles successfully.

## Exercise 4: Implement a prohibited API rule

1. Use the teaching query in `examples.md`.
2. Run it against a Python database.
3. Confirm the direct prohibited call is reported.
4. Add a safe wrapper example.
5. Check whether the simple string match produces false positives or false negatives.

**Deliverable:** query and observed results.

## Exercise 5: Improve semantic matching

1. Research the Python CodeQL library's call and import models.
2. Replace fragile rendered-string matching with semantic API identification.
3. Test direct imports, aliases, qualified names, and unrelated functions with the same short name.
4. Document remaining limitations.

**Deliverable:** improved query and test matrix.

## Exercise 6: Design a weak-password-hash rule

1. Define the exact policy for password storage.
2. Identify APIs that must be prohibited and approved alternatives.
3. Explain why flagging every SHA-256 call would be noisy.
4. Build positive and negative examples.
5. Propose how to model wrappers and helper functions.

**Deliverable:** rule specification and test corpus.

## Exercise 7: Design an insecure TLS configuration rule

1. Identify insecure TLS options in the chosen language/framework.
2. Create one positive example and two safe examples.
3. Consider wrappers, defaults, and configuration objects.
4. Decide whether the rule should flag a call, configuration value, or data flow.
5. Write remediation guidance.

**Deliverable:** query design and examples.

## Exercise 8: Test rule quality

For one custom rule, create at least:

- Three positive cases.
- Three negative cases.
- Two boundary cases.
- One alias or wrapper case.
- One regression case.

Record expected and actual results. Explain every mismatch.

**Deliverable:** test plan and result table.

## Exercise 9: Add query help

1. Create a Markdown help file beside the `.ql` query.
2. Explain the risk in plain language.
3. Describe the safe alternative.
4. Run analysis with SARIF query help enabled.
5. Inspect the SARIF output.

**Deliverable:** query help and SARIF excerpt.

## Exercise 10: Integrate into CI

1. Build or retrieve the CodeQL database in the workflow.
2. Install the custom pack.
3. Run `database analyze`.
4. Upload SARIF using the supported integration.
5. Set least-privilege permissions.
6. Test on a branch before enabling required checks.

**Deliverable:** CI workflow and run evidence.

## Exercise 11: Tune false positives

1. Review each alert from your test repository.
2. Identify whether the query is too broad.
3. Improve semantic matching or add a safe API model.
4. Add a negative regression test for every corrected false positive.
5. Rerun the full test suite.

**Deliverable:** before/after precision notes.

## Exercise 12: Exception governance

Create an exception process that includes:

- Rule ID and exact affected location.
- Owner and approver.
- Business reason and risk assessment.
- Compensating controls.
- Expiry and review dates.
- Evidence that the exception is narrowly scoped.

**Deliverable:** sample exception record and workflow.

## Exercise 13: Measure rule effectiveness

Define how you will measure:

- True-positive rate.
- False-positive rate.
- Time to triage.
- Time to remediate.
- Rule execution time.
- Exception age.
- Repository coverage.

**Deliverable:** metrics dashboard outline.

## Exercise 14: Final mini-project

Create one production-style custom security rule for an application-specific risk.

Include:

1. Rule specification.
2. CodeQL query or appropriate alternative.
3. Positive, negative, boundary, and regression tests.
4. Query help and remediation advice.
5. CI integration.
6. Exception process.
7. A short review of limitations and maintenance needs.

**Deliverable:** complete rule pack and project report.

## Assessment rubric

| Area | Marks |
|---|---:|
| Policy and threat definition | 10 |
| Rule specification | 10 |
| Query implementation | 20 |
| Positive/negative test coverage | 20 |
| False-positive tuning | 10 |
| CI integration | 15 |
| Documentation and governance | 10 |
| Metrics and maintenance plan | 5 |
| **Total** | **100** |
