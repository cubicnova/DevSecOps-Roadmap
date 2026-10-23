# Error Handling — Suggested Solutions

Use these notes to compare your lab observations. Framework behavior and API contracts may differ, but the security goals should remain consistent.

## Lab 1 — Response inventory
Define a consistent error schema and map common failures to documented status codes. Use client-error status codes for invalid requests and server-error status codes for unexpected failures. Do not return `200 OK` when the operation failed. Avoid revealing sensitive distinctions where account or resource enumeration is a concern.

## Lab 2 — Information disclosure
Production responses should not include stack traces, SQL queries, hostnames, filesystem paths, environment variables, framework debug output, or secrets. Disable debug mode in production and review gateway-generated error pages as well as application handlers.

## Lab 3 — Exception handling
Handle expected exceptions close to the operation with safe, stable responses. Use centralized handling for unexpected exceptions. Log sanitized diagnostics with a request ID, return a generic server error, and do not silently convert failures into success. Avoid duplicate noisy logs for the same exception where possible.

## Lab 4 — Transaction integrity
Use database transactions for related state changes. If an operation cannot be atomic, design an explicit recovery or compensating-action strategy. Use idempotency controls for retryable non-idempotent operations and ensure audit records reflect committed state.

## Lab 5 — Resource cleanup
Prefer language/framework constructs that guarantee cleanup, such as context managers, `finally` blocks, or scoped resource APIs. Clean up temporary files, close streams and connections, release locks, and ensure cleanup failures do not disclose sensitive details or hide the original exception.

## Lab 6 — Access-control errors
Authentication and authorization checks must fail closed. Follow the documented `401`/`403` behavior consistently. A `404` may be appropriate when intentionally avoiding resource-existence disclosure, but use it consistently and never as a substitute for authorization. Ensure errors cannot reveal private data.

## Lab 7 — Logging
Use structured logging and sanitize untrusted fields. Redact passwords, authorization headers, cookies, access tokens, reset tokens, and sensitive payloads. Use a request/correlation ID and access controls. Validate that control characters cannot forge additional log entries or corrupt log structure.

## Sample finding
**Title:** Production API returns stack traces on unexpected errors  
**Severity:** Risk-dependent; consider whether internal details or secrets are exposed and whether the information helps further attacks.  
**Impact:** Attackers may learn framework details, internal paths, database technology, or infrastructure names.  
**Root cause:** Debug exception middleware is enabled or the global handler serializes raw exceptions.  
**Remediation:** Disable production debug output, centralize exception handling, return a stable generic error with a request ID, and retain sanitized diagnostics in restricted logs.  
**Regression test:** Trigger a controlled server exception and assert the response contains no stack trace, internal path, SQL text, or secret.

## Reporting quality
Use redacted evidence, identify the exact route and environment, separate facts from assumptions, and include a regression test that proves the fix.
