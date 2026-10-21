# Linux Users, Groups and Permissions — Solutions

This file provides reference solutions and explanations for the exercises in `practical.md`.

**Environment:** Ubuntu, Debian, or Kali Linux.

> Run administrative commands only in your lab VM. Commands below assume the named test users and groups are dedicated to these exercises.

## Solution 1: Inspect User Identity

```bash
whoami
id
groups
getent passwd "$(whoami)"
```

- `whoami` displays the effective username.
- `id` displays the effective UID, GID, and group memberships.
- `groups` displays group membership information.
- `getent passwd` queries the configured user database.

The shell field in a passwd record identifies the configured login shell.

## Solution 2: Create a User Account

```bash
sudo useradd -m -s /bin/bash labuser
sudo passwd labuser
```

Verify:

```bash
id labuser
getent passwd labuser
ls -ld /home/labuser
```

`-m` requests a home directory, and `-s` specifies the login shell. If the account already exists, inspect it rather than creating it again.

## Solution 3: Create Groups and Assign Membership

```bash
sudo groupadd developers
sudo groupadd security
sudo usermod -aG developers,security labuser
id labuser
groups labuser
```

Remove the user from `security`:

```bash
sudo gpasswd -d labuser security
groups labuser
```

`usermod -aG` appends supplementary groups. Using `usermod -G` without `-a` replaces the supplementary group list. A new login session may be required for group changes to affect an existing shell.

## Solution 4: Read Permission Strings

```bash
mkdir -p ~/permissions-lab
cd ~/permissions-lab
touch file1.txt file2.txt
mkdir private_dir
ls -l
stat file1.txt
stat private_dir
```

Example permission string:

```text
-rw-r--r--
```

- `-`: regular file.
- `rw-`: owner can read and write.
- `r--`: group can read.
- `r--`: others can read.

For a directory, `d` denotes a directory. Read permission lists entries; execute permission permits traversal. Actual values depend on the environment and `umask`.

## Solution 5: Apply Numeric Permissions

```bash
touch confidential.txt
chmod 600 confidential.txt
stat -c '%a %A %U %G' confidential.txt

chmod 640 confidential.txt
stat -c '%a %A %U %G' confidential.txt

chmod 644 confidential.txt
stat -c '%a %A %U %G' confidential.txt

chmod 600 confidential.txt
```

| Mode | Owner | Group | Others |
|---|---|---|---|
| `600` | Read, write | None | None |
| `640` | Read, write | Read | None |
| `644` | Read, write | Read | Read |

Mode `600` is the most restrictive of these three for ordinary permission bits. Avoid `777` for confidential files because it grants read, write, and execute permission to all permission classes.

## Solution 6: Apply Symbolic Permissions

```bash
cd ~/permissions-lab

cat > hello.sh <<'EOF'
#!/bin/bash
echo "Hello from the Linux permissions lab"
EOF

chmod a-x hello.sh
chmod u+x hello.sh
chmod go-w hello.sh

ls -l hello.sh
./hello.sh
stat -c '%a %A' hello.sh
```

The owner has execute permission, while group and others do not have write permission. The exact final mode depends on the initial mode. Execution also requires a suitable interpreter and a filesystem that permits execution.

## Solution 7: Change Ownership

```bash
cd ~/permissions-lab
touch team-report.txt

getent group developers || sudo groupadd developers
sudo chown labuser team-report.txt
sudo chgrp developers team-report.txt

ls -l team-report.txt
stat team-report.txt
```

Combined alternative:

```bash
sudo chown labuser:developers team-report.txt
```

- `chown` changes owner and optionally group.
- `chgrp` changes group.
- `chmod` changes permission bits.

Changing ownership generally requires appropriate privileges.

## Solution 8: Test umask

```bash
umask
umask 027
touch newfile.txt
mkdir newdirectory
stat -c '%a %A %n' newfile.txt newdirectory
```

Typical output:

```text
640 -rw-r----- newfile.txt
750 drwxr-x--- newdirectory
```

With conventional creation modes, regular files start from mode `666` and directories from `777`. The mask removes group write and all permissions for others. Applications and ACLs can affect the final permissions.

The change affects the current shell and its child processes, not every user's future sessions.

## Solution 9: Build a Shared Team Directory

```bash
sudo groupadd projectteam
sudo mkdir -p /srv/project
sudo chown root:projectteam /srv/project
sudo chmod 2770 /srv/project
sudo usermod -aG projectteam labuser
ls -ld /srv/project
id labuser
getent group projectteam
```

Expected directory permissions:

```text
drwxrws---
```

The leading `2` enables SGID. On typical Linux filesystems, new entries inherit the directory's group. A new login session may be needed for updated supplementary group membership.

If group members need to edit one another's files, ensure the group membership and `umask` or default ACL support the desired collaboration.

## Solution 10: Audit Special Permissions

```bash
find /usr/bin -type f -perm -4000 -print 2>/dev/null
find /usr/bin -type f -perm -2000 -print 2>/dev/null
find /tmp -type d -perm -0002 -print 2>/dev/null
```

- **SUID:** On applicable executable files, a process can run with the file owner's effective identity.
- **SGID:** On applicable executable files, a process can run with the file's group identity; on directories it commonly supports group inheritance.
- **Sticky bit:** On shared writable directories, it restricts unprivileged users from deleting or renaming entries owned by others.

These bits are not automatically vulnerabilities. Investigate each file and its purpose before taking action.

## Solution 11: Review sudo Access

```bash
sudo -l
sudo visudo
```

A narrowly scoped policy grants only the commands and targets required for a task. Unrestricted root access increases the consequences of compromised credentials. Avoid broad rules such as `NOPASSWD: ALL` for convenience.

Do not change production sudoers configuration for this exercise. Follow distribution guidance and retain a recovery path when testing custom rules.

## Solution 12: Account Locking and Cleanup

Lock the test account:

```bash
sudo passwd -l labuser
sudo passwd -S labuser
```

Unlock it:

```bash
sudo passwd -u labuser
sudo passwd -S labuser
```

Password locking does not necessarily prevent SSH public-key authentication, existing sessions, or all other authentication methods.

After verifying that the account is no longer needed and contains no required data:

```bash
sudo userdel -r labuser
```

Remove dedicated groups only when no users or files still depend on them:

```bash
sudo groupdel developers
sudo groupdel security
sudo groupdel projectteam
```

Remove the lab directory:

```bash
rm -rf ~/permissions-lab
```

These deletion commands are destructive. Verify every target first.

## Solution 13: Final Permission-Hardening Challenge

Given:

```text
drwxrwxrwx root root /srv/app
-rw-rw-rw-  root root /srv/app/config.env
```

### Problems

1. The directory is writable by every user.
2. The configuration file is readable and writable by every user.
3. Other users could potentially tamper with application files or read exposed secrets.
4. Ownership does not reflect a clear application or administration access policy.

### Example remediation

Suppose a dedicated `appteam` group needs to maintain the application directory:

```bash
sudo groupadd appteam
sudo chown -R root:appteam /srv/app
sudo chmod 2750 /srv/app
sudo chmod 640 /srv/app/config.env

ls -ld /srv/app
ls -l /srv/app/config.env
```

This is an illustrative starting point, not a universal production configuration. Mode `2750` gives the owner full access, the group read and traversal access, and no access to others. Mode `640` gives the owner read/write access, the group read access, and denies access to others through ordinary permission bits.

If `appteam` members must create or modify files in the directory, adjust directory group-write access and the ACL policy accordingly. Verify runtime user and service requirements before applying recursive ownership changes.

### Verify permissions and access controls

```bash
stat -c '%A %a %U %G %n' /srv/app /srv/app/config.env
namei -l /srv/app/config.env
getfacl /srv/app/config.env
```

`getfacl` may require installing ACL utilities.

For sensitive configuration:

- Keep secrets out of source control.
- Use an appropriate secret manager or protected configuration mechanism.
- Restrict access to the application runtime identity and authorized administrators.
- Rotate credentials if they may already have been exposed.
- Audit access and follow least-privilege principles.

## Final Review

You have completed this module when you can explain and demonstrate:

- User and group administration.
- File and directory permission semantics.
- Numeric and symbolic `chmod`.
- Ownership changes.
- `umask` and special permissions.
- Controlled `sudo` access.
- Permission auditing and security hardening.

## References

- [GNU Coreutils Manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [`chmod` Manual](https://man7.org/linux/man-pages/man1/chmod.1.html)
- [`chown` Manual](https://man7.org/linux/man-pages/man1/chown.1.html)
- [`umask` Manual](https://man7.org/linux/man-pages/man2/umask.2.html)
