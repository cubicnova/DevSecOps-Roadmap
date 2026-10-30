# Solutions — HTTP and HTTPS

These are model answers and diagnostic approaches. Actual responses vary by server, protocol negotiation, browser, and configuration. Record your own evidence rather than claiming an example result happened on your system.

## Lab 1 — Read a URL

For `https://api.example.test:8443/v1/users?active=true#results`:
- Scheme: `https`
- Hostname: `api.example.test`
- Port: `8443`
- Path: `/v1/users`
- Query: `active=true`
- Fragment: `results`

The fragment is processed by the client and is not included in the ordinary HTTP request target. The hostname is resolved using the client's name-resolution path. Secrets in query strings may be retained in logs, history, analytics, and referrer-related contexts.

## Lab 2 — Inspect a GET response

```bash
curl -i --max-time 10 https://example.com/
```

Record the actual status and headers. Useful headers to recognize include `Content-Type`, `Cache-Control`, `Content-Length`, `Location`, `Set-Cookie`, and security headers. The body could be HTML, JSON, an image, or another representation; inspect `Content-Type` and actual content rather than assuming.

## Lab 3 — Compare HEAD and GET

- HEAD requests headers corresponding to GET without returning response content.
- GET requests a representation and normally returns its body.
- A server, CDN, or application may implement HEAD behavior differently or omit certain headers. Compare results and report the observed behavior.

## Lab 4 — Learn HTTP status codes

| Code | Typical meaning | Example / next check |
|---|---|---|
| 200 | Success | Inspect body and application result |
| 201 | Created | Check resource identifier and returned representation |
| 204 | Success, no content | Confirm client expects an empty body |
| 301 | Permanent redirect | Inspect `Location` and canonical URL |
| 302 | Temporary redirect in common use | Inspect `Location` and redirect behavior |
| 304 | Not modified | Check cache validators and browser cache |
| 400 | Bad request | Inspect syntax, encoding, required fields |
| 401 | Authentication required/invalid | Check authentication scheme and credentials without exposing them |
| 403 | Refused | Check role, policy, and server logs |
| 404 | Not found or intentionally concealed | Check path, routing, and resource permissions |
| 429 | Rate limited | Check rate-limit policy and `Retry-After` |
| 500 | Internal server error | Check application logs and dependency failures |
| 502 | Bad upstream response | Check gateway and upstream service |
| 503 | Temporarily unavailable | Check health, overload, maintenance, and retry policy |
| 504 | Gateway timed out | Check upstream latency and network/timeouts |

These are typical interpretations, not guaranteed root causes.

## Lab 5 — Follow redirects

`curl -I` shows the first response headers; adding `-L` follows redirects up to the configured maximum. A redirect loop can occur when two URLs redirect to each other, or when an application behind a proxy incorrectly determines whether the original request used HTTP or HTTPS.

Check `Location`, proxy configuration, forwarded scheme/host handling, and canonical URL settings. Do not blindly increase redirect limits.

## Lab 6 — Review TLS certificate details

`openssl s_client` can show the presented certificate chain, issuer, dates, negotiated parameters, and verification information. `-servername` supplies Server Name Indication so a virtual host can present the appropriate certificate.

A full check must confirm:
- The certificate is within its validity period.
- The requested hostname matches a Subject Alternative Name.
- The chain is trusted by the client's configured trust store.
- The system clock is correct.
- TLS parameters meet the environment's security policy.

A successful TCP/TLS connection alone does not prove that the application is trustworthy or safe.

## Lab 7 — Verify HTTPS with curl

`curl -Iv` shows verbose connection and TLS diagnostics while issuing a HEAD request. Available details depend on the curl build and TLS backend. `-k` disables certificate verification; this can conceal an impersonation or man-in-the-middle risk. Fix the underlying certificate, hostname, trust-chain, or clock issue instead of making verification failures invisible.

TLS protects data in transit between the TLS endpoints. It does not prevent a malicious website from collecting data that the user voluntarily submits, and it does not secure a compromised endpoint.

## Lab 8 — Inspect cookies in a lab

- `Secure`: browser sends the cookie only over secure connections.
- `HttpOnly`: ordinary JavaScript cannot read the cookie through `document.cookie`.
- `SameSite`: controls cross-site cookie sending behavior and helps mitigate some CSRF scenarios.
- `Path` and `Domain`: limit where the cookie is sent; use the narrowest suitable scope.

Session design also requires server-side authorization, unpredictable session identifiers, appropriate rotation, expiration, invalidation, and protection against session fixation. Cookie attributes do not replace those controls.

## Lab 9 — Review security headers

A good answer records actual headers and then reviews their values:
- **HSTS:** should be deployed only after HTTPS coverage and operational readiness are confirmed; `includeSubDomains` and preload have broader consequences.
- **CSP:** restricts sources and behaviors appropriate to the application; a permissive policy may provide little protection.
- **X-Content-Type-Options:** `nosniff` helps prevent MIME sniffing in supported contexts.
- **Referrer-Policy:** should minimize unnecessary URL leakage while supporting application needs.

Header recommendations depend on application features, subdomains, content sources, and compatibility requirements. Test changes before broad deployment.

## Lab 10 — Understand CORS

CORS is enforced by browsers. `curl` sends a request and displays the response but does not enforce browser access restrictions. CORS determines whether browser JavaScript may read a cross-origin response; it does not replace server-side authentication or authorization.

Blindly reflecting arbitrary origins while permitting credentials can allow untrusted origins to read sensitive responses in some configurations. Use an explicit origin allowlist and appropriate credential policy. Never assume a CORS header alone proves a vulnerability.

## Lab 11 — Diagnose a 502 or 504

Typical approach:
1. Record timestamp, URL pattern, request ID, status, and response headers.
2. Determine whether the response came from a reverse proxy, load balancer, CDN, or origin.
3. Check upstream service health, listener address/port, DNS, and route.
4. Check upstream TLS settings if the proxy uses HTTPS to the application.
5. Compare proxy and application logs at the same time.
6. Review timeout and connection-pool settings alongside measured latency.
7. Verify with a repeat request and monitor for recurrence.

A `502` typically means a gateway received an invalid response from upstream; `504` typically means it did not receive a timely response. Implementations and surrounding infrastructure can affect the exact behavior.

## Lab 12 — Browser Network analysis

Record:
- Method and URL pattern, with sensitive query parameters removed.
- Status and response content type.
- Timing and whether the request was redirected.
- Failed resource dependencies and console messages.
- Whether the failure occurs only in the browser or also with a command-line client.

Do not export or share a HAR file without inspecting it: HAR exports can contain cookies, authorization headers, form data, and personal information.

## Lab 13 — Compare HTTP versions

- **HTTP/1.1:** commonly uses TCP; persistent connections are supported.
- **HTTP/2:** commonly uses TLS over TCP in browsers, with binary framing, multiplexed streams, and header compression.
- **HTTP/3:** uses QUIC over UDP, with secure multiplexed streams.

Check `curl --version` for build features. A version-specific test can fail because the client lacks support, the server or intermediary does not offer that version, UDP is blocked, or the connection environment differs. A failed optional test does not automatically indicate a server defect.

## Lab 14 — Write a web troubleshooting report

A concise evidence-based report should separate facts and hypotheses:

```text
Symptom: [observed behavior]
Time/environment: [actual time, timezone, client]
Request: [redacted URL pattern and method]
Evidence: [status, relevant headers, timing, TLS result]
Logs: [matching proxy/application entries if available]
Hypothesis: [possible cause and confidence]
Next test: [test that distinguishes alternative causes]
Action: [approved change, if any]
Verification: [repeat request and expected result]
Remaining uncertainty: [unknowns and follow-up]
```

Never include live cookies, bearer tokens, passwords, private keys, or unnecessary personal information.

## Key reminders

- HTTP is a request/response application protocol; HTTPS protects it with TLS.
- Status codes and headers need context; neither alone proves root cause.
- A valid TLS certificate authenticates control of a hostname under a trust system, not the moral or business trustworthiness of the site.
- Browser CORS enforcement is not server-side access control.
- Redact secrets before sharing curl output, browser screenshots, logs, or HAR captures.
