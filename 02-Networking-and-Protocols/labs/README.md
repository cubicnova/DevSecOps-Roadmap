# Networking and Protocols — Labs

This folder contains guided, hands-on labs for practising networking and protocol concepts in a controlled environment. Labs progress from basic interface inspection to DNS, TCP, HTTP/TLS, routing, packet analysis, firewalls, and load balancing.

## Learning outcomes

After completing these labs, you should be able to:

- Inspect local network interfaces, addresses, routes, and listening sockets.
- Explain common DNS lookup results and diagnose basic resolution issues.
- Test TCP connectivity and distinguish a refusal from a timeout.
- Inspect HTTP responses and TLS certificate details.
- Observe traffic with `tcpdump` or Wireshark using narrow, authorized captures.
- Troubleshoot a local reverse proxy and backend service.
- Produce a concise evidence-based network incident report.
- Apply safe practices for scanning, packet capture, configuration changes, and handling diagnostic data.

## Lab safety and authorization

- Run labs on your own computer, a local VM, or an explicitly authorized environment.
- Do not scan, stress-test, or capture traffic from third-party systems without written permission.
- Keep demo services bound to `127.0.0.1` unless a lab explicitly requires a secured isolated network.
- Do not disable firewalls or certificate validation as a general troubleshooting fix.
- Packet captures and verbose client output may contain internal hostnames, IP addresses, cookies, tokens, and other sensitive data. Limit collection, redact before sharing, and follow retention policies.
- Commands that change routes, firewall rules, DNS settings, or services should be run only with appropriate authorization and a rollback plan.

## Suggested lab sequence

| Lab | Topic | Main tools | Estimated time |
|---|---|---|---:|
| 01 | Interface and route discovery | `ip`, `ss` | 20 min |
| 02 | DNS lookup investigation | `getent`, `dig` | 25 min |
| 03 | TCP ports and listeners | `ss`, `nc`, `curl` | 25 min |
| 04 | HTTP and HTTPS inspection | `curl`, `openssl` | 30 min |
| 05 | Path, latency, and loss | `ping`, `tracepath`, `mtr` | 30 min |
| 06 | Packet capture basics | `tcpdump`, Wireshark | 35 min |
| 07 | Local firewall and proxy review | `ufw`, `nft`, environment variables | 30 min |
| 08 | NGINX load-balancer lab | NGINX, Python HTTP server | 45 min |
| 09 | Troubleshooting scenario | Multiple tools | 40 min |
| 10 | Final network incident report | All relevant tools | 45 min |

Times are estimates and vary by operating system and setup.

## Requirements

Recommended:
- Linux VM or Linux host with shell access.
- Python 3.
- `curl`, `iproute2`, `iputils-ping`, and `dnsutils`/`bind-utils`.
- Optional: `netcat`, `traceroute` or `tracepath`, `mtr`, `tcpdump`, Wireshark, NGINX.
- `sudo` for selected administrative diagnostics.

Package names vary by distribution. Use your operating system's official package documentation.

## Lab 01 — Interface and route discovery

### Objective
Identify interface state, assigned addresses, and the route selected for a destination.

### Commands

```bash
ip -br link
ip -br address
ip route
ip route get 1.1.1.1
ss -lntup
```

### Tasks
1. Record interface names and link state.
2. Identify the default route and gateway, if present.
3. Run `ip route get` for a destination and record the selected interface/source address.
4. Identify three listening sockets, if any, using `ss`.
5. Explain why a host can have an IP address but still lack usable connectivity.

### Expected learning
Interface state, addressing, and routing are separate facts. A listening socket indicates a local service endpoint, not necessarily external reachability.

## Lab 02 — DNS lookup investigation

### Objective
Compare the operating-system resolver path with DNS query results.

### Commands

```bash
getent hosts example.com
dig example.com A
dig example.com AAAA
dig example.com MX
```

If policy permits, compare a specific resolver:

```bash
dig @1.1.1.1 example.com A
```

### Tasks
1. Record returned A and AAAA records.
2. Compare `getent` and `dig`.
3. Explain how VPNs, split-horizon DNS, search domains, and caches can affect results.
4. Describe the difference between `NXDOMAIN`, `SERVFAIL`, and a timeout.
5. Explain why a public resolver may not be appropriate for internal hostnames.

## Lab 03 — TCP ports and listeners

### Objective
Observe a listening TCP port and compare success with failure.

### Terminal A

```bash
python3 -m http.server 18080 --bind 127.0.0.1
```

### Terminal B

```bash
ss -lntp
nc -vz -w 3 127.0.0.1 18080
nc -vz -w 3 127.0.0.1 18081
curl -i --max-time 5 http://127.0.0.1:18080/
```

### Tasks
1. Confirm the server is listening.
2. Compare connection results for ports 18080 and 18081.
3. Explain connection refusal versus timeout.
4. Stop the server with `Ctrl+C` and repeat the test.
5. Explain why UDP diagnostics behave differently from TCP.

## Lab 04 — HTTP and HTTPS inspection

### Objective
Inspect response status, redirects, and TLS certificate details.

```bash
curl -sS -D - -o /dev/null https://example.com/
curl -v --connect-timeout 5 --max-time 15 https://example.com/
openssl s_client -connect example.com:443 -servername example.com </dev/null
```

### Tasks
1. Record the HTTP status and important response headers.
2. Identify any redirect and its `Location`.
3. Inspect the certificate hostname and validity dates.
4. List three possible causes of TLS handshake failure.
5. Explain why `curl -k` is not an appropriate permanent fix.

Use an approved hostname if external access is unavailable.

## Lab 05 — Path, latency, and loss

```bash
ping -c 20 example.com
tracepath example.com
```

Optional, if installed and allowed:

```bash
mtr -rw -c 20 example.com
```

### Tasks
1. Record latency and reported packet loss.
2. Identify responding and non-responding hops.
3. Explain why an intermediate hop may not reply even when forwarding traffic.
4. Compare ICMP results with an application-level `curl` test.
5. Explain the difference between latency, jitter, packet loss, and throughput.

## Lab 06 — Packet capture basics

### Objective
Collect a limited, authorized packet sample and identify DNS traffic.

```bash
ip -br link
sudo tcpdump -i <interface> -nn -c 100 port 53
```

While the capture runs, in another terminal:

```bash
dig example.com
```

### Tasks
1. Select the correct interface.
2. Identify the DNS query and response if visible.
3. Explain why DNS traffic might not appear (for example, encrypted DNS, a local cache, or wrong interface).
4. Explain what sensitive information a packet capture can contain.
5. Describe safe storage and deletion practices.

Do not broaden the capture beyond the lab need.

## Lab 07 — Firewall and proxy review

### Commands

```bash
env | grep -i proxy
```

Use the applicable read-only firewall inspection command:

```bash
sudo ufw status
# or
sudo nft list ruleset
```

### Tasks
1. Check whether proxy variables are set.
2. Explain how proxy settings can make command-line traffic take a different path.
3. Inspect firewall rules without modifying them.
4. Draft a narrowly scoped firewall change request with source, destination, protocol, port, business reason, and expiry/review date.
5. Explain why flushing rules or disabling the firewall is not a safe first diagnostic step.

## Lab 08 — Local NGINX load balancer

### Objective
Route local HTTP requests to two local backends.

Start backend A in Terminal A:

```bash
mkdir -p /tmp/lb-lab-a
echo "Backend A" > /tmp/lb-lab-a/index.html
cd /tmp/lb-lab-a
python3 -m http.server 18081 --bind 127.0.0.1
```

Start backend B in Terminal B:

```bash
mkdir -p /tmp/lb-lab-b
echo "Backend B" > /tmp/lb-lab-b/index.html
cd /tmp/lb-lab-b
python3 -m http.server 18082 --bind 127.0.0.1
```

Create a lab configuration file in the NGINX configuration include directory used by your distribution:

```nginx
upstream lab_backends {
    server 127.0.0.1:18081;
    server 127.0.0.1:18082;
}

server {
    listen 127.0.0.1:18080;
    server_name localhost;

    location / {
        proxy_pass http://lab_backends;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Validate and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Tasks
1. Verify both backends directly with `curl`.
2. Send repeated requests through `http://127.0.0.1:18080/`.
3. Record which backend responds.
4. Stop one backend and observe the result.
5. Explain the difference between passive failure handling and active health checks.
6. Remove the lab config after the exercise, then validate and reload NGINX again.

NGINX paths and service managers vary. Keep all listeners local and do not expose the demo publicly.

## Lab 09 — Troubleshooting scenario

### Scenario
A service is reported as unreachable by hostname. A second tester says that accessing the IP address works, but HTTPS from the affected host fails intermittently.

### Tasks
1. Write down the first five diagnostic questions you would ask.
2. Compare `getent hosts` with `dig`.
3. Check route selection with `ip route get`.
4. Test TCP port 443 with `nc` if permitted.
5. Inspect HTTPS with `curl -v`.
6. Check TLS certificate identity with `openssl s_client`.
7. Explain at least three hypotheses and what evidence would confirm or reject each.
8. Recommend the least disruptive next step.

Do not assume the scenario has one specific root cause; base the conclusion on your collected evidence.

## Lab 10 — Final incident report

Write a concise report for an intermittent connectivity issue.

Include:
- Summary, impact, and time window.
- Affected source hosts/users and destination service.
- Expected versus observed behavior.
- Commands run and sanitized evidence.
- Recent changes and comparison with a known-good path.
- Root cause or best-supported hypothesis and confidence.
- Remediation, approval, rollback, and verification.
- Preventive follow-up actions.

## Completion checklist

- [ ] Complete all 10 labs.
- [ ] Save sanitized command output or screenshots for each lab.
- [ ] Explain the limits of each diagnostic method.
- [ ] Include a clear root cause and verification in the final report.
- [ ] Remove lab services/configuration and securely handle any captures.
