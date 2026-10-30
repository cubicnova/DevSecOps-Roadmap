# Practical Labs: Data Flow Diagrams

## Lab 1 — Build a context diagram
**Scenario:** A course portal lets learners sign in, view lessons, submit assignments, and receive email notifications.

Tasks:
1. Define the system boundary.
2. Identify at least three external entities.
3. Identify major data flows and their direction.
4. Label each flow with its purpose and protocol.
5. Mark trust boundaries and list assumptions.

**Deliverable:** one context diagram and a short scope statement.

## Lab 2 — Decompose a login flow
Add the authentication API, user database, session/token mechanism, and security log store.

Tasks:
- Label credential, account lookup, and session flows.
- Show where passwords or tokens must never appear.
- Mark the trust boundary between public clients and server-side services.
- List three controls that should be verified.

## Lab 3 — Model a file upload
Model browser, API, quarantine store, scanning/validation process, approved store, and download endpoint.

Tasks:
- Distinguish untrusted upload from approved content.
- Identify who can read each store.
- Add flows for scan result and download.
- Consider oversized files, malicious content, path traversal, and direct access to quarantine.

## Lab 4 — Model a third-party payment integration
A shop sends an order amount and reference to a payment provider and receives a callback.

Tasks:
- Show browser redirect, server-to-provider request, and provider callback separately.
- Label each flow and its authentication mechanism.
- Identify which component is authoritative for payment status.
- List mitigations for forged callbacks, replay, and mismatched order amounts.

## Lab 5 — Add a message queue and worker
Model an API that publishes order events to a queue and a worker that processes them.

Tasks:
- Identify producer and consumer trust boundaries.
- Record sensitive fields in event payloads.
- Consider duplicate delivery, forged messages, queue flooding, and over-privileged workers.
- Suggest controls for authorization, schema validation, idempotency, and monitoring.

## Lab 6 — Review a flawed diagram
Use this intentionally incomplete description:
“Browser connects to application. Application connects to database and email.”

Find at least eight missing details. Consider:
- Data types and flow directions
- Authentication and authorization
- Protocols and encryption
- Trust boundaries
- External email provider
- Logging and backups
- Sensitive data
- Error paths and asynchronous jobs

## Lab 7 — Create a Level 1 DFD
Choose a small feature in a system you own or a fictional app. Break the main application into 3–6 processes and identify relevant data stores.

Tasks:
- Give each flow a unique ID (F1, F2, …).
- Add data classification and protocol.
- Record assumptions and unresolved questions.
- Identify three STRIDE threats using the DFD.

## Lab 8 — Peer review and change control
Exchange diagrams with a peer.

Review:
- Is scope clear?
- Are external entities, processes, stores, flows, and trust boundaries shown?
- Are arrows directional and labeled?
- Are third parties and privileged paths visible?
- Does the diagram match the current architecture?
- Are threat and mitigation notes linked to specific elements or flows?

**Deliverable:** annotated review checklist and a short change log.

## Submission checklist
- [ ] Diagram source is editable and stored with project documentation.
- [ ] Scope and assumptions are documented.
- [ ] Flows have unique IDs and useful labels.
- [ ] Trust boundaries are explicit.
- [ ] Sensitive data and external dependencies are identified.
- [ ] Threats and mitigations are traceable to the diagram.
- [ ] A reviewer has checked accuracy and completeness.

Only model systems you own or are authorized to assess. Use fictional or sanitized data in exercises.
