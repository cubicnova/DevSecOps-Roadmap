# XSS and CSRF Prevention — Examples

These examples illustrate defensive patterns. Adapt them to your framework and verify the exact APIs against current documentation.

## 1. Safe plain-text rendering in JavaScript

```javascript
const output = document.querySelector("#output");
output.textContent = userSuppliedComment;
```

For plain text, prefer `textContent` instead of assigning untrusted data to `innerHTML`.

## 2. Avoid unsafe HTML interpolation

```javascript
// UNSAFE: parses the string as HTML.
container.innerHTML = userSuppliedComment;

// SAFER for plain text:
container.textContent = userSuppliedComment;
```

If the application intentionally supports rich HTML, use a maintained sanitizer with an explicit policy. Do not treat a home-grown string replacement or a blocklist of suspicious characters as a reliable sanitizer.

## 3. HTML sanitization for rich content

```javascript
// Example with DOMPurify installed and imported according to its documentation.
const cleanHtml = DOMPurify.sanitize(untrustedRichText);
container.innerHTML = cleanHtml;
```

Keep DOMPurify up to date. Avoid modifying `cleanHtml` after sanitization in ways that can introduce active markup or unsafe attributes.

## 4. Validate links before rendering

```javascript
function approvedLink(rawValue) {
  const url = new URL(rawValue, window.location.origin);

  if (url.protocol !== "https:" && url.protocol !== "http:") {
    throw new Error("Unsupported URL scheme");
  }

  return url.href;
}

link.href = approvedLink(userSuppliedUrl);
link.textContent = "Open link";
```

This is a starting point. For links that should only point to your own site, also compare the parsed origin against an explicit allow-list. Do not accept arbitrary destinations if the feature does not need them.

## 5. Template rendering

Use a framework's normal escaped interpolation for plain text. Avoid disabling auto-escaping or using raw-HTML features with untrusted values.

```html
<!-- Template-style pseudocode: normal escaped interpolation -->
<p>{{ comment_text }}</p>
```

Template syntax and defaults vary by framework; confirm that escaping is enabled and understand any “raw”, “safe”, or “dangerously set HTML” escape hatch.

## 6. CSRF token in a server-rendered form

```html
<form method="post" action="/profile/email">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <label>
    New email
    <input type="email" name="email" required>
  </label>
  <button type="submit">Update email</button>
</form>
```

This is template pseudocode. Generate the token securely on the server and validate it on submission. Use your framework's built-in CSRF middleware rather than implementing token lifecycle from scratch when possible.

## 7. CSRF token in a JavaScript request

```javascript
await fetch("/api/profile/email", {
  method: "PATCH",
  credentials: "same-origin",
  headers: {
    "Content-Type": "application/json",
    "X-CSRF-Token": csrfToken
  },
  body: JSON.stringify({ email: newEmail })
});
```

The server must validate the token and the authenticated session. The client sending a header does not itself provide protection.

## 8. Express-style server-side token validation (illustrative pseudocode)

```javascript
app.patch("/api/profile/email", requireAuthenticatedSession, csrfProtection, async (req, res) => {
  await updateEmail(req.user.id, req.body.email);
  res.sendStatus(204);
});
```

`csrfProtection` represents maintained middleware configured for the chosen session and framework. Do not assume this exact identifier is built into Express. Use a documented library or framework feature and test its configuration.

## 9. Cookie attributes

An illustrative session cookie configuration might include:

```http
Set-Cookie: __Host-session=opaque-value; Path=/; Secure; HttpOnly; SameSite=Lax
```

Choose `Strict`, `Lax`, or `None` based on the application's navigation and embedding needs. `SameSite=None` requires `Secure` in modern browsers. Cookie attributes reduce risk but do not replace appropriate CSRF validation in applications that need tokens.

## 10. Origin validation

For protected state-changing requests, compare the parsed `Origin` against the exact expected scheme, host, and port. If `Origin` is absent, a carefully implemented `Referer` fallback may be appropriate. Do not use substring checks such as `origin.includes("example.com")`. Reject unknown origins unless another explicitly designed, validated defense applies.

## 11. Safe HTTP method design

- `GET /profile` — read profile data.
- `PATCH /profile` — change profile data; require authentication and CSRF validation when applicable.
- `POST /transfer` — perform a state change; require authentication, CSRF protection, authorization, and any transaction-specific confirmation.

Do not delete records, change settings, or transfer funds as a side effect of a `GET` request.

## 12. Testing ideas

For XSS, store a harmless string containing HTML-looking characters and verify that the UI displays it as text, not as a new element. For rich HTML, test the sanitizer's documented policy.

For CSRF, verify that a state-changing request with a valid session but a missing or invalid CSRF token is rejected. Also test valid tokens, cross-origin requests, and session rotation. Use a local test environment.
