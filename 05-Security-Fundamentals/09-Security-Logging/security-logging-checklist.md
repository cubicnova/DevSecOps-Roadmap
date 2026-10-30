# Security Logging Checklist

## Event coverage
- [ ] Authentication successes/failures and MFA changes are recorded.
- [ ] Authorization failures and privilege changes are recorded.
- [ ] Administrative and security configuration changes are recorded.
- [ ] Sensitive-data access and bulk exports are logged where justified.
- [ ] Validation failures, security exceptions, and relevant system failures are recorded.
- [ ] Session/token validation failures and key/certificate events are recorded as appropriate.
- [ ] Logging configuration changes and collector failures are monitored.

## Event quality
- [ ] Use structured events, stable schemas, and consistent event names.
- [ ] Include UTC timestamp, severity, source/service, outcome, and correlation ID.
- [ ] Include actor and target context where relevant.
- [ ] Bound field lengths and validate untrusted data.
- [ ] Synchronize clocks and monitor time drift.
- [ ] Preserve investigative context without excessive data collection.

## Privacy and secrets
- [ ] Never log passwords, OTPs, private keys, bearer tokens, or session cookies.
- [ ] Avoid full request/response bodies by default.
- [ ] Minimize sensitive personal and payment data.
- [ ] Sanitize exception messages and database errors.
- [ ] Define retention/deletion rules according to policy and law.

## Integrity and access
- [ ] Restrict read/write/configuration/delete permissions.
- [ ] Audit log access and monitor unusual access.
- [ ] Forward important logs securely to a central collector.
- [ ] Protect stored logs from unauthorized modification/deletion.
- [ ] Test CR/LF, delimiter injection, and log-viewer behavior.
- [ ] Configure rotation, quotas, backups, and capacity alerts.

## Monitoring and response
- [ ] Define use cases, thresholds, and alert ownership.
- [ ] Correlate identity, application, host, network, and cloud events.
- [ ] Alert when expected sources stop reporting or ingestion falls behind.
- [ ] Test alert routing and incident-response handoffs.
- [ ] Tune detections against baselines without hiding real incidents.
- [ ] Test storage/network/collector failure behavior.
- [ ] Document evidence gaps and uncertainty during investigations.

## Release and review
- [ ] Logging is enabled in security testing and production-like environments.
- [ ] Tests cover sensitive-data leakage and log injection.
- [ ] Schema changes are versioned and reviewed.
- [ ] Unauthorized users cannot silently disable logging.
- [ ] Retention, access, and alert configurations are reviewed periodically.
