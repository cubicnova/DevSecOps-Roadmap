# Networking Fundamentals — Examples

These examples are designed for a local Linux machine or an authorized lab. Some commands require tools such as `iproute2`, `curl`, `dig`, or `tcpdump`.

## 1. Inspect network interfaces

```bash
ip address show
```

Look for:
- Interface name, such as `eth0`, `ens33`, or `wlan0`.
- `inet` for IPv4 addresses.
- `inet6` for IPv6 addresses.
- Interface state, such as `UP`.

The loopback interface is commonly `lo`, with IPv4 address `127.0.0.1` and IPv6 address `::1`.

## 2. Inspect the routing table

```bash
ip route show
ip -6 route show
```

A default route often looks like:

```text
default via 192.168.1.1 dev eth0
```

This indicates that traffic without a more specific route may be forwarded to gateway `192.168.1.1` through `eth0`. Your actual output will differ.

## 3. Inspect neighbor discovery

```bash
ip neigh show
```

The table may show IPv4-to-MAC neighbor entries discovered using ARP, or IPv6 neighbor entries using Neighbor Discovery. Entries can be incomplete, stale, or absent until traffic is exchanged.

## 4. Test the local TCP/IP stack

```bash
ping -c 4 127.0.0.1
```

This tests ICMP reachability to the local loopback address. A successful loopback test does not prove that the network adapter, gateway, DNS, or internet connection works.

## 5. Check name resolution

```bash
getent hosts example.com
```

If `dig` is installed:

```bash
dig example.com
dig A example.com
dig AAAA example.com
dig MX example.com
```

- `A`: IPv4 address.
- `AAAA`: IPv6 address.
- `MX`: mail exchange records.
- `NS`: authoritative name servers.
- `TXT`: text records, often used for verification and email security policies.

DNS answers can vary by resolver, cache, network, and time.

## 6. Inspect an HTTPS response

```bash
curl -I https://example.com
```

This sends an HTTP HEAD request when supported and prints response headers. A status such as `200`, `301`, or `404` is an HTTP response code, not a direct measure of network security.

To see connection and TLS details:

```bash
curl -vI https://example.com
```

Verbose output may expose hostnames and connection metadata; avoid publishing sensitive output.

## 7. Inspect listening sockets

```bash
ss -tuln
```

Common flags:
- `-t`: TCP sockets.
- `-u`: UDP sockets.
- `-l`: listening sockets.
- `-n`: show numeric addresses and ports.

Use `sudo ss -tulpn` only when process details are needed and you have appropriate permissions.

## 8. Understand a TCP connection

A typical TCP connection begins with a three-way handshake:

1. Client sends `SYN`.
2. Server replies `SYN-ACK`.
3. Client sends `ACK`.

TCP provides ordered, reliable byte-stream delivery. UDP sends independent datagrams without the same built-in connection setup and delivery guarantees.

## 9. Capture a small amount of authorized traffic

On your own machine, if `tcpdump` is installed:

```bash
sudo tcpdump -ni any -c 20
```

Capture only 20 packets, then stop. A narrower DNS filter is:

```bash
sudo tcpdump -ni any -c 20 'port 53'
```

Packet capture permissions and interface names vary. Do not capture other people's traffic or credentials.

## 10. Calculate a simple subnet

For `192.168.10.0/24`:
- Prefix length: 24 bits are network bits.
- Subnet mask: `255.255.255.0`.
- Total IPv4 addresses: \(2^{32-24} = 256\).
- Conventional usable host addresses: 254, excluding network and broadcast addresses.
- Network address: `192.168.10.0`.
- Broadcast address: `192.168.10.255`.
- Conventional host range: `192.168.10.1`–`192.168.10.254`.

Special-purpose subnets and point-to-point links can have different practical rules; IPv6 does not use broadcast addresses.

## 11. Common troubleshooting sequence

1. Check interface state and address: `ip address`.
2. Check route: `ip route`.
3. Check gateway reachability if ICMP is permitted.
4. Check DNS with `getent hosts` or `dig`.
5. Check service reachability with `curl` or an approved client.
6. Inspect firewall and service logs where authorized.
7. Capture a small sample of traffic only if necessary.

A failed `ping` alone does not prove a host is down; ICMP may be filtered while TCP services remain reachable.
