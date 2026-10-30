# Network Troubleshooting — Solutions and Explanations

These are reference answers. Exact output depends on the operating system, resolver, network policy, and target service.

## Lab 1 — Baseline

Useful commands include:

```bash
ip -br link
ip -br address
ip route
ip route get <approved-destination-ip>
```

Look for interface state, assigned addresses, default route, route-specific interface, gateway, and source address. Redact internal addresses or hostnames before sharing a report outside the organization.

## Lab 2 — DNS resolution

Useful commands:

```bash
getent hosts example.com
dig example.com A
dig example.com AAAA
```

`getent` follows the host's configured name-service path. `dig` sends DNS queries directly and can be used to inspect specific record types or resolvers. Corporate split DNS, VPN settings, search domains, and local caches can explain differences.

Possible `NXDOMAIN` causes:
- The name does not exist in the queried DNS view.
- A typo or wrong search suffix was used.

Possible timeout causes:
- Resolver is unreachable or blocked.
- Packet loss, firewall policy, or a nonresponsive DNS service prevents a reply.

A timeout does not prove the record is absent. Confirm the hostname, resolver, and network context before changing settings.

## Lab 3 — TCP port diagnostics

The local server should listen on `127.0.0.1:18080`. A connection to that port should normally succeed while the process is running. A connection to port 18081 should commonly be refused because no service is listening.

- **Refused:** an explicit rejection was received, often because no listener exists.
- **Timeout:** no successful response arrived before the timeout, which may indicate filtering, routing problems, loss, or an unresponsive target.

Exact errors depend on the OS and network path.

## Lab 4 — HTTP and TLS

Record the HTTP status and headers, redirects, TLS handshake result, certificate dates, and hostname identity. Use `-servername` with OpenSSL so SNI is sent for the intended hostname.

A TLS failure may be caused by certificate expiry, hostname mismatch, an incomplete chain, unsupported protocol/cipher settings, incorrect system time, or a proxy. The fix is to address the cause, not permanently disable certificate validation.

## Lab 5 — Path and latency

Record several probes and compare them with application behavior. `ping` measures ICMP round-trip time, not full application response time. `tracepath`, `traceroute`, and `mtr` depend on probe types that some networks filter or deprioritize.

If an intermediate hop shows loss but later hops respond normally, the intermediate device may be rate-limiting its own diagnostic replies while still forwarding traffic. Investigate end-to-end loss and service symptoms before blaming that hop.

## Lab 6 — Packet capture

A command such as:

```bash
sudo tcpdump -i <interface> -nn -c 100 port 53
```

collects a bounded sample of visible DNS traffic on the selected interface. Trigger a lookup in another terminal and examine the query and response, if both are visible.

No visible packets may mean the wrong interface was selected, DNS is encrypted, a local cache answered the query, or the packet filter does not match the traffic. Do not broaden the capture without a reason and authorization.

Treat packet captures as sensitive. Limit collection, permissions, storage duration, and sharing.

## Lab 7 — Local service failure

Expected observations:
1. While the server runs, `curl -i http://127.0.0.1:18080/` should receive an HTTP response.
2. After the server stops, the request should fail to connect.
3. `ss -lntp` should no longer show the demo listener.
4. After restart, the request should work again.

The likely root cause is the stopped local server, supported by the listener check and repeatable test. The verification step is a successful request after restart.

## Lab 8 — Firewall and proxy review

Proxy variables can make command-line requests use a proxy while other traffic takes a different path. Firewall status can show whether local rules might affect a connection, but cloud security groups, network ACLs, remote firewalls, and routing may also be involved.

A well-scoped access request names:
- Source address or approved source group.
- Destination address/service.
- Protocol and destination port.
- Business purpose.
- Owner and expiration/review date.
- Validation plan.

Do not disable security controls or flush rules as a diagnostic shortcut.

## Lab 9 — Decision tree example

```text
Service unreachable
  |
  +-- Hostname resolves?
  |     No -> Check name, resolver, DNS path and record
  |     Yes
  |
  +-- Route/interface correct?
  |     No -> Check address, link, gateway and route
  |     Yes
  |
  +-- TCP connection succeeds?
  |     No -> Check listener, port, firewall and route
  |     Yes
  |
  +-- TLS handshake succeeds?
  |     No -> Check hostname, time, certificate and TLS policy
  |     Yes
  |
  +-- HTTP response expected?
        No -> Check status, proxy/backend logs and application
        Yes -> Investigate intermittent performance or client-specific behavior
```

This is a starting point, not a strict universal sequence. Some systems use proxies, service meshes, IPv6, or multiple DNS layers that require additional branches.

## Lab 10 — Incident report example

**Summary:** A group of users reports intermittent HTTPS timeouts between 14:05 and 14:20.

**Evidence to collect:** affected source networks, timestamps, DNS answers, selected routes, TCP connection results, TLS errors, proxy/backend logs, latency samples, and recent deployment or firewall changes.

**Hypothesis:** A backend or network path is intermittently unavailable. This remains a hypothesis until logs and repeatable tests correlate failures to a specific component.

**Remediation:** Apply the smallest approved change supported by evidence, such as restoring a failed service or correcting a narrowly scoped rule. Keep a rollback plan.

**Verification:** Repeat the original failing request from an affected path, compare results with a known-good path, and monitor error rate and latency for an agreed period.

**Prevention:** Add targeted health checks, alerting, runbook steps, and change validation based on the confirmed root cause.

## Key takeaways

- Troubleshoot from evidence and isolate one layer at a time.
- A single failed ping, DNS query, or traceroute hop is not sufficient to prove a root cause.
- Distinguish connection refusal, timeout, TLS failure, and application error.
- Capture the minimum necessary traffic and protect diagnostic output.
- Verify the fix with the same test that reproduced the issue, then document the result.
