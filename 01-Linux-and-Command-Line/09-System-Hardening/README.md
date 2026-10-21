# 09 — System Hardening

![Linux](https://img.shields.io/badge/Linux-System%20Hardening-FCC624?logo=linux&logoColor=black)
![Level](https://img.shields.io/badge/Level-Intermediate-blue)
![Focus](https://img.shields.io/badge/Focus-DevSecOps%20%7C%20Linux%20Security-red)

## Overview

System hardening reduces a computer's attack surface by removing unnecessary components, applying secure configurations, limiting privileges, protecting remote access, enabling monitoring, and keeping software updated. Hardening should be tailored to the system's purpose and validated to avoid breaking required services.

This module introduces practical Linux hardening techniques for lab environments, with an emphasis on safe auditing before making changes.

## Learning Objectives

By the end of this module, you will be able to:

- Explain attack-surface reduction and defense in depth.
- Establish a basic system security baseline.
- Review installed packages, enabled services, listening ports, and user privileges.
- Apply safer SSH and firewall practices in a controlled environment.
- Review file permissions, account policies, and automatic updates.
- Inspect system logs and audit security-relevant events.
- Understand host firewall, MAC, and service-isolation concepts.
- Use a hardening checklist and document exceptions.
- Explain CIS Benchmarks and Ubuntu Security Guide (USG).
- Plan, test, and roll back hardening changes safely.

## Topics Covered

### 1. Hardening Fundamentals

- Attack surface and threat modeling
- Least privilege
- Defense in depth
- Secure defaults
- Baseline configuration and change control
- Risk-based prioritization

### 2. System Inventory

- OS and kernel version
- Installed packages
- Enabled services
- Listening ports
- Local users and privileged groups
- Scheduled tasks and startup services

### 3. Patch and Package Hygiene

- Security updates
- Removing unnecessary software
- Trusted package repositories
- Reboot planning
- Vulnerability and lifecycle tracking

### 4. Accounts and Access

- Remove or disable unused accounts according to policy
- Review sudo privileges
- Restrict root login where appropriate
- Strong authentication and SSH keys
- Account lifecycle and least privilege

### 5. SSH Hardening

- Review `sshd_config`
- Prefer key-based authentication where operationally appropriate
- Limit users or groups when justified
- Disable direct root login where suitable
- Validate configuration before reload
- Maintain an alternate session or console before changing remote access

### 6. Firewall and Network Exposure

- Inventory listening sockets
- Default-deny inbound policy where suitable
- Allow only required services
- UFW basics on supported Ubuntu/Debian setups
- Avoid locking yourself out of remote systems
- Recheck exposure after changes

### 7. Filesystem and Kernel Security

- File ownership and permissions
- Secure handling of temporary directories
- `sysctl` overview
- AppArmor and SELinux concepts
- Service isolation and systemd security controls
- Avoid unreviewed recursive permission changes

### 8. Logging and Auditing

- `journalctl`
- Authentication logs
- Audit trail retention
- Time synchronization
- Remote log collection
- File integrity monitoring
- Alerting on suspicious events

### 9. Baselines and Compliance

- CIS Benchmarks
- DISA STIG overview
- Ubuntu Security Guide (USG)
- Audit vs. remediation
- Tailoring profiles to workload requirements
- Exception management

## Essential Audit Commands

| Command | Purpose |
|---|---|
| `cat /etc/os-release` | Identify distribution and version |
| `uname -r` | Show running kernel release |
| `ss -tulpn` | Inspect listening sockets (some process details may require privileges) |
| `systemctl --type=service --state=running` | List running service units |
| `systemctl list-unit-files --type=service` | Inspect service unit enablement |
| `getent passwd` | Query account records |
| `id USER` | Inspect a user's identity and groups |
| `sudo -l` | Review current user's allowed sudo commands |
| `journalctl -p warning..alert` | Review warning and higher-priority journal messages |
| `find PATH -xdev -type f -perm -0002 -print` | Audit world-writable files on a chosen filesystem |
| `ufw status verbose` | Inspect UFW status where UFW is installed |
| `aa-status` | Inspect AppArmor status where available |

## Safe Hardening Workflow

1. **Inventory:** Understand the workload, users, services, and network exposure.
2. **Baseline:** Capture current configuration and relevant command output.
3. **Prioritize:** Address exposed, exploitable, high-impact risks first.
4. **Plan:** Define intended changes, impact, backup, and rollback steps.
5. **Test:** Apply changes in a VM or staging environment.
6. **Implement:** Change one logical control at a time.
7. **Validate:** Verify that security improved and required services still work.
8. **Monitor:** Review logs and detect drift.
9. **Document:** Record evidence, exceptions, and next review date.

## Important Safety Notes

- These labs are for systems you own or are authorized to administer.
- Never apply a blanket hardening script to a production host without reviewing each change.
- Do not disable SSH password authentication until key-based access has been tested and a recovery console is available.
- Do not enable a firewall remotely until the required management port is allowed and the rules have been validated.
- Avoid blindly applying CIS or STIG rules: they may conflict with application, cloud, or operational requirements.
- Back up configuration and have a tested rollback plan before changing security-critical settings.

## Repository Files

- `README.md` — concepts, workflow, and audit commands
- `examples.md` — command demonstrations
- `practical.md` — hands-on exercises and hardening scenarios
- `solution.md` — reference solutions and explanations

## Completion Checklist

- [ ] Inventory the OS, services, ports, and accounts.
- [ ] Review updates and installed packages.
- [ ] Audit sudo access and account status.
- [ ] Review SSH configuration safely.
- [ ] Build a minimal firewall policy for a lab VM.
- [ ] Audit risky file permissions.
- [ ] Review logs and security controls.
- [ ] Explain AppArmor/SELinux and service isolation.
- [ ] Understand CIS benchmarks and USG.
- [ ] Document validation evidence and rollback steps.

## Further Reading

- [Ubuntu: A Guide to Infrastructure Hardening](https://ubuntu.com/engage/a-guide-to-infrastructure-hardening)
- [Ubuntu Security Guide Documentation](https://documentation.ubuntu.com/security/compliance/usg/)
- [CIS Ubuntu Linux Benchmarks](https://www.cisecurity.org/benchmark/ubuntu_linux)
- [Linux `ss` Manual](https://man7.org/linux/man-pages/man8/ss.8.html)
- [systemd Security Features](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html)

## Next Module

Continue to the next module in the DevSecOps Roadmap to build on Linux security administration and operational monitoring.
