# ✅ Processes and Services — Solutions

Use these suggested solutions in a Linux lab. PIDs, output, available utilities, service names, and systemd behavior vary by environment.

## Lab 1 — Process identity

```bash
echo "$$"
ps -p "$$" -o pid,ppid,user,stat,comm
cat "/proc/$$/status"
```

- **PID:** Process identifier.
- **PPID:** Parent process identifier.
- `/proc/<PID>/status` exposes information about a process, subject to permissions and system configuration.

## Lab 2 — Process discovery

```bash
ps -ef
ps -eo pid,ppid,user,stat,%cpu,%mem,comm --sort=-%cpu | head
pgrep -a bash
pstree -p
```

If `pstree` is not installed, use:

```bash
ps -eo pid,ppid,comm --forest
```

A process listing is a snapshot. A process may exit or change resource usage immediately afterward.

## Lab 3 — Foreground and background jobs

Foreground:

```bash
sleep 300
```

Press `Ctrl+C` to interrupt.

Background:

```bash
sleep 300 &
test_pid=$!
jobs -l
ps -p "$test_pid" -o pid,ppid,stat,cmd
```

Terminate the lab process:

```bash
kill -TERM "$test_pid"
wait "$test_pid" 2>/dev/null || true
```

For interactive job control, run `sleep 300`, press `Ctrl+Z`, then inspect `jobs -l`, resume with `bg`, bring it back with `fg`, and press `Ctrl+C`.

## Lab 4 — Signals

```bash
sleep 300 &
test_pid=$!
kill -TERM "$test_pid"
wait "$test_pid" 2>/dev/null || true
ps -p "$test_pid"
```

After termination, `ps` should normally report that no matching process exists. A brief race or shell job-table behavior may affect the exact output.

`SIGTERM` requests a graceful exit. `SIGKILL` forces termination and cannot be handled by the target process, so it can prevent cleanup. Consider it only after confirming the target and trying normal termination.

## Lab 5 — Priority and resources

```bash
nice -n 10 sleep 60 &
test_pid=$!
ps -o pid,ni,stat,comm -p "$test_pid"
free -h
uptime
ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head
kill "$test_pid"
```

A high load average can reflect runnable tasks or tasks waiting on uninterruptible operations, such as some I/O waits. Check CPU, memory, and I/O context before deciding on a cause.

## Lab 6 — Service inspection

Check the init process:

```bash
ps -p 1 -o comm=
```

If systemd is active:

```bash
systemctl list-units --type=service
systemctl --failed
systemctl status SERVICE
systemctl is-active SERVICE
systemctl is-enabled SERVICE
```

Replace `SERVICE` with an installed unit name. `is-active` reports runtime state; `is-enabled` reports whether the unit is configured to start automatically. They are different properties.

If systemd is unavailable, document that limitation and use `ps` to inspect running processes.

## Lab 7 — Service logs

```bash
journalctl -b -n 100 --no-pager
journalctl -u SERVICE -n 50 --no-pager
journalctl -p err -b
```

Look for timestamps, exit status, missing files, permission errors, configuration parse errors, and dependency failures. Do not assume that every error message is the root cause; correlate logs with service status and configuration.

## Lab 8 — Troubleshooting scenario

A reasonable sequence is:

1. Confirm the exact unit name.
2. Run `systemctl status SERVICE`.
3. Read `journalctl -u SERVICE` for the relevant time window.
4. Inspect configuration with `systemctl cat SERVICE` and the application's own validation tool where available.
5. Verify ownership and permissions on required files.
6. Check relevant ports with `ss -tuln`.
7. Inspect dependencies with `systemctl list-dependencies SERVICE`.
8. Make a single evidence-based change in a lab.
9. Recheck service status and logs.

Avoid restarting services repeatedly without understanding the failure.

## Lab 9 — Example health report script

Save as `service-health-report.sh`:

```bash
#!/usr/bin/env bash

set -u

OUT="${HOME}/process-service-lab/service-health-report.txt"
SERVICE="${1:-}"

mkdir -p "$(dirname "$OUT")"

{
    echo "===== Service Health Report ====="
    echo "Generated: $(date)"
    echo "Hostname: $(hostname)"
    echo
    echo "===== Uptime ====="
    uptime
    echo
    echo "===== Memory ====="
    free -h 2>&1 || true
    echo
    echo "===== Top Processes by CPU ====="
    ps -eo pid,ppid,user,%cpu,%mem,stat,comm --sort=-%cpu | head -n 15
    echo
    echo "===== Service Status ====="

    if command -v systemctl >/dev/null 2>&1 &&
       systemctl is-system-running >/dev/null 2>&1; then
        if [[ -n "$SERVICE" ]]; then
            systemctl status "$SERVICE" --no-pager 2>&1 || true
            echo
            echo "===== Recent Service Logs ====="
            journalctl -u "$SERVICE" -n 30 --no-pager 2>&1 || true
        else
            echo "No service supplied. Run: $0 SERVICE_NAME"
        fi
    else
        echo "systemd is unavailable or not active in this environment."
    fi
} > "$OUT" 2>&1

chmod 600 "$OUT"
printf 'Report saved to %s\n' "$OUT"
```

Run it:

```bash
chmod u+x service-health-report.sh
./service-health-report.sh
```

Or specify an installed service:

```bash
./service-health-report.sh ssh
```

Replace `ssh` with a unit that exists on your system. On some distributions, the SSH service is named `sshd`. The script only inspects services; it does not change their state.

**Important:** A systemd service can be accessible even when `systemctl is-system-running` returns a degraded state. The example uses a simple check for learning purposes, not as a complete production health test.

## Reflection — Suggested answers

1. **Process:** A running instance of a program.
2. **PID vs PPID:** PID identifies the process; PPID identifies its parent.
3. **Background job vs service:** A shell background job is launched from a shell session; a service is managed by a service manager and may be started at boot or restarted according to its unit configuration.
4. **SIGTERM:** Requests graceful termination.
5. **SIGKILL:** It cannot be handled and can prevent cleanup, so use it only when necessary.
6. **`start` vs `enable`:** `start` changes runtime state; `enable` configures automatic activation at boot.
7. **`systemctl status`:** Shows service state, recent logs, and other unit details, depending on system and permissions.
8. **`journalctl`:** Filters system journal entries by unit, time, priority, or boot to help investigate failures.
9. **Log sensitivity:** Logs may reveal internal paths, hostnames, account names, tokens, or user data.
10. **Before restarting:** Verify the service identity, impact, logs, configuration, dependencies, and whether a restart is authorized.

## Completion criteria

You can inspect processes, manage a test process safely, distinguish service runtime state from boot enablement, read relevant logs, and describe a careful troubleshooting sequence.
