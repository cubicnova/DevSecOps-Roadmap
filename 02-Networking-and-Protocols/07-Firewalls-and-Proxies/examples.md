# Firewalls and Proxies — Examples

Commands and configuration differ by distribution and product. Inspect the existing policy before changing it. Use a disposable lab or an approved maintenance window for changes.

## 1. Inspect Linux firewall state

Depending on the system, one or more of these commands may be available:

```bash
sudo nft list ruleset
sudo ufw status verbose
sudo iptables -S
```

Do not assume that an empty output from one tool means no firewall exists; another framework, cloud security group, or upstream network device may enforce policy.

## 2. Understand a narrow allow rule

A policy might permit HTTPS from a trusted client network to a web service while denying unrelated inbound traffic. The exact syntax depends on the firewall system. Before writing a rule, identify:
- interface and address family;
- source and destination ranges;
- transport protocol and port;
- connection state;
- rule order and default policy;
- logging requirements and rollback plan.

Avoid copying rules into a production host without adapting and testing them.

## 3. Check listening services

```bash
ss -tuln
```

This shows local TCP/UDP listening sockets. A service listening on `0.0.0.0` or `::` may be bound to all local interfaces, depending on the system. A listening socket does not necessarily mean it is reachable through the firewall.

## 4. Inspect proxy environment variables

```bash
env | grep -i proxy
```

Common variable names include `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` (case handling depends on the client). Environment variables can route command-line traffic through a proxy. Do not publish values if they include credentials.

## 5. Make an HTTP request

```bash
curl -I https://example.com
```

To see connection details:

```bash
curl -vI --connect-timeout 5 https://example.com
```

Verbose output can reveal hostnames, proxy use, and certificate details. Review it before sharing.

## 6. Test through an explicitly configured proxy

For an approved proxy:

```bash
curl -I --proxy http://proxy.example.internal:3128 https://example.com
```

Replace the example proxy with one you are authorized to use. Do not put proxy passwords in shell history. Prefer an approved credential mechanism if authentication is required.

## 7. Understand forward-proxy flow

```text
Client -> Forward Proxy -> Destination Service
          policy/logging
```

The proxy can apply egress policy, authentication, content controls, and logging. If HTTPS is passed through using CONNECT, the proxy may see connection metadata but not necessarily the encrypted application content. TLS inspection changes the trust and privacy model and must be explicitly authorized and managed.

## 8. Understand reverse-proxy flow

```text
Client -> Reverse Proxy -> Backend Application
          TLS/routing          private network
```

A reverse proxy can terminate TLS, route by hostname/path, apply request limits, and forward requests to backend services. Protect the backend so clients cannot bypass the proxy's intended controls.

## 9. Troubleshoot a blocked connection

For a service you are authorized to test:

```bash
ip route
ss -tuln
curl -vI --connect-timeout 5 https://example.com
```

Check DNS, routing, service health, host firewall, network firewall/security groups, proxy configuration, and TLS validation. Use firewall logs where authorized. A timeout, connection refusal, DNS error, and certificate error point to different layers.

## 10. Rule review checklist

Before approving a rule, answer:
- What business/service need does it support?
- Which source and destination are necessary?
- Which protocol and port are required?
- Is the rule inbound or outbound?
- Is there a narrower scope?
- Who owns it and when should it be reviewed?
- What logs and alerts are appropriate?
- How will the change be rolled back?
