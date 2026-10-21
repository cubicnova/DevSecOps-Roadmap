# DNS and DHCP — Reference Solutions

Answers below are examples; live DNS responses and local DHCP configuration vary by environment and time.

## Exercise 1 — DNS record inventory

- `A`: IPv4 address.
- `AAAA`: IPv6 address.
- `NS`: name servers delegated for the zone.
- `MX`: mail exchangers and their priorities.
- `SOA`: zone metadata, including primary-server and timing fields.

TTL values are expressed in seconds in typical `dig` output. A missing answer for a specific type does not mean the domain does not exist.

## Exercise 2 — Resolver comparison

Different resolvers may return different cached values, use different filtering policies, or receive different answers because of geography, load balancing, or split-horizon DNS. A public resolver may be unreachable due to network policy. In a managed environment, use the resolver authorized by the organization.

## Exercise 3 — Delegation

DNS is hierarchical. Root servers refer queries to top-level-domain servers, which then refer them to the name servers authoritative for the requested zone. Caching can shorten the process for later queries.

## Exercise 4 — System resolver path

`getent` follows the operating system's configured name-service path, which can include `/etc/hosts`, DNS, and other sources. `dig` is a DNS diagnostic client. Resolver configuration may be managed dynamically, so `/etc/resolv.conf` might point to a local stub resolver rather than directly to an upstream server.

## Exercise 5 — Caching and TTL

A resolver may cache a record for up to its TTL. As time passes, a cached response often shows a smaller remaining TTL. After a change, clients may continue to use cached data until it expires; application caches and multiple DNS layers can also affect when the change is observed.

## Exercise 6 — DNS troubleshooting

- `getent hosts`: tests the system name-service path.
- `dig`: tests DNS queries and provides DNS-specific response details.
- `ip route`: helps confirm whether a usable route exists.
- `curl`: tests a real application request and may expose connection or TLS errors.

Possible causes include a resolver outage, incorrect or stale record, local host-file entry, routing issue, firewall rule, remote server outage, TLS failure, proxy configuration, or application error. A successful connection by IP can still fail at TLS or HTTP because hostnames are used for certificate checks and virtual hosting.

## Exercise 7 — DHCP inventory

`ip address` and `ip route` show active configuration, but may not identify its source. NetworkManager's `nmcli device show` can show DHCP-provided fields on systems that use NetworkManager. Other platforms store lease details in different locations.

## Exercise 8 — DORA

Typical DHCPv4 flow:

1. Client → broadcast: DHCP Discover, UDP 68 to 67.
2. Server → client/network: DHCP Offer, UDP 67 to 68.
3. Client → broadcast: DHCP Request, UDP 68 to 67.
4. Server → client/network: DHCP ACK, UDP 67 to 68.

Exact packet delivery can vary with relays, client state, and network configuration. A relay forwards requests between the client subnet and server network.

## Exercise 9 — DNS security review

A reasonable baseline includes role-based administration, multi-factor authentication for management accounts, change review, protected backups, restricted zone transfers, recursion limited to intended clients, logging and alerting, DNSSEC validation where supported, and monitoring for unusual query patterns. DNSSEC helps authenticate DNS data; it does not encrypt queries.

## Exercise 10 — DHCP security design

Use DHCP snooping on supported managed switches, designate trusted uplinks, restrict network-device administration, monitor for unexpected DHCP servers, and document approved relay paths. Test changes in a lab first because an incorrect trust configuration can interrupt legitimate address assignment.

## Review questions

1. A recursive resolver obtains an answer for a client; an authoritative server provides data for the zones it serves.
2. TTL is the duration a DNS record may be cached.
3. CNAME creates an alias from one DNS name to another name.
4. Discover, Offer, Request, Acknowledge.
5. DHCPv4 server UDP 67 and client UDP 68.
6. DNSSEC authenticates DNS data; it does not encrypt query traffic.
7. Local files, NSS configuration, caches, resolver selection, and policy can cause different results.
8. Lease renewal can change address or routing configuration and interrupt the remote session.
