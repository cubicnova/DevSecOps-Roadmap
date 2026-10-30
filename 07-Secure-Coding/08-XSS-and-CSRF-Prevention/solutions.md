# XSS and CSRF Prevention — Suggested Solutions

These are reference answers. Use the security middleware and APIs documented for your framework and keep dependencies patched.

## Solution 1: Classify XSS

1. Search text rendered by the server without correct encoding is typically reflected XSS.
2. A stored comment rendered unsafely is stored XSS.
3. Reading `location.hash` and assigning it to `innerHTML` is a DOM-based XSS pattern.

For all three, trace the untrusted source to the rendering sink. Use normal escaped template interpolation or safe DOM APIs for plain text; sanitize with a maintained library only when HTML is an intended feature. Add tests that assert untrusted text is not parsed into active elements or attributes.

## Solution 2: Safe DOM rendering

```javascript
results.textContent = `Welcome ${displayName}`;
```

This displays the value as text. Validation can enforce product rules such as length or allowed characters, but it does not replace safe rendering because valid-looking strings can still contain markup-significant characters.

## Solution 3: Rich text

Use a maintained HTML sanitizer such as DOMPurify with a narrow allow-list for the tags and attributes the product supports. Test links, attributes, malformed markup, and disallowed active content. Keep the library updated and avoid modifying the sanitized result in ways that reintroduce unsafe markup. Encoding alone would display the markup literally instead of rendering the intended formatting.

## Solution 4: Output contexts

- HTML text: use framework auto-escaping or an HTML text encoder.
- Quoted ordinary attribute: keep the attribute name fixed, quote the value, and use context-appropriate attribute encoding.
- URL query parameter: percent-encode the individual parameter value.
- Complete link destination: parse and validate the URL, allow-list schemes and possibly origins, then render it safely in the HTML attribute context.
- Inline JavaScript: avoid inserting untrusted values into executable script contexts; prefer external scripts and data serialization designed for the exact context.
- Rich HTML: sanitize using a maintained sanitizer and restrictive policy.

Generic escaping is not universal. Avoid untrusted event-handler attributes, executable script construction, `eval()`, and arbitrary CSS/HTML contexts.

## Solution 5: CSRF risk

A state-changing GET can be triggered by navigation, embedded content, or other browser actions, and a browser may automatically attach the session cookie. Use a state-changing method such as `POST` or `PATCH`, require authentication and authorization, and validate a CSRF token when using cookie-based authentication. Consider exact Origin/Referer validation and cookie attributes as additional layers. Keep GET safe and free of side effects.

## Solution 6: CSRF test matrix

| Case | Expected outcome |
|---|---|
| Valid session and valid token | Accept if all other checks pass |
| Missing token | Reject |
| Incorrect token | Reject |
| Expired session | Reject authentication |
| Cross-origin request with missing token | Reject |
| Token from another session | Reject |

Log a structured denial event with a request/correlation ID and a reason category. Do not log the CSRF token, session cookie, or other secrets.

## Solution 7: Cookie controls

- `Secure`: send the cookie only over secure HTTPS connections.
- `HttpOnly`: prevent ordinary JavaScript from reading the cookie; this does not stop the browser from sending it or fix XSS.
- `SameSite`: limit when the browser attaches cookies to cross-site requests.

For a typical first-party application, `Lax` is a common baseline; `Strict` may be appropriate where cross-site navigation is not needed. Cross-site embedding or federated flows may need different settings. Choose deliberately and keep server-side CSRF protection where the threat model requires it.

## Solution 8: Origin validation

Substring checks can accept attacker-controlled hosts such as `example.com.attacker.invalid`. Parse the header as a URL/origin and compare the normalized scheme, hostname, and port against an exact allow-list. If `Origin` is missing, use a carefully implemented `Referer` fallback or another configured CSRF defense; do not treat a missing or `null` origin as automatically trusted.

## Solution 9: CSP

CSP can restrict which scripts and other resources the browser may load or execute, reducing the impact of some injection bugs. It is defense in depth: it may be misconfigured, and it does not make unsafe HTML sinks or incorrect output encoding safe. Fix the underlying rendering issue first.

## Solution 10: Framework review

- Confirm template auto-escaping is enabled; test a string containing markup-significant characters.
- Review raw HTML features; ensure they only receive sanitized HTML when required.
- Confirm CSRF middleware protects every state-changing route; test missing and invalid tokens.
- Review cookie flags and scope; verify the actual `Set-Cookie` header.
- Search for state-changing GET handlers; convert them to appropriate methods and add regression tests.
- Inventory and patch security dependencies; run automated checks and review release advisories.

## Solution 11: Threat model

Possible data sources include profile names, comments, and URL fragments. Potential sinks include `innerHTML`, unsafe template raw rendering, and an unvalidated link destination. State-changing operations may include changing email, updating account settings, and deleting a profile.

Controls include safe DOM APIs, contextual encoding, sanitization for intentional HTML, URL allow-lists, CSRF middleware/tokens, secure cookie settings, and Origin validation. Negative tests should cover unsafe text rendering, disallowed HTML, invalid URL schemes, missing/invalid CSRF tokens, and cross-origin attempts.

## Solution 12: Mini-project checklist

A complete implementation should:
- Render ordinary user content as text.
- Sanitize rich HTML using a maintained library and explicit policy.
- Validate URLs before assigning `href` or `src`.
- Enable the framework's CSRF protection or validate tokens on the server.
- Protect state-changing operations and keep GET safe.
- Configure session cookies deliberately.
- Include tests for both successful requests and rejected cases.
- Keep secrets and tokens out of logs.

## Further reading

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
