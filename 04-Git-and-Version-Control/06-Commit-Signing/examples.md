# Commit Signing — Examples

These examples assume you have already generated a key and configured the correct signing method. Do not copy placeholder key IDs as literal values.

## 1. Inspect Git signing configuration

```bash
git --version
git config --show-origin --get gpg.format
git config --show-origin --get user.signingkey
git config --show-origin --get commit.gpgsign
```

A missing value can mean the setting is not configured at that scope.

## 2. Configure SSH signing

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

Use the path to your actual public key. SSH signing support requires Git 2.34 or later.

## 3. Sign one commit

```bash
git add README.md
git commit -S -m "Document commit signing"
```

The `-S` option requests a cryptographic signature for that commit.

## 4. Verify the latest commit

```bash
git log -1 --show-signature
git verify-commit HEAD
```

Local verification depends on your Git and signature-tool configuration.

## 5. Configure GPG signing

```bash
gpg --list-secret-keys --keyid-format=long
git config --global user.signingkey YOUR_GPG_KEY_ID
git config --global commit.gpgsign true
```

Replace the placeholder with a key ID from your own key list.

## 6. Export a GPG public key

```bash
gpg --armor --export YOUR_GPG_KEY_ID
```

Add only the public-key output to the appropriate GitHub settings. Do not export or share the secret key.

## 7. Check the commit's identity metadata

```bash
git log -1 --format=fuller
git config user.name
git config user.email
```

Names and email addresses are metadata; they are not a substitute for signature verification.

## 8. Temporarily disable default signing in one repository

```bash
git config commit.gpgsign false
```

To turn it back on for that repository:

```bash
git config commit.gpgsign true
```

This setting changes future default behavior and does not alter signatures already recorded.

## 9. Diagnose a key mismatch

```bash
git config --show-origin --get gpg.format
git config --show-origin --get user.signingkey
git log -1 --show-signature
```

Compare the configured key with the key you intended to use. For GitHub's **Verified** status, also check that the matching public signing key has been added to the correct account.

## 10. Sign a tag

For a GPG key configured in Git:

```bash
git tag -s v1.0.0 -m "Release v1.0.0"
git tag -v v1.0.0
```

SSH and other supported signature formats have their own configuration requirements. Verify the tag before publishing it.
