# 11 — Error Handling

Secure error handling helps an application fail safely without exposing secrets, internal implementation details, or inconsistent behavior that attackers can exploit. Good errors also help legitimate users recover and help developers diagnose problems through controlled, sanitized logs.

## Learning objectives
- Distinguish expected validation errors from unexpected application failures.
- Design consistent, safe error responses for web apps and APIs.
- Avoid leaking stack traces, SQL details, secrets, filesystem paths, and internal infrastructure.
- Log enough diagnostic context without logging credentials or sensitive payloads.
- Handle exceptions safely, clean up resources, and preserve transaction integrity.
- Test error paths, status codes, and failure behavior.

## Secure error-handling principles
- Return generic, actionable messages to users; retain detailed diagnostics only in access-controlled server logs.
- Never return stack traces, raw exception messages, SQL queries, environment variables, API keys, session IDs, or internal paths to untrusted clients.
- Use appropriate HTTP status codes and a stable response format for APIs.
- Validate input at trust boundaries and return predictable client errors for invalid input.
- Catch specific exceptions where possible. Avoid broad exception handlers that silently swallow failures.
- Do not continue with partially completed security-sensitive operations after an unexpected failure.
- Use database transactions and rollback behavior for multi-step changes.
- Ensure cleanup of files, connections, locks, and temporary resources on both success and failure.
- Avoid leaking account existence or other sensitive state through error messages or materially different responses.
- Keep error pages accessible and useful without disclosing implementation details.
- Log a correlation/request ID so support teams can find the corresponding server-side event.
- Sanitize log fields to prevent log injection and redact secrets before logging.
- Do not expose detailed exception information in production debug pages.
- Fail closed for authorization and security checks: if a required check cannot be completed, do not grant access.

## Common HTTP response guidance
| Status | Typical use |
|---|---|
| `400 Bad Request` | Malformed request or invalid syntax |
| `401 Unauthorized` | Missing or invalid authentication credentials |
| `403 Forbidden` | Authenticated caller lacks permission |
| `404 Not Found` | Resource absent; sometimes used to avoid disclosing resource existence |
| `409 Conflict` | Request conflicts with current resource state |
| `413 Content Too Large` | Request body exceeds configured limit |
| `415 Unsupported Media Type` | Unsupported request content type |
| `422 Unprocessable Content` | Syntactically valid request fails semantic validation, where used by the API |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Unexpected server-side failure |
| `503 Service Unavailable` | Temporary service unavailability |

Choose status codes consistently for your API contract. Avoid returning `200 OK` for failed operations.

## Example safe API error
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "One or more fields are invalid.",
    "request_id": "req_7f2a..."
  }
}
```

Do not include raw exception text, SQL statements, filesystem paths, stack traces, or secrets in the response.

## Suggested learning sequence
1. Read this overview and `examples.md`.
2. Review current application error pages and API responses.
3. Complete the authorized exercises in `practical.md`.
4. Compare findings with `solutions.md`.
5. Use `error-handling-checklist.md` during code review.
6. Record test results in `error-handling-test-matrix.csv`.

## References
- OWASP Error Handling Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- RFC 9457 — Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457.html
- MDN — HTTP response status codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
