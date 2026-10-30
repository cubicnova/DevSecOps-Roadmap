# Practical Labs — HTTP and HTTPS

Use your own application, a local development server, or a system you have explicit permission to test. These labs emphasize observation and configuration review, not unauthorized exploitation.

## Lab 1 — Read a URL

Given:

```text
https://api.example.test:8443/v1/users?active=true#results
```

**Tasks**
1. Identify scheme, hostname, port, path, query, and fragment.
2. Explain which components are sent to the server in a normal HTTP request.
3. Explain why secrets should not be placed in query strings.
4. Describe how DNS relates to the hostname.

## Lab 2 — Inspect a basic GET response

```bash
curl -i --max-time 10 https://example.com/
```

**Tasks**
1. Record the status code.
2. Identify at least four response headers.
3. Identify the content type if present.
4. Explain why the response body may not be HTML.
5. Redact sensitive details if you use a private endpoint.

## Lab 3 — Compare HEAD and GET

```bash
curl -I https://example.com/
curl https://example.com/ -o /dev/null -w 'status=%{http_code} bytes=%{size_download}\n'
```

**Tasks**
1. Compare the status and headers.
2. Explain why HEAD usually returns no body.
3. Note any differences and why server behavior can vary.

## Lab 4 — Learn HTTP status codes

Create a table for these codes: `200`, `201`, `204`, `301`, `302`, `304`, `400`, `401`, `403`, `404`, `429`, `500`, `502`, `503`, `504`.

For each, record:
- Class and typical meaning
- A plausible example
- One additional check before concluding root cause

## Lab 5 — Follow redirects

```bash
curl -I --max-redirs 5 https://example.com/
curl -I -L --max-redirs 5 https://example.com/
```

**Tasks**
1. Compare the first response and final response.
2. Record `Location` headers where present.
3. Explain how redirect loops can happen.
4. Describe why reverse-proxy scheme headers and application base URLs can matter.

## Lab 6 — Review TLS certificate details

```bash
openssl s_client -connect example.com:443 -servername example.com
```

**Tasks**
1. Identify the certificate subject/SAN information shown.
2. Record issuer and validity dates if available.
3. Explain why SNI is supplied.
4. Explain why a successful handshake is not a complete validation report.
5. Do not bypass certificate checks to “fix” a warning.

## Lab 7 — Verify HTTPS with curl

```bash
curl -Iv --max-time 10 https://example.com/
```

**Tasks**
1. Find the negotiated TLS version/cipher if shown.
2. Note whether certificate verification succeeds.
3. Explain the risk of using `curl -k`.
4. Explain why TLS protects data in transit but does not prove the site is benign.

## Lab 8 — Inspect cookies in a lab application

Using an application you control, inspect a `Set-Cookie` response header.

**Tasks**
1. Review `Secure`, `HttpOnly`, `SameSite`, `Path`, and `Domain`.
2. Explain the security purpose of each attribute.
3. Identify where the session is created, refreshed, and invalidated.
4. Do not share a real cookie value in the report.

## Lab 9 — Review security headers

Run:

```bash
curl -sSI https://example.com/
```

**Tasks**
1. Look for HSTS, CSP, `X-Content-Type-Options`, and `Referrer-Policy`.
2. Record which are present.
3. Explain why presence alone does not prove correct configuration.
4. Draft a suitable header policy for a simple application you control, noting assumptions.

## Lab 10 — Understand CORS

On a local API you control:

```bash
curl -i \
  -H 'Origin: https://client.example.test' \
  http://127.0.0.1:8000/api/demo
```

**Tasks**
1. Inspect CORS-related response headers.
2. Explain why curl does not enforce CORS.
3. Explain the difference between CORS and authorization.
4. Describe the risk of blindly reflecting arbitrary origins when credentials are allowed.

Do not test this against an application without authorization.

## Lab 11 — Diagnose a 502 or 504

**Scenario:** A web app returns `502 Bad Gateway` or `504 Gateway Timeout`.

**Tasks**
1. Identify whether the response likely comes from the origin app or a proxy/gateway.
2. List checks for upstream health, DNS, port, TLS, timeout settings, and logs.
3. Explain the difference between a 502 and 504 in typical gateway behavior.
4. Write an evidence-based troubleshooting sequence.

## Lab 12 — Browser Network analysis

Using a site or lab application you are allowed to inspect:
1. Open Developer Tools → Network.
2. Reload the page.
3. Select a document or API request.
4. Record method, URL pattern, status, request type, response type, and timing.
5. Identify any redirect or failed dependency.
6. Redact cookies, tokens, personal data, and private URLs before sharing.

## Lab 13 — Compare HTTP versions

**Tasks**
1. Summarize HTTP/1.1, HTTP/2, and HTTP/3.
2. Explain TCP vs QUIC/UDP transport use.
3. Use `curl --version` to inspect installed feature support.
4. If supported and permitted, test `curl --http2` or `curl --http3` against a compatible endpoint.
5. Record why a failed version-specific test may mean the client or server does not support that mode.

## Lab 14 — Write a web troubleshooting report

Use a symptom from your own lab, such as a redirect loop, certificate warning, 403, or slow response.

Include:
- Time and environment
- URL pattern (remove secrets)
- Client/tool and request method
- Status and relevant headers
- TLS/certificate observations
- Browser or curl evidence
- Relevant server/proxy logs if available
- Hypothesis and confidence
- Proposed action and verification plan

## Submission checklist

- [ ] URL components documented.
- [ ] Request and response inspected.
- [ ] Status-code table completed.
- [ ] TLS certificate validation understood.
- [ ] Cookie and security header review completed.
- [ ] CORS behavior explained.
- [ ] HTTP version comparison completed.
- [ ] Troubleshooting report contains redacted evidence.
