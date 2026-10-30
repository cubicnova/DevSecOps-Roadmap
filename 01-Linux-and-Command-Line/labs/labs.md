# Linux and Command-Line — Lab Workbook

This workbook contains seven practical labs. Use a disposable Linux VM and record your results.

## Lab 1: Command-Line Basics

### Tasks

1. Display the current directory.
2. Display the current username and system date.
3. Read the manual page for `ls`.
4. Create a directory for lab output.
5. Redirect command output to a text file.
6. Count the lines in that file.

### Commands to explore

```bash
pwd
whoami
date
man ls
mkdir -p ~/linux-roadmap-labs
ls -la ~ > ~/linux-roadmap-labs/home-listing.txt
wc -l ~/linux-roadmap-labs/home-listing.txt
```

### Questions

- What does `>` do to an existing file?
- How does `>>` differ from `>`?
- Why should command output be reviewed before sharing?

## Lab 2: Files and Directories

### Tasks

1. Create `~/linux-roadmap-labs/files`.
2. Create `notes.txt` and `todo.txt`.
3. Add a few lines to each file.
4. Copy one file to a backup.
5. Rename the other file.
6. Find all `.txt` files under the lab directory.
7. Compare file metadata with `stat`.

### Commands to explore

```bash
mkdir -p ~/linux-roadmap-labs/files
cd ~/linux-roadmap-labs/files
printf 'Linux lab notes\n' > notes.txt
printf 'Review permissions\nPractice find\n' > todo.txt
cp notes.txt notes.txt.bak
mv todo.txt tasks.txt
find ~/linux-roadmap-labs -type f -name '*.txt' -print
stat notes.txt
```

### Questions

- When should you use an absolute path rather than a relative path?
- What happens if a copy operation targets an existing file?
- Why is `rm -rf` dangerous when the target path is wrong?

## Lab 3: Users, Groups and Permissions

### Tasks

1. Inspect your current identity and groups.
2. Create a dedicated lab group and test user.
3. Add the test user to the group.
4. Create a sample file and apply mode `640`.
5. Inspect ownership and permissions.
6. Explain the purpose of a shared directory with SGID.

### Commands to explore

```bash
whoami
id
groups
sudo groupadd labteam
sudo useradd -m -s /bin/bash labuser
sudo usermod -aG labteam labuser
touch ~/linux-roadmap-labs/files/private.txt
chmod 640 ~/linux-roadmap-labs/files/private.txt
stat -c '%A %a %U %G %n' ~/linux-roadmap-labs/files/private.txt
```

Only create these accounts and groups if they do not already exist and are dedicated to your lab. Do not use a real person's account name. Clean up test accounts only after verifying they are unused.

### Questions

- What is the difference between a primary and supplementary group?
- Why is `usermod -aG` important?
- What can the owner, group, and others do with mode `640`?

## Lab 4: Package Management

### Tasks

1. Identify your distribution.
2. Refresh package metadata.
3. Search for `tree`.
4. Inspect package details.
5. Install it if available and review the proposed transaction.
6. Verify its version and owning package.
7. Remove it after the lab if it was installed only for this exercise.

### Commands to explore (Debian-based systems)

```bash
cat /etc/os-release
sudo apt update
apt search tree
apt show tree
sudo apt install tree
tree --version
dpkg -S "$(command -v tree)"
```

Review all installation and removal proposals before confirming. If the package is unavailable, document the repository issue rather than adding an unknown source.

### Questions

- How does `apt update` differ from `apt upgrade`?
- What is the difference between `remove` and `purge`?
- Why should package-signature checks remain enabled?

## Lab 5: Environment Variables

### Tasks

1. Display `HOME` and `PATH`.
2. Create a shell variable that is not exported.
3. Export it and verify that a child process can read it.
4. Set a variable for one command only.
5. Create a script that uses a default value.
6. Explain why secrets should not be committed to Git.

### Commands to explore

```bash
printf 'HOME=%s\nPATH=%s\n' "$HOME" "$PATH"
LAB_MESSAGE="hello"
printenv LAB_MESSAGE
export LAB_MESSAGE
bash -c 'printf "%s\n" "$LAB_MESSAGE"'
LAB_MODE=testing printenv LAB_MODE
```

### Questions

- Why does a child process not normally inherit an unexported shell variable?
- What is the difference between an unset variable and an empty value?
- Why are environment variables not a complete secrets vault?

## Lab 6: Processes and Services

### Tasks

1. Inspect running processes.
2. Find a process by name.
3. Inspect a service's status.
4. Review recent journal warnings.
5. Inspect listening network sockets.
6. Explain why a listening port should be mapped to a legitimate service.

### Commands to explore

```bash
ps aux
pgrep -a ssh
systemctl --type=service --state=running
journalctl -p warning..alert --since "24 hours ago"
sudo ss -tulpn
```

Service names and log availability vary by distribution. Do not stop or kill services unless they are dedicated lab processes and you understand the impact.

### Questions

- What is the difference between a process and a service?
- Why can a listening socket be security-relevant?
- What information can logs provide during incident investigation?

## Lab 7: System Hardening Review

### Tasks

1. Record OS and kernel versions.
2. Review administrative group membership.
3. Inspect SSH configuration syntax and selected effective settings if OpenSSH server is installed.
4. Review firewall status using the tool configured on your system.
5. Find world-writable files in the dedicated lab directory.
6. Review a sample of security logs.
7. Produce three findings with risk, recommendation, and validation method.

### Commands to explore

```bash
cat /etc/os-release
uname -r
getent group sudo
sudo ss -tulpn
sudo sshd -t
sudo sshd -T | grep -E 'permitrootlogin|passwordauthentication|pubkeyauthentication'
find ~/linux-roadmap-labs -xdev -type f -perm -0002 -print
```

`sshd` commands require an installed OpenSSH server. Administrative group names and firewall tooling differ by distribution. Do not change SSH or firewall settings on a remote host during this lab.

### Questions

- Why should you inventory before hardening?
- Why is it risky to apply a generic hardening script without reviewing it?
- What evidence should a security finding include?

## Final Challenge: Mini Linux Security Assessment

Write a short report containing:

1. Scope and environment.
2. Five observations from your lab.
3. Risk and likely impact.
4. A recommended remediation for each issue.
5. Validation steps.
6. Rollback or recovery plan.
7. Cleanup confirmation.

Do not claim that a system is fully secure based on these basic checks. This workbook is an introductory practice set, not a complete security audit.
