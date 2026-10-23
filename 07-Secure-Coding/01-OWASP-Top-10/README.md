# 01 — OWASP Top 10

The **OWASP Top 10:2025** is an awareness document describing ten important categories of web application security risk. It is a starting point for secure coding, threat modeling, testing, and security improvement—not a complete security standard or a guarantee that an application is secure. See the [official OWASP Top 10:2025](https://owasp.org/Top10/) and [OWASP introduction](https://top10.owasp.org/2025/0x00_2025-Introduction/).

## Learning objectives

After completing this module, you should be able to:

- Name and explain the ten OWASP Top 10:2025 categories.
- Recognize common vulnerable design and coding patterns.
- Recommend preventive controls and verification tests.
- Integrate secure coding checks into a DevSecOps workflow.
- Distinguish a vulnerability category from a specific exploit or finding.
- Document risk, remediation, and evidence clearly.

## OWASP Top 10:2025 categories

| ID | Category | Typical risk examples |
|---|---|---|
| A01:2025 | Broken Access Control | IDOR/BOLA, privilege escalation, missing server-side authorization |
| A02:2025 | Security Misconfiguration | Debug mode, permissive CORS, default accounts, exposed management interfaces |
| A03:2025 | Software Supply Chain Failures | Compromised dependencies, build pipeline, package sources, or distribution artifacts |
| A04:2025 | Cryptographic Failures | Weak or misused cryptography, exposed secrets, inadequate protection of sensitive data |
| A05:2025 | Injection | SQL, command, template, or other interpreter injection |
| A06:2025 | Insecure Design | Missing security requirements, abuse-case controls, or safe business logic |
| A07:2025 | Authentication Failures | Weak session management, credential attacks, flawed authentication flows |
| A08:2025 | Software or Data Integrity Failures | Untrusted updates, unsafe deserialization, unverified integrity of artifacts or data |
| A09:2025 | Security Logging and Alerting Failures | Missing security events, ineffective alerts, logs that are incomplete or exposed |
| A10:2025 | Mishandling of Exceptional Conditions | Fail-open behavior, unsafe error handling, logic errors during abnormal conditions |

Category names and ordering follow the official 2025 edition. Older training material may use the 2021 categories, which differ—especially supply-chain risks, SSRF classification, and exceptional-condition handling.

## A01:2025 — Broken Access Control

**What it means:** The application does not correctly enforce which users or services can perform actions on which resources.

**Examples**
- A user changes `/orders/200` to `/orders/201` and sees another user's order.
- A regular user invokes an administrator endpoint directly.
- A multi-tenant API checks login status but not tenant ownership.

**Defenses**
- Enforce authorization server-side for every protected operation.
- Check object-level and tenant-level permissions, not only roles.
- Deny by default and use least privilege.
- Avoid trusting client-side checks or client-supplied role headers.

**Verification:** test horizontal and vertical privilege escalation, including direct API calls and alternate HTTP methods.

## A02:2025 — Security Misconfiguration

**What it means:** Application, cloud, server, framework, or deployment settings expose unnecessary capabilities or weaken protections.

**Examples**
- Production debug mode exposes stack traces.
- Default credentials remain enabled.
- A storage bucket or admin console is public unintentionally.
- CORS allows untrusted origins with sensitive credentialed requests.

**Defenses**
- Use hardened baseline configurations and configuration as code.
- Remove unused services, accounts, routes, and sample files.
- Separate development and production settings.
- Continuously check deployed configuration and access policies.

**Verification:** inspect deployment manifests, cloud policies, HTTP headers, exposed ports, and environment-specific settings.

## A03:2025 — Software Supply Chain Failures

**What it means:** Security failures arise in dependencies, package ecosystems, source control, build systems, CI/CD, artifact distribution, or update mechanisms.

**Examples**
- A dependency contains a known exploitable vulnerability.
- A build job downloads an unpinned tool from an untrusted source.
- A compromised CI token can publish a release.
- A production build consumes an unverified artifact.

**Defenses**
- Inventory dependencies and generate a software bill of materials (SBOM) where appropriate.
- Pin and verify dependencies; use trusted registries and lockfiles.
- Scan dependencies and prioritize findings by exploitability and exposure.
- Protect build identities, secrets, runners, branches, and release permissions.
- Verify artifact provenance and integrity; review and control updates.

**Verification:** dependency scanning, secret scanning, SBOM review, protected pipeline checks, and artifact-signature/provenance verification.

## A04:2025 — Cryptographic Failures

**What it means:** Sensitive data is not adequately protected because cryptography is absent, incorrectly selected, or incorrectly implemented.

**Examples**
- Credentials are sent over plaintext transport.
- Passwords are stored with a fast general-purpose hash instead of a password-hashing function.
- Encryption keys are hardcoded beside encrypted data.
- Sensitive fields are collected and retained unnecessarily.

**Defenses**
- Classify data and minimize collection and retention.
- Use correctly configured TLS for transport.
- Use established cryptographic libraries and approved algorithms.
- Store passwords with a suitable password-hashing algorithm and unique salts.
- Keep keys in a suitable key-management system with controlled access and lifecycle processes.

**Verification:** review transport settings, storage design, key access, password hashing, and data retention.

## A05:2025 — Injection

**What it means:** Untrusted data is interpreted as part of a command or query rather than handled as data.

**Examples**
- SQL is built by concatenating request parameters.
- User input reaches a shell command without safe handling.
- Untrusted text is interpreted as a server-side template.

**Defenses**
- Use parameterized queries and safe APIs.
- Avoid shell invocation where a library or direct API can do the job.
- Apply allowlist validation and strict schemas.
- Encode output for its exact context; validation and output encoding are not substitutes for parameterized database queries.

**Verification:** code review, static analysis, and controlled negative tests in an authorized lab.

## A06:2025 — Insecure Design

**What it means:** The design lacks necessary security controls, requirements, or safeguards for expected abuse cases.

**Examples**
- A password-reset flow has no abuse controls.
- A payment workflow can be replayed or applied twice.
- The application has no tenant-isolation requirements.
- Security controls are added only after implementation, without revisiting the architecture.

**Defenses**
- Threat-model important data flows and trust boundaries.
- Define abuse cases and security requirements before implementation.
- Use secure design patterns and defense in depth.
- Include rate limits, safe workflow states, and explicit failure behavior.

**Verification:** design review, abuse-case tests, architecture decision records, and acceptance criteria tied to risks.

## A07:2025 — Authentication Failures

**What it means:** The application cannot reliably establish or maintain a user's or service's identity.

**Examples**
- Weak credential recovery or unlimited login attempts.
- Session identifiers are not rotated after authentication.
- Tokens are accepted without validating issuer, audience, signature, or expiry.
- MFA recovery paths are weaker than normal authentication.

**Defenses**
- Use maintained authentication frameworks and trusted identity providers.
- Apply risk-appropriate MFA and abuse controls.
- Secure session cookies and rotate session identifiers when appropriate.
- Validate tokens fully and implement safe refresh-token handling.
- Avoid responses that unnecessarily reveal whether an account exists.

**Verification:** test expired and malformed tokens, session fixation, logout, recovery, MFA, and brute-force controls.

## A08:2025 — Software or Data Integrity Failures

**What it means:** The application does not adequately verify the integrity or trustworthiness of code, updates, serialized data, or critical inputs crossing trust boundaries.

**Examples**
- An update is installed without signature or provenance verification.
- An untrusted serialized object is deserialized unsafely.
- A workflow trusts a client-supplied price or approval status.
- A build artifact is replaced after security checks.

**Defenses**
- Verify integrity and authenticity of software artifacts.
- Use safe data formats and avoid unsafe deserialization of untrusted data.
- Recompute important business values on the server.
- Protect CI/CD permissions and release approvals.
- Validate data at trust boundaries.

**Verification:** tampered-artifact tests, integrity verification checks, code review, and negative tests for client-controlled fields.

## A09:2025 — Security Logging and Alerting Failures

**What it means:** Important security events are not recorded, monitored, or escalated in a way that supports timely investigation and response.

**Examples**
- Repeated authorization failures are not recorded.
- Logs omit actor, target, outcome, or timestamp.
- Alerts exist but have no owner or response process.
- Logs expose passwords, access tokens, or sensitive personal data.

**Defenses**
- Log authentication, authorization, privilege, administrative, and sensitive-data events.
- Use structured logs, timestamps, correlation IDs, and access controls.
- Redact secrets and avoid unnecessary sensitive payloads.
- Define alerts, severity, ownership, retention, and incident-response procedures.
- Protect logs from unauthorized access and tampering.

**Verification:** generate test events and confirm they are searchable, correlated, alerted on, and handled by the documented process.

## A10:2025 — Mishandling of Exceptional Conditions

**What it means:** Unexpected states, failures, or unusual input lead to unsafe behavior, information disclosure, logic errors, or fail-open outcomes.

**Examples**
- An authorization service times out and the application allows the request.
- An exception leaves a transaction partially applied.
- A retry duplicates a sensitive operation.
- Error responses reveal internal stack traces.

**Defenses**
- Define safe behavior for timeouts, exceptions, retries, and partial failure.
- Fail securely for protected operations when authorization cannot be confirmed.
- Use transactions and idempotency controls where appropriate.
- Return generic client errors while retaining protected diagnostic details.
- Test abnormal states, not only happy paths.

**Verification:** fault injection in a controlled environment, timeout and retry tests, transaction tests, and assertions about safe error responses.

## DevSecOps workflow

1. **Plan:** identify assets, security requirements, abuse cases, and relevant Top 10 categories.
2. **Code:** use secure frameworks, peer review, secrets scanning, and static analysis.
3. **Build:** scan dependencies, protect build credentials, and verify artifact integrity.
4. **Test:** add unit, integration, authorization, and security regression tests.
5. **Deploy:** apply hardened configuration and least-privilege identities.
6. **Operate:** collect security events, alert on meaningful patterns, patch dependencies, and respond to incidents.
7. **Improve:** use findings and incident lessons to update requirements and tests.

## Practical lab: secure a sample web API

Use a local intentionally vulnerable training application or your own test project.

1. Create a simple API with user and administrator roles and tenant-owned records.
2. Add a deliberate authorization weakness in a local-only lab.
3. Write a test proving the weakness, then implement server-side authorization.
4. Replace any string-built SQL with parameterized queries.
5. Add safe error handling, request limits, and structured security events.
6. Scan dependencies and configuration.
7. Re-run regression tests and record the evidence.

Do not test systems you do not own or have explicit permission to assess.

## Reporting a finding

For each finding, document:
- Title and affected component
- Applicable OWASP category and specific weakness
- Preconditions and safe reproduction steps
- Impact and affected data or trust boundary
- Evidence with secrets and personal data redacted
- Recommended fix and defense-in-depth measures
- Retest result and residual risk

## Further reading

- [OWASP Top 10:2025 — Official site](https://owasp.org/Top10/)
- [OWASP Top 10:2025 — Introduction and changes](https://top10.owasp.org/2025/0x00_2025-Introduction/)
- [OWASP Developer Guide — Top Ten](https://devguide.owasp.org/en/07-training-education/05-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)

## Completion criteria

You can explain all ten 2025 categories, identify likely root causes, recommend suitable preventive controls, write negative tests, and describe how a control will be verified in the development and deployment pipeline.
