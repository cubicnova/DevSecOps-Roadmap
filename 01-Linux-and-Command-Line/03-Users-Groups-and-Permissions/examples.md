# Linux Users, Groups and Permissions — Examples

This file demonstrates common Linux account and permission commands with explanations and sample behavior.

> **Environment:** Ubuntu, Debian, or Kali Linux. Commands that modify accounts or ownership may require `sudo`.

## 1. Identify the Current User

```bash
whoami
id
id username
groups
groups username
```

Example output:

```text
$ whoami
student

$ id
uid=1000(student) gid=1000(student) groups=1000(student),27(sudo)
```

UID and GID values depend on the system.

## 2. Inspect User and Group Information

```bash
getent passwd student
getent group sudo
```

Example:

```text
student:x:1000:1000:Student:/home/student:/bin/bash
sudo:x:27:student
```

Passwd fields: `username:password-placeholder:UID:GID:comment:home-directory:login-shell`. The `x` placeholder indicates that protected password information is stored separately, typically in `/etc/shadow`.

## 3. Create a User

```bash
sudo useradd -m -s /bin/bash devuser
sudo passwd devuser
id devuser
getent passwd devuser
ls -ld /home/devuser
```

`-m` creates a home directory; `-s` sets the login shell. Set the password interactively and do not place real passwords in command-line arguments or Git repositories.

## 4. Modify a User

```bash
sudo usermod -aG developers devuser
id devuser
groups devuser
```

The `-a` option appends supplementary groups. Omitting it from `usermod -G` can replace the user's existing supplementary group list.

Lock and unlock an account:

```bash
sudo passwd -l devuser
sudo passwd -u devuser
```

Password locking affects password-based authentication; it does not necessarily disable every authentication method.

## 5. Create and Manage Groups

```bash
sudo groupadd developers
sudo groupadd security
sudo usermod -aG developers devuser
sudo gpasswd -d devuser developers
getent group developers
groups devuser
```

The `gpasswd -d` command removes the user from the named group.

## 6. Understand File Permissions

```bash
mkdir -p ~/permissions-lab
cd ~/permissions-lab
touch report.txt
ls -l report.txt
```

Example:

```text
-rw-r--r-- 1 student student 0 Oct 21 21:00 report.txt
```

Interpretation:

```text
- rw- r-- r--
|  |   |   |
|  |   |   +-- Others: read
|  |   +------ Group: read
|  +---------- Owner: read and write
+------------- Regular file
```

For directories, the first character is typically `d`.

## 7. Change Permissions with chmod

Numeric notation:

```bash
chmod 600 report.txt
chmod 640 report.txt
chmod 644 report.txt
chmod 755 script.sh
chmod 700 private_dir
```

Symbolic notation:

```bash
chmod u+x script.sh
chmod g+r report.txt
chmod o-r report.txt
chmod u=rw,g=r,o= report.txt
```

Inspect the result:

```bash
ls -l
stat report.txt
```

Directory execute permission controls traversal, not whether the directory can be run like a program.

## 8. Change Ownership

```bash
sudo chown devuser report.txt
sudo chgrp developers report.txt
sudo chown devuser:developers report.txt
ls -l report.txt
stat report.txt
```

Recursive example (use only when every item in the tree should receive this ownership):

```bash
sudo chown -R devuser:developers project/
```

Review the target path before using `-R`.

## 9. Understand umask

```bash
umask
umask -S
umask 027
touch private.txt
mkdir private_dir
ls -ld private.txt private_dir
```

With conventional creation modes and no overriding ACL, `umask 027` typically results in file permissions `640` and directory permissions `750`. Applications and ACLs can affect the result.

## 10. Configure a Shared Directory

```bash
sudo groupadd projectteam
sudo mkdir -p /srv/project
sudo chown root:projectteam /srv/project
sudo chmod 2770 /srv/project
ls -ld /srv/project
```

The expected permission string includes `drwxrws---`. SGID helps new entries inherit the directory's group on typical Linux filesystems. Group membership and `umask` or default ACLs still affect collaboration.

## 11. Inspect Special Permissions

```bash
find /usr/bin -type f -perm -4000 -print 2>/dev/null
find /usr/bin -type f -perm -2000 -print 2>/dev/null
find /tmp -type d -perm -0002 -print 2>/dev/null
```

These commands audit SUID files, SGID files, and world-writable directories. Do not remove special bits from system files indiscriminately; investigate each result first.

## 12. Use sudo Safely

```bash
sudo -l
sudo id
sudo visudo
```

`visudo` validates sudoers syntax before saving. Follow your distribution's recommended policy for creating individual rules.

## 13. Cleanup

Remove only the dedicated lab directory after you have finished:

```bash
rm -rf ~/permissions-lab
```

If you created test accounts and groups, remove them only after verifying that they contain no needed data and are not used by other processes.

## Key Takeaways

- Use `id` and `groups` to inspect identity and memberships.
- Use `chmod` to manage permission bits.
- Use `chown` and `chgrp` to manage ownership.
- Use `umask` to control default permissions.
- Use `sudo` with least privilege.
- Review special permissions and recursive operations carefully.
