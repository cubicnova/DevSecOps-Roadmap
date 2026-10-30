# STRIDE Threat Model Review Checklist

## Scope and architecture
- [ ] Scope, assumptions, exclusions, and security objectives are documented.
- [ ] Assets, actors, processes, data stores, and data flows are identified.
- [ ] Trust boundaries are shown and justified.
- [ ] Sensitive data and authentication material are labeled on relevant flows.
- [ ] Third-party services and privileged components are included.

## STRIDE coverage
- [ ] Spoofing: identity claims, credentials, sessions, and service identities reviewed.
- [ ] Tampering: inputs, messages, stored data, configuration, and build artifacts reviewed.
- [ ] Repudiation: audit events, timestamps, log integrity, and accountability reviewed.
- [ ] Information Disclosure: authorization, data minimization, encryption, and error leakage reviewed.
- [ ] Denial of Service: limits, timeouts, quotas, dependency failure, and resource exhaustion reviewed.
- [ ] Elevation of Privilege: role checks, service permissions, privilege boundaries, and administrative paths reviewed.
- [ ] Each threat category is considered where relevant; non-applicability is explained.

## Threat quality
- [ ] Each threat describes an actor, precondition/weakness, action, affected component, and impact.
- [ ] Threats are linked to assets and trust boundaries.
- [ ] Existing controls and assumptions are recorded.
- [ ] Risk ratings use a documented method and explain uncertainty.
- [ ] Related threats are linked without hiding distinct impacts.

## Mitigation and verification
- [ ] Each actionable threat has a mitigation or documented risk decision.
- [ ] Controls are specific and proportionate to the threat.
- [ ] Verification evidence or a test is defined.
- [ ] An accountable owner and target date are assigned.
- [ ] Residual risk is documented and accepted by the authorized role where required.
- [ ] Detection and recovery controls are considered, not just prevention.

## Lifecycle
- [ ] Threat model is reviewed by engineering and security stakeholders.
- [ ] Findings become tracked work items.
- [ ] Important threats are addressed before relevant release gates.
- [ ] Architecture, dependencies, and trust-boundary changes trigger review.
- [ ] Model and mitigation status are updated after testing and incidents.
