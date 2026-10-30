# Data Flow Diagrams (DFDs) for Threat Modeling

## Overview
A Data Flow Diagram (DFD) is a simplified view of how information moves through a system. In security design, it helps teams identify components, data stores, external entities, communication paths, and trust boundaries before implementation.

DFDs are a foundation for threat modeling—not a proof that a system is secure. Keep diagrams accurate, scoped, readable, and updated as architecture changes.

## Learning objectives
By completing this module, you should be able to:
- Explain the purpose of a DFD in secure SDLC and threat modeling.
- Identify external entities, processes, data stores, data flows, and trust boundaries.
- Label flows with data type, protocol, direction, and security properties.
- Create context and Level 1 diagrams.
- Identify trust-boundary crossings and use a DFD to support STRIDE analysis.
- Review diagrams for omissions and stale assumptions.

## Core DFD elements
| Element | Purpose | Example |
|---|---|---|
| External entity | Actor or system outside the modeled system | Browser, payment provider, identity provider |
| Process | Component that receives, transforms, or sends data | Web app, API, authentication service |
| Data store | Data at rest | SQL database, object storage, message queue |
| Data flow | Data moving between elements | HTTPS request, SQL query, event message |
| Trust boundary | A change in trust or administrative/security control | Internet-to-app boundary, app-to-database zone |

Use a consistent notation across a project. Common DFD conventions use rectangles for external entities, rounded processes/circles for processes, open-ended or parallel-line symbols for data stores, arrows for flows, and dashed lines for trust boundaries. Teams may use other documented notation.

## Build a DFD step by step
1. **Define scope:** name the feature, system boundary, and use case.
2. **List actors and dependencies:** users, administrators, third-party services, and external systems.
3. **List processes:** services, APIs, jobs, functions, and gateways that transform data.
4. **List stores:** databases, caches, logs, queues, file storage, and backups relevant to the scope.
5. **Draw directional flows:** show what data moves, in which direction, and by what protocol.
6. **Mark trust boundaries:** identify transitions between different trust levels or administrative domains.
7. **Label flows:** include data classification, protocol, authentication, encryption, and validation where relevant.
8. **Review security assumptions:** identify where authorization, validation, rate limiting, monitoring, and data minimization are required.
9. **Threat model:** use STRIDE or another suitable method to assess components and flows.
10. **Maintain the model:** update it when architecture, dependencies, or data handling changes.

## Diagram levels
- **Context diagram:** one system process plus external entities and the major incoming/outgoing flows.
- **Level 1 DFD:** decomposes the system into major processes and data stores.
- **Level 2 DFD:** expands one process or flow when more detail is needed for a security decision.

Avoid making one enormous diagram. Use a high-level overview and smaller diagrams for important services or workflows.

## Flow-label checklist
For each important flow, record:
- Source and destination
- Direction and business purpose
- Data types and sensitivity
- Protocol and whether encryption is used
- Authentication and authorization expectations
- Input validation or output encoding
- Logging/monitoring expectations
- Any assumptions or unresolved questions

## Common mistakes
- Showing components but not the data moving between them.
- Omitting trust boundaries or third-party services.
- Treating internal traffic as automatically trusted.
- Leaving arrows unlabeled or direction ambiguous.
- Forgetting logs, backups, queues, temporary files, or object storage.
- Including too much implementation detail in a context diagram.
- Using a diagram that no longer matches production.
- Treating a DFD as a vulnerability scan or security guarantee.

## Tools
Use a diagramming tool, whiteboard, or text-based diagram language such as Mermaid. Pick a format the team can review and update in version control. Follow a single notation consistently.

## Suggested learning path
1. Read `examples.md`.
2. Complete the tasks in `practical.md`.
3. Attempt the questions before checking `solutions.md`.
4. Review `dfd-review-checklist.md` during a peer review.
5. Use `dfd-flow-inventory-template.csv` to document flow metadata.

## References
- OWASP Threat Modeling Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
- OWASP DevSecOps Guideline — Threat Modeling: https://owasp.github.io/DevSecOpsGuideline/2-Process/2-1-Design/2-1-1-Threat-modeling/
- Microsoft Secure by Design: https://www.microsoft.com/en-us/securityengineering/sdl/practices/secure-by-design
- Microsoft Learn — Create a threat model using foundational DFD elements: https://learn.microsoft.com/en-us/training/modules/tm-create-a-threat-model-using-foundational-data-flow-diagram-elements/
