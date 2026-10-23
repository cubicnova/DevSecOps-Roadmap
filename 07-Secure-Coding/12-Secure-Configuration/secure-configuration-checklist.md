# Secure Configuration Review Checklist

Use this checklist during design review, deployment review, and periodic configuration audits.

## Governance and inventory
- [ ] Asset, service owner, environment, and data classification are recorded.
- [ ] A supported platform version and approved baseline are defined.
- [ ] Configuration changes are reviewed, tracked, and attributable.
- [ ] Exceptions have a rationale, approver, compensating controls, and expiry/review date.
- [ ] Drift detection and periodic reassessment are planned.

## Application
- [ ] Debug mode, development routes, sample accounts, and test endpoints are disabled in production.
- [ ] Error responses do not reveal stack traces, secrets, file paths, or internal topology.
- [ ] Host allowlists and CORS origins are explicit and justified.
- [ ] Authentication, authorization, session, and CSRF settings match the application threat model.
- [ ] Security headers and TLS settings are reviewed for the deployment.
- [ ] Upload limits, request sizes, timeouts, and rate limits are appropriate.

## Secrets and cryptography
- [ ] No real credentials, tokens, private keys, or connection strings are committed to source control.
- [ ] Secrets are provided through an approved secret-management mechanism.
- [ ] Secret access is least-privilege and auditable.
- [ ] Rotation, revocation, and emergency response procedures exist.
- [ ] Sensitive values are excluded or redacted from logs, traces, and error reports.
- [ ] Cryptographic algorithms, key sizes, storage, and rotation follow approved guidance.

## Host and operating system
- [ ] Supported packages and security updates are maintained.
- [ ] Unneeded services, accounts, packages, and listening ports are removed or disabled.
- [ ] Privileged access is restricted, attributable, and protected with MFA where supported.
- [ ] SSH/remote administration is limited to approved paths and settings.
- [ ] File and directory permissions follow least privilege.
- [ ] Time synchronization, audit logging, and log protection are configured.

## Containers and orchestration
- [ ] Images come from trusted sources and are pinned/verified according to policy.
- [ ] Containers run as non-root where feasible.
- [ ] Privileged mode and unnecessary capabilities are disabled.
- [ ] Secrets are not baked into image layers.
- [ ] Unneeded ports and host mounts are not exposed.
- [ ] Read-only filesystems, resource limits, and security profiles are considered.
- [ ] Kubernetes or orchestration RBAC, network policies, pod security, and service-account tokens are reviewed.

## Cloud and network
- [ ] Public access is disabled by default for storage, databases, and management services.
- [ ] Network rules permit only required source/destination/port combinations.
- [ ] Workload identities and IAM roles are scoped to the required actions and resources.
- [ ] Root/owner accounts are not used for routine workloads.
- [ ] Administrative interfaces use private or identity-aware access.
- [ ] Encryption at rest and in transit is enabled where required.
- [ ] Cloud audit logs and configuration findings are monitored.

## CI/CD and deployment
- [ ] Untrusted code cannot access production secrets or privileged deployment credentials.
- [ ] Build and deployment identities are short-lived and scoped where possible.
- [ ] Configuration is validated before release.
- [ ] Production changes require appropriate approval and audit trail.
- [ ] Rollback and recovery procedures are tested.
- [ ] Post-deployment checks confirm effective runtime settings.

## Evidence and closure
- [ ] Each finding has evidence, severity, owner, due date, and remediation guidance.
- [ ] Fixes are retested and recorded.
- [ ] Residual risk is explicitly accepted by an authorized owner.
