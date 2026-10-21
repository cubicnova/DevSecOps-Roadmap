# Firewalls and Proxies — Reference Solutions

These are example answers. The correct policy depends on application architecture, business requirements, and the network controls already in place.

## Exercise 1 — Firewall inventory

`nft`, `ufw`, and `iptables` are different interfaces or frameworks that may be used depending on the distribution and configuration. A host can have multiple enforcement layers, including cloud security groups, network ACLs, appliances, and Kubernetes policies. Inspect the actual active path rather than assuming one command shows every control.

## Exercise 2 — Listening sockets

`ss -tuln` lists local listening TCP and UDP sockets. Evaluate whether each service needs to listen on all interfaces or can bind to loopback or a private interface. Reachability also depends on routing, host firewall, upstream controls, and service-level authentication.

## Exercise 3 — Default-deny policy

A reasonable conceptual policy:
- Allow inbound TCP 443 from intended clients to the web service.
- Allow SSH only from a trusted management range or approved access gateway.
- Allow necessary outbound DNS, time synchronization, and updates to approved destinations.
- Deny unrelated inbound traffic by default.
- Log security-relevant denials with rate limits and monitor rule changes.

Use the actual required sources and destinations. Avoid assuming every server needs the same outbound access.

## Exercise 4 — Rule hygiene

An unrestricted allow rule provides no meaningful segmentation and can enable unintended exposure. Replace it with specific source/destination ranges, protocol, port, direction, business justification, owner, review date, and appropriate logging. Remove temporary exceptions when they expire.

## Exercise 5 — Proxy configuration

Proxy variables may affect tools that honor them, but not every application uses environment variables. Inspect values carefully and redact credentials or tokens. Explicit proxy configuration should use an approved endpoint and credential mechanism.

## Exercise 6 — Direct versus proxied requests

A proxy may deny destinations, require authentication, resolve names differently, or use a different egress route. Direct and proxied status codes can differ. Use the proxy configured by your organization; do not attempt to bypass it.

## Exercise 7 — Reverse-proxy architecture

Clients should reach the reverse proxy on approved listener ports. The proxy should reach backend instances only on required application ports. Backends should be on a private network and accept traffic only from the proxy or approved internal callers. Management endpoints should be separately restricted.

## Exercise 8 — Troubleshooting sequence

1. Confirm the service is running and listening on the expected interface/port.
2. Check host firewall policy and local logs.
3. Verify DNS and route selection.
4. Review upstream firewall, ACL, and security-group rules in both directions.
5. Check proxy configuration, TLS trust, hostname, and certificate expiry.
6. Correlate timestamps across application and network logs.

A local request succeeding does not prove that remote routing or ingress policy is correct.

## Exercise 9 — Logging and monitoring

Useful events include repeated denied connections, unusual outbound destinations, administrative policy changes, proxy authentication failures, anomalous request rates, and unexpected backend exposure. Avoid logging passwords, authorization headers, cookies, full sensitive payloads, or other secrets. Define retention and access controls for logs.

## Exercise 10 — Change-management plan

A safe plan records the current state, exact proposed change, expected impact, reviewer, test plan, maintenance window if needed, out-of-band access, rollback command/procedure, and post-change verification. Test in a lab first and ensure rollback is possible if the connection drops.

## Review questions

1. A stateful firewall tracks connection state; a stateless filter evaluates each packet against rules without the same connection context.
2. A forward proxy acts on behalf of clients; a reverse proxy receives requests on behalf of servers.
3. Default-deny limits exposure by allowing only explicitly approved traffic.
4. A firewall, route, security group, interface binding, or service-level control can block reachability.
5. TLS termination means the proxy negotiates TLS with the client and may create a separate connection to the backend.
6. TLS inspection can expose sensitive content, requires managed trust, and raises privacy, compliance, and key-security concerns.
7. Shell history can persist credentials and may be readable by other processes or users with access.
8. Rollback should restore a known-good policy and preserve a way to regain access, ideally through tested console or out-of-band access.
