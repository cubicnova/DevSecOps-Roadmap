# Solutions — Ports and Protocols

These are example answers and diagnostic approaches. Your actual listeners, network policy, and command output depend on your system. Do not copy example observations as if they were measured facts.

## Lab 1 — Build a port reference table

Useful common associations include:

| Service | Common port(s) | Transport | Security notes |
|---|---:|---|---|
| SSH | 22 | TCP | Strong authentication; restrict administrative access |
| Telnet | 23 | TCP | Plaintext; avoid for sensitive administration |
| SMTP relay | 25 | TCP | Server-to-server mail transfer; secure configuration required |
| DNS | 53 | UDP/TCP | Both transports are used |
| DHCPv4 | 67/68 | UDP | Usually local network/relay scope |
| HTTP | 80 | TCP | Plain HTTP does not provide TLS protection |
| POP3 | 110 | TCP | Prefer protected transport |
| NTP | 123 | UDP | Restrict and configure appropriately |
| IMAP | 143 | TCP | Prefer protected transport |
| SNMP | 161/162 | UDP | Restrict sources and use secure configuration |
| HTTPS | 443 | TCP commonly; UDP for HTTP/3 | Validate certificates and application configuration |
| SMB | 445 | TCP | Avoid public exposure |
| SMTP submission | 587 | TCP | Authenticated submission; TLS commonly used |
| LDAPS | 636 | TCP | Certificate validation |
| IMAPS | 993 | TCP | TLS-protected mail access |
| RDP | 3389 | TCP/UDP | Restrict; use strong access controls |
| MySQL | 3306 | TCP | Private access only unless justified |
| PostgreSQL | 5432 | TCP | Restrict to approved clients |
| Redis | 6379 | TCP | Avoid public exposure |
| HTTP alternate | 8080 | TCP commonly | Not guaranteed to be HTTP |
| HTTPS alternate | 8443 | TCP commonly | Verify actual service |
| MongoDB | 27017 | TCP | Restrict network access and authenticate |

Use the IANA registry and vendor documentation for authoritative service information. Registered ports are not proof of actual service identity.

## Lab 2 — List local listeners

Linux examples:

```bash
ss -lnt
ss -lnu
sudo ss -lntup
```

Windows examples:

```powershell
Get-NetTCPConnection -State Listen
Get-NetUDPEndpoint
```

Interpretation:
- `127.0.0.1` or `::1` usually indicates loopback-only binding.
- `0.0.0.0` or `::` commonly indicates listening on all IPv4 or IPv6 interfaces, subject to OS behavior and socket options.
- A bound socket does not prove the host firewall allows remote access.
- Identify the owning process and service before changing anything.

## Lab 3 — Test a known HTTPS port

```bash
nc -vz -w 3 example.com 443
curl -I --max-time 10 https://example.com/
```

`nc` checks whether a TCP connection can be established to the endpoint. `curl` additionally performs TLS and HTTP behavior, including certificate verification unless configured otherwise. TCP may succeed while TLS or HTTP fails. Conversely, network or proxy configuration can affect the two tools differently.

## Lab 4 — Compare TCP and UDP

TCP provides a reliable, ordered byte stream with retransmission and flow control. UDP sends datagrams without TCP-style delivery or ordering guarantees. Applications may add their own reliability.

DNS commonly uses UDP for ordinary queries but also uses TCP for cases including zone transfers and some large/truncated responses. HTTP/3 uses QUIC over UDP, commonly on port 443, while HTTP/1.1 and HTTP/2 are commonly deployed over TCP.

UDP testing is often inconclusive because many UDP services do not respond to unexpected probes and filtering can silently drop packets.

## Lab 5 — Diagnose a refused connection

Suggested sequence:

```bash
systemctl status SERVICE_NAME
journalctl -u SERVICE_NAME --since "1 hour ago" --no-pager
sudo ss -lntup
```

Then confirm expected port, bind address, configuration, and firewall behavior. A refusal often indicates no listener or an active reject, but the exact source can be a host or intermediate device. Do not restart or change a service until evidence and impact are understood.

## Lab 6 — Diagnose a timeout

Check:
1. Name resolution and the intended destination IP.
2. Local interface and route.
3. Destination service listener (if authorized to inspect server).
4. Host firewall and upstream ACL/security group.
5. Packet loss, routing, and return path.
6. Proxy or NAT behavior if present.

A timeout means no timely response was received. It does not identify which device or layer caused the problem.

## Lab 7 — Inspect DNS behavior

`getent` uses the system name-service path, while `dig` sends DNS queries directly to a selected/configured resolver. A TCP query can be made with `dig +tcp example.com` on common versions. Results can differ because of resolver configuration, caches, split-horizon DNS, or policy.

DNS success only shows that the query returned a result; the destination may still be unreachable or the application may not be listening.

## Lab 8 — Review firewall posture

Read-only inspection can include:

```bash
sudo ufw status verbose
sudo nft list ruleset
```

Only one tool may be active, or a host may use a different firewall manager. Review cloud security groups, network ACLs, routing, and upstream firewalls as applicable. Recommend only required inbound ports from required source networks; do not blindly copy rules or risk locking out administrators.

## Lab 9 — Create a local port inventory

For each listener, establish:
- Process and owning service
- Expected business purpose
- Bind address and actual reachability
- Required source networks
- Authentication and encryption
- Service owner and patch status
- Approved next action

An unfamiliar port is not automatically malicious. Correlate with packages, process details, deployment configuration, and logs.

## Lab 10 — Security exposure scenario

A database exposed publicly can face unauthorized login attempts, exploitation of unpatched services, data theft, and denial of service.

A safe response:
1. Preserve relevant logs and document the exposed endpoint.
2. Notify the service owner and follow incident/change procedures.
3. Restrict network access to approved application hosts or private networks.
4. Preserve an approved administrative recovery path.
5. Confirm authentication, encryption, patching, and monitoring.
6. Verify reachability from both an approved client and an untrusted/external vantage point under authorization.
7. Record rollback steps and monitor for recurrence.

Do not abruptly block the only management path without a recovery plan.

## Lab 11 — Port versus service identity

Port 8080 is commonly used for alternate HTTP services but can host other protocols. Port 443 can host a misconfigured service or an untrusted application. Service identity should be supported by process information, configuration, protocol handshake, logs, and approved service documentation—not just the port number or a banner.

## Lab 12 — Incident report

A good report format:

```text
Finding: [observed issue]
System/time: [host, time, timezone]
Endpoint: [port/protocol and redacted address as appropriate]
Evidence: [commands, results, logs]
Impact: [confirmed or suspected]
Hypothesis: [cause and confidence]
Next test: [evidence needed]
Action: [approved change, if any]
Verification: [how to confirm resolution]
Remaining risk: [unknowns and follow-up]
```

Separate confirmed facts from hypotheses. Include enough detail to reproduce the observation while avoiding secrets and unnecessary topology disclosure.

## Key reminders

- Ports identify transport endpoints, not guaranteed application identity.
- TCP and UDP use separate port spaces.
- Listening state, firewall policy, routing, and application health are different things.
- A refusal and a timeout suggest different patterns but do not prove root cause.
- Expose only required services to required source networks.
