# 05 — TLS and Certificates

Learn how Transport Layer Security (TLS) protects network communication, how X.509 certificates establish server identity, and how to inspect and troubleshoot certificate chains. These concepts are essential for HTTPS, APIs, reverse proxies, service-to-service communication, and DevSecOps.

## Learning objectives

By the end of this module, you should be able to:

- Explain TLS confidentiality, integrity, authentication, and the role of certificates.
- Describe the high-level TLS handshake and the difference between TLS and HTTPS.
- Identify certificate fields such as subject, Subject Alternative Name (SAN), issuer, validity, and public key.
- Explain root, intermediate, and leaf certificates and how chain validation works.
- Use OpenSSL and curl to inspect certificates and TLS connections.
- Generate a self-signed certificate for a local lab and understand why it is not automatically trusted.
- Troubleshoot common certificate errors without disabling validation.
- Recommend secure certificate lifecycle practices.

## Prerequisites

- Basic networking, TCP/IP, DNS, and HTTP knowledge.
- A terminal with `openssl` and `curl`.
- Use only systems, domains, and certificates you own or are authorized to inspect.

## Core concepts

- **TLS:** Cryptographic protocol that protects data in transit.
- **HTTPS:** HTTP carried over TLS.
- **Certificate:** A signed data structure binding an identity (such as a DNS name) to a public key.
- **Certificate Authority (CA):** An entity that signs certificates under a trust model.
- **Public/private key pair:** The public key can be shared; the private key must remain secret.
- **SAN:** Subject Alternative Name, used to list DNS names or IP addresses the certificate is valid for.
- **Certificate chain:** Leaf certificate plus required intermediate certificates, validated to a trusted root.
- **Validity period:** `Not Before` and `Not After` times that bound certificate validity.
- **Revocation:** Mechanisms such as CRLs and OCSP can communicate certificate status, though client behavior varies.

## Simplified TLS connection

1. Client and server negotiate protocol parameters and cryptographic options.
2. The server provides its certificate chain and proves possession of the associated private key as required by the handshake.
3. The client validates the certificate chain, hostname, validity period, and trust.
4. The peers establish session keys and protect application traffic.

Modern TLS versions have important differences; this is a conceptual overview rather than a packet-by-packet specification. TLS 1.3 removed several legacy options and typically completes the handshake more efficiently.

## Useful commands

Inspect a remote server's certificate (replace the hostname with an authorized target):

```bash
openssl s_client -connect example.com:443 -servername example.com -showcerts
```

Inspect a local certificate:

```bash
openssl x509 -in certificate.pem -noout -subject -issuer -dates -ext subjectAltName
```

Check an HTTPS response:

```bash
curl -Iv https://example.com
```

Generate a local self-signed certificate for testing:

```bash
openssl req -x509 -newkey rsa:2048 -sha256 -days 30 -nodes \
  -keyout lab-key.pem -out lab-cert.pem \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

Keep private keys private. The `-nodes` option writes an unencrypted private key, suitable only for a controlled lab example; use appropriate key protection for real deployments.

## Files in this module

- `README.md` — concepts, objectives, and quick reference.
- `examples.md` — OpenSSL and curl examples.
- `practical.md` — hands-on exercises.
- `solutions.md` — reference answers and troubleshooting.

## Security best practices

- Prefer currently supported TLS versions and secure library defaults; disable obsolete protocol versions and weak cipher suites according to your environment's baseline.
- Validate the certificate chain and hostname. Do not use `curl -k` or equivalent validation bypasses as a fix.
- Protect private keys with restrictive file permissions and appropriate secret-management controls.
- Automate certificate renewal and monitor expiry.
- Include all required SAN entries and intermediate certificates.
- Use certificates from a trusted CA for public services; use a managed internal CA for private services where appropriate.
- Rotate keys and revoke/replace certificates when compromise is suspected.
- Avoid putting private keys in Git repositories, container images, logs, or public issue trackers.
