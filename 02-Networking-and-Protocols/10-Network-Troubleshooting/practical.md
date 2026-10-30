# Network Troubleshooting — Practical Exercises

## Safety and scope

Use your own Linux machine, a disposable VM, or an approved lab. Only scan or capture traffic for systems you administer or have permission to test. Avoid disabling firewalls, changing routes, or collecting broad packet captures as a first response.

## Lab 1 — Establish a baseline

**Tasks**
1. Record the current date/time and network interface names.
2. Run `ip -br link` and `ip -br address`.
3. Run `ip route` and `ip route get <approved-destination-ip>`.
4. Record the selected interface and source address.
5. Explain which outputs would be useful when comparing a working and failing host.

**Deliverable:** A short baseline report with sensitive data redacted where appropriate.

## Lab 2 — DNS resolution

**Tasks**
1. Query an approved public hostname with `getent hosts`.
2. Query its A and AAAA records with `dig`.
3. If policy permits, compare with a specific resolver using `dig @<resolver-ip> <hostname> A`.
4. Explain why public DNS and corporate DNS may legitimately return different results.
5. Write down two possible causes of `NXDOMAIN` and two causes of a timeout.

**Deliverable:** DNS comparison table and a conclusion supported by evidence.

## Lab 3 — TCP port diagnostics

**Tasks**
1. Use `ss -lntup` to inspect local listening sockets.
2. Start a local HTTP server on port 18080:
   `python3 -m http.server 18080 --bind 127.0.0.1`
3. In another terminal, run `nc -vz -w 3 127.0.0.1 18080`.
4. Test port 18081, where no demo server should be running.
5. Compare the success and failure messages. Explain why a timeout differs from a refusal.

**Deliverable:** Terminal output and a short explanation.

## Lab 4 — HTTP and TLS diagnosis

**Tasks**
1. Run `curl -sS -D - -o /dev/null https://example.com/`.
2. Run `curl -v --connect-timeout 5 --max-time 15 https://example.com/`.
3. Inspect the certificate using `openssl s_client -connect example.com:443 -servername example.com </dev/null`.
4. Record the HTTP status, redirect behavior, certificate validity window, and any relevant error.
5. Explain why disabling certificate verification is not an acceptable permanent fix.

Use an approved hostname if outbound access to `example.com` is unavailable.

## Lab 5 — Path and latency analysis

**Tasks**
1. Run `ping -c 20 <approved-host>`.
2. Run `tracepath <approved-host>` or an approved alternative.
3. If available, run `mtr -rw -c 20 <approved-host>`.
4. Record loss, round-trip time, and responding hops.
5. Explain why loss at an intermediate hop does not necessarily mean that hop is dropping forwarded application traffic.

## Lab 6 — Capture a small DNS trace

**Tasks**
1. Identify the interface with `ip -br link`.
2. Start a limited capture: `sudo tcpdump -i <interface> -nn -c 100 port 53`.
3. In another terminal, perform a DNS lookup.
4. Identify the query and response, where visible.
5. Stop after the packet limit or as soon as the evidence is collected.
6. Describe the privacy risks and storage controls for the capture.

If DNS is encrypted or traffic uses another interface, the expected packets may not be visible. Explain this limitation rather than changing security settings.

## Lab 7 — Diagnose a simulated web-service issue

Use a local demo server, not a third-party target.

**Tasks**
1. Start a local HTTP server on `127.0.0.1:18080`.
2. Verify it with `curl -i http://127.0.0.1:18080/`.
3. Stop it and repeat the request.
4. Record the client error and check `ss -lntp`.
5. Restart it and verify recovery.
6. Write a brief incident timeline with symptom, evidence, root cause, fix, and validation.

## Lab 8 — Firewall and proxy review

**Tasks**
1. Check whether proxy environment variables are set with `env | grep -i proxy`.
2. Inspect firewall status using the approved tool for your OS (for example, `sudo ufw status` or `sudo nft list ruleset`).
3. Do not change or flush rules.
4. Draft a narrowly scoped access request containing source, destination, protocol, port, business reason, and expiry/review date.
5. Explain how you would test the rule after approval.

## Lab 9 — Build a troubleshooting decision tree

Create a flowchart or checklist that begins with “The service is unreachable” and branches through:
- Name resolution.
- Route/interface.
- TCP connection.
- TLS handshake.
- HTTP status.
- Backend health or application logs.

For each branch, identify one test, one possible interpretation, and the next step.

## Lab 10 — Incident report

Write a one-page report for a hypothetical intermittent HTTPS timeout. Include:
- Impact and time window.
- Affected users and services.
- Expected and observed behavior.
- Commands run and sanitized evidence.
- Recent changes and comparison to a healthy path.
- Root cause or best-supported hypothesis, with confidence.
- Remediation, validation, and rollback.
- Preventive follow-up actions.

## Submission checklist

- [ ] Baseline interface and route report.
- [ ] DNS comparison and interpretation.
- [ ] TCP success/refusal comparison.
- [ ] HTTP/TLS diagnostic notes.
- [ ] Path/latency interpretation.
- [ ] Limited packet-capture notes and privacy controls.
- [ ] Local service failure timeline.
- [ ] Firewall/proxy review.
- [ ] Troubleshooting decision tree.
- [ ] Incident report with verification evidence.
