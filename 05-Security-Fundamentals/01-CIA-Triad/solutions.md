# CIA Triad - Suggested Solutions

These are example answers, not the only acceptable responses. Strong answers explain why a principle applies and connect each recommendation to the risk.

## Part A: Knowledge Check

1. **Confidentiality:** Information is accessible only to authorized people, services, or systems. **Integrity:** Information remains accurate, complete, and protected from unauthorized changes. **Availability:** Authorized users can access information and services when needed.
2. Encryption protects data confidentiality in particular contexts, but authorization decides who is allowed to access an operation or resource. An authorized but compromised application may still expose decrypted data.
3. A cryptographic hash produces a digest that can help detect changes when compared with a trusted expected value. A digital signature uses a private key to sign data and can be verified with the corresponding trusted public key, supporting integrity and publisher authenticity.
4. A backup may be incomplete, corrupted, inaccessible, or too slow to restore. Restore tests validate that recovery actually works within business requirements.
5. Yes. Ransomware combined with data theft may disclose information (confidentiality), alter files (integrity), and prevent access to systems (availability).

## Part B: Identify the Principle

1. **Confidentiality:** Customer details were disclosed to an unauthorized recipient.
2. **Confidentiality and integrity:** The attacker changed access permissions, potentially granting unauthorized access and modifying the system's access-control data.
3. **Availability:** The only production server is offline.
4. **Availability:** Excessive traffic prevents legitimate API use.
5. **Integrity:** Application files or behavior have been tampered with. Confidentiality or availability may also be affected by the malicious code.
6. **Availability:** The company cannot recover from a failure. Integrity may also be a concern if backup consistency is unknown.
7. **Integrity:** Audit evidence was altered or removed. Confidentiality or availability may be affected depending on what the logs contain and how they are used.
8. **Integrity:** A stolen signing key can make malicious software appear to have a trusted signature. The signing identity is also compromised.

## Part C: Match Controls to Principles

| Control | Most direct principle(s) | Explanation |
|---|---|---|
| Multi-factor authentication | Confidentiality; indirectly integrity | Makes unauthorized account access harder, reducing opportunities to view or change data |
| RBAC | Confidentiality and integrity | Limits who can read data and who can modify privileged resources |
| Digital signatures | Integrity | Detects modification and verifies that the signature corresponds to a trusted signing key |
| DDoS protection and rate limiting | Availability | Helps keep services responsive to legitimate traffic |
| Immutable off-site backups | Availability and integrity | Supports recovery and makes unauthorized backup modification or deletion harder |
| Centralized protected audit logging | Integrity; supports confidentiality investigations | Helps preserve trustworthy records of access and changes |
| Redundant network links | Availability | Reduces reliance on a single network path |
| DLP | Confidentiality | Helps detect or prevent unauthorized movement of sensitive information |

A control can support more than one principle depending on its design and deployment.

## Part D: Mini-Labs

### Lab 1: Example Asset and Risk Mapping

| Asset | CIA requirement | Threat | Potential impact | Proposed control |
|---|---|---|---|---|
| Customer database | Confidentiality | Unauthorized database access | Customer data exposure | Least privilege, network restrictions, encryption |
| Appointment records | Integrity | Unauthorized record modification | Incorrect appointments | RBAC, change auditing, validation, approval for sensitive changes |
| Customer portal | Availability | Traffic flood or server failure | Users cannot book appointments | DDoS protection, monitoring, redundancy, recovery plan |

### Lab 2: Integrity Verification

The SHA-256 digest should normally change when the file content changes. The exact output depends on the file contents. A hash comparison is meaningful only if the expected digest is trusted. If an attacker can replace both the file and the published digest, the comparison may not reveal tampering. For release verification, use a trusted signature or obtain the digest through an independent trusted channel.

### Lab 3: Availability Planning

Possible causes include a failed database instance and a DDoS attack. Monitor database health and latency for the first; monitor request rates, error rates, and traffic anomalies for the second. Controls may include database failover, DDoS mitigation, capacity planning, and tested backups.

RTO is the target time to restore service after disruption. RPO is the maximum targeted amount of data loss measured in time. The values should be selected based on business impact rather than copied without analysis. Test restoration and failover, and record actual results.

### Lab 4: Incident Review

1. **Confidentiality:** customer export copied. **Integrity:** configuration changed and logs deleted. **Availability:** potentially affected if the server or service was disrupted.
2. Follow the incident-response plan; isolate affected systems where appropriate; preserve evidence and coordinate with the incident-response team before destructive remediation.
3. Potential sources include centralized logs, cloud audit trails, identity-provider records, firewall or proxy logs, EDR telemetry, network monitoring, backups, and logs from related systems.
4. **Confidentiality:** strengthen least privilege and data-exfiltration monitoring. **Integrity:** protect configurations and logs, use file-integrity monitoring, and require controlled changes. **Availability:** maintain tested clean backups and a recovery plan.

## Part E: Short Scenario

Possible controls:

- **Confidentiality:** MFA, least-privilege access, encryption in transit and at rest, and auditing of access to patient records.
- **Integrity:** role-based permissions, server-side validation, audit trails, and approval or verification for sensitive appointment changes.
- **Availability:** redundant service components, monitoring and alerting, DDoS protection, and tested backups or recovery procedures.

Test access restrictions with authorized test accounts, verify that unauthorized appointment changes are rejected and logged, test backup restoration, and run controlled failover exercises. Avoid testing that could disrupt real patient services; use a staging environment or approved maintenance window.

## Assessment Rubric

| Criterion | What a good answer demonstrates |
|---|---|
| CIA identification | Correctly identifies primary and relevant secondary principles |
| Risk reasoning | Explains the likely impact on data or services |
| Control selection | Recommends controls that address the specific threat |
| Validation | Describes how to test that controls work |
| Operational awareness | Considers recovery, evidence preservation, and business needs |
