# 05 — Package Management

![Linux](https://img.shields.io/badge/Linux-Package%20Management-FCC624?logo=linux&logoColor=black)
![Level](https://img.shields.io/badge/Level-Beginner%20to%20Intermediate-blue)
![Focus](https://img.shields.io/badge/Focus-DevSecOps%20%7C%20System%20Administration-red)

## Overview

Package management is the process of installing, updating, configuring, querying, and removing software through a distribution's package tools. Reliable package management helps keep systems maintainable, reproducible, and secure.

This module introduces APT and DPKG on Debian-based systems such as Ubuntu, Debian, and Kali Linux, along with an overview of DNF and RPM on Fedora/RHEL-family systems.

## Learning Objectives

By the end of this module, you will be able to:

- Explain packages, repositories, package indexes, dependencies, and package managers.
- Refresh APT repository metadata and upgrade installed packages.
- Search for, inspect, install, and remove packages.
- Query installed package information with `dpkg`.
- Inspect package files and verify package ownership.
- Understand repository signing and package authenticity.
- Troubleshoot common package-manager errors.
- Use package management safely in automation and DevSecOps workflows.

## Topics Covered

### 1. Package Management Fundamentals

- What is a software package?
- Package managers vs. package formats
- Repositories and mirrors
- Package indexes and metadata
- Dependencies and dependency resolution
- Installed, available, and held packages

### 2. APT on Debian-Based Distributions

- `apt update`
- `apt upgrade`
- `apt full-upgrade`
- `apt install`
- `apt remove`
- `apt purge`
- `apt autoremove`
- `apt search`
- `apt show`
- `apt list --installed`
- `apt-mark`

### 3. DPKG Package Queries

- `dpkg -l`
- `dpkg -s`
- `dpkg -L`
- `dpkg -S`
- `dpkg -i`
- `dpkg --configure -a`

### 4. Package Files and Dependencies

- `.deb` packages
- Package metadata
- Dependency inspection
- File ownership
- Configuration files
- Package verification and integrity considerations

### 5. Repositories and Trust

- `/etc/apt/sources.list`
- `/etc/apt/sources.list.d/`
- Repository signing keys
- Signed Release metadata
- `Signed-By` keyring configuration
- Why arbitrary repositories and installation scripts are risky

### 6. Troubleshooting

- Failed downloads and mirror errors
- Package index refresh failures
- Unmet dependencies
- Interrupted installations
- Package locks
- Disk-space issues
- Repository and signing-key errors

### 7. Other Linux Package Managers

| Distribution family | High-level tools | Package format |
|---|---|---|
| Debian, Ubuntu, Kali | APT, DPKG | `.deb` |
| Fedora, RHEL-family | DNF, RPM | `.rpm` |
| Arch Linux | Pacman | `.pkg.tar.*` |
| Alpine Linux | APK | `.apk` |

Use the tools appropriate to your distribution; commands and repository configuration differ.

## Essential APT Commands

| Command | Purpose |
|---|---|
| `sudo apt update` | Refresh package indexes |
| `apt search NAME` | Search package metadata |
| `apt show NAME` | Show package details |
| `sudo apt install NAME` | Install a package |
| `sudo apt upgrade` | Upgrade installed packages |
| `sudo apt remove NAME` | Remove a package but usually retain configuration |
| `sudo apt purge NAME` | Remove a package and its package-managed configuration |
| `sudo apt autoremove` | Remove automatically installed dependencies no longer required |
| `dpkg -l` | List package records |
| `dpkg -s NAME` | Inspect an installed package |
| `dpkg -L NAME` | List files installed by a package |
| `dpkg -S PATH` | Find which installed package owns a path |
| `apt-mark showhold` | Show packages marked as held |

## Important Distinctions

- `apt update` refreshes package indexes; it does **not** upgrade installed software.
- `apt upgrade` upgrades installed packages when the upgrade can proceed without removing packages.
- `apt full-upgrade` may remove packages to complete an upgrade.
- `remove` usually retains package-managed configuration files.
- `purge` also removes package-managed configuration, but does not guarantee removal of every user-created file.
- `autoremove` can remove packages. Review the proposed changes before confirming.

## Safe Lab Environment

Recommended: Kali Linux, Ubuntu, or Debian virtual machine or disposable container.

Before changing packages:

1. Confirm your distribution and version.
2. Review the package name and repository source.
3. Read the proposed transaction before confirming.
4. Keep a VM snapshot or backup for risky system changes.
5. Avoid piping remote scripts directly into a privileged shell.
6. Never disable package signature checks to work around repository errors.

## Repository Files

- `README.md` — concepts, commands, and learning objectives
- `examples.md` — command demonstrations and explanations
- `practical.md` — hands-on exercises
- `solution.md` — suggested commands and reasoning

## Completion Checklist

- [ ] Explain package managers, repositories, and dependencies.
- [ ] Refresh package indexes and upgrade packages.
- [ ] Search and inspect package metadata.
- [ ] Install and remove a safe test package.
- [ ] Query installed packages using DPKG.
- [ ] Identify which package owns a file.
- [ ] Explain repository signing and trust.
- [ ] Diagnose common package-management errors.
- [ ] Explain why arbitrary repositories and scripts can be risky.

## Further Reading

- [APT User's Guide](https://www.debian.org/doc/manuals/apt-guide/)
- [APT Manual](https://manpages.debian.org/apt/apt.8.en.html)
- [DPKG Manual](https://manpages.debian.org/dpkg/dpkg.1.en.html)
- [Debian Repository Setup](https://wiki.debian.org/SourcesList)
- [Fedora DNF Documentation](https://docs.fedoraproject.org/en-US/quick-docs/dnf/)

## Next Module

Continue to **06 — Processes and Services** (or the next numbered module in your repository) to explore process management, systemd services, and service security.
