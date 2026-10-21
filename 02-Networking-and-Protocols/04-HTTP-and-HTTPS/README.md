# 04 — HTTP and HTTPS

Learn how web clients and servers communicate, how HTTP requests and responses are structured, what common methods and status codes mean, and how HTTPS uses TLS to protect traffic.

## Learning objectives

By the end of this module, you should be able to:

- Explain the HTTP request/response model and statelessness.
- Read a URL and identify scheme, host, port, path, query, and fragment.
- Inspect HTTP methods, headers, status codes, and message bodies.
- Explain the security differences between HTTP and HTTPS.
- Describe TLS certificates, certificate validation, encryption, integrity, and authentication.
- Use `curl`, browser Developer Tools, and optional packet inspection to investigate requests.
- Recognize common HTTP security headers, cookie attributes, and web troubleshooting patterns.

## 1. What is HTTP?

Hypertext Transfer Protocol (HTTP) is an application-layer protocol used to exchange representations of resources between clients and servers. A browser, mobile app, or API client sends a request; a server or intermediary returns a response. HTTP is designed to be stateless: each request can generally be understood independently, although cookies, tokens, and application logic can maintain state across requests.

HTTP is used for websites, APIs, software downloads, and many other network services. The semantics of HTTP are defined separately from the wire formats used by individual versions. See [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).

## 2. HTTP and HTTPS

| Property | HTTP | HTTPS |
|---|---|---|
| Typical URL scheme | `http://` | `https://` |
| Common default port | TCP 80 for HTTP/1.1 and HTTP/2 deployments | TCP 443 for HTTP/1.1/HTTP/2; commonly UDP 443 for HTTP/3 over QUIC |
| Traffic confidentiality | No TLS protection by HTTP itself | TLS protects data in transit |
| Integrity protection | No TLS integrity protection | TLS detects unauthorized modification in transit |
| Server authentication | No certificate authentication inherent to HTTP | Usually validates the server's certificate and hostname |
| Suitable for sensitive traffic | No | Yes, when configured and validated correctly |

HTTPS is HTTP carried over a secure transport. TLS aims to provide confidentiality, integrity, and authentication. HTTPS does not guarantee that a site is trustworthy, that its application is secure, or that data is safe after it reaches the server. A valid certificate does not prove a business is legitimate.

**Important:** HTTP/3 uses QUIC over UDP, while HTTP/1.1 and HTTP/2 are commonly deployed over TCP; HTTP/2 can also be used in contexts beyond the usual browser-to-origin TLS connection. Do not assume all HTTPS traffic uses TCP.

## 3. URL anatomy

Example:

```text
https://shop.example.test:8443/products?id=42#details
```

- `https`: scheme
- `shop.example.test`: hostname
- `8443`: explicit port
- `/products`: path
- `id=42`: query string
- `details`: fragment identifier

The fragment is handled by the client and is not sent as part of the HTTP request target in ordinary HTTP requests. Query strings may contain sensitive information; avoid placing secrets in URLs because they can be logged or exposed in browser history and referrer data.

## 4. HTTP request structure

A readable HTTP/1.1 request resembles:

```http
GET /docs HTTP/1.1
Host: example.com
User-Agent: ExampleClient/1.0
Accept: text/html
Connection: close

```

Common components:
1. Request line: method, request target, HTTP version.
2. Header fields: metadata and request preferences.
3. Blank line: ends the header section.
4. Optional body: data sent with methods such as POST or PUT.

HTTP/2 and HTTP/3 use different binary framing and header representations, so this textual format is illustrative of HTTP/1.1.

## 5. HTTP response structure

Example:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Cache-Control: no-store
Content-Length: 12

Hello world!
```

Common components:
1. Status line in HTTP/1.1: version, status code, reason phrase.
2. Response headers.
3. Blank line.
4. Optional body.

The reason phrase is not the authoritative meaning of the response; the status code and protocol semantics are what matter. HTTP/2 and HTTP/3 do not use the HTTP/1.1 status-line syntax on the wire.

## 6. Common request methods

| Method | Typical purpose | Notes |
|---|---|---|
| GET | Retrieve a representation | Defined as safe; should not request a state-changing action |
| HEAD | Retrieve headers that would correspond to GET | Response has no content body |
| POST | Submit data or ask the resource to process it | Semantics depend on the target resource |
| PUT | Create or replace the state of a target resource | Idempotent by method semantics |
| PATCH | Apply a partial modification | Idempotence depends on the patch operation |
| DELETE | Request removal of a target resource | Defined as idempotent in HTTP semantics, though responses can differ |
| OPTIONS | Discover communication options | Often used for capability checks and CORS preflight |
| TRACE | Diagnostic loop-back method | Commonly disabled due to risk and limited need |
| CONNECT | Establish a tunnel to a target | Used by proxies and related mechanisms |

“Safe” means the client is not requesting a state change; “idempotent” means repeating the same request has the same intended effect as making it once. These terms do not mean a request can never produce side effects such as logging.

Do not test state-changing methods against systems without permission.

## 7. Status code classes

| Range | Meaning | Examples |
|---|---|---|
| 1xx | Informational | `100 Continue`, `101 Switching Protocols` |
| 2xx | Success | `200 OK`, `201 Created`, `204 No Content` |
| 3xx | Redirection or conditional/cache behavior | `301 Moved Permanently`, `302 Found`, `304 Not Modified` |
| 4xx | Client-side request issue or refusal | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `429 Too Many Requests` |
| 5xx | Server or gateway failure | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout` |

Notes:
- `401` generally indicates missing or invalid authentication credentials; `403` indicates refusal despite understanding the request, often because permission is insufficient.
- `404` can also be used to avoid revealing whether a resource exists.
- `429` often indicates rate limiting.
- `502`, `503`, and `504` commonly involve a gateway, upstream service, or availability problem.
- A status code alone does not establish the root cause; examine headers, body, timing, and logs.

## 8. Important HTTP headers

| Header | Common role |
|---|---|
| `Host` | Identifies the target authority in HTTP/1.1 |
| `Accept` | Describes acceptable response media types |
| `Content-Type` | Describes the media type of message content |
| `Content-Length` | Indicates content length in applicable message framing |
| `Authorization` | Carries credentials or authorization data |
| `Cookie` | Sends matching cookies to a server |
| `Set-Cookie` | Instructs a user agent to store a cookie |
| `Cache-Control` | Controls caching behavior |
| `Location` | Identifies a redirect target or related resource location |
| `Origin` | Indicates the origin associated with a request in contexts such as CORS |
| `Referer` | Identifies the referring URL, subject to browser policy |
| `User-Agent` | Describes the client software; not a reliable identity proof |
| `Access-Control-Allow-Origin` | CORS response header controlling browser access to a response |
| `Strict-Transport-Security` | Tells browsers to use HTTPS for a domain for a configured period |
| `Content-Security-Policy` | Restricts resource loading and other browser behaviors |
| `X-Content-Type-Options: nosniff` | Helps prevent MIME type sniffing in supported contexts |
| `Referrer-Policy` | Controls referrer information sent by the browser |

Header behavior depends on the specification and context. Security headers should be designed and tested for the application rather than copied blindly.

## 9. Cookies and sessions

HTTP is stateless by design. Applications often create continuity using cookies or other tokens.

Example:

```http
Set-Cookie: session=REDACTED; Secure; HttpOnly; SameSite=Lax; Path=/
```

- `Secure`: send the cookie over secure connections.
- `HttpOnly`: prevent ordinary client-side JavaScript from reading the cookie.
- `SameSite`: helps control cross-site cookie sending; common values include `Strict`, `Lax`, and `None`.
- `Path` and `Domain`: scope where the cookie is sent.

Never put real session tokens in public examples or screenshots. Session cookies should be unpredictable, rotated when appropriate, protected against theft, and invalidated on logout or expiry according to the application's requirements. `HttpOnly` does not prevent all actions by an attacker who can execute script in a page.

## 10. How HTTPS/TLS works at a high level

1. The client resolves the hostname and establishes network connectivity.
2. The client and server negotiate TLS parameters and exchange handshake messages.
3. The server presents a certificate chain.
4. The client validates the certificate chain, validity, and hostname according to its trust configuration.
5. Key agreement establishes shared traffic keys.
6. HTTP messages are carried inside the protected connection.

Modern TLS uses cryptographic key exchange and symmetric traffic encryption. Exact handshake details differ by TLS version and deployment. Certificate validation failures should not be bypassed casually.

TLS protects data in transit between TLS endpoints. A reverse proxy may terminate TLS, meaning traffic on a separate internal hop needs its own protection if that hop crosses an untrusted network.

## 11. HTTP versions at a glance

| Version | Common transport | Key characteristics |
|---|---|---|
| HTTP/1.1 | TCP | Textual message syntax; persistent connections; request/response exchange |
| HTTP/2 | Usually TLS over TCP in browsers | Binary framing, multiplexed streams, header compression |
| HTTP/3 | QUIC over UDP | Multiplexed streams over QUIC; QUIC provides transport security |

HTTP semantics such as methods and status codes are shared across versions. A browser may negotiate a version automatically. Use browser DevTools or `curl --http2` / `curl --http3` only when the installed curl build and destination support them.

## 12. Practical tools

### Inspect response headers

```bash
curl -I https://example.com
```

### Show request and response details

```bash
curl -v --max-time 10 https://example.com/
```

Be careful: verbose output may expose cookies, authorization headers, internal hostnames, or other sensitive data. Redact before sharing.

### Show response headers and body

```bash
curl -sS -D response-headers.txt -o response-body.html https://example.com/
```

### Inspect certificate information

```bash
openssl s_client -connect example.com:443 -servername example.com
```

This opens a TLS connection and prints diagnostic details; it is not a full certificate validation report by itself. Use the correct hostname and verify trust and hostname matching with suitable tools/options.

### Browser Developer Tools

1. Open Developer Tools.
2. Select **Network**.
3. Reload the page.
4. Select a request.
5. Review method, URL, status, request/response headers, timing, and response preview.
6. Avoid sharing screenshots that expose tokens, cookies, personal data, or internal URLs.

## 13. Common troubleshooting cases

- **Name does not resolve:** inspect DNS settings and resolver results.
- **Connection refused:** destination reached a host or network device that actively rejected the connection; check listener and policy.
- **Connection timeout:** consider filtering, routing, loss, or an unresponsive endpoint.
- **TLS certificate error:** check hostname, validity dates, chain, trust store, system clock, and TLS termination.
- **HTTP 301/302 loop:** inspect `Location`, redirect scheme, proxy headers, and application URL configuration.
- **HTTP 401/403:** inspect authentication, roles, access policy, and server logs.
- **HTTP 429:** check rate limits, retry policy, and `Retry-After` where provided.
- **HTTP 502/504:** inspect reverse proxy, upstream health, network path, and timeout settings.
- **Browser-only failure:** compare DevTools, cookies, cache, CORS, extensions, and server-side logs.

## 14. Security considerations

- Use HTTPS for all website traffic, with modern TLS configuration.
- Validate certificates and hostnames; do not disable verification as a routine workaround.
- Never send secrets over plaintext HTTP.
- Use secure cookie attributes and appropriate session lifecycle controls.
- Validate and authorize all server-side inputs; client-side checks are not sufficient.
- Apply least privilege and safe defaults to methods and endpoints.
- Avoid leaking stack traces, tokens, internal hostnames, or personal information in responses and logs.
- Use CSP, HSTS, and other security headers based on a tested deployment plan.
- Keep web server, framework, and TLS libraries updated.
- Test only applications you own or have permission to assess.

## Knowledge check

1. What is the difference between HTTP and HTTPS?
2. What are the parts of an HTTP/1.1 request?
3. How do `401` and `403` differ?
4. What does `Content-Type` describe?
5. What do TLS encryption, integrity, and authentication provide?
6. Why is a valid certificate not proof that a website is trustworthy?
7. Why can a `502` response be generated by a reverse proxy?
8. What do `Secure`, `HttpOnly`, and `SameSite` do for cookies?
9. How does HTTP/3 differ from HTTP/2 in transport?
10. Why should verbose curl output be treated carefully?

## Further reading

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [RFC 9112 — HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112.html)
- [RFC 9113 — HTTP/2](https://www.rfc-editor.org/rfc/rfc9113.html)
- [RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html)
- [MDN — Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)
- [MDN — HTTP messages](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages)
- [MDN — TLS overview](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Transport_Layer_Security)

## Completion checklist

- [ ] I can read HTTP request and response structures.
- [ ] I understand common methods, headers, and status codes.
- [ ] I can explain what HTTPS and TLS protect.
- [ ] I can inspect a request using curl and browser DevTools.
- [ ] I can troubleshoot common HTTP and TLS failures.
- [ ] I understand cookie security attributes and basic web security headers.
