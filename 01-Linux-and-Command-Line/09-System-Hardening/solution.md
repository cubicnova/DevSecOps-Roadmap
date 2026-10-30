# Linux System Hardening — Solutions

These are reference solutions for the exercises in `practical.md`. Actual results depend on the distribution, version, installed services, and workload.

> Apply changes only to a system you own or are authorized to administer. Use a VM snapshot and recovery console before testing access-control changes.

## Solution 1: Establish a System Baseline

```bash
cat /etc/os-release
uname -r
systemctl --type=service --state=running
sudo ss -tulpn
getent group sudo
```

On some distributions, the administrative group is `wheel`. Some services may be socket-activated or otherwise not represented by a simple running-service list, so combine service and socket inspection.

Record outputs securely because they may reveal hostnames, service names, local addresses, and process details.

## Solution 2: Review Installed Packages

Debian-based systems:

```bash
apt list --upgradable
dpkg -l
```

Fedora/RHEL-family systems:

```bash
dnf check-update
rpm -qa
```

Build an inventory of software that is unsupported or not required by the workload. Before removing a package, inspect its dependencies and the proposed transaction. Maintain backups and a tested recovery path.

## Solution 3: Audit User Accounts and Privileges

```bash
getent passwd
getent group sudo
sudo -l
```

Use the appropriate administrative group for the distribution. Review privileged membership against a documented business need. Do not assume that every account with a non-interactive shell is unused or safe to delete.

Account removal or locking should follow the organization's identity lifecycle policy and should preserve service dependencies and required evidence.

## Solution 4: SSH Configuration Review

Find the SSH daemon configuration and validate it:

```bash
sudo sshd -t
sudo sshd -T | grep -E 'permitrootlogin|passwordauthentication|pubkeyauthentication'
```

Possible hardening goals include:

- Disable direct root login where appropriate.
- Prefer public-key or certificate-based authentication when supported by the operational model.
- Limit permitted users or groups where justified.
- Use strong key management and monitor authentication attempts.

Do not blindly paste settings into a configuration file: `Match` blocks and included files can affect effective configuration.

Before implementing:
1. Back up the configuration.
2. Test key-based access in a second session.
3. Ensure console or out-of-band recovery.
4. Validate syntax with `sshd -t`.
5. Reload only after validation.
6. Verify a new connection before closing the existing session.

## Solution 5: Firewall Exposure Review

```bash
sudo ss -tulpn
sudo ufw status verbose
```

The second command applies only when UFW is installed and used. Other systems may use nftables, firewalld, or cloud network controls.

Create an allowlist based on required services. For remote administration, verify the correct port and source networks before enabling or changing firewall policy. Test on a disposable VM with console access and retain a rollback plan.

A listening port is not automatically exposed to the public internet; host firewall, routing, cloud security groups, and network architecture also matter.

## Solution 6: Audit File Permissions

```bash
mkdir -p ~/hardening-lab
touch ~/hardening-lab/sample.txt
chmod 666 ~/hardening-lab/sample.txt

find ~/hardening-lab -xdev -type f -perm -0002 -print
stat -c '%A %a %U %G %n' ~/hardening-lab/sample.txt
```

For a private file owned by the current user, a common mode is:

```bash
chmod 600 ~/hardening-lab/sample.txt
stat -c '%A %a %U %G %n' ~/hardening-lab/sample.txt
```

This removes group and other access through ordinary permission bits. Choose modes based on actual sharing requirements and review ACLs where relevant.

## Solution 7: Review Logs and Authentication Events

```bash
sudo journalctl -p warning..alert --since "24 hours ago"
sudo journalctl -u ssh --since "24 hours ago"
```

The SSH unit may be named `sshd` on some distributions. Authentication logs may be stored in different locations or primarily in the journal.

Review timestamps, authentication failures, service errors, and repeated anomalies. Correlate events using synchronized system time. For stronger resilience, consider forwarding logs to a protected central service with appropriate retention and access controls.

## Solution 8: Review Mandatory Access Control

AppArmor:

```bash
command -v aa-status && sudo aa-status
```

SELinux:

```bash
command -v getenforce && getenforce
```

Discretionary access control (DAC) uses ownership and ordinary permission bits. Mandatory access control (MAC) applies additional policy restrictions, even where DAC permissions would otherwise permit access.

Investigate policy denials and adjust the policy narrowly. Disabling MAC entirely can remove an important defense-in-depth control.

## Solution 9: Review Kernel Parameters

```bash
sysctl kernel.randomize_va_space
sysctl net.ipv4.ip_forward
```

- `kernel.randomize_va_space` controls address-space layout randomization behavior on Linux.
- `net.ipv4.ip_forward` controls IPv4 packet forwarding.

Whether forwarding should be enabled depends on the machine's role. A router or gateway may require it; a general-purpose host often does not. Record the baseline, review dependencies, test a proposed value, and document rollback before changing settings.

## Solution 10: Service Hardening

Inspect a chosen unit:

```bash
systemctl cat example.service
systemctl show example.service -p User -p Group -p NoNewPrivileges -p PrivateTmp -p ProtectSystem
```

Replace `example.service` with the actual service name.

Potential controls include:
- Running under a dedicated, non-root service account.
- `NoNewPrivileges=yes` where compatible.
- `PrivateTmp=yes` where compatible.
- Appropriate filesystem protections.
- Restricting writable paths and unnecessary capabilities.

Systemd directives have compatibility implications and are not suitable for every workload. Apply them in staging, review service logs, and test normal application operations before rollout.

## Solution 11: CIS Benchmark and Compliance Planning

CIS Benchmarks provide security configuration recommendations. Auditing checks the current system against selected rules; remediation changes configuration to address findings.

A safe workflow is:

1. Select a benchmark version and profile appropriate to the OS and workload.
2. Run an audit first.
3. Review each finding and operational dependency.
4. Tailor rules where justified.
5. Back up configuration and test remediation in staging.
6. Apply approved changes with a rollback plan.
7. Re-audit and retain evidence.
8. Document accepted exceptions and their owners.

For Ubuntu, the Ubuntu Security Guide (USG) can help audit and apply supported compliance profiles. Availability and supported profiles depend on the Ubuntu release and subscription/setup. Consult the official documentation before installation or remediation.

Official documentation: https://documentation.ubuntu.com/security/compliance/usg/

## Solution 12: Example Hardening Report

A sample report might include:

| Finding | Risk | Suggested action | Validation |
|---|---|---|---|
| Unneeded service listening | Increased attack surface | Confirm owner and disable only if not required | Recheck service state and sockets |
| Excessive sudo access | Privilege escalation impact | Reduce membership and scope of rules | Review `sudo -l` and group membership |
| Weak remote-access policy | Unauthorized access | Test and enforce stronger authentication | Validate SSH config and new login |
| World-writable sensitive file | Unauthorized modification | Correct owner and permissions | Check `stat` and ACLs |
| Insufficient log monitoring | Delayed detection | Forward and alert on relevant events | Confirm receipt and alert tests |

This is an illustrative template, not a claim about a particular system. Populate the report with actual evidence from the lab.

## Final Review

You should now be able to:

- Inventory a Linux system and its exposure.
- Prioritize and validate hardening changes.
- Review account, SSH, firewall, file, and service security.
- Inspect logs and mandatory access controls.
- Understand compliance profiles and tailoring.
- Document risk, evidence, exceptions, and rollback.

## References

- [Ubuntu Infrastructure Hardening Guide](https://ubuntu.com/engage/a-guide-to-infrastructure-hardening)
- [Ubuntu Security Guide Documentation](https://documentation.ubuntu.com/security/compliance/usg/)
- [CIS Ubuntu Linux Benchmarks](https://www.cisecurity.org/benchmark/ubuntu_linux)
- [Linux `ss` Manual](https://man7.org/linux/man-pages/man8/ss.8.html)
- [systemd Execution and Security Options](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html)
