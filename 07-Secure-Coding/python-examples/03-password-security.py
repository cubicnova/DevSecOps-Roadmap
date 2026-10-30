"""Educational password hashing with PBKDF2-HMAC-SHA256."""
import hashlib
import hmac
import secrets

ITERATIONS = 600_000
SALT_LENGTH = 16


def hash_password(password: str) -> tuple[bytes, bytes]:
    """Return a random salt and derived hash; never store plaintext."""
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")
    salt = secrets.token_bytes(SALT_LENGTH)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS
    )
    return salt, digest


def verify_password(password: str, salt: bytes, expected: bytes) -> bool:
    """Verify a password using a constant-time comparison."""
    if not isinstance(password, str):
        return False
    actual = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS
    )
    return hmac.compare_digest(actual, expected)


if __name__ == "__main__":
    salt, stored_hash = hash_password("Example-Password-123!")
    print("Correct password:", verify_password("Example-Password-123!", salt, stored_hash))
    print("Wrong password:", verify_password("wrong-password", salt, stored_hash))
