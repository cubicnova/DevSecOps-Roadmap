# 10 — Audit and Troubleshooting

Learn how to inspect Linux system health, audit configuration, investigate common failures, and collect useful evidence safely.

## Learning objectives

By the end of this module, you should be able to:

- Establish a baseline for system, process, storage, memory, and network health.
- Inspect systemd service state and logs.
- Filter system logs by time, service, and severity.
- Identify disk-space, inode, memory, CPU, DNS, and connectivity problems.
- Review users, permissions, listening ports, and recent authentication events.
- Collect a repeatable troubleshooting snapshot without changing system state.
- Document findings, impact, likely cause, remediation, and verification.

## Prerequisites

- Basic Linux shell navigation and permissions.
- Familiarity with processes, files, services, and networking.
- A Linux VM or lab machine. Commands may differ across distributions.
- `sudo` access for some audit logs and administrative checks.

## Safety first

1. Start with read-only commands and gather evidence before changing configuration.
2. Run checks only on systems you own or are explicitly authorized to administer.
3. Avoid posting logs publicly without reviewing them for usernames, hostnames, IP addresses, tokens, and other sensitive data.
4. Do not clear logs, delete files, kill processes, or restart services as a first step.
5. Treat any remediation as a controlled change: record the current state, make one change at a time, and verify the result.

## 1. Establish a system baseline

```bash
date
hostnamectl
uname -a
uptime
who
w
```

Useful commands:
- `uptime`: uptime and load averages.
- `top` or `htop`: live CPU and process activity.
- `ps aux --sort=-%cpu | head`: processes with high CPU use.
- `free -h`: memory and swap summary.
- `df -hT`: filesystem space and filesystem type.
- `df -ih`: inode consumption.
- `lsblk -f`: block devices and filesystems.
- `ip address`: interface addresses.
- `ip route`: routing table.
- `ss -tulpn`: listening TCP/UDP sockets (process details may require elevated privileges).

## 2. Services and systemd

```bash
systemctl --failed
systemctl status ssh
systemctl is-enabled ssh
systemctl list-units --type=service --state=running
```

The SSH service may be named `ssh` on Debian/Ubuntu and `sshd` on some other distributions. Substitute the actual unit name for your system.

Before restarting a service:
- Capture `systemctl status SERVICE`.
- Read recent logs with `journalctl -u SERVICE --since "1 hour ago"`.
- Check configuration syntax if the service provides a validation command.
- Confirm whether restarting could interrupt users or applications.

## 3. Logs and event investigation

### systemd journal

```bash
journalctl -b -p warning
journalctl --since "today"
journalctl -u ssh --since "1 hour ago"
journalctl -k --since "today"
journalctl -b -1
```

- `-b`: current boot; `-b -1`: previous boot if logs are retained.
- `-p warning`: warning priority and more severe messages.
- `-u`: filter by systemd unit.
- `--since` / `--until`: constrain the time window.

### Traditional log files

Depending on the distribution, relevant files may include:
- `/var/log/syslog`
- `/var/log/messages`
- `/var/log/auth.log`
- `/var/log/secure`
- `/var/log/kern.log`

Check which files exist; not every distribution uses all of them. Prefer `journalctl` on systemd-based systems where appropriate.

### Search logs

```bash
sudo grep -iE 'error|failed|denied|timeout' /var/log/syslog
sudo journalctl --since "2 hours ago" | grep -iE 'error|failed|timeout'
```

A matching word is a lead, not proof of a root cause. Correlate timestamps, affected services, and other evidence.

## 4. Storage troubleshooting

```bash
df -hT
df -ih
lsblk -f
du -xhd1 /var 2>/dev/null | sort -h
```

- `df -hT` reports filesystem space.
- `df -ih` reports inode use; a filesystem can run out of inodes even with free bytes.
- `du` estimates space used by directories. Permission restrictions can hide some results.
- `du -x` keeps traversal on one filesystem; `-d1` limits depth on GNU `du`.

If `df` says a filesystem is full but `du` does not account for the usage, investigate deleted-but-open files with tools such as `sudo lsof +L1` if installed. Do not delete unfamiliar files or logs just to free space.

## 5. Memory and CPU

```bash
free -h
vmstat 1 5
ps aux --sort=-%mem | head
ps aux --sort=-%cpu | head
top
```

Interpretation tips:
- Linux uses available RAM for cache; low `free` memory alone does not automatically indicate a problem.
- Check `available`, swap activity, sustained CPU use, and application symptoms together.
- Load average is not a CPU percentage; interpret it alongside CPU count and I/O wait.
- Kernel OOM messages may appear in `journalctl -k` or `dmesg`.

## 6. Network troubleshooting

Use a layered approach:

```bash
ip address
ip route
getent hosts example.com
ping -c 4 1.1.1.1
ping -c 4 example.com
ss -tulpn
curl -I --max-time 10 https://example.com
```

Not every network permits ICMP, so failed `ping` does not by itself prove the host is unreachable. Compare IP connectivity, DNS resolution, route, port state, and application-level requests. Use approved destinations only.

For a service that should listen on a port:

```bash
sudo ss -ltnp
```

Confirm the service is listening on the expected address and port, then check host firewall rules and any upstream network controls.

## 7. Security and configuration audit

Read-only checks to begin with:

```bash
id
getent passwd
getent group sudo
sudo ss -tulpn
sudo find /etc -type f -perm -002 -print 2>/dev/null
sudo find /home -maxdepth 2 -type f -name 'authorized_keys' -print 2>/dev/null
```

Notes:
- Review output manually; a finding is not automatically a vulnerability.
- Some service accounts and world-writable paths are expected.
- Avoid dumping password hashes or private keys.
- Check authentication logs according to the distribution and your access rights.
- Compare configuration against an approved baseline and organizational policy.

Optional audit tools depend on distribution and installed packages: `auditd`, `lynis`, `aide`, `needrestart`, and package-specific configuration validators. Install or run tools only under your organization's change and authorization process.

## 8. Troubleshooting workflow

1. **Define the symptom:** what fails, who is affected, and when it began.
2. **Scope impact:** one user, one service, one host, or a wider outage?
3. **Preserve evidence:** timestamps, commands, exit codes, logs, and recent changes.
4. **Check dependencies:** DNS, network, storage, credentials, service dependencies.
5. **Form a hypothesis:** explain how the evidence supports it.
6. **Test safely:** one reversible change at a time, preferably in a lab or maintenance window.
7. **Verify:** repeat the failing action and check logs and service health.
8. **Document:** root cause (or uncertainty), impact, fix, verification, and follow-up.

## 9. Create a support bundle

This read-only Bash script records a basic diagnostic snapshot. It writes only to the output directory you choose. Review the resulting files before sharing; they may contain sensitive host details.

```bash
#!/usr/bin/env bash
set -u
OUT="${1:-./linux-audit-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$OUT" || exit 1
run() {
  local name="$1"; shift
  { printf '$'; printf ' %q' "$@"; printf '\n\n'; "$@"; } >"$OUT/$name.txt" 2>&1 || true
}
run system date
run hostname hostnamectl
run kernel uname -a
run uptime uptime
run memory free -h
run disk df -hT
run inodes df -ih
run block_devices lsblk -f
run processes ps aux
run routes ip route
run addresses ip address
run sockets ss -tulpn
run failed_units systemctl --failed
run recent_warnings journalctl -b -p warning --no-pager -n 300
printf 'Snapshot saved to: %s\n' "$OUT"
```

Save as `collect-audit.sh`, then run:

```bash
chmod 700 collect-audit.sh
./collect-audit.sh
```

Some commands may be unavailable or return limited output without elevated privileges. Do not run the script with `sudo` by default; elevate only for a clearly justified need.

## Quick reference

| Symptom | First checks |
|---|---|
| Service unavailable | `systemctl status`, `journalctl -u`, `ss -ltnp` |
| Disk full | `df -hT`, `df -ih`, `du -xhd1` |
| Slow system | `uptime`, `top`, `vmstat`, `free -h` |
| DNS failure | `getent hosts`, resolver configuration, compare IP vs hostname |
| Port unreachable | `ss -ltnp`, route, firewall, service bind address |
| Unexpected reboot | `last -x`, `journalctl -b -1`, kernel logs |
| Permission denied | `id`, `namei -l PATH`, `stat PATH`, ACLs if applicable |
| Authentication issue | correct auth log/journal, account status, time, SSH configuration |

## Suggested learning sequence

1. Run the baseline commands and record normal output.
2. Inspect warnings and errors from the current boot.
3. Compare filesystem bytes and inode use.
4. Trace a local service from process state to listening socket and logs.
5. Complete the exercises in [`practical.md`](practical.md).
6. Compare your answers with [`solutions.md`](solutions.md).

## Further reading

- [`systemctl(1)` manual](https://man7.org/linux/man-pages/man1/systemctl.1.html)
- [`journalctl(1)` manual](https://man7.org/linux/man-pages/man1/journalctl.1.html)
- [`df(1)` manual](https://man7.org/linux/man-pages/man1/df.1.html)
- [`free(1)` manual](https://man7.org/linux/man-pages/man1/free.1.html)
- [`ss(8)` manual](https://man7.org/linux/man-pages/man8/ss.8.html)
- [Ubuntu Server firewall logging documentation](https://documentation.ubuntu.com/server/how-to/security/firewalls/)

## Completion checklist

- [ ] I can gather a system baseline.
- [ ] I can filter service and kernel logs by time.
- [ ] I can distinguish disk-space and inode exhaustion.
- [ ] I can investigate service, DNS, and port issues methodically.
- [ ] I can collect and redact a diagnostic snapshot.
- [ ] I can document findings and verify a fix.
