# XSS and CSRF Prevention — Exercises

Complete the exercises in a local application or a system you are explicitly authorized to test.

## Exercise 1: Classify XSS

Classify each scenario as reflected, stored, or DOM-based XSS and explain the unsafe data flow:

1. Search text is inserted unescaped into a server-generated results page.
2. A comment is saved in a database and later rendered as active markup.
3. A client-side script reads `location.hash` and assigns it to `innerHTML`.

For each case, propose a prevention and a regression test.

## Exercise 2: Replace an unsafe DOM sink

Review:

```javascript
results.innerHTML = "Welcome " + displayName;
```

Rewrite it so `displayName` is displayed as plain text. Explain why input validation alone is not a replacement for safe rendering.

## Exercise 3: Rich-text feature

A product allows users to submit formatted descriptions with links and lists.

1. Explain why encoding all content would change the intended feature.
2. Recommend a safe sanitization approach.
3. List maintenance and testing requirements for the sanitizer.
4. Explain why sanitizing and then appending untrusted markup is unsafe.

## Exercise 4: Context-aware output handling

For each destination, name the appropriate control:

- User value between HTML text tags.
- User value in a quoted ordinary HTML attribute.
- User value in a URL query parameter.
- User value used as a complete link destination.
- User value in an inline JavaScript block.
- User-authored rich HTML.

Identify any contexts that should be avoided rather than made safe with generic escaping.

## Exercise 5: Find the CSRF risk

An application changes a user's email using `GET /change-email?email=...` and relies on the browser's session cookie.

1. Explain the risk.
2. Propose a safer HTTP method and request flow.
3. List the server-side checks needed.
4. Explain why a `GET` request should not perform the change.

## Exercise 6: CSRF token tests

Write a test matrix for a state-changing endpoint with these cases:

- Valid session and valid token.
- Valid session but missing token.
- Valid session but incorrect token.
- Expired session.
- Cross-origin request with missing token.
- Token from a different session.

State expected outcomes and what should be logged.

## Exercise 7: Cookie controls

Explain the purpose and limitations of `Secure`, `HttpOnly`, and `SameSite`. Choose a `SameSite` value for a typical first-party web app and explain when cross-site functionality may require a different choice.

## Exercise 8: Origin validation

A developer checks `Origin` with `origin.includes("example.com")`.

1. Why is this check unsafe?
2. Describe exact origin parsing and comparison.
3. Explain how missing or `null` origins should be handled according to the application's threat model.

## Exercise 9: CSP and defense in depth

Describe how Content Security Policy can reduce the impact of some XSS bugs. Explain why CSP does not replace safe DOM APIs, contextual output encoding, or HTML sanitization.

## Exercise 10: Framework configuration review

Review a web application's use of:
- Template auto-escaping.
- Raw HTML escape hatches.
- CSRF middleware.
- Cookie attributes.
- State-changing `GET` routes.
- Security library updates.

Create a checklist and identify a test for each item.

## Exercise 11: Threat model

For a profile-management web app, identify:
- Three user-controlled data sources.
- Three XSS sinks.
- Three state-changing operations that need CSRF consideration.
- Controls that prevent or reduce each risk.
- At least five negative tests.

## Exercise 12: Mini-project

Build a small profile web application that supports comments and profile updates. Include:

- Safe text rendering.
- Sanitization for any intentional rich-text feature.
- URL validation for links.
- Framework CSRF middleware or server-validated tokens.
- Safe session-cookie attributes.
- No state-changing `GET` endpoints.
- Automated tests for unsafe rendering and missing/invalid CSRF tokens.

**Acceptance criteria:** user-provided plain text is never interpreted as markup, rich HTML is sanitized under an explicit policy, and protected state-changing requests are rejected when CSRF validation fails.
