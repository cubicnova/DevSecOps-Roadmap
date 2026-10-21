# Load Balancers — Examples

These examples are for learning and authorized local environments. Adapt paths and service commands to your operating system.

## Example 1 — Round-robin upstream in NGINX

```nginx
upstream app_pool {
    server 127.0.0.1:8081;
    server 127.0.0.1:8082;
}

server {
    listen 127.0.0.1:8080;

    location / {
        proxy_pass http://app_pool;
    }
}
```

**What it demonstrates:** NGINX distributes requests across eligible upstream servers using round robin by default.

**Try it:** Start two local HTTP backends, validate with `sudo nginx -t`, reload NGINX, then run repeated `curl` requests.

## Example 2 — Weighted upstreams

```nginx
upstream app_pool {
    server 127.0.0.1:8081 weight=3;
    server 127.0.0.1:8082 weight=1;
}
```

**Interpretation:** Under suitable conditions, the first server receives approximately three times the share of the second. This is not a promise of equal CPU usage or an exact ratio over a small number of requests.

## Example 3 — Least-connections selection

```nginx
upstream app_pool {
    least_conn;
    server 127.0.0.1:8081;
    server 127.0.0.1:8082;
}
```

**Use case:** Requests or connections may last for different durations. Least-connections can help distribute active connection counts, but it does not directly measure CPU, queue depth, or request cost.

## Example 4 — Forwarding useful request headers

```nginx
location / {
    proxy_pass http://app_pool;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**Security note:** The backend should trust forwarded headers only when the request came through a trusted proxy. Direct client-supplied values can otherwise be spoofed.

## Example 5 — Mark a backend as unavailable

```nginx
upstream app_pool {
    server 127.0.0.1:8081;
    server 127.0.0.1:8082 down;
}
```

**Use case:** Temporarily exclude a backend through a controlled configuration change. Validate before reload and restore the server when appropriate.

## Example 6 — Passive failure handling parameters

```nginx
upstream app_pool {
    server 127.0.0.1:8081 max_fails=3 fail_timeout=10s;
    server 127.0.0.1:8082 max_fails=3 fail_timeout=10s;
}
```

These parameters influence passive failure handling in NGINX; they are not the same as a universal active HTTP health-check system. Behavior also depends on NGINX version, upstream type, and configuration.

## Example 7 — Validate before reloading

```bash
sudo nginx -t && sudo systemctl reload nginx
```

The reload only runs if the configuration test succeeds. If your system does not use systemd, replace the service command with the correct one for your platform.

## Example 8 — Check local listeners

```bash
ss -lntp
```

Look for the proxy listener and backend ports. If a port is absent, confirm the process is running and bound to the expected address.

## Example 9 — Inspect HTTP response status

```bash
curl -i --max-time 5 http://127.0.0.1:8080/
```

- `200` commonly indicates a successful HTTP response.
- `502` often indicates the proxy could not obtain a valid upstream response.
- `504` commonly indicates an upstream timeout.

Use logs and backend checks to establish the actual cause.

## Example 10 — Simple request sampling

```bash
for i in $(seq 1 10); do
  printf 'Request %s: ' "$i"
  curl -sS --max-time 3 http://127.0.0.1:8080/ || echo "request failed"
done
```

Use this only against your own local lab or an authorized test environment. This is a small functional test, not a performance or stress test.

## Example 11 — TLS termination design sketch

```text
Client -- HTTPS --> Load Balancer -- HTTPS --> Backend
```

The load balancer terminates the client TLS connection and creates a separate TLS connection to the backend. Configure certificate validation for the backend hop where supported and required; do not assume encryption alone validates the backend identity.

## Example 12 — Choosing an algorithm

| Situation | Possible starting point | Considerations |
|---|---|---|
| Similar servers and short requests | Round robin | Simple baseline |
| Different backend capacities | Weighted round robin | Reassess weights as capacity changes |
| Uneven connection durations | Least connections | Active connection count is only a proxy for work |
| Client affinity needed for legacy state | Source/cookie affinity | Can cause hotspots and complicate failover |
| Routing based on URL path or host | Layer 7 rules | Validate routing precedence and prevent unsafe exposure |

## Cleanup

Remove the lab configuration and stop the two Python servers when finished. Before deleting any file, verify the path is the dedicated lab file rather than a production configuration.
