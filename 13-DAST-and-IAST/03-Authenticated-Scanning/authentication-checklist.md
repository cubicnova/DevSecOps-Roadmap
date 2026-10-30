# Authenticated DAST Checklist

## Before scanning
- [ ] Written authorization and target owner confirmed
- [ ] Local/staging/ephemeral environment selected
- [ ] Exact host, paths, ports, and exclusions documented
- [ ] Dedicated synthetic test account provisioned
- [ ] Least privilege applied
- [ ] Credentials stored outside source control
- [ ] Destructive routes and logout excluded where appropriate

## Authentication configuration
- [ ] Context includes all required application URLs
- [ ] Authentication method matches the real login flow
- [ ] Session management method matches cookies/headers/custom flow
- [ ] Logged-in and logged-out indicators tested
- [ ] Verification endpoint is authenticated-only and reliable
- [ ] Test user is configured in the Context
- [ ] Login success independently verified

## During scanning
- [ ] Spider runs as the intended user
- [ ] Protected requests return authenticated content
- [ ] Session expiry/re-authentication behavior checked
- [ ] 401 and 403 responses reviewed
- [ ] Role-specific coverage recorded
- [ ] Reports and logs do not expose secrets

## After scanning
- [ ] Findings manually triaged
- [ ] Coverage gaps and excluded workflows documented
- [ ] Reports stored with restricted access and retention
- [ ] Temporary accounts, tokens, and sessions revoked
- [ ] Ephemeral environment removed
