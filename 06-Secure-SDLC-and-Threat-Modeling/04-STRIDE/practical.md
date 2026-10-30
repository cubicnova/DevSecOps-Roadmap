# Practical Labs: STRIDE Threat Modeling

Work with fictional systems or systems you are authorized to assess. The goal is design analysis and defensive mitigation, not exploitation of real targets.

## Lab 1 — Learn the six categories

For each scenario, choose one primary STRIDE category and explain why:
1. A user changes a request field to alter an invoice amount.
2. An API accepts a forged identity header.
3. A public endpoint can trigger unlimited expensive jobs.
4. An admin action has no reliable audit trail.
5. An endpoint returns another customer's record.
6. A normal user invokes a privileged admin operation.

Some scenarios may fit more than one category; record the primary category and any secondary category with rationale.

## Lab 2 — Draw a data-flow diagram

Model a web application with:
- Browser/customer.
- Public web/API service.
- Identity provider.
- Application database.
- Central logging service.

Show data flows and trust boundaries. Label whether flows carry credentials, tokens, personal data, or audit events. You may use a diagramming tool or a text diagram.

**Deliverable:** `data-flow-diagram.md` or an image exported from your diagramming tool.

## Lab 3 — STRIDE per component

For each DFD element and flow, ask which STRIDE categories apply. Record at least eight concrete threat scenarios. Do not force a category where it does not make sense; explain “not applicable” decisions.

## Lab 4 — Build a threat register

Use `stride-threat-register.csv`. Add at least eight threats with:
- ID, element/flow, category, scenario, impact, existing controls.
- Likelihood/impact rating using a defined local scale.
- Proposed mitigation, owner, verification evidence, status, and residual risk.

## Lab 5 — Mitigation quality review

For three threats, propose:
- One preventive control.
- One detective control.
- One recovery or resilience control, if applicable.
- A test or evidence item for each.

Explain why a control reduces risk and what it does not address.

## Lab 6 — Threat modeling an upload feature

A web application accepts documents, stores them in object storage, and queues them for background processing. Apply all six STRIDE categories to relevant elements and flows. Consider identity, file integrity, auditability, confidentiality, resource exhaustion, and worker permissions.

## Lab 7 — Challenge assumptions

List five assumptions in your model, such as “the identity provider is always available” or “internal traffic is trustworthy.” For each, explain what happens if it is false and identify a control or follow-up question.

## Lab 8 — Review and update

Pretend the system adds a third-party payment provider or a new administrator workflow. Identify new trust boundaries and update the threat register. Record the reason for each change and who must approve residual risk.

## Deliverables
- Data-flow diagram.
- Threat register with at least eight entries.
- Mitigation and verification plan.
- Short assumptions and residual-risk summary.

## Completion checklist
- [ ] I can explain all six STRIDE categories.
- [ ] I can identify DFD elements and trust boundaries.
- [ ] Threats describe concrete attack scenarios and impacts.
- [ ] Mitigations are linked to threats and have verification evidence.
- [ ] Owners, priorities, assumptions, and residual risks are recorded.
- [ ] The model is updated when the design changes.
