# XSS and CSRF Prevention

This module covers two common web application security risks: Cross-Site Scripting (XSS), where untrusted content is interpreted as executable browser content, and Cross-Site Request Forgery (CSRF), where a browser is tricked into sending an unwanted authenticated request.

## Learning objectives

By completing this module, you should be able to:

- Explain reflected, stored, and DOM-based XSS.
- Choose safe DOM APIs and context-appropriate output encoding.
- Recognize when HTML sanitization is required.
- Describe CSRF and why cookie-based authentication can be exposed to forged requests.
- Use framework CSRF protections and server-validated tokens for state-changing requests.
- Apply `SameSite` cookies and Origin/Referer checks as defense-in-depth.
- Write tests for both allowed and rejected requests.

## Part 1: Cross-Site Scripting (XSS)

### Common types

- **Reflected XSS:** request data is included in a response without appropriate handling.
- **Stored XSS:** untrusted content is stored and later rendered unsafely to users.
- **DOM-based XSS:** client-side code sends untrusted data to a dangerous DOM sink.

### Core defenses

1. Use framework templates with automatic escaping enabled.
2. Encode output for the exact context where it is rendered: HTML text, a quoted attribute, a URL component, JavaScript, or CSS.
3. Prefer safe DOM APIs such as `textContent`, `value`, and `createTextNode` instead of `innerHTML` for plain text.
4. If users must author limited HTML, use a maintained HTML sanitizer with a restrictive policy. Do not sanitize and then modify the result in ways that reintroduce unsafe markup.
5. Validate URL schemes and destinations before using untrusted URLs in `href` or `src`.
6. Avoid dangerous contexts and APIs such as inline event-handler code, `eval()`, and untrusted strings passed to HTML-parsing APIs.
7. Consider Content Security Policy (CSP) and Trusted Types as additional layers, not substitutes for safe rendering.

### Safe DOM example

```javascript
const message = document.querySelector("#message");
message.textContent = userSuppliedText;
```

For plain text, `textContent` treats the value as text instead of parsing it as HTML.

### When HTML is a feature

If a product deliberately allows rich HTML content, output encoding will show the markup as text rather than render it. Use a well-maintained sanitizer such as DOMPurify with an explicit policy, keep it updated, and avoid changing the sanitized output afterward.

## Part 2: Cross-Site Request Forgery (CSRF)

### How CSRF works

Browsers may automatically attach session cookies to requests. A malicious site may cause a logged-in browser to send a request to a trusted application. If the application does not verify that the request was intentionally initiated from a trusted interaction, a state-changing action could occur with the user's privileges.

### Core defenses

1. Use the web framework's built-in CSRF middleware where available.
2. Validate a secret, unpredictable CSRF token on every protected state-changing request when using cookie-based authentication.
3. Keep `GET`, `HEAD`, and `OPTIONS` free of state-changing behavior.
4. Set session cookies with appropriate `Secure`, `HttpOnly`, and `SameSite` attributes.
5. Validate `Origin` and, where appropriate, `Referer` against the exact expected origin as a defense-in-depth measure.
6. Do not place CSRF tokens in URLs or logs.
7. Do not treat CORS as a general CSRF defense; CORS primarily controls whether scripts can read cross-origin responses.
8. Choose protections appropriate to the authentication design. Bearer tokens explicitly attached by client code have a different CSRF threat model, but still require secure token storage and XSS defenses.

### Example request flow

1. Server issues a CSRF token associated with the user's session.
2. Client submits the token in a hidden form field or a custom header on a state-changing request.
3. Server validates the token and the session relationship.
4. Missing or invalid tokens are rejected, and the failure is logged safely.

## XSS vs. CSRF

| Topic | XSS | CSRF |
|---|---|---|
| Main issue | Untrusted content executes in the application's browser origin | Browser sends an unwanted authenticated request |
| Common root cause | Unsafe rendering or DOM manipulation | Missing request-intent validation |
| Main defenses | Context-aware output encoding, safe DOM APIs, sanitization when needed | Framework CSRF protection, server-validated tokens, cookie controls, origin checks |
| Relationship | XSS may undermine CSRF defenses | CSRF does not require injecting script into the target application |

## Combined security checklist

- [ ] Keep framework auto-escaping enabled.
- [ ] Use context-appropriate output encoding.
- [ ] Prefer `textContent` over `innerHTML` for plain text.
- [ ] Sanitize user-authored HTML with a maintained library and restrictive policy.
- [ ] Validate URL schemes and destinations.
- [ ] Avoid unsafe script execution and inline event-handler construction.
- [ ] Deploy CSP as a defense-in-depth control.
- [ ] Use built-in CSRF middleware or server-validated CSRF tokens.
- [ ] Ensure state-changing operations do not use `GET`.
- [ ] Set session cookies with `Secure`, `HttpOnly`, and an appropriate `SameSite` value.
- [ ] Validate Origin/Referer carefully where appropriate.
- [ ] Test missing/invalid CSRF tokens and unsafe rendering paths.
- [ ] Keep security libraries and frameworks patched.

## Safe practice boundaries

Use a local demo application or a system you are explicitly authorized to test. Do not run XSS or CSRF tests against third-party users or production services without permission.

## References

- [OWASP Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
- [MDN: SameSite cookies explained](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#samesitesamesite-value)
