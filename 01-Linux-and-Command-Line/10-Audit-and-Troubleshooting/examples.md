# Examples — Audit and Troubleshooting

Use these commands on a Linux system you own or are authorized to administer. Most examples are read-only; output varies by distribution and machine.

## 1. Quick baseline

```bash
date
hostname
uname -r
uptime
who
free -h
df -hT
```

**Read it:** timestamp and hostname establish context; uptime and load provide a quick performance clue; memory and filesystem output show resource status.

## 2. Find failed services

```bash
systemctl --failed
systemctl status cron
```

Some distributions name the scheduler service `cron`; others use `crond`. If a unit is not found, check its actual name with `systemctl list-unit-files | grep -E 'cron|ssh|network'`.

## 3. Inspect service logs

```bash
sudo journalctl -u ssh --since "30 minutes ago" --no-pager
```

If the service is called `sshd`, substitute that unit. Use a bounded time window around the reported failure.

## 4. Review warnings from the current boot

```bash
sudo journalctl -b -p warning --no-pager -n 100
```

This prints up to 100 recent warning-or-higher journal entries for the current boot. Investigate timestamps and components rather than assuming every warning is actionable.

## 5. Search text logs safely

```bash
sudo grep -iE 'error|failed|denied|timeout' /var/log/auth.log
```

The file may not exist on your distribution. Try `/var/log/secure`, or use `journalctl` when appropriate.

## 6. Identify full filesystems and inode exhaustion

```bash
df -hT
df -ih
```

Example interpretation:
- `/` at 98% usage: investigate large directories and application growth.
- Inodes at 100%: a very large number of small files may be the issue.
- Do not remove files until their owner, purpose, and retention requirements are understood.

## 7. Find large top-level directories

```bash
sudo du -xhd1 /var 2>/dev/null | sort -h
```

GNU `du` supports `-d`; on other systems, use the equivalent depth option. The command may omit directories you cannot read.

## 8. Check for deleted-but-open files

```bash
sudo lsof +L1
```

This requires `lsof`. A process can keep disk blocks allocated after a file is deleted. Investigate the process and service owner before taking action; a controlled service restart may be needed, but do not do it blindly.

## 9. Check listening sockets

```bash
sudo ss -tulpn
sudo ss -ltn
```

- `-t`: TCP; `-u`: UDP; `-l`: listening; `-p`: process information; `-n`: numeric addresses and ports.
- If a service is missing from the list, check whether it started and whether it binds to a different address or port.

## 10. Separate DNS from connectivity

```bash
getent hosts example.com
ping -c 3 1.1.1.1
ping -c 3 example.com
curl -I --max-time 10 https://example.com
```

A host may block ping. Compare results and consider proxy settings, routing, resolver configuration, firewall policy, and TLS/application errors.

## 11. Check route and interface state

```bash
ip address
ip route
ip neigh
```

Look for the expected interface, IP address, default route, and neighbor entries. Avoid modifying routes until you understand the host's network design.

## 12. Investigate high CPU or memory use

```bash
ps aux --sort=-%cpu | head -n 10
ps aux --sort=-%mem | head -n 10
free -h
vmstat 1 5
```

A single snapshot may be misleading. Observe trends and correlate them with application latency, logs, and workload.

## 13. Inspect a path's permissions

```bash
namei -l /var/log
stat /var/log
```

`namei -l` shows permissions on each path component. Access can fail because a parent directory lacks execute/search permission, even if the final file looks readable.

## 14. Check recent reboots

```bash
last -x | head -n 20
journalctl --list-boots
journalctl -b -1 -p warning --no-pager
```

Previous-boot logs are only available if retained. Unexpected reboot evidence may be incomplete, so corroborate with monitoring and provider logs where available.

## 15. Capture command output with timestamps

```bash
{
  date --iso-8601=seconds
  uptime
  free -h
  df -hT
  systemctl --failed
} 2>&1 | tee "snapshot-$(date +%Y%m%d-%H%M%S).txt"
```

Review the snapshot for sensitive information before sharing it.

## 16. Inspect authentication events

```bash
sudo journalctl --since "today" | grep -iE 'authentication failure|failed password|accepted publickey'
```

Exact messages and locations differ. A failed login is not sufficient proof of compromise; review source, time, account, surrounding events, and expected activity.

## 17. Check firewall state without changing it

```bash
sudo ufw status verbose
sudo nft list ruleset
```

Use the tool that is installed and configured. Avoid changing firewall rules during diagnosis without authorization and a rollback plan.

## 18. Validate a hypothesis

Scenario: an internal web service is reported as unavailable.

```bash
systemctl status nginx
journalctl -u nginx --since "30 minutes ago" --no-pager
sudo ss -ltnp
curl -I --max-time 5 http://127.0.0.1/
```

If the service is not Nginx, replace the unit and test URL. A successful localhost request does not prove external access works; also inspect bind address, host firewall, routes, and upstream controls.

## 19. Build a small evidence note

```text
Incident ID:
Host and environment:
First observed time and timezone:
Reported symptom:
Affected users/services:
Commands run and relevant output:
Recent changes:
Evidence supporting hypothesis:
Actions taken (with approval):
Verification performed:
Remaining risk / follow-up:
```

Keep notes factual. Distinguish confirmed facts from hypotheses.

## 20. Mini audit command set

```bash
id
getent passwd | cut -d: -f1,3,6,7
getent group sudo
sudo ss -tulpn
find "$HOME" -maxdepth 2 -type f -perm -002 -print 2>/dev/null
```

Review the output in context. Avoid exposing sensitive data and do not treat every finding as a security defect.
