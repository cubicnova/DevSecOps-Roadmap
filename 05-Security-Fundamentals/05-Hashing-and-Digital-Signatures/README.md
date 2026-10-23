# Hashing and Digital Signatures

A practical learning module covering cryptographic hash functions, file integrity checks, HMAC, password hashing, and digital signatures.

## Learning objectives

By completing this module, you should be able to:

- Explain hashing, encryption, HMAC, and digital signatures and distinguish their purposes.
- Describe collision resistance, preimage resistance, and the avalanche effect.
- Calculate SHA-256 digests and verify file integrity using Python.
- Explain why fast hashes such as SHA-256 are not suitable for password storage.
- Generate and verify digital signatures with a maintained cryptography library.
- Identify common implementation mistakes and test integrity controls safely.

## Contents

- [`examples.md`](examples.md) — runnable Python examples and command-line checks.
- [`practical.md`](practical.md) — guided labs and exercises.
- [`solutions.md`](solutions.md) — sample answers and reference implementations.
- [`security-checklist.md`](security-checklist.md) — implementation and review checklist.

## Core concepts

### Hashing

A cryptographic hash function maps arbitrary-length input to a fixed-length digest. A secure hash is designed to make it computationally infeasible to recover an input from its digest or find two different inputs with the same digest.

Common uses include checking file integrity, signing messages, and building message authentication mechanisms. SHA-256 and SHA-3 are common modern choices for general-purpose cryptographic hashing. Avoid MD5 and SHA-1 for collision-sensitive security uses.

### Hashing is not encryption

Hashing is intended to be one-way; encryption is designed to be reversible with the appropriate key. A hash does not hide information in the same way encryption does.

### Password storage

Do not store passwords as plaintext or as a plain SHA-256/MD5 digest. Use a purpose-built password hashing function such as Argon2id, scrypt, bcrypt, or PBKDF2 with a unique salt and an appropriately tuned cost. Use a trusted framework/library rather than inventing a password-storage scheme.

### HMAC

HMAC combines a cryptographic hash function with a secret key to provide message authentication. It can help verify integrity and possession of a shared secret. A plain hash alone does not prove who created a message.

### Digital signatures

A signer uses a private key to create a signature; a verifier uses the corresponding public key to check it. Properly implemented signatures can provide message integrity and evidence that the holder of a private key signed the data. Trust in the identity behind a public key depends on key distribution, certificates, and operational controls.

Typical workflow:

1. Obtain the exact bytes to sign.
2. Sign those bytes using the private key and an approved scheme.
3. Send the message and signature to the verifier.
4. Verify the signature with the correct public key.
5. Reject if verification fails; do not treat a failed verification as a warning only.

## Environment

Python 3.10+ is recommended. Standard-library examples use `hashlib` and `hmac`. The signature example uses the maintained `cryptography` package:

```bash
python -m pip install cryptography
```

Run the scripts from a terminal. Examples use sample data only; never commit private keys, production secrets, real password data, or confidential files to a public repository.

## Further reading

- Python `hashlib`: https://docs.python.org/3/library/hashlib.html
- Python `hmac`: https://docs.python.org/3/library/hmac.html
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- NIST Digital Signature Standard (FIPS 186-5): https://csrc.nist.gov/pubs/fips/186-5/final
