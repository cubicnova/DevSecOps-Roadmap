# DAST Scan Risk Matrix

Use this worksheet with the application owner before scanning.

| Activity | Possible side effect | Initial risk | Safeguard / approval |
|---|---|---|---|
| Passive traffic analysis | Sensitive data in reports | Low | Restrict report access |
| Traditional spider | Form submissions / workflow triggers | Medium | Review forms and disable state-changing actions |
| AJAX spider | UI-driven state changes | Medium | Use synthetic account and sandbox |
| Active scan | Data mutation / service impact | High | Isolated target and explicit approval |
| File upload fuzzing | Storage exhaustion / parser load | High | Dedicated disposable storage |
| Payment workflow | Real transaction | Critical | Provider sandbox; exclude production |
| Email/SMS action | External message delivery | High | Mail/SMS sink or disabled integration |
| Delete operation | Data loss | Critical | Exclude; use disposable test data only |

Risk ratings are starting points. Adjust them for the actual application, data, architecture, and environment.

## Monitoring signals
- HTTP 5xx and application error rate
- p95/p99 response latency
- CPU, memory, database and queue load
- Unexpected record creation/deletion
- Outbound email, SMS, payment, or webhook activity
- Requests to out-of-scope hosts
