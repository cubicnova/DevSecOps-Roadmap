# TLS and Certificates — Practical Exercises

Use a local VM or endpoints you are authorized to test. Never upload private keys or sensitive certificate materials to a public repository.

## Exercise 1 — Inspect a public certificate

Run:

```bash
openssl s_client -connect example.com:443 -servername example.com -showcerts </dev/null
```

Record the protocol version, verification result, leaf subject, issuer, validity dates, and SANs. Results can vary by server and time.

**Deliverable:** a redacted certificate-inspection report.

## Exercise 2 — Extract certificate metadata

Save a PEM certificate as `certificate.pem` and run:

```bash
openssl x509 -in certificate.pem -noout -subject -issuer -dates
openssl x509 -in certificate.pem -noout -ext subjectAltName
```

Explain the role of subject, issuer, SAN, and validity period.

## Exercise 3 — TLS versus HTTP

Run:

```bash
curl -Iv http://example.com
curl -Iv https://example.com
```

Compare redirects, TLS negotiation, and certificate validation. Explain why HTTPS protects transport but does not prove that a website is trustworthy.

## Exercise 4 — Create a lab certificate

Create a localhost certificate using the command in `examples.md`. Inspect it with `openssl x509`. Confirm that its SAN contains `DNS:localhost` and `IP Address:127.0.0.1`.

**Safety:** keep the private key in a disposable directory and restrict its permissions.

## Exercise 5 — Test hostname validation

1. Start the local TLS server from `examples.md`.
2. Try connecting to `https://localhost:8443`.
3. Observe the trust error for a self-signed certificate.
4. Explain why bypassing validation is not a proper production solution.
5. Stop the server and remove the lab key when finished.

## Exercise 6 — Understand chain validation

Draw a chain containing:
- leaf/server certificate;
- intermediate CA;
- root CA in the client's trust store.

Explain why a valid date alone is insufficient for trust and why servers usually send intermediates but not the root certificate.

## Exercise 7 — Troubleshooting scenario

A deployment starts failing with a TLS error. Create a checklist that checks:
- client/server clock;
- certificate expiry;
- hostname and SAN;
- missing intermediate certificates;
- trust store;
- proxy/load-balancer configuration;
- renewal and deployment status.

Do not disable certificate validation to suppress the error.

## Exercise 8 — Key matching

For your lab certificate, export the certificate's public key and the private key's public portion as shown in `examples.md`. Use `diff` to compare them.

**Deliverable:** state whether the keys match. Do not include the private key in the report.

## Exercise 9 — Certificate lifecycle plan

Design a lifecycle for a web certificate covering:
1. issuance and identity validation;
2. private-key storage;
3. deployment;
4. renewal and expiry alerts;
5. revocation or replacement after compromise;
6. audit records and ownership.

Include a named owner or role for each step.

## Exercise 10 — Secure deployment review

Review a hypothetical reverse proxy that serves an API. Recommend:
- supported TLS versions;
- correct SANs and complete chain;
- protected private-key storage;
- automated renewal and monitoring;
- strict certificate validation for upstream services;
- removal of obsolete ciphers/protocols under the organization's security baseline.

## Review questions

1. What security properties does TLS provide?
2. What is the purpose of SNI?
3. What is SAN and why is it important?
4. Why is a self-signed certificate not automatically trusted?
5. What is the difference between a leaf and an intermediate certificate?
6. Why should private keys never be committed to Git?
7. Why is `curl -k` unsafe as a routine fix?
8. What should be checked first when a certificate error appears?
