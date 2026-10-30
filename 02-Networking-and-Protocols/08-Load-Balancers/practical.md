# Load Balancers — Practical Exercises

## Lab safety

Use a local machine, disposable VM, or environment you are authorized to administer. Keep the demo listener bound to loopback (`127.0.0.1`) unless you have a deliberate, secured network design. Do not load-test public or third-party services without written authorization.

## Lab 1 — Draw a load-balanced architecture

**Tasks**
1. Draw a client, load balancer, two application backends, and a database.
2. Label listener ports and protocol for each hop.
3. Mark where TLS terminates.
4. Identify possible single points of failure.
5. Propose one improvement for each single point of failure.

**Evidence:** Save a diagram or a short written architecture.

## Lab 2 — Start two backends

Run in separate terminals:

Backend A:

```bash
mkdir -p /tmp/lb-demo-a
echo "Hello from backend A" > /tmp/lb-demo-a/index.html
cd /tmp/lb-demo-a
python3 -m http.server 8081 --bind 127.0.0.1
```

Backend B:

```bash
mkdir -p /tmp/lb-demo-b
echo "Hello from backend B" > /tmp/lb-demo-b/index.html
cd /tmp/lb-demo-b
python3 -m http.server 8082 --bind 127.0.0.1
```

**Tasks**
- Verify each backend directly with `curl http://127.0.0.1:8081/` and `curl http://127.0.0.1:8082/`.
- Use `ss -lntp` to confirm listeners.
- Record what happens if one server is stopped.

## Lab 3 — Configure NGINX as a reverse proxy

Create `/etc/nginx/conf.d/lb-demo.conf` if that directory is used on your distribution:

```nginx
upstream demo_backends {
    server 127.0.0.1:8081;
    server 127.0.0.1:8082;
}

server {
    listen 127.0.0.1:8080;
    server_name localhost;

    location / {
        proxy_pass http://demo_backends;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Tasks**
1. Check that the include path is enabled in the active NGINX configuration.
2. Run `sudo nginx -t`.
3. Reload only after a successful test.
4. Send at least eight requests to `http://127.0.0.1:8080/`.
5. Record which backend answered each request.

## Lab 4 — Compare algorithms

Make one change at a time and validate the configuration before reloading.

**Tasks**
- Test the default round-robin configuration.
- Test `weight=3` on backend A and `weight=1` on backend B.
- Test `least_conn;`.
- Describe whether the output matches your expectation and why a small sample may not demonstrate the intended distribution precisely.
- Explain which metrics you would collect before selecting an algorithm for production.

## Lab 5 — Backend failure observation

**Tasks**
1. Send requests while both backends are running.
2. Stop backend A.
3. Continue a small number of requests.
4. Record status codes, response bodies, and relevant error-log lines.
5. Restart backend A and observe recovery.
6. Explain the difference between passive failure detection and active health checks.

Do not assume every failed backend is removed immediately in every load-balancer implementation.

## Lab 6 — Troubleshoot a 502

Create a troubleshooting record with:
- Client request and timestamp.
- Proxy listener status.
- Backend process and port status.
- `curl` results to each backend directly.
- Relevant proxy error-log lines.
- Root cause and fix.
- Verification after the fix.

Avoid pasting secrets, cookies, authorization headers, or private keys into the report.

## Lab 7 — Forwarded-header trust

**Tasks**
1. Explain the purpose of `X-Forwarded-For` and `X-Forwarded-Proto`.
2. Explain how a client might spoof a forwarded header if the application trusts all sources.
3. Design a trust rule that accepts proxy headers only from the known load-balancer path.
4. State what should happen to untrusted client-supplied forwarding headers.

## Lab 8 — TLS and certificate planning

Prepare a short design for HTTPS at the load balancer:
- Certificate storage and access control.
- Renewal and expiry monitoring.
- Backend transport (HTTP or HTTPS) and why.
- Backend certificate validation requirements.
- How clients reach the service during certificate rotation.
- Rollback steps if the new configuration fails validation.

Do not use real private keys in a learning repository.

## Lab 9 — Capacity and observability

Create a monitoring checklist for:
- Request rate.
- p50, p95, and p99 latency.
- 4xx and 5xx rates.
- Active connections and queue depth, if available.
- Backend health and saturation.
- Load-balancer CPU/memory.
- TLS handshake failures.
- Configuration changes and deployment events.

For each metric, explain one symptom it could help detect.

## Lab 10 — Production-readiness review

Review a hypothetical service with two backends and one load balancer. Identify at least eight questions across:
- Redundancy and failover.
- Health checks.
- Timeouts and retries.
- TLS.
- Logging and alerting.
- Access control.
- Connection draining.
- Deployment and rollback.

## Submission checklist

- [ ] Architecture diagram or written design.
- [ ] Backend verification output.
- [ ] NGINX configuration and successful syntax-test evidence.
- [ ] Request-distribution observations.
- [ ] Failure scenario report.
- [ ] 502 troubleshooting record.
- [ ] Forwarded-header trust explanation.
- [ ] TLS plan and monitoring checklist.
