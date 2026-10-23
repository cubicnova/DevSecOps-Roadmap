"""Allowlist-based validation of a username."""
import re

USERNAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]{2,19}$")


def validate_username(username: str) -> str:
    """Accept 3–20 characters, starting with a letter."""
    if not isinstance(username, str):
        raise ValueError("Username must be a string")
    if not USERNAME_PATTERN.fullmatch(username):
        raise ValueError("Invalid username format")
    return username


if __name__ == "__main__":
    for candidate in ("alice_01", "admin", "../etc/passwd", "user name"):
        try:
            print("Accepted:", validate_username(candidate))
        except ValueError:
            print("Rejected:", repr(candidate))
