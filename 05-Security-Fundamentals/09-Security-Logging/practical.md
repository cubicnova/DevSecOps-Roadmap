# Practical Labs: Security Logging

Use local labs, synthetic identities, and authorized systems only.

## Lab 1 — Design an event schema
Create structured events for failed login, authorization denial, administrator role change, sensitive-report access, and collector failure. Include UTC timestamp, severity, event name, outcome, actor, target, service, request ID, and a safe reason. Mark fields that must never contain secrets.

## Lab 2 — Add logging to a toy application
Create a small Python program with synthetic authentication. Record success/failure, but never record passwords or submitted tokens. Test correct credentials, incorrect credentials, missing usernames, and malformed input.

## Lab 3 — Detect repeated failures
Parse `sample-security-events.jsonl`; count failed logins by source IP and distinct targeted accounts. Define a threshold and explain how you would tune it to reduce false positives.

## Lab 4 — Review log injection
Review an application that logs a user-supplied username by string concatenation. Explain how CR/LF characters can forge misleading entries. Replace the design with structured JSON logging, bounded values, and safe encoding. Test quotes, CR, LF, long strings, and Unicode in a local lab.

## Lab 5 — Sensitive-data audit
Classify `username`, `password`, `Authorization`, `session_cookie`, `source_ip`, `request_id`, `exception`, and `event` as keep, mask/minimize, remove, or restrict. Explain why avoiding collection is safer than relying only on redaction.

## Lab 6 — Design a central pipeline
Diagram sources → secure transport/agent → central collector → parsing/normalization → protected storage → alerting/SIEM → incident response. Include clock synchronization, access auditing, retention, and missing-source monitoring.

## Lab 7 — Test failure behavior
Write test cases for disk full, collector unavailable, invalid fields, log rotation, permission denied, high-volume bursts, and clock skew. Define expected behavior, detection, and alert ownership.

## Lab 8 — Mini investigation
Reconstruct failed logins, a successful login, a role change, sensitive-report access, and a collector outage from the sample events. State what is known, what is uncertain, and which additional sources could help.

## Completion checklist
- [ ] Can design structured security events.
- [ ] Know which security events to log.
- [ ] Avoid logging secrets and unnecessary personal data.
- [ ] Can explain log injection and structured encoding.
- [ ] Can query sample logs for suspicious patterns.
- [ ] Can describe collection, retention, access control, and failure monitoring.
