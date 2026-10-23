# Examples: Security Logging

Use synthetic data and systems you are authorized to administer. Never put real secrets in a test log.

## 1. Basic Python logging
```python
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("demo.auth")
logger.info("authentication succeeded")
logger.warning("authentication failed")
```

## 2. Emit a structured JSON event
```python
import json
from datetime import datetime, timezone

event = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "severity": "WARN",
    "event": "auth.login_failed",
    "outcome": "failure",
    "actor_id": "user-demo-17",
    "source_ip": "192.0.2.25",  # documentation-only address
    "service": "sample-api",
    "environment": "lab",
    "request_id": "req-demo-0001",
    "reason": "invalid_credentials",
}
print(json.dumps(event, separators=(",", ":"), ensure_ascii=False))
```

## 3. Redact sensitive fields
```python
SENSITIVE_KEYS = {"password", "passwd", "authorization", "access_token",
                  "refresh_token", "session_cookie", "api_key", "private_key"}

def redact(event):
    return {k: ("[REDACTED]" if k.lower() in SENSITIVE_KEYS else v)
            for k, v in event.items()}

print(redact({"event": "auth.login_failed", "password": "never-log-this"}))
```
This is a minimal example. Production redaction must handle nested objects, headers, URLs, exceptions, and schema changes. Safer still: never pass secrets to the logger.

## 4. Validate event names and bound untrusted fields
```python
import json
import re

EVENT_NAME = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$")

def safe_event(event_name, supplied_reason):
    if not EVENT_NAME.fullmatch(event_name):
        raise ValueError("invalid event name")
    return json.dumps({"event": event_name, "reason": supplied_reason[:200]})
```
Use structured serialization, bound field lengths, and test the actual viewer and downstream parsers. Parameterized logging alone does not guarantee protection from CR/LF injection.

## 5. Write JSON Lines
```python
import json
from datetime import datetime, timezone
from pathlib import Path

def write_event(path, event_name, outcome):
    event = {"timestamp": datetime.now(timezone.utc).isoformat(),
             "event": event_name, "outcome": outcome, "service": "local-lab"}
    with Path(path).open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event) + "\n")

write_event("security-events.jsonl", "auth.login_failed", "failure")
```
This teaching example does not implement rotation, centralized forwarding, or access controls.

## 6. Count failed logins by source IP
```python
import json
from collections import Counter
from pathlib import Path

counts = Counter()
for line in Path("sample-security-events.jsonl").read_text(encoding="utf-8").splitlines():
    event = json.loads(line)
    if event.get("event") == "auth.login_failed":
        counts[event.get("source_ip", "unknown")] += 1
print(counts)
```
Production detection should also consider time windows, distinct accounts, successful logins after failures, baselines, and false positives.

## 7. Command-line inspection
```bash
tail -n 50 app.log
grep -i 'auth.login_failed' app.log
tail -f app.log
jq 'select(.event == "auth.login_failed")' sample-security-events.jsonl
journalctl -u ssh --since "1 hour ago"
```
Commands and service names vary by platform.

## Never log directly
Passwords, one-time codes, session cookies, bearer tokens, private keys, database credentials, full payment-card data, or unnecessary sensitive personal data. Prefer safe categories and correlation IDs.
