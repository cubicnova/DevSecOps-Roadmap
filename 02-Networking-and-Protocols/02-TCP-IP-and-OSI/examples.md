# Examples — TCP/IP and OSI

These examples are for learning and authorized troubleshooting. Outputs vary by operating system and network.

## 1. Map a web request to the layers

When a user opens `https://example.com`:

1. **Application:** the browser uses DNS and HTTPS-related application behavior.
2. **Transport:** TCP commonly carries HTTPS on port 443; HTTP/3 uses QUIC over UDP.
3. **Internet:** IP routes packets toward the destination.
4. **Link:** Ethernet or Wi-Fi frames carry traffic over the local link.
5. **Physical:** bits are transmitted through copper, fiber, or radio.

This is a simplified view. Proxies, VPNs, NAT, caches, and protocol negotiation may change the path or transport.

## 2. Compare OSI and TCP/IP

```text
OSI                         TCP/IP (4 layers)
7 Application  ┐
6 Presentation ├──────────> Application
5 Session      ┘
4 Transport    ───────────> Transport
3 Network      ───────────> Internet
2 Data Link    ┐
1 Physical     ┘──────────> Network Access / Link
```

The mapping is conceptual, not a perfect one-to-one protocol implementation.

## 3. Check an IP configuration (Linux)

```bash
ip address
ip route
ip neigh
```

Look for:
- An address and correct prefix on the expected interface.
- A route to the target network or a default route.
- Neighbor entries for local next hops, when applicable.

## 4. Resolve a hostname

```bash
getent hosts example.com
```

Alternative:

```bash
dig example.com
```

If `getent` fails, investigate resolver configuration and DNS reachability. If DNS succeeds, the application may still fail because of routing, filtering, TLS, or server issues.

## 5. Test a TCP port (Linux)

```bash
curl -I --max-time 10 https://example.com
```

Or, if `nc` is installed:

```bash
nc -vz -w 3 example.com 443
```

A successful TCP connection indicates that a connection was established to that endpoint and port at that moment. It does not guarantee that the application is healthy or that the correct service is behind the port.

## 6. Test a port (Windows PowerShell)

```powershell
Test-NetConnection example.com -Port 443
```

Review `TcpTestSucceeded`, target address, and route/source information. A failure can arise from DNS, routing, filtering, or a non-listening service.

## 7. Observe local sockets (Linux)

```bash
ss -tuna
```

- `-t`: TCP
- `-u`: UDP
- `-n`: numeric addresses and ports
- `-a`: listening and non-listening sockets

For listening sockets with process details:

```bash
sudo ss -tulpn
```

## 8. Capture TCP handshake packets

```bash
sudo tcpdump -i eth0 'tcp port 443' -c 30
```

Replace `eth0` with the correct interface. In Wireshark, a TCP connection commonly shows:
- SYN
- SYN/ACK
- ACK

Retransmissions or repeated SYN packets can suggest loss, filtering, or an unavailable endpoint, but capture location and other evidence matter.

## 9. Understand a TCP header

Fields commonly discussed include:
- Source port and destination port
- Sequence number and acknowledgment number
- Flags such as SYN, ACK, FIN, and RST
- Window size
- Checksum

TCP sequence numbers and acknowledgments support ordered, reliable byte-stream delivery. UDP has a simpler header and does not provide TCP-style reliability.

## 10. Understand an IP packet

IP header fields include source and destination IP addresses and fields used for forwarding and handling packets. IPv4 includes a header checksum; IPv6 has a different header design and no IPv6 base-header checksum.

Routers use the destination IP address and routing information to forward packets. Link-layer headers are rewritten at each routed hop in ordinary Ethernet/IP forwarding, while the end-to-end IP addresses usually remain the same unless NAT or another transformation is used.

## 11. Distinguish the three common identifiers

| Identifier | Example | Typical purpose |
|---|---|---|
| MAC address | `00:11:22:33:44:55` | Local-link delivery |
| IP address | `192.0.2.10` | Logical addressing and routing |
| Port | TCP `443` | Identify a transport endpoint/application socket |

The examples use documentation/example values where possible. MAC addresses may be locally administered or randomized; do not assume a MAC permanently identifies a person or device.

## 12. ARP and the default gateway

For IPv4 on Ethernet, a host sending to a remote IP generally sends the frame to the router's local MAC address. ARP helps resolve the next-hop IPv4 address to a link-layer address on the local network.

```bash
ip route
ip neigh
```

Do not assume the destination server's MAC address is visible on the local LAN when the server is remote.

## 13. Identify the layer from the symptom

| Symptom | Useful first checks |
|---|---|
| Interface reports no link | Interface status, cable/Wi-Fi, switch/AP, Layer 1/2 |
| Host has no expected IP | DHCP, address/prefix, VLAN, Layer 2/3 |
| Local subnet works, remote network fails | Default gateway, routes, ACLs |
| DNS fails but IP-based test works | Resolver config, DNS server reachability |
| TCP port refuses connection | Target service, listening socket, active reject |
| TCP connection times out | Routing, filtering, packet loss, endpoint state |
| TLS certificate warning | Hostname, certificate chain, system time, TLS endpoint |
| HTTP 500 response | Application/server logs and dependencies |

Symptoms are clues, not definitive layer assignments. Several layers may be involved.

## 14. Example troubleshooting transcript

```text
Symptom: Client cannot load internal site.
1. Confirm hostname resolves to the expected address.
2. Check local IP address and route.
3. Test TCP connectivity to the expected port.
4. If TCP fails, inspect server listener and network controls.
5. If TCP succeeds, inspect TLS negotiation and HTTP response.
6. Correlate server logs with the request timestamp.
7. Record evidence, hypothesis, action, and verification.
```

## 15. Packet capture privacy

Before sharing a capture:
- Confirm authorization and purpose.
- Limit capture duration and scope.
- Prefer capture filters that collect only necessary traffic.
- Protect files with appropriate permissions.
- Check for cookies, tokens, personal data, internal hostnames, and unencrypted payloads.
- Share only with approved recipients and follow retention policy.
