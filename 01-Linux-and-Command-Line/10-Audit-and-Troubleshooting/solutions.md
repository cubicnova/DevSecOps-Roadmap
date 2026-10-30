# Solutions — Audit and Troubleshooting

These are example approaches, not the only correct answers. Your output will depend on distribution, permissions, installed services, and workload. Never invent findings if your system shows none.

## Lab 1 — Build a baseline

**Example commands**

```bash
date
hostnamectl
uname -a
uptime
free -h
df -hT
df -ih
```

**How to interpret**
- `hostnamectl` and `uname` provide host and kernel context.
- `uptime` reports load averages and uptime. Compare load with CPU count and I/O symptoms.
- `free -h`: examine `available` memory and swap use, not just `free`.
- `df -hT`: compare filesystem capacity and mount points.
- `df -ih`: look for high inode use.

**Example report:** “The root filesystem is at 72% and inode use is 18%. No immediate capacity issue is visible in this snapshot. Repeat during the reported slowdown to compare trends.” Use your actual observations.

## Lab 2 — Audit failed services

```bash
systemctl --failed
systemctl status SERVICE_NAME
journalctl -u SERVICE_NAME --since "1 hour ago" --no-pager
systemctl is-enabled SERVICE_NAME
```

- `active` describes current runtime state.
- `enabled` describes whether the unit is configured to start automatically through its enablement links.
- A service can be active but disabled, or enabled but currently inactive.
- If there are no failed units, report that honestly and inspect one relevant service anyway.

## Lab 3 — Filter journal entries

```bash
journalctl -b -p warning --no-pager -n 100
journalctl --since "today" --no-pager
```

For each relevant entry, record:
1. Timestamp and timezone context.
2. Unit/process or kernel component.
3. Severity and exact message (redact secrets).
4. Whether it repeats and whether it matches the incident window.
5. The next evidence source to consult.

Do not assume that a warning is a failure. Correlate it with impact and other logs.

## Lab 4 — Investigate disk usage

```bash
df -hT
df -ih
sudo du -xhd1 /var 2>/dev/null | sort -h
sudo lsof +L1
```

- High `df -hT` usage means allocated filesystem space is high.
- High `df -ih` usage means available file inodes are low.
- `du` identifies directories consuming space, subject to permissions and mount boundaries.
- `lsof +L1` may reveal deleted files still held open by processes.

**Safe response:** identify the owning service and growth pattern, preserve logs and evidence, check retention policy, confirm backups, and coordinate cleanup or log rotation. Verify capacity and application health afterward.

## Lab 5 — Diagnose a service port

```bash
systemctl status SERVICE_NAME
journalctl -u SERVICE_NAME --since "1 hour ago" --no-pager
sudo ss -ltnp
```

If the unit is active but no expected socket exists:
1. Check service configuration and startup logs.
2. Confirm the configured port and bind address.
3. Check whether the service listens on a different port or fails before binding.

If it listens only on `127.0.0.1`, remote clients cannot connect directly to that loopback-bound socket. Confirm intended architecture before changing the bind address; exposing a service publicly may create a security risk.

## Lab 6 — DNS and network checks

```bash
ip address
ip route
getent hosts example.com
ping -c 3 1.1.1.1
curl -I --max-time 10 https://example.com
```

Possible diagnostic branches:
- **No default route:** inspect network configuration and gateway reachability.
- **IP works but DNS fails:** inspect `/etc/resolv.conf`, system resolver status, configured DNS servers, and resolver logs.
- **DNS works but HTTPS fails:** inspect route, proxy, TLS errors, port filtering, server status, and application response.
- **Ping fails but HTTPS works:** ICMP may be filtered; ping alone is inconclusive.

Use an approved destination and compare against a known-good host when possible.

## Lab 7 — Permissions audit

```bash
namei -l /var/log
stat /var/log
find "$HOME" -maxdepth 2 -type f -perm -002 -print 2>/dev/null
```

`namei -l` shows permissions along the path; `stat` shows owner, group, and mode. A world-writable file is a candidate for review, not automatically a vulnerability. Verify the file's purpose, owner, access needs, and application requirements before changing permissions.

## Lab 8 — Authentication log review

```bash
sudo journalctl --since "today" --no-pager | grep -iE 'failed password|accepted publickey|authentication failure'
```

Record the time, account, source address if present, and surrounding events. Correlate with approved administration, VPN records, endpoint monitoring, and other logs. A failed attempt may be normal background noise; repeated attempts, successful unexpected logins, or unusual privilege changes deserve deeper investigation.

## Lab 9 — Kernel and reboot investigation

```bash
sudo journalctl -k --since "today" --no-pager
last -x | head -n 20
journalctl --list-boots
```

Look for timestamps near the incident and messages about I/O errors, filesystem issues, device resets, OOM kills, or hardware faults. These messages need context and may not establish causation. Corroborate with monitoring, hypervisor/cloud event logs, UPS logs, and application logs.

## Lab 10 — Create a diagnostic snapshot

Expected output includes files for system identity, uptime, memory, disk, inode use, block devices, processes, routes, addresses, sockets, failed units, and recent warnings.

The script uses `|| true` so one failed diagnostic command does not stop the entire collection. This also means its overall exit status may not reveal individual failures. Read each output file and note unavailable commands, permission errors, or empty results. Review and redact the bundle before sharing.

## Lab 11 — Disk nearly full

A reasonable read-only first pass:

```bash
date
df -hT
df -ih
sudo du -xhd1 /var 2>/dev/null | sort -h
sudo lsof +L1
sudo journalctl --since "1 hour ago" --no-pager
```

A safe plan:
1. Confirm affected mount, usage trend, and impact.
2. Identify the owning directory, process, or logging workload.
3. Preserve relevant logs and confirm retention/backups.
4. Agree on cleanup, rotation, or capacity expansion with the service owner.
5. Make one approved change and verify free space, application health, and new log behavior.

Avoid blanket deletion commands and do not remove files simply because they are large.

## Lab 12 — Service unreachable

Use a layered sequence:

```bash
systemctl status SERVICE_NAME
journalctl -u SERVICE_NAME --since "1 hour ago" --no-pager
sudo ss -ltnp
getent hosts APP_HOSTNAME
ip route
curl -I --max-time 5 http://127.0.0.1/
```

Then inspect host firewall policy, upstream ACLs/security groups, load balancer health, and remote client routing. A successful localhost test proves only that the local request succeeded through that path; it does not prove the service is reachable from another host.

## Lab 13 — Incident note

A strong note is factual and concise. Example structure:

```text
Incident: Web service timeout
Observed: Remote client times out at 14:05 local time.
Evidence: Unit active; expected TCP socket absent; service log reports configuration parse error.
Hypothesis: Service did not bind because configuration validation failed.
Action: Captured logs and config version; requested approval before changing configuration.
Verification: Pending approved fix; repeat local and remote requests after change.
Open questions: Confirm upstream firewall and load-balancer health.
```

This is illustrative only; replace every statement with evidence from your lab.

## Lab 14 — Repeatable audit checklist

Example entries:

| Check | Command | Expected observation | Escalate when |
|---|---|---|---|
| Identity | `hostnamectl` | Correct host and OS | Host identity unexpected |
| Uptime/load | `uptime` | Consistent with baseline | Sustained unexplained load |
| Failed units | `systemctl --failed` | No unexplained failures | Critical unit failed |
| Service logs | `journalctl -u SERVICE` | No relevant recurring errors | Errors align with impact |
| Memory | `free -h` | Adequate available memory | Low available memory plus symptoms |
| CPU | `top` | Expected workload | Sustained abnormal usage |
| Disk | `df -hT` | Capacity below alert threshold | Near full or rapidly growing |
| Inodes | `df -ih` | Inodes available | Inode use near exhaustion |
| Sockets | `ss -tulpn` | Expected ports only | Unexpected exposed listener |
| Routes | `ip route` | Expected routes | Missing or unexpected route |
| Accounts | `getent passwd` | Accounts align with baseline | Unknown or unauthorized account |
| Permissions | `namei -l PATH` | Access matches policy | Unexpected broad access |
| Auth events | `journalctl` / auth log | Expected access patterns | Unexpected successful access |
| Evidence | snapshot review | Sensitive fields redacted | Secret or personal data exposed |

Tune thresholds to your organization's baseline and policies.

## General troubleshooting answer format

For any incident, organize your response as:

1. **Symptom and scope**
2. **Time window and recent changes**
3. **Read-only evidence collected**
4. **Likely cause and confidence**
5. **Proposed action and risk**
6. **Approval / rollback plan**
7. **Verification and remaining risk**

A good troubleshooting result is reproducible, evidence-based, and safe—not simply a command that appears to make the error disappear.
