# Commit Signing — Suggested Solutions

These examples assume a properly installed signing tool and a key you control. Replace example paths and placeholders with your actual configuration.

## Exercise 1 — Inspect configuration

```bash
git --version
git config --show-origin --get gpg.format
git config --show-origin --get user.signingkey
git config --show-origin --get commit.gpgsign
```

Git settings may come from system, global, local repository, or worktree configuration. The `--show-origin` output helps identify the source.

## Exercise 2 — Public versus private key

The private key creates signatures and must remain secret. The public key is shared with verifiers so they can validate signatures. A `.pub` file is the public half of an SSH key pair.

## Exercise 3 — SSH signing setup

For Git 2.34 or later:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

Use your actual public-key path. Register the public key in GitHub settings as a signing key; never upload the private key.

## Exercise 4 — Sign and verify

```bash
git add README.md
git commit -S -m "Add signed commit practice"
git log -1 --show-signature
git verify-commit HEAD
```

A successful local verification indicates that the local verifier accepts the signature. It does not alone guarantee GitHub will display **Verified**.

## Exercise 5 — GitHub verification

Possible causes of a missing **Verified** badge include:
- the commit was not signed;
- the corresponding public key was not registered as a signing key;
- the key is associated with a different account;
- the committer identity does not meet GitHub's verification requirements;
- the commit was rewritten after signing.

Check the commit details and settings rather than sharing private key data.

## Exercise 6 — SSH versus GPG

SSH signing is often simpler when SSH keys are already in use. GPG provides additional key-management features such as expiry and revocation. Organizational requirements, tooling, and key lifecycle practices should guide the choice.

## Exercise 7 — Troubleshooting

1. **Signing failure:** check installed tools, configured key, key availability, passphrase agent, terminal environment, and `gpg.format`.
2. **Local verified, GitHub not verified:** confirm the public key is registered as a signing key on the correct account and the commit identity matches requirements.
3. **Unexpected key:** inspect `git config --show-origin --get user.signingkey` and correct the appropriate configuration scope.
4. **Suspected compromise:** stop using the key, follow the organization's incident process, revoke or remove the key where appropriate, generate a replacement, update registrations, and review affected commits.

## Exercise 8 — Example team policy

- All commits to protected branches must be signed using an approved method.
- Public signing keys must be registered with the developer's account and verified during onboarding.
- Private keys must be passphrase-protected and excluded from repositories and CI logs.
- Compromised or retired keys must be revoked or removed promptly.
- Reviewers must check required status checks and signature verification before merging.
- Exceptions must be documented and approved according to team policy.

## Mini-project — Signed release checklist

- [ ] Working tree is clean and release commit is reviewed.
- [ ] Required tests pass.
- [ ] Commit signature verifies locally.
- [ ] Public signing key is registered with the expected account.
- [ ] Release tag name and target commit are correct.
- [ ] Signed tag verifies, if the release process requires signed tags.
- [ ] No private keys or credentials are included in the release.
- [ ] Release artifacts and notes are reviewed before publication.
