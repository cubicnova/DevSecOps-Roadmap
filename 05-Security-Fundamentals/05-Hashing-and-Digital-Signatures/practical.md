# Practical Labs: Hashing and Digital Signatures

Use only files and systems you own or have explicit permission to test. These labs use local sample data.

## Lab 1 — Observe the avalanche effect

**Goal:** See how a small input change affects a digest.

1. Use `hashlib.sha256()` to hash `b"hello"`.
2. Hash `b"Hello"` and `b"hello!"`.
3. Compare the three hexadecimal outputs.
4. Explain why the digest is not a meaningful summary of the input's human-readable content.

**Deliverable:** A short table of input and SHA-256 digest.

## Lab 2 — Build a file integrity checker

**Goal:** Calculate and compare a file digest.

1. Create `sample.txt` containing a few lines of text.
2. Calculate SHA-256 using Python or the OS command.
3. Add one character to the file and calculate the digest again.
4. Restore the original file and verify that the digest returns to the original value.
5. Explain why the expected checksum must be obtained from a trusted channel.

**Deliverable:** Script and a short test report.

## Lab 3 — HMAC message authentication

**Goal:** Authenticate a message with a shared secret.

1. Generate an HMAC-SHA-256 tag for a sample message.
2. Verify the original message and tag.
3. Change the message but keep the original tag; verification should fail.
4. Change one character in the tag; verification should fail.
5. List two secure ways to provision and rotate the shared key.

**Deliverable:** Python script and results.

## Lab 4 — Password storage design review

**Goal:** Identify insecure password storage patterns.

Review the following hypothetical implementations:

- A: `sha256(password).hexdigest()`
- B: MD5 with a fixed salt shared by every account
- C: Argon2id through a reputable password-hashing library with unique salts and suitable parameters
- D: Passwords encrypted with a reversible application key

For each, explain the risks and choose the preferred approach for a new application. Do not use real user passwords.

**Deliverable:** One-page review with a remediation plan.

## Lab 5 — Digital signature verification

**Goal:** Verify authenticity and integrity with an asymmetric key pair.

1. Install `cryptography`.
2. Generate an Ed25519 key pair in a local script.
3. Sign a sample release manifest.
4. Verify the original bytes.
5. Change one byte and verify again.
6. Explain why a valid signature alone does not prove that the public key belongs to a particular publisher.

**Deliverable:** Script plus a screenshot or terminal transcript.

## Lab 6 — Release artifact verification

**Goal:** Design a safer release distribution workflow.

Write a checklist for publishing a software archive. Include:

- SHA-256 checksum for accidental/corruption detection.
- Digital signature and an independently trusted public key for authenticity.
- Secure storage and restricted access for the private signing key.
- Key rotation and incident response if a signing key is exposed.
- A clear failure path when verification fails.

**Deliverable:** `release-verification-checklist.md`.

## Lab 7 — Review a flawed design

A service stores `SHA256(password + "company-salt")` in its database, logs the resulting digest during login failures, and distributes signed update files with the public key downloaded from the same untrusted mirror as the update.

Identify at least four issues and propose safer alternatives.

## Completion criteria

- [ ] Can distinguish hashing, HMAC, password hashing, encryption, and digital signatures.
- [ ] Can calculate and verify file hashes.
- [ ] Can test an HMAC with altered message/tag values.
- [ ] Can explain why salts are unique and why password hashing must be slow/adaptive.
- [ ] Can generate and verify a digital signature.
- [ ] Can describe trusted public-key distribution and private-key protection.
