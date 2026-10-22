# CIA Triad - Exercises

Try the questions before checking `solutions.md`. Use the CIA principles to explain both the risk and the control you recommend.

## Part A: Knowledge Check

1. Define confidentiality, integrity, and availability in one or two sentences each.
2. Why is encryption not a complete substitute for authorization?
3. What is the difference between a hash and a digital signature in an integrity-verification workflow?
4. Why should backups be tested rather than merely configured?
5. Can one incident affect all three CIA principles? Give an example.

## Part B: Identify the Principle

For each scenario, identify the primary CIA principle affected. Include secondary principles if relevant.

1. A staff member emails a spreadsheet containing customer details to the wrong recipient.
2. An attacker changes a user's role from `viewer` to `administrator`.
3. A power failure takes a company's only production server offline.
4. An attacker floods an API with requests, preventing legitimate requests from completing.
5. A malicious software update contains code that changes application files.
6. A company cannot restore its backups because the backup encryption key was lost.
7. A privileged employee deletes audit logs to hide unauthorized changes.
8. An attacker steals a signing key and uses it to sign a malicious release.

## Part C: Match Controls to Principles

For each control, name the CIA principle or principles it most directly supports and explain why.

- Multi-factor authentication
- Role-based access control (RBAC)
- Digital signatures for software releases
- DDoS protection and rate limiting
- Immutable off-site backups
- Centralized, access-controlled audit logging
- Redundant network links
- Data-loss prevention (DLP)

## Part D: Mini-Labs

### Lab 1: Asset and Risk Mapping

Choose a fictional web application with user accounts and a database. Create a table with these columns:

| Asset | CIA requirement | Threat | Potential impact | Proposed control |
|---|---|---|---|---|

Add at least three rows, with one row for each CIA principle.

### Lab 2: Integrity Verification

1. Create a harmless text file named `sample.txt`.
2. Calculate a SHA-256 hash using a trusted local tool.
3. Change one character in the file and calculate the hash again.
4. Compare the two hashes.
5. Write down why the expected hash must be obtained through a trusted channel.

Example commands:

Linux:
```bash
sha256sum sample.txt
```

PowerShell:
```powershell
Get-FileHash .\sample.txt -Algorithm SHA256
```

### Lab 3: Availability Planning

For a fictional customer portal, identify:

- Two causes of downtime
- One monitoring signal for each cause
- Two preventive or mitigating controls
- A backup and recovery test
- A reasonable recovery-time objective (RTO) and recovery-point objective (RPO), with a brief justification

### Lab 4: Incident Review

A company discovers that an attacker accessed a web server, copied a customer export, changed a configuration file, and deleted the local logs.

1. Identify the CIA principles affected.
2. List the first three defensive response steps.
3. Name evidence sources that may still be available.
4. Recommend one long-term improvement for each CIA principle.

## Part E: Short Scenario

A healthcare appointment service must protect patient details, prevent unauthorized appointment changes, and remain available during business hours. Recommend at least two controls for each CIA principle. Explain any trade-offs and how you would test the controls.

## Submission Checklist

- [ ] Every scenario has a reasoned CIA mapping.
- [ ] Recommended controls address the stated risk.
- [ ] The integrity lab includes before-and-after hash observations.
- [ ] The availability plan includes monitoring and recovery testing.
- [ ] Incident-response actions prioritize containment, evidence preservation, and safe recovery.
