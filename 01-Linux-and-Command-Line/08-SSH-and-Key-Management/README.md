# 🔐 SSH and Key Management

[![OpenSSH](https://img.shields.io/badge/OpenSSH-Secure_Shell-2E6DB4)](https://www.openssh.org/)
[![Level](https://img.shields.io/badge/Level-Beginner_to_Intermediate-success)](.)
[![Roadmap](https://img.shields.io/badge/Path-DevSecOps-blue)](../../README.md)

Welcome to **SSH and Key Management**, a module in the Linux and Command Line section of the **CubicNova DevSecOps Roadmap**. Learn how to connect to Linux systems securely, create and protect SSH keys, authenticate with public keys, transfer files, use `ssh-agent`, verify server identities, and troubleshoot common SSH issues.

This module uses a step-by-step workflow. Practice locally first, then connect only to systems you own or are authorized to access.

## 📚 Table of Contents

- [Learning Objectives](#-learning-objectives)
- [Prerequisites and Safety](#-prerequisites-and-safety)
- [Step 1: Check SSH Tools](#step-1-check-ssh-tools)
- [Step 2: Understand SSH](#step-2-understand-ssh)
- [Step 3: Inspect Existing Keys](#step-3-inspect-existing-keys)
- [Step 4: Generate a Key Pair](#step-4-generate-a-key-pair)
- [Step 5: Protect Your Keys](#step-5-protect-your-keys)
- [Step 6: Understand Public-Key Authentication](#step-6-understand-public-key-authentication)
- [Step 7: Connect to a Remote Host](#step-7-connect-to-a-remote-host)
- [Step 8: Configure ssh-agent](#step-8-configure-ssh-agent)
- [Step 9: Copy Files Securely](#step-9-copy-files-securely)
- [Step 10: Use SSH Configuration](#step-10-use-ssh-configuration)
- [Step 11: Verify Host Keys](#step-11-verify-host-keys)
- [Step 12: Troubleshoot SSH](#step-12-troubleshoot-ssh)
- [Key Rotation and Revocation](#key-rotation-and-revocation)
- [Hands-On Labs](#-hands-on-labs)
- [Mini Project](#-mini-project)
- [Module Files](#-module-files)
- [Security Best Practices](#-security-best-practices)
- [Learning Resources](#-learning-resources)
- [Next Steps](#-next-steps)

## 🎯 Learning Objectives

By completing this module, you should be able to:

1. Explain SSH encryption, host authentication, and user authentication at a high level.
2. Inspect SSH client and server tools.
3. Generate and identify SSH key pairs.
4. Protect private keys and understand public keys.
5. Configure public-key authentication on an authorized server.
6. Use `ssh-agent` and `ssh-add`.
7. Transfer files with `scp` and `sftp`.
8. Create host aliases in SSH client configuration.
9. Verify host fingerprints and respond safely to host-key warnings.
10. Troubleshoot and rotate keys using safe operational practices.

## 🧰 Prerequisites and Safety

- A Linux terminal, WSL, macOS terminal, or another OpenSSH client environment.
- A local account and, for remote exercises, a server you own or have explicit authorization to access.
- Basic command-line and file-permission knowledge.

**Important:** Never share or upload a private key (`id_ed25519`, `id_rsa`, or similar), its passphrase, or a private key backup. Public keys (`*.pub`) are intended to be shared with the service or account that should trust them.

Do not disable host-key checking to bypass a warning. Verify a server's identity through a trusted channel.

---

## Step 1: Check SSH Tools

Check whether the client utilities are installed:

```bash
ssh -V
ssh-keygen -h
command -v ssh
command -v ssh-keygen
command -v ssh-agent
command -v scp
command -v sftp
```

`ssh-keygen -h` behavior can vary by OpenSSH version; if it displays an error or usage information, consult `man ssh-keygen`.

On Debian- or Ubuntu-based systems, client tools can commonly be installed with:

```bash
sudo apt update
sudo apt install openssh-client
```

For a server, the OpenSSH server package may be required, such as `openssh-server` on Debian/Ubuntu. Do not install or enable a server unless you need one and can administer it securely.

## Step 2: Understand SSH

SSH (Secure Shell) provides encrypted communication between an SSH client and server. It supports remote login, command execution, file transfer, and tunneling.

Three concepts matter:

- **Host authentication:** Helps the client verify that it is connecting to the intended server using the server's host key.
- **User authentication:** The server verifies the user's identity, for example through a password, public key, or another configured method.
- **Encrypted transport:** Protects data in transit and provides integrity protections.

Do not confuse the server's host key with your user authentication key pair. They serve different purposes.

## Step 3: Inspect Existing Keys

List the SSH directory without printing private key contents:

```bash
ls -la ~/.ssh
```

Look for familiar key pairs, such as:

```text
id_ed25519
id_ed25519.pub
```

- `id_ed25519` is the private key.
- `id_ed25519.pub` is the public key.

If you already have a key, verify its fingerprint:

```bash
ssh-keygen -lf ~/.ssh/id_ed25519.pub
```

Do not overwrite an existing key until you understand which services rely on it. If necessary, generate a new key with a distinct filename.

## Step 4: Generate a Key Pair

For a new key dedicated to a learning lab:

```bash
ssh-keygen -t ed25519 -C "cubicnova-lab" -f ~/.ssh/id_ed25519_lab
```

When prompted, choose a strong passphrase unless your use case and key-management system dictate otherwise. A passphrase adds protection if the private key file is copied.

The command creates a private key and a corresponding `.pub` public key. The comment is a label, not a secret.

Inspect the public key fingerprint:

```bash
ssh-keygen -lf ~/.ssh/id_ed25519_lab.pub
```

## Step 5: Protect Your Keys

Check permissions:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519_lab
chmod 644 ~/.ssh/id_ed25519_lab.pub
```

Apply permissions only to your own key files and directories. These are common Unix permissions; system ACLs, ownership, and platform-specific behavior may also affect access.

Display the public key when you need to register it with a service:

```bash
cat ~/.ssh/id_ed25519_lab.pub
```

Never display, paste, email, or commit the private key file. Do not add private keys to Git repositories, even private repositories.

## Step 6: Understand Public-Key Authentication

Public-key authentication generally works as follows:

1. You create a public/private key pair on the client.
2. The server account is configured to trust your public key.
3. The client proves possession of the private key during authentication.
4. The server checks the proof against an authorized public key.
5. The private key itself is not sent to the server.

On a server you administer, the account's `~/.ssh/authorized_keys` file commonly contains allowed public keys.

If `ssh-copy-id` is installed and password-based setup is permitted, it can install a public key for an authorized account:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519_lab.pub USER@HOST
```

Replace `USER` and `HOST` with the correct remote username and hostname. Confirm the destination before running it.

Alternatively, add the public key through your cloud provider's supported access-management process or an administrator-approved method.

## Step 7: Connect to a Remote Host

```bash
ssh USER@HOST
```

For a particular private key:

```bash
ssh -i ~/.ssh/id_ed25519_lab USER@HOST
```

For a non-default port:

```bash
ssh -p 2222 USER@HOST
```

Replace all example values with information supplied by your administrator or lab. On first connection, verify the host fingerprint using a trusted source before accepting it.

For diagnostic output:

```bash
ssh -v USER@HOST
```

Verbose logs may reveal usernames, hostnames, file paths, or configuration details. Review them before sharing.

## Step 8: Configure ssh-agent

`ssh-agent` can hold unlocked keys in memory so you do not need to enter the passphrase repeatedly during a session.

Check the agent and loaded keys:

```bash
ssh-add -l
```

If no agent is running in a simple Bash session, start one:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_lab
ssh-add -l
```

Remove a key from the agent when no longer needed:

```bash
ssh-add -d ~/.ssh/id_ed25519_lab
```

Remove all identities from the current agent:

```bash
ssh-add -D
```

Use `ssh-add -D` carefully: it removes all loaded identities from that agent and may affect other SSH sessions. Agent behavior differs across desktop environments and operating systems.

Avoid agent forwarding unless you understand the trust implications and need it.

## Step 9: Copy Files Securely

Copy a file to a remote host:

```bash
scp ./notes.txt USER@HOST:~/notes.txt
```

Copy a file from a remote host:

```bash
scp USER@HOST:~/notes.txt ./notes-from-server.txt
```

Use SFTP for interactive file transfer:

```bash
sftp USER@HOST
```

Common SFTP commands include `pwd`, `ls`, `put`, `get`, and `exit`.

Confirm remote paths and destination permissions before transferring sensitive data. OpenSSH's `scp` uses SFTP by default in modern versions, but behavior and options may vary.

## Step 10: Use SSH Configuration

Create or edit `~/.ssh/config`:

```sshconfig
Host lab-server
    HostName server.example.com
    User labuser
    IdentityFile ~/.ssh/id_ed25519_lab
    IdentitiesOnly yes
```

Replace the example hostname and username with authorized values. Protect the configuration file:

```bash
chmod 600 ~/.ssh/config
```

Connect using the alias:

```bash
ssh lab-server
```

A host alias reduces repeated typing. It does not replace host-key verification.

## Step 11: Verify Host Keys

Known server host keys are typically recorded in `~/.ssh/known_hosts`.

```bash
ssh-keygen -F server.example.com
```

To view a fingerprint from a trusted server console, an administrator can run a command such as:

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

If SSH reports that a host identification has changed, stop and investigate. The server may have been rebuilt legitimately, but the change could also indicate a misdirected connection or interception. Verify the new fingerprint through an independent trusted channel before updating the local record.

Do not blindly run `ssh-keygen -R HOST` or accept a replacement key until the change has been verified.

## Step 12: Troubleshoot SSH

Useful commands:

```bash
ssh -v USER@HOST
ssh -G lab-server
ssh-add -l
ssh-keygen -lf ~/.ssh/id_ed25519_lab.pub
```

Common causes:

- Wrong username or hostname.
- Network or firewall restrictions.
- SSH server not running.
- Incorrect private key selected.
- Private key permissions too open.
- Public key missing from the correct remote account's `authorized_keys`.
- Incorrect ownership or permissions on the remote `.ssh` directory.
- Host key changed or not yet verified.
- Authentication method disallowed by server policy.

On a server you administer, inspect service state and logs with the tools available on that system, such as `systemctl status ssh` or `journalctl -u ssh`. Some distributions name the service `sshd` instead.

Do not weaken server authentication settings just to make a connection work.

## 🔄 Key Rotation and Revocation

A basic rotation workflow:

1. Create a new key pair with a distinct filename.
2. Register the new public key with the authorized service or remote account.
3. Test the new key in a separate session.
4. Confirm recovery access before removing the old key.
5. Remove the old public key from accounts and services where it is no longer required.
6. Retire or securely dispose of old private-key copies according to your organization's policy.
7. Update documentation and key inventory.

If a private key is exposed, treat it as compromised. Remove the corresponding public key from every place that trusts it, replace the key, and investigate potential unauthorized access. Changing the key's passphrase alone does not revoke a compromised public key.

## 🧪 Hands-On Labs

1. Inspect the local SSH installation and `~/.ssh` directory.
2. Generate a dedicated Ed25519 lab key pair.
3. Display and record the public key fingerprint.
4. Set and verify private-key permissions.
5. Add the public key to a lab account you control.
6. Connect using the explicit key path.
7. Add the key to `ssh-agent` and inspect loaded identities.
8. Transfer a harmless text file with `scp` or `sftp`.
9. Create an SSH host alias.
10. Practice a key-rotation plan on a test account.

See [`practical.md`](practical.md) for detailed exercises and [`solutions.md`](solutions.md) for suggested answers.

## 🚀 Mini Project: SSH Access Checklist

Create a checklist or script that reports:

- SSH client version.
- Whether the selected public key exists.
- The public key fingerprint.
- Key-file permissions.
- Whether an agent has loaded identities.
- Whether a configured host alias resolves to the expected settings.

The project must not print private key contents, change server configuration, disable host-key checking, or attempt unauthorized logins. Treat verbose connection output and host inventories as potentially sensitive.

## 📂 Module Files

| File | Purpose |
|---|---|
| `README.md` | Step-by-step SSH and key management tutorial |
| `examples.md` | Copyable SSH commands and configuration examples |
| `practical.md` | Guided labs and independent challenges |
| `solutions.md` | Suggested solutions and verification commands |

## 🛡️ Security Best Practices

- Keep private keys secret and protect them with suitable permissions.
- Use a strong passphrase for private keys where appropriate.
- Verify server host keys using a trusted source.
- Never ignore changed-host-key warnings without investigation.
- Use separate keys for distinct roles or environments when practical.
- Remove obsolete public keys from systems that trust them.
- Limit access to `authorized_keys` and SSH configuration files.
- Avoid unnecessary agent forwarding.
- Do not disable authentication safeguards to bypass troubleshooting.
- Rotate compromised keys promptly and investigate the incident.
- Never commit private keys, passphrases, tokens, or sensitive connection details to Git.

## 📚 Learning Resources

- [OpenSSH Manual Pages](https://www.openssh.org/manual.html) — official OpenSSH command and configuration references.
- [OpenSSH Project](https://www.openssh.org/) — project information and documentation.
- [ssh-keygen manual](https://man.openbsd.org/ssh-keygen.1) — key generation and fingerprint management.
- [ssh-agent manual](https://man.openbsd.org/ssh-agent.1) — authentication agent behavior.
- [GitHub: Generating an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) — SSH keys for GitHub authentication.

## 🗺️ Next Steps

Continue through the [Linux and Command Line](../README.md) section of the [CubicNova DevSecOps Roadmap](../../README.md).

**Protect private keys. Verify every host. Authenticate securely.**
