# Network Segmentation — Reference Solutions

These are example answers. Real segmentation policy should be based on a verified asset inventory, service dependencies, business requirements, and the enforcement points in the environment.

## Exercise 1 — Asset classification

Group assets by trust level and function rather than relying only on hostname or location. A useful inventory includes owner, sensitivity, environment, data type, exposed services, and approved communication partners. Review the inventory with service owners before enforcing policy.

## Exercise 2 — Segmented architecture

A reasonable high-level design:
- Internet-facing clients reach only the public reverse proxy on required ports.
- The reverse proxy can reach approved application listeners.
- Application servers can reach only required database endpoints.
- Employee endpoints cannot directly access the database zone by default.
- Guest devices are isolated from corporate and management networks.
- Administrators use a controlled bastion or management network with strong authentication.
- Required logs are sent to a protected monitoring zone.

## Exercise 3 — Flow matrix

Example entries:

| Source | Destination | Flow | Decision | Reason |
|---|---|---|---|---|
| Internet | Reverse proxy | TCP 443 | Allow | Public HTTPS |
| Reverse proxy | API | TCP 8443 | Allow | Backend requests |
| API | Database | TCP 5432 | Allow | Required data access |
| Guest Wi-Fi | Database | Any | Deny | Untrusted guest zone |
| Employee endpoints | Database | Any | Deny by default | Use approved application paths |
| Admin bastion | Managed Linux host | TCP 22 | Allow narrowly | Administration |
| Workload | Management network | Any | Deny by default | Protect management plane |

Ports are examples. Real policy must reflect actual services and should specify precise sources and destinations.

## Exercise 4 — Excessive access

Broad internal access enables lateral movement, expands the impact of compromised endpoints, exposes unnecessary services, and makes monitoring less meaningful. Replace it with service-specific rules and a default-deny inter-zone policy. Include owners, justification, review dates, and logging.

## Exercise 5 — Linux inspection

- `ip address` shows local interface addresses.
- `ip route` shows local route selection.
- `ss -tuln` lists local listening TCP/UDP sockets.
- `nft list ruleset` displays rules when nftables is used and accessible.

These commands provide only a host-level view; upstream firewalls, cloud security groups, routes, and application controls also matter.

## Exercise 6 — Boundary testing

A positive test should confirm that a documented required flow works. A negative test should confirm that a prohibited flow is blocked. Record source, destination, time, protocol/port, result, and matching logs. A timeout alone may not prove which control blocked the traffic, so correlate logs and test the expected service carefully.

## Exercise 7 — Cloud network review

A subnet can have routes through an internet gateway, NAT gateway, peering, VPN, transit gateway, or private endpoint. Security groups, ACLs, host firewalls, and service bindings all affect the final path. Verify effective routes and rules rather than trusting a label such as “private.”

## Exercise 8 — Microsegmentation design

Allow frontend-to-API traffic only on the API listener; allow API-to-database traffic only on the required database port; allow approved monitoring, backup, and administration flows; deny other workload-to-workload traffic by default. Validate health checks and service discovery so that necessary dependencies are not accidentally broken.

## Exercise 9 — Incident containment

Use approved incident-response procedures to isolate the suspected workload or restrict its egress and east-west paths while preserving logs, volatile evidence where required, and a controlled management/forensics path. Coordinate with incident responders and service owners; document changes and ensure recovery/rollback steps are available.

## Exercise 10 — Verification plan

Test each required flow from its actual source and each prohibited flow from relevant untrusted zones. Include IPv4/IPv6, VPN/peering, alternate routes, and both host and network enforcement. Confirm that logs and alerts are generated and retain evidence of results. Obtain approval before changing production policy.

## Review questions

1. VLANs separate Layer 2 broadcast domains, but routing, trunk mistakes, or permissive ACLs can allow cross-zone traffic.
2. North-south traffic crosses the environment's boundary; east-west traffic moves between internal systems.
3. Direct public database access increases exposure and attack surface.
4. Microsegmentation applies fine-grained controls between individual workloads or identities.
5. Positive tests validate required business functions; negative tests validate security boundaries.
6. Routes, gateways, peering, VPNs, public IPs, permissive security groups, or exposed services can create reachability.
7. Segmentation restricts the paths an attacker can use after compromising a host.
8. Document source, destination, protocol, port, direction, purpose, owner, logging, approval, and review/expiry date.
