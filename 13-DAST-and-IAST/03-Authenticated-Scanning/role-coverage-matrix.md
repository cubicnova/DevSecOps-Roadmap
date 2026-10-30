# Authenticated DAST Role Coverage Matrix

| Feature / endpoint | Anonymous | Standard user | Privileged user | Tenant A | Tenant B | Evidence / notes |
|---|---|---|---|---|---|---|
| `/api/me` | | | | | | |
| `/account` | | | | | | |
| `/admin` | | | | | | |
| `/api/orders` | | | | | | |
| `/api/reports` | | | | | | |

Use `Allowed`, `Denied`, `Not tested`, or `Not applicable` in each cell.

## Review questions
- Are routes discovered under one role absent under another?
- Can one tenant access another tenant's synthetic records?
- Are privileged actions denied to standard users?
- Were denial responses checked for information leakage?
- Which roles, workflows, or endpoints remain untested?

Do not treat a route's appearance in the crawler tree as proof that its authorization behavior was tested.
