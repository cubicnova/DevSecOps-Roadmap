# Network Segmentation — Practical Exercises

Complete these exercises using a lab network or a design-only scenario. Only test connectivity to systems you own or have explicit permission to assess.

## Exercise 1 — Asset classification

Create an inventory of at least 10 fictional or lab assets. Include hostname, owner, business function, sensitivity, environment, and required communication partners.

**Deliverable:** an asset inventory grouped into trust zones.

## Exercise 2 — Draw a segmented architecture

Design a network with:
- public reverse proxy;
- application servers;
- database;
- employee endpoints;
- guest Wi-Fi;
- management/bastion host;
- centralized logging.

Show the security boundaries and label the intended traffic paths.

## Exercise 3 — Build a flow matrix

For each required communication path, record:
- source zone and workload;
- destination zone and workload;
- protocol and port;
- direction;
- business justification;
- owner;
- review/expiry date.

Include at least five allowed flows and five denied flows.

## Exercise 4 — Identify excessive access

Review this fictional policy: “All internal subnets can reach every server on all ports.”

Explain at least four risks and propose narrower rules based on actual service dependencies.

## Exercise 5 — Inspect a Linux host

Run:

```bash
ip address
ip route
ss -tuln
sudo nft list ruleset
```

If a command is unavailable, record which tool your distribution uses instead. Identify the host's interfaces, listening ports, and local filtering policy where visible.

**Deliverable:** a redacted configuration summary.

## Exercise 6 — Test a boundary

In an authorized lab, choose one flow that should be allowed and one that should be denied. Test each from the correct source zone and record results. Correlate the denied test with logs if available.

Do not change production rules or probe unrelated hosts.

## Exercise 7 — Cloud network review

For a sample VPC/VNet, inspect subnets, route tables, security groups, network ACLs, public IPs, and peering/VPN routes. Explain how a path might remain reachable despite a subnet being labeled “private.”

## Exercise 8 — Microsegmentation design

Design rules for three workloads: frontend, API, and database. Include required application flows, monitoring, backups, and management. Deny unrelated east-west traffic by default.

## Exercise 9 — Incident containment plan

A workload is suspected to be compromised. Describe how segmentation could restrict its access while preserving required evidence, monitoring, and recovery paths. Include approval and rollback considerations.

## Exercise 10 — Segmentation verification plan

Write a test plan covering:
- positive tests for required flows;
- negative tests for prohibited flows;
- IPv4 and IPv6 paths where enabled;
- alternate routes and VPN/peering paths;
- logging and alert generation;
- documentation and change approval.

## Review questions

1. Why is a VLAN alone not necessarily a security boundary?
2. What is the difference between north-south and east-west traffic?
3. Why should databases usually avoid direct public access?
4. What is microsegmentation?
5. Why should both allowed and denied paths be tested?
6. What can make a “private” cloud subnet reachable?
7. How does segmentation help limit lateral movement?
8. What should be documented for each firewall exception?
