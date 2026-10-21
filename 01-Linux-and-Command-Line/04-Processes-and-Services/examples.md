# 💡 Processes and Services — Examples

Run these examples on a Linux machine you are authorized to administer. Service names and available commands vary by distribution.

## 1. Inspect your shell

```bash
echo "Shell PID: $$"
ps -p "$$" -o pid,ppid,user,stat,comm
cat "/proc/$$/status"
```

`$$` is the current Bash process ID. The process status file exposes fields such as PID, PPID, and state.

## 2. List and filter processes

```bash
ps -ef
ps aux
ps -eo pid,ppid,user,stat,%cpu,%mem,comm --sort=-%cpu | head
pgrep -a bash
```

`ps` produces a snapshot; `top` provides an interactive, repeatedly refreshed view.

## 3. Inspect process relationships

```bash
pstree -p
ps -eo pid,ppid,comm --forest
```

`pstree` may need to be installed separately. The `--forest` option is supported by common procps versions.

## 4. Practice a background job

```bash
sleep 300 &
jobs -l
pgrep -a sleep
```

Capture the PID immediately if needed:

```bash
sleep 300 &
test_pid=$!
echo "$test_pid"
ps -p "$test_pid" -o pid,stat,cmd
```

Stop only the test process you created:

```bash
kill "$test_pid"
wait "$test_pid" 2>/dev/null || true
```

## 5. Practice job control

Start a foreground job:

```bash
sleep 300
```

Press `Ctrl+Z` to suspend it. Then:

```bash
jobs -l
bg %1
jobs -l
fg %1
```

Press `Ctrl+C` to stop it. Job number `%1` is only an example; check `jobs -l` for the actual number.

## 6. Learn about signals

```bash
kill -l
sleep 300 &
test_pid=$!
kill -TERM "$test_pid"
wait "$test_pid" 2>/dev/null || true
```

`SIGTERM` requests graceful termination. Use `SIGKILL` only as a last resort, and only after confirming the correct PID.

## 7. Check process priority

```bash
nice -n 10 sleep 60 &
test_pid=$!
ps -o pid,ni,stat,comm -p "$test_pid"
kill "$test_pid"
```

A higher nice value generally means lower scheduling priority under CPU contention. Priority changes may require privileges.

## 8. Check whether systemd is active

```bash
ps -p 1 -o comm=
systemctl --version
systemctl is-system-running
```

If `systemctl` reports that the system has not been booted with systemd, use process-inspection commands instead or practice in a suitable VM.

## 9. Inspect service units

```bash
systemctl list-units --type=service
systemctl --failed
systemctl status SERVICE
systemctl cat SERVICE
systemctl is-enabled SERVICE
systemctl is-active SERVICE
```

Replace `SERVICE` with a valid unit name. Inspect before changing anything.

## 10. Manage a service carefully

For a service you are authorized to manage:

```bash
sudo systemctl start SERVICE
sudo systemctl status SERVICE
```

Other common operations are:

```bash
sudo systemctl stop SERVICE
sudo systemctl restart SERVICE
sudo systemctl reload SERVICE
sudo systemctl enable SERVICE
sudo systemctl disable SERVICE
```

Not every service supports `reload`. `enable` does not necessarily start a service immediately; use `start` for the current runtime state.

## 11. Read logs

```bash
journalctl -b -n 100 --no-pager
journalctl -u SERVICE -n 50 --no-pager
journalctl -u SERVICE --since "30 minutes ago"
journalctl -p err -b
```

Journal access can be restricted. Logs may contain secrets, usernames, internal hostnames, or other sensitive data.

## 12. Monitor system resources

```bash
uptime
free -h
vmstat 1 5
ps -eo pid,comm,%cpu,%mem --sort=-%mem | head
```

`vmstat` may not be installed by default. Interpret metrics in context rather than relying on a single number.

## 13. Troubleshooting checklist

- Confirm the exact PID or service name.
- Check the process owner and full command line.
- Inspect service status and recent logs.
- Check configuration syntax and file permissions.
- Check required ports, files, and dependencies.
- Make one controlled change at a time.
- Verify the result and preserve useful logs.
