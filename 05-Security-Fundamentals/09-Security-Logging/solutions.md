# Solutions and Reference Answers

Real logging policies should be tailored to the application, threat model, privacy obligations, and operational environment.

## Lab 1 — Schema example
```json
{
  "timestamp": "2026-01-15T12:00:00Z",
  "severity": "WARN",
  "event": "auth.login_failed",
  "outcome": "failure",
  "actor_id": "user-demo-17",
  "target": "web-portal",
  "source_ip": "192.0.2.25",
  "service": "identity-api",
  "request_id": "req-demo-001",
  "reason": "invalid_credentials"
}
```
All values are synthetic. Do not include passwords, one-time codes, bearer tokens, or raw authorization headers.

## Lab 2 — Toy application
Log event name, outcome, synthetic account identifier, timestamp, and request ID. Never log submitted passwords or tokens. Handle malformed inputs safely and avoid writing unbounded raw input to logs.

## Lab 3 — Detection
Count total failures and distinct accounts per source in a time window. Also consider many sources targeting one account. Tune thresholds against baseline behavior and correlate with successful logins and MFA events.

## Lab 4 — Log injection
A naive line-oriented log can treat embedded CR/LF as extra records. Use structured serialization, fixed event names, validated fields, bounded values, and safe encoding. Test the actual log viewer. Parameterized messages alone may not prevent injection.

## Lab 5 — Sensitive-data treatment
- `username`: use a stable internal ID or minimized account reference where justified.
- `password`: never log.
- `Authorization`: never log raw header/token.
- `session_cookie`: never log raw value; use an approved correlation method only if necessary.
- `source_ip`: collect only when justified and consistent with privacy/retention policy.
- `request_id`: retain for correlation.
- `exception`: retain bounded diagnostic details after secret/sensitive-data review.
- `event`: retain a stable controlled event name.

## Lab 6 — Central pipeline
`Sources → Secure transport/agent → Central collector → Parse/normalize → Protected storage → Detection/alerting → Incident response`

Use authenticated agents, encrypted transport, role-based access, audit trails for log access, synchronized clocks, retention policies, capacity monitoring, and alerts when sources stop reporting.

## Lab 7 — Failure behavior
- Disk full: alert, rotate/manage capacity, and follow documented behavior for security-critical audit operations.
- Collector unavailable: bounded local buffering/retries where appropriate; alert on prolonged gaps.
- Invalid fields: reject or safely normalize and record validation failure without raw sensitive content.
- Rotation: verify no event loss/duplication and restrictive permissions.
- Permission denied: alert operators without exposing secrets to end users.
- Event burst: apply careful rate/capacity controls and monitor dropped events.
- Clock skew: synchronize clocks and monitor drift.

## Lab 8 — Investigation
Build a UTC timeline using correlation IDs. Review source/account context, the successful login after failures, who performed the role change, and whether report access was authorized. A collector outage means the timeline may be incomplete; consult identity-provider, endpoint, application, and cloud audit records.

## Common mistakes
- Logging credentials or entire request bodies.
- Treating every failed login as a confirmed attack.
- Inconsistent event names and timestamps.
- Excessively broad access to log data.
- Keeping logs forever or deleting them too early.
- Ignoring collector outages, parsing failures, and missing events.
