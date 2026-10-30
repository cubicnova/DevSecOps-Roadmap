# Practical Labs: Input Validation

Use a local toy application or code you are authorized to test. These labs focus on defensive implementation and testing.

## Lab 1 — Define a field contract
Build a table for a profile form with `display_name`, `email`, `age`, and `preferred_language`.

For each field define:
- Required or optional
- Accepted type and format
- Minimum/maximum length or range
- Null/empty behavior
- Business rules
- Error response
- Positive and negative test cases

## Lab 2 — Validate numeric input
Implement a `page_size` validator with a range of 1–100.

Test:
- Valid: `1`, `25`, `100`
- Invalid: `0`, `101`, `-1`, `1.5`, `true`, `"10abc"`, `null`, missing value
- Resource limit: an extremely long digit string

Document whether the API accepts JSON numbers, numeric strings, or only one representation.

## Lab 3 — Validate identifiers with an allowlist
Create a validator for a project code such as `AB-1234`.

Tasks:
- Accept the defined format only.
- Test lower-case values, spaces, suffixes, line breaks, and overlong strings.
- Explain why this rule is suitable for project codes but not general names or comments.

## Lab 4 — Validate a date range
Create a booking validator that requires valid ISO dates and an end date later than the start date.

Test invalid calendar dates, missing fields, wrong types, same-day range, end-before-start, and leap-year dates. Document any timezone requirements if the application accepts timestamps.

## Lab 5 — Validate nested JSON
Create a request schema with required `display_name` and `quantity`, optional `tags`, and no unknown top-level fields.

Test:
- Missing required fields
- Unknown properties
- Wrong field types
- Nested invalid values
- Oversized arrays and strings
- Malformed JSON and oversized request bodies

Configure parser and request limits before expensive parsing where your framework permits it.

## Lab 6 — Review SQL query handling
Review a toy search endpoint.

Tasks:
- Identify any string concatenation used to build SQL.
- Replace it with a parameterized query.
- If sort columns are selectable, map the user option to a fixed allowlist.
- Add tests for normal values and unexpected input.
- Explain why validation alone is not a SQL injection defense.

## Lab 7 — File upload review
Design validation for a profile-image upload.

Tasks:
- Define allowed size and image formats.
- Explain why filename and content-type metadata can be forged.
- Propose content checks, generated names, private storage, and safe serving.
- Include authorization and download checks.
- Create test cases for oversized, malformed, and mismatched files.

## Lab 8 — Validation vs. authorization vs. output encoding
For each example, identify the primary control:
1. `quantity` must be an integer from 1–100.
2. A customer must not access another customer's invoice.
3. A display name is inserted into an HTML page.
4. An email value is used in a database query.
5. A URL-fetching feature accepts a user-supplied destination.

Explain the additional protections needed for each case.

## Lab 9 — Test matrix and code review
Use `validation-test-matrix.csv` to document at least 15 test cases for one API endpoint.

Include valid, invalid, boundary, missing, null, wrong-type, unexpected-field, and oversized-input cases. Record expected behavior and actual result.

## Submission checklist
- [ ] Server-side validation covers all untrusted inputs.
- [ ] Syntax and semantic rules are separate and explicit.
- [ ] All relevant boundaries and parser limits are considered.
- [ ] Safe APIs are used for database and other interpreter sinks.
- [ ] Authorization and output encoding are handled independently.
- [ ] Positive, negative, boundary, and regression tests exist.
- [ ] Error responses are safe and consistent.
