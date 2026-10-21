# 03 — Users, Groups and Permissions

![Linux](https://img.shields.io/badge/Linux-User%20Management-FCC624?logo=linux&logoColor=black)
![Level](https://img.shields.io/badge/Level-Beginner%20to%20Intermediate-blue)
![Focus](https://img.shields.io/badge/Focus-DevSecOps%20%7C%20Linux%20Security-red)

## Overview

Linux is a multi-user operating system. User accounts, groups, ownership, and file permissions determine who can access files, modify resources, and execute programs.

This module explains how to manage Linux users and groups, configure file and directory permissions, control administrative privileges, and apply security best practices.

## Learning Objectives

By the end of this module, you will be able to:

- Understand Linux users, groups, UIDs, and GIDs.
- Create, modify, lock, and delete user accounts.
- Create groups and manage group membership.
- Read and interpret Linux file permission strings.
- Configure permissions using `chmod`.
- Change file ownership using `chown` and `chgrp`.
- Understand and configure `umask`.
- Use `sudo` for controlled administrative access.
- Explain SUID, SGID, and sticky-bit permissions.
- Audit permissions and identify common security misconfigurations.

## Topics Covered

### 1. Linux User Fundamentals

- Root user and regular users
- System and service accounts
- User IDs (UIDs)
- Primary and supplementary groups
- `/etc/passwd`
- `/etc/shadow`
- `/etc/group`
- `/etc/gshadow`

### 2. User Management

- `useradd`, `adduser`, `usermod`, `passwd`, `userdel`
- `id`, `whoami`, `getent`
- Account locking and unlocking
- Login shells and home directories

### 3. Group Management

- `groupadd`, `groupmod`, `groupdel`
- `groups`, `gpasswd`, `newgrp`
- Adding and removing group members
- Shared group access

### 4. Linux File Permissions

| Permission | Files | Directories |
|---|---|---|
| Read (`r`) | Read contents | List directory entries |
| Write (`w`) | Modify contents | Create, remove, or rename entries, subject to other restrictions |
| Execute (`x`) | Execute a program or script | Search or traverse the directory |

Permission classes: `u` (owner), `g` (group), `o` (others), and `a` (all).

### 5. Permission Management

- `ls -l`, `stat`
- `chmod` with symbolic and octal notation
- `chown`, `chgrp`
- Recursive permission changes

### 6. Default Permissions

- `umask`
- Default file and directory permissions
- Restrictive permission policies

### 7. Advanced Permissions

- SUID
- SGID
- Sticky bit
- Shared directories with SGID
- World-writable directory risks

### 8. Privilege Management and Auditing

- `sudo`, `/etc/sudoers`, `visudo`
- Least privilege
- Find world-writable files and directories
- Find SUID and SGID files
- Review account and group membership

## Essential Commands

| Command | Purpose |
|---|---|
| `whoami` | Display current username |
| `id` | Display UID, GID, and group memberships |
| `getent passwd` | Query user account records |
| `useradd` | Create a user |
| `usermod` | Modify a user account |
| `passwd` | Manage passwords |
| `userdel` | Delete a user |
| `groupadd` | Create a group |
| `groups` | Display group memberships |
| `chmod` | Change permissions |
| `chown` | Change ownership |
| `chgrp` | Change group ownership |
| `umask` | View or set the permission creation mask |
| `sudo` | Execute an authorized command with elevated privileges |
| `find` | Search files and directories |
| `stat` | Display file metadata and permissions |

## Numeric Permissions Reference

| Value | Permission |
|---:|---|
| 0 | `---` |
| 1 | `--x` |
| 2 | `-w-` |
| 3 | `-wx` |
| 4 | `r--` |
| 5 | `r-x` |
| 6 | `rw-` |
| 7 | `rwx` |

Examples:

- `chmod 755 script.sh` — owner can read, write, and execute; group and others can read and execute.
- `chmod 640 report.txt` — owner can read and write; group can read; others have no permissions.
- `chmod 700 private_dir` — only the owner has directory permissions.
- `chmod 2770 shared_dir` — full access for owner and group, no access for others, and SGID enabled.

## Hands-On Lab Environment

Recommended: Kali Linux, Ubuntu, Debian, or a Linux virtual machine.

**Safety:** Perform account and permission exercises in a disposable VM or controlled lab. Do not change permissions on system directories or modify production `/etc/sudoers` settings while learning.

## Repository Files

- `README.md` — concepts, commands, and learning objectives
- `examples.md` — command demonstrations and expected behavior
- `practical.md` — hands-on exercises and challenges
- `solution.md` — suggested commands and explanations

## Completion Checklist

- [ ] Explain UIDs and GIDs.
- [ ] Create users and groups.
- [ ] Add a user to a supplementary group.
- [ ] Interpret permission strings.
- [ ] Configure permissions using octal and symbolic notation.
- [ ] Change file ownership and group ownership.
- [ ] Explain `umask`.
- [ ] Configure a shared directory using SGID.
- [ ] Identify SUID and world-writable files.
- [ ] Apply least-privilege principles.

## Further Reading

- [GNU Coreutils Manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [Linux `chmod` Manual](https://man7.org/linux/man-pages/man1/chmod.1.html)
- [Linux `chown` Manual](https://man7.org/linux/man-pages/man1/chown.1.html)
- [Linux `umask` Manual](https://man7.org/linux/man-pages/man2/umask.2.html)

## Next Module

Continue to **04 — Processes and Services** to learn how Linux processes, services, and system resources are managed.
