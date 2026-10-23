# Security Logging

Learn to record, protect, and monitor security events so suspicious activity can be detected and investigated.

## Learning objectives
- Distinguish security logging, audit trails, monitoring, and centralized log management.
- Identify events to record across applications, identity systems, hosts, networks, and cloud platforms.
- Design structured logs with timestamps, event names, outcomes, actors, targets, and correlation IDs.
- Avoid recording passwords, tokens, session cookies, private keys, and unnecessary sensitive data.
- Reduce log injection, tampering, unauthorized access, and storage exhaustion risks.

## Contents
- `examples.md` — Python, JSON, redaction, parsing, and command-line examples.
- `practical.md` — eight hands-on labs.
- `solutions.md` — sample answers and investigation guidance.
- `security-logging-checklist.md` — implementation and review checklist.
- `sample-security-events.jsonl` — synthetic events for practice.

## Security events to consider
- Authentication success/failure, MFA changes, lockouts, and suspicious login patterns.
- Authorization denials, privilege changes, role assignments, and administrative actions.
- Access to sensitive records, bulk exports, and security configuration changes.
- Input-validation failures, suspicious requests, application exceptions, and security-control failures.
- Session/token validation failures, key rotation, and certificate/TLS validation failures.
- Deployment events, account lifecycle changes, and log-collection failures.

Choose event coverage based on the threat model, operational requirements, and applicable legal obligations. Logging everything indiscriminately creates cost, privacy, and signal-to-noise problems.

## Structured event fields
Use a consistent schema containing fields such as `timestamp` (UTC), `severity`, `event`, `outcome`, `actor_id`, `target`, `source_ip` where justified, `service`, `environment`, `request_id`/`trace_id`, and a bounded safe `reason`. Never put secrets or raw sensitive payloads in these fields.

## Protect logs
- Use structured formats and correctly escape untrusted fields to prevent log injection.
- Restrict read/write/delete permissions and monitor log access.
- Forward important logs to a centralized collector over secure transport.
- Synchronize clocks and monitor ingestion gaps, tampering, and storage exhaustion.
- Define retention/deletion schedules according to policy and legal requirements.
- Test behavior when log storage or the collector is unavailable.

## References
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- OWASP Developer Guide: https://devguide.owasp.org/en/04-design/02-web-app-checklist/09-logging-monitoring/
- NIST SP 800-92: https://csrc.nist.gov/pubs/sp/800/92/final
- NIST Log Management project: https://csrc.nist.gov/projects/log-management
