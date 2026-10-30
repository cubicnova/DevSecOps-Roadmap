# Solutions — APIs and Requests

Reference solutions for the exercises in `practical.ipynb`. Live API cells require internet access and the test service to be available.

## 1. GET one record

```python
response = requests.get(f"{BASE_URL}/posts/1", timeout=10)
response.raise_for_status()
record = response.json()
print(record["id"], record["title"])
```

## 2. Filter with query parameters

```python
response = requests.get(
    f"{BASE_URL}/posts",
    params={"userId": 1},
    timeout=10,
)
response.raise_for_status()
user_posts = response.json()
assert all(post["userId"] == 1 for post in user_posts)
```

## 3. Send a JSON POST

```python
payload = {"title": "training", "body": "sample payload", "userId": 1}
response = requests.post(f"{BASE_URL}/posts", json=payload, timeout=10)
response.raise_for_status()
created = response.json()
print(created)
```

The test API may return a simulated ID; the data is not permanently stored.

## 4. Handle failures

```python
try:
    response = requests.get(f"{BASE_URL}/posts/1", timeout=(3, 10))
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("Timed out")
except requests.exceptions.HTTPError as exc:
    print("HTTP status error:", exc)
except requests.exceptions.ConnectionError:
    print("Connection failed")
except requests.exceptions.RequestException as exc:
    print("Request error:", exc)
```

## 5. Validate the response

```python
def validate_post(record):
    if not isinstance(record, dict):
        raise ValueError("Expected an object")
    if not isinstance(record.get("id"), int):
        raise ValueError("Expected integer id")
    if not isinstance(record.get("title"), str):
        raise ValueError("Expected string title")
    return record
```

Validation should match the actual API schema and fields your application relies on.

## 6. Build a report

```python
from collections import Counter
import json
from pathlib import Path

response = requests.get(f"{BASE_URL}/posts", timeout=10)
response.raise_for_status()
posts = response.json()

if not isinstance(posts, list):
    raise ValueError("Expected a list of posts")

user_counts = Counter(
    post["userId"]
    for post in posts
    if isinstance(post, dict) and isinstance(post.get("userId"), int)
)

report = {
    "total_posts": len(posts),
    "posts_per_user": dict(user_counts),
}
Path("api_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
```

## 7. Key concepts

- `params=` encodes query parameters.
- `json=` serializes a Python object as JSON and sets the JSON content type.
- `raise_for_status()` raises an HTTP error for unsuccessful status codes.
- A timeout limits how long a request waits for network activity; it is not a strict total-workflow deadline.
- TLS verification should remain enabled.
- API tokens should come from a secret manager or environment variable, not source code.
- A successful status code does not prove the response has the expected schema.
- Retry only according to the API's documented rules, with bounded attempts and backoff.
