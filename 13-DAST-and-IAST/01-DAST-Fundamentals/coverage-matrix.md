# DAST Coverage Matrix

Use this worksheet during a local or explicitly authorized assessment.

| Feature / route | Public or authenticated | Role tested | Discovered by | Tested? | Evidence / gap |
|---|---|---|---|---|---|
| Home page | Public | N/A | Crawler | | |
| Login | Public | N/A | Manual | | |
| User profile | Authenticated | Test user | Manual/crawler | | |
| Admin function | Authenticated | Admin test user | Manual/API spec | | |
| API endpoint | Authenticated | Test user | OpenAPI | | |

## Coverage notes
- Record routes that require JavaScript interactions or multi-step state.
- Record roles and tenant contexts that were not tested.
- Distinguish discovered endpoints from endpoints actually exercised.
- Never claim complete coverage based only on a successful scanner exit code.
