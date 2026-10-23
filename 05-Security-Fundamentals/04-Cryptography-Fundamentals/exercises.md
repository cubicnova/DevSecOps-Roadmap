# Cryptography Fundamentals - Exercises

Use test data and non-production keys only. Never commit real credentials, API keys, passwords, or private keys.

## Part A: Knowledge Check
1. Explain plaintext and ciphertext.
2. Compare symmetric and asymmetric cryptography and give one use case for each.
3. Explain the difference between encryption and hashing.
4. What does HMAC provide that a plain hash does not?
5. What can a digital signature help a verifier establish?
6. Why is Base64 not encryption?
7. Why is secure randomness important for cryptographic keys?
8. Why should TLS certificate validation remain enabled?

## Part B: Select a Mechanism
For each requirement, select an appropriate mechanism and justify your choice.
1. Protect a database backup so only authorized systems can read it.
2. Detect changes to a downloaded file using a trusted expected digest.
3. Verify a software release was signed by a trusted publisher.
4. Authenticate a message between two services that share a secret.
5. Generate a high-entropy temporary session token.
6. Store user passwords to resist offline guessing after a database leak.

## Part C: Practical Labs

### Lab 1: File Hashing
1. Create `sample.txt` with the text `cryptography lab`.
2. Calculate its SHA-256 digest using the Python example in `examples.md`.
3. Change one character and calculate the digest again.
4. Record both results and explain why the digest changed.
5. Explain why a trusted expected digest or signature is needed.

### Lab 2: Secure Randomness
1. Generate three tokens with Python's `secrets` module.
2. Confirm the outputs differ.
3. Explain why `random` is unsuitable for security tokens.
4. Describe safe token storage, expiry, and revocation.

### Lab 3: HMAC
1. Run the HMAC example.
2. Change the message but keep the original tag.
3. Verify that the comparison fails.
4. Explain why the key must remain secret.

### Lab 4: Secret Handling Review
Review this intentionally unsafe snippet:

```python
API_KEY = "demo-key-123456"
print("Starting application with key", API_KEY)
```

Identify at least four issues and recommend safer alternatives.

### Lab 5: TLS
For a test HTTPS endpoint you are authorized to inspect:
1. Find the certificate issuer, subject, and validity period.
2. Explain hostname validation.
3. Describe how to investigate an expired or untrusted certificate.
4. Explain why disabling validation is not an acceptable permanent fix.

## Part D: Scenario Analysis

### Scenario 1: Unauthenticated Encryption
An application encrypts a file but cannot detect ciphertext tampering. What risk exists? What kind of cryptographic construction can help? Why use a vetted library?

### Scenario 2: Compromised Signing Key
A build server's private signing key is exposed. List immediate response steps, how to identify affected releases, and long-term improvements.

### Scenario 3: Password Storage
A database stores `SHA256(password)` without a salt. Explain the weaknesses and recommend a password-hashing approach with unique salts and suitable work factors.

## Submission Checklist
- [ ] Mechanisms are matched to the security requirements.
- [ ] File-hashing and randomness labs are complete.
- [ ] Secret-handling problems and mitigations are documented.
- [ ] Key compromise response and password storage are understood.
