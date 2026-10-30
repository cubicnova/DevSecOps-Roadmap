# Firewalls and Proxies — Practical Exercises

Perform exercises in a local VM or an environment you are authorized to administer. Avoid applying rules to a remote system unless you have console access or a tested recovery method.

## Exercise 1 — Firewall inventory

Run whichever commands are available:

```bash
sudo nft list ruleset
sudo ufw status verbose
sudo iptables -S
```

Identify the active firewall framework if possible. Explain why a cloud security group or upstream firewall might still affect connectivity.

**Deliverable:** a short inventory with sensitive internal addresses redacted.

## Exercise 2 — Listening sockets

Run:

```bash
ss -tuln
```

Choose three listening sockets or explain why your system has few. For each, identify protocol, port, and whether the service should be reachable from other hosts.

**Deliverable:** a service exposure table.

## Exercise 3 — Design a default-deny policy

For a simple web server, specify inbound and outbound rules for:
- public HTTPS access;
- SSH administration from a trusted management range;
- DNS and time synchronization as required;
- application updates;
- all other traffic by default.

Do not apply the rules until reviewed and tested.

## Exercise 4 — Rule hygiene review

Review a fictional rule: “Any source → any destination → any port → allow.”

Explain why it is risky and propose a least-privilege replacement. Include the service owner, purpose, expiry/review date, and logging needs.

## Exercise 5 — Proxy configuration

Run:

```bash
env | grep -i proxy
```

If a proxy is configured, document its presence without publishing credentials. If not, explain how a command-line client can be given an approved proxy explicitly with `curl --proxy`.

## Exercise 6 — Compare direct and proxied requests

If your organization provides an approved proxy, compare:

```bash
curl -I https://example.com
curl -I --proxy http://proxy.example.internal:3128 https://example.com
```

Record only status, timing, and relevant non-sensitive errors. Do not bypass policy or attempt to evade monitoring.

## Exercise 7 — Reverse-proxy architecture

Draw a simple flow with client, reverse proxy, and two backend instances. Mark where TLS terminates, where access logs are generated, and which network paths should be blocked.

**Deliverable:** a diagram and a short explanation of how direct backend access is prevented.

## Exercise 8 — Troubleshooting scenario

An application works from the server but not from a remote client. Create a diagnostic sequence that checks:
1. application listening address and port;
2. local host firewall;
3. routing and DNS;
4. network firewall/security groups;
5. proxy and TLS settings;
6. logs and return traffic.

For each step, state what a success or failure indicates.

## Exercise 9 — Logging and monitoring

Define a minimal set of firewall/proxy events to monitor: repeated denied connections, unexpected egress, policy changes, authentication failures, and unusual request rates. Explain how to avoid logging credentials or sensitive request bodies.

## Exercise 10 — Change-management plan

Write a safe firewall change plan including pre-checks, proposed rule, peer review, test cases, rollback steps, and a verification window.

## Review questions

1. What is the difference between a stateful firewall and a stateless packet filter?
2. How does a forward proxy differ from a reverse proxy?
3. Why is default-deny useful?
4. Why can a listening service still be unreachable?
5. What does a reverse proxy do during TLS termination?
6. What risks are introduced by TLS inspection?
7. Why should proxy credentials not be stored in shell history?
8. What should a firewall change rollback plan include?
