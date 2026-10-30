# Security Review Checklist Examples

## Example 1 — Pull request adds invoice download
**Change:** Adds `GET /api/invoices/{invoice_id}/download`.

Review focus:
- Authentication and object-level authorization on every request.
- Tenant and ownership enforcement; do not trust a client-supplied ID.
- Safe file/object retrieval and content disposition.
- Rate limits and audit events.
- Negative tests for another user's invoice and nonexistent IDs.
- No invoice contents, tokens, or personal data in logs.

**Example finding:** “The endpoint checks that the user is logged in but does not verify invoice ownership. A customer may download another customer's invoice by changing `invoice_id`. Add server-side ownership authorization and tests for cross-account access.”

## Example 2 — New dependency added
Review focus:
- Is the package needed?
- Is the package name and source correct?
- Is the version pinned/locked according to project conventions?
- Does it have known vulnerabilities, suspicious install scripts, or unclear maintenance?
- Are licenses acceptable?
- Does the dependency introduce transitive packages or runtime permissions?
- Is there a plan to update it?

## Example 3 — CI pipeline change
**Change:** A workflow now runs on pull requests from forks and has access to deployment secrets.

Review focus:
- Can untrusted pull-request code read or exfiltrate secrets?
- Are workflow permissions minimal?
- Are privileged deployment jobs isolated from untrusted build/test jobs?
- Are actions pinned and reviewed?
- Can an attacker modify workflow definitions and trigger a privileged run?
- Are logs and artifacts free of secrets?

A safe design separates untrusted validation from privileged deployment and grants production credentials only to trusted, approved release paths.

## Example 4 — File upload feature
Review focus:
- Server-side size and content checks.
- Server-generated filenames and safe path handling.
- Quarantine and scanning before publication.
- Storage outside executable web roots.
- Authorization on upload and download.
- Archive expansion limits and malicious content handling.
- No public access to unapproved files.
- Tests for oversized files, invalid types, and unauthorized retrieval.

## Example 5 — Security review record
| Field | Example |
|---|---|
| Review ID | SR-2026-014 |
| Scope | Invoice download endpoint |
| Checklist areas | Authentication, authorization, API, logging |
| Status | Needs changes |
| Finding | Missing object ownership check |
| Severity | High in this fictional scenario |
| Owner | API team |
| Required evidence | Authorization unit tests and retest |
| Decision | Do not merge until policy-required fix is verified |

Severity must be based on the actual environment, data, exploitability, and organizational criteria. This table is only an example.

## Example 6 — Checklist status
- **PASS:** Verified the endpoint rejects cross-tenant object IDs; test evidence linked.
- **FAIL:** API accepts a protected field from user-controlled JSON.
- **N/A:** No file uploads exist in the reviewed change; reason recorded.
- **NEEDS-REVIEW:** A new encryption setting is present but effective runtime configuration has not been verified.
