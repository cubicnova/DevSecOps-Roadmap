# Error Handling — Practical Labs

Run the exercises in a local development environment or on systems you are authorized to test. Use synthetic data and redact secrets from all evidence.

## Lab 1 — Inventory error responses
1. Select a set of application and API routes.
2. Test valid requests and controlled invalid inputs.
3. Record status code, response shape, error code, and request ID.
4. Identify inconsistent formats or failed operations that return `200 OK`.

**Deliverable:** error-response inventory.

## Lab 2 — Check information disclosure
1. Trigger a controlled validation failure and a simulated server-side exception.
2. Inspect responses for stack traces, database details, internal hostnames, filesystem paths, framework versions, environment values, or secrets.
3. Confirm production mode does not expose debug pages.
4. Check gateway/proxy error pages as well as application responses.

**Deliverable:** sanitized evidence and remediation list.

## Lab 3 — Validate centralized exception handling
1. Identify where expected and unexpected exceptions are handled.
2. Confirm expected errors map to stable client responses.
3. Confirm unexpected exceptions are logged once with a request ID and return a generic response.
4. Check that the handler does not swallow exceptions and report success.
5. Verify sensitive request headers and bodies are excluded from logs.

**Deliverable:** exception-handling flow diagram.

## Lab 4 — Check transaction and state integrity
1. Use test data to trigger a controlled failure midway through a multi-step operation.
2. Confirm database changes roll back or the operation reaches a documented safe state.
3. Retry the request where appropriate and check for duplicate effects.
4. Confirm audit events accurately represent committed actions.

**Deliverable:** transaction-failure test results.

## Lab 5 — Verify resource cleanup
1. Exercise upload, file processing, connection, and temporary-file error paths.
2. Cause a controlled failure in a local environment.
3. Check that files, locks, and connections are released.
4. Confirm cleanup errors do not leak details or suppress the original error.

**Deliverable:** cleanup checklist.

## Lab 6 — Test authentication and authorization errors
1. Request a protected route without credentials.
2. Request it with invalid credentials and with a valid account lacking permission.
3. Confirm responses follow the documented `401`/`403` policy.
4. Check whether error differences expose sensitive account or resource existence.
5. Verify failed authorization never falls through to an allow path.

**Deliverable:** access-control error test matrix.

## Lab 7 — Logging and log injection review
1. Inspect sanitized logs for validation, authentication, and server errors.
2. Confirm logs contain useful event type, timestamp, request ID, and safe context.
3. Verify passwords, tokens, cookies, and sensitive payloads are not recorded.
4. Submit controlled newline/control-character input in a local lab and verify log structure remains intact.

**Deliverable:** logging review and redaction rules.

## Lab 8 — Write a security finding
For a confirmed issue, document title, severity rationale, affected route, preconditions, steps, redacted evidence, impact, root cause, remediation, and regression test.

## Completion criteria
- Client errors are consistent and do not reveal internals.
- Unexpected failures return generic responses with a correlation ID.
- Diagnostics are logged safely and access-controlled.
- Transactions and cleanup behave correctly under failure.
- Authorization checks fail closed.
- Tests cover validation, authentication, dependencies, rate limits, and server errors.
