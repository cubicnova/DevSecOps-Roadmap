# Input Validation — Secure Coding

## Overview
Input validation checks whether data conforms to the format, type, size, and business rules expected by an application before it is processed. It is a core secure-coding control, but it does not replace parameterized queries, context-aware output encoding, authorization, or safe file handling.

## Learning objectives
- Distinguish syntactic validation from semantic validation.
- Apply server-side allowlist validation to common data types.
- Validate structured JSON, nested objects, and arrays.
- Handle strings, numbers, dates, URLs, identifiers, and file uploads safely.
- Avoid denylist-only filtering and unsafe “sanitization.”
- Write positive and negative validation tests.
- Recognize when other controls are required to prevent injection and access-control issues.

## Core principles
1. **Validate at trust boundaries.** Treat browser input, API requests, partner feeds, queues, imported files, and other external data as untrusted.
2. **Validate server-side.** Browser checks improve user experience but can be bypassed.
3. **Prefer allowlists.** Define what is valid for each field and reject values outside the accepted contract.
4. **Check syntax and semantics.** `2026-02-31` may resemble a date but is not a valid calendar date; a valid end date may still need to be after the start date.
5. **Bound resource use.** Limit request sizes, string lengths, array counts, nesting depth, and parser work before expensive processing.
6. **Decode consistently.** Decode according to the protocol, validate the representation that will be used, and avoid repeated decoding later.
7. **Fail safely.** Reject invalid requests clearly; do not process partially validated values.
8. **Preserve legitimate data.** Avoid simplistic rules that reject normal punctuation or non-English text.
9. **Keep controls separate.** Validation does not make SQL string concatenation safe, does not encode HTML output, and does not authorize access to a record.
10. **Log carefully.** Record validation failures without exposing secrets or logging untrusted input in a way that permits log injection.

## Syntax vs. semantics
| Type | Syntactic checks | Semantic checks |
|---|---|---|
| Email | Format accepted by the application | Verification link proves mailbox control |
| Quantity | Integer, within allowed range | Quantity available for purchase |
| Date range | Valid date representations | End date is after start date |
| Account ID | Correct type and identifier format | Caller is authorized to access the account |
| Sort field | Matches a known option | Option is allowed for this operation |
| File upload | Size, allowed type and content checks | User is allowed to upload to this resource |

## Recommended workflow
1. Identify each input source and field.
2. Define required/optional, type, length, range, allowed values, and null behavior.
3. Set request and parser limits before parsing large inputs.
4. Parse using maintained libraries.
5. Validate fields and nested structures.
6. Enforce business rules and authorization separately.
7. Use safe APIs at sensitive sinks (for example, parameterized SQL).
8. Return a consistent error response without sensitive details.
9. Add positive, negative, boundary, and regression tests.
10. Monitor validation failures without retaining unnecessary payload data.

## Python examples
```python
import re

def parse_quantity(value: object) -> int:
    # Reject bool, which is a subclass of int in Python.
    if isinstance(value, bool):
        raise ValueError("quantity must be an integer")
    if isinstance(value, int):
        quantity = value
    elif isinstance(value, str) and re.fullmatch(r"[0-9]{1,3}", value):
        quantity = int(value)
    else:
        raise ValueError("quantity must be a whole number")
    if not 1 <= quantity <= 100:
        raise ValueError("quantity must be between 1 and 100")
    return quantity

def validate_username(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("username must be text")
    if not 3 <= len(value) <= 30:
        raise ValueError("username length must be 3-30")
    if not re.fullmatch(r"[A-Za-z0-9_]+", value):
        raise ValueError("username contains unsupported characters")
    return value
```

These examples are intentionally narrow field policies. Do not reuse the username rule for people's names, comments, or other free-form text.

## Common mistakes
- Relying only on HTML form validation.
- Trying to block every “bad” substring with a denylist.
- Removing punctuation from names and comments.
- Treating a valid identifier as proof of authorization.
- Assuming an allowed filename extension proves a file is safe.
- Parsing a huge request before enforcing size limits.
- Using a regex with unbounded or catastrophic backtracking.
- Validating one representation, then decoding or normalizing it differently downstream.
- Treating validation as a replacement for parameterized SQL or output encoding.
- Returning detailed stack traces or logging credentials in error records.

## Suggested learning path
1. Read `examples.md`.
2. Complete the labs in `practical.md`.
3. Try the exercises before reading `solutions.md`.
4. Use `validation-test-matrix.csv` to record test cases.
5. Apply `input-validation-checklist.md` during code review.

## References
- OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- OWASP Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html
- OWASP Developer Guide — Validate All Inputs: https://devguide.owasp.org/en/04-design/02-web-app-checklist/05-validate-inputs/
- CWE-20: Improper Input Validation: https://cwe.mitre.org/data/definitions/20.html
