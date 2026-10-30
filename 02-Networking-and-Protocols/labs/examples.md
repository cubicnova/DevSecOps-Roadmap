# Networking and Protocols Labs — Command Examples

Use these examples only on systems you own or are authorized to test. Replace placeholders before running commands. Output varies by operating system and network policy.

## 1. Inspect interfaces and addresses

```bash
ip -br link
ip -br address
```

Use these commands to identify interface state and configured addresses. An interface can be up without having working end-to-end connectivity.

## 2. Inspect the route

```bash
ip route
ip route get 1.1.1.1
```

The route lookup shows the route selected for a destination. Compare the chosen interface and source address with a known-good host when diagnosing an issue.

## 3. Resolve a hostname

```bash
getent hosts example.com
dig example.com A
dig example.com AAAA
dig example.com MX
```

`getent` follows the operating system's resolver configuration. `dig` lets you inspect DNS records directly. Different results can be caused by split-horizon DNS, VPN configuration, caches, or search domains.

## 4. Test a specific DNS resolver

```bash
dig @1.1.1.1 example.com A
```

Only use direct public resolver queries when permitted. A public resolver may not know internal DNS names and may bypass required corporate DNS policy.

## 5. Inspect listening sockets

```bash
ss -lntup
ss -tan
```

The first command lists listening TCP/UDP sockets; process details may require elevated privileges. The second displays TCP sockets and their states.

## 6. Test a local TCP port

Terminal A:

```bash
python3 -m http.server 18080 --bind 127.0.0.1
```

Terminal B:

```bash
nc -vz -w 3 127.0.0.1 18080
nc -vz -w 3 127.0.0.1 18081
curl -i --max-time 5 http://127.0.0.1:18080/
```

Port 18080 should accept connections while the demo server runs. Port 18081 should commonly be refused if no service is listening.

## 7. Inspect HTTP response headers

```bash
curl -sS -D - -o /dev/null --connect-timeout 5 --max-time 15 https://example.com/
```

Review the status code, redirects, and relevant headers. Avoid sharing response headers if they contain cookies or tokens.

## 8. Inspect TLS

```bash
openssl s_client -connect example.com:443 -servername example.com </dev/null
```

Check the certificate hostname, validity dates, chain, and handshake errors. Do not permanently disable certificate validation to work around a failure.

## 9. Check path and latency

```bash
ping -c 20 example.com
tracepath example.com
```

If installed and approved:

```bash
mtr -rw -c 20 example.com
```

Diagnostic probes may be filtered or rate-limited. Missing replies from an intermediate hop do not alone prove that forwarded traffic is being dropped.

## 10. Capture a limited DNS trace

```bash
ip -br link
sudo tcpdump -i <interface> -nn -c 100 port 53
```

Trigger a lookup in another terminal:

```bash
dig example.com
```

Select the correct interface and keep the capture narrow. Captures can reveal internal hostnames and other sensitive metadata.

## 11. Review proxy variables

```bash
env | grep -i proxy
```

A CLI request may use a proxy while another application follows a different route. Redact credentials if a proxy URL includes them.

## 12. Read-only firewall inspection

Use the applicable command for your distribution:

```bash
sudo ufw status
# or
sudo nft list ruleset
```

Do not flush rules or disable security controls as a first diagnostic step.

## 13. NGINX load-balancer request test

After configuring a local NGINX upstream and two loopback backends:

```bash
for i in $(seq 1 8); do
  curl -sS --max-time 3 http://127.0.0.1:18080/ || echo "request failed"
done
```

The response body should identify which backend answered. A small sample is a functional test, not a performance benchmark.

## 14. Validate NGINX before reload

```bash
sudo nginx -t && sudo systemctl reload nginx
```

The reload occurs only if the syntax test succeeds. Paths and service managers vary by distribution.

## 15. Record an evidence-based troubleshooting result

For each test, note:
- Timestamp and timezone.
- Exact command and sanitized output.
- Expected result versus actual result.
- What the result proves and what it does not prove.
- Next diagnostic step.

Do not paste passwords, tokens, private keys, session cookies, or unnecessary personal data into lab notes.
