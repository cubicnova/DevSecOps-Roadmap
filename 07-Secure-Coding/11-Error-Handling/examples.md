# Error Handling — Examples

The examples are illustrative. Use your framework's exception and logging facilities, and never expose internal exception details to untrusted clients.

## 1. Unsafe versus safe error response

**Unsafe**
```json
{
  "error": "psycopg2.OperationalError: connection failed to db-prod-03.internal",
  "query": "SELECT * FROM users WHERE email='...'",
  "stack": "Traceback ..."
}
```

**Safer**
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "The request could not be completed.",
    "request_id": "req_7f2a..."
  }
}
```

Store the detailed exception in restricted logs with sensitive values redacted. Give support staff the request ID for investigation.

## 2. Catch expected exceptions specifically

```python
def get_order(order_id):
    try:
        return order_service.fetch(order_id)
    except OrderNotFound:
        return response(status=404, body={"error": {"code": "NOT_FOUND"}})
    except DependencyUnavailable:
        return response(status=503, body={"error": {"code": "SERVICE_UNAVAILABLE"}})
```

The `response` helper and exception classes are illustrative. Unexpected exceptions should reach a centralized handler that records sanitized diagnostics and returns a generic server error.

## 3. Centralized unexpected-error handler

```python
def handle_unexpected_error(exception, request):
    request_id = get_or_create_request_id(request)

    logger.exception(
        "Unhandled request failure",
        extra={"request_id": request_id, "route": safe_route_name(request)}
    )

    return json_response(
        status=500,
        body={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "The request could not be completed.",
                "request_id": request_id
            }
        }
    )
```

Ensure logging configuration and formatters do not serialize the exception into the client response. Avoid logging raw request bodies, cookies, authorization headers, or secret query parameters.

## 4. Validation errors

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "One or more fields are invalid.",
    "fields": {
      "email": "Enter a valid email address."
    },
    "request_id": "req_7f2a..."
  }
}
```

Return field-level details only when they are safe and useful. Do not echo the full submitted payload. Avoid messages that reveal whether a private account or resource exists.

## 5. Resource cleanup

```python
def process_upload(upload):
    temp_file = create_temporary_file()
    try:
        write_upload(temp_file, upload)
        validate_upload(temp_file)
        return process_validated_file(temp_file)
    finally:
        safely_remove_temporary_file(temp_file)
```

Use context managers or framework-managed resource lifetimes where possible. Cleanup should not hide the original failure; report cleanup failures through safe operational logging.

## 6. Transaction integrity

```python
def transfer_funds(source, destination, amount):
    with database.transaction():
        debit(source, amount)
        credit(destination, amount)
        write_audit_event(source, destination, amount)
```

The transaction context is illustrative. Ensure a failure rolls back the entire state change and that retries cannot accidentally duplicate a non-idempotent operation.

## 7. Prevent log injection

Treat user-controlled values as untrusted. Prefer structured logging, sanitize control characters, and do not build log lines by concatenating raw input.

```python
logger.warning(
    "Authentication failure",
    extra={"request_id": request_id, "account_ref": safe_internal_ref}
)
```

Do not include submitted passwords, raw tokens, cookies, or unbounded user input in log fields.

## 8. Production configuration
- Disable debug mode and detailed error pages in production.
- Use generic error pages with a request/correlation ID.
- Keep diagnostics in access-controlled logs and monitoring.
- Verify reverse proxies, gateways, and framework middleware do not replace safe errors with verbose default pages.
