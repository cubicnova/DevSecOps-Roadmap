# Finding Triage — Practical Labs

## Lab safety and prerequisites

Use security findings from your own training repository, local vulnerable application, or an authorized assessment. Do not paste secrets, personal data, production customer records, or unredacted tokens into tickets or public reports.

Suggested tools:
- SAST, DAST, IAST, and SCA sample reports.
- SARIF and JSON viewers.
- Spreadsheet or issue tracker.
- Python 3.
- Git repository with a known test commit.

## Lab 1 — Build a finding inventory

**Tasks**

1. Collect sample findings from at least three sources (for example SAST, DAST, and SCA).
2. Record source tool, rule/CVE, title, severity, confidence, asset, location, and first-seen date.
3. Preserve a copy of the raw report.
4. Identify missing fields and inconsistent severity labels.

**Deliverable:** `finding-inventory.csv` and a data-quality note.

## Lab 2 — Normalize scanner output

**Tasks**

1. Define a common finding schema.
2. Map each scanner's fields into the schema.
3. Preserve original rule IDs, CVE/CWE identifiers, and evidence references.
4. Keep the original severity alongside normalized severity.
5. Record the mapping rules.

**Deliverable:** normalized JSON and mapping document.

## Lab 3 — Deduplicate findings

**Tasks**

1. Create sample duplicate alerts from two scanners.
2. Compare asset, location, package, endpoint, rule, and root cause.
3. Group alerts that share the same remediation.
4. Select a canonical finding ID.
5. Link duplicate records without deleting their evidence.
6. Identify two cases that should not be merged.

**Deliverable:** deduplication rules and canonical-finding table.

## Lab 4 — Validate a SAST finding

**Tasks**

1. Select a SAST alert for injection or insecure API usage.
2. Check the exact commit and file/line.
3. Trace the source and sink.
4. Determine whether input is attacker-controlled.
5. Inspect validation, parameterization, or encoding.
6. Reproduce safely or create a focused unit/integration test.
7. Record the evidence and verdict.

**Deliverable:** finding validation record.

## Lab 5 — Validate a DAST/API finding

**Tasks**

1. Select a finding from a local training API.
2. Recreate the request using a test account.
3. Capture a sanitized response.
4. Confirm the behavior and affected endpoint.
5. Assess authentication and authorization requirements.
6. Record the business impact and remediation.

**Deliverable:** sanitized reproduction steps.

## Lab 6 — Classify dispositions

For at least ten sample findings, assign one of:
- Confirmed true positive.
- False positive.
- Duplicate.
- Accepted risk.
- Needs investigation.
- Not applicable/out of scope.

**Tasks**

1. Write the reason for each decision.
2. Attach evidence.
3. Identify the reviewer.
4. Set an owner and next action for unresolved findings.
5. Ensure accepted risk has approval and expiry.

**Deliverable:** `triage-register.csv`.

## Lab 7 — Prioritize using context

**Tasks**

For each finding, record:
- Technical severity and scoring version.
- Exploitability and reachability.
- Internet/internal exposure.
- Asset criticality.
- Data sensitivity.
- Existing mitigations.
- Exploit intelligence where applicable (EPSS/KEV for CVEs).

Rank the findings and explain the top five decisions. Do not use CVSS alone.

**Deliverable:** risk-prioritization matrix.

## Lab 8 — False-positive management

**Tasks**

1. Select two sample false positives.
2. Document why each is not a vulnerability.
3. Define the narrowest suppression scope.
4. Record reviewer, date, and review/expiry date.
5. Explain what code or configuration change should trigger reassessment.

**Deliverable:** false-positive decision records.

## Lab 9 — Risk acceptance workflow

**Tasks**

1. Select a real or simulated confirmed finding that cannot be fixed immediately.
2. Describe residual risk and business impact.
3. Identify compensating controls.
4. Assign an accountable risk owner.
5. Set an expiry and review date.
6. Define monitoring and early-review triggers.

**Deliverable:** time-bounded risk-acceptance record. A training record must be clearly marked as simulated.

## Lab 10 — Remediation and retest

**Tasks**

1. Select a confirmed finding.
2. Create a remediation ticket.
3. Implement a fix in a training branch.
4. Run the original reproduction test.
5. Run the relevant scanner again.
6. Compare before/after results.
7. Close only if verification passes; otherwise reopen.

**Deliverable:** remediation ticket and retest evidence.

## Lab 11 — Build a triage dashboard

**Tasks**

Create a summary showing:
- Total findings by severity.
- Findings by source tool.
- Findings by disposition.
- Overdue items.
- Accepted risks nearing expiry.
- Mean time to triage and remediate.
- Reopened findings.

Use synthetic data. Explain why a low finding count alone does not prove better security.

**Deliverable:** dashboard or summary report.

## Lab 12 — CI/CD quality gate

**Tasks**

1. Define a blocking policy for new confirmed findings.
2. Normalize scanner reports.
3. Fail if required scanners fail or reports are missing.
4. Block confirmed critical/high findings according to policy.
5. Route non-blocking findings to a ticket queue.
6. Preserve raw and normalized reports as artifacts.
7. Test false-positive and accepted-risk exceptions.
8. Confirm the pipeline does not treat scanner failure as zero findings.

**Deliverable:** policy script, workflow, and test cases.

## Lab 13 — SLA and backlog management

**Tasks**

1. Define risk tiers and remediation targets.
2. Assign owners to all confirmed findings.
3. Identify overdue items.
4. Define escalation rules.
5. Review accepted-risk expiry dates.
6. Produce a backlog health summary.

**Deliverable:** remediation SLA matrix and backlog report.

## Lab 14 — Capstone: end-to-end finding management

Build a small finding-management workflow for a training application.

Required capabilities:
1. Ingest findings from at least three sources.
2. Preserve raw evidence.
3. Normalize and deduplicate records.
4. Validate findings with reproducible tests.
5. Classify disposition.
6. Prioritize with technical and business context.
7. Assign owners and due dates.
8. Document false positives and accepted risks.
9. Track remediation and retesting.
10. Generate metrics and dashboard.
11. Integrate a quality gate into CI.
12. Protect sensitive evidence and audit decisions.

**Deliverables:**
- Data schema.
- Sample raw and normalized findings.
- Deduplication rules.
- Triage register.
- Risk-prioritization matrix.
- False-positive and risk-acceptance records.
- CI policy and test results.
- Dashboard and final process document.

## Submission checklist

- [ ] Raw scanner reports preserved.
- [ ] Findings normalized without losing source metadata.
- [ ] Duplicates linked to canonical records.
- [ ] True positives validated.
- [ ] False-positive decisions evidence-based.
- [ ] Accepted risks approved and time-bounded.
- [ ] Unresolved findings have owners and next actions.
- [ ] Risk prioritization includes context beyond CVSS.
- [ ] Remediation SLAs defined.
- [ ] Fixes retested before closure.
- [ ] CI distinguishes scanner failure from clean results.
- [ ] Reports and evidence protect sensitive data.
