# Commit Signing — Exercises

Use a personal practice repository. Never share private keys or passphrases.

## Exercise 1 — Inspect your environment

Run:

```bash
git --version
git config --show-origin --get gpg.format
git config --show-origin --get user.signingkey
git config --show-origin --get commit.gpgsign
```

Record which settings are configured and at what scope. Do not include private key contents in your notes.

## Exercise 2 — Inspect existing keys

For SSH, list filenames in `~/.ssh` and identify public-key files ending in `.pub`. For GPG, use:

```bash
gpg --list-secret-keys --keyid-format=long
```

Explain the difference between a private key and a public key.

## Exercise 3 — Configure SSH signing

Configure SSH signing using a key you control. Confirm Git is 2.34 or later, set `gpg.format` to `ssh`, and set `user.signingkey` to the public-key path.

**Validation:** inspect the effective Git settings and confirm they point to the intended key.

## Exercise 4 — Create a signed commit

Make a small change in a practice repository, then sign it:

```bash
git add README.md
git commit -S -m "Add signed commit practice"
git verify-commit HEAD
```

Record the verification result without exposing sensitive key material.

## Exercise 5 — GitHub verification

Add the public signing key to the correct GitHub account. Push the signed commit and inspect the commit page.

Explain why a locally valid signature might not display as **Verified** on GitHub.

## Exercise 6 — Compare signing methods

Research SSH and GPG signing. Compare setup complexity, key management, expiry/revocation options, and fit for your team. Do not assume one method is universally best.

## Exercise 7 — Troubleshooting

For each scenario, list likely causes and safe checks:

1. `git commit -S` fails with a signing error.
2. A commit verifies locally but not on GitHub.
3. Git uses an unexpected key.
4. A signing key is suspected to be compromised.

## Exercise 8 — Team policy

Draft a policy that specifies:
- whether signing is required;
- supported signing formats;
- how public keys are registered;
- how keys are rotated or revoked;
- how reviewers check verification status;
- what to do if a key is lost or compromised.

## Mini-project — Signed release checklist

Prepare a checklist for creating a signed release tag. Include version naming, clean working tree, tests, commit verification, tag verification, key handling, and release publication steps.
