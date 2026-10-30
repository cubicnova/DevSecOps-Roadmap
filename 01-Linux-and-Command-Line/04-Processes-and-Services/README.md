# ⚙️ Processes and Services

[![Linux](https://img.shields.io/badge/Linux-Administration-FCC624?logo=linux&logoColor=black)](https://www.kernel.org/)
[![systemd](https://img.shields.io/badge/Service_Manager-systemd-blue)](https://systemd.io/)
[![Level](https://img.shields.io/badge/Level-Beginner_to_Intermediate-success)](.)

Welcome to **Processes and Services**, a module in the Linux and Command Line section of the **CubicNova DevSecOps Roadmap**. Learn how to inspect running processes, understand process states and signals, manage foreground and background jobs, operate systemd services, inspect logs, and troubleshoot common service failures.

These skills are essential for Linux administration, cloud operations, incident response, application deployment, and DevSecOps troubleshooting.

## 📚 Table of Contents

- [Learning Objectives](#-learning-objectives)
- [Prerequisites](#-prerequisites)
- [Processes vs Services](#-processes-vs-services)
- [Process Inspection](#-process-inspection)
- [Foreground and Background Jobs](#-foreground-and-background-jobs)
- [Signals and Process Control](#-signals-and-process-control)
- [Process Priority](#-process-priority)
- [Services with systemd](#-services-with-systemd)
- [Logs and Troubleshooting](#-logs-and-troubleshooting)
- [Resource Monitoring](#-resource-monitoring)
- [Security Best Practices](#-security-best-practices)
- [Hands-On Labs](#-hands-on-labs)
- [Mini Project](#-mini-project)
- [Module Files](#-module-files)
- [Learning Resources](#-learning-resources)
- [Next Steps](#-next-steps)

## 🎯 Learning Objectives

After completing this module, you should be able to:

1. Explain the difference between a process, a daemon, and a service.
2. Inspect process IDs, parent process IDs, users, states, and resource use.
3. Use `ps`, `top`, `pgrep`, `pstree`, and `/proc` for process inspection.
4. Start and manage background jobs in a shell.
5. Explain common signals and terminate processes safely.
6. Understand basic process priorities.
7. Inspect and manage services with `systemctl` on systemd-based systems.
8. Read service logs using `journalctl`.
9. Troubleshoot failed services using status, logs, and dependency information.
10. Apply least privilege and safe operational practices.

## 🧰 Prerequisites

- A Linux VM, WSL environment, or authorized Linux host.
- Basic command-line skills.
- Familiarity with files, directories, and permissions.
- `systemd` commands apply only where systemd is the active service manager; containers and some WSL environments may not run it as PID 1.

## 🔍 Processes vs Services

A **process** is a running instance of a program, usually identified by a process ID (PID). A process may have a parent process ID (PPID), user identity, state, and resource usage.

A **service** is a managed system function or application, commonly running in the background. On many Linux distributions, `systemd` manages services through unit files and the `systemctl` command. A service may supervise one or more processes, and a process can exist without being managed as a system service.

A **daemon** is a background program that provides a function, often independently of a user terminal.

## 🔎 Process Inspection

```bash
ps
ps -ef
ps aux
ps -eo pid,ppid,user,stat,%cpu,%mem,comm --sort=-%cpu
pgrep -a ssh
pstree -p
```

| Command | Purpose |
|---|---|
| `ps -ef` | Snapshot of processes in full-format output |
| `ps aux` | Common BSD-style process listing |
| `pgrep -a NAME` | Find processes by name and show command lines |
| `pstree -p` | Display process relationships, if installed |
| `top` | Interactive process and resource monitor |
| `pidof NAME` | Find PIDs for a program, where supported |

Useful `/proc` examples:

```bash
cat /proc/$$/status
readlink /proc/$$/exe
```

`$$` expands to the current shell's PID in Bash. Access to some process details may be restricted by permissions or system configuration.

## 🏃 Foreground and Background Jobs

Run a long-running, harmless test command:

```bash
sleep 300
```

Press `Ctrl+C` to interrupt it.

Run it in the background:

```bash
sleep 300 &
jobs -l
```

Bring the job to the foreground:

```bash
fg %1
```

Use `Ctrl+Z` to suspend a foreground job, then resume it in the background:

```bash
bg %1
```

Job numbers vary. Use `jobs -l` to confirm the correct job. Background jobs started from a shell are not necessarily managed system services and may end when the session closes.

## 🛑 Signals and Process Control

```bash
kill -l
pgrep -a sleep
kill PID
```

Replace `PID` with the actual PID of the process you started. `kill PID` normally sends `SIGTERM`, requesting graceful termination.

Common signals:

| Signal | Number | Purpose |
|---|---:|---|
| `SIGTERM` | 15 | Request a process to terminate gracefully |
| `SIGKILL` | 9 | Force termination; cannot be caught or ignored |
| `SIGINT` | 2 | Interrupt, commonly from `Ctrl+C` |
| `SIGHUP` | 1 | Hangup; some programs use it to reload configuration |

Use `kill -9 PID` only when normal termination fails and you understand the consequences. Never terminate a process solely because its name looks unfamiliar; identify its owner, command, and purpose first.

## ⚖️ Process Priority

Linux scheduling priorities influence how CPU time is allocated under contention.

```bash
nice -n 10 sleep 60 &
ps -o pid,ni,stat,comm -p "$!"
renice 5 -p PID
```

`$!` expands to the PID of the most recently started background process in Bash. Replace `PID` in the `renice` example with an actual process ID. Permission to change priority depends on user privileges and system policy.

## 🧩 Services with systemd

Check whether systemd is available:

```bash
ps -p 1 -o comm=
systemctl --version
```

Inspect services:

```bash
systemctl list-units --type=service
systemctl --failed
systemctl status cron
```

The example service name varies by distribution: some systems use `cron`, while others use `crond`. Choose a service that exists on your lab machine.

Common operations:

```bash
sudo systemctl start SERVICE
sudo systemctl stop SERVICE
sudo systemctl restart SERVICE
sudo systemctl reload SERVICE
sudo systemctl enable SERVICE
sudo systemctl disable SERVICE
```

Replace `SERVICE` with a real, appropriate service name. `start` and `stop` affect current runtime state; `enable` and `disable` affect whether the service is configured to start automatically at boot. Not every service supports `reload`.

Before changing a service, inspect it:

```bash
systemctl status SERVICE
systemctl cat SERVICE
systemctl is-enabled SERVICE
systemctl is-active SERVICE
```

## 📜 Logs and Troubleshooting

```bash
journalctl -b
journalctl -u SERVICE
journalctl -u SERVICE --since "1 hour ago"
journalctl -p warning -b
journalctl -n 100 --no-pager
```

A practical troubleshooting sequence:

1. Check the service status.
2. Read recent logs for the unit.
3. Confirm the service name and configuration.
4. Check dependencies, ports, files, and permissions as relevant.
5. Make one controlled change at a time.
6. Verify status and logs after the change.

Use `systemctl list-dependencies SERVICE` to inspect dependencies. Logs can contain sensitive information; do not publish them without review.

## 📈 Resource Monitoring

```bash
uptime
free -h
vmstat 1 5
ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head
df -h
```

- `uptime`: load averages and uptime.
- `free -h`: memory usage.
- `vmstat`: process, memory, and system statistics, if installed.
- `ps`: point-in-time process resource snapshot.
- `df -h`: filesystem capacity.

High load does not automatically mean a CPU problem; inspect CPU, memory, I/O, and workload context before drawing conclusions.

## 🛡️ Security Best Practices

- Run commands with the least privilege required.
- Inspect process identity and command line before taking action.
- Avoid killing unknown or critical processes.
- Prefer graceful termination before forceful termination.
- Do not disable security or logging services to hide errors.
- Validate service configuration before restarting production services.
- Restrict write access to service unit files and configuration.
- Review logs carefully and redact credentials, tokens, and personal data.
- Enable only services that are required for the machine's purpose.
- Test service changes in a lab before applying them to production.

## 🧪 Hands-On Labs

1. **Process discovery:** Find your shell PID and parent PID.
2. **Process tree:** Display process relationships.
3. **Background jobs:** Start `sleep`, inspect it, suspend it, resume it, and terminate it.
4. **Signals:** Send `SIGTERM` to a process you created and verify it exits.
5. **Resource monitoring:** Identify processes with the highest CPU or memory usage.
6. **Service inspection:** Find a service installed on your system and inspect its status.
7. **Log analysis:** Review the last entries for a selected service.
8. **Failure diagnosis:** Use a harmless test unit or a non-production service to practice status and log-based troubleshooting.

See [`practical.md`](practical.md) for detailed instructions and [`solutions.md`](solutions.md) for suggested solutions.

## 🚀 Mini Project: Service Health Report

Create a Bash script that generates a local report containing:

- Timestamp and hostname.
- Current uptime and memory summary.
- A process snapshot sorted by CPU usage.
- The state of a service you choose.
- Recent logs for that service, if available.

Keep the report local and treat it as potentially sensitive. Use a service that exists on your lab system. Do not automatically restart or disable services from the report script.

## 📂 Module Files

| File | Purpose |
|---|---|
| `README.md` | Concepts, commands, and overview |
| `examples.md` | Copyable process and service command examples |
| `practical.md` | Guided labs and challenges |
| `solutions.md` | Suggested answers and verification steps |

## 📚 Learning Resources

- [systemd documentation](https://systemd.io/) — system and service management.
- [systemd manual](https://www.freedesktop.org/software/systemd/man/latest/systemd.html) — units, dependencies, and service-manager concepts.
- [systemd.service manual](https://www.man7.org/linux/man-pages/man5/systemd.service.5.html) — service unit configuration.
- [ps manual](https://man7.org/linux/man-pages/man1/ps.1.html) — process reporting.
- [Linux man-pages](https://www.kernel.org/doc/man-pages/) — command and system-call reference.

## 🗺️ Next Steps

Continue with the next topic in the [Linux and Command Line](../README.md) section of the [CubicNova DevSecOps Roadmap](../../README.md).

**Observe carefully. Troubleshoot methodically. Operate securely.**
