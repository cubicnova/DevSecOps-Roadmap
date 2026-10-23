# Threat Modeling Fundamentals

Learn how to identify, assess, prioritize, and mitigate security threats during software design and throughout the Secure SDLC.

## Learning objectives

By the end of this module, you should be able to:

- Explain threat modeling and why it belongs early in the SDLC.
- Define scope, assets, actors, assumptions, entry points, trust boundaries, and data flows.
- Read and draft a simple data-flow diagram (DFD).
- Apply STRIDE to components and data flows.
- Use misuse cases and attack trees to explore attacker goals.
- Estimate and prioritize risk consistently.
- Convert threats into specific security requirements, tests, and tracked actions.
- Keep a threat model current as architecture and dependencies change.

## Suggested learning path

1. Learn the core terminology and four threat-modeling questions.
2. Decompose a simple application into components, flows, stores, and trust boundaries.
3. Apply STRIDE to the diagram.
4. Rate threats using a documented likelihood-and-impact scale.
5. Select mitigations and define validation tests.
6. Complete the exercises and compare your reasoning with `solutions.md`.

## Core questions

A practical threat-modeling session should answer:

1. **What are we building?** Define scope and create a system model.
2. **What can go wrong?** Identify plausible threats and abuse cases.
3. **What will we do about it?** Choose and assign mitigations or explicitly accept residual risk.
4. **Did we do a good enough job?** Validate assumptions, controls, and remaining risks.

## Key terminology

| Term | Meaning |
|---|---|
| Asset | Something valuable to protect, such as credentials, personal data, money, or service availability. |
| Threat | A potential event or action that can cause harm to an asset. |
| Vulnerability | A weakness that may be exploited by a threat. |
| Risk | The combination of likelihood and impact, assessed in context. |
| Actor | A person, service, or system that interacts with the application. |
| Entry point | An interface through which an actor can interact with the system. |
| Trust boundary | A point where control, identity, privilege, or trust changes. |
| Data flow | Data moving between actors, processes, or stores. |
| Mitigation | A design, process, or technical control that reduces risk. |
| Residual risk | Risk remaining after selected controls are applied. |

A threat is not the same thing as a vulnerability: “an attacker reads another user's invoice” is a threat scenario; “the API does not check invoice ownership” is a possible vulnerability.

## The STRIDE mnemonic

| Category | Security property at risk | Example prompt |
|---|---|---|
| Spoofing | Authentication | Can an attacker impersonate a user or service? |
| Tampering | Integrity | Can data or configuration be modified without authorization? |
| Repudiation | Accountability | Can an important action be denied because evidence is missing or unreliable? |
| Information disclosure | Confidentiality | Can private data be exposed to an unauthorized party? |
| Denial of service | Availability | Can a component be exhausted or made unavailable? |
| Elevation of privilege | Authorization | Can a user or component gain permissions beyond its intended role? |

STRIDE is a prompt for systematic thinking, not proof that every category is applicable to every component.

## Basic workflow

1. **Set scope:** state what is in scope, out of scope, assumptions, and security objectives.
2. **Identify assets and actors:** include legitimate users, administrators, services, third parties, and plausible malicious actors.
3. **Draw the system:** show processes, data stores, data flows, external entities, and trust boundaries.
4. **Identify threats:** use STRIDE, abuse cases, and attacker-goal questions.
5. **Assess risk:** consider likelihood, impact, exposure, existing controls, and uncertainty.
6. **Respond:** mitigate, eliminate the risky feature, transfer some responsibility where appropriate, or formally accept the risk.
7. **Validate:** define tests and evidence that demonstrate mitigations work.
8. **Maintain:** revisit the model after material changes, incidents, or new dependencies.

## Example: file-upload service

A simplified flow:

```text
[User / Browser]
       |
       | HTTPS: upload request
       v
+----------------------+     +----------------------+
| Web/API Application  |---->| Object Storage       |
| authentication,      |     | uploaded files       |
| validation, metadata |     +----------------------+
+----------------------+
       |
       | metadata query
       v
+----------------------+
| Application Database |
| owner, object key,    |
| status, audit record |
+----------------------+
```

Trust boundaries should be drawn around the public internet, the application environment, and any separately controlled storage or database service. This is an illustrative model; actual architecture may differ.

| Threat scenario | STRIDE | Example mitigation | Validation |
|---|---|---|---|
| A caller forges another user's identity | Spoofing / Elevation of privilege | Validate authentication server-side; never trust client-supplied user IDs | Tests with missing, invalid, and cross-user credentials |
| Uploaded content is modified or misclassified | Tampering | Validate content, calculate a hash where useful, and track scan status | Upload test corpus and verify status transitions |
| Private upload is served to another user | Information disclosure | Enforce object-level authorization on every download | Attempt cross-account access in an authorized test environment |
| Very large uploads exhaust resources | Denial of service | Enforce size, rate, concurrency, and storage quotas | Test limits with controlled test files |
| User denies uploading a file | Repudiation | Maintain access-controlled, tamper-resistant audit records | Verify events include actor, time, object ID, and outcome |
| Uploaded file is executed by the application server | Elevation of privilege / Tampering | Store uploads outside executable web paths; use safe serving headers and content handling | Verify storage and serving configuration |

## Risk prioritization

Use the team's approved risk method when one exists. A simple training scale is:

- Likelihood: 1 (unlikely) to 5 (very likely)
- Impact: 1 (minor) to 5 (critical)
- Initial score: likelihood × impact

Example: likelihood 4 × impact 5 = 20, which may be treated as high under a sample policy. Define score bands before using them; a numeric score is a prioritization aid, not an objective measurement. Account for exposure, existing controls, uncertainty, and business context.

## Useful deliverables

A small, useful threat-model package usually contains:

- Scope, assumptions, and security objectives
- Architecture or data-flow diagram
- Assets, actors, entry points, and trust boundaries
- Threat register with scenarios, affected components, and risk ratings
- Mitigations with owners and due dates
- Validation tests or evidence
- Decisions and accepted residual risks
- Review date and change triggers

## Tools and references

- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [OWASP Threat Modeling Project](https://owasp.org/www-project-threat-model/)
- [Microsoft Threat Modeling Tool — getting started](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-getting-started)
- [Microsoft SDL threat modeling](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
- [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/)

## Responsible practice

Use fictional systems or environments you own or are explicitly authorized to assess. Threat modeling is a design and risk-analysis activity; do not test production systems or third-party services without authorization.
