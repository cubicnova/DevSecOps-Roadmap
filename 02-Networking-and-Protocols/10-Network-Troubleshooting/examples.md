# Network Troubleshooting — Examples

Use these examples only on your own systems or against destinations you are authorized to test. Replace placeholders such as `<host>`, `<interface>`, and `<port>` before running commands.

## Example 1 — Check interface state and address

```bash
ip -br link
ip -br address
```

**Look for:** an interface that is down, a missing address, or an unexpected subnet. Do not assume every virtual interface should be up.

## Example 2 — Inspect the selected route

```bash
ip route
ip route get 198.51.100.20
```

`198.51.100.0/24` is reserved for documentation. Replace it with a target address from your approved lab. The route query can reveal the chosen interface, gateway, and source address.

## Example 3 — Compare OS DNS and direct DNS query

```bash
getent hosts example.com
dig example.com A
dig example.com AAAA
```

The OS resolver may use local configuration, search domains, or a corporate DNS service. A `dig` result can differ without either result necessarily being wrong.

## Example 4 — Test DNS against a named resolver

```bash
dig @1.1.1.1 example.com A
```

Use only if direct queries to that resolver are allowed by your network policy. Public DNS may not return internal split-horizon records.

## Example 5 — Test TCP connectivity

```bash
nc -vz -w 3 example.com 443
```

- Success: a TCP connection was established.
- Refused: a rejection was received.
- Timeout: no successful response arrived within the configured time.

A successful TCP connection does not prove the HTTPS application is healthy.

## Example 6 — Inspect listening sockets

```bash
sudo ss -lntup
ss -tan
```

Check whether the service is listening on the expected port and address. A service bound only to `127.0.0.1` cannot normally accept direct connections arriving on another interface.

## Example 7 — Inspect HTTP status and headers

```bash
curl -sS -D - -o /dev/null --connect-timeout 5 --max-time 15 https://example.com/
```

The output includes response headers and status. Check redirects, authentication requirements, rate limits, and server errors. Avoid sharing headers that contain secrets.

## Example 8 — Inspect TLS handshake

```bash
openssl s_client -connect example.com:443 -servername example.com </dev/null
```

Check certificate dates, subject alternative names, issuer/chain, and handshake errors. Use the hostname in `-servername` so the server can select the expected certificate.

## Example 9 — Trace the network path

```bash
tracepath example.com
```

If `tracepath` is unavailable, use an approved alternative such as `traceroute` or `mtr`. Intermediate hops may not reply, so missing responses alone do not prove an outage.

## Example 10 — Check packet loss over a short sample

```bash
ping -c 20 <approved-host>
```

Record packet loss and round-trip time. ICMP can be filtered or rate-limited, so compare with the actual application test and avoid treating ping as a definitive service-health check.

## Example 11 — Capture a small DNS trace

```bash
sudo tcpdump -i <interface> -nn -c 100 port 53
```

Start this only with authorization and on the correct interface. DNS queries may reveal internal hostnames. Limit access to captures and follow retention rules.

## Example 12 — Capture traffic for a specific host

```bash
sudo tcpdump -i <interface> -nn -c 200 -w /tmp/diagnostic.pcap host <target-ip>
```

Use a narrow filter and a small packet count. Treat the capture as sensitive evidence. Do not collect unrelated user traffic.

## Example 13 — Check proxy environment

```bash
env | grep -i proxy
```

A command-line client may use `HTTP_PROXY`, `HTTPS_PROXY`, or `NO_PROXY` settings. Redact credentials if any proxy URL contains them.

## Example 14 — Simulate a connection refusal locally

Terminal 1:

```bash
python3 -m http.server 18080 --bind 127.0.0.1
```

Terminal 2:

```bash
curl -v --max-time 3 http://127.0.0.1:18081/
curl -v --max-time 3 http://127.0.0.1:18080/
```

The first request will commonly fail because no service is listening on port 18081; the second should reach the demo server. Stop the demo server with `Ctrl+C` when done.

## Example 15 — A concise troubleshooting sequence

```bash
ip -br address
ip route
getent hosts <hostname>
nc -vz -w 3 <hostname> <port>
curl -v --connect-timeout 5 --max-time 15 https://<hostname>/
```

Run the sequence one step at a time and record where the first unexpected result occurs. Do not automatically change network settings based on a single failed probe.
