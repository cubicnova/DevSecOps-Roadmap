# 04 - Cryptography Fundamentals

Cryptography uses mathematical techniques to protect information. It supports confidentiality, integrity, authentication, and digital signatures.

## Learning Objectives
- Explain plaintext, ciphertext, encryption, decryption, and keys.
- Compare symmetric and asymmetric cryptography.
- Distinguish encryption, hashing, HMAC, and digital signatures.
- Understand secure randomness, key management, certificates, and common implementation mistakes.

## Core Concepts

### Symmetric Cryptography
Uses a shared secret key for encryption and decryption. It is efficient for bulk data protection, such as files, backups, and databases. Use a vetted authenticated-encryption implementation, such as AES-GCM where appropriate, and follow its nonce requirements.

### Asymmetric Cryptography
Uses a related public/private key pair. Public keys may be distributed; private keys must be protected. Common uses include digital signatures, certificates, and key establishment. Not every public-key algorithm supports every use case.

### Encryption, Hashes, HMAC, and Signatures

| Mechanism | Main purpose | Secret/key use | Reversible? |
|---|---|---|---|
| Encryption | Confidentiality | Secret key or public/private keys | Yes, with the appropriate decryption key |
| Cryptographic hash | Digest/change detection with a trusted expected value | No key | No |
| HMAC | Integrity and authenticity between secret-sharing parties | Shared secret | No |
| Digital signature | Integrity and signer authentication | Private key signs; public key verifies | No |

A hash alone does not authenticate a file. If an attacker can replace both the file and its expected hash, the check may still pass. Use a trusted signature or authenticated mechanism when origin matters.

### Key Management
- Generate keys using cryptographically secure randomness.
- Never commit production secrets or private keys to Git.
- Store secrets in a suitable secret manager or protected key store.
- Apply least privilege, monitor access, and plan rotation and revocation.
- Do not log keys, tokens, passwords, or sensitive plaintext.

### Certificates and TLS
TLS certificates help bind a public key to an identity. Validate certificate chains and hostnames, monitor expiry, and protect private keys. Never disable certificate validation as a permanent workaround.

### Common Mistakes
- Treating Base64 as encryption.
- Using obsolete algorithms or insecure modes.
- Reusing nonces where uniqueness is required.
- Hardcoding secrets in source code or CI/CD logs.
- Using a fast general-purpose hash alone for password storage.
- Designing custom cryptographic algorithms.
- Trusting a checksum from the same untrusted source as the file.

## Module Files
- [`examples.md`](examples.md): worked examples and code snippets.
- [`exercises.md`](exercises.md): knowledge checks and safe labs.
- [`solutions.md`](solutions.md): suggested answers and explanations.

## Further Reading
- [NIST Cryptography](https://www.nist.gov/cryptography)
- [NIST Cryptographic Standards and Guidelines](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)
- [NIST Key Management FAQs](https://csrc.nist.gov/Projects/Key-Management/faqs)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

## Completion Checklist
- [ ] I can distinguish symmetric and asymmetric cryptography.
- [ ] I understand encryption, hashing, HMAC, and signatures.
- [ ] I can describe safe key and secret handling.
- [ ] I understand why secure randomness and TLS validation matter.
