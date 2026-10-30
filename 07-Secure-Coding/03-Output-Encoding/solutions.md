# Output Encoding — Sample Solutions

These are example answers. Framework behavior and APIs vary, so verify the exact contract for the library and version used by your project.

## Exercise 1: Identify the context

1. **HTML text:** use template auto-escaping or a trusted HTML text encoder; on the DOM, use `textContent`.
2. **Quoted text attribute:** use a framework's attribute escaping, keep the attribute name fixed, and quote the value.
3. **URL query parameter:** encode the value as a URL component, such as with `encodeURIComponent()`.
4. **Full destination URL:** parse and validate scheme and destination against an allowlist, then render the URL with safe attribute handling.
5. **Inline JavaScript:** avoid interpolation; pass data through JSON or framework-supported binding. If unavoidable, use a maintained encoder designed for the exact JavaScript-in-HTML context.
6. **CSS value:** use a fixed property and allowlisted values. Avoid arbitrary CSS input.
7. **Rich HTML:** use a maintained HTML sanitizer with a restrictive policy; output encoding alone would display tags as text.
8. **DOM `innerHTML`:** use `textContent` for plain text, or sanitize intentionally allowed HTML.
9. **JSON:** use a JSON serializer and correct JSON content type; separately protect any later HTML rendering.
10. **Event-handler attribute:** avoid dynamic event-handler code. Register trusted handlers with `addEventListener()` and pass untrusted values as data.

## Exercise 2: Fix a DOM XSS sink

Safer plain-text rendering:

```javascript
const term = location.hash.slice(1);
document.querySelector("#result").textContent = term;
```

Test idea: set the hash to a harmless markup-like string such as `<b>sample</b>` and assert that the result element's text equals the supplied string and no new `<b>` child element exists. Use a browser-based test runner or the application's normal UI test framework.

Other APIs to review include `outerHTML`, `document.write()`, `insertAdjacentHTML()`, `srcdoc`, and unsafe framework HTML rendering APIs.

## Exercise 3: URL encoding versus validation

- **Encoding a query parameter** preserves a value as one URL component; it does not establish whether a complete URL is trustworthy.
- **URL validation** parses a full URL and checks allowed schemes, hosts, ports, and any product-specific path restrictions.

Example documentation-link policy:
- Permit only HTTPS.
- Require an exact hostname or explicit allowlist.
- Reject credentials embedded in URLs and unapproved ports.
- Consider whether redirects to unapproved destinations are possible.
- Validate at the trusted server boundary whenever the destination affects server-side decisions.

Reject schemes such as `javascript:` and any other scheme not required by the feature. Avoid substring checks such as “URL contains the approved domain,” which can be bypassed by deceptive hostnames.

## Exercise 4: Template escaping review

The `safe` filter may disable the template engine's automatic escaping. If `comment` contains untrusted data, the browser can interpret it as markup.

For ordinary text, remove the bypass and use the template's default escaping, or use a safe DOM text API. If the product intentionally supports a limited subset of HTML, sanitize it with a maintained library and a defined policy.

Regression tests should include ordinary text, ampersands, quotes, angle brackets, and markup-like strings. Verify the displayed text is correct and unexpected DOM elements are not created.

## Exercise 5: Context mapping

| Context | Recommended approach | Common mistake | Test |
|---|---|---|---|
| HTML text | Auto-escaping or `textContent` | Assigning to `innerHTML` | Markup-like input remains text |
| Quoted attribute | Attribute-aware template escaping | Dynamic attribute names or event handlers | Value stays inside intended attribute |
| URL query value | URL-component encoding | Concatenating raw value | Reserved characters remain in one parameter |
| Complete URL | Parse and allowlist scheme/host | Treating encoding as validation | Unapproved scheme/host rejected |
| JavaScript data | Avoid inline interpolation; JSON/data binding | Manual quote escaping | Quotes and delimiters cannot change code structure |
| CSS value | Fixed property and allowlist | Accepting arbitrary CSS | Invalid value rejected |
| Rich HTML | Maintained sanitizer and explicit policy | Trusting raw HTML or mutating sanitized output | Disallowed elements/attributes removed |

## Exercise 6: JSON response

Example in Python:

```python
import json
from flask import Response

body = json.dumps({"name": user_name})
return Response(
    body,
    content_type="application/json; charset=utf-8"
)
```

A framework's native JSON response helper is often preferable. JSON serialization protects JSON structure, but if a client later assigns the parsed name to `innerHTML`, that is a new HTML interpretation step and still needs safe handling.

## Exercise 7: Rich-text requirement

Output encoding displays markup as literal text, so it does not preserve intended formatting. A sanitizer can permit only the product's supported tags and attributes.

Example policy:
- Allow simple formatting tags such as paragraphs, emphasis, lists, and list items.
- Allow only explicitly required attributes.
- For links, validate allowed schemes and reject script-like schemes.
- Disallow scripts, event-handler attributes, embedded objects, iframes, and arbitrary style unless a specific reviewed requirement exists.
- Keep the sanitizer current and do not modify its output using unsafe string concatenation afterward.

Positive tests should preserve approved formatting. Negative tests should confirm disallowed tags, event handlers, unsafe URLs, and unapproved attributes are removed or rejected.

## Exercise 8: DevSecOps integration

| Stage | Check |
|---|---|
| Pull request | Review rendering context, unsafe sinks, template escape hatches, and URL policies |
| Static analysis | Search or scan for `innerHTML`, `outerHTML`, `document.write`, `eval`, unsafe HTML APIs, and unsafe template filters |
| Unit/integration tests | Verify special characters, plain-text rendering, and URL allowlist behavior |
| Dependency scanning | Keep framework, encoder, and sanitizer dependencies patched |
| Deployment | Confirm CSP and other headers are configured appropriately as defense in depth |
| Runtime | Monitor relevant client-side errors and security signals without logging sensitive user data |

Assign fixes to the team that owns the rendering component. Security engineering can help define standards and review high-risk contexts.

## Exercise 9: Double encoding and data lifecycle

Double encoding may cause the user to see text such as `&lt;` rather than the intended `<` character. It can also create inconsistent behavior when the same stored value is rendered in different contexts.

Normally store data in its ordinary form and encode when rendering it into a specific context. If existing records were pre-encoded, identify which fields and records were transformed, take a backup, design a carefully tested migration, and avoid blindly decoding arbitrary data. Add tests that verify both intended visible text and safe DOM behavior.

## Exercise 10: Mini project sample

A good submission might document:
1. A comment displayed in an HTML container — replace `innerHTML` with `textContent`.
2. A search link — encode the query parameter and keep the destination path fixed.
3. A user-supplied external URL — parse it and enforce the allowed scheme and hostname policy.

For each change, include a failing test that demonstrates the original behavior, a passing regression test, code-review evidence, and a note about residual risks. Do not assume a successful static scan proves the absence of all XSS.

## Final rubric

A strong solution:
- Chooses controls based on the actual parser context.
- Uses safe APIs and framework protections rather than ad hoc escaping.
- Distinguishes encoding, validation, and sanitization.
- Avoids dangerous contexts and unsafe DOM sinks.
- Tests the browser-visible result and adds regression coverage.
