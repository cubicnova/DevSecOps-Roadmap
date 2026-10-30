# Suggested Solutions and Review Notes

Solutions are illustrative. Field rules must match the real product contract and should be documented.

## Lab 1 — Field contract
Example:
- `display_name`: required string, 1–80 characters, preserve supported Unicode, reject control characters if policy requires, encode on output.
- `email`: required string within documented length limit, validate using a maintained library compatible with supported addresses; verify mailbox control when required.
- `age`: optional integer within a product-defined range; reject booleans and decimals if the API contract requires integers.
- `preferred_language`: optional exact value from a maintained allowlist such as `en`, `hi`, or `es`.

## Lab 2 — Numeric input
A robust validator checks the type, explicitly rejects `bool` in Python, applies a maximum string length before integer conversion, parses the value, and enforces `1 <= value <= 100`. Use a consistent API contract rather than silently coercing arbitrary strings or decimals.

## Lab 3 — Identifier
A whole-value match such as `r"[A-Z]{2}-[0-9]{4}"` is suitable for the fictional project-code format. Reject extra characters and excessive length. This pattern is not suitable for people's names, addresses, or free-form comments.

## Lab 4 — Date range
Parse using a maintained date parser or standard library, reject invalid calendar dates, and require `end > start`. If timestamps are used, define timezone and daylight-saving behavior. A syntactically valid date does not establish booking availability or authorization.

## Lab 5 — Nested JSON
Use a schema validator with required fields, explicit types, maximum lengths, array limits, nested item schemas, and an explicit policy for unknown fields. Configure request size and parser limits. Return a generic validation error with safe field-level details; never expose stack traces.

## Lab 6 — SQL handling
Use the database driver's parameterized-query API for values. Map a sort option to one of a fixed set of trusted SQL expressions because identifiers generally cannot be bound like values. Validation helps enforce the expected contract but does not replace parameterization.

## Lab 7 — File uploads
Apply request and file size limits; allow only needed file types; inspect content rather than trusting headers; generate storage names; quarantine or scan as appropriate; store privately; and authorize every download. Reject malformed files and test bypasses in a controlled environment.

## Lab 8 — Primary controls
1. Quantity range: syntactic and semantic input validation.
2. Invoice ownership: server-side authorization.
3. HTML display: context-aware output encoding; use an HTML sanitizer for intentionally allowed rich HTML.
4. Database query: parameterized query; validate field semantics as defense in depth.
5. User-supplied URL: SSRF defenses, destination/egress restrictions, DNS/IP validation strategy, redirect handling, and safe network architecture; ordinary format validation is not sufficient.

## Lab 9 — Test matrix
A strong matrix includes test input, expected status/result, observed result, evidence, and defect reference. Include boundary values (`min-1`, `min`, `max`, `max+1`), missing and null values, wrong types, malformed structures, extra properties, large inputs, and valid Unicode/punctuation cases where supported.

## Self-assessment rubric (20 points)
- Field rules and scope: 0–4
- Syntax and semantic validation: 0–4
- Safe handling at sensitive sinks: 0–4
- Negative and boundary tests: 0–4
- Error handling and documentation: 0–4
