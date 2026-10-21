# 🧪 Processes and Services — Practical Labs

**Level:** Beginner to intermediate  
**Estimated time:** 60–90 minutes  
**Environment:** Linux VM or another authorized Linux host

## Safety rules

- Use harmless processes such as `sleep` for termination practice.
- Never kill a process solely because its name is unfamiliar.
- Do not stop, disable, or restart production services as part of these labs.
- Inspect a service before changing it; use a disposable VM for service-control practice.
- Some commands require `systemd`, `procps`, or `pstree`; alternatives may vary by distribution.

## Setup

```bash
mkdir -p ~/process-service-lab
cd ~/process-service-lab
printf 'Lab workspace: %s\n' "$PWD"
```

## Lab 1 — Process identity

**Tasks**

1. Print the current shell PID.
2. Show PID, PPID, user, state, and command for the shell.
3. Read the shell's `/proc` status file.
4. Explain PID and PPID.

**Hints:** `$$`, `ps`, `/proc`

## Lab 2 — Process discovery

**Tasks**

1. List all processes.
2. List processes sorted by CPU usage.
3. Find your current shell using `pgrep`.
4. Display a process tree if the required utility is installed.
5. Explain why process listings are snapshots.

**Hints:** `ps -ef`, `ps -eo`, `pgrep`, `pstree`

## Lab 3 — Foreground and background jobs

**Tasks**

1. Run `sleep 300` in the foreground.
2. Interrupt it with `Ctrl+C`.
3. Run it in the background.
4. Inspect the job list and PID.
5. Bring the job to the foreground and stop it.
6. Repeat by suspending a foreground job with `Ctrl+Z`, then resuming it with `bg`.

**Hints:** `&`, `jobs -l`, `fg`, `bg`

## Lab 4 — Signals

**Tasks**

1. Start a new `sleep 300` background process.
2. Record its PID using `$!`.
3. Send `SIGTERM` to that PID.
4. Verify that the test process has exited.
5. Explain when `SIGKILL` might be considered and why it should not be the first choice.

**Hints:** `kill -TERM`, `ps`, `wait`

## Lab 5 — Priority and resources

**Tasks**

1. Start a harmless `sleep` command with a non-default nice value.
2. Inspect its nice value.
3. Review CPU and memory usage of running processes.
4. Display memory and uptime.
5. Explain why a high load average does not automatically mean CPU saturation.

**Hints:** `nice`, `ps`, `free -h`, `uptime`

## Lab 6 — Service inspection

**Tasks**

1. Determine whether PID 1 is systemd.
2. List service units if systemd is active.
3. List failed units.
4. Choose an installed service and inspect its status.
5. Identify the service's main PID, if shown.
6. Record the unit's current active and enabled states.

**Hints:** `ps -p 1`, `systemctl list-units`, `systemctl status`, `systemctl is-enabled`

Do not alter a critical service to complete this lab.

## Lab 7 — Service logs

**Tasks**

1. Read recent system journal entries.
2. Read recent logs for the service selected in Lab 6.
3. Search the output for warnings or errors.
4. Write down one likely cause for a failure, if a genuine failure exists.
5. Redact sensitive data from any report.

**Hints:** `journalctl -b`, `journalctl -u`, `journalctl -p err`

If no service errors exist, record that fact instead of inventing a failure.

## Lab 8 — Troubleshooting scenario

**Scenario:** A service is reported as unavailable.

Write a troubleshooting checklist that includes:

1. Checking the service name and status.
2. Inspecting recent logs.
3. Confirming configuration files and permissions.
4. Checking whether a required port is listening.
5. Checking dependencies.
6. Making a controlled change only when supported by evidence.
7. Verifying service health afterward.

Use a lab service or a simulated report. Do not intentionally break a production service.

## Lab 9 — Mini project: Service health report

Create `service-health-report.sh` that records:

- Timestamp and hostname.
- Uptime.
- Memory summary.
- Top processes by CPU usage.
- Status of a service you choose, if systemd is available.
- Recent logs for that service, if available.

Requirements:

- Save output to a file in `~/process-service-lab`.
- Do not automatically start, stop, restart, or disable any service.
- Handle unavailable systemd commands gracefully.
- Treat the generated report as sensitive.

## Submission checklist

- [ ] Process IDs and parent IDs identified.
- [ ] Process listing and tree inspected.
- [ ] Background job started and stopped safely.
- [ ] `SIGTERM` practiced on a lab process.
- [ ] Priority and resource metrics inspected.
- [ ] Service status and enabled state recorded where systemd is available.
- [ ] Logs reviewed and sensitive data protected.
- [ ] Troubleshooting plan documented.
- [ ] Health-report script created and tested.

## Reflection questions

1. What is a process?
2. What is the difference between a PID and PPID?
3. How does a background shell job differ from a systemd service?
4. What does `SIGTERM` do?
5. Why should `SIGKILL` be a last resort?
6. What is the difference between `start` and `enable`?
7. What information does `systemctl status` provide?
8. How can `journalctl` help diagnose a service failure?
9. Why should logs be treated as potentially sensitive?
10. What should you verify before restarting a service?
