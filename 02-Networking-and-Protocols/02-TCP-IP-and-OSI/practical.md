# Practical Labs — TCP/IP and OSI

Perform the labs on your own machine, a private lab, or a network you are explicitly authorized to test. Do not capture other people's traffic or scan networks without permission.

## Lab 1 — Memorize the OSI layers

**Tasks**
1. Write the seven layers from 1 to 7 and from 7 to 1.
2. For each layer, list one responsibility and one example.
3. Match each PDU term: bits, frame, packet, segment/datagram, data.
4. Explain why the model is useful for troubleshooting.

**Deliverable:** A one-page OSI table.

## Lab 2 — Compare TCP/IP and OSI

**Tasks**
1. Create a mapping table for the four-layer TCP/IP model.
2. Identify which OSI layers map to TCP/IP Application.
3. Explain why TCP/IP Network Access combines OSI Physical and Data Link in the four-layer convention.
4. Mention one limitation of a strict one-to-one mapping.

## Lab 3 — Trace a web request

Choose an approved website or an internal test server.

**Commands (Linux):**

```bash
getent hosts example.com
ip address
ip route
curl -I --max-time 10 https://example.com
```

**Tasks**
1. Record the DNS result.
2. Identify the interface and route likely used.
3. Record the HTTP status line if returned.
4. Map each observed step to the relevant layer(s).
5. Explain what these commands cannot prove.

## Lab 4 — Inspect local addresses

**Linux:**

```bash
ip address
ip route
ip neigh
```

**Windows PowerShell:**

```powershell
ipconfig /all
route print
arp -a
```

**Tasks**
1. Identify your active interface.
2. Record its private/public address classification where applicable, prefix/subnet mask, and default gateway.
3. Find a neighbor/ARP entry if present.
4. Explain which values are link-layer identifiers and which are IP addresses.
5. Redact identifying details before sharing your report.

## Lab 5 — Compare DNS and TCP connectivity

Test an approved hostname and port.

```bash
getent hosts example.com
nc -vz -w 3 example.com 443
curl -I --max-time 10 https://example.com
```

If `nc` is unavailable, use `curl` or your OS's TCP test utility.

**Tasks**
1. Record which checks succeed.
2. Explain why DNS success does not prove TCP reachability.
3. Explain the difference between a refused connection and a timeout.
4. Identify two other possible causes of failure.

## Lab 6 — Observe a TCP handshake

With permission, capture a short request to a known test endpoint:

```bash
sudo tcpdump -i INTERFACE 'tcp port 443' -c 30
```

Replace `INTERFACE` with a valid interface name. You may also use Wireshark.

**Tasks**
1. Find a SYN, SYN/ACK, ACK sequence if visible.
2. Record source/destination IPs and ports, redacting sensitive details.
3. Explain what the handshake establishes.
4. If the sequence is incomplete, list multiple possible explanations.
5. Stop the capture promptly and protect the file.

## Lab 7 — Explore UDP versus TCP

**Tasks**
1. Explain the difference between TCP's byte stream and UDP datagrams.
2. Identify one common application use for each.
3. Observe DNS traffic in an authorized capture, if available.
4. Explain why DNS may use TCP as well as UDP.
5. Do not conclude that all DNS traffic always uses one transport.

## Lab 8 — Identify the layer from scenarios

Assign the most relevant layer or layers and justify each answer:
1. A fiber link is disconnected.
2. A switch has learned the wrong MAC forwarding information.
3. A host has an incorrect subnet mask.
4. A route to a remote network is missing.
5. A TCP service is not listening on its expected port.
6. DNS returns an unexpected address.
7. A server returns HTTP 500.
8. A TLS certificate hostname does not match the requested site.

## Lab 9 — Encapsulation diagram

Draw a data flow for a browser request. Include:
- Application data
- TCP or UDP header
- IP header
- Link-layer header/trailer
- Bits on the medium

Then draw decapsulation at the receiver. Explain why the link-layer source/destination addresses may change at a router while end-to-end IP addresses usually remain stable absent NAT/tunneling.

## Lab 10 — Troubleshooting decision tree

Create a decision tree for “website unavailable” that tests:
1. Name resolution
2. Local interface/address
3. Route/default gateway
4. TCP port connectivity
5. TLS/HTTP response
6. Server logs

For each branch, specify the next check and at least one alternative explanation.

## Lab 11 — Read a packet capture

Open an authorized `.pcap` or `.pcapng` file in Wireshark.

**Tasks**
1. Find a DNS query/response if present.
2. Find a TCP connection and identify its handshake.
3. Inspect Ethernet, IP, and TCP headers.
4. Apply a display filter such as `dns`, `tcp`, or `ip.addr == 192.0.2.10` (replace the example address).
5. Explain why encrypted HTTPS payloads are not normally readable without appropriate decryption material.

## Lab 12 — Write a layer-based incident report

Scenario: a client cannot connect to an internal application.

Create a report with:
- Symptom and time
- Scope and affected endpoints
- Commands and results
- Relevant OSI/TCP/IP layers
- Hypothesis with confidence
- Next test
- Recommended fix (if supported by evidence)
- Verification and remaining uncertainty

## Submission checklist

- [ ] OSI and TCP/IP comparison completed.
- [ ] Address, route, and DNS checks recorded.
- [ ] TCP connectivity test interpreted.
- [ ] Encapsulation diagram created.
- [ ] Scenario layer mappings justified.
- [ ] Packet capture reviewed only with authorization.
- [ ] Incident report separates facts from hypotheses.
