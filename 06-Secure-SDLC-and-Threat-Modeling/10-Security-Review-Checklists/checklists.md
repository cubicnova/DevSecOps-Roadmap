# Security Review Checklists

Use `PASS`, `FAIL`, `N/A`, or `NEEDS-REVIEW` for each item. Add evidence and an owner for failures or unresolved items. These checklists are a practical baseline, not a guarantee of security or a substitute for requirements applicable to your environment.

## 1. Review preparation and architecture
- [ ] Scope, feature, and expected behavior are clear.
- [ ] Diff and affected components have been identified.
- [ ] Relevant threat model, data-flow diagram, and prior findings were reviewed.
- [ ] New entry points, trust boundaries, integrations, and data stores are identified.
- [ ] Sensitive assets and security requirements are documented.
- [ ] Review depth is appropriate for the risk of the change.
- [ ] Reviewers know how to escalate critical concerns.

## 2. Input validation and injection
- [ ] All external input is validated server-side for type, format, length, and allowed values.
- [ ] Validation is performed at trust boundaries; client-side validation is not the only control.
- [ ] Database queries use parameterization or safe ORM APIs.
- [ ] Shell commands do not concatenate untrusted input; safer APIs are preferred.
- [ ] Output is encoded for its HTML, JavaScript, URL, or other output context.
- [ ] File paths are constrained to intended directories and canonicalized safely.
- [ ] File uploads enforce size limits, content validation, safe filenames, and safe storage.
- [ ] URL fetching features defend against SSRF and restrict destinations as appropriate.
- [ ] XML parsers and deserializers use safe settings for untrusted content.
- [ ] Errors do not reveal SQL, stack traces, internal paths, or secrets.

## 3. Authentication and session management
- [ ] Authentication is required for protected functionality.
- [ ] Passwords are stored with an appropriate password-hashing algorithm and unique salts.
- [ ] Password reset and account recovery flows are time-limited and resistant to abuse.
- [ ] MFA is applied to privileged or high-risk access where required.
- [ ] Login and recovery endpoints have abuse protections and monitoring.
- [ ] Session IDs and tokens are generated and handled securely.
- [ ] Sessions are invalidated on logout and relevant security events.
- [ ] Cookie-based sessions use appropriate `Secure`, `HttpOnly`, and `SameSite` settings.
- [ ] Sensitive actions require re-authentication or step-up verification when appropriate.
- [ ] Tokens, passwords, and recovery codes are not exposed in URLs, logs, or analytics.

## 4. Authorization and access control
- [ ] Access decisions are enforced server-side and default to deny.
- [ ] Every sensitive action checks the user's permissions.
- [ ] Object-level authorization prevents IDOR/BOLA.
- [ ] Function-level authorization protects administrative and privileged operations.
- [ ] Role and tenant membership changes cannot be self-assigned by untrusted users.
- [ ] Authorization is checked on direct API requests, not only in the UI.
- [ ] Resource ownership and tenant boundaries are enforced consistently.
- [ ] Privilege escalation and horizontal access paths are tested.
- [ ] Service identities use least privilege.
- [ ] Negative tests prove unauthorized requests are rejected.

## 5. API and business logic
- [ ] API schemas and types are validated.
- [ ] Rate limits, quotas, pagination limits, and timeouts are appropriate.
- [ ] Mass assignment and over-posting cannot change protected fields.
- [ ] Workflow state transitions are checked on the server.
- [ ] Payment, approval, and account-change operations validate authoritative server-side state.
- [ ] Sensitive operations are protected against replay or duplicate processing where needed.
- [ ] Concurrent requests cannot bypass limits or corrupt state.
- [ ] CORS allows only intended origins and methods.
- [ ] Webhooks validate provider authenticity and handle replay/duplicates safely.
- [ ] Error responses are consistent and do not leak implementation details.

## 6. Sensitive data and cryptography
- [ ] Data classification and minimization requirements are followed.
- [ ] Sensitive data is encrypted in transit using appropriately configured TLS.
- [ ] At-rest protection is applied where required by the data and threat model.
- [ ] Cryptographic operations use vetted libraries and maintained algorithms.
- [ ] Keys and secrets are stored outside source code and rotated according to policy.
- [ ] Randomness for tokens and security-sensitive values is cryptographically secure.
- [ ] Certificate and hostname validation are enabled.
- [ ] Secrets, credentials, payment data, and unnecessary personal data are not logged.
- [ ] Retention, deletion, backup, and export behavior are considered.
- [ ] Cryptographic exceptions or legacy algorithms are documented and approved.

## 7. Errors, logging, and monitoring
- [ ] Failure paths do not disclose secrets or internal implementation details.
- [ ] Security-relevant authentication and authorization events are logged.
- [ ] Sensitive actions have suitable audit trails.
- [ ] Logs are access-controlled and protected against tampering.
- [ ] Log fields are sanitized to reduce injection and parsing risks.
- [ ] Passwords, session tokens, access tokens, and keys are excluded from logs.
- [ ] Alerts exist for critical or suspicious events where appropriate.
- [ ] Logging failures do not create unsafe fail-open behavior for critical controls.
- [ ] Incident responders can identify relevant events and correlation IDs.

## 8. Dependencies and software supply chain
- [ ] New dependencies are necessary, correctly named, and obtained from trusted sources.
- [ ] Lockfiles and version changes are reviewed.
- [ ] Dependency scanning is performed and findings are triaged.
- [ ] Known exploitable vulnerabilities are remediated or formally handled.
- [ ] Package lifecycle scripts and build-time behavior are considered for high-risk dependencies.
- [ ] Dependency licenses and provenance meet project requirements.
- [ ] Build artifacts and release packages come from the expected pipeline.
- [ ] Secrets are not included in packages, images, or source maps.
- [ ] Unsupported dependencies have an upgrade or isolation plan.

## 9. Cloud, containers, and infrastructure as code
- [ ] Resources are not publicly exposed unless explicitly required.
- [ ] IAM roles and service accounts follow least privilege.
- [ ] Network rules limit ingress and egress to required paths.
- [ ] Secrets use an approved secret manager or equivalent protected mechanism.
- [ ] Storage permissions, encryption, and retention are appropriate.
- [ ] Container images use trusted bases and are scanned.
- [ ] Containers avoid privileged mode and unnecessary capabilities.
- [ ] Images run as non-root where feasible and appropriate.
- [ ] Kubernetes RBAC, network policies, and pod security settings are reviewed where applicable.
- [ ] Terraform or other IaC changes are reviewed, scanned, and planned before apply.
- [ ] Environment separation and production access controls are maintained.
- [ ] Backup and recovery protections are addressed for critical data.

## 10. CI/CD and release security
- [ ] Workflow permissions are minimal and scoped.
- [ ] Secrets are not exposed to untrusted pull-request code or printed in logs.
- [ ] Third-party actions/plugins are pinned and reviewed according to policy.
- [ ] Branch protection and required reviews are enabled for protected branches.
- [ ] Build and deployment identities use short-lived credentials where possible.
- [ ] Build steps do not execute untrusted scripts with production privileges.
- [ ] SAST, dependency scanning, secret scanning, and relevant tests run in the pipeline.
- [ ] Security gate failures cannot be silently ignored.
- [ ] Artifacts are traceable to reviewed source and trusted builds.
- [ ] Rollback and incident response steps are available.

## 11. Release readiness
- [ ] Relevant security requirements have evidence of verification.
- [ ] High-severity findings are resolved or handled under formal policy.
- [ ] Exceptions have a named authorized approver and expiry/review date.
- [ ] Threat model and DFD are updated for material changes.
- [ ] Monitoring, alerting, and incident response are ready.
- [ ] Operational owners understand new security behavior and limitations.
- [ ] Retest evidence is attached to closed findings.
- [ ] Residual risk is documented and accepted by the correct authority.
