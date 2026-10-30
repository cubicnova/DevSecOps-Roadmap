# TLS and Certificates — Reference Solutions

These answers describe general principles. Exact output depends on the endpoint, operating system, OpenSSL version, and trust store.

## Exercise 1 — Inspect a public certificate

The `s_client` output typically includes negotiated protocol/cipher details, the server's certificate chain, and a verification result. Record the SANs and validity dates for the specific authorized endpoint at the time of testing. Do not assume that one successful endpoint proves every server behind a load balancer is configured identically.

## Exercise 2 — Certificate fields

- **Subject:** identity information in the certificate.
- **Issuer:** the CA or issuer that signed it.
- **SAN:** names and addresses for which the certificate is valid.
- **Validity period:** the `Not Before` and `Not After` window.

Modern hostname verification relies on SAN entries. A certificate with a valid signature can still be wrong for the requested hostname.

## Exercise 3 — TLS versus HTTP

HTTP does not use TLS by itself. HTTPS carries HTTP inside TLS, which protects data in transit and can authenticate the server identity. A phishing or malicious site can still have a correctly issued HTTPS certificate.

## Exercise 4 — Lab certificate

The generated certificate should show `DNS:localhost` and `IP Address:127.0.0.1` in its SAN. It is self-signed, so clients will not trust it unless the lab trust configuration explicitly trusts it. Restrict the private key with `chmod 600` and do not reuse it outside the lab.

## Exercise 5 — Hostname validation

A client normally rejects a self-signed certificate because it cannot build a trusted chain. Skipping validation removes a key protection against impersonation. For a controlled lab, use a lab CA installed only in the test trust store and connect with correct hostname validation.

## Exercise 6 — Chain validation

The leaf certificate identifies the service. An intermediate certificate links the leaf issuer to a trusted root. The root is generally configured in the client's trust store. Trust requires a valid chain, acceptable dates and algorithms, and a matching hostname, among other policy checks.

## Exercise 7 — Troubleshooting checklist

1. Confirm system clocks are correct.
2. Check `Not Before` and `Not After`.
3. Confirm the requested hostname is in SAN.
4. Verify the server sends required intermediate certificates.
5. Check the client's trust store and relevant CA policy.
6. Inspect proxy/load-balancer TLS termination and upstream settings.
7. Confirm renewal ran and the renewed certificate was actually deployed.

Avoid disabling validation. If a fix is urgent, use an approved rollback or restore the known-good certificate configuration.

## Exercise 8 — Key matching

If `diff -u cert-public.pem key-public.pem` prints no differences, the public key in the certificate matches the public portion derived from the private key. A mismatch means the pair should not be deployed together. Do not disclose the private key to demonstrate the result.

## Exercise 9 — Lifecycle plan

A good lifecycle has an accountable service owner, automated issuance where appropriate, access-controlled private-key storage, repeatable deployment, expiry monitoring, documented renewal, tested rollback, and a defined response for suspected key compromise. Record changes without logging private key material.

## Exercise 10 — Secure deployment review

Use currently supported TLS versions and a maintained crypto library; configure certificates with the correct SANs and complete chain; protect keys with least privilege and a secret-management solution; automate renewal; monitor expiry and failures; validate upstream certificates; and remove obsolete protocol/cipher configurations according to a maintained security baseline.

## Review questions

1. TLS provides confidentiality, integrity, and authentication according to the connection's configuration.
2. SNI lets a client indicate the target hostname during the TLS handshake so a server can select the right configuration/certificate.
3. SAN lists the DNS names or IP addresses covered by the certificate and is central to hostname validation.
4. A self-signed certificate is not linked to a trusted CA by default.
5. The leaf identifies the service; an intermediate certificate helps link it to a trusted root.
6. Git history and clones can preserve secrets; private keys must remain in controlled secret storage.
7. `curl -k` disables certificate verification and can hide impersonation or trust problems.
8. Check clock, hostname/SAN, expiry, chain completeness, and trust configuration.
