# Output Encoding — Exercises

Use a local test application or an environment you are authorized to assess.

## Exercise 1: Identify the context

For each location, identify the parser context and recommend a safe approach.

1. A comment is displayed between `<p>` tags.
2. A profile name is placed in an `<input value="...">`.
3. A search term is appended to a URL query parameter.
4. A user-provided URL is assigned to an anchor's `href`.
5. A display name is inserted into an inline `<script>`.
6. A preference is used to change a panel's color.
7. A rich-text editor allows limited HTML.
8. A value from `location.hash` is assigned to `innerHTML`.
9. A server returns a JSON object containing a quote character.
10. A user value is inserted into an HTML event-handler attribute.

For each, explain why one generic encoder is not suitable for all cases.

## Exercise 2: Fix a DOM XSS sink

Review:

```javascript
const term = location.hash.slice(1);
document.querySelector("#result").innerHTML = term;
```

1. Explain the unsafe behavior.
2. Rewrite the code to display plain text.
3. Write a test case proving markup-like input does not create a DOM element.
4. Identify two other DOM APIs that deserve security review.

## Exercise 3: URL encoding versus URL validation

A site builds a link from a user-supplied URL.

1. Explain the difference between encoding a query parameter and validating a full destination URL.
2. Define an allowlist policy for a feature that links to documentation.
3. Identify dangerous schemes or destinations the policy should reject.
4. Explain where the validation must occur if the link influences a security-sensitive server action.

## Exercise 4: Template escaping review

A developer writes:

```html
<div>{{ comment | safe }}</div>
```

1. Why might this be unsafe?
2. What should be used for ordinary text?
3. When might HTML sanitization be appropriate?
4. What tests should be added after remediation?

## Exercise 5: Context mapping table

Create a table for HTML text, quoted attributes, URL query values, complete URLs, JavaScript data, CSS values, and rich HTML. Include:
- Recommended safe API or encoder
- Dangerous sink or misuse
- Required validation or allowlist
- Regression test

## Exercise 6: JSON response

Review this conceptual code:

```python
body = '{"name": "' + user_name + '"}'
return Response(body, content_type="text/html")
```

Rewrite it using a JSON serializer and the correct response content type. Explain why correct JSON serialization does not automatically make it safe to later insert the value into HTML.

## Exercise 7: Rich-text requirement

A product team wants users to format descriptions with bold text, lists, and links.

1. Explain why output encoding alone may break the feature.
2. Define a restrictive HTML sanitization policy.
3. Describe link validation requirements.
4. Explain how sanitizer updates and post-sanitization transformations affect risk.
5. Write positive and negative test cases.

## Exercise 8: DevSecOps integration

Design checks for each stage:
- Pull request review
- Static analysis
- Unit and integration tests
- Dependency scanning
- Deployment configuration
- Runtime monitoring

Include how to search for unsafe sinks and framework escape hatches, how to test context-specific behavior, and who owns remediation.

## Exercise 9: Double encoding and data lifecycle

A name is HTML-encoded before storage, then encoded again by the template.

1. Describe the visible symptom.
2. Explain why encoding should normally occur near the rendering sink.
3. Define a migration approach if the database already contains encoded values.
4. Identify how tests can distinguish safe rendering from double encoding.

## Exercise 10: Mini project

In a local web application:
1. Find three places where untrusted data is rendered.
2. Document each output context.
3. Replace unsafe sinks with appropriate APIs or encoders.
4. Add regression tests.
5. Run available static analysis.
6. Record the results and any remaining risky contexts.

## Submission checklist

- [ ] Each output context is identified correctly.
- [ ] Plain text is not parsed as HTML.
- [ ] Full URLs are validated separately from parameter encoding.
- [ ] Inline script and event-handler interpolation are avoided.
- [ ] Rich HTML is sanitized only when required.
- [ ] Tests cover normal text, special characters, and invalid destinations.
- [ ] Remediation and evidence are documented.
