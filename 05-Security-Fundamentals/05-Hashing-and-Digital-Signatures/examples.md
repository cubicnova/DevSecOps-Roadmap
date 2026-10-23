# Examples: Hashing and Digital Signatures

These examples are for learning and defensive validation. Run them locally with sample data.

## 1. Compute a SHA-256 digest

```python
import hashlib

message = b"DevSecOps learning"
digest = hashlib.sha256(message).hexdigest()
print(digest)
```

Changing even one byte should produce a very different digest. A digest is not encryption and cannot be used to recover the original message.

## 2. Compare digests safely

```python
import hashlib
import hmac

expected = hashlib.sha256(b"approved sample").hexdigest()
candidate = hashlib.sha256(b"approved sample").hexdigest()

print("Match:", hmac.compare_digest(expected, candidate))
```

For security-sensitive comparisons of authentication tags or digests, prefer `hmac.compare_digest` to a normal equality comparison.

## 3. Hash a file in chunks

```python
from pathlib import Path
import hashlib

def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

print(sha256_file("sample.bin"))
```

Use binary mode so bytes are hashed exactly as stored. A checksum only helps detect tampering if the expected digest comes from a trusted source.

## 4. Verify a file against a trusted digest

```python
import hashlib
import hmac
from pathlib import Path

def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

trusted_digest = "REPLACE_WITH_TRUSTED_SHA256"
actual_digest = sha256_file("downloaded-file.zip")

if hmac.compare_digest(actual_digest.lower(), trusted_digest.lower()):
    print("Digest matches")
else:
    print("Digest mismatch: do not trust the file")
```

Do not copy the expected digest from the same untrusted location as the file if an attacker could replace both.

## 5. HMAC-SHA-256

```python
import hashlib
import hmac

secret = b"demo-key-do-not-use-in-production"
message = b"amount=100&currency=INR"

tag = hmac.new(secret, message, hashlib.sha256).hexdigest()
received_tag = tag  # Simulates a tag received with the message

valid = hmac.compare_digest(tag, received_tag)
print("Valid HMAC:", valid)
```

Both parties must protect the shared secret. Do not hard-code production keys in source code. HMAC is not a digital signature: both parties can generate valid tags because they share the same secret.

## 6. Password hashing demonstration with PBKDF2

```python
import hashlib
import hmac
import os

password = "sample-passphrase".encode("utf-8")
salt = os.urandom(16)
iterations = 600_000  # Example starting point; benchmark and follow current guidance.

derived = hashlib.pbkdf2_hmac("sha256", password, salt, iterations)
print("salt (hex):", salt.hex())
print("derived key (hex):", derived.hex())

candidate = "sample-passphrase".encode("utf-8")
check = hashlib.pbkdf2_hmac("sha256", candidate, salt, iterations)
print("Password matches:", hmac.compare_digest(derived, check))
```

This illustrates PBKDF2, not a complete account system. For new applications, consider Argon2id where available and use a vetted password-hashing library/framework. Store the algorithm and parameters with the encoded hash so they can be upgraded.

## 7. Create and verify an Ed25519 signature

Install dependency:

```bash
python -m pip install cryptography
```

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.exceptions import InvalidSignature

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

message = b"Release version 1.2.3"
signature = private_key.sign(message)

try:
    public_key.verify(signature, message)
    print("Signature valid")
except InvalidSignature:
    print("Signature invalid")
```

This generates an ephemeral key pair in memory for demonstration. It does not persist the key or establish a real-world identity.

## 8. Demonstrate tamper detection

Add this after the signature example:

```python
tampered = b"Release version 1.2.4"

try:
    public_key.verify(signature, tampered)
    print("Signature valid")
except InvalidSignature:
    print("Tampering detected: verification failed")
```

## 9. Command-line file hashing

Linux:

```bash
sha256sum sample.bin
sha512sum sample.bin
```

macOS:

```bash
shasum -a 256 sample.bin
```

Windows PowerShell:

```powershell
Get-FileHash .\sample.bin -Algorithm SHA256
```

Compare the result with a trusted checksum obtained independently.

## Common mistakes

- Using MD5 or SHA-1 for security-sensitive integrity guarantees.
- Treating a plain hash as proof of authorship.
- Using SHA-256 directly to store user passwords.
- Reusing a password salt across users.
- Comparing HMAC tags with ad-hoc string logic instead of a constant-time comparison helper.
- Accepting a signature without checking the public key's trust and identity.
- Signing one representation of data and verifying a different representation.
- Storing private signing keys in source control or logs.
