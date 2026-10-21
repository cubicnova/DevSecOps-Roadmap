# Networking Fundamentals — Practical Exercises

Use your own Linux VM, local lab, or an explicitly authorized environment. Record commands, observations, and explanations in a lab notebook.

## Exercise 1 — Interface inventory

Run:

```bash
ip address show
```

Record each interface name, state, IPv4 address (if present), and IPv6 address (if present). Identify the loopback interface.

**Deliverable:** a short interface inventory with sensitive addresses redacted before publishing.

## Exercise 2 — Routing table

Run:

```bash
ip route show
ip -6 route show
```

Identify the default route, outgoing interface, and any directly connected routes. Explain how a more-specific route can take precedence over a default route.

**Deliverable:** annotated route-table notes.

## Exercise 3 — Neighbor table

1. Run `ip neigh show`.
2. Generate traffic to your local gateway or another device you own.
3. Run the command again.
4. Describe any changes in neighbor entries and states.

**Deliverable:** before-and-after notes. Do not attempt ARP spoofing.

## Exercise 4 — DNS investigation

Use `getent hosts example.com` and, if available, `dig example.com`, `dig A example.com`, and `dig AAAA example.com`.

Explain the difference between a hostname, a DNS resolver, and an IP address. Note that answers can vary by resolver and time.

**Deliverable:** a DNS lookup summary with the query type and observed result.

## Exercise 5 — HTTP and HTTPS

Run:

```bash
curl -I http://example.com
curl -I https://example.com
```

Compare status codes and headers. Explain what TLS protects and why HTTPS does not guarantee that a website's content is trustworthy.

**Deliverable:** a short comparison. Do not include cookies, authorization headers, or other secrets.

## Exercise 6 — TCP/UDP and listening ports

Run:

```bash
ss -tuln
```

Find examples of TCP and UDP sockets. If no listening services are shown, explain why that may be normal for a workstation.

**Deliverable:** list three observed or researched services and their typical transport/port.

## Exercise 7 — IPv4 subnet calculations

Calculate network address, broadcast address, usable host range, and total addresses for:

1. `192.168.20.0/24`
2. `10.10.8.0/23`
3. `172.16.5.64/26`

For each, show how the prefix length determines the number of host bits.

**Deliverable:** a completed subnet table.

## Exercise 8 — Basic packet capture

On your own device, capture up to 20 packets:

```bash
sudo tcpdump -ni any -c 20
```

If appropriate, repeat with a narrow filter such as `port 53`. Identify source/destination addresses, protocol, and port where visible.

**Deliverable:** observations only. Do not upload raw captures if they could contain private data.

## Exercise 9 — Troubleshooting scenario

A browser cannot load `https://example.com`. Use the following sequence and record what each step tells you:

```bash
ip address
ip route
getent hosts example.com
curl -I --connect-timeout 5 https://example.com
```

If a command fails, state at least two possible causes rather than assuming a single cause.

**Deliverable:** a short decision tree and findings.

## Exercise 10 — Network security design

Design a small three-tier service with:
- public-facing web tier;
- private application tier;
- private database tier.

Describe which connections should be allowed and which should be denied. Apply least privilege: the database should not be directly reachable from the internet.

**Deliverable:** a simple diagram and a table of source, destination, port/protocol, and justification.

## Review questions

1. What is the difference between a MAC address and an IP address?
2. Why are TCP and UDP different?
3. What does a default gateway do?
4. Why can DNS work while an HTTPS connection still fails?
5. What does a `/26` prefix mean?
6. Why does a failed ping not prove a service is offline?
7. What kinds of sensitive information can packet captures contain?
