# 10 — Network Troubleshooting

Build a repeatable workflow for diagnosing network connectivity, name resolution, routing, transport, application, and performance problems. This module focuses on Linux command-line tools and practical evidence collection for DevSecOps and system administration.

## Learning objectives

By completing this module, you should be able to:

- Troubleshoot a network issue from physical/link layer through DNS, transport, and application layers.
- Use `ip`, `ping`, `traceroute`, `tracepath`, `ss`, `dig`, `curl`, and packet-capture tools appropriately.
- Distinguish name-resolution failures, routing problems, blocked ports, TLS errors, and application failures.
- Read useful TCP connection states and interpret common HTTP status codes.
- Capture only necessary packet data and protect sensitive information in diagnostic output.
- Record a reproducible incident timeline, evidence, root cause, remediation, and verification.

## Prerequisites

- Basic TCP/IP and OSI model knowledge.
- Familiarity with IP addresses, subnet masks/CIDR, gateways, DNS, ports, TCP/UDP, HTTP/HTTPS.
- Linux shell access. Some commands may require `sudo`; install optional tools only when authorized.

## 1. Use a layered troubleshooting workflow

Start with the narrowest, least disruptive checks and work outward. Avoid changing firewall, route, or DNS configuration before collecting evidence.

1. **Scope:** What is failing, for whom, since when, and what changed?
2. **Link/interface:** Is the interface up and configured?
3. **Addressing/routing:** Does the host have the expected address, route, and gateway?
4. **Name resolution:** Does the hostname resolve to the expected address?
5. **Transport:** Can the host reach the destination port?
6. **TLS/application:** Does the handshake complete, and does the application return the expected response?
7. **Path and performance:** Where might loss, latency, congestion, or MTU problems occur?
8. **Change and verify:** Apply the smallest approved fix, test, monitor, and document.

A successful test at one layer does not prove every layer is healthy. For example, ping can be blocked while HTTPS works, and a successful TCP connection does not prove that the application is healthy.

## 2. Quick triage commands

```bash
# Interface addresses and state
ip -br address
ip link

# Routing table and selected route
ip route
ip route get 1.1.1.1

# Resolver configuration and lookup
cat /etc/resolv.conf
getent hosts example.com

# Connectivity (ICMP may be filtered)
ping -c 4 1.1.1.1

# Path diagnostics
tracepath example.com
# Alternative, if installed:
traceroute example.com

# Listening sockets and connection states
ss -lntup
ss -tan

# TCP port test (requires netcat)
nc -vz -w 3 example.com 443

# HTTP response and TLS diagnostics
curl -v --connect-timeout 5 --max-time 15 https://example.com/
```

Use approved destinations and respect organizational policies. `curl -v` may display headers, cookies, or other sensitive values; redact before sharing output.

## 3. Interface, address, and routing checks

### Inspect interfaces

```bash
ip -br link
ip -br address
```

Look for an interface that is down, a missing address, an unexpected subnet, or an address assigned to the wrong interface. Wireless and virtual interfaces may have different naming conventions.

### Inspect the route decision

```bash
ip route
ip route get 203.0.113.10
```

`203.0.113.0/24` is reserved for documentation; replace the example address with an approved target in your environment. `ip route get` shows the route decision for a destination, including the selected interface and source address.

### Gateway reachability

```bash
ip route
ping -c 4 <gateway-ip>
```

A failed ping does not prove the gateway is down; ICMP may be filtered. Compare with ARP/neighbor state and a permitted TCP test if needed.

## 4. DNS troubleshooting

DNS problems can arise from incorrect records, stale caches, resolver reachability, search domains, split-horizon DNS, or DNSSEC validation.

```bash
# OS resolver path
getent hosts example.com

# Query a record
dig example.com A
dig example.com AAAA
dig example.com MX

# Ask a specific resolver
dig @1.1.1.1 example.com A

# Trace the delegation chain (may be blocked by policy)
dig +trace example.com
```

Compare the OS resolver result with a direct query where permitted. A direct query to a public resolver may bypass corporate split DNS and is not necessarily the correct expected answer. Never change DNS settings solely because one resolver returns a different answer.

## 5. TCP, UDP, and ports

```bash
# Listening TCP/UDP sockets and owning processes
sudo ss -lntup

# All TCP sockets
ss -tan

# Test a TCP connection
nc -vz -w 3 <host> <port>

# Show sockets in common states
ss -tan state established
ss -tan state syn-sent
ss -tan state time-wait
```

Useful distinctions:
- **Connection refused:** a host or device actively rejected the connection, often because nothing is listening or a firewall sent a reject.
- **Timeout:** no response arrived within the timeout; possible causes include filtering, routing failure, packet loss, or an unresponsive service.
- **No route to host/network:** the local host or a network device cannot find or use a viable route, though exact messages vary.
- **Listening port absent:** the service may be stopped, bound to another address, or configured for another port.

UDP has no TCP-style handshake. A lack of response to a UDP probe is often inconclusive.

## 6. HTTP and TLS diagnostics

```bash
# Response headers and status
curl -sS -D - -o /dev/null https://example.com/

# Verbose handshake and request details
curl -v --connect-timeout 5 --max-time 15 https://example.com/

# Test only the TLS handshake and inspect certificate chain
openssl s_client -connect example.com:443 -servername example.com </dev/null
```

Interpret the full evidence, not just one code:
- `301`/`302`: redirect; check `Location` and expected canonical URL.
- `401`: authentication is required or failed.
- `403`: access is forbidden by application or policy.
- `404`: requested resource was not found at that route.
- `429`: request rate or quota may have been exceeded.
- `500`: application-side failure.
- `502`: gateway/proxy could not obtain a valid upstream response.
- `503`: service unavailable or overloaded.
- `504`: gateway/proxy timed out waiting for an upstream.

TLS failures may involve expired certificates, hostname mismatch, incomplete chain, unsupported protocol/cipher, wrong system clock, or interception by a trusted/untrusted proxy. Do not disable certificate validation as a fix. Use `curl -k` only in a controlled diagnostic comparison, never as a production workaround.

## 7. Latency, packet loss, and path analysis

```bash
ping -c 20 <approved-host>
tracepath <approved-host>
mtr -rw -c 20 <approved-host>
```

`mtr` may need installation and elevated privileges depending on platform. Intermediate routers may rate-limit or deprioritize diagnostic traffic, so loss shown at one hop but not later hops is not proof that forwarded traffic is being dropped there.

Compare results over time and from more than one approved endpoint. Distinguish:
- **Latency:** time for a packet or request to travel and return.
- **Packet loss:** probes or packets not observed at the expected point.
- **Jitter:** variation in latency.
- **Throughput:** amount of data transferred per unit time.
- **Application response time:** includes server processing and dependencies, not just network transit.

## 8. Packet capture basics

Capture only what is necessary, with authorization, a limited time window, and a clear storage/retention plan.

```bash
# List interfaces
ip -br link

# Capture DNS traffic on a chosen interface
sudo tcpdump -i <interface> -nn -c 100 port 53

# Capture TCP traffic to a specific host and port
sudo tcpdump -i <interface> -nn -c 100 host <target-ip> and port 443

# Write a short capture to a local file
sudo tcpdump -i <interface> -nn -c 200 -w /tmp/diagnostic.pcap host <target-ip>
```

Replace placeholders with actual values. A packet capture can contain personal data, session tokens, internal addresses, or payload content. Restrict access and delete it according to policy. HTTPS encrypts application payloads, but metadata such as IP addresses, ports, timing, and some handshake information may remain visible.

## 9. Firewall and proxy checks

- Verify the intended service is listening on the correct address and port.
- Check host firewall rules using the platform's approved tooling (for example, `nft list ruleset`, `ufw status`, or the relevant cloud firewall/security-group console).
- Compare source address, destination address, protocol, and port against policy.
- Check proxy environment variables when CLI requests behave differently from browser requests:

```bash
env | grep -i proxy
```

Do not paste credentials embedded in proxy URLs into tickets. Do not flush firewall rules or disable security controls as a troubleshooting shortcut. Request an approved, narrowly scoped rule change when evidence supports it.

## 10. Common symptoms and likely causes

| Symptom | Possible causes | First checks |
|---|---|---|
| Hostname fails but IP works | DNS/resolver/search-domain issue | `getent hosts`, `dig` |
| Nothing on a subnet is reachable | Interface, route, VPN, gateway, ACL | `ip -br address`, `ip route` |
| One port times out | Firewall drop, route issue, service hang | `nc`, route, firewall logs |
| Connection refused | No listener, wrong bind address, active reject | `ss -lntup`, service logs |
| TLS hostname error | Wrong URL, certificate SAN mismatch | `curl -v`, `openssl s_client` |
| Intermittent 502/504 | Unhealthy upstream, overload, timeout | Proxy and backend logs, latency |
| Slow only for large transfers | MTU/MSS, congestion, throughput limit | Compare transfer sizes, approved packet evidence |
| Works on VPN only | Split DNS, private route, access policy | Compare resolver and route on/off VPN |
| Works from one network only | Source ACL, NAT, regional path, DNS differences | Compare source/path and destination logs |

## 11. Incident notes template

Record:
- Start time and timezone.
- Affected service, host, user group, and network.
- Expected versus observed behavior.
- Exact error and a reproducible command.
- Recent changes and known-good comparison.
- Commands run and sanitized outputs.
- Root cause, confidence level, and evidence.
- Fix, approver, rollback plan, and verification.
- Follow-up actions to prevent recurrence.

## 12. Practice checklist

- [ ] Inspect interface addresses and routing.
- [ ] Compare OS DNS resolution with `dig`.
- [ ] Test a TCP port without assuming ping is decisive.
- [ ] Inspect HTTP status and TLS certificate details.
- [ ] Run path diagnostics and explain their limitations.
- [ ] Capture a small, authorized packet trace.
- [ ] Diagnose a simulated refused connection and timeout.
- [ ] Write a concise incident report with evidence and verification.

## Further reading

- `ip` manual: https://man7.org/linux/man-pages/man8/ip.8.html
- `ss` manual: https://man7.org/linux/man-pages/man8/ss.8.html
- `dig` documentation: https://bind9.readthedocs.io/
- `curl` documentation: https://curl.se/docs/
- `tcpdump` manual: https://www.tcpdump.org/manpages/tcpdump.1.html
