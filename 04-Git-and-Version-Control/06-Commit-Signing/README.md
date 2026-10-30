# Git Commit Signing

Git commit signing attaches a cryptographic signature to a commit so others can verify that the signed commit data has not been altered and that the signature corresponds to a configured public key. GitHub can show a signature as **Verified** when its verification requirements are satisfied.

This module covers SSH and GPG signing, verification, troubleshooting, and safe key handling.

## Learning objectives

- Explain the purpose and limits of signed commits.
- Configure Git to sign commits with SSH or GPG.
- Sign individual commits and enable signing by default.
- Verify a local commit signature.
- Connect a signing public key to GitHub for hosted verification.
- Troubleshoot unsigned or unverified commits.

## Key concepts

- **Signing key:** private key used to produce a signature. Keep it private and protected.
- **Public key:** corresponding public material used to verify signatures and, for GitHub verification, added to your GitHub account as a signing key.
- **Signed commit:** a commit object containing a cryptographic signature.
- **Verified status:** GitHub has successfully verified the signature against a supported public key and account configuration.
- **Commit author/committer identity:** names and email fields in commit metadata. These fields alone are not cryptographic proof of identity.
- **Commit sign-off:** a `Signed-off-by` line, often used for a Developer Certificate of Origin (DCO). It is not the same as a cryptographic commit signature.

## Option A: SSH commit signing

SSH signing is a straightforward option for many individual developers. SSH commit signing requires Git 2.34 or later.

### 1. Check your Git version and existing key

```bash
git --version
ls -la ~/.ssh
```

Use an existing SSH key if appropriate, or generate a separate signing key. Example key generation:

```bash
ssh-keygen -t ed25519 -C "commit-signing"
```

Choose a secure passphrase and a clear filename when prompted. Do not share the private key file. If you already use an SSH key for authentication, it can also be used for signing, but GitHub requires it to be added as a signing key for signature verification.

### 2. Configure Git to use SSH signatures

Replace the example path with your actual **public** key path:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

If you created a key with a different filename, update the path. `user.signingkey` points to the public key for SSH signing.

### 3. Add the signing key to GitHub

In GitHub settings, open **SSH and GPG keys**, choose **New SSH key**, select the key type for signing if prompted, and paste the contents of your `.pub` file. Do not paste or upload the private key.

### 4. Create and verify a signed commit

```bash
git status
git add README.md
git commit -S -m "Add commit signing guide"
git log -1 --show-signature
git verify-commit HEAD
```

The final verification command should report a valid signature when your local verifier is configured correctly.

## Option B: GPG commit signing

GPG is another widely supported method. You need a GPG key pair and a working GPG installation.

### 1. Check for keys

```bash
gpg --list-secret-keys --keyid-format=long
```

If you need a key, create one using your GPG tool's key-generation flow. Protect the private key and passphrase.

### 2. Configure Git

Use the key ID from your own key listing:

```bash
git config --global user.signingkey YOUR_GPG_KEY_ID
git config --global commit.gpgsign true
```

Replace `YOUR_GPG_KEY_ID` with your real key ID. Do not copy a placeholder literally.

### 3. Add the public key to GitHub

Export the public key and add it in GitHub settings under **SSH and GPG keys**:

```bash
gpg --armor --export YOUR_GPG_KEY_ID
```

Copy only the public-key output. Never publish your secret key export.

### 4. Sign and verify

```bash
git commit -S -m "Sign a practice commit"
git log -1 --show-signature
git verify-commit HEAD
```

## Sign one commit without enabling signing globally

If your signing key is already configured, you can sign a single commit:

```bash
git commit -S -m "Sign this commit"
```

To inspect the setting:

```bash
git config --show-origin --get commit.gpgsign
git config --show-origin --get gpg.format
git config --show-origin --get user.signingkey
```

To disable default signing for the current repository only:

```bash
git config commit.gpgsign false
```

This does not remove signatures from existing commits.

## Verification on GitHub

After pushing a signed commit, open the repository's commit history or the commit details page. GitHub may show **Verified** when the signature validates and the key is correctly associated with your account. Local verification and GitHub's hosted verification are related but not identical: a commit can verify locally while GitHub lacks the required public key or identity association.

See the official [GitHub commit signature verification guide](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification).

## Troubleshooting

### `gpg failed to sign the data`

- Confirm GPG is installed and Git can find it.
- Check the configured signing key ID.
- Confirm the key is available and not expired or revoked.
- Check passphrase-agent or terminal configuration.
- If using SSH signing, check `gpg.format` and `user.signingkey`.

### Commit exists but is not shown as Verified on GitHub

- Confirm the commit was actually signed: `git log -1 --show-signature`.
- Confirm the matching public key was added as a signing key in GitHub settings.
- Confirm the commit email/identity configuration matches the account requirements.
- Confirm the commit was not rewritten after signing; rewriting creates a new commit object that must be signed again.

### Wrong signing key configured

Inspect the settings, then update the value for your chosen method. Be careful with global settings if you work across personal and organizational repositories.

## Security best practices

- Never commit or upload private signing keys, passphrases, or secret-key exports.
- Protect keys with a strong passphrase and suitable local permissions.
- Use a separate key for signing if that better fits your threat model.
- Revoke or rotate keys when compromised or no longer trusted.
- Review key ownership and expiry periodically.
- Remember that a valid signature verifies signed data against a key; it does not prove the code is safe or that the signer reviewed every line.

## Exercises

1. Inspect your Git version and existing SSH/GPG keys.
2. Configure SSH signing in a practice repository.
3. Create a signed commit and verify it locally.
4. Add the public signing key to GitHub and inspect the commit's verification status.
5. Compare `git commit -S` with `commit.gpgsign=true`.
6. Diagnose a simulated mismatch between the configured key and the key uploaded to GitHub.
7. Write a short key-rotation and incident-response checklist.

## References

- [GitHub: About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
- [GitHub: Signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
- [Git: `git commit` documentation](https://git-scm.com/docs/git-commit)
- [Git: signature format](https://git-scm.com/docs/signature-format)
