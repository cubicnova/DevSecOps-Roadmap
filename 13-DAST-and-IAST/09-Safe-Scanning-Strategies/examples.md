# Safe Scanning Strategies - Examples

> These examples are for local disposable labs or explicitly authorized environments. Review the target and scope before running any scanner.

## 1. Confirm a local target
```bash
curl --fail --silent --show-error -I http://127.0.0.1:3000/
```
Confirm the response belongs to the intended lab application. Do not infer authorization from reachability.

## 2. Safe mode and Protected mode
In the ZAP UI, use the mode selector to choose:
- **Safe** when you want ZAP to prevent potentially dangerous operations.
- **Protected** when you want potentially dangerous operations allowed only for in-scope URLs.

Protected mode is only as safe as the Context and scope patterns you configure. Verify included and excluded URLs before scanning.

## 3. Define narrow scope
Example local-lab URL pattern:
```regex
^http://127\.0\.0\.1:3000/.*$
```
Example routes to review for exclusion:
```text
/logout
/account/delete
/admin/users/delete
/orders/submit
/payments/refund
```
These are illustrative route names. Use the actual routes from your application and exclude only what is necessary.

## 4. Passive baseline scan
```bash
docker run --rm -t \
  -v "$PWD:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://host.docker.internal:3000 \
  -r passive-baseline.html
```
The baseline scan performs spidering and passive analysis. Spidering can still interact with application routes, so use a local lab and review the target application's behavior. Container-to-host networking differs by platform; on Linux, configure an appropriate host gateway or isolated shared network.

## 5. Bounded readiness check
```bash
#!/usr/bin/env bash
set -euo pipefail
target="${TARGET_HEALTH_URL:-http://127.0.0.1:3000/}"

for attempt in {1..20}; do
  if curl --fail --silent "$target" >/dev/null; then
    echo "Target ready"
    exit 0
  fi
  sleep 2
done

echo "Target failed readiness check" >&2
exit 1
```

## 6. Example monitoring thresholds
```yaml
monitoring:
  max_scan_minutes: 15
  max_error_rate_percent: 5
  max_p95_latency_ms: 1500
  stop_on_unexpected_data_change: true
  stop_on_out_of_scope_request: true
```
This is a planning example, not a ZAP configuration schema. Choose thresholds with the application owner based on a measured baseline.

## 7. Example rules-of-engagement excerpt
```text
Target: isolated staging instance only
Window: approved maintenance window
Mode: Protected
Initial phase: passive baseline and limited crawl
Active scan: requires separate approval
Request rate: agreed conservative limit
Excluded: logout, delete, payment, outbound notification routes
Stop: elevated errors, latency, unexpected data changes, scope violation
Contacts: application owner and security lead
```

## 8. Example scan stop procedure
1. Stop the active scan using the ZAP UI or supported API control.
2. Confirm the scan status is stopped.
3. Check application health and recent side effects.
4. Notify the agreed owner/contact.
5. Preserve relevant logs and timestamps.
6. Do not perform unapproved data restoration.

ZAP exposes API actions for stopping scans; protect the API and use the current API documentation for exact endpoint and authentication requirements.

## 9. Example scan activity log
```text
Time (UTC): 2026-01-15T10:15:00Z
Target: local disposable training application
Mode: Protected
Phase: limited crawl
Observed: p95 latency increased beyond agreed threshold
Action: scan stopped; owner notified
Follow-up: environment reset and test repeated at lower intensity
```
Use the actual date/time and measured evidence in a real assessment.
