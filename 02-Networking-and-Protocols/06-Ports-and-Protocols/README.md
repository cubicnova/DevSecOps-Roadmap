# 06 — Ports and Protocols

Learn how network ports identify transport endpoints, how TCP and UDP differ, which common ports you are likely to encounter, and how to troubleshoot services safely.

## Learning objectives

By the end of this module, you should be able to:

- Explain the relationship between IP addresses, transport protocols, and port numbers.
- Distinguish TCP, UDP, and ICMP.
- Describe the registered, dynamic/private, and system port ranges.
- Recognize common service ports without assuming a port proves service identity.
- Inspect listening sockets and test connectivity with appropriate tools.
- Interpret connection refused, timeout, and DNS-related failures.
- Apply least privilege when exposing services and writing firewall rules.

## 1. What is a port?

An IP address identifies a network interface or endpoint at the network layer. TCP and UDP port numbers identify transport endpoints on a host. Together with the transport protocol and IP addresses, ports help distinguish concurrent conversations.

For example, an HTTPS connection may use:
- Client IP and an ephemeral client port
- Server IP and TCP destination port 443
- TCP as the transport protocol

A port number is not the same thing as a physical connector, and it does not guarantee which application is running. Services can use non-default ports, and a port may be open without serving the expected protocol.

## 2. Port-number ranges

TCP and UDP each have a 16-bit port-number space: 0–65535. The IANA convention divides the range into:

| Range | Name | General meaning |
|---|---|---|
| 0–1023 | System / Well-Known Ports | Common core services; OS privileges and binding rules vary |
| 1024–49151 | User / Registered Ports | Registered services and applications |
| 49152–65535 | Dynamic / Private Ports | Commonly used for temporary client-side ports |

The ranges are conventions for allocation, not a guarantee of how every operating system chooses ephemeral ports. A client can use an ephemeral source port while connecting to a well-known destination port.

See [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml).

## 3. TCP versus UDP

| Feature | TCP | UDP |
|---|---|---|
| Service model | Connection-oriented byte stream | Connectionless datagrams |
| Delivery and ordering | Provides reliable, ordered delivery to the application | No TCP-style delivery or ordering guarantee |
| Connection setup | TCP handshake | No TCP handshake |
| Common uses | Web (HTTP/1.1, HTTP/2), SSH, SMTP, many database services | DNS queries, DHCP, voice/video, QUIC/HTTP/3 |
| Header overhead | Larger than UDP's basic header | Smaller basic header |
| Application responsibility | TCP handles retransmission and ordering; app still handles application-level semantics | Applications handle any needed reliability, ordering, or retransmission |

UDP is not automatically faster or more secure; suitability depends on the application and network conditions. TCP and UDP port spaces are separate, so the same numeric port can be used by different services over different transports.

## 4. Common TCP ports

| Port | Transport | Common service | Notes |
|---:|---|---|---|
| 20/21 | TCP | FTP data/control (traditional active FTP uses port 20 for data) | FTP is plaintext unless protected by a separate mechanism; passive FTP uses negotiated ports |
| 22 | TCP | SSH / SFTP / SCP | Secure remote administration and file transfer |
| 23 | TCP | Telnet | Plaintext remote terminal; avoid on untrusted networks |
| 25 | TCP | SMTP server-to-server mail transfer | Not the same as mail submission on 587 |
| 53 | TCP/UDP | DNS | UDP common for queries; TCP is also required in several cases |
| 67/68 | UDP | DHCPv4 server/client | Broadcast and relay behavior may be involved |
| 69 | UDP | TFTP | Minimal file transfer protocol, no built-in strong authentication |
| 80 | TCP | HTTP | Common default for HTTP/1.1 and HTTP/2 |
| 110 | TCP | POP3 | Plaintext unless protected with TLS |
| 123 | UDP | NTP | Time synchronization |
| 143 | TCP | IMAP | Mail access; TLS can be used |
| 161/162 | UDP | SNMP queries/traps | Secure configuration and access controls are important |
| 179 | TCP | BGP | Routing protocol used between autonomous systems |
| 389 | TCP/UDP | LDAP | LDAPS commonly uses TCP 636 |
| 443 | TCP | HTTPS (HTTP/1.1 and HTTP/2 commonly) | HTTP/3 commonly uses QUIC over UDP 443 |
| 445 | TCP | SMB | File/printer sharing; restrict exposure |
| 465 | TCP | SMTP submission over implicit TLS (commonly used) | Service policy varies |
| 514 | UDP | Syslog (traditional) | Transport/security depend on deployment |
| 587 | TCP | SMTP message submission | Usually authenticated; STARTTLS commonly supported |
| 636 | TCP | LDAP over TLS (LDAPS) | Certificate validation matters |
| 993 | TCP | IMAP over implicit TLS | Mail access |
| 995 | TCP | POP3 over implicit TLS | Mail access |
| 1433 | TCP | Microsoft SQL Server (common default) | Restrict to trusted networks |
| 1521 | TCP | Oracle Database listener (common default) | Configuration varies |
| 3306 | TCP | MySQL (common default) | Avoid public exposure |
| 3389 | TCP/UDP | Remote Desktop Protocol | Restrict and protect access |
| 5432 | TCP | PostgreSQL (common default) | Restrict to required clients |
| 5900 | TCP | VNC (common default display range begins here) | Protect with secure tunneling and access controls |
| 6379 | TCP | Redis (common default) | Do not expose publicly without a deliberate secure design |
| 8080 | TCP | Common alternate HTTP / development service | Not inherently HTTP or safe |
| 8443 | TCP | Common alternate HTTPS/admin service | Configuration varies |
| 27017 | TCP | MongoDB (common default) | Restrict network access and authenticate |

These are common associations, not guarantees. Verify the actual service configuration and protocol.

## 5. Ports, sockets, and listening services

A **listening socket** is a local endpoint waiting for connections or datagrams. A firewall rule may allow a port while no application listens, or a service may listen while a firewall blocks remote access.

### Linux

```bash
ss -lnt
ss -lnu
sudo ss -lntup
```

- `-l`: listening
- `-n`: numeric addresses/ports
- `-t`: TCP
- `-u`: UDP
- `-p`: process information (often requires privileges)

To see active TCP connections:

```bash
ss -tn state established
```

### Windows PowerShell

```powershell
Get-NetTCPConnection -State Listen
Get-NetUDPEndpoint
```

For process IDs:

```powershell
Get-NetTCPConnection -State Listen |
  Select-Object LocalAddress,LocalPort,OwningProcess
```

Use `Get-Process -Id <PID>` to identify a process when appropriate.

## 6. Test connectivity

### Linux

```bash
nc -vz -w 3 example.com 443
curl -I --max-time 10 https://example.com/
```

### Windows PowerShell

```powershell
Test-NetConnection example.com -Port 443
```

These commands test different things:
- `nc` attempts a transport connection to a host and port.
- `Test-NetConnection` reports Windows network diagnostics and TCP test results.
- `curl` goes further into HTTP/TLS behavior if connection setup succeeds.

A successful TCP test does not prove that the application is healthy. A failed test may be caused by DNS, routing, firewall policy, endpoint state, or client-side restrictions.

## 7. How to interpret common outcomes

- **Connection refused:** the endpoint or an intermediate device actively rejected the connection; the service may not be listening.
- **Timeout:** packets or replies may be dropped, routing may be broken, or the endpoint may not respond.
- **Name resolution failure:** investigate DNS and hostname configuration before attributing the problem to the port.
- **TCP succeeds but application fails:** inspect TLS, protocol expectations, authentication, application logs, and request format.
- **Local works, remote fails:** check bind address, host firewall, routing, network ACLs/security groups, and upstream controls.
- **Port scan says open:** a listener or network responder accepted the probe; that does not prove identity or vulnerability.

## 8. Firewall and exposure principles

1. Allow only required inbound ports and source networks.
2. Keep database, cache, administrative, and development services off the public internet unless a documented architecture requires otherwise.
3. Prefer VPN, bastion, or other controlled access for administrative interfaces.
4. Use encryption and strong authentication where supported.
5. Review both host firewall and cloud/network firewall controls.
6. Document changes, test impact, and maintain a rollback plan.
7. Avoid scanning networks unless you have explicit authorization.

Example UFW status check:

```bash
sudo ufw status verbose
```

Example nftables read-only inspection:

```bash
sudo nft list ruleset
```

Do not apply firewall rules copied from an example without adapting them to your network and ensuring that administrative access will not be lost.

## 9. DNS and port 53

DNS maps names to records, including IP addresses. DNS commonly uses UDP port 53 for ordinary queries, but TCP port 53 is also used (for example, zone transfers and some larger/truncated responses). DNS-over-TLS commonly uses TCP 853; DNS-over-HTTPS uses HTTPS, often TCP 443 or HTTP/3 over UDP 443.

A DNS lookup succeeding does not prove the destination application port is reachable.

## 10. Dynamic and ephemeral ports

Clients often use a temporary source port when connecting to a server's destination port. For example:

```text
Client 192.0.2.25:53144  ->  Server 198.51.100.10:443 (TCP)
```

The example addresses are reserved for documentation. The client port is illustrative; actual ephemeral port ranges vary by OS and configuration. Firewalls and NAT devices track connection state so response traffic can return to the right client.

## 11. Security checklist

- [ ] Inventory listening TCP and UDP sockets.
- [ ] Identify each service owner and business need.
- [ ] Confirm bind addresses and exposure.
- [ ] Restrict inbound access with least privilege.
- [ ] Remove or disable unneeded services through approved change control.
- [ ] Protect administrative ports with strong authentication and network restrictions.
- [ ] Avoid plaintext protocols for sensitive data.
- [ ] Keep services patched and monitor logs.
- [ ] Confirm cloud security groups, network ACLs, and host firewall rules agree.
- [ ] Record findings, risk, remediation, and verification.

## Knowledge check

1. What does a port number identify?
2. How does TCP differ from UDP?
3. Why can TCP 443 and UDP 443 both be in use?
4. What is the difference between a listening socket and a firewall-allowed port?
5. What does “connection refused” suggest compared with a timeout?
6. Why should database ports rarely be exposed publicly?
7. Does an open port prove which service is running?
8. Why does DNS use both UDP and TCP in some situations?

## Further reading

- [IANA Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
- [RFC 9293 — Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293.html)
- [RFC 768 — User Datagram Protocol (UDP)](https://www.rfc-editor.org/rfc/rfc768.html)
- [RFC 1035 — Domain Names: Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035.html)
- [Nmap Reference Guide](https://nmap.org/book/man.html)
- [`ss(8)` manual](https://man7.org/linux/man-pages/man8/ss.8.html)

## Completion checklist

- [ ] I understand port ranges and transport endpoints.
- [ ] I can distinguish TCP and UDP behavior.
- [ ] I recognize common service ports and their risks.
- [ ] I can list listening sockets on Linux or Windows.
- [ ] I can test a port and interpret the result cautiously.
- [ ] I can recommend least-privilege network exposure.
