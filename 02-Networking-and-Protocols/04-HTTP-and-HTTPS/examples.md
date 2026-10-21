# Examples — HTTP and HTTPS

Use public examples only for basic read-only requests, or use your own lab application. Do not send test credentials or state-changing requests to systems without permission.

## 1. Request response headers

```bash
curl -I https://example.com/
```

`-I` sends a HEAD request. Review the status and headers. Some servers handle HEAD differently from GET, so this is not identical to fetching the page body.

## 2. Show connection details

```bash
curl -v --max-time 10 https://example.com/
```

This can show DNS/address selection, connection details, TLS negotiation, request headers, and response headers. Redact cookies, authorization fields, internal hostnames, and any other sensitive data before sharing logs.

## 3. Make a GET request

```bash
curl --max-time 10 https://example.com/
```

This requests a representation. The response body may be HTML or another content type. Use `-I` if only response headers are needed.

## 4. Save response headers and body separately

```bash
curl -sS -D headers.txt -o body.html https://example.com/
```

- `-D headers.txt`: save response headers.
- `-o body.html`: save the response body.
- `-sS`: reduce progress output but still show errors.

Inspect the files before sharing them.

## 5. Follow redirects

```bash
curl -I -L --max-redirs 5 https://example.com/
```

`-L` follows redirects. Compare the original URL, each `Location` header, and the final response. Avoid following redirects automatically when testing unknown or untrusted URLs.

## 6. Inspect a chosen status code in your lab

For a local test server you control, create endpoints that return known status codes, then request them:

```bash
curl -i http://127.0.0.1:8000/
```

Review the status line, headers, and body. Do not attempt to create or trigger errors on a third-party service.

## 7. Send a JSON request to your own API

```bash
curl -i \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  --data '{"name":"test-user"}' \
  http://127.0.0.1:8000/api/demo
```

This sends a POST request with a harmless example body to a local API. Adjust the endpoint and schema to match your own lab. Do not include real passwords, tokens, or personal data in command history.

## 8. Use a custom request header

```bash
curl -i \
  -H 'Accept: application/json' \
  https://example.com/
```

The server may return a different representation depending on content negotiation. Do not assume every server honors every `Accept` value.

## 9. Test a specific HTTP method against a local lab

```bash
curl -i -X OPTIONS http://127.0.0.1:8000/
```

`OPTIONS` can reveal communication options exposed by a resource. The response is application-specific. Do not use `PUT`, `PATCH`, or `DELETE` against systems without authorization.

## 10. Inspect a TLS handshake and certificate

```bash
openssl s_client -connect example.com:443 -servername example.com
```

`-servername` supplies SNI, helping the server select the right certificate. The output includes certificate and handshake diagnostics. Verify certificate chain and hostname properly; a successful connection alone does not prove validation was correct.

To close the interactive connection, type `Q` or press Ctrl+C.

## 11. Verify certificate trust with curl

```bash
curl -Iv --max-time 10 https://example.com/
```

Review TLS-related output. Do not use `-k` / `--insecure` as a normal fix: it disables certificate verification and can hide a man-in-the-middle risk.

## 12. Compare HTTP and HTTPS behavior

```bash
curl -I --max-time 10 http://example.com/
curl -I --max-time 10 https://example.com/
```

A site may redirect HTTP to HTTPS. Observe the status and `Location` header. Do not assume every hostname supports both schemes.

## 13. Check HTTP status classes

Example interpretations:
- `200`: request succeeded.
- `201`: resource created.
- `204`: request succeeded with no response content.
- `301` / `302`: redirect.
- `304`: cached representation may be reused.
- `400`: request could not be processed as sent.
- `401`: authentication is required or credentials are invalid.
- `403`: access is refused.
- `404`: resource not found, or existence intentionally concealed.
- `429`: too many requests.
- `500`: internal server error.
- `502`: gateway received an invalid upstream response.
- `503`: service unavailable.
- `504`: gateway timed out waiting for upstream.

Interpret status codes with response headers, application behavior, and logs.

## 14. Review a cookie in browser DevTools

In your own lab:
1. Open Developer Tools → Network.
2. Select the response that sets the cookie.
3. Inspect `Set-Cookie`.
4. Check whether `Secure`, `HttpOnly`, and a suitable `SameSite` value are present.
5. Confirm cookie scope and expiration align with the application's design.

Never copy a live session cookie into a public report.

## 15. Inspect CORS in a lab

CORS is a browser-enforced mechanism controlling whether a web page can read a cross-origin response. It is not a replacement for server-side authorization.

For an application you control:

```bash
curl -i \
  -H 'Origin: https://client.example.test' \
  http://127.0.0.1:8000/api/demo
```

Inspect response headers such as `Access-Control-Allow-Origin`. `curl` displays the server response but does not enforce browser CORS rules. Do not assume that a permissive CORS header alone means an API is exploitable; authentication and authorization remain separate.

## 16. Inspect security headers

```bash
curl -sSI https://example.com/
```

Review whether headers such as `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, and `Referrer-Policy` are present and suitable. Header presence alone does not prove a secure configuration; evaluate directives and application requirements.

## 17. Use browser Network tools to diagnose a slow request

1. Open Developer Tools → Network.
2. Reload the page.
3. Sort by duration or inspect the Timing panel.
4. Compare DNS, connection, TLS, waiting/TTFB, and content download where available.
5. Check whether the delay is on one resource, many resources, or a backend request.
6. Correlate timestamps with server and proxy logs.

Timing labels differ by browser and protocol. Avoid drawing conclusions from a single request alone.

## 18. Safe troubleshooting checklist

```text
[ ] Is the hostname correct and resolving?
[ ] Does TCP/QUIC connectivity reach the expected endpoint?
[ ] Does TLS validate the expected hostname and trust chain?
[ ] What status code and response headers are returned?
[ ] Is the request redirected?
[ ] Is the expected authentication/session state present?
[ ] Are CORS errors browser-side while the server still responds?
[ ] Do proxy and application logs match the request time?
[ ] Have tokens, cookies, and personal data been redacted?
```
