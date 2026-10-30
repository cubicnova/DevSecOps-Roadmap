# Practical Labs — Audit and Troubleshooting

Complete these labs on a personal Linux VM, container, or explicitly authorized test machine. Prefer read-only inspection. Do not intentionally break a production system.

## Lab 1 — Build a baseline

**Goal:** Record system identity and resource health.

Run:

```bash
date
hostnamectl
uname -a
uptime
free -h
df -hT
df -ih
```

**Tasks**
1. Record hostname, kernel version, uptime, and load average.
2. Identify the filesystem with the highest usage percentage.
3. Check whether any filesystem has high inode use.
4. Explain why low `free` RAM does not automatically mean memory pressure.

**Deliverable:** A short baseline report with command output summarized.

## Lab 2 — Audit failed services

**Goal:** Identify failed systemd units.

```bash
systemctl --failed
systemctl list-units --type=service --state=running
```

**Tasks**
1. Record failed units, if any.
2. Pick one running service and inspect its status.
3. Find its recent logs.
4. Explain the difference between a service being `enabled` and `active`.

Do not stop or restart services just to create a failure.

## Lab 3 — Filter journal entries

**Goal:** Practice time-bounded log review.

```bash
journalctl -b -p warning --no-pager -n 100
journalctl --since "today" --no-pager | tail -n 50
```

**Tasks**
1. Identify up to three entries that warrant further investigation.
2. Record timestamp, component, severity, and message.
3. Determine whether each is still relevant or may be a known/benign warning.
4. State what additional evidence you would collect.

If no warnings appear, record that result and use a lab log file containing sample messages instead.

## Lab 4 — Investigate disk usage

**Goal:** Compare filesystem capacity, inode use, and directory usage.

```bash
df -hT
df -ih
sudo du -xhd1 /var 2>/dev/null | sort -h
```

**Tasks**
1. Record the filesystem containing `/var`.
2. Identify the largest visible top-level directory under `/var`.
3. Explain how inode exhaustion differs from byte exhaustion.
4. Propose safe next steps if `/var` is nearly full.

Do not delete logs, package caches, or application data without understanding retention and service requirements.

## Lab 5 — Diagnose a service port

**Goal:** Trace a service from systemd to socket state.

Choose a service already installed on your lab system.

```bash
systemctl status SERVICE_NAME
journalctl -u SERVICE_NAME --since "1 hour ago" --no-pager
sudo ss -ltnp
```

**Tasks**
1. Confirm whether the service is active.
2. Identify the expected listening port from its configuration or documentation.
3. Determine whether a matching socket is listening.
4. If it is listening only on `127.0.0.1`, explain what that means for remote clients.
5. Write the next three diagnostic steps.

Replace `SERVICE_NAME` with a real unit. Do not paste the placeholder literally.

## Lab 6 — DNS and network checks

**Goal:** Separate name-resolution failures from routing and application failures.

```bash
ip address
ip route
getent hosts example.com
ping -c 3 1.1.1.1
curl -I --max-time 10 https://example.com
```

**Tasks**
1. Record whether a default route exists.
2. Record whether the hostname resolves.
3. Explain what each command can and cannot prove.
4. Provide a diagnostic branch for: IP connectivity works, but DNS lookup fails.
5. Note that ICMP may be blocked even when HTTPS works.

Use approved destinations only.

## Lab 7 — Permissions audit

**Goal:** Inspect permissions on a chosen directory.

```bash
namei -l /var/log
stat /var/log
find "$HOME" -maxdepth 2 -type f -perm -002 -print 2>/dev/null
```

**Tasks**
1. Explain owner, group, and mode bits for one path.
2. Identify any files in your home directory that are world-writable.
3. Decide whether each finding is expected.
4. Suggest a least-privilege remediation only where justified.

Do not change permissions on system directories as part of this lab.

## Lab 8 — Authentication log review

**Goal:** Identify authentication-related events.

```bash
sudo journalctl --since "today" --no-pager | grep -iE 'failed password|accepted publickey|authentication failure'
```

**Tasks**
1. Record the time and account for any matching event.
2. Determine whether the event is expected, suspicious, or inconclusive.
3. List evidence that would help validate the event.
4. Explain why failed logins alone do not establish a compromise.

Logs and message formats vary across distributions.

## Lab 9 — Kernel and reboot investigation

**Goal:** Review kernel warnings and previous boot evidence.

```bash
sudo journalctl -k --since "today" --no-pager
last -x | head -n 20
journalctl --list-boots
```

**Tasks**
1. Identify kernel messages that might relate to hardware, storage, or memory.
2. Find the most recent reboot recorded by `last`, if available.
3. Check whether previous-boot journal data is retained.
4. List two other evidence sources you would check for an unexpected restart.

## Lab 10 — Create a diagnostic snapshot

**Goal:** Produce a repeatable support bundle.

Create `collect-audit.sh` using the script in `README.md`, then run:

```bash
chmod 700 collect-audit.sh
./collect-audit.sh ./audit-output
```

**Tasks**
1. Confirm the output directory contains reports for system identity, memory, disk, processes, network, and failed units.
2. Note commands that were unavailable or returned limited data.
3. Inspect the files for sensitive details before sharing.
4. Explain why the script uses `|| true` and why this can hide command failures unless the output is reviewed.

## Lab 11 — Troubleshooting scenario: disk nearly full

**Scenario:** A server alert reports `/var` at 97% capacity. An application has begun logging errors.

**Tasks**
1. Write the first five read-only commands you would run.
2. Explain how you would distinguish large files from inode exhaustion.
3. Describe how to investigate deleted-but-open files.
4. Provide a safe remediation plan with approvals and verification.
5. List the evidence to preserve before any cleanup.

## Lab 12 — Troubleshooting scenario: service unreachable

**Scenario:** A web application times out from another host, but a local user says it worked earlier.

**Tasks**
1. Check service state and recent logs.
2. Check listening sockets and bind address.
3. Check DNS resolution and routing.
4. Check host firewall and upstream network controls.
5. Explain why a successful localhost request is not enough to prove remote reachability.

## Lab 13 — Write an incident note

Use the template in `examples.md` to document one of the scenarios above. Clearly label:
- Confirmed observations
- Hypotheses
- Actions taken
- Verification
- Unresolved questions and next steps

## Lab 14 — Build a repeatable audit checklist

Create `audit-checklist.md` containing at least 12 checks grouped into:
- System identity and uptime
- Services and logs
- CPU and memory
- Storage and inodes
- Network and listening ports
- Accounts and permissions
- Evidence handling

For each check, include the command, expected observation, and escalation condition.

## Submission checklist

- [ ] Baseline report saved.
- [ ] Service and log review completed.
- [ ] Disk and inode analysis completed.
- [ ] Network troubleshooting notes completed.
- [ ] Permissions and authentication review documented.
- [ ] Diagnostic snapshot created and reviewed for sensitive data.
- [ ] Incident note includes evidence and verification.
