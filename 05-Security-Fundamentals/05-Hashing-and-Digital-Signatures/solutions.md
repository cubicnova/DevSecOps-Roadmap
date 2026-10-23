# Solutions and Reference Answers

Use these as a guide after attempting the practical labs.

## Lab 1 — Avalanche effect

The three inputs should produce different SHA-256 digests. A cryptographic hash is designed so that small changes in input cause unpredictable, large changes in output. Do not expect the output to reveal which input was used.

## Lab 2 — File integrity checker

A correct solution opens the file in binary mode, reads all bytes (preferably in chunks for large files), and compares the resulting digest against an independently trusted expected digest.

```python
import hashlib
import hmac
from pathlib import Path

def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

expected = input("Trusted SHA-256: ").strip().lower()
actual = sha256_file("sample.txt").lower()
print("PASS" if hmac.compare_digest(expected, actual) else "FAIL")
```

The script does not establish trust in the expected digest. If an attacker can replace both the file and checksum, the comparison can still pass.

## Lab 3 — HMAC

The receiver must calculate an HMAC over the exact received bytes using the same secret key and compare the received tag with `hmac.compare_digest`. Any change to the message or tag should make verification fail. Provision secrets through a secret manager or a secure key-management process; rotate them with an overlap period and a documented revocation plan where appropriate.

## Lab 4 — Password storage

- **A:** Insecure for password storage because SHA-256 is fast and enables high-rate offline guessing.
- **B:** Insecure because MD5 is unsuitable and a shared salt removes per-user salt uniqueness; it does not prevent efficient guessing.
- **C:** Preferred among the options. Use a maintained implementation, unique salts, suitable parameters, rate limiting, and an upgrade strategy.
- **D:** Usually inappropriate because compromise of the encryption key may reveal every password. Password verification normally does not require recovering the original password.

Never invent a custom password hashing construction. See the OWASP Password Storage Cheat Sheet.

## Lab 5 — Digital signature

The valid signature verifies only for the exact signed bytes and corresponding public key. Changing the message should raise `InvalidSignature`. A public key must be authenticated through a trusted distribution mechanism, certificate validation, a verified fingerprint, or another out-of-band trust process.

## Lab 6 — Release artifact verification

A checksum is useful for detecting corruption when its source is trusted, but it is not by itself proof of publisher identity. Sign the release metadata or artifact with a protected private key; verify using a trusted public key or certificate chain. Limit signing permissions, audit signing activity, rotate keys under a documented procedure, and publish revocation/recovery guidance.

## Lab 7 — Flawed design

Issues and remediations:

1. **Fast password hash:** Replace with Argon2id, scrypt, bcrypt, or PBKDF2 via a trusted library.
2. **Fixed shared salt:** Use a unique random salt per password, managed by the password-hashing library.
3. **Hash logged:** Never log password material or password-derived authentication values. Remove the logging and review access/retention of existing logs.
4. **Untrusted key distribution:** Obtain and verify the public key through a trusted independent channel, authenticated certificate chain, or pinned fingerprint.
5. **Missing integrity-failure handling:** Reject altered artifacts and avoid executing or installing them.
6. **Potential secret exposure:** If the shared salt was intended to be secret, it is not a substitute for a properly managed pepper or a password hashing scheme. Keep any pepper in a separate secrets system.

## Review questions

1. **Does hashing provide confidentiality?** No. Hashing is not reversible encryption and does not hide low-entropy data from guessing.
2. **Does a plain hash prove who created a file?** No. Anyone can compute a hash. Use a trusted digital signature or authenticated MAC depending on the trust model.
3. **Can HMAC provide public verification?** No. The verifier needs the shared secret and can also create tags.
4. **Why use a salt?** A unique random salt prevents identical passwords from producing identical stored hashes and defeats precomputed rainbow-table reuse.
5. **Why protect the private signing key?** Anyone who obtains it may be able to create signatures that verifiers trust.
6. **What should happen after signature verification fails?** Reject the artifact/message and follow the incident/reporting procedure; do not continue as if verification succeeded.
