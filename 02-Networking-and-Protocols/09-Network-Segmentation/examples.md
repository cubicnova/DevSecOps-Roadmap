# Network Segmentation — Examples

These are design and inspection examples. Adapt all address ranges and policies to your own lab. Do not apply example firewall rules to production without review.

## 1. Example three-tier architecture

```text
Internet
   |
[Edge Firewall]
   |
[DMZ: Reverse Proxy]
   | TCP 8443 (example application port)
[Application Zone]
   | TCP 5432 (example PostgreSQL port)
[Database Zone]
```

Intent:
- Internet clients can reach the reverse proxy only on the required public service port.
- The reverse proxy can reach application instances only on the configured application port.
- Application instances can reach the database only on the database port.
- The database has no direct public route or public inbound rule.
- Administrative access uses a controlled management path.

The ports shown are examples, not universal requirements.

## 2. Example zone and flow matrix

| Source zone | Destination zone | Example allowed flow | Default intent |
|---|---|---|---|
| Internet | DMZ | TCP 443 to public reverse proxy | Allow required public service only |
| DMZ | Application | App-specific port to approved backends | Allow narrowly |
| Application | Data | TCP 5432 to approved database | Allow narrowly |
| User | Data | No direct database access | Deny |
| Guest | Corporate | No access | Deny |
| Management | Managed servers | Approved SSH/RDP/admin ports | Allow from managed admin hosts |
| Workloads | Management | No general initiation | Deny by default |

Always document the business owner, source/destination scope, and review date for each exception.

## 3. Inspect local addressing and routes

```bash
ip address show
ip route show
ip neigh show
```

These commands help identify local addresses, routes, and neighbor entries. They do not show the entire network topology or prove that a firewall permits a flow.

## 4. Inspect host firewall policy

```bash
sudo nft list ruleset
sudo ufw status verbose
```

Which command is useful depends on the distribution and active firewall framework. Network firewalls and cloud security groups may add additional enforcement layers.

## 5. Check listening services

```bash
ss -tuln
```

Compare listening ports with the host's intended role. For example, a database server should not expose an administrative interface to all untrusted interfaces unless explicitly required and controlled.

## 6. Validate an allowed path

For a service you own or are authorized to test:

```bash
curl -I --connect-timeout 5 https://service.example.internal
```

Use the actual approved hostname and port. A successful request validates only that specific path and application exchange, not the entire segmentation design.

## 7. Validate a prohibited path

From a test host in a zone that should not reach the database, attempt a normal connection to the documented database endpoint only with authorization. Record whether it is denied and correlate the timestamp with firewall logs. Do not scan broad ranges or probe systems outside the approved test scope.

## 8. Cloud segmentation considerations

Review these layers together:
- subnet and route-table associations;
- security groups or workload firewall policies;
- network ACLs;
- public IP assignments and internet gateways;
- peering, transit gateway, VPN, and private endpoint paths;
- management-plane permissions and logs.

A subnet being called “private” does not by itself prove that it is isolated. Effective routing and policy determine reachability.

## 9. Microsegmentation example

Instead of allowing every application server to reach every other application server, define explicit workload relationships:

```text
frontend -> API: TCP 8443
API -> database: TCP 5432
monitoring agent -> collector: approved telemetry port
all other workload-to-workload traffic: deny unless required
```

Use real ports and identities from your architecture. Include service discovery, health checks, backup traffic, and management flows where needed.

## 10. Troubleshooting checklist

When a legitimate flow fails:
1. Confirm source/destination addresses and ports.
2. Check local routes and DNS.
3. Confirm the destination service is listening.
4. Inspect host firewall, network firewall, ACL, and security-group rules.
5. Check return routing and stateful inspection behavior.
6. Review logs and policy order.
7. Make a narrow change, test, and document the result.
