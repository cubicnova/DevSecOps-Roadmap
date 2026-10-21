# Linux and Command-Line Labs — Solutions

These are example answers for `labs.md`. Output varies by distribution, permissions, and installed packages.

## Solution 1: Command-Line Basics

```bash
pwd
whoami
date
man ls
mkdir -p ~/linux-roadmap-labs
ls -la ~ > ~/linux-roadmap-labs/home-listing.txt
wc -l ~/linux-roadmap-labs/home-listing.txt
```

- `pwd` prints the current directory.
- `whoami` prints the effective username.
- `date` prints the system date and time.
- `man ls` opens the manual page.
- `>` redirects output and truncates an existing destination file.
- `>>` appends output.
- `wc -l` counts newline characters/lines in the file.

Review output before sharing because paths and filenames can reveal personal or system information.

## Solution 2: Files and Directories

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

Use absolute paths when clarity or script reliability matters; relative paths are interpreted from the current working directory. Copying over an existing file can replace its contents. Recursive deletion is dangerous because a wrong target can remove many files.

## Solution 3: Users, Groups and Permissions

Inspect identity:

```bash
whoami
id
groups
```

In a lab VM, create dedicated test resources only if they do not already exist:

```bash
sudo groupadd labteam
sudo useradd -m -s /bin/bash labuser
sudo usermod -aG labteam labuser
```

Create and inspect a file:

```bash
touch ~/linux-roadmap-labs/files/private.txt
chmod 640 ~/linux-roadmap-labs/files/private.txt
stat -c '%A %a %U %G %n' ~/linux-roadmap-labs/files/private.txt
```

Mode `640` grants the owner read/write, the group read, and others no access through ordinary permission bits.

A primary group is the account's main group ID; supplementary groups provide additional group memberships. `usermod -aG` appends a supplementary group without replacing the existing list.

Do not remove test accounts until confirming they contain no required data and are not used by other processes.

## Solution 4: Package Management

For Debian-based systems:

```bash
cat /etc/os-release
sudo apt update
apt search tree
apt show tree
sudo apt install tree
tree --version
dpkg -S "$(command -v tree)"
```

Review the proposed transaction before confirming. `apt update` refreshes package metadata; `apt upgrade` installs available upgrades. `remove` generally retains package-managed configuration, while `purge` also removes it. Keep repository signature verification enabled to help ensure metadata and packages come from trusted sources.

If you installed `tree` only for the lab, remove it after checking the proposed transaction:

```bash
sudo apt remove tree
```

## Solution 5: Environment Variables

```bash
printf 'HOME=%s\nPATH=%s\n' "$HOME" "$PATH"

LAB_MESSAGE="hello"
printenv LAB_MESSAGE
export LAB_MESSAGE
bash -c 'printf "%s\n" "$LAB_MESSAGE"'

LAB_MODE=testing printenv LAB_MODE
```

A shell variable is available in the current shell. Exporting it makes it part of the environment inherited by child processes. A command-scoped assignment applies to that command and its child processes, not as a persistent assignment in the current shell.

An unset variable and an empty variable can both expand to an empty string, but they are different states. Environment variables may leak through process inspection, logs, diagnostics, or application behavior, so production secrets should use appropriate secret-management controls.

## Solution 6: Processes and Services

```bash
ps aux
pgrep -a ssh
systemctl --type=service --state=running
journalctl -p warning..alert --since "24 hours ago"
sudo ss -tulpn
```

A process is a running program instance. A service is commonly a managed background workload, often controlled by systemd. A listening socket can expose a network service and should be mapped to a known purpose and appropriate access policy.

Logs help reconstruct events, troubleshoot failures, and identify suspicious patterns. Review and redact sensitive details before sharing.

## Solution 7: System Hardening Review

```bash
cat /etc/os-release
uname -r
getent group sudo
sudo ss -tulpn
find ~/linux-roadmap-labs -xdev -type f -perm -0002 -print
```

If OpenSSH server is installed:

```bash
sudo sshd -t
sudo sshd -T | grep -E 'permitrootlogin|passwordauthentication|pubkeyauthentication'
```

Do not assume the `sudo` group exists on all distributions; some use `wheel`. Do not change remote SSH or firewall settings without verified alternative access and a recovery path.

A useful finding includes:
- **Observation:** What was actually found.
- **Evidence:** Relevant command output, redacted as needed.
- **Risk:** Likely security or operational impact.
- **Recommendation:** A specific, justified change.
- **Validation:** How to verify the change.
- **Rollback:** How to recover if it causes problems.

## Solution 8: Example Mini Security Assessment

| Observation | Risk | Recommendation | Validation |
|---|---|---|---|
| Unneeded listener found | Larger attack surface | Confirm ownership and disable only if unnecessary | Recheck service and sockets |
| Lab file is world-writable | Unauthorized modification | Set appropriate ownership and permissions | Check `stat` and ACLs |
| Excessive admin group membership | Increased impact of account compromise | Review and reduce access by policy | Recheck group membership and sudo rules |
| Packages have security updates | Known issues may remain unpatched | Plan and test updates | Recheck package status and application health |
| Logs are not centrally reviewed | Delayed detection | Define retention and forwarding controls | Confirm events arrive and alerts work |

This is a sample format, not a claim that these issues exist on your machine. Use actual evidence from your lab.

## Cleanup Guidance

Remove only the files created for the exercise. If you created `labuser` or `labteam`, verify they are dedicated lab resources, no longer needed, and not referenced by files or processes before removing them. Do not delete system accounts or shared groups as part of cleanup.

## Final Notes

These labs build introductory Linux operational and security skills. They do not replace a full threat model, vulnerability assessment, compliance audit, or distribution-specific hardening guide.
