# Linux and Command-Line Labs

![Linux](https://img.shields.io/badge/Linux-Hands--On%20Labs-FCC624?logo=linux&logoColor=black)
![Level](https://img.shields.io/badge/Level-Beginner%20to%20Intermediate-blue)
![Focus](https://img.shields.io/badge/Focus-DevSecOps%20%7C%20Linux%20Administration-red)

## Overview

This lab collection provides practical exercises for the **Linux and Command Line** section of the CubicNova DevSecOps Roadmap. It reinforces terminal fundamentals, filesystem navigation, users and permissions, package management, environment variables, and basic system hardening.

Run the exercises only on a Linux VM, disposable container, or system you are authorized to administer. Some tasks use `sudo`; read every command and inspect its target before execution.

## Learning Objectives

By completing these labs, you will be able to:

- Navigate the Linux filesystem and manipulate files safely.
- Inspect users, groups, ownership, and permissions.
- Search for files and process command output using pipes and filters.
- Install and inspect packages with the distribution's package manager.
- Use shell variables and environment variables in scripts.
- Inspect processes, services, listening ports, and logs.
- Recognize risky permissions and basic host-hardening opportunities.
- Document evidence, findings, and safe remediation steps.

## Suggested Lab Structure

Each lab can be saved as a separate Markdown file. The following structure is recommended:

```text
labs/
├── README.md
├── 01-command-line-basics.md
├── 02-files-and-directories.md
├── 03-users-groups-permissions.md
├── 04-package-management.md
├── 05-environment-variables.md
├── 06-processes-and-services.md
├── 07-system-hardening.md
└── lab-report-template.md
```

This archive includes the README, a lab workbook, a solutions guide, and a reusable report template.

## Prerequisites

- A Linux VM running Ubuntu, Debian, or Kali Linux.
- A non-root account with `sudo` access for selected administrative exercises.
- Basic terminal familiarity.
- A snapshot or backup before system-level changes.
- A text editor and a place to save lab notes.

## Lab Index

| Lab | Topic | Key skills |
|---|---|---|
| 1 | Command-Line Basics | `pwd`, `whoami`, `man`, pipes, redirection |
| 2 | Files and Directories | `ls`, `mkdir`, `cp`, `mv`, `find` |
| 3 | Users, Groups and Permissions | `id`, `useradd`, `chmod`, `chown`, `umask` |
| 4 | Package Management | `apt`, `dpkg`, package metadata |
| 5 | Environment Variables | `export`, `env`, `PATH`, Bash configuration |
| 6 | Processes and Services | `ps`, `top`, `systemctl`, `journalctl`, `ss` |
| 7 | System Hardening | account review, firewall audit, SSH review, logs |

## How to Use This Collection

1. Read the task and its safety notes.
2. Predict what each command will do.
3. Run the exercise in your lab environment.
4. Record the command, output, and what you learned.
5. Compare your results with `solutions.md`.
6. Clean up only the dedicated test files, accounts, and groups you created.

## Safety Rules

- Do not run destructive commands on production systems.
- Never test account deletion, recursive permission changes, firewall rules, or SSH changes on a remote production host.
- Review package-manager transaction summaries before confirming.
- Do not add unknown repositories or disable package-signature verification to bypass errors.
- Do not use real passwords, tokens, or API keys in lab files.
- Avoid copying logs or environment dumps into public repositories without redacting sensitive data.
- Treat the solutions as examples and adapt them to the distribution and lab requirements.

## Recommended Evidence for Each Lab

For each exercise, record:

- **Objective:** What are you testing?
- **Environment:** Distribution and version.
- **Commands:** Commands actually run.
- **Output:** Relevant, redacted output.
- **Result:** Pass, partial, or blocked.
- **Explanation:** What the result means.
- **Remediation:** Any recommended improvement.
- **Cleanup:** Resources removed or restored.

## Completion Checklist

- [ ] Completed the command-line basics lab.
- [ ] Practiced safe file and directory operations.
- [ ] Created test users/groups and inspected permissions.
- [ ] Queried and installed a safe test package.
- [ ] Used exported and command-scoped environment variables.
- [ ] Inspected processes, services, ports, and logs.
- [ ] Completed a system-hardening review.
- [ ] Wrote a lab report with evidence and lessons learned.
- [ ] Removed dedicated test resources.

## Further Reading

- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Linux man-pages project](https://man7.org/linux/man-pages/)
- [Debian APT Guide](https://www.debian.org/doc/manuals/apt-guide/)
- [Ubuntu Security Guide](https://documentation.ubuntu.com/security/compliance/usg/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)

## Next Steps

Complete the individual roadmap modules alongside these labs. Then extend the collection with DevSecOps-focused exercises such as shell-script linting, dependency inventory, secure configuration checks, and automated baseline reporting.
