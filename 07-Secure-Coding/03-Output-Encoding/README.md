# 03 — Output Encoding

Output encoding is a core secure-coding defense that helps ensure untrusted data is interpreted as **data**, not as executable markup or code, by the component receiving it. In web applications, the correct encoding depends on the output context: HTML text, HTML attributes, URL components, JavaScript strings, or CSS values.

This module follows the [OWASP Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) and the [OWASP Developer Guide — Encode and Escape Data](https://devguide.owasp.org/en/04-design/02-web-app-checklist/04-encode-escape-data/).

## Learning objectives

By the end of this module, you should be able to:

- Explain the difference between input validation, output encoding, and HTML sanitization.
- Select encoding appropriate to the exact output context.
- Use framework auto-escaping and safe DOM APIs correctly.
- Recognize dangerous contexts where encoding alone is insufficient.
- Avoid DOM-based XSS sinks and unsafe HTML construction.
- Build regression tests and include output-encoding checks in a DevSecOps workflow.

## 1. What is output encoding?

Output encoding transforms characters so the target parser does not treat untrusted content as syntax. For example, when displaying user text inside HTML, the less-than character can be represented as `&lt;`, so it is displayed rather than interpreted as the start of a tag.

The correct defense depends on where the value is placed. HTML encoding is not interchangeable with JavaScript, URL, or CSS encoding.

### Related concepts

| Technique | Purpose | Example use |
|---|---|---|
| Input validation | Reject or constrain values that do not match expected data rules | Ensure a page number is an integer in range |
| Output encoding | Make data safe for a specific parser context | Display a comment as HTML text |
| HTML sanitization | Allow a restricted subset of HTML when rich text is a real requirement | Render user-authored formatted content |
| Parameterized query | Keep values separate from SQL syntax | Database access |
| URL validation | Ensure a destination is an allowed URL or scheme | Links and redirects |

These controls solve different problems. Do not rely on validation alone to prevent XSS.

## 2. Context-specific rules

### HTML text context

Use a trusted template engine's default auto-escaping or a well-maintained HTML encoder when displaying text between ordinary HTML tags.

```html
<p>Comment: {{ comment }}</p>
```

This example is safe only if the template engine uses the expected HTML escaping mode and the value is not passed through an unsafe bypass.

For client-side DOM updates, prefer:

```javascript
messageElement.textContent = untrustedComment;
```

`textContent` creates text rather than parsing the string as HTML. Do not use it to place untrusted data inside executable script or style elements.

### Quoted HTML attribute context

Keep element and attribute names fixed, quote attribute values, and use the framework's correct attribute escaping.

```html
<input type="text" name="displayName" value="{{ display_name }}">
```

This is intended for a normal text attribute with template auto-escaping. It is not a safe way to construct event-handler attributes, `srcdoc`, CSS, or arbitrary URL attributes.

### URL component context

Encode an untrusted value as a **URL component** when placing it in a query parameter or other URL component.

```javascript
const url = "/search?q=" + encodeURIComponent(searchTerm);
```

`encodeURIComponent()` does not validate a complete destination URL. If users can supply a whole URL for `href` or `src`, validate the parsed scheme and destination against the application's policy. Allow only intended schemes—typically `https:` and sometimes `http:`—and reject script or other unwanted schemes.

When a URL containing encoded query values is placed in an HTML attribute, also rely on correct HTML attribute handling.

### JavaScript context

Best practice: **do not interpolate untrusted values into inline JavaScript**. Put data in a JSON response or a safely encoded data attribute, then read it as data.

```javascript
// Safer when the value is already available as a JavaScript string:
const message = serverProvidedMessage;
showMessage(message);
```

If server-side templates must embed data in a script, use a maintained encoder explicitly designed for that JavaScript-in-HTML context. Do not manually escape quotes or assume HTML encoding alone makes inline JavaScript safe. Never pass untrusted data to `eval()` or other code-interpreting APIs.

### CSS context

Avoid placing untrusted input in CSS source, selectors, property names, or entire declaration blocks. Prefer a fixed property and a constrained allowlist:

```javascript
const allowedColors = new Set(["navy", "teal", "gray"]);
if (allowedColors.has(userColor)) {
  element.style.color = userColor;
}
```

Use application-defined values rather than accepting arbitrary CSS. Properties that accept URLs need additional URL controls.

### JSON output

Return JSON with the correct content type, such as `Content-Type: application/json; charset=utf-8`. Serialize data with a JSON serializer; do not build JSON by concatenating strings. If JSON is later inserted into HTML, that new HTML context needs its own safe handling.

## 3. Dangerous contexts

Avoid inserting untrusted values directly into:

- `<script>` bodies or JavaScript event-handler attributes such as `onclick`
- `<style>` blocks, CSS selectors, or arbitrary CSS declarations
- HTML tag names or attribute names
- `innerHTML`, `outerHTML`, `document.write()`, or `srcdoc`
- `eval()` or other APIs that interpret strings as code
- `href`, `src`, or redirect destinations without URL validation

Output encoding is not a universal “sanitize everything” operation. First choose a safe API or a suitable context. If the application needs to display a user's authored HTML, use a maintained HTML sanitizer with a deliberate allowlist and keep it patched.

## 4. DOM-based XSS and safe sinks

**Risky:**

```javascript
resultContainer.innerHTML = location.hash.slice(1);
```

The browser parses the value as HTML.

**Safer for plain text:**

```javascript
resultContainer.textContent = location.hash.slice(1);
```

If rich HTML is a requirement, sanitize it with a maintained sanitizer such as [DOMPurify](https://github.com/cure53/DOMPurify), then avoid modifying the sanitized result in ways that reintroduce unsafe content. Sanitization is not needed merely to display text; text APIs are simpler.

Frameworks help through auto-escaping, but escape hatches such as unsafe HTML rendering or bypass APIs can undo protections. Understand the framework's documented trust boundaries.

## 5. Common mistakes

- Using HTML encoding for data inserted into JavaScript.
- Encoding a complete URL instead of its individual parameter values.
- Treating `encodeURIComponent()` as validation for a whole URL.
- Double-encoding values and showing literal entities to users.
- Pre-encoding data before storing it, then reusing it in different contexts.
- Using a global response filter without knowing the context in which each value is rendered.
- Assuming a WAF, CSP, or cookie flags replace safe rendering.
- Sanitizing HTML, then mutating it with unsafe string operations.
- Assuming a value from a database is always trusted.

**Rule of thumb:** keep stored data in its normal form, then apply the correct output encoding as close as practical to the rendering sink.

## 6. Testing output encoding

Create tests that verify both safety and normal functionality.

1. Place harmless test strings containing characters such as `<`, `>`, `&`, `"`, and `'` into fields.
2. Confirm the application displays the expected text without interpreting it as markup.
3. Test each rendering context separately: HTML body, attribute, URL parameter, and DOM insertion.
4. Confirm URL destinations are validated, not merely encoded.
5. Review dangerous sinks and framework escape hatches.
6. Add regression tests for any confirmed issue.
7. Run static analysis and authorized dynamic testing in a test environment.

Avoid running active payloads against systems without authorization. Use a local training app or a controlled test instance.

## 7. DevSecOps checklist

- [ ] Framework auto-escaping is enabled and not bypassed unnecessarily.
- [ ] Untrusted values are rendered using context-appropriate encoding.
- [ ] Plain text uses safe sinks such as `textContent`.
- [ ] User-supplied URLs are parsed and validated against an allowlist.
- [ ] Rich HTML is sanitized using a maintained library and explicit policy.
- [ ] Dangerous sinks and unsafe framework APIs are searched during code review.
- [ ] Tests cover normal characters and hostile-looking input in each context.
- [ ] JSON uses a serializer and the correct content type.
- [ ] Security headers, including a suitable CSP, are used as defense in depth.
- [ ] Dependency scanning keeps rendering and sanitization libraries current.

## Further reading

- [OWASP Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP Developer Guide — Encode and Escape Data](https://devguide.owasp.org/en/04-design/02-web-app-checklist/04-encode-escape-data/)
- [OWASP DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
- [OWASP HTML Sanitization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML_Sanitization_Cheat_Sheet.html)
- [DOMPurify](https://github.com/cure53/DOMPurify)

## Completion criteria

You can identify the output context, choose an appropriate safe API or encoder, explain why dangerous contexts need special handling, and demonstrate the behavior with regression tests.
