# CVSS and Risk Rating Checklist

## Finding validation

- [ ] Confirm the affected asset, product, version, and configuration.
- [ ] Validate that the finding is reproducible or supported by credible evidence.
- [ ] Record the vulnerability identifier and advisory/source.
- [ ] Record the exact CVSS version, score type, score, severity, and vector.
- [ ] Do not invent a score when none is available.

## Threat and exposure

- [ ] Is the asset internet-facing, partner-facing, internal, or isolated?
- [ ] Is the vulnerable service enabled and reachable?
- [ ] Is exploit code available?
- [ ] Is exploitation reported or confirmed in the relevant environment?
- [ ] Are privileges or user interaction required?
- [ ] Are compensating controls tested and effective?
- [ ] Are there dependencies or paths to other systems?

## Business impact

- [ ] How critical is the affected asset or business process?
- [ ] Does it handle sensitive, regulated, or customer data?
- [ ] Could exploitation affect confidentiality, integrity, availability, or safety?
- [ ] What is the expected downtime, recovery effort, or financial/operational impact?
- [ ] Are downstream systems or third parties affected?

## Risk rating and prioritization

- [ ] Use the organization's approved risk methodology and thresholds.
- [ ] Keep CVSS and organizational risk fields separate.
- [ ] Document likelihood and impact evidence.
- [ ] Record assumptions, unknowns, and confidence.
- [ ] Explain any priority that differs from a CVSS-only ordering.
- [ ] Set an owner, target date, mitigation, and escalation path.
- [ ] Apply required remediation SLAs and exception approvals.

## Closure and reassessment

- [ ] Retest the fix or validate the mitigation.
- [ ] Verify affected versions and exposure.
- [ ] Record evidence and closure date.
- [ ] Reassess if exploit activity, asset importance, or deployment context changes.
- [ ] Give every exception an accountable risk owner and expiry date.
