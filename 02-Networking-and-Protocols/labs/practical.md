# Networking and Protocols Labs — Practical Workbook

## Safety rules

Use your own system, a disposable VM, or an explicitly authorized lab. Do not scan or capture third-party traffic without permission. Keep demo services on loopback, avoid disabling security controls, and treat diagnostic output and packet captures as sensitive.

## Lab 01 — Interface and route discovery

**Tasks**
1. Run `ip -br link` and `ip -br address`.
2. Run `ip route`.
3. Run `ip route get <approved-destination-ip>`.
4. Record the selected interface, source address, and gateway if present.
5. Explain why a configured IP address does not guarantee connectivity.

**Deliverable:** A short baseline report.

## Lab 02 — DNS investigation

**Tasks**
1. Run `getent hosts example.com`.
2. Query A, AAAA, and MX records with `dig`.
3. If allowed, compare results using a specific resolver.
4. Explain `NXDOMAIN`, `SERVFAIL`, and timeout.
5. List two reasons corporate DNS might differ from public DNS.

**Deliverable:** A table of results and a conclusion supported by evidence.

## Lab 03 — TCP listeners and connection tests

1. Start `python3 -m http.server 18080 --bind 127.0.0.1`.
2. Run `ss -lntp`.
3. Test port 18080 with `nc -vz -w 3 127.0.0.1 18080`.
4. Test port 18081, where no server should be running.
5. Stop the server and repeat the port 18080 test.
6. Explain the difference between a refusal and a timeout.

**Deliverable:** Sanitized command output and explanation.

## Lab 04 — HTTP and TLS

1. Use `curl -sS -D - -o /dev/null https://example.com/`.
2. Use `curl -v --connect-timeout 5 --max-time 15 https://example.com/`.
3. Use `openssl s_client -connect example.com:443 -servername example.com </dev/null`.
4. Record status, redirects, certificate hostname, validity dates, and any error.
5. Explain why disabling certificate verification is not a permanent solution.

Use an approved hostname if external access is unavailable.

## Lab 05 — Path and performance

1. Run `ping -c 20 <approved-host>`.
2. Run `tracepath <approved-host>` or an approved alternative.
3. If available, run `mtr -rw -c 20 <approved-host>`.
4. Record latency and reported loss.
5. Explain why an intermediate hop may not answer probes even when it forwards traffic.

## Lab 06 — Limited packet capture

1. Identify the correct interface with `ip -br link`.
2. Run `sudo tcpdump -i <interface> -nn -c 100 port 53`.
3. In another terminal, trigger a DNS lookup.
4. Identify query/response packets if visible.
5. Explain why the packets may not appear and list three privacy precautions.

Do not broaden the capture without a clear, authorized reason.

## Lab 07 — Firewall and proxy review

1. Run `env | grep -i proxy`.
2. Inspect firewall status using the read-only tool for your OS.
3. Do not modify or flush any rules.
4. Draft a narrowly scoped firewall access request including source, destination, protocol, port, business reason, and review/expiry date.
5. Explain how you would verify an approved change.

## Lab 08 — Local load balancer

Start two backends in separate terminals.

Backend A:

```bash
mkdir -p /tmp/lb-lab-a
echo "Backend A" > /tmp/lb-lab-a/index.html
cd /tmp/lb-lab-a
python3 -m http.server 18081 --bind 127.0.0.1
```

Backend B:

```bash
mkdir -p /tmp/lb-lab-b
echo "Backend B" > /tmp/lb-lab-b/index.html
cd /tmp/lb-lab-b
python3 -m http.server 18082 --bind 127.0.0.1
```

Configure NGINX in the active include directory:

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
    }
}
```

**Tasks**
1. Confirm both backends respond directly.
2. Run `sudo nginx -t` and reload only if validation succeeds.
3. Send repeated requests through `http://127.0.0.1:18080/`.
4. Stop one backend and record behavior.
5. Remove only the dedicated lab configuration, validate again, and reload.

NGINX configuration paths vary. Keep the demo listener local; do not expose it publicly.

## Lab 09 — Troubleshooting scenario

A hostname is reported as unreachable. A tester says the IP address works, but HTTPS from one host fails intermittently.

**Tasks**
1. Record the initial questions you would ask.
2. Compare `getent hosts` and `dig`.
3. Inspect route selection with `ip route get`.
4. Test TCP 443 if permitted.
5. Inspect HTTPS with `curl -v` and certificate identity with OpenSSL.
6. List at least three hypotheses and the evidence needed to confirm or reject each.
7. Recommend the least disruptive next diagnostic step.

Do not assume a single root cause without evidence.

## Lab 10 — Incident report

Write a concise report including:
- Impact, scope, and time window.
- Expected versus observed behavior.
- Commands run and sanitized output.
- Recent changes and a known-good comparison.
- Root cause or best-supported hypothesis and confidence.
- Remediation, approval, rollback, and verification.
- Preventive follow-up actions.

## Submission checklist

- [ ] Baseline interface and route report.
- [ ] DNS results and interpretation.
- [ ] TCP listener/refusal comparison.
- [ ] HTTP/TLS diagnostic notes.
- [ ] Path and latency interpretation.
- [ ] Limited packet-capture notes and privacy controls.
- [ ] Firewall/proxy review.
- [ ] Load-balancer test and cleanup.
- [ ] Troubleshooting decision tree or hypothesis list.
- [ ] Final incident report with verification.
