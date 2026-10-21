# 03 — DNS and DHCP

Learn how DNS translates domain names into records and how DHCP provides hosts with network configuration. These services are foundational to network operations, troubleshooting, and DevSecOps.

## Learning objectives

By the end of this module, you should be able to:

- Explain recursive resolvers, authoritative name servers, zones, caching, TTL, and DNS delegation.
- Recognize common DNS record types: A, AAAA, CNAME, MX, NS, TXT, PTR, SRV, and SOA.
- Use `dig`, `host`, and `getent` to troubleshoot name resolution.
- Explain DHCP discovery, offer, request, and acknowledgement (DORA).
- Identify DHCP scope, lease, reservation, option, relay, and default-gateway concepts.
- Recognize DNS and DHCP security risks and suggest practical mitigations.
- Distinguish a DNS failure from routing, firewall, TLS, or application failure.

## Prerequisites

- Basic networking, IP addressing, routing, and TCP/UDP concepts.
- Linux terminal access is helpful.
- Use only domains, resolvers, and networks you own or are authorized to test.

## DNS essentials

DNS is a distributed naming system. A client may ask a recursive resolver to find an answer; the resolver can use cached data or query other DNS servers. Authoritative name servers provide records for the zones they serve.

Common record types:

| Record | Purpose |
|---|---|
| A | Maps a name to an IPv4 address |
| AAAA | Maps a name to an IPv6 address |
| CNAME | Alias from one name to another name |
| MX | Mail exchanger for a domain |
| NS | Name servers for a zone |
| TXT | Text data, including SPF and domain-verification values |
| PTR | Reverse lookup from an address to a name |
| SRV | Service location and port information |
| SOA | Zone authority and timing metadata |

A DNS TTL controls how long a cached record may be retained. A low TTL can help with planned changes but may increase query volume; it does not guarantee instant global updates.

## DHCP essentials

DHCP automatically supplies configuration such as an IP address, subnet mask/prefix, default gateway, DNS servers, and lease duration.

Typical DHCPv4 DORA sequence:

1. **Discover** — client broadcasts to locate DHCP servers.
2. **Offer** — a server offers a lease and configuration.
3. **Request** — the client requests the offered configuration.
4. **Acknowledge** — the server confirms the lease.

DHCPv4 commonly uses UDP ports 67 (server) and 68 (client). DHCPv6 commonly uses UDP ports 547 (server) and 546 (client). DHCP relay agents can forward requests between subnets.

## Useful commands

```bash
dig example.com A
dig example.com AAAA
dig example.com MX
dig example.com NS
dig +trace example.com
getent hosts example.com
cat /etc/resolv.conf
ip address
ip route
```

For DHCP lease details, file locations vary by distribution and network manager. Use your system's documented network tools and avoid sharing lease files publicly because they can reveal internal network details.

## Lab files

- `README.md` — concepts and reference.
- `examples.md` — practical DNS/DHCP command examples.
- `practical.md` — exercises and scenarios.
- `solutions.md` — sample answers and troubleshooting workflow.

## Security considerations

- Restrict who can administer DNS zones and DHCP servers.
- Use change control, backups, and logging for zone and scope changes.
- Prevent rogue DHCP servers using switch protections where supported, such as DHCP snooping.
- Restrict DNS recursion to intended clients; avoid operating an open recursive resolver.
- Use DNSSEC validation where appropriate to help detect forged DNS data; DNSSEC does not encrypt DNS queries.
- Consider encrypted DNS transports where they fit your threat model and policy.
- Protect zone-transfer access and expose transfers only to authorized secondary servers.
- Monitor unexpected DNS changes, suspicious query patterns, and lease exhaustion.
- Never put passwords, tokens, or other secrets in TXT records.
