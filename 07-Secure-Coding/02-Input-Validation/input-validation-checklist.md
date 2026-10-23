# Input Validation Code Review Checklist

## Input inventory and limits
- [ ] All input sources are identified, including API clients, uploads, queues, partner feeds, and imports.
- [ ] Validation is enforced server-side.
- [ ] Request size limits are applied before buffering/parsing where possible.
- [ ] Parser limits include relevant nesting depth, array count, and processing cost.
- [ ] Inputs are decoded consistently before validation; downstream code does not decode them again unexpectedly.

## Field rules
- [ ] Required, optional, missing, empty, and null behavior are explicit.
- [ ] Types, formats, lengths, and ranges are checked.
- [ ] Allowlist validation is used for fixed choices and identifiers where appropriate.
- [ ] Semantic/business rules are enforced in addition to syntax.
- [ ] Nested objects, arrays, and each array item are validated.
- [ ] Unknown fields are handled according to an explicit schema policy.
- [ ] Numeric conversion avoids overflow, coercion surprises, and unbounded input.
- [ ] Regexes match the entire intended value and avoid excessive backtracking.
- [ ] Legitimate Unicode and punctuation are supported where required.
- [ ] Validation errors do not reveal secrets or implementation details.

## Sensitive sinks and separate controls
- [ ] SQL values use parameterized queries or safe ORM APIs.
- [ ] Dynamic SQL identifiers map to trusted allowlisted values.
- [ ] Output is encoded for its destination context.
- [ ] Rich HTML uses a maintained sanitizer and explicit policy.
- [ ] Authorization is checked independently of identifier format.
- [ ] Shell, URL-fetch, XML, deserialization, and file operations use their specific defenses.
- [ ] File upload checks do not rely only on extension or content-type metadata.

## Testing and operations
- [ ] Positive, negative, boundary, missing, null, and wrong-type cases are tested.
- [ ] Oversized and malformed requests are tested.
- [ ] Error responses are consistent and fail closed.
- [ ] Rejected input is not logged verbatim with secrets or unsafe control characters.
- [ ] Regression tests cover previously found issues.
- [ ] Validation policy is documented and updated with API/schema changes.
