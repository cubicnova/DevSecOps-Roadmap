# Solutions — TCP/IP and OSI

These are sample answers. Your local command output will differ by device, operating system, and network. Record what you actually observe rather than copying example results as facts.

## Lab 1 — Memorize the OSI layers

From Layer 1 to Layer 7:

1. **Physical:** signaling and transmission media; PDU commonly called bits.
2. **Data Link:** local-link framing and MAC addressing; frame.
3. **Network:** logical addressing and routing; packet.
4. **Transport:** process-to-process delivery and ports; TCP segment or UDP datagram.
5. **Session:** dialog/session management; often described as data.
6. **Presentation:** representation, encoding, compression, and encryption functions; data.
7. **Application:** services used by applications; data.

The PDU labels are conventional teaching terms. They are not universal names for every protocol's unit.

## Lab 2 — Compare TCP/IP and OSI

| OSI layers | TCP/IP four-layer model |
|---|---|
| Application, Presentation, Session (7–5) | Application |
| Transport (4) | Transport |
| Network (3) | Internet |
| Data Link and Physical (2–1) | Network Access / Link |

The TCP/IP model groups functions differently from the OSI reference model. Real protocols may cross these conceptual boundaries, so avoid saying that every protocol belongs exclusively to one OSI layer.

## Lab 3 — Trace a web request

Possible interpretation:
- `getent hosts` tests name resolution through the system's name-service configuration.
- `ip address` shows local interface addresses.
- `ip route` shows the routing table.
- `curl -I` requests headers and can reveal an HTTP status if the connection succeeds.

These commands do not by themselves prove every hop is healthy, show all firewall decisions, or reveal encrypted application payloads. DNS may be cached, and the actual path may include proxies or VPNs.

## Lab 4 — Inspect local addresses

- Interface address and subnet/prefix: Layer 3 information.
- Default gateway: next-hop routing information, Layer 3.
- MAC/neighbor entry: local link-layer information used for delivery.
- ARP tables/neighbor caches may be empty or incomplete if the host has not recently communicated with a neighbor.

Redact public IPs, internal topology, and device identifiers when sharing output outside the approved team.

## Lab 5 — Compare DNS and TCP connectivity

- DNS success means the resolver returned a result for that query.
- TCP success means a connection was established to a particular IP and port at that time.
- A **refused** connection often means the endpoint or an active network device rejected it; the service may not be listening.
- A **timeout** can result from packet loss, filtering, routing issues, or a nonresponsive endpoint.
- HTTP or TLS can still fail after TCP succeeds.

Possible next checks: confirm the resolved address, inspect the service listener, check firewall/security-group policy, and inspect TLS/application errors.

## Lab 6 — Observe a TCP handshake

A typical TCP handshake:
1. Client sends SYN.
2. Server responds SYN/ACK.
3. Client sends ACK.

This establishes TCP connection state and synchronizes sequence numbers. It does not prove the application is healthy or the user is authorized.

An incomplete handshake may be caused by capture on the wrong interface, asymmetric routing, filtering, loss, endpoint unavailability, or a capture that started too late. Treat it as evidence to investigate, not a definitive diagnosis.

## Lab 7 — Explore UDP versus TCP

- **TCP:** connection-oriented byte stream, with sequence numbers, acknowledgments, retransmission, and flow control.
- **UDP:** connectionless datagrams without TCP-style delivery or ordering guarantees.
- DNS commonly uses UDP for many queries and can use TCP in situations such as larger responses, truncation fallback, and zone transfers. Actual behavior depends on DNS implementation and configuration.

## Lab 8 — Identify the layer from scenarios

1. **Fiber disconnected:** Layer 1, with possible Layer 2 link effects.
2. **Incorrect MAC forwarding:** Layer 2.
3. **Incorrect subnet mask:** Layer 3 configuration.
4. **Missing route:** Layer 3.
5. **TCP service not listening:** primarily Layer 4/service configuration, with application/service diagnostics.
6. **Unexpected DNS answer:** Application-layer DNS behavior and potentially resolver/cache/configuration issues.
7. **HTTP 500:** Application layer.
8. **TLS hostname mismatch:** application security/TLS validation; TLS does not map cleanly to a single OSI layer.

Some cases involve multiple layers. The answer should explain the evidence behind the chosen layer.

## Lab 9 — Encapsulation diagram

Simplified sender flow:

```text
Application data
  + TCP header
  = TCP segment
  + IP header
  = IP packet
  + link-layer header/trailer
  = frame
  -> bits/signals on the medium
```

At the receiver, each layer interprets and removes its own header/trailer before passing data upward. A router typically receives a link-layer frame, processes the IP packet, and sends it in a new link-layer frame for the next link. IP addresses usually remain end-to-end unless NAT, tunneling, or other transformations occur.

## Lab 10 — Troubleshooting decision tree

A useful sequence:

1. **Name does not resolve:** inspect resolver settings and DNS server reachability; compare with an approved known-good resolver if policy permits.
2. **No expected local address:** inspect interface state, DHCP/static configuration, and VLAN/link.
3. **No route:** inspect subnet, gateway, and routing policy.
4. **TCP fails:** confirm destination IP/port, server listener, firewall, and route.
5. **TCP succeeds but TLS fails:** check certificate validity/hostname, system time, SNI, and TLS endpoint.
6. **HTTP error:** inspect status, request path, application logs, and dependencies.

Do not assume that a failed test identifies one root cause. Use tests that distinguish between competing explanations.

## Lab 11 — Read a packet capture

Useful Wireshark display filters:
- `dns`
- `tcp`
- `ip.addr == 192.0.2.10` (replace the example address)
- `tcp.port == 443`

The packet details pane can show Ethernet, IP, TCP/UDP, and visible application metadata. HTTPS content is encrypted in ordinary captures, though metadata may remain visible. Protect captures because they may contain credentials or personal information from unencrypted protocols and application metadata.

## Lab 12 — Layer-based incident report

Example structure:

```text
Symptom: Internal application connection fails.
Time window: [actual time and timezone]
Scope: [actual client(s) and server]
Facts:
- [DNS result]
- [interface address and route]
- [TCP test result]
- [service/socket/log result]
Hypothesis: [supported explanation and confidence]
Next test: [test that distinguishes alternatives]
Action: [approved change, if any]
Verification: [repeat test and application check]
Uncertainty: [remaining unknowns]
```

Do not claim a root cause until evidence supports it. If no cause is confirmed, say so and identify the next best test.

## General reminders

- OSI is a reference model; TCP/IP is a protocol suite/model.
- MAC addresses are for local-link delivery; IP addresses support internetwork routing; ports identify transport endpoints.
- DNS resolution, IP reachability, TCP connectivity, TLS negotiation, and application health are separate checks.
- A failed ping is inconclusive because ICMP may be filtered.
- Capture only traffic you are authorized to inspect and handle capture files as sensitive data.
