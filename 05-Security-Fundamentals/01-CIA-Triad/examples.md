# CIA Triad - Worked Examples

This file demonstrates how to apply Confidentiality, Integrity, and Availability to common security situations.

## Example 1: Exposed Customer Database

**Scenario:** A cloud database containing customer information is accessible from the public internet without appropriate authentication.

- **Primary principle:** Confidentiality
- **Potential impact:** Personal information may be disclosed or copied.
- **Preventive controls:** Restrict network access, require strong authentication, apply least privilege, and encrypt sensitive data.
- **Detective controls:** Audit database access and alert on unusual queries or access locations.
- **Validation:** Confirm that unauthenticated and unauthorized users cannot access the database.

**Discussion:** Encryption helps protect stored data, but it does not replace access controls. If an authorized application can decrypt data, a compromised application may still expose it.

## Example 2: Supplier Payment Details Changed

**Scenario:** An attacker changes a supplier's bank account number in a finance system.

- **Primary principle:** Integrity
- **Potential impact:** Payments may be redirected and records may become unreliable.
- **Preventive controls:** Role-based access, approval workflows, MFA, and separation of duties.
- **Detective controls:** Change logs, alerts for sensitive-field updates, and independent supplier verification.
- **Recovery:** Restore correct details from a trusted source and investigate the change.

**Discussion:** A log is useful only if it is protected from unauthorized modification and reviewed when appropriate.

## Example 3: Denial-of-Service Attack

**Scenario:** A public website receives more traffic than it can handle and becomes unavailable.

- **Primary principle:** Availability
- **Potential impact:** Customers cannot use the service, and business operations may be interrupted.
- **Preventive and mitigating controls:** DDoS protection, rate limiting, traffic filtering, scalable infrastructure, and capacity planning.
- **Detective controls:** Availability monitoring, traffic anomaly detection, and service alerts.
- **Recovery:** Follow the incident-response plan and restore normal service.

## Example 4: Release Artifact Tampering

**Scenario:** A download mirror serves a modified application installer.

- **Primary principle:** Integrity
- **Potential secondary principle:** Confidentiality or availability may also be affected if the installer steals data or damages systems.
- **Controls:** Verify a digital signature against a trusted publisher key; protect signing keys; use controlled build and release pipelines.
- **Important distinction:** Checking a checksum from the same compromised mirror may not detect tampering if both the file and checksum were replaced.

## Example 5: Ransomware Incident

**Scenario:** Ransomware encrypts files on a company's servers. Investigators also find evidence that data was copied before encryption.

| CIA principle | How it is affected | Example response |
|---|---|---|
| Confidentiality | Stolen data may be disclosed | Investigate data access and exfiltration; follow notification obligations |
| Integrity | Files and configurations have been changed | Validate system and data integrity before restoring |
| Availability | Systems and files cannot be used | Isolate affected systems and restore from tested clean backups |

**Lesson:** Do not assume ransomware is only an availability problem.

## Example 6: Balancing Security and Availability

**Scenario:** A company introduces strict access restrictions that accidentally block legitimate users from a critical application.

- **Principle at risk:** Availability for authorized users
- **Underlying issue:** A security control was deployed without adequate testing or fallback.
- **Improvements:** Test policy changes, use staged rollout, monitor authentication failures, document emergency access, and maintain rollback procedures.

**Lesson:** Controls should be designed to protect one principle without unnecessarily undermining another.
