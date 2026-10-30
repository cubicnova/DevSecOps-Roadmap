# 09 — Network Segmentation

Network segmentation divides an environment into smaller security zones and controls the traffic allowed between them. It limits unnecessary connectivity, reduces lateral movement opportunities, and helps enforce least privilege across on-premises, cloud, and hybrid environments.

## Learning objectives

By completing this module, you should be able to:

- Explain physical, logical, VLAN-based, subnet-based, and software-defined segmentation.
- Distinguish segmentation from network isolation and microsegmentation.
- Design trust zones for users, servers, applications, databases, management, and guests.
- Define inter-zone traffic policies using source, destination, protocol, port, and business purpose.
- Understand how routers, firewalls, ACLs, security groups, and network policies enforce boundaries.
- Identify common segmentation mistakes and test policy intent.
- Describe how segmentation reduces blast radius without replacing endpoint security or identity controls.

## Core concepts

- **Segment:** A logical or physical portion of a network.
- **Trust zone:** A group of systems with similar security requirements.
- **VLAN:** A Layer 2 logical broadcast domain.
- **Subnet:** An IP address range used for Layer 3 addressing and routing.
- **ACL:** An access control list that permits or denies traffic based on defined criteria.
- **Microsegmentation:** Fine-grained controls between workloads, often at the host, hypervisor, or workload identity layer.
- **DMZ:** A zone for services that need controlled access from less-trusted networks, often including public-facing services.
- **East-west traffic:** Traffic between internal workloads.
- **North-south traffic:** Traffic entering or leaving an environment.
- **Blast radius:** The scope of impact when an account, workload, or system is compromised.

A VLAN alone is not a complete security boundary. Routing, trunk configuration, firewall policy, identity, and management access all affect whether segmentation is effective.

## Example trust zones

| Zone | Example assets | Typical policy goal |
|---|---|---|
| Internet edge / DMZ | Public web endpoints, reverse proxies | Permit only required public service ports |
| Application | Application servers and APIs | Accept traffic only from approved upstream systems |
| Data | Databases and storage | Permit only required application-to-data flows |
| User | Employee endpoints | Restrict direct access to sensitive server networks |
| Management | Admin workstations, bastions | Allow controlled administrative access |
| Guest / IoT | Guest devices, printers, IoT | Isolate from corporate and sensitive systems |
| Security monitoring | SIEM collectors and sensors | Permit narrowly scoped telemetry and administration |

## Segmentation design workflow

1. Inventory assets, owners, data sensitivity, and communication dependencies.
2. Group systems by business function and trust level.
3. Identify required flows, including source, destination, protocol, port, and direction.
4. Define default-deny boundaries and explicit allow rules.
5. Implement controls with VLANs, routing ACLs, firewalls, security groups, or workload policies.
6. Test permitted and prohibited paths.
7. Monitor denies and unexpected flows; update rules through change control.
8. Review zones and rules periodically as services change.

## Useful tools and commands

```bash
ip address
ip route
ip neigh
ss -tuln
sudo nft list ruleset
sudo ufw status verbose
```

For cloud environments, inspect security groups, network ACLs, route tables, and workload network policies using the provider's approved tooling.

## Files in this module

- `README.md` — core concepts and design workflow.
- `examples.md` — sample architectures, flow matrices, and inspection commands.
- `practical.md` — hands-on design and validation exercises.
- `solutions.md` — example answers and policy guidance.

## Security principles

- Start with explicit requirements and deny unneeded inter-zone traffic.
- Apply least privilege to both ingress and egress.
- Keep management planes separate from user and public service networks.
- Restrict direct database access to approved application or administration paths.
- Use identity-aware controls where practical; IP-based rules alone may not be enough.
- Log and review important policy changes and denied traffic.
- Test segmentation from both allowed and disallowed vantage points.
- Avoid broad exceptions that silently undermine zone boundaries.
