# STRIDE Threat Modeling

STRIDE is a structured way to identify potential security threats during system design and throughout the Secure Software Development Lifecycle (SDLC). It prompts a team to consider six categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.

## Learning objectives

- Explain each STRIDE category and the security property it threatens.
- Identify system assets, actors, processes, data stores, data flows, and trust boundaries.
- Apply STRIDE to a data-flow diagram (DFD) and realistic use cases.
- Describe threats with a concrete scenario, impact, and affected component.
- Select proportionate mitigations and define how to verify them.
- Record threat owners, priorities, status, and residual risk.

## Contents

- `examples.md` — worked STRIDE examples and threat-to-mitigation mappings.
- `practical.md` — guided threat-modeling labs.
- `solutions.md` — sample answers and reasoning.
- `stride-threat-register.csv` — reusable threat register template with example rows.
- `stride-review-checklist.md` — DFD, threat discovery, mitigation, and review checklist.

## The six STRIDE categories

| Category | Security property | Prompt |
|---|---|---|
| **S — Spoofing** | Authentication | Can an attacker impersonate a user, service, or system? |
| **T — Tampering** | Integrity | Can data, messages, configuration, or code be changed without authorization? |
| **R — Repudiation** | Accountability / non-repudiation | Could an actor deny an action because evidence is missing or unreliable? |
| **I — Information Disclosure** | Confidentiality | Could sensitive information reach an unauthorized party? |
| **D — Denial of Service** | Availability | Could a component or dependency be overwhelmed or made unavailable? |
| **E — Elevation of Privilege** | Authorization | Could an actor gain permissions beyond those intended? |

STRIDE is a set of prompts, not a guarantee that every threat has been found. Use it with domain knowledge, abuse cases, attack paths, and review by people who understand the system.

## A practical workflow

1. **Define scope:** system, feature, users, and exclusions.
2. **Identify assets:** data, credentials, services, and business-critical functions.
3. **Draw a data-flow diagram:** external entities, processes, data stores, flows, and trust boundaries.
4. **Enumerate threats:** consider all six STRIDE categories for relevant elements and interactions.
5. **Describe scenarios:** attacker, preconditions, action, weakness, impact, and evidence.
6. **Rate risk:** use your organization's approved likelihood/impact method; document assumptions.
7. **Choose mitigations:** preventive, detective, and recovery controls as appropriate.
8. **Verify:** assign tests, evidence, owners, and due dates.
9. **Revisit:** update the model when architecture, data flows, dependencies, or threats change.

## Data-flow diagram elements

- **External entity:** user, partner, browser, or third-party service.
- **Process:** API, worker, authentication service, or business application.
- **Data store:** database, queue, object storage, cache, or log store.
- **Data flow:** data moving between entities, processes, and stores.
- **Trust boundary:** a change in trust or control, such as internet-to-service, service-to-database, or tenant-to-tenant.

A trust boundary is a useful prompt for analysis, not an automatic vulnerability.

## Threat statement pattern

> Because [weakness or assumption], [threat actor] could [action] against [component/data], causing [security/business impact]. Mitigate by [control] and verify with [test/evidence].

## References

- Microsoft Secure by Design / threat modeling: https://www.microsoft.com/en-us/securityengineering/sdl/practices/secure-by-design
- Microsoft Threat Modeling Tool getting started: https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-getting-started
- OWASP Threat Modeling Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
- OWASP DevSecOps Guideline — Threat Modeling: https://owasp.github.io/DevSecOpsGuideline/2-Process/2-1-Design/2-1-1-Threat-modeling/
