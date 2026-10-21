# 🐧 Linux Fundamentals

[![Linux](https://img.shields.io/badge/Linux-Fundamentals-FCC624?logo=linux&logoColor=black)](https://www.kernel.org/)
[![Shell](https://img.shields.io/badge/Shell-Bash-4EAA25?logo=gnubash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Roadmap](https://img.shields.io/badge/Path-DevSecOps-blue)](../../README.md)
[![Level](https://img.shields.io/badge/Level-Beginner-success)](.)

Welcome to **Linux Fundamentals**, the first module in the Linux and Command Line section of the **CubicNova DevSecOps Roadmap**. This module introduces the Linux operating system, command-line interface, filesystem, user management, permissions, processes, and essential commands used in system administration, cybersecurity, and DevSecOps.

The goal is to build a strong Linux foundation before moving on to shell scripting, networking, security tools, automation, containers, and CI/CD pipelines.

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Learning Objectives](#-learning-objectives)
- [Prerequisites](#-prerequisites)
- [Topics Covered](#-topics-covered)
- [Linux Distributions](#-linux-distributions)
- [Environment Setup](#-environment-setup)
- [Essential Linux Commands](#-essential-linux-commands)
- [Filesystem Fundamentals](#-filesystem-fundamentals)
- [File Permissions](#-file-permissions)
- [Users and Groups](#-users-and-groups)
- [Processes and System Information](#-processes-and-system-information)
- [Package Management](#-package-management)
- [Linux Networking Basics](#-linux-networking-basics)
- [Security-Focused Commands](#-security-focused-commands)
- [Hands-On Labs](#-hands-on-labs)
- [Practice Exercises](#-practice-exercises)
- [Mini Project](#-mini-project)
- [Common Mistakes](#-common-mistakes)
- [Best Practices](#-best-practices)
- [Learning Resources](#-learning-resources)
- [Next Steps](#-next-steps)

---

## 🎯 Overview

Linux is an open-source, Unix-like operating system widely used in servers, cloud infrastructure, containers, embedded systems, and security environments.

Linux knowledge is essential for DevSecOps engineers because many build servers, cloud workloads, containers, monitoring systems, and security tools run on Linux.

In this module, you will learn how to:

- Navigate a Linux terminal.
- Create, read, modify, copy, move, and delete files.
- Understand the Linux directory structure.
- Manage users, groups, and file permissions.
- Inspect processes and system resources.
- Install and update software.
- Perform basic network troubleshooting.
- Apply fundamental Linux security practices.

## 🎓 Learning Objectives

After completing this module, you should be able to:

1. Explain the Linux architecture and the role of the kernel and shell.
2. Identify common Linux distributions and their use cases.
3. Execute commands and interpret their output.
4. Navigate the filesystem using absolute and relative paths.
5. Manage files, directories, and text files.
6. Explain ownership and permission bits.
7. Perform basic user and group administration.
8. Inspect processes, services, disk usage, and system information.
9. Use package managers to install and update software.
10. Apply basic security checks and troubleshoot common issues.

## 🧰 Prerequisites

No previous Linux experience is required.

Recommended:

- Basic computer knowledge.
- Access to a Linux terminal or virtual machine.
- Familiarity with installing applications.
- Curiosity about system administration and cybersecurity.

## 📖 Topics Covered

| Topic | Key Concepts |
|---|---|
| Linux Introduction | Kernel, shell, distributions, terminal |
| Command-Line Basics | Syntax, arguments, options, help |
| Filesystem | Root directory, paths, directory navigation |
| File Management | Create, copy, move, rename, delete |
| Text Processing | `cat`, `less`, `head`, `tail`, `grep` |
| Permissions | Read, write, execute, ownership, `chmod` |
| User Management | Users, groups, `sudo`, account information |
| Process Management | `ps`, `top`, `kill`, process IDs |
| System Administration | Disk usage, memory, services, logs |
| Package Management | `apt`, package installation and updates |
| Networking | IP addresses, DNS lookup, connectivity |
| Security Basics | Least privilege, permissions, audit checks |

---

## 🐧 Linux Distributions

A Linux distribution combines the Linux kernel with system utilities, package management, and other software.

| Distribution | Common Use Case |
|---|---|
| Ubuntu | Learning, servers, cloud, development |
| Debian | Stable servers and infrastructure |
| Kali Linux | Authorized penetration testing and security labs |
| Fedora | Development and modern Linux technologies |
| Red Hat Enterprise Linux | Enterprise infrastructure |
| Rocky Linux | Enterprise-compatible server environments |
| Arch Linux | Custom Linux environments and advanced learning |

### Check your Linux distribution

```bash
cat /etc/os-release
uname -a
hostnamectl
```

These commands show distribution details, kernel information, hostname, and related system properties.

## 💻 Environment Setup

You can practice using any of these environments:

- **Ubuntu VM:** Recommended for beginners.
- **Kali Linux VM:** Useful if you also want to learn security tooling.
- **WSL:** Run a Linux environment on Windows.
- **Cloud Linux VM:** Practice on a remote server you own or are authorized to access.

### Verify your environment

```bash
whoami
pwd
uname -r
echo "$SHELL"
```

Expected results vary by operating system and configuration.

---

## ⌨️ Essential Linux Commands

### 1. Navigation

| Command | Purpose | Example |
|---|---|---|
| `pwd` | Print current directory | `pwd` |
| `ls` | List directory contents | `ls -la` |
| `cd` | Change directory | `cd /etc` |
| `tree` | Display directory tree | `tree -L 2` |
| `clear` | Clear terminal display | `clear` |

### 2. File and directory management

| Command | Purpose | Example |
|---|---|---|
| `touch` | Create an empty file | `touch notes.txt` |
| `mkdir` | Create a directory | `mkdir practice` |
| `cp` | Copy files | `cp notes.txt backup.txt` |
| `mv` | Move or rename files | `mv notes.txt linux-notes.txt` |
| `rm` | Remove files | `rm backup.txt` |
| `rmdir` | Remove an empty directory | `rmdir empty-folder` |
| `file` | Identify file type | `file linux-notes.txt` |
| `stat` | Display file metadata | `stat linux-notes.txt` |

**Warning:** Commands such as `rm` can permanently remove files. Verify paths before running destructive commands, particularly when using recursive or force options.

### 3. Viewing and searching files

| Command | Purpose | Example |
|---|---|---|
| `cat` | Display file contents | `cat notes.txt` |
| `less` | Read a file interactively | `less /var/log/syslog` |
| `head` | Display first lines | `head -n 10 notes.txt` |
| `tail` | Display last lines | `tail -n 20 notes.txt` |
| `grep` | Search matching text | `grep "error" app.log` |
| `find` | Search for files | `find . -type f -name "*.txt"` |
| `wc` | Count lines, words, bytes | `wc -l notes.txt` |
| `sort` | Sort text lines | `sort names.txt` |
| `uniq` | Remove adjacent duplicates | `sort names.txt \| uniq` |

### 4. Help and command discovery

```bash
man ls
ls --help
type cd
which python3
history
```

Useful tips:

- Use `man COMMAND` to read a command's manual page.
- Use `COMMAND --help` when supported.
- Use `type COMMAND` to identify aliases, built-ins, functions, or executable commands.
- Use `history` to review recent commands.

---

## 📁 Filesystem Fundamentals

Linux uses a hierarchical filesystem that begins at the root directory `/`.

| Directory | Purpose |
|---|---|
| `/` | Filesystem root |
| `/home` | Regular users' home directories |
| `/root` | Root user's home directory |
| `/etc` | System configuration files |
| `/var` | Variable data, logs, caches |
| `/tmp` | Temporary files |
| `/usr` | User-space programs and shared resources |
| `/bin` | Essential user commands on many systems; may link to `/usr/bin` |
| `/sbin` | System administration commands; may link to `/usr/sbin` |
| `/opt` | Optional application software |
| `/dev` | Device files |
| `/proc` | Process and kernel information |
| `/sys` | Kernel and device information |
| `/mnt` | Common mount point for temporary mounts |
| `/media` | Common mount point for removable media |

### Absolute and relative paths

An **absolute path** begins at `/`.

```bash
cd /etc
```

A **relative path** is interpreted from your current working directory.

```bash
cd ..
cd ./practice
cd ~
```

### Practice

```bash
mkdir -p ~/linux-labs/files
cd ~/linux-labs/files
touch first.txt second.txt
ls -la
pwd
```

---

## 🔐 File Permissions

Linux permissions determine who can read, modify, or execute a file.

Three permission classes:

- **User (`u`):** File owner.
- **Group (`g`):** Associated group.
- **Others (`o`):** Everyone else.

Three basic permissions:

| Permission | Symbol | Numeric Value | Meaning |
|---|---|---:|---|
| Read | `r` | 4 | Read file contents or list directory entries |
| Write | `w` | 2 | Modify a file or directory entries |
| Execute | `x` | 1 | Execute a file or traverse a directory |

### Inspect permissions

```bash
ls -l
stat first.txt
```

Example:

```text
-rw-r--r-- 1 user user 0 Oct 21 10:00 first.txt
```

The permissions `rw-r--r--` mean that the owner can read and write, while the group and others can read.

### Change permissions

```bash
chmod 644 first.txt
chmod 600 first.txt
chmod u+x script.sh
```

- `644`: Owner can read and write; group and others can read.
- `600`: Only the owner can read and write.
- `u+x`: Adds execute permission for the owner.

### Change ownership

```bash
sudo chown username:groupname first.txt
```

Replace `username` and `groupname` with valid account and group names.

**Security tip:** Avoid making files world-writable or using `chmod 777` as a generic fix. Grant only the permissions needed.

---

## 👥 Users and Groups

Linux supports multiple users, each with a user ID (UID), and groups, each with a group ID (GID).

### Inspect user information

```bash
whoami
id
who
groups
getent passwd
getent group
```

### User administration examples

On Debian- and Ubuntu-based systems:

```bash
sudo adduser labuser
sudo usermod -aG sudo labuser
id labuser
```

The second command adds `labuser` to the `sudo` group. Elevated privileges should be assigned only when required.

### Important concepts

- Root is the superuser, traditionally UID `0`.
- `sudo` allows authorized users to run commands with elevated privileges.
- Group membership can control access to files and resources.
- `/etc/passwd` stores account information; password hashes are not normally stored in this file.
- `/etc/shadow` stores protected password-related information on typical Linux systems.

Never share password hashes, private keys, or sensitive account information.

---

## ⚙️ Processes and System Information

A process is an executing program identified by a process ID (PID).

### Monitor system resources

```bash
ps aux
top
free -h
df -h
du -sh ~/linux-labs
uptime
```

| Command | Purpose |
|---|---|
| `ps aux` | List running processes |
| `top` | Monitor processes and system activity |
| `free -h` | Display memory usage |
| `df -h` | Display filesystem capacity |
| `du -sh PATH` | Estimate disk usage |
| `uptime` | Show uptime and load averages |
| `lscpu` | Display CPU information |
| `lsblk` | List block devices |

### Process management

```bash
sleep 300 &
jobs
pgrep -a sleep
```

Find the relevant PID and terminate only the process you started:

```bash
kill PID
```

Replace `PID` with the actual process ID. Use `kill -9` only as a last resort when normal termination fails.

### Inspect services

On systems using systemd:

```bash
systemctl status
systemctl --type=service --state=running
```

Inspect logs when troubleshooting:

```bash
journalctl -n 50
journalctl -p err -b
```

Some commands may require `sudo` or may be unavailable in minimal containers.

---

## 📦 Package Management

Package managers install, update, and remove software using the distribution's repositories.

### Ubuntu and Debian

```bash
sudo apt update
sudo apt upgrade
sudo apt install curl git tree
apt search package-name
apt show curl
```

`apt update` refreshes package indexes. `apt upgrade` upgrades installed packages where supported by the package manager's dependency rules.

### Fedora and RHEL-family systems

```bash
sudo dnf check-update
sudo dnf install curl git tree
sudo dnf info curl
```

Only install software from trusted repositories or verified sources.

---

## 🌐 Linux Networking Basics

Linux commands help you inspect interfaces, routes, DNS, and connectivity.

```bash
ip addr
ip route
ip link
hostname
getent hosts example.com
```

### Test network connectivity

```bash
ping -c 4 127.0.0.1
curl -I https://example.com
ss -tuln
```

| Command | Purpose |
|---|---|
| `ip addr` | Inspect network interfaces and addresses |
| `ip route` | View routing table |
| `getent hosts` | Resolve host information using system name-service configuration |
| `ping` | Test ICMP reachability when permitted |
| `curl -I` | Inspect HTTP response headers |
| `ss -tuln` | List listening TCP and UDP sockets |

Network utilities and options can vary by distribution. A failed ping does not necessarily mean a host is offline because ICMP may be filtered.

---

## 🛡️ Security-Focused Commands

These commands introduce basic system inspection for defensive security and authorized lab work.

### 1. Check the current identity

```bash
whoami
id
sudo -l
```

Use `sudo -l` to inspect the current account's permitted elevated commands when authorized.

### 2. Review file permissions

```bash
ls -l ~/.ssh
stat ~/.ssh
```

Private SSH keys should be protected from access by other users. A typical private key permission is `600`, while the `.ssh` directory commonly uses `700`.

### 3. Inspect listening services

```bash
ss -tuln
```

Identify services that are listening and confirm that they are intentionally exposed.

### 4. Review system logs

```bash
journalctl -p warning -b
```

On Debian- or Ubuntu-based systems where the file exists:

```bash
sudo tail -n 50 /var/log/auth.log
```

Log locations and permissions vary across distributions. Treat logs as sensitive data.

### 5. Check file integrity

```bash
sha256sum first.txt
```

Save the hash and compare it against a trusted reference to detect unexpected changes. A hash alone does not establish that a file is trustworthy.

### 6. Inspect scheduled jobs

```bash
crontab -l
systemctl list-timers
```

Review scheduled tasks for unexpected entries during an authorized system audit.

---

## 🧪 Hands-On Labs

Complete these labs in your own Linux VM or another environment you are authorized to administer.

### Lab 1: Explore the system

**Tasks:**

1. Identify the Linux distribution.
2. Find the kernel version.
3. Display the current user.
4. Find the current working directory.
5. List files, including hidden files, in your home directory.

**Commands:**

```bash
cat /etc/os-release
uname -r
whoami
pwd
ls -la ~
```

### Lab 2: Create a practice workspace

**Tasks:**

1. Create a `devsecops-lab` directory.
2. Create `notes.txt` and `commands.txt`.
3. Copy the notes file.
4. Rename the copy.
5. Display the final directory contents.

```bash
mkdir -p ~/devsecops-lab
cd ~/devsecops-lab
touch notes.txt commands.txt
cp notes.txt notes-backup.txt
mv notes-backup.txt notes-copy.txt
ls -la
```

### Lab 3: Practice permissions

**Tasks:**

1. Create a file named `secret.txt`.
2. Set permissions to `600`.
3. Verify the result.
4. Explain why these permissions are appropriate for a private file.

```bash
touch ~/devsecops-lab/secret.txt
chmod 600 ~/devsecops-lab/secret.txt
stat ~/devsecops-lab/secret.txt
```

Use dummy content only; do not put real passwords or secrets in the lab file.

### Lab 4: Search system logs

**Tasks:**

1. Display the last 20 lines of an accessible log.
2. Search for occurrences of `error`.
3. Count matching lines.
4. Explain what the results indicate.

```bash
tail -n 20 /var/log/syslog
grep -i "error" /var/log/syslog
grep -ic "error" /var/log/syslog
```

The example path is common on some Debian- and Ubuntu-based systems. If the file is absent or inaccessible, use an available log file or `journalctl`.

### Lab 5: Inspect processes and network services

**Tasks:**

1. List running processes.
2. Identify a process by name.
3. Inspect listening sockets.
4. Record the services you recognize.
5. Investigate any unexpected listener in your own lab.

```bash
ps aux
pgrep -a bash
ss -tuln
```

### Lab 6: Practice safe user administration

On a disposable VM, create a temporary user, inspect its UID and groups, and remove the user when finished.

```bash
sudo adduser labuser
id labuser
groups labuser
```

Clean up only after verifying that the account is the temporary account you created:

```bash
sudo deluser labuser
```

This example applies to Debian- and Ubuntu-based systems. Other distributions use different account-management commands.

---

## 📝 Practice Exercises

Try solving these without looking at the examples above.

1. Display the current date and time.
2. Find your current shell.
3. Create a directory structure with three nested directories.
4. Create a file and append text to it.
5. Search for `.log` files under a practice directory.
6. Count the number of lines in a text file.
7. Explain the difference between `>` and `>>`.
8. Explain the difference between `chmod` and `chown`.
9. Find the disk usage of your home directory.
10. Identify the PID of a running process.
11. Find listening network sockets.
12. Explain why running every command with `sudo` is a bad practice.
13. Describe how Linux permissions protect sensitive files.
14. Identify an error message in a sample log.
15. Explain the difference between an absolute and a relative path.

### Bonus: Pipes and redirection

```bash
echo "Linux Fundamentals" > notes.txt
echo "DevSecOps Practice" >> notes.txt
cat notes.txt
grep "Linux" notes.txt
```

- `>` creates or overwrites a file.
- `>>` appends output to a file.
- `|` passes one command's standard output to another command's standard input.

Always check the target file before using overwrite redirection.

---

## 🚀 Mini Project: Linux System Information Report

### Objective

Create a Bash script that generates a basic system information report for your local lab machine.

### Requirements

The report should include:

- Date and time.
- Hostname and current user.
- Distribution and kernel version.
- Memory usage.
- Disk usage.
- Current uptime.
- Listening network sockets.

### Example script

Create `system-report.sh`:

```bash
#!/usr/bin/env bash

set -u

REPORT="system-report.txt"

{
    echo "===== Linux System Information Report ====="
    echo "Generated: $(date)"
    echo "Hostname: $(hostname)"
    echo "Current user: $(whoami)"
    echo
    echo "===== Operating System ====="
    cat /etc/os-release
    echo
    echo "===== Kernel ====="
    uname -r
    echo
    echo "===== Uptime ====="
    uptime
    echo
    echo "===== Memory ====="
    free -h
    echo
    echo "===== Disk Usage ====="
    df -h
    echo
    echo "===== Listening Sockets ====="
    ss -tuln
} > "$REPORT" 2>&1

echo "Report saved to: $REPORT"
```

Run the script:

```bash
chmod u+x system-report.sh
./system-report.sh
less system-report.txt
```

### Expected outcome

The script creates a text report containing basic system information for review.

**Security considerations:**

- Run it only on systems you are authorized to inspect.
- Treat the report as potentially sensitive because it can reveal system configuration.
- Review the output before sharing it.
- Do not add passwords, access tokens, or private keys to the report.

---

## ⚠️ Common Mistakes

| Mistake | Better Approach |
|---|---|
| Running commands in the wrong directory | Check `pwd` before file operations |
| Using `rm -rf` without verifying paths | Inspect the target and use safer alternatives |
| Applying `chmod 777` to fix access problems | Grant only required permissions |
| Running everything as root | Use a normal account and elevate only when needed |
| Overwriting files accidentally | Understand `>` versus `>>` |
| Assuming every distribution has the same tools | Check installed utilities and distribution documentation |
| Ignoring error messages | Read the error and inspect command options |
| Installing packages from unknown sources | Prefer trusted repositories |
| Exposing secrets in logs or reports | Review and protect generated output |

---

## ✅ Best Practices

- Practice on a virtual machine or isolated lab environment.
- Learn command syntax, options, and exit codes.
- Use manual pages to understand unfamiliar commands.
- Follow the principle of least privilege.
- Keep your operating system and packages updated.
- Protect sensitive files using appropriate ownership and permissions.
- Inspect commands before executing them with elevated privileges.
- Back up important data before system changes.
- Avoid copying commands from untrusted sources without understanding them.
- Document your lab exercises and troubleshooting steps.

---

## 📚 Learning Resources

1. [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/) — shell syntax, commands, scripting, and built-in features.
2. [Linux man-pages project](https://www.kernel.org/doc/man-pages/) — reference documentation for Linux commands and system interfaces.
3. [Linux Kernel Documentation](https://docs.kernel.org/) — kernel concepts and technical documentation.
4. [Ubuntu Documentation](https://documentation.ubuntu.com/) — Ubuntu system administration and troubleshooting.
5. [Debian Documentation](https://www.debian.org/doc/) — Debian installation, administration, and package management.

---

## 🗺️ Next Steps

After completing this module, continue through the DevSecOps roadmap:

1. **Linux and Command Line:** Build confidence with everyday Linux commands.
2. **Shell Scripting:** Automate repetitive tasks using Bash.
3. **Networking Fundamentals:** Learn TCP/IP, DNS, ports, routing, and troubleshooting.
4. **Git and Version Control:** Manage code and configuration changes.
5. **Security Fundamentals:** Apply access control, system hardening, and secure configuration.
6. **Containers and CI/CD:** Progress toward Docker, Kubernetes, and automated security pipelines.

Return to the [Linux and Command Line](../README.md) section or the [DevSecOps Roadmap](../../README.md) to continue learning.

---

## 🤝 Contributing

Contributions are welcome! You can improve this module by:

- Adding beginner-friendly examples.
- Improving lab instructions.
- Fixing errors or broken links.
- Adding exercises and solutions.
- Sharing tested commands and troubleshooting tips.

Please follow the repository's contribution guidelines before submitting changes.

## 📄 License

This module is part of the [CubicNova DevSecOps Roadmap](https://github.com/cubicnova/DevSecOps-Roadmap). Refer to the repository's license for usage and distribution terms.

---

**Maintained by [CubicNova](https://github.com/cubicnova)**

*Learn Linux. Automate intelligently. Build securely.*
