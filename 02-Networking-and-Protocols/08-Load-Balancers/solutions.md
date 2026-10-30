# Load Balancers — Solutions and Explanations

Use these as reference answers after attempting the practical exercises. Your exact output can differ by OS, NGINX version, service manager, and timing.

## Lab 1 — Architecture

A typical design is:

```text
Client -- HTTPS --> Load Balancer -- HTTPS or HTTP --> App A
                                      |-------------> App B
                                                        |
                                                        v
                                                   Shared database
```

The load balancer distributes incoming traffic across eligible application instances. If there is only one load balancer, it may remain a single point of failure. The database may also be a single point of failure unless its own availability design addresses that risk.

Possible improvements include redundant load balancers, multiple availability zones, health checks, shared session storage, replicated data services, and tested failover procedures. The correct choices depend on service requirements and budget.

## Lab 2 — Backend verification

Expected commands:

```bash
curl -i http://127.0.0.1:8081/
curl -i http://127.0.0.1:8082/
ss -lntp
```

The response body should identify backend A or B. If the connection fails, check that the process is still running, the command was started from the intended directory, and the server is bound to `127.0.0.1` on the expected port.

## Lab 3 — NGINX reverse proxy

A minimal working upstream is:

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

Validate and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

The file path and service manager may vary. If the test fails, fix the reported syntax or include-path issue before reloading. If the proxy is unreachable, verify it actually listens on `127.0.0.1:8080`.

## Lab 4 — Algorithms

- **Round robin:** a simple baseline for similar backends. It distributes eligible requests/connections according to the implementation.
- **Weighted round robin:** gives the higher-weight backend a greater share over time; short samples may not show exact ratios.
- **Least connections:** selects based on active connection counts, which may help with uneven connection durations but does not directly measure CPU or request complexity.

Collect request rate, latency percentiles, backend error rate, active connections, queue depth, resource saturation, and workload-specific request cost. Test using representative, authorized traffic rather than assuming one algorithm is universally best.

## Lab 5 — Failure observation

When a backend is stopped, the proxy may initially attempt to use it and return an error before passive failure handling changes selection. Exact behavior depends on version, upstream configuration, and the number of available backends.

A complete report should include:
- Time the backend was stopped and restarted.
- HTTP status codes and response bodies.
- Whether requests continued to reach the healthy backend.
- Error-log entries.
- How and when the failed backend became usable again.

**Active health checks** periodically probe backend readiness. **Passive failure handling** infers failure from actual traffic. Feature availability depends on the load-balancer product and edition.

## Lab 6 — 502 troubleshooting

A good investigation proceeds from the outside inward:

1. Confirm the proxy listener is running.
2. Request each backend directly.
3. Confirm configured upstream addresses and ports.
4. Read the proxy error log at the matching timestamp.
5. Check firewall rules, process crashes, and address binding.
6. Apply the smallest safe fix and validate configuration.
7. Repeat the original request and confirm normal logs.

Common causes include a stopped backend, wrong upstream port, refused connection, incorrect socket permissions, or invalid upstream response. A 502 is a symptom, not a root cause.

## Lab 7 — Forwarded-header trust

Forwarded headers help an application learn the original client scheme or address after a proxy. If an application trusts headers from arbitrary clients, an attacker may supply a false IP or scheme and influence logging, access controls, redirects, or rate limits.

A safer design accepts forwarding metadata only from known proxy addresses and prevents direct client access to the backend where practical. The edge proxy should establish or sanitize the headers according to a documented trust model.

## Lab 8 — TLS plan

A reasonable plan includes:
- Store private keys with restrictive permissions and limited operator access.
- Automate renewal and alert before expiry.
- Choose HTTP or HTTPS to backends based on the threat model and policy.
- If using HTTPS upstream, validate the backend certificate and hostname where supported.
- Test configuration before deployment and keep a known-good rollback version.
- Monitor handshake errors and certificate expiration.

Never commit private keys or production certificates with embedded private material to a public repository.

## Lab 9 — Metrics

| Metric | Example signal |
|---|---|
| Request rate | Sudden traffic increase or unexpected drop |
| p95/p99 latency | Slow tail requests despite acceptable average latency |
| 5xx rate | Application or upstream failures |
| Active connections | Connection buildup or overloaded backend |
| Backend health | Instance failing readiness checks |
| CPU/memory | Saturation or resource leak |
| TLS handshake errors | Certificate or protocol mismatch |
| Deployment events | Correlation between a change and new failures |

Metrics need context and thresholds based on a normal baseline. Alerting on a single noisy metric can create false positives.

## Lab 10 — Production-readiness questions

A strong review asks:
1. Is the load balancer redundant?
2. Are backends spread across independent failure domains?
3. Does the health check test readiness rather than only port reachability?
4. Are timeouts consistent across the proxy and application?
5. Are retries safe for non-idempotent operations?
6. Is TLS configured and renewed safely?
7. Are forwarding headers trusted only from controlled proxies?
8. Are logs, latency, saturation, and backend health monitored?
9. Is connection draining configured for maintenance?
10. Is there a tested rollback plan?
11. Are administrative endpoints restricted?
12. Has failover been tested in a staging environment?

## Key takeaways

- Load balancing improves distribution and can support availability, but it is not a complete high-availability strategy by itself.
- Health checks, timeouts, logging, TLS, and backend access controls are as important as the balancing algorithm.
- Validate configuration before reload and test failure behavior in a controlled environment.
