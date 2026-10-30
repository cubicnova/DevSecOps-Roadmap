# API Security Review Checklist

## Inventory and exposure
- [ ] All routes, methods, versions, and owners are inventoried.
- [ ] Debug, test, undocumented, and deprecated endpoints are identified.
- [ ] API documentation and deployed behavior are reconciled.
- [ ] Public, internal, partner, and service-to-service APIs are classified.
- [ ] API retirement and version-support policies are defined.

## Authentication and authorization
- [ ] Authentication is required wherever intended and implemented with maintained libraries.
- [ ] Token signature, issuer, audience, expiry, and required claims are validated.
- [ ] Scopes and roles are checked separately from token validity.
- [ ] Object-level authorization is enforced for every object reference.
- [ ] Function-level authorization protects privileged operations.
- [ ] Property-level authorization limits writable and readable fields.
- [ ] Tenant boundaries are enforced server-side.
- [ ] Authorization is deny-by-default and tested for negative cases.

## Input, output, and errors
- [ ] Inputs have type, format, length, range, and business-rule validation.
- [ ] Unexpected fields are rejected or safely ignored.
- [ ] Request and response schemas are explicit and separate.
- [ ] Responses expose only necessary properties.
- [ ] Pagination, filters, sorting, and query complexity are bounded.
- [ ] Errors do not reveal stack traces, internal paths, SQL details, or secrets.
- [ ] Request and upload size limits are configured.

## Resource and workflow abuse
- [ ] Rate limits and quotas cover relevant identities, tenants, and endpoints.
- [ ] Expensive operations have timeouts and concurrency limits.
- [ ] Sensitive workflows enforce state transitions and eligibility server-side.
- [ ] Replay and duplicate-submission behavior is defined.
- [ ] Uploads and imports have appropriate validation and scanning.
- [ ] Abuse signals are monitored and handled proportionately.

## Network and integrations
- [ ] HTTPS is enforced.
- [ ] CORS allows only required browser origins and headers.
- [ ] CORS is not relied on as an authorization control.
- [ ] URL-fetching features have SSRF controls and egress restrictions.
- [ ] Third-party API responses are treated as untrusted input.
- [ ] Webhook authentication, signature validation, and replay controls are reviewed.

## Secrets and observability
- [ ] API keys and tokens are not embedded in public clients or source code.
- [ ] Secrets are stored and rotated using an approved process.
- [ ] Credentials and sensitive payloads are redacted from logs.
- [ ] Security events include useful correlation identifiers.
- [ ] Monitoring covers authentication failures, authorization denials, rate-limit events, and suspicious workflows.
- [ ] Security tests and regression tests run in CI.
