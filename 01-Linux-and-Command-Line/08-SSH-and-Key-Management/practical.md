# 🧪 SSH and Key Management — Practical Labs

**Level:** Beginner to intermediate  
**Estimated time:** 90–120 minutes  
**Environment:** Linux/WSL/macOS SSH client and, for remote labs, a test host you control

## Safety rules

- Never share private keys or passphrases.
- Do not overwrite existing keys until you know what depends on them.
- Use only systems and accounts you are authorized to access.
- Verify host fingerprints through a trusted channel.
- Do not bypass host-key checking to silence warnings.
- Do not change a remote SSH server configuration unless you have authorization and recovery access.

## Lab 1 — Inspect the SSH client

**Tasks**

1. Print the SSH client version.
2. Locate `ssh`, `ssh-keygen`, and `ssh-agent`.
3. List the filenames in `~/.ssh` without printing private-key contents.
4. Identify public/private key pairs, if any.

**Hints:** `ssh -V`, `command -v`, `ls -la`

## Lab 2 — Generate a dedicated key pair

**Tasks**

1. Generate an Ed25519 key pair named `id_ed25519_lab`.
2. Set a passphrase.
3. Identify the private and public key files.
4. Generate the public-key fingerprint.
5. Explain why the private key must remain secret.

**Hint:**

```bash
ssh-keygen -t ed25519 -C "lab-key" -f ~/.ssh/id_ed25519_lab
```

If that filename already exists, choose another unique name rather than overwriting it.

## Lab 3 — Secure key permissions

**Tasks**

1. Inspect `.ssh` directory and key permissions.
2. Set the directory to `700`.
3. Set the lab private key to `600`.
4. Set the lab public key to `644`.
5. Verify ownership and permissions.

**Hints:** `chmod`, `ls -ld`, `ls -l`

## Lab 4 — Understand public-key authorization

Using a test server or cloud VM you control:

1. Record the remote username and hostname.
2. Verify the server's host-key fingerprint from a trusted channel.
3. Add the lab public key to the correct remote account using an approved method.
4. Test a new SSH session with the explicit identity file.
5. Confirm you can still recover access before changing other authentication methods.

If no remote host is available, document the steps and use the local key files for fingerprint and permission practice.

## Lab 5 — Use ssh-agent

**Tasks**

1. Start or identify your SSH agent.
2. Add the lab key.
3. List loaded identities.
4. Remove the lab key.
5. Explain why agent access should be protected.

**Hints:** `ssh-agent`, `ssh-add -l`, `ssh-add`, `ssh-add -d`

## Lab 6 — File transfer

Using an authorized test host:

1. Create a harmless text file.
2. Upload it with `scp`.
3. Download it under a different local filename.
4. Compare the two local files.
5. Repeat using `sftp`.

Do not transfer credentials or sensitive data for this lab.

## Lab 7 — SSH client configuration

**Tasks**

1. Create a host alias in `~/.ssh/config`.
2. Set the hostname, username, identity file, and `IdentitiesOnly yes`.
3. Set file permissions to `600`.
4. Inspect the resolved configuration with `ssh -G ALIAS`.
5. Connect only after verifying the host fingerprint.

If you do not have a server, use a placeholder configuration and do not attempt a connection.

## Lab 8 — Troubleshooting scenarios

For each scenario, write down the diagnostic commands and a safe next step:

1. SSH says `Permission denied (publickey)`.
2. The private key is ignored because permissions are too open.
3. The server hostname cannot be resolved.
4. The connection times out.
5. The host identification has changed.
6. The wrong key is being offered.
7. The server refuses connections.

**Hints:** `ssh -v`, `ssh-add -l`, `ssh-keygen -lf`, `ssh -G`, network diagnostics, server logs when authorized.

Never resolve a host-key warning by disabling verification.

## Lab 9 — Key rotation tabletop exercise

You suspect a private key was accidentally committed to a repository.

Write a response plan that:

1. Treats the key as compromised.
2. Identifies every account or service trusting its public key.
3. Removes the compromised public key from those trust locations.
4. Creates a replacement key and registers the new public key.
5. Tests recovery access before removing fallback access.
6. Reviews logs for possible misuse.
7. Removes the exposed secret from repositories and history according to incident procedures, without assuming history rewriting alone revokes the key.

## Lab 10 — Mini project: SSH access checklist

Create `ssh-audit-checklist.sh` or a Markdown checklist that reports:

- SSH client version.
- Existence of a chosen public key.
- Fingerprint of that public key.
- File permissions.
- Agent identity count, where available.
- Resolved configuration for a named alias, if configured.

Requirements:

- Never read or print private key contents.
- Do not change remote configuration.
- Do not automatically accept host keys.
- Do not expose sensitive details in shared reports.

## Submission checklist

- [ ] SSH tools inspected.
- [ ] Dedicated key pair created or existing key documented.
- [ ] Public-key fingerprint recorded.
- [ ] Private-key permissions checked.
- [ ] Host-key verification explained.
- [ ] Agent identity added and removed, if supported.
- [ ] File transfer tested on an authorized host or documented.
- [ ] SSH alias configuration inspected.
- [ ] Troubleshooting scenarios answered.
- [ ] Key rotation plan written.

## Reflection questions

1. What is the difference between a host key and a user authentication key?
2. What is the difference between a private key and its `.pub` file?
3. Why use a passphrase?
4. What does `authorized_keys` do?
5. What does `ssh-agent` store?
6. Why is a changed host-key warning important?
7. What is the purpose of `IdentitiesOnly yes`?
8. Why should agent forwarding be used cautiously?
9. What should happen if a private key is exposed?
10. Why is removing a key from `ssh-agent` not the same as revoking it on servers?
