# Linux System Hardening — Practical Lab

## Lab Information

**Level:** Intermediate

**Objective:** Audit a Linux system, identify security weaknesses, propose mitigations, and validate changes safely.

**Environment:** Disposable Ubuntu, Debian, or Kali Linux VM. Take a snapshot before configuration changes.

## Safety Rules

- Work only on systems you own or are authorized to administer.
- Do not perform these exercises directly on a production server.
- Never change SSH or firewall settings remotely without a recovery path.
- Back up configuration before editing it.
- Validate each change and keep a rollback plan.
- Do not run unreviewed hardening scripts or blindly apply compliance profiles.

---

## Practical 1: Establish a System Baseline

**Tasks**

1. Record the distribution and kernel version.
2. List running services.
3. List listening network sockets.
4. Record privileged users or groups.
5. Store the outputs in a private lab directory.

Explore:

```bash
cat /etc/os-release
uname -r
systemctl --type=service --state=running
sudo ss -tulpn
getent group sudo
```

Some commands and group names differ by distribution.

## Practical 2: Review Installed Packages

**Tasks**

1. List packages that have updates available.
2. Identify unnecessary or unsupported packages.
3. Document why each package is needed or may be removable.
4. Propose a safe removal plan without removing essential dependencies.

Use the package manager appropriate for your distribution.

## Practical 3: Audit User Accounts and Privileges

**Tasks**

1. Review local account records.
2. Identify members of administrative groups.
3. Inspect your own `sudo` privileges.
4. Identify unused accounts for investigation.
5. Write a recommended access-review process.

Do not delete or lock accounts without confirming their purpose and the applicable account policy.

## Practical 4: SSH Configuration Review

**Tasks**

1. Find the SSH server configuration file.
2. Run the SSH configuration syntax test.
3. Inspect effective root-login, password-authentication, and public-key settings.
4. Propose a safer SSH configuration for a server.
5. Document how to test key-based access before disabling passwords.
6. Describe your recovery plan if a new configuration blocks access.

Do not apply changes to a remote host during this exercise.

## Practical 5: Firewall Exposure Review

**Tasks**

1. List listening sockets.
2. Identify which services need network access.
3. Inspect the active firewall and rules.
4. Propose an inbound allowlist.
5. Identify the management port that must remain reachable.
6. Write rollback steps before applying any rule.

Perform any actual firewall change only on a disposable VM with console access.

## Practical 6: Audit File Permissions

Create a lab file:

```bash
mkdir -p ~/hardening-lab
touch ~/hardening-lab/sample.txt
chmod 666 ~/hardening-lab/sample.txt
```

**Tasks**

1. Find world-writable files within the lab directory.
2. Inspect owner, group, and mode.
3. Explain why world-writable configuration files are risky.
4. Recommend an appropriate replacement mode for a private file.
5. Verify the change.

Do not run broad recursive `chmod` or `chown` commands against system directories.

## Practical 7: Review Logs and Authentication Events

**Tasks**

1. Review warnings and higher-priority journal messages.
2. Review SSH service logs, if present.
3. Identify examples of failed authentication or service errors if available.
4. Explain how time synchronization helps correlate events.
5. Propose a secure log-retention and remote-logging policy.

Avoid exposing usernames, IP addresses, tokens, or other sensitive log data when sharing evidence.

## Practical 8: Review Mandatory Access Control

**Tasks**

1. Determine whether AppArmor or SELinux is available.
2. Inspect its current status.
3. Explain the difference between discretionary file permissions and mandatory access control.
4. Describe how to investigate a denied application operation.
5. Explain why disabling the control is not the preferred first response.

## Practical 9: Review Kernel Parameters

**Tasks**

1. Inspect `kernel.randomize_va_space`.
2. Inspect `net.ipv4.ip_forward`.
3. Explain what each parameter controls.
4. Determine which setting is appropriate for your VM's role.
5. Document any proposed change and its rollback.

Do not blindly apply values from generic hardening lists. Routers, containers, and ordinary workstations may require different settings.

## Practical 10: Service Hardening

Choose a non-critical service in your VM.

**Tasks**

1. Inspect its unit file and effective properties.
2. Identify the service account.
3. Review available systemd isolation options such as `NoNewPrivileges`, `PrivateTmp`, and filesystem protection.
4. Propose a minimal set of appropriate controls.
5. Test the service in staging and verify its normal functionality.

Do not apply restrictive settings to a critical service without understanding its filesystem, device, and network requirements.

## Practical 11: CIS Benchmark and Compliance Planning

**Tasks**

1. Read the relevant CIS Benchmark overview.
2. Explain the difference between auditing and remediation.
3. Identify why workstation and server profiles differ.
4. Explain how a compliance rule could break an application.
5. Draft a process for tailoring rules, documenting exceptions, and retesting.

For Ubuntu, research Ubuntu Security Guide (USG) availability and requirements before attempting to run it.

## Final Challenge: Hardening Report

Prepare a report with:

1. System inventory and scope.
2. Five prioritized findings.
3. Risk and impact for each finding.
4. Recommended mitigation.
5. Validation evidence.
6. Rollback steps.
7. Any exceptions or operational dependencies.
8. A date for the next review.

Use a risk-based approach and distinguish observed facts from assumptions.

## Submission Checklist

- [ ] Baseline collected.
- [ ] Package inventory reviewed.
- [ ] Privileged accounts audited.
- [ ] SSH settings reviewed safely.
- [ ] Listening ports and firewall rules assessed.
- [ ] File permissions audited.
- [ ] Logs reviewed.
- [ ] MAC and kernel controls understood.
- [ ] Service hardening options evaluated.
- [ ] CIS/compliance approach documented.
- [ ] Final hardening report completed.

Compare your work with `solution.md`.
