# Output Encoding — Practical Examples

These examples illustrate safe rendering patterns. Adapt syntax to your framework and version.

## Example 1: HTML text — render as data

**Risky browser code:**

```javascript
commentBox.innerHTML = userComment;
```

**Safer for plain text:**

```javascript
commentBox.textContent = userComment;
```

The first assignment asks the browser to parse HTML. The second creates text. If the requirement is to display a comment literally, do not sanitize it into HTML; use a text sink.

## Example 2: Template auto-escaping

A template engine with HTML auto-escaping can safely render an ordinary text variable:

```html
<p>{{ comment }}</p>
```

Confirm that:
- Auto-escaping is enabled for the template.
- `comment` has not been marked “safe” or passed through a bypass.
- The output location is ordinary HTML text.
- The rendered value is not later copied into a dangerous JavaScript or CSS context.

Template syntax and default escaping behavior vary by framework.

## Example 3: Quoted text attribute

```html
<input
  type="text"
  name="nickname"
  value="{{ nickname }}"
>
```

Use normal attribute escaping and fixed attribute names. Do not use user input to create attribute names or event-handler attributes. URL attributes need URL validation in addition to correct attribute handling.

## Example 4: URL query parameter

```javascript
const query = "network & application";
const link = "/search?q=" + encodeURIComponent(query);
```

The query value is encoded as a URL component. The resulting URL is still an application URL, and if inserted into an HTML `href`, the framework should safely render the attribute.

**Important:** this is not enough when the user supplies an entire URL. Parse and validate the destination, including its scheme and host, according to the application’s policy.

## Example 5: Validate a user-supplied destination

Illustrative browser-side check for a feature that accepts only HTTPS destinations from a known host:

```javascript
function approvedDestination(input) {
  try {
    const url = new URL(input);
    if (url.protocol !== "https:") return null;
    if (url.hostname !== "docs.example.test") return null;
    return url.href;
  } catch {
    return null;
  }
}
```

Replace `docs.example.test` with an application-controlled allowlist entry. Validation rules should be enforced at the trusted server boundary when they affect security decisions. This example is not a general-purpose URL sanitizer.

## Example 6: Avoid inline JavaScript interpolation

**Avoid:**

```html
<script>
  const displayName = '{{ user_display_name }}';
</script>
```

Correct escaping for this location is complex because both JavaScript and the enclosing HTML parser are involved.

**Prefer:** deliver the value through a JSON endpoint and parse it with `response.json()`, or use a framework-supported data-binding mechanism. Do not pass data to `eval()`.

## Example 7: JSON serialization

**Avoid manual JSON concatenation:**

```python
# Unsafe pattern: do not assemble JSON this way.
body = '{"message": "' + message + '"}'
```

**Use a serializer:**

```python
import json

body = json.dumps({"message": message})
```

Send the response with an appropriate JSON content type, for example `application/json; charset=utf-8`. If a client later renders `message` as HTML, it must still use a safe rendering method.

## Example 8: Allowlisted CSS values

```javascript
const allowed = new Set(["navy", "teal", "gray"]);
if (allowed.has(preference)) {
  panel.style.color = preference;
}
```

The application selects a fixed CSS property and accepts only approved values. Do not accept a whole CSS declaration or arbitrary selector from the user.

## Example 9: Rich text — sanitize only when needed

If users are intentionally allowed to submit limited HTML (for example, formatted descriptions), output encoding would display the tags as text and break the feature. Use a maintained HTML sanitizer with a restrictive policy, such as DOMPurify in a suitable client-side workflow, and keep it updated.

```javascript
const cleanHtml = DOMPurify.sanitize(untrustedHtml);
richTextContainer.innerHTML = cleanHtml;
```

This pattern depends on correctly loading and maintaining DOMPurify and defining an appropriate policy. Do not modify the sanitized output using unsafe string operations afterward. For plain text, use `textContent` instead.

## Example 10: Test cases

| Input type | Expected behavior |
|---|---|
| Plain text such as `Hello` | Displays normally |
| Text containing `<` and `>` | Displays as text in an HTML text context |
| Text containing `&` and quotes | Displays without changing the intended content |
| Search value containing spaces and `&` | Encoded as one query parameter value |
| Unapproved URL scheme | Rejected by URL policy |
| Rich HTML with disallowed elements | Disallowed markup removed by sanitizer |
| JSON string containing quotes | Correctly serialized and parsed |
| DOM value inserted into a text element | Not parsed as HTML |

Use synthetic input and a local test environment. A string appearing encoded in raw HTML does not alone prove the entire application is safe; verify browser behavior and all subsequent sinks.

## Example 11: Code review checklist for a finding

```markdown
### Finding: Untrusted comment rendered as HTML

**Affected component:** Comment preview

**Root cause:** User-controlled text is assigned to `innerHTML`.

**Impact:** Browser may interpret the value as markup or executable content.

**Remediation:** Use `textContent` for plain text. If rich HTML is required,
apply a maintained sanitizer with an explicit policy.

**Verification:** Add a regression test confirming markup-like input is
displayed as text and does not create unexpected DOM elements.
```
