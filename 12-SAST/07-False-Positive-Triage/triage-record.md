# SAST Alert Triage Record

> Use this record for one alert. Do not classify a finding as a false positive without evidence.

## Alert identification

- Alert ID:
- Scanner / query:
- Rule ID:
- Repository / branch:
- File and line:
- Date reviewed:
- Reviewer:

## Initial assessment

- Reported weakness:
- Severity:
- Query precision / confidence:
- Source:
- Sink:
- Data-flow path:

## Security analysis

- Is the input attacker-controlled? Why?
- Is the code reachable in the relevant deployment?
- What transformations occur?
- What validation, sanitization, or authorization is applied?
- Is the control appropriate for this sink and context?
- What evidence supports the conclusion?

## Classification

Choose one:

- [ ] True positive
- [ ] False positive
- [ ] Accepted risk
- [ ] Duplicate
- [ ] Inconclusive

## Decision and action

- Classification rationale:
- Remediation / dismissal / escalation:
- Regression test or evidence link:
- Rule improvement required:
- Owner:
- Approver (if risk acceptance):
- Review / expiry date (if applicable):

## Final verification

- [ ] Evidence reviewed by a second person where required
- [ ] Fix or dismissal recorded
- [ ] Scan rerun where applicable
- [ ] Ticket and audit record updated
