# ✅ SSH and Key Management — Solutions

Use these examples only with your own account or an authorized test environment. Never paste private keys or passphrases into reports or chat.

## Lab 1 — Inspect the client

```bash
ssh -V
command -v ssh
command -v ssh-keygen
command -v ssh-agent
ls -la ~/.ssh
```

The `.ssh` directory may contain configuration, known-host records, public keys, private keys, and other SSH-related files. Do not reveal private-key contents.

## Lab 2 — Generate a lab key pair

```bash
ssh-keygen -t ed25519 -C "lab-key" -f ~/.ssh/id_ed25519_lab
```

Enter a strong passphrase when prompted. If the target file exists, choose a new filename or deliberately follow your key-replacement process rather than overwriting it.

Inspect the public key and fingerprint:

```bash
ssh-keygen -lf ~/.ssh/id_ed25519_lab.pub
cat ~/.ssh/id_ed25519_lab.pub
```

The private key is `~/.ssh/id_ed25519_lab`; the public key is `~/.ssh/id_ed25519_lab.pub`.

## Lab 3 — Permissions

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519_lab
chmod 644 ~/.ssh/id_ed25519_lab.pub
ls -ld ~/.ssh
ls -l ~/.ssh/id_ed25519_lab*
```

Typical permissions are `700` for the SSH directory, `600` for the private key, and `644` for the public key. Ownership and platform-specific access controls also matter.

## Lab 4 — Public-key authorization

On a permitted host, one common setup method is:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519_lab.pub USER@HOST
ssh -i ~/.ssh/id_ed25519_lab USER@HOST
```

Replace `USER` and `HOST` with verified details. `ssh-copy-id` must be available, and the remote account must permit the setup method. Cloud environments may use a provider-managed process instead.

Verify the server fingerprint before accepting a first connection. Do not change server authentication settings merely to make the lab pass.

## Lab 5 — Agent management

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_lab
ssh-add -l
ssh-add -d ~/.ssh/id_ed25519_lab
ssh-add -l
```

Agent management differs by operating system and desktop session. Do not run `ssh-add -D` unless you intend to remove all identities loaded in that agent.

## Lab 6 — File transfer

Create harmless test data:

```bash
printf 'SSH file-transfer lab\n' > notes.txt
```

Upload and download:

```bash
scp ./notes.txt USER@HOST:~/notes.txt
scp USER@HOST:~/notes.txt ./notes-from-server.txt
cmp notes.txt notes-from-server.txt
```

If `cmp` prints nothing and exits successfully, the files match. For SFTP, run `sftp USER@HOST`, then use `put notes.txt`, `get notes.txt`, and `exit`.

## Lab 7 — SSH configuration

Example `~/.ssh/config` entry:

```sshconfig
Host lab-server
    HostName server.example.com
    User labuser
    IdentityFile ~/.ssh/id_ed25519_lab
    IdentitiesOnly yes
```

Protect and inspect it:

```bash
chmod 600 ~/.ssh/config
ssh -G lab-server
```

Replace the example host and username with verified values before connecting. `ssh -G` prints the effective client configuration; it does not prove the server is reachable or authenticated.

## Lab 8 — Troubleshooting guide

### `Permission denied (publickey)`

- Confirm the username and host.
- Confirm the client is offering the intended key: `ssh -v -i ~/.ssh/id_ed25519_lab USER@HOST`.
- Confirm the matching public key is installed for that remote account.
- On a server you administer, check ownership, permissions, server policy, and authentication logs.

### Private key permissions are too open

```bash
chmod 600 ~/.ssh/id_ed25519_lab
```

Ensure the key is owned by the expected local user. Do not recursively change permissions on the whole home directory.

### Hostname cannot be resolved

Check spelling and DNS configuration, and verify the host information with the administrator. A DNS failure differs from a host-key verification failure.

### Connection times out

Check network reachability, routing, firewall policy, server address, and whether the server is listening. Do not assume the SSH service itself is the only possible cause.

### Host identification changed

Stop. Verify the new host fingerprint with an independent trusted source, such as the server console or administrator. Only after confirming a legitimate change should you update the known-host record.

### Wrong key offered

Inspect `ssh -v` output, use `-i` with the intended key, or set `IdentityFile` and `IdentitiesOnly yes` in the host configuration.

### Connection refused

The host may be reachable but not accepting connections on that address and port. Check service state and firewall configuration with an authorized administrator.

## Lab 9 — Key rotation plan

Suggested workflow:

1. Treat the exposed private key as compromised.
2. Identify all services and accounts that trust its public key.
3. Generate a replacement key on a trusted device.
4. Register the replacement public key.
5. Test new authentication in a separate session.
6. Remove the old public key from all authorized locations.
7. Review relevant authentication logs and investigate suspicious activity.
8. Follow the repository's secret-incident procedure to remove the exposed material where possible.
9. Store the replacement key securely and update the key inventory.

Changing the passphrase does not invalidate a copied private key. Removing a key from the local agent also does not remove its public key from remote servers.

## Lab 10 — Example local checklist script

Save as `ssh-audit-checklist.sh`:

```bash
#!/usr/bin/env bash
set -u

key="${1:-$HOME/.ssh/id_ed25519_lab.pub}"
alias_name="${2:-lab-server}"

echo "===== SSH Client ====="
if command -v ssh >/dev/null 2>&1; then
    ssh -V 2>&1
else
    echo "ssh client not found."
fi

echo
echo "===== Public Key ====="
if [[ -f "$key" && -r "$key" ]]; then
    printf 'Public key file: %s\n' "$key"
    ssh-keygen -lf "$key"
else
    printf 'Public key file missing or unreadable: %s\n' "$key" >&2
fi

echo
echo "===== Permissions ====="
if [[ -e "$key" ]]; then
    ls -l -- "$key"
fi
if [[ -d "$HOME/.ssh" ]]; then
    ls -ld -- "$HOME/.ssh"
fi

echo
echo "===== Agent ====="
if command -v ssh-add >/dev/null 2>&1; then
    ssh-add -l 2>&1 || true
else
    echo "ssh-add not available."
fi

echo
echo "===== Client Configuration ====="
if command -v ssh >/dev/null 2>&1; then
    ssh -G "$alias_name" 2>/dev/null |
        grep -E '^(hostname|user|identityfile|identitiesonly) ' || true
fi
```

Run:

```bash
chmod u+x ssh-audit-checklist.sh
bash -n ssh-audit-checklist.sh
./ssh-audit-checklist.sh
```

Optional arguments can specify a public key path and a configured host alias:

```bash
./ssh-audit-checklist.sh ~/.ssh/id_ed25519_lab.pub lab-server
```

The script inspects local SSH settings only. It does not read private-key contents, accept host keys, or change remote access.

## Reflection — Suggested answers

1. **Host key vs user key:** The host key authenticates the server to the client; a user key pair authenticates a user to the server.
2. **Private vs public key:** The private key must be protected; the public key can be distributed to services that should trust it.
3. **Passphrase:** It adds a layer of protection if the private key file is copied or stolen.
4. **`authorized_keys`:** Lists public keys allowed to authenticate to a particular remote account.
5. **`ssh-agent`:** Holds unlocked key identities and can perform authentication signatures on request.
6. **Changed host key:** It may be a legitimate rebuild or a security issue; verify the fingerprint independently.
7. **`IdentitiesOnly yes`:** Restricts authentication attempts to configured identity files and certificates rather than offering every available agent identity.
8. **Agent forwarding:** A remote host may gain the ability to request signatures through the forwarded agent during the session; use only with trusted hosts and suitable restrictions.
9. **Exposed private key:** Treat it as compromised, revoke its trust on servers and services, replace it, and investigate possible misuse.
10. **Agent removal vs revocation:** Removing a local identity stops that agent from offering it; remote `authorized_keys` entries and other trust registrations remain until separately removed.

## Completion criteria

You can create and identify key pairs, protect private keys, explain host verification, configure public-key access on a lab server, transfer files, use an agent carefully, and describe a safe key rotation response.
