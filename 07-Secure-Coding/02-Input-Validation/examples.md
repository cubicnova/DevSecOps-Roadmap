# Input Validation Examples

Examples use Python for readability. Adapt them to your language and framework. Validation policies must match actual business requirements.

## 1. Allowlist for a fixed option
```python
ALLOWED_SORTS = {"created_at", "name", "status"}

def validate_sort(value: object) -> str:
    if not isinstance(value, str) or value not in ALLOWED_SORTS:
        raise ValueError("unsupported sort field")
    return value
```
Use the validated value to select a known query expression. SQL bind parameters generally cannot represent column identifiers; do not concatenate arbitrary client input into SQL syntax.

## 2. Numeric range
```python
def validate_page_size(value: object) -> int:
    if isinstance(value, bool):
        raise ValueError("page_size must be an integer")
    if isinstance(value, int):
        result = value
    elif isinstance(value, str) and value.isascii() and value.isdecimal():
        result = int(value)
    else:
        raise ValueError("page_size must be a whole number")

    if not 1 <= result <= 100:
        raise ValueError("page_size must be between 1 and 100")
    return result
```
Set an upper bound to prevent expensive responses. For production, consider the request framework's parsing behavior and reject excessively long numeric strings before conversion.

## 3. String length and allowed format
```python
import re

def validate_project_code(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("project code must be text")
    if not re.fullmatch(r"[A-Z]{2}-[0-9]{4}", value):
        raise ValueError("invalid project code")
    return value
```
This strict format is appropriate only if project codes really follow `AA-1234`. Do not impose this rule on arbitrary user names.

## 4. Date semantics
```python
from datetime import date

def validate_date_range(start_text: str, end_text: str) -> tuple[date, date]:
    try:
        start = date.fromisoformat(start_text)
        end = date.fromisoformat(end_text)
    except (TypeError, ValueError) as exc:
        raise ValueError("dates must use valid ISO calendar dates") from exc

    if end <= start:
        raise ValueError("end date must be after start date")
    return start, end
```
For real API inputs, validate input types and length before parsing and define the timezone policy if timestamps are accepted.

## 5. Structured JSON schema
Example JSON Schema fragment for a request:
```json
{
  "type": "object",
  "required": ["display_name", "quantity"],
  "additionalProperties": false,
  "properties": {
    "display_name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 80
    },
    "quantity": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100
    },
    "tags": {
      "type": "array",
      "maxItems": 10,
      "items": {
        "type": "string",
        "maxLength": 30
      }
    }
  }
}
```
Use a maintained schema validator. Configure request body size and parser depth limits too. Schema validation does not replace business rules or authorization.

## 6. Safe SQL handling
```python
# Safe pattern: values are passed separately to the database driver.
cursor.execute(
    "SELECT id, display_name FROM users WHERE email = %s",
    (email,)
)
```
Placeholder syntax varies by driver. Never build SQL by concatenating user input. Input validation is an additional layer, not the primary SQL injection defense.

## 7. Validation is not output encoding
A display name can contain legitimate characters such as `<`, `>`, quotes, or apostrophes. Validate it against product requirements, store it safely, and encode it for the output context when rendering HTML. For rich HTML content, use a maintained HTML sanitizer with an explicit policy.

## 8. Safe file upload validation
Do not trust the submitted filename or `Content-Type` header alone. Use layered controls:
- Request and file size limits.
- Allowlisted business file types.
- File-signature/content checks where appropriate.
- Server-generated storage names.
- Storage outside executable web roots or in private object storage.
- Malware scanning or quarantine when appropriate.
- Authorization on every download.
- Safe content disposition and serving headers.

## 9. Error handling
```python
def validate_request(data: object) -> dict:
    if not isinstance(data, dict):
        raise ValueError("request body must be an object")
    allowed = {"display_name", "quantity"}
    unknown = set(data) - allowed
    if unknown:
        raise ValueError("request contains unsupported fields")
    if "display_name" not in data or "quantity" not in data:
        raise ValueError("required fields are missing")
    # Validate each field before business logic.
    return {
        "display_name": validate_display_name(data["display_name"]),
        "quantity": parse_quantity(data["quantity"]),
    }

def validate_display_name(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("display_name must be text")
    if not 1 <= len(value) <= 80:
        raise ValueError("display_name length must be 1-80")
    return value
```
Framework code should translate expected validation errors into a consistent 4xx response without returning stack traces or internal details.

## 10. Boundary test examples
For a quantity field with range 1–100, test `1`, `100`, `0`, `101`, `-1`, `1.5`, `true`, `"10x"`, `null`, a very long string, and a missing field. Test the exact JSON types accepted by the API contract.
