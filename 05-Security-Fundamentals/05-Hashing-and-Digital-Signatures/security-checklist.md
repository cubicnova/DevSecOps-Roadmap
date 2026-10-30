# Hashing and Digital Signature Security Checklist

Use this checklist during code review, architecture review, or release engineering.

## Hashing and integrity

- [ ] Use a modern cryptographic hash (for example, SHA-256 or SHA-3) for general cryptographic integrity use.
- [ ] Do not use MD5 or SHA-1 where collision resistance is a security requirement.
- [ ] Hash exact bytes; avoid accidental text encoding or newline transformations.
- [ ] For large files, stream data in chunks rather than loading everything into memory.
- [ ] Obtain expected checksums from a trusted, authenticated source.
- [ ] Do not confuse a checksum with proof of publisher identity.

## Password storage

- [ ] Never store plaintext passwords.
- [ ] Do not use plain SHA-256, SHA-1, or MD5 as a password-storage scheme.
- [ ] Use a maintained password-hashing implementation such as Argon2id, scrypt, bcrypt, or PBKDF2 when appropriate.
- [ ] Ensure each password has a unique salt generated/managed by the library.
- [ ] Benchmark and configure cost parameters for the deployment environment.
- [ ] Store algorithm/version/parameters so hashes can be upgraded.
- [ ] Do not log passwords, password hashes, reset tokens, or authentication secrets.
- [ ] Apply rate limiting and monitoring to authentication endpoints.

## HMAC

- [ ] Use a standard HMAC implementation rather than a home-grown construction.
- [ ] Protect shared keys in a secret manager or approved key-management service.
- [ ] Compare tags using a constant-time comparison helper where available.
- [ ] Authenticate the exact canonical bytes and reject malformed or unexpected input.
- [ ] Define key rotation, revocation, access control, and incident response.
- [ ] Remember that any holder of the shared key can generate valid tags.

## Digital signatures

- [ ] Use a vetted cryptographic library and a suitable, supported signature scheme.
- [ ] Keep private keys secret and restrict signing permissions.
- [ ] Never commit private keys to Git or embed them in client-side code.
- [ ] Verify signatures before installing, executing, or trusting artifacts.
- [ ] Authenticate public keys independently of the untrusted artifact source.
- [ ] Validate certificate chains, identities, validity periods, and revocation as required by the design.
- [ ] Sign and verify the exact same byte representation or a well-defined canonical format.
- [ ] Treat verification failures as hard failures.
- [ ] Plan key backup, rotation, revocation, and compromise recovery.
- [ ] Log security-relevant signing events without logging private key material.

## Final review

- [ ] Threat model documents what the hash, MAC, or signature is intended to prove.
- [ ] Tests cover altered messages, incorrect keys, malformed signatures, and corrupted files.
- [ ] Dependencies are maintained and updated.
- [ ] Cryptographic choices meet applicable policy and compliance requirements.
