# TLS and Certificates — Examples

Run these commands against your own lab or an authorized endpoint. Remote certificate details can change, and command output depends on the OpenSSL version and server configuration.

## 1. Inspect a server's TLS certificate

```bash
openssl s_client -connect example.com:443 -servername example.com -showcerts
```

- `-connect` specifies the host and port.
- `-servername` sends SNI, allowing servers hosting multiple sites to select the right certificate.
- `-showcerts` prints the certificate list sent by the server.

Look for the certificate chain and verification result. A server may send its leaf and intermediate certificates; the trust root is commonly supplied by the client trust store rather than sent by the server.

## 2. View selected certificate fields

Save a certificate in PEM format as `certificate.pem`, then run:

```bash
openssl x509 -in certificate.pem -noout -subject -issuer -dates
openssl x509 -in certificate.pem -noout -ext subjectAltName
openssl x509 -in certificate.pem -noout -fingerprint -sha256
```

- **Subject:** identity fields in the certificate.
- **Issuer:** entity that signed the certificate.
- **Dates:** validity window.
- **SAN:** DNS names and/or IP addresses covered by the certificate.
- **Fingerprint:** hash used to identify the certificate; compare it through a trusted channel when identity matters.

## 3. Check a TLS endpoint and hostname validation

```bash
curl -Iv https://example.com
```

Verbose output can show TLS negotiation, certificate validation, and HTTP headers. Do not post verbose logs publicly without reviewing them for sensitive information.

## 4. Check a certificate chain

```bash
openssl s_client -connect example.com:443 \
  -servername example.com \
  -verify_return_error \
  -showcerts </dev/null
```

`-verify_return_error` makes verification errors fail the connection. The trust store and OpenSSL build affect the result. This is a diagnostic, not a complete external security audit.

## 5. Create a self-signed localhost certificate

```bash
openssl req -x509 -newkey rsa:2048 -sha256 -days 30 -nodes \
  -keyout lab-key.pem -out lab-cert.pem \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
chmod 600 lab-key.pem
```

This creates a certificate and private key for a local lab. Self-signed means it is not automatically trusted by normal clients. The SAN extension is important because modern hostname verification uses SAN rather than relying only on the Common Name.

## 6. Start a local TLS test server

In one terminal, run:

```bash
openssl s_server -accept 8443 -cert lab-cert.pem -key lab-key.pem -www
```

In a second terminal, test the connection:

```bash
curl -vk https://localhost:8443/
```

The `-k` flag is used here only to demonstrate the effect of skipping trust validation in a local lab. It should not be used as a production fix. A safer test is to configure an appropriate trusted lab CA and use `curl --cacert lab-ca.pem` when the certificate is signed by that CA.

Stop the server with `Ctrl+C` when finished.

## 7. Inspect key details

For a certificate:

```bash
openssl x509 -in lab-cert.pem -noout -text
```

For a private key, inspect only the metadata and never paste the private key itself into tickets or chats:

```bash
openssl pkey -in lab-key.pem -noout -text
```

Be cautious: some tools may print sensitive key parameters. Prefer metadata-only commands when possible.

## 8. Compare certificate and private-key public keys

For an RSA or other supported key:

```bash
openssl x509 -in lab-cert.pem -pubkey -noout > cert-public.pem
openssl pkey -in lab-key.pem -pubout > key-public.pem
diff -u cert-public.pem key-public.pem
```

No output from `diff` indicates that the public keys match. Delete temporary public-key files when no longer needed.

## 9. Common certificate errors

- **Expired:** the current time is outside the certificate validity period.
- **Hostname mismatch:** the requested DNS name or IP is not covered by SAN.
- **Unknown issuer / incomplete chain:** the client cannot build a chain to a trusted root.
- **Not yet valid:** system clock or certificate dates are incorrect.
- **Untrusted self-signed certificate:** the certificate is not anchored in the client's trust store.

Check system time, hostname, SAN, chain, and trust configuration before making changes.
