# Practical Labs — Ports and Protocols

Perform these labs on your own computer, a private lab, or systems you are explicitly authorized to administer. Do not scan public IP ranges or change firewall rules on production systems without approval.

## Lab 1 — Build a port reference table

Create a table with at least 20 common services.

For each entry, include:
- Service name
- Default/common port
- TCP, UDP, or both
- Purpose
- Whether the service commonly needs encryption/authentication
- One exposure risk

Include DNS, DHCP, SSH, HTTP, HTTPS, SMTP, NTP, LDAP, SMB, RDP, and at least three database/cache services.

## Lab 2 — List local listeners

On Linux:

```bash
ss -lnt
ss -lnu
sudo ss -lntup
```

On Windows PowerShell:

```powershell
Get-NetTCPConnection -State Listen
Get-NetUDPEndpoint
```

**Tasks**
1. Record listening TCP and UDP endpoints.
2. Identify process/service names where possible.
3. Note the local bind address.
4. Distinguish loopback-only listeners from listeners on external interfaces.
5. Do not stop services simply because you do not recognize them; investigate ownership and purpose first.

## Lab 3 — Test a known HTTPS port

Use an approved endpoint:

```bash
nc -vz -w 3 example.com 443
curl -I --max-time 10 https://example.com/
```

**Tasks**
1. Record each result.
2. Explain what the `nc` result proves.
3. Explain what additional information curl provides.
4. Identify two reasons one test could succeed while the other fails.

If `nc` is unavailable, use an equivalent approved TCP test tool.

## Lab 4 — Compare TCP and UDP

**Tasks**
1. Explain the delivery guarantees of TCP and UDP.
2. Give three applications commonly associated with TCP and three with UDP.
3. Explain why DNS uses both transports.
4. Explain why TCP 443 and UDP 443 can serve different traffic.
5. State why a UDP scan or test may be inconclusive.

## Lab 5 — Diagnose a refused connection

**Scenario:** A user receives “connection refused” when connecting to a lab web service.

**Tasks**
1. Check whether the service is active.
2. Check whether the expected port is listening.
3. Inspect recent service logs.
4. Verify bind address and port.
5. Identify whether a firewall could be actively rejecting traffic.
6. Propose the safest next test.

Use your own service or a local lab service; do not intentionally interrupt a production application.

## Lab 6 — Diagnose a timeout

**Scenario:** A TCP connection to a server times out.

**Tasks**
1. Verify the hostname resolves to the expected IP.
2. Check the route and destination address.
3. Review host firewall and network ACL/security group policy.
4. Check the service listener from the server side if you have authorization.
5. Explain how timeout differs from refusal.
6. List at least three possible causes without prematurely choosing one.

## Lab 7 — Inspect DNS behavior

```bash
getent hosts example.com
dig example.com
dig example.com TCP
```

If your `dig` version requires different syntax for TCP, consult `dig -h` or the manual and use the equivalent `+tcp` option.

**Tasks**
1. Compare the resolver result and direct DNS query.
2. Try a TCP DNS query where supported.
3. Explain why DNS may use UDP or TCP.
4. Explain why successful DNS resolution does not guarantee that the application port is reachable.

## Lab 8 — Review firewall posture

Read-only inspection:

```bash
sudo ufw status verbose
sudo nft list ruleset
```

**Tasks**
1. Identify which firewall tool is in use, if any.
2. Record relevant inbound rules without copying secrets or sensitive topology into public notes.
3. Explain why host firewall review alone may be insufficient.
4. Recommend least-privilege rules for a web server and a private database.
5. Do not apply changes during this lab.

## Lab 9 — Create a local port inventory

Build a table for each listener found in Lab 2:

| Port/protocol | Process | Bind address | Purpose | Required sources | Risk | Next action |
|---|---|---|---|---|---|---|

**Tasks**
1. Identify the service owner or package.
2. Verify expected use.
3. Identify unexpected or overly broad exposure.
4. Recommend an action only when supported by evidence.

## Lab 10 — Security exposure scenario

**Scenario:** A database listener is reachable from the public internet.

**Tasks**
1. Identify the risks.
2. Propose a containment plan that preserves authorized administrative access.
3. Recommend network restrictions, authentication, encryption, patching, and monitoring.
4. Describe how to verify the database is no longer publicly reachable.
5. Include rollback and change approval considerations.

## Lab 11 — Port versus service identity

**Tasks**
1. Explain why port 8080 does not guarantee HTTP.
2. Explain why port 443 does not guarantee safe HTTPS.
3. List evidence that helps identify a service (process, protocol handshake, configuration, logs).
4. Explain why a banner alone can be misleading.
5. Write a short evidence-based finding for an unknown listener in your lab.

## Lab 12 — Incident report

Pick one lab result and write a report with:
- Time and system
- Port and transport
- Source/destination and whether details are redacted
- Command and observed output
- Hypotheses
- Additional evidence needed
- Recommended action
- Verification plan

## Submission checklist

- [ ] Port reference table completed.
- [ ] Local listeners inventoried.
- [ ] TCP connectivity test interpreted.
- [ ] TCP/UDP differences explained.
- [ ] Refusal and timeout scenarios documented.
- [ ] Firewall posture reviewed read-only.
- [ ] Port inventory includes purpose and exposure.
- [ ] Incident report separates evidence from hypotheses.
