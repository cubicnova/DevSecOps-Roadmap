# Suggested Solutions and Review Notes

These are sample answers, not the only valid designs. Real diagrams should reflect the actual architecture.

## Lab 1 — Course portal
Possible external entities: learner browser, administrator browser, identity provider (if external), email provider, and learning-content provider (if external). Processes may include web/API service, authentication service, assignment service, and notification worker. Stores may include user database, course database, and assignment object storage.

Important flows: HTTPS page/API requests, authenticated identity assertions, assignment upload, database reads/writes, and email notification API calls. Mark the public Internet boundary and any third-party service boundary.

## Lab 2 — Login flow
A useful model includes browser → authentication API, authentication API ↔ user database, authentication API → browser for session establishment, and authentication API → security log store. The client-to-service flow crosses a trust boundary. Passwords and tokens should not be written to logs. Verify secure password hashing, rate limiting, secure session settings, and server-side authorization.

## Lab 3 — File upload
Keep uploaded content in quarantine until validation and scanning succeed. Use server-generated object identifiers, strict size limits, layered file validation, least-privilege scanning, and authorization checks on every download. Prevent public access to quarantine and avoid executing uploaded content. Consider archive expansion limits and malware scanning.

## Lab 4 — Payment integration
Model the user's browser redirect separately from server-to-provider traffic and provider-to-server callbacks. Verify callbacks using the provider's documented signature/authentication mechanism, validate amount/currency/order ID against server-side state, use unique event IDs or idempotency controls to handle replay/duplicates, and do not trust a browser-only success message as payment proof.

## Lab 5 — Queue and worker
Restrict queue producer/consumer permissions, use TLS and service identity, validate message schema, minimize payload fields, and implement idempotent processing. Apply bounded retries, dead-letter handling, rate/size limits, and monitoring. A worker should have only the permissions required for its task.

## Lab 6 — Flawed diagram
Possible omissions:
1. Data-flow direction.
2. Data types and sensitivity.
3. Protocols and encryption.
4. Authentication and authorization.
5. Trust boundaries.
6. External email provider as an entity.
7. Logging and monitoring.
8. Backups, caches, or queues if present.
9. Error and retry paths.
10. Administrative access.
11. Data retention and deletion.
12. Third-party credentials and secrets management.

## Lab 7 — Level 1 DFD
A valid submission has a clearly defined scope, 3–6 meaningful processes, relevant stores, external entities, directional and labeled flows, and unique flow IDs. STRIDE threats should point to specific diagram elements or flows rather than generic statements. Example: forged identity on a client-to-API flow (spoofing), unauthorized modification of an order event (tampering), or sensitive data exposed in logs (information disclosure).

## Lab 8 — Peer review
The review should record specific corrections, not only “looks good.” Examples include adding a missing external provider, identifying a trust-boundary crossing, labeling a flow with protocol/data type, or documenting an assumption about TLS termination. Record reviewer, date, diagram version, findings, owners, and follow-up status.

## Self-assessment rubric (20 points)
- Scope and system boundary: 0–3
- Correct DFD elements: 0–4
- Directional, labeled flows: 0–4
- Trust boundaries and external dependencies: 0–4
- Security/privacy considerations: 0–3
- Readability and maintainability: 0–2

Suggested interpretation: 17–20 strong; 13–16 revise a few details; 9–12 revisit flow coverage; below 9 rebuild from the use case and system boundary.
