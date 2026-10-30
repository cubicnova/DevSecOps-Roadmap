# Examples — Ports and Protocols

Run examples only against your own systems or approved targets. Port numbers are conventions; verify the actual service before making conclusions.

## 1. List listening TCP sockets (Linux)

```bash
ss -lnt
```

This displays listening TCP sockets with numeric addresses and ports. A listener bound to `127.0.0.1` is reachable only from the local host through that loopback address; it is not directly listening on all network interfaces.

## 2. List listening UDP sockets (Linux)

```bash
ss -lnu
```

UDP does not have TCP-style connection state, so a UDP endpoint is commonly shown as bound rather than “listening” in the TCP sense.

## 3. Show process details for sockets

```bash
sudo ss -lntup
```

Use this to correlate listening endpoints with process information. Access to process details may require elevated privileges.

## 4. Check established TCP connections

```bash
ss -tn state established
```

This is a snapshot. A connection can appear or disappear between checks, and local firewall/NAT state may not be visible from this command alone.

## 5. Test a TCP port on an approved host

```bash
nc -vz -w 3 example.com 443
```

- `-v`: verbose
- `-z`: connection check without sending application data
- `-w 3`: timeout in seconds (behavior can vary by implementation)

A successful connection only shows that TCP connection establishment worked at that moment.

## 6. Use Windows PowerShell

```powershell
Test-NetConnection example.com -Port 443
```

Review `TcpTestSucceeded`, resolved address, and route information. This tests TCP connectivity, not full HTTPS health.

## 7. Inspect local service process (Linux)

```bash
sudo ss -lntup
systemctl --type=service --state=running
```

Correlate the port, process, and service unit. Do not stop or disable a service based only on its port number.

## 8. Find the process for a listening port (Linux)

```bash
sudo lsof -nP -iTCP:8080 -sTCP:LISTEN
```

Requires `lsof`. If no output appears, the process may not be listening on that port, or the tool may lack permission or be unavailable.

## 9. Check DNS resolution

```bash
getent hosts example.com
```

Alternative:

```bash
dig example.com
```

A DNS result gives an address/record, not proof that a particular TCP or UDP port is reachable.

## 10. Compare HTTP and TCP checks

```bash
nc -vz -w 3 example.com 443
curl -I --max-time 10 https://example.com/
```

If TCP succeeds but curl fails, inspect TLS negotiation, certificate validation, proxy settings, HTTP response, and server behavior.

## 11. Check a local firewall without changing it

```bash
sudo ufw status verbose
sudo nft list ruleset
```

Use the tool configured on your system. A host firewall is only one part of the path; cloud security groups, network ACLs, routers, and upstream firewalls may also filter traffic.

## 12. Inspect common port mappings

| Service | Common port(s) | Transport |
|---|---:|---|
| SSH | 22 | TCP |
| DNS | 53 | UDP and TCP |
| DHCPv4 | 67/68 | UDP |
| HTTP | 80 | TCP |
| HTTPS (HTTP/1.1, HTTP/2 common deployment) | 443 | TCP |
| HTTP/3 over QUIC | 443 | UDP |
| SMTP submission | 587 | TCP |
| NTP | 123 | UDP |
| RDP | 3389 | TCP/UDP |
| PostgreSQL | 5432 | TCP |
| Redis | 6379 | TCP |

These are common defaults, not proof of what is running on a host.

## 13. Understand source and destination ports

Example TCP flow:

```text
192.0.2.25:53144 -> 198.51.100.10:443
```

- `192.0.2.25`: client IP (documentation range)
- `53144`: illustrative ephemeral client source port
- `198.51.100.10`: server IP (documentation range)
- `443`: destination port commonly used by HTTPS over TCP

The reply reverses the endpoint direction for the connection. NAT may change addresses and ports along the path.

## 14. Interpret failure patterns

| Result | Possible explanations | Next checks |
|---|---|---|
| Name lookup fails | Resolver or hostname issue | DNS configuration, `dig`, resolver logs |
| Connection refused | No listener or active reject | Service status, `ss`, firewall reject |
| Timeout | Dropping, routing, loss, unresponsive host | Route, firewall, security group, endpoint logs |
| TCP works, HTTPS fails | TLS/certificate/application issue | `curl -v`, certificate, server logs |
| Local connection works, remote fails | Bind address or network filtering | Listener address, host and upstream firewalls |

These patterns guide investigation; they do not prove root cause.

## 15. Safe port inventory worksheet

For each listening port, record:

```text
Host:
Port and transport:
Process/service:
Bind address:
Business purpose:
Required source networks:
Authentication/encryption:
Owner:
Exposure risk:
Approved action:
Verification:
```

Never expose a database, cache, remote administration service, or development server simply because it has a familiar port number.
