# Networking Fundamentals — Reference Solutions

These are example answers. Your interface names, routes, DNS responses, and socket listings will depend on your environment.

## Exercise 1 — Interface inventory

- `lo` is the loopback interface.
- `127.0.0.1` is the IPv4 loopback address.
- `::1` is the IPv6 loopback address.
- Other interface names depend on the operating system and virtual environment.
- An interface marked `DOWN` may be disabled or unused; it is not necessarily a fault.

## Exercise 2 — Routing table

A route specifies a destination prefix and where to send matching traffic. A default route is used when no more-specific route matches. Route selection commonly prefers the most-specific matching prefix, with other routing metrics and policy rules also relevant.

Example:

```text
default via 192.168.1.1 dev eth0
192.168.1.0/24 dev eth0 proto kernel scope link
```

The first route is a default path through the gateway. The second says the local `/24` network is directly connected through `eth0`.

## Exercise 3 — Neighbor table

IPv4 commonly uses ARP to resolve a local IPv4 address to a link-layer address. IPv6 uses Neighbor Discovery. Entries may appear after communication, expire, or show states such as `REACHABLE`, `STALE`, or `INCOMPLETE`.

## Exercise 4 — DNS investigation

- A hostname is a human-readable name such as `example.com`.
- A resolver queries DNS and may cache responses.
- An IP address identifies a network-layer endpoint for routing.
- `A` records provide IPv4 addresses; `AAAA` records provide IPv6 addresses.
- DNS can return multiple addresses, and responses can change with time or resolver policy.

## Exercise 5 — HTTP and HTTPS

HTTP sends application data without TLS protection. HTTPS is HTTP carried over TLS, which can provide confidentiality, integrity, and server authentication when certificate validation succeeds. HTTPS does not guarantee that a site is honest, free of malware, or factually accurate.

## Exercise 6 — TCP/UDP

`ss -tuln` lists local listening TCP and UDP sockets. A workstation may have few or no listening services. Common examples include SSH over TCP 22, DNS over UDP/TCP 53, HTTP over TCP 80, and HTTPS over TCP 443; these are typical defaults, not guarantees.

## Exercise 7 — Subnet calculations

| CIDR | Mask | Total IPv4 addresses | Network | Broadcast | Conventional usable range |
|---|---|---:|---|---|---|
| `192.168.20.0/24` | `255.255.255.0` | 256 | `192.168.20.0` | `192.168.20.255` | `192.168.20.1`–`192.168.20.254` |
| `10.10.8.0/23` | `255.255.254.0` | 512 | `10.10.8.0` | `10.10.9.255` | `10.10.8.1`–`10.10.9.254` |
| `172.16.5.64/26` | `255.255.255.192` | 64 | `172.16.5.64` | `172.16.5.127` | `172.16.5.65`–`172.16.5.126` |

For IPv4, total addresses equal \(2^{32-\text{prefix}}\). The conventional usable host count subtracts the network and broadcast addresses for ordinary multi-access subnets.

## Exercise 8 — Packet capture

Look for packet timestamps, source/destination endpoints, protocol, and ports when decoded. A capture on `any` may use a Linux cooked capture format rather than Ethernet headers. Results depend on which interfaces and traffic are active.

## Exercise 9 — Troubleshooting scenario

A useful interpretation sequence:

1. `ip address`: check that an appropriate interface has an address.
2. `ip route`: check that a route exists.
3. `getent hosts`: check whether the system can resolve the hostname.
4. `curl`: test a real HTTPS request and report the connection/HTTP result.

Possible causes include a disabled interface, missing route, DNS resolver issue, firewall rule, remote service outage, TLS/certificate issue, proxy configuration, or a captive portal. One failed command rarely identifies the root cause by itself.

## Exercise 10 — Network security design

Example policy:

| Source | Destination | Allow | Reason |
|---|---|---|---|
| Internet | Web tier | TCP 443 | Public HTTPS access |
| Web tier | Application tier | App-specific port only | Required application traffic |
| Application tier | Database tier | Database port only | Required data access |
| Internet | Database tier | Deny | Prevent direct public database access |
| Web tier | Database tier | Deny by default | Enforce tier boundaries |
| Admin network | Managed hosts | Approved management port | Restricted administration |

Actual ports depend on the application. Add monitoring, identity-aware administration, patching, and carefully scoped outbound rules.

## Review questions

1. MAC addresses are link-layer identifiers used on a local network segment; IP addresses are network-layer addresses used for routing.
2. TCP provides a reliable, ordered byte stream; UDP sends datagrams without TCP's connection and delivery guarantees.
3. A default gateway forwards traffic toward destinations without a more-specific route.
4. DNS and HTTPS are separate stages; TLS negotiation, routing, firewall rules, or the remote service can still fail.
5. `/26` means 26 network bits and 6 host bits in IPv4, giving 64 total addresses per subnet.
6. ICMP can be blocked while other protocols and services still work.
7. Captures can reveal IPs, hostnames, timing, URLs, and potentially sensitive payload data.
