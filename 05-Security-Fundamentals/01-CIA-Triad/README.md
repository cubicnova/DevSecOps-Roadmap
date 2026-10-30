# 01 - CIA Triad

The **CIA Triad** is a foundational information-security model made up of **Confidentiality, Integrity, and Availability**. It helps teams identify what must be protected and choose suitable security controls.

## Learning Objectives

- Define each of the three CIA principles.
- Identify threats that affect confidentiality, integrity, and availability.
- Select appropriate preventive, detective, and recovery controls.
- Apply the CIA Triad to practical security scenarios.

## 1. Confidentiality

Confidentiality means information is available only to authorized people, services, or systems.

**Threat examples:** stolen credentials, exposed cloud storage, eavesdropping, accidental disclosure, excessive permissions.

**Controls:** MFA, least-privilege authorization, encryption at rest and in transit, data classification, secure secret storage, and access auditing.

## 2. Integrity

Integrity means information and systems remain accurate, complete, and protected from unauthorized changes.

**Threat examples:** tampered records, modified files, compromised software updates, corrupted data, altered audit logs.

**Controls:** digital signatures, trusted hash verification, file-integrity monitoring, database constraints, change management, and protected audit logs.

> A hash is useful for detecting changes only when the expected hash comes from a trusted source. A hash alone does not prove who created a file.

## 3. Availability

Availability means authorized users can access information and services when required.

**Threat examples:** DoS/DDoS attacks, hardware failure, ransomware, exhausted resources, outages, and accidental deletion.

**Controls:** redundancy, failover, monitoring, capacity planning, DDoS protection, tested backups, incident response, and disaster recovery.

## CIA Triad at a Glance

| Principle | Key question | Example incident | Example controls |
|---|---|---|---|
| Confidentiality | Who can access the data? | Customer records exposed | MFA, authorization, encryption |
| Integrity | Can the data be trusted? | Supplier bank details changed | Digital signatures, audit logs, change controls |
| Availability | Can authorized users access the service? | Website outage | Redundancy, DDoS protection, recovery plans |

## Applying the CIA Triad

1. Identify the assets and data being protected.
2. Determine confidentiality, accuracy, and uptime requirements.
3. Identify threats and likely impacts.
4. Choose suitable preventive, detective, and recovery controls.
5. Test whether the controls work as intended.
6. Review risks and update controls as systems change.

One incident may affect multiple principles. For example, ransomware can make systems unavailable, alter or encrypt data, and involve a confidentiality breach if information is also stolen.

## Module Files

- [`examples.md`](examples.md) — worked scenarios and control mapping.
- [`exercises.md`](exercises.md) — practice questions and mini-labs.
- [`solutions.md`](solutions.md) — suggested answers with explanations.

## Further Reading

- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [NIST SP 1800-26: Data Integrity](https://www.nccoe.nist.gov/publication/1800-26/VolA/1800-26A.html)
- [OWASP Developer Guide: Security Fundamentals](https://devguide.owasp.org/en/02-foundations/01-security-fundamentals/)

## Completion Checklist

- [ ] I can explain all three CIA principles.
- [ ] I can map incidents to the affected principles.
- [ ] I can recommend controls for common risks.
- [ ] I understand that a single incident can affect multiple principles.
