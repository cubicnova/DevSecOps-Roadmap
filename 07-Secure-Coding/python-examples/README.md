# Python Secure Coding Examples

A hands-on secure-coding module for the [CubicNova DevSecOps Roadmap](https://github.com/cubicnova/DevSecOps-Roadmap/tree/main/07-Secure-Coding/python-examples).

## Learning objectives

- Validate untrusted input with explicit rules.
- Prevent SQL injection with parameterized queries.
- Hash passwords with a password-hashing function.
- Load secrets from the environment instead of source code.
- Reduce path-traversal risk.
- Avoid shell command injection.
- Use safe data formats instead of unsafe deserialization.
- Create files safely and avoid leaking sensitive data in logs.
- Add automated regression tests.

## Requirements

- Python 3.10+
- No third-party packages are needed to run the examples or unit tests.

## Setup

From this directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Run an example:

```bash
python examples/01-input-validation.py
```

Run all tests:

```bash
python -m unittest discover -s tests -v
```

## Examples

| File | Topic |
|---|---|
| `01-input-validation.py` | Allowlist input validation |
| `02-sql-injection.py` | Parameterized SQL |
| `03-password-security.py` | Password hashing and verification |
| `04-secrets-management.py` | Environment-based secrets |
| `05-path-traversal.py` | Restricting file access |
| `06-command-injection.py` | Fixed subprocess arguments |
| `07-unsafe-deserialization.py` | JSON parsing and schema checks |
| `08-secure-file-handling.py` | Unique temporary files |
| `09-secure-logging.py` | Redacting common secret assignments |

## Suggested workflow

1. Read each example and identify the security boundary.
2. Explain what could go wrong without the defensive control.
3. Run the example and inspect its behavior.
4. Add a test for valid input and one or more invalid cases.
5. Run the unit tests and static analysis.
6. Document residual risks and limitations.

## Safety notes

These are educational examples, not a complete production security design. Run intentionally vulnerable comparisons only in an isolated local lab. Do not use real credentials or production data in exercises.

Some controls need additional protections in production:
- Path validation can be vulnerable to symlink and time-of-check/time-of-use races if an attacker can modify the filesystem concurrently.
- Regex-based log redaction is not a complete data-loss prevention strategy. Prefer structured, allowlisted log fields.
- Password-hashing parameters should be benchmarked and reviewed for your environment. For production systems, consider a vetted password-hashing library and an algorithm such as Argon2id.
- A JSON parser still needs input-size limits and strict schema validation.
- Use least-privilege execution and resource limits for subprocesses.

## References

- Python documentation: https://docs.python.org/3/
- OpenSSF Secure Coding Guide for Python: https://best.openssf.org/Secure-Coding-Guide-for-Python/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- Bandit: https://bandit.readthedocs.io/
- Ruff: https://docs.astral.sh/ruff/
