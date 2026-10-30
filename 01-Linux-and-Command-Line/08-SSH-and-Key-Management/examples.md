# 💡 SSH and Key Management — Examples

These examples are intended for your own account, test VM, or authorized remote host. Replace placeholder usernames and hostnames before use.

## 1. Check OpenSSH tools

```bash
ssh -V
command -v ssh
command -v ssh-keygen
command -v ssh-agent
command -v scp
command -v sftp
```

## 2. Inspect existing SSH files

```bash
ls -la ~/.ssh
```

Do not use `cat` on a private key. To inspect a public key fingerprint:

```bash
ssh-keygen -lf ~/.ssh/id_ed25519.pub
```

The filename may differ if your key uses another name.

## 3. Generate a lab key pair

```bash
ssh-keygen -t ed25519 -C "lab-key" -f ~/.ssh/id_ed25519_lab
```

Choose a passphrase when prompted. The private key is `id_ed25519_lab`; the public key is `id_ed25519_lab.pub`.

## 4. Inspect the public key and fingerprint

```bash
cat ~/.ssh/id_ed25519_lab.pub
ssh-keygen -lf ~/.ssh/id_ed25519_lab.pub
```

Share only the public key with the service or account that should authorize it.

## 5. Set permissions

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519_lab
chmod 644 ~/.ssh/id_ed25519_lab.pub
ls -ld ~/.ssh
ls -l ~/.ssh/id_ed25519_lab*
```

Ensure you own these files and the directory. Do not change permissions on unrelated keys without checking how they are used.

## 6. Connect using a key

```bash
ssh -i ~/.ssh/id_ed25519_lab USER@HOST
```

Replace `USER` and `HOST` with authorized connection details. Verify the server fingerprint before accepting a new host key.

## 7. Install a public key on a lab server

If permitted and available:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519_lab.pub USER@HOST
```

This installs the public key for the specified remote account. Confirm that the host and username are correct.

## 8. Use ssh-agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_lab
ssh-add -l
```

Remove the lab key when done:

```bash
ssh-add -d ~/.ssh/id_ed25519_lab
```

The agent's lifecycle depends on your shell and operating system. Avoid exposing agent sockets or forwarding an agent to hosts you do not trust.

## 9. Copy files

```bash
printf 'Harmless SSH lab note\n' > notes.txt
scp ./notes.txt USER@HOST:~/notes.txt
scp USER@HOST:~/notes.txt ./notes-from-server.txt
```

For interactive transfer:

```bash
sftp USER@HOST
```

Inside SFTP, common commands include `pwd`, `ls`, `put notes.txt`, `get notes.txt`, and `exit`.

## 10. Configure a host alias

Add to `~/.ssh/config`:

```sshconfig
Host lab-server
    HostName server.example.com
    User labuser
    IdentityFile ~/.ssh/id_ed25519_lab
    IdentitiesOnly yes
```

Then:

```bash
chmod 600 ~/.ssh/config
ssh -G lab-server
ssh lab-server
```

Replace example values before connecting.

## 11. Verify host-key records

```bash
ssh-keygen -F server.example.com
```

If a host-key warning appears, independently verify the server's new fingerprint with an administrator or trusted console. Do not automatically remove the old record or disable checking.

## 12. Verbose troubleshooting

```bash
ssh -v -i ~/.ssh/id_ed25519_lab USER@HOST
```

Look for which key is offered and the reason authentication fails. Review verbose output before sharing because it may reveal internal connection details.

## 13. Inspect SSH server configuration (authorized server only)

On a server you administer:

```bash
sudo sshd -t
```

This tests SSH daemon configuration syntax on systems where `sshd` supports `-t`. It does not replace a review of the configuration or a safe reload plan.

Service names vary. Common examples include:

```bash
systemctl status ssh
systemctl status sshd
```

Use the service name that exists on the distribution. Do not restart a remote SSH service without a recovery plan and authorized access.

## 14. Key rotation checklist

1. Generate a new key under a distinct filename.
2. Add its public key to the authorized account.
3. Test a new connection in a separate terminal.
4. Confirm you have a recovery method.
5. Remove the old public key from the relevant authorized-key lists.
6. Update your key inventory.

If a private key is compromised, remove the associated public key from every trusting service and investigate potential misuse.
