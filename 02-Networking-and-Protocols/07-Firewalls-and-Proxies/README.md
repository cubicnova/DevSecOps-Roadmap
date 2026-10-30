# 07 — Firewalls and Proxies

Learn how network firewalls and proxy servers control traffic, enforce security policy, and support visibility across enterprise networks and cloud environments.

## Learning objectives

By completing this module, you should be able to:

- Explain packet-filtering, stateful, application-layer, and next-generation firewalls.
- Distinguish forward proxies, reverse proxies, transparent proxies, and load balancers.
- Understand ingress/egress rules, default-deny policy, NAT, and network segmentation.
- Inspect local firewall state using common Linux tools.
- Explain how HTTP proxies and reverse proxies handle requests.
- Identify firewall and proxy misconfigurations and propose safer rules.
- Troubleshoot blocked traffic methodically without weakening controls unnecessarily.

## Prerequisites

- Basic networking, IP addressing, routing, TCP/UDP, DNS, HTTP/HTTPS, and TLS.
- A Linux VM is recommended for the labs.
- Use only systems and networks you own or are authorized to administer.

## Firewall concepts

A firewall enforces a policy about which traffic may pass between interfaces, hosts, networks, or application contexts.

- **Packet-filtering firewall:** evaluates packet fields such as addresses, protocol, and ports.
- **Stateful firewall:** tracks connection state and evaluates packets in context.
- **Application-layer firewall:** understands application protocols such as HTTP.
- **Next-generation firewall (NGFW):** may combine stateful filtering with application awareness, intrusion prevention, identity, and threat-intelligence features.
- **Host firewall:** controls traffic to and from an individual machine.
- **Network firewall:** enforces policy between network segments or trust zones.

A common baseline is to deny traffic by default and allow only required flows. Exact policies depend on the system's role and operational needs.

## Proxy concepts

- **Forward proxy:** represents clients making requests to external services; often used for egress control, filtering, or caching.
- **Reverse proxy:** receives requests on behalf of backend services; often handles TLS termination, routing, rate limiting, and load balancing.
- **Transparent proxy:** intercepts or redirects traffic without explicit per-client proxy configuration; its behavior and visibility depend on the deployment.
- **Load balancer:** distributes requests or connections across backend instances; it may be implemented by a reverse proxy but is not identical to every proxy.

## Useful Linux commands

Inspect firewall rules (the available tool depends on the system):

```bash
sudo nft list ruleset
sudo ufw status verbose
sudo iptables -S
```

Inspect listening services and routes:

```bash
ss -tuln
ip route
```

Check proxy-related environment variables:

```bash
env | grep -i proxy
```

Test an HTTP endpoint:

```bash
curl -I https://example.com
```

These commands are primarily for inspection. Do not apply firewall changes on a remote host without a recovery path; an incorrect rule can disconnect you.

## Files in this module

- `README.md` — concepts, objectives, and quick reference.
- `examples.md` — rule inspection, proxy examples, and request flow.
- `practical.md` — hands-on exercises and design scenarios.
- `solutions.md` — reference answers and troubleshooting guidance.

## Security best practices

- Apply least privilege: allow only required sources, destinations, protocols, and ports.
- Prefer explicit default-deny rules at trust boundaries.
- Document rule owners, purpose, change date, and review date.
- Avoid broad rules such as “allow any to any” unless a carefully justified temporary exception is approved.
- Restrict firewall administration and review changes.
- Log useful denied/allowed events without overwhelming storage or exposing sensitive payloads.
- Keep proxy software and policy lists updated.
- Protect proxy administration endpoints and backend services from direct unintended access.
- Validate TLS certificates for upstream services; avoid disabling certificate checks.
- Test policy changes in a lab and maintain rollback access.
