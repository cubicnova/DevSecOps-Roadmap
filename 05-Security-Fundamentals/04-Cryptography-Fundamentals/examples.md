# Cryptography Fundamentals - Examples

Use sample data and demo keys only. Never paste production secrets into learning scripts.

## 1. Hash a File with SHA-256

```python
from pathlib import Path
import hashlib

data = Path("sample.txt").read_bytes()
print(hashlib.sha256(data).hexdigest())
```

Change the file and run the script again; the digest should change with overwhelming probability. A hash alone does not prove who created the file. The expected digest must come from a trusted source.

## 2. Generate a Random Token

```python
import secrets

token = secrets.token_urlsafe(32)
print(token)
```

Use a cryptographically secure API for security-sensitive tokens. Do not log or commit real tokens; set suitable scope, lifetime, storage, and revocation behavior.

## 3. Calculate and Verify an HMAC

```python
import hashlib
import hmac

key = b"demo-only-secret"
message = b"deployment=staging"

tag = hmac.new(key, message, hashlib.sha256).digest()
received_tag = tag  # Demonstration only

print(hmac.compare_digest(tag, received_tag))
```

A changed message should fail verification when checked against the original tag. The shared key must remain secret. The hardcoded key here is for demonstration only.

## 4. Base64 Is Encoding, Not Encryption

```python
import base64

message = b"not-secret"
encoded = base64.b64encode(message)
print(encoded.decode())
print(base64.b64decode(encoded).decode())
```

No secret key is required to decode Base64. Do not use it to protect confidential data.

## 5. Digital Signature Workflow

1. A controlled build process creates a release artifact.
2. A protected private signing key signs the artifact or its defined digest.
3. The artifact and signature are distributed.
4. The consumer verifies the signature using a trusted public key.
5. If verification fails, do not treat the artifact as trusted.

The signature's value depends on the trust in the public key and the protection of the private key.

## 6. TLS Certificate Validation

Clients should validate certificate chains and hostnames using a trusted TLS implementation. If validation fails, investigate the certificate chain, hostname, expiration, system clock, and server configuration. Do not disable validation to bypass the error.

## 7. Key Lifecycle

Generate keys securely, store them in a protected key-management system, limit access, monitor use, rotate or revoke them when necessary, and securely retire old material according to policy.
