# 02 — TCP/IP and OSI Models

Understand how network communication is organized, how data moves between layers, and how to use the OSI and TCP/IP models to troubleshoot connectivity.

## Learning objectives

By the end of this module, you should be able to:

- Explain the purpose of layered network models.
- Name the seven OSI layers in order and describe their responsibilities.
- Describe the four-layer TCP/IP model and map it to OSI.
- Identify common protocols, addresses, devices, and protocol data units (PDUs).
- Explain encapsulation and decapsulation.
- Distinguish MAC addresses, IP addresses, and transport ports.
- Use basic command-line tools to investigate a connection layer by layer.
- Analyze a simple packet capture with Wireshark or `tcpdump`.

## Prerequisites

- Basic computer and command-line knowledge.
- A Linux, Windows, or macOS computer; a lab VM is helpful.
- Wireshark or `tcpdump` is optional for packet-analysis exercises.

## 1. Why use layered models?

Network communication involves applications, transport protocols, IP routing, local-link delivery, and physical signaling. A layered model divides these responsibilities into manageable functions. It helps people design systems, describe protocol behavior, and narrow down faults.

The OSI model is a **reference model**. The TCP/IP model describes the architecture of the Internet protocol suite. Their layer boundaries are useful guides, not a claim that every real protocol fits perfectly into only one layer.

## 2. The seven OSI layers

Remember the layers from Layer 7 down to Layer 1:

**Application → Presentation → Session → Transport → Network → Data Link → Physical**

| Layer | Name | Main responsibility | Examples / concepts | PDU (common teaching term) |
|---|---|---|---|---|
| 7 | Application | Network services used by applications | HTTP, DNS, SMTP, SSH | Data |
| 6 | Presentation | Data representation, encoding, compression, encryption functions | Character encoding, formats, TLS functions often discussed here conceptually | Data |
| 5 | Session | Establishing, managing, and ending dialogs/sessions | Session control and checkpoints as model concepts | Data |
| 4 | Transport | Process-to-process delivery, ports, segmentation, reliability or datagrams | TCP, UDP | Segment (TCP) / Datagram (UDP) |
| 3 | Network | Logical addressing and forwarding between networks | IPv4, IPv6, ICMP; routers | Packet |
| 2 | Data Link | Delivery over a local link, framing, MAC addressing | Ethernet, Wi-Fi MAC, switches, VLANs | Frame |
| 1 | Physical | Transmission of bits as electrical, optical, or radio signals | Cables, fiber, radio, connectors, signaling | Bits |

**Important nuance:** These are teaching associations. Real protocols may span functions that the OSI model separates. For example, TLS is commonly described as operating between application protocols and transport; calling it strictly an OSI Layer 6 protocol is an oversimplification.

### Layer 7 — Application

Provides network services to applications. Examples include HTTP for web traffic, DNS for name resolution, SMTP for mail transfer, and SSH for remote administration.

Troubleshooting examples: HTTP status codes, application configuration, DNS query behavior, and service logs.

### Layer 6 — Presentation

Describes how data is represented, encoded, compressed, or protected so communicating systems can interpret it consistently. Character encoding and media formats are common examples. Encryption can be discussed at this layer in the OSI model, although real-world TLS does not map neatly to one OSI layer.

### Layer 5 — Session

Describes management of dialogs between communicating applications, including establishing, coordinating, and ending sessions. In practical TCP/IP networks, session responsibilities are often implemented by application protocols and libraries rather than a distinct Session-layer protocol.

### Layer 4 — Transport

Provides communication between processes on endpoints. Ports identify transport endpoints. TCP provides a reliable, ordered byte stream using sequence numbers, acknowledgments, retransmission, and flow control. UDP provides a lightweight datagram service without TCP's delivery guarantees.

Examples: TCP port 443 commonly carries HTTPS; UDP port 53 is commonly used for DNS queries, though DNS can also use TCP.

### Layer 3 — Network

Moves packets between networks using logical addresses and routing. IPv4 and IPv6 are core protocols. Routers forward packets based on network-layer information. ICMP supports diagnostic and error-reporting functions; it is not a transport protocol like TCP or UDP.

### Layer 2 — Data Link

Moves frames over a local link. Ethernet and Wi-Fi use link-layer addressing and link-specific framing. Switches commonly forward Ethernet frames using MAC address tables. VLANs logically separate Layer 2 broadcast domains.

A MAC address is used for local-link delivery; it is not normally the end-to-end address used by IP routing.

### Layer 1 — Physical

Carries bits over a physical medium, such as copper, fiber, or radio. Link status, cabling, radio conditions, connectors, transceivers, and negotiated speed can all affect connectivity.

## 3. TCP/IP model

A commonly taught four-layer TCP/IP model is:

| TCP/IP layer | Typical responsibilities | Approximate OSI mapping | Examples |
|---|---|---|---|
| Application | Application protocols and data representation/dialog functions | OSI 5–7 | HTTP(S), DNS, SMTP, SSH, DHCP |
| Transport | Process-to-process communication | OSI 4 | TCP, UDP |
| Internet | Logical addressing and routing | OSI 3 | IPv4, IPv6, ICMP |
| Network Access / Link | Local-link delivery and access to the medium | OSI 1–2 | Ethernet, Wi-Fi |

Some courses use a **five-layer Internet model**, splitting Network Access into Data Link and Physical. Both conventions are useful if you state which one you are using.

## 4. OSI and TCP/IP comparison

| OSI | TCP/IP (four-layer convention) |
|---|---|
| Application (7) | Application |
| Presentation (6) | Application |
| Session (5) | Application |
| Transport (4) | Transport |
| Network (3) | Internet |
| Data Link (2) | Network Access / Link |
| Physical (1) | Network Access / Link |

Do not memorize the mapping as an exact one-to-one implementation. The OSI model is a conceptual reference; TCP/IP describes a working protocol suite.

## 5. Encapsulation and decapsulation

As data is sent, each layer passes information to the layer below. The lower layer typically adds its own header (and sometimes a trailer). At the receiver, the process is reversed.

```text
Application data
      ↓ Transport adds TCP/UDP header
TCP segment / UDP datagram
      ↓ Internet adds IP header
IP packet
      ↓ Link adds frame header/trailer
Link-layer frame
      ↓ Physical medium carries bits
Bits on the medium
```

At the destination, link, IP, transport, and application processing remove or interpret their respective headers. Actual packet formats and offloading can make packet captures look different from this simplified diagram.

### Addressing at different layers

- **Application naming:** a hostname such as `example.com`.
- **Transport:** source and destination port numbers, such as TCP destination port 443.
- **Network:** source and destination IP addresses.
- **Data Link:** source and destination MAC addresses on the local link.
- **Physical:** signals representing bits.

When a host sends traffic to a remote network, the Ethernet destination MAC address is generally the next-hop router's MAC address, while the IP destination remains the remote endpoint's IP address (unless a proxy, NAT, tunnel, or other mechanism changes the path).

## 6. Common protocols and tools

| Protocol / technology | Main role | Common layer association |
|---|---|---|
| HTTP / HTTPS | Web application traffic | Application |
| DNS | Names to records such as IP addresses | Application |
| DHCP | Automatic IP configuration | Application |
| SSH | Encrypted remote shell and tunneling | Application |
| SMTP | Mail transfer | Application |
| TCP | Reliable, ordered transport stream | Transport |
| UDP | Datagram transport | Transport |
| IPv4 / IPv6 | Addressing and routing | Internet / Network |
| ICMP | Error reporting and diagnostics | Internet / Network |
| ARP (IPv4 Ethernet) | Resolve IPv4 next-hop address to link-layer address on a local network | Link-related support |
| Ethernet / Wi-Fi | Local-link framing and medium access | Link / Network Access |
| TLS | Cryptographic protection for application traffic | Often placed between application and transport conceptually; not a strict single-layer fit |

Port numbers are conventions, not guarantees about what service is actually running. Verify the service and traffic rather than assuming a port proves application identity.

## 7. Practical command-line checks

### Linux

```bash
ip address
ip route
ip neigh
getent hosts example.com
ping -c 4 example.com
curl -I --max-time 10 https://example.com
ss -tuna
```

### Windows PowerShell

```powershell
ipconfig /all
route print
arp -a
Resolve-DnsName example.com
Test-NetConnection example.com -Port 443
```

### macOS

```bash
ifconfig
netstat -rn
arp -a
dig example.com
curl -I --max-time 10 https://example.com
```

Commands may require different options or privileges depending on OS version. A failed ping is not proof that a host is down: ICMP may be filtered. A successful DNS lookup proves name resolution worked for that query, not that the application is reachable.

## 8. Troubleshooting using layers

Work from the symptom and test each relevant dependency:

1. **Physical/link:** cable or Wi-Fi association, interface state, link errors.
2. **Local network:** IP address, subnet, VLAN, neighbor/ARP resolution.
3. **Routing:** default gateway and route to destination.
4. **Transport:** destination port, listening socket, firewall, TCP handshake.
5. **Application:** DNS behavior, TLS certificate, HTTP response, service logs.

You do not always need to start at Layer 1. Begin with the reported symptom and choose tests that discriminate between likely causes.

### Example: website does not load

- Check whether the hostname resolves.
- Check local IP and route.
- Test TCP connectivity to the expected port.
- Inspect TLS and HTTP responses.
- Review browser and server logs.
- Compare with another known-good client or destination where appropriate.

## 9. Packet capture basics

Capture only on systems and networks you own or are explicitly authorized to inspect. Packet captures can include personal or confidential data.

With `tcpdump` installed:

```bash
# List interfaces (option varies by platform)
sudo tcpdump -D

# Capture a small number of packets on an interface
sudo tcpdump -i eth0 -c 20

# Filter for TCP port 443
sudo tcpdump -i eth0 'tcp port 443' -c 50
```

Replace `eth0` with an interface listed on your system. Capture filters use `tcpdump`/libpcap syntax. You may need to run with elevated privileges; do not leave long-running captures active unnecessarily.

With Wireshark:
1. Select the correct interface.
2. Start a short, authorized capture.
3. Generate a known test request.
4. Stop the capture and filter by host, protocol, or port.
5. Inspect Ethernet, IP, TCP/UDP, and application details where visible.
6. Remember that HTTPS payloads are encrypted; you can still observe metadata such as addresses, ports, and handshake information, depending on protocol version and capture point.

## 10. Knowledge check

1. Which OSI layer is associated with routing IP packets?
2. Which layer uses TCP and UDP ports?
3. What is the difference between a MAC address and an IP address?
4. What happens during encapsulation?
5. Why can ping fail while HTTPS still works?
6. Which TCP/IP layer includes DNS and HTTP in the common four-layer model?
7. What does a successful DNS lookup tell you—and what does it not prove?
8. Why is a packet capture sensitive information?

Answers and explanations are in [`solutions.md`](solutions.md).

## Further reading

- [RFC 1180 — A TCP/IP Tutorial](https://www.rfc-editor.org/info/rfc1180/)
- [RFC 1122 — Requirements for Internet Hosts: Communication Layers](https://www.rfc-editor.org/rfc/rfc1122.html)
- [RFC 791 — Internet Protocol](https://www.rfc-editor.org/info/rfc791/)
- [Cisco — TCP/IP Overview](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13769-5.html)
- [Cisco Networking Academy — OSI model study resource](https://learningnetwork.cisco.com/sfc/servlet.shepherd/document/download/0693i000001r6HTAAY?operationContext=S1)

## Completion checklist

- [ ] I can explain each OSI layer and its PDU.
- [ ] I can map the OSI model to the TCP/IP model.
- [ ] I understand ports, IP addresses, and MAC addresses.
- [ ] I can explain encapsulation and decapsulation.
- [ ] I can run basic DNS, route, and port connectivity checks.
- [ ] I can inspect a small packet capture safely.
