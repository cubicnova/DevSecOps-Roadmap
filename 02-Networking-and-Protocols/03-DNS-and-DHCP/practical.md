# DNS and DHCP — Practical Exercises

Use a lab VM, your own test domain, or a network for which you have explicit permission. Do not change production DNS zones or DHCP scopes as a learning exercise.

## Exercise 1 — DNS record inventory

Run the following queries and record the result and TTL where shown:

```bash
dig example.com A
dig example.com AAAA
dig example.com NS
dig example.com MX
dig example.com SOA
```

Explain what each record type is used for. If no record appears in the answer section, note that rather than assuming the domain is invalid.

## Exercise 2 — Resolver comparison

Query your system resolver and one approved alternative:

```bash
dig example.com
dig @1.1.1.1 example.com
```

Compare returned addresses, TTLs, and response status. If direct external DNS queries are blocked or prohibited, document that restriction and use your approved internal resolver.

## Exercise 3 — Trace delegation

Run:

```bash
dig +trace example.com
```

Identify the root, top-level-domain, and authoritative stages. Explain how delegation connects a parent zone to child-zone name servers.

## Exercise 4 — System resolver path

Run:

```bash
getent hosts example.com
cat /etc/resolv.conf
```

If available, also run `resolvectl status`. Explain why system-level name resolution may differ from a direct `dig` query.

## Exercise 5 — DNS caching and TTL

1. Query a record twice and note the TTL.
2. Explain why the TTL may decrease in a cached response.
3. Describe why changing a record does not guarantee every client sees the new value immediately.

Do not change records on a domain you do not control.

## Exercise 6 — DNS troubleshooting scenario

A user reports that a website cannot be reached by name but may be reachable by IP. Use:

```bash
getent hosts example.com
dig example.com
ip route
curl -I --connect-timeout 5 https://example.com
```

Write down what each test establishes and at least two possible explanations for a failure. Do not bypass certificate validation to make the test pass.

## Exercise 7 — DHCP configuration inventory

Run the commands appropriate for your system:

```bash
ip address
ip route
nmcli device show
```

If NetworkManager is not installed, use the tools available on your distribution. Identify the configured address, prefix, default gateway, and DNS servers if visible.

**Safety:** do not run `dhclient -r`, disconnect interfaces, or restart networking on a remote system unless you have a recovery path.

## Exercise 8 — DHCP DORA diagram

Draw the Discover, Offer, Request, and Acknowledge flow. Label client/server UDP ports and explain the role of a relay agent when the client and server are on different subnets.

## Exercise 9 — DNS security review

Create a checklist for a hypothetical organization:
- Who may edit DNS records?
- Are zone transfers restricted?
- Is recursion limited to intended clients?
- Are DNS changes logged?
- Is DNSSEC validation enabled where appropriate?
- Are suspicious query spikes monitored?

Do not attempt zone transfers or configuration changes against third-party systems.

## Exercise 10 — DHCP security design

Describe how to reduce the risk of a rogue DHCP server on a managed LAN. Include switch controls such as DHCP snooping where supported, access controls for network equipment, monitoring, and a plan for legitimate DHCP relay.

## Review questions

1. What is the difference between a recursive resolver and an authoritative server?
2. What does a DNS TTL represent?
3. What is the purpose of a CNAME record?
4. What are the four DHCPv4 DORA stages?
5. Which UDP ports are commonly used by DHCPv4 clients and servers?
6. Why does DNSSEC not provide DNS query confidentiality?
7. What can cause `dig` and `getent` to return different results?
8. Why can renewing a DHCP lease be risky over a remote connection?
