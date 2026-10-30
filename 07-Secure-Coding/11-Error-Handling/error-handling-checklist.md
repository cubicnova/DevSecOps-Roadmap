# Error Handling Security Checklist

## Client responses
- [ ] Responses use documented and consistent status codes.
- [ ] Failed operations never return success status without a clear contract reason.
- [ ] Error bodies follow a stable schema with safe codes/messages.
- [ ] Unexpected errors do not reveal stack traces, SQL, internal paths, hostnames, versions, environment variables, or secrets.
- [ ] Field-level validation messages do not echo sensitive input.
- [ ] Account/resource enumeration risks are considered.
- [ ] Error pages are accessible and provide a useful recovery path where appropriate.

## Exception handling
- [ ] Expected exceptions are handled specifically.
- [ ] Unexpected exceptions reach a centralized safe handler.
- [ ] Broad catch blocks do not silently swallow failures.
- [ ] Security checks fail closed when dependencies or checks fail.
- [ ] Debug mode and verbose exception pages are disabled in production.
- [ ] Gateway, proxy, and framework-generated errors are also reviewed.

## Logging and monitoring
- [ ] Errors include a request/correlation ID.
- [ ] Logs capture useful sanitized diagnostic context.
- [ ] Passwords, cookies, session IDs, tokens, and secrets are redacted.
- [ ] Raw sensitive request bodies are not logged.
- [ ] Untrusted log fields are sanitized against log injection.
- [ ] Logs have access controls, retention rules, and monitoring.
- [ ] Duplicate errors are handled without losing important events or flooding logs.

## State and resource safety
- [ ] Transactions roll back on failure.
- [ ] Partial operations have a documented recovery strategy.
- [ ] Retries cannot unintentionally duplicate non-idempotent actions.
- [ ] Temporary files are removed and connections/locks are released.
- [ ] Cleanup errors do not expose details or mask the original failure.
- [ ] Audit events reflect committed state accurately.

## Testing and operations
- [ ] Tests cover validation, authentication, authorization, dependencies, rate limits, and unexpected errors.
- [ ] Error responses are checked for sensitive information.
- [ ] Production configuration is tested, not only development configuration.
- [ ] Alerting distinguishes expected client errors from unusual server-side failures.
- [ ] Error-handling changes have regression tests.
