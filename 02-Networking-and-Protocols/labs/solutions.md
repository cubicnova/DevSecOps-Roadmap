# Networking and Protocols Labs — Solutions

These are reference explanations, not fixed expected outputs. Results vary by OS, resolver, routing policy, network controls, and target availability.

## Lab 01 — Interface and route discovery

Useful commands:

```bash
ip -br link
ip -br address
ip route
ip route get 1.1.1.1
ss -lntup
```

- `ip -br link` summarizes interface state.
- `ip -br address` shows configured addresses.
- `ip route` displays the routing table.
- `ip route get` shows the selected route for one destination.
- `ss -lntup` shows listening TCP/UDP sockets and may require elevated privileges to show process details.

A configured IP address does not guarantee connectivity: the interface may be down, the route may be missing, a gateway may be unreachable, or a firewall may block traffic.

## Lab 02 — DNS lookup investigation

`getent hosts` uses the operating system's configured name-service path. `dig` queries DNS and allows inspection of record types and resolvers. Results may differ because of local caching, search domains, split-horizon DNS, VPN configuration, or the resolver chosen.

- **NXDOMAIN:** the queried DNS view reports that the name does not exist.
- **SERVFAIL:** the resolver could not complete processing successfully.
- **Timeout:** no response arrived within the wait period; possible causes include filtering, packet loss, or an unavailable resolver.

A public resolver may not know internal corporate records and can bypass required DNS policy.

## Lab 03 — TCP ports and listeners

While the demo server runs, port 18080 should normally accept connections on loopback. Port 18081 should commonly be refused if nothing is listening.

- `ss -lntp` helps confirm a listener.
- `nc -vz -w 3` tests whether a TCP connection can be established.
- `curl` checks the HTTP service response, not just TCP reachability.

A refusal usually indicates an explicit rejection; a timeout means the connection did not succeed before the deadline. UDP has no TCP-style handshake, so a missing UDP reply is often inconclusive.

## Lab 04 — HTTP and HTTPS

`curl -D -` prints response headers, while `curl -v` gives more connection and TLS detail. `openssl s_client` can show certificate-chain and handshake information.

Possible TLS problems include:
- Expired certificate or incorrect system time.
- Hostname mismatch or incomplete certificate chain.
- Unsupported TLS protocol/cipher or a proxy-interception issue.

Do not permanently disable certificate verification. Fix the certificate, hostname, trust configuration, or protocol mismatch responsible for the failure.

## Lab 05 — Path, latency, and loss

Ping measures ICMP round-trip time; it does not directly measure full application latency. `tracepath`, `traceroute`, and `mtr` rely on diagnostic probes that some routers filter or rate-limit.

Loss reported at one intermediate hop but not at later hops can mean that the intermediate router deprioritizes its own replies while forwarding normal traffic. Compare end-to-end tests and the actual application before identifying a failing hop.

- **Latency:** time for a packet/request to travel and return.
- **Jitter:** variation in latency.
- **Packet loss:** probes or packets not observed at the expected point.
- **Throughput:** amount of data transferred per unit time.

## Lab 06 — Packet capture

A command such as:

```bash
sudo tcpdump -i <interface> -nn -c 100 port 53
```

collects up to 100 matching packets on the selected interface. A DNS query triggered with `dig` may appear with its response if the traffic is visible on that interface.

No packets may appear because the wrong interface was selected, the resolver answered from cache, DNS is encrypted, or the filter did not match the actual traffic. Do not broaden collection without a clear reason and authorization.

Captures can expose internal hostnames, addresses, timing, and potentially application data. Use minimal filters, restricted permissions, limited retention, and redaction before sharing.

## Lab 07 — Firewall and proxy review

Proxy variables can cause CLI requests to use a proxy while other applications use a different route. Firewall rules are only one part of the path; cloud security groups, network ACLs, remote firewalls, routing, and application listeners can also affect access.

A safe firewall request names the source, destination, protocol, port, business justification, owner, and review/expiry date. Do not flush rules or disable security controls as a first response.

## Lab 08 — NGINX load balancer

Both Python backends should answer directly on loopback ports 18081 and 18082. NGINX listens on 127.0.0.1:18080 and forwards requests to the upstream pool.

Useful checks:

```bash
curl -i http://127.0.0.1:18081/
curl -i http://127.0.0.1:18082/
curl -i http://127.0.0.1:18080/
sudo nginx -t
```

If the proxy returns `502`, check whether the backends are running, whether the ports match the config, and what the NGINX error log says. Stop one backend only for the controlled exercise; some failed requests may occur before passive failure handling changes selection. Basic open-source NGINX upstream behavior should not be assumed to provide every active health-check feature.

After the lab, remove only the dedicated lab configuration, validate the remaining NGINX configuration, reload safely, and stop both Python servers.

## Lab 09 — Troubleshooting scenario

Possible hypotheses include:
1. **DNS inconsistency:** the affected host resolves to an unexpected address. Compare OS resolver output and DNS records.
2. **Route or VPN issue:** the hostname resolves but the selected route differs. Inspect `ip route get` and compare the known-good path.
3. **TCP filtering or service issue:** port 443 times out or is refused. Check permitted connection tests, listeners, and relevant firewall/service logs.
4. **TLS identity or chain problem:** TCP succeeds but TLS fails. Inspect certificate identity, dates, chain, and system time.
5. **Intermittent backend/proxy failure:** TLS may succeed but HTTP returns 502/504 or latency spikes. Correlate timestamps with proxy and backend logs.

The next step should be based on the first reproducible failure and should avoid unnecessary configuration changes.

## Lab 10 — Incident report rubric

A strong report:
- Defines impact and timeline clearly.
- Separates observed facts from hypotheses.
- Includes commands and sanitized evidence.
- Names a root cause only when evidence supports it.
- Documents the approved fix and rollback.
- Verifies recovery using the original failing test.
- Lists a small number of prevention actions tied to the confirmed cause.

## Cleanup checklist

- Stop local demo services with `Ctrl+C`.
- Remove the dedicated lab configuration only after verifying its path.
- Validate NGINX configuration before reloading.
- Delete packet captures according to your organization's retention policy.
- Redact secrets, cookies, and private host details before publishing lab evidence.
