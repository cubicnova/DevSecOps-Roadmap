# 08 — Load Balancers

Learn how load balancers distribute traffic across multiple servers, improve availability, and support scalable application delivery. This module covers core concepts, algorithms, health checks, reverse proxies, TLS termination, session persistence, and operational troubleshooting.

## Learning objectives

By the end of this module, you should be able to:

- Explain why load balancing is used and where it fits in a network/application architecture.
- Distinguish Layer 4 (transport) and Layer 7 (application) load balancing.
- Compare common balancing algorithms and select one for a workload.
- Explain health checks, failover, draining, sticky sessions, and TLS termination.
- Configure and test a small local NGINX reverse proxy/load-balancer lab.
- Identify common load-balancing failures using logs and command-line tools.
- Apply safe configuration practices, including restricted admin access and validated upstream health.

## Prerequisites

- Basic TCP/IP, DNS, ports, HTTP/HTTPS, and Linux command-line knowledge.
- Familiarity with `curl`, `ss`, and reading service logs.
- Docker is optional; the core concepts can be practised with local processes.

## 1. What is a load balancer?

A **load balancer** accepts client traffic and forwards each request or connection to one of several backend servers. The goal may be to improve throughput, distribute resource use, reduce single-server dependency, and enable maintenance without taking the whole application offline.

Typical request path:

```text
Client
  |
  v
DNS / Edge / Firewall
  |
  v
Load Balancer (listener :80 or :443)
  |                 |
  v                 v
Backend A         Backend B
  |                 |
  +------ Shared application/data dependencies ------+
```

A load balancer does not automatically make an application highly available. Backends, network paths, configuration, data stores, and the load balancer itself must all be considered.

## 2. Layer 4 vs Layer 7

| Property | Layer 4 | Layer 7 |
|---|---|---|
| Main information | TCP/UDP connection metadata | HTTP method, host, path, headers, cookies |
| Routing example | Send TCP port 443 connections to a pool | `/api/` to API servers, `/static/` to web servers |
| Protocol awareness | Limited application awareness | Application-aware |
| Typical use | High-throughput TCP/UDP forwarding | HTTP routing, redirects, header manipulation |
| TLS | May pass encrypted traffic through or terminate it, depending on product | Often terminates TLS and may re-encrypt to backends |

Exact capabilities vary by product. Layer 4 and Layer 7 are architectural descriptions, not guarantees about every feature.

## 3. Common balancing algorithms

- **Round robin:** distribute requests sequentially across eligible backends. Simple when capacity is similar.
- **Weighted round robin:** give higher-capacity backends a larger share.
- **Least connections:** prefer a backend with fewer active connections. Useful when connection duration varies.
- **Weighted least connections:** consider both active connections and backend capacity.
- **IP hash / source affinity:** map a client source address to a backend. NAT can cause many clients to share one source address.
- **Consistent hashing:** attempt to keep keys or clients mapped to the same backend while reducing remapping when pool membership changes.
- **Random / power of two choices:** choose randomly or compare a small sample of candidates; implementations vary.

Algorithm choice depends on request duration, backend capacity, statefulness, client distribution, and product behavior. Do not assume round robin means equal CPU use or equal response time.

## 4. Health checks and failover

Health checks determine whether a backend should receive new traffic.

- **TCP check:** can the target accept a TCP connection?
- **HTTP check:** does an endpoint return an expected status or response?
- **Readiness check:** is the application ready to serve requests, not merely running?
- **Passive checks:** infer health from actual traffic failures.

A good health endpoint should be lightweight and meaningful. Avoid exposing sensitive diagnostics publicly. Configure sensible intervals, timeouts, and failure thresholds to avoid flapping. A healthy response from one endpoint does not prove every dependency is healthy.

## 5. Reverse proxy and TLS termination

A reverse proxy receives client requests and forwards them to upstream services. A Layer 7 load balancer commonly behaves as a reverse proxy.

TLS may be:
1. **Terminated at the load balancer:** client TLS ends there; backend traffic may be HTTP or a separate TLS connection.
2. **Passed through:** the load balancer forwards the encrypted connection without inspecting HTTP content.
3. **Terminated and re-encrypted:** TLS is used on both client-to-balancer and balancer-to-backend legs.

Choose based on security requirements. If TLS is terminated at the balancer, protect the internal hop when the network or policy requires it. Trust forwarded headers only from known proxies, and do not let clients spoof identity or source-IP headers.

## 6. Session persistence and application state

**Sticky sessions** try to send a client back to the same backend. They may be useful for legacy applications that store session state locally, but they can cause uneven load and complicate failover.

Prefer external/shared session storage or stateless application design when practical. Never treat affinity as a replacement for secure session management. If a backend fails, a sticky session may still be lost unless session state is shared.

## 7. Availability and capacity concepts

- **Redundancy:** multiple backends, and where needed multiple load balancer instances/zones.
- **Failover:** stop sending new traffic to a failed or unhealthy backend.
- **Connection draining:** allow existing connections to finish while preventing new connections during maintenance.
- **Timeouts:** set connect, read, and idle timeouts consistently across proxies and applications.
- **Overload protection:** limit queues, requests, or connections according to the platform.
- **Observability:** collect request rate, latency, error rate, active connections, backend health, and saturation.
- **Single point of failure:** a single load balancer can itself become a critical dependency.

## 8. NGINX lab: two local backends

This lab uses three local ports on one machine. It is for learning and should not be exposed to the public internet.

### Step 1 — Create two simple backend servers

In separate terminals, run the following commands from a shell with Python 3 installed.

Terminal A:

```bash
mkdir -p /tmp/lb-demo-a
printf 'Hello from backend A\n' > /tmp/lb-demo-a/index.html
cd /tmp/lb-demo-a
python3 -m http.server 8081 --bind 127.0.0.1
```

Terminal B:

```bash
mkdir -p /tmp/lb-demo-b
printf 'Hello from backend B\n' > /tmp/lb-demo-b/index.html
cd /tmp/lb-demo-b
python3 -m http.server 8082 --bind 127.0.0.1
```

These Python servers are intentionally simple demo backends, not production application servers.

### Step 2 — Install NGINX

On Debian/Ubuntu-based Linux, if you are authorized to install packages:

```bash
sudo apt update
sudo apt install nginx
```

On other distributions, use the package manager and package name documented for that OS.

### Step 3 — Add a lab configuration

Create a separate file such as `/etc/nginx/conf.d/lb-demo.conf` (path may vary by distribution):

```nginx
upstream demo_backends {
    # Default upstream selection is round robin.
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

Binding to `127.0.0.1` keeps the demo listener local to the machine. Do not change it to a public interface unless you intentionally design and secure a reachable service.

### Step 4 — Validate and reload

```bash
sudo nginx -t
sudo systemctl reload nginx
```

If NGINX is not managed by systemd on your platform, use the service control method appropriate to the environment. Never reload a configuration that has failed validation.

### Step 5 — Send requests

```bash
for i in $(seq 1 8); do
  curl -s http://127.0.0.1:8080/
done
```

The output should show responses from both backends over repeated requests. Exact ordering depends on the configuration and request behavior.

### Step 6 — Observe listeners and logs

```bash
ss -lntp
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

Log locations vary by configuration. Use `nginx -T` only where you have permission; it prints the effective configuration and may reveal sensitive values if secrets have been embedded in configuration files.

### Step 7 — Simulate a backend failure

Stop one Python server with `Ctrl+C`, then repeat the `curl` loop. Basic open-source NGINX upstream behavior is not equivalent to active, configurable HTTP health checking in every commercial or third-party load-balancer product. Some failed requests may occur before failure is observed. Record the behavior rather than assuming instantaneous failover.

## 9. Troubleshooting checklist

1. **Client cannot connect:** confirm DNS, firewall rules, listener address, and listener port.
2. **502 Bad Gateway:** inspect upstream address/port, backend process state, and NGINX error logs.
3. **504 Gateway Timeout:** inspect backend latency, proxy timeout settings, network reachability, and dependency health.
4. **One backend gets all requests:** confirm both servers are reachable, the upstream config is loaded, and requests are actually reaching the proxy.
5. **Unexpected client IP:** check proxy trust boundaries and forwarded-header handling.
6. **TLS errors:** check certificate chain, hostname, expiry, protocol/cipher policy, and backend TLS verification.
7. **Uneven traffic:** compare backend capacity, long-lived connections, session affinity, request duration, and algorithm.
8. **Config change appears ignored:** run `nginx -t`, inspect the effective config, and confirm the correct service was reloaded.

## 10. Security best practices

- Keep administrative interfaces and management APIs on restricted networks.
- Use least privilege for service accounts and configuration files.
- Protect TLS private keys and rotate certificates before expiry.
- Validate configuration before reload and maintain a rollback path.
- Avoid placing secrets in logs, URLs, or public health responses.
- Restrict backend access so only intended proxy/load-balancer paths can reach services.
- Apply rate limiting and request-size limits where appropriate, but test them against legitimate traffic patterns.
- Trust `X-Forwarded-For` and similar headers only when supplied by known, controlled proxies.
- Monitor for traffic spikes, abnormal error rates, and backend saturation.

## 11. Review questions

1. What problem does a load balancer solve, and what problems does it not solve by itself?
2. Give two differences between Layer 4 and Layer 7 balancing.
3. When could least-connections be a better fit than round robin?
4. Why are readiness checks often more useful than checking only whether a port is open?
5. What is the difference between TLS termination and TLS pass-through?
6. What risks can sticky sessions introduce?
7. Explain connection draining.
8. What are three likely causes of a 502 response?
9. Why should forwarded headers be trusted only from known proxies?
10. How would you test backend failover without disrupting a production service?

## Further reading

- NGINX documentation: https://nginx.org/en/docs/
- NGINX HTTP load balancing: https://nginx.org/en/docs/http/load_balancing.html
- HAProxy documentation: https://docs.haproxy.org/
- AWS Elastic Load Balancing documentation: https://docs.aws.amazon.com/elasticloadbalancing/

## Suggested completion criteria

- [ ] Explain Layer 4 and Layer 7 balancing.
- [ ] Compare at least four algorithms.
- [ ] Configure and validate a local NGINX upstream.
- [ ] Demonstrate requests reaching both local backends.
- [ ] Record observed behavior after stopping one backend.
- [ ] Document one troubleshooting case and one security control.
