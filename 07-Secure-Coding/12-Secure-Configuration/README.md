# 12 — Secure Configuration

A practical learning module for configuring applications, operating systems, containers, cloud services, and deployment pipelines securely.

## Learning objectives

By completing this module, you should be able to:

- Explain how insecure defaults, unnecessary services, exposed administration interfaces, and configuration drift create risk.
- Separate development, test, staging, and production configuration.
- Keep credentials and cryptographic keys out of source control, images, logs, and error messages.
- Apply least privilege to service accounts, file permissions, network access, and cloud identities.
- Establish and validate secure baselines for applications, hosts, containers, and infrastructure.
- Review configuration changes, detect drift, and document exceptions.

## Core principles

1. **Secure defaults:** deny access unless it is explicitly required.
2. **Least functionality:** disable unused services, endpoints, modules, ports, and accounts.
3. **Least privilege:** grant each identity only the access required for its task.
4. **Environment separation:** use distinct identities, secrets, data, and permissions per environment.
5. **Secrets management:** inject secrets at runtime from an approved secret store; never commit real secrets.
6. **Defense in depth:** combine application controls, host hardening, network boundaries, monitoring, and deployment safeguards.
7. **Repeatability:** use version-controlled, reviewed configuration and automated checks where practical.
8. **Verifiability:** test the effective runtime configuration, not just the intended file contents.

## Configuration review workflow

1. Identify the asset, owner, environment, and security requirements.
2. Inventory active services, ports, accounts, dependencies, APIs, and configuration sources.
3. Compare current settings with an approved baseline and vendor security guidance.
4. Identify risky defaults, unused features, weak permissions, public exposure, and hard-coded secrets.
5. Assess likelihood, impact, exposure, and compensating controls.
6. Make a minimal, reviewed change with a rollback plan.
7. Validate functionality and security after deployment.
8. Record evidence, exceptions, owners, and review dates.
9. Monitor for drift and re-review after significant changes.

## Common risk areas

| Area | Examples of insecure configuration | Safer direction |
|---|---|---|
| Application | Debug mode in production; verbose stack traces | Disable debug features; return generic errors and log details securely |
| Secrets | Passwords in Git, Dockerfile, or logs | Use a secret manager or protected runtime injection |
| Network | Public admin panel; broad inbound rules | Private access, allowlists, least-privilege rules |
| Identity | Shared admin account; wildcard permissions | Individual identities, scoped roles, MFA for privileged access |
| Host | Default accounts, unused services, weak permissions | Hardened baseline, remove unused components, audit access |
| Containers | Running as root; privileged mode; mutable tags | Non-root user, minimal capabilities, pinned/verified images |
| TLS | Plain HTTP for sensitive traffic; obsolete protocols | Enforce HTTPS/TLS with approved protocol and certificate settings |
| Cloud storage | Public bucket/container by default | Block public access unless explicitly approved |
| Logging | Secrets or personal data in logs | Redaction, access controls, retention policy |
| CI/CD | Untrusted pull request gets production secrets | Isolate untrusted jobs; short-lived, scoped credentials |

## Practical lab setup

Use a local disposable VM or container and intentionally vulnerable sample configuration. Do not test against systems you do not own or have explicit permission to assess.

Suggested tools:
- Git and code review
- Docker or Podman
- A YAML/JSON linter
- `grep` or a secret-scanning tool
- `ss` / `systemctl` on a Linux lab host
- Infrastructure-as-code validation tools where applicable

## Suggested exercises

1. Review an application configuration for debug mode, wildcard CORS, weak cookies, and exposed management routes.
2. Find and remove a fake secret from a sample repository; rotate it if it had ever been real.
3. Review a container build for root execution, unnecessary packages, and embedded credentials.
4. Draft a least-privilege firewall policy for a web application and database.
5. Create a configuration checklist and record evidence for each control.
6. Simulate configuration drift and document how it would be detected and corrected.

## Completion criteria

You can explain the risk, identify the affected setting, recommend a least-privilege correction, validate the result, and record evidence plus any accepted residual risk.

## References

- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- OWASP Application Security Verification Standard: https://owasp.org/www-project-application-security-verification-standard/
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks
- NIST National Checklist Program: https://ncp.nist.gov/
- Docker security: https://docs.docker.com/engine/security/
