# Linux Users, Groups and Permissions — Practical Lab

## Lab Information

**Level:** Beginner to Intermediate

**Objective:** Practice Linux account administration, group management, file permissions, ownership, and security auditing.

**Environment:** Kali Linux, Ubuntu, or Debian virtual machine.

### Safety Rules

- Use a lab VM and a non-root account.
- Inspect commands before running them with `sudo`.
- Never experiment by changing permissions on `/etc`, `/usr`, `/bin`, or other system directories.
- Do not make sensitive files world-writable.
- Use only test accounts and groups created for this lab.

---

## Practical 1: Inspect User Identity

**Tasks**

1. Display your current username.
2. Display your UID and primary GID.
3. List supplementary groups.
4. Display the account entry for your user.
5. Identify the configured login shell.

**Commands to explore**

```bash
whoami
id
groups
getent passwd "$(whoami)"
```

**Expected learning:** Understand usernames, UIDs, GIDs, group membership, and login shells.

## Practical 2: Create a User Account

**Tasks**

1. Create a user named `labuser`.
2. Create its home directory.
3. Set its login shell to Bash.
4. Set a password interactively.
5. Verify the account and home directory.

Use `useradd` or your distribution's equivalent. Do not put real passwords in command-line arguments or Git.

## Practical 3: Create Groups and Assign Membership

**Tasks**

1. Create groups named `developers` and `security`.
2. Add `labuser` to both groups.
3. Verify group membership.
4. Remove `labuser` from `security`.
5. Verify membership in `developers` remains intact.

**Challenge:** Explain why `usermod -aG` is generally safer for adding supplementary groups than `usermod -G`.

## Practical 4: Read Permission Strings

Run:

```bash
mkdir -p ~/permissions-lab
cd ~/permissions-lab
touch file1.txt file2.txt
mkdir private_dir
ls -l
```

**Tasks**

1. Explain each permission string.
2. Identify the owner and owning group.
3. Explain the difference between file and directory permissions.
4. Use `stat` to inspect metadata.

## Practical 5: Apply Numeric Permissions

Create `confidential.txt`.

**Tasks**

1. Set permissions to `600`.
2. Set permissions to `640`.
3. Set permissions to `644`.
4. Explain who can read or modify the file under each mode.
5. Restore mode `600`.

**Challenge:** Explain why `777` is inappropriate for a confidential file.

## Practical 6: Apply Symbolic Permissions

Create `hello.sh`:

```bash
#!/bin/bash
echo "Hello from the Linux permissions lab"
```

**Tasks**

1. Remove all execute permissions.
2. Grant execute permission to the owner.
3. Remove write permission for group and others.
4. Run the script.
5. Verify the final permissions.

**Expected learning:** Understand `u`, `g`, `o`, `a`, `+`, `-`, and `=`.

## Practical 7: Change Ownership

**Tasks**

1. Create `team-report.txt`.
2. Change its owner to `labuser`.
3. Create the `developers` group if it does not exist.
4. Change the file's group to `developers`.
5. Verify the result.

**Challenge:** Explain the difference between `chown`, `chgrp`, and `chmod`.

## Practical 8: Test umask

**Tasks**

1. Record the current `umask`.
2. Set `umask` to `027` for the current shell.
3. Create a file and a directory.
4. Inspect their permissions.
5. Explain why their permissions differ.

Typical results on a conventional Linux setup without an overriding ACL:

| Object | Typical permissions |
|---|---|
| Newly created regular file | `640` |
| Newly created directory | `750` |

## Practical 9: Build a Shared Team Directory

**Scenario:** The development team needs a shared directory writable by its members but inaccessible to other users.

**Tasks**

1. Create a `projectteam` group.
2. Create `/srv/project`.
3. Set its owner to `root` and group to `projectteam`.
4. Apply mode `2770`.
5. Verify the SGID bit.
6. Explain group inheritance.
7. Explain why group membership and `umask` still matter.

**Security requirement:** Other users must not have access through the directory's ordinary permission bits.

## Practical 10: Audit Special Permissions

**Tasks**

1. Find SUID files under `/usr/bin`.
2. Find SGID files under `/usr/bin`.
3. Find world-writable directories under `/tmp`.
4. Record a few results.
5. Explain the purpose and risk of each permission type.

Use read-only auditing commands. Do not change system-file permissions.

## Practical 11: Review sudo Access

**Tasks**

1. Run `sudo -l`.
2. Explain why unrestricted administrative access creates risk.
3. Read the documentation for `visudo`.
4. Describe how a narrowly scoped sudo rule differs from unrestricted root access.

Do not edit production sudoers configuration for this exercise. If you test a rule, use a disposable VM and retain a recovery path.

## Practical 12: Account Locking and Cleanup

**Tasks**

1. Lock the dedicated `labuser` account.
2. Verify its status.
3. Unlock the account.
4. Verify its status again.
5. Remove the test account and groups after confirming they are no longer needed.
6. Remove the lab directory.

**Challenge:** Explain why locking a password does not necessarily block every login method.

---

## Final Challenge: Linux Permission Hardening

A team has a project directory configured as follows:

```text
drwxrwxrwx root root /srv/app
-rw-rw-rw-  root root /srv/app/config.env
```

Answer the following:

1. Identify the security weaknesses.
2. Propose a suitable group-based access model.
3. Recommend safer directory and file permissions.
4. Explain how to verify ownership and permissions.
5. Explain why secret files should not be committed to Git.
6. Describe how least privilege reduces the impact of a compromised account.

Do not modify a real production directory. Document your proposed remediation or reproduce the scenario in your VM.

## Submission Checklist

- [ ] User creation and inspection completed.
- [ ] Group membership tasks completed.
- [ ] Numeric and symbolic permissions tested.
- [ ] File ownership changed and verified.
- [ ] `umask` behavior explained.
- [ ] Shared directory configured with SGID.
- [ ] Special permissions audited.
- [ ] `sudo` access reviewed.
- [ ] Account cleanup completed.
- [ ] Final hardening recommendations documented.

**Next step:** Compare your commands and reasoning against `solution.md`.
