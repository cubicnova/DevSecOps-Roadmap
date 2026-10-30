# APIs and Requests — Python Examples

Install the dependency:

```bash
python -m pip install requests
```

Examples use public test APIs. Run only against endpoints you are authorized to use.

## 1. Make a GET request

```python
import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/posts/1",
    timeout=10,
)
response.raise_for_status()
post = response.json()
print(post["title"])
```

## 2. Add query parameters

```python
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1},
    timeout=(3, 10),
)
response.raise_for_status()
posts = response.json()
print("Records:", len(posts))
```

Passing parameters with `params=` lets Requests encode the query string.

## 3. Inspect status and headers

```python
print(response.status_code)
print(response.headers.get("Content-Type", "unknown"))
```

Do not assume a response is JSON solely because the request succeeded.

## 4. Send a JSON POST request

```python
payload = {"title": "sample", "body": "training data", "userId": 1}
response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=payload,
    timeout=10,
)
response.raise_for_status()
print(response.status_code, response.json())
```

JSONPlaceholder simulates writes; it does not persist the created record.

## 5. Set request headers

```python
headers = {
    "Accept": "application/json",
    "User-Agent": "DevSecOps-Learning-Lab/1.0",
}
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts/1",
    headers=headers,
    timeout=10,
)
response.raise_for_status()
```

Never place real secrets in a public repository or notebook output.

## 6. Handle request errors

```python
import requests

try:
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1",
        timeout=(3, 10),
    )
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("The request timed out.")
except requests.exceptions.HTTPError as exc:
    print(f"HTTP error: {exc}")
except requests.exceptions.ConnectionError:
    print("Could not connect to the API.")
except requests.exceptions.RequestException as exc:
    print(f"Request failed: {exc}")
```

## 7. Validate JSON structure

```python
data = {"id": 1, "title": "Example"}

if not isinstance(data, dict):
    raise ValueError("Expected a JSON object")
if not isinstance(data.get("id"), int):
    raise ValueError("Missing or invalid id")
```

Validate the fields and types your application actually needs.

## 8. Reuse a session

```python
import requests

with requests.Session() as session:
    session.headers.update({"Accept": "application/json"})
    response = session.get(
        "https://jsonplaceholder.typicode.com/posts/1",
        timeout=10,
    )
    response.raise_for_status()
    record = response.json()
```

Sessions can reuse connections and common settings.

## 9. Read a token from an environment variable

```python
import os

api_token = os.environ.get("TRAINING_API_TOKEN")
if not api_token:
    raise RuntimeError("Set TRAINING_API_TOKEN in your environment")

# Example only: use the authentication scheme documented by your API.
headers = {"Authorization": f"Bearer {api_token}"}
```

Do not print `headers` or commit a real token. This snippet intentionally does not send the token to a public test endpoint.

## 10. Pagination template

```python
import requests

all_records = []
page = 1
page_size = 20

while True:
    response = requests.get(
        "https://example.invalid/api/records",
        params={"page": page, "limit": page_size},
        timeout=10,
    )
    # Replace example.invalid with an API you own or may use.
    response.raise_for_status()
    batch = response.json()
    if not batch:
        break
    all_records.extend(batch)
    if len(batch) < page_size:
        break
    page += 1
```

This is a template: pagination parameter names and response shape depend on the API. `.invalid` is a reserved example domain and will not resolve.

## 11. Respect rate limits

```python
if response.status_code == 429:
    print("Rate limit reached. Follow the API's documented retry policy.")
```

For production clients, follow documented `Retry-After` behavior and bounded backoff. Do not retry indefinitely.

## 12. Write a JSON report

```python
import json
from pathlib import Path

report = {"records_received": 1, "source": "public-test-api"}
Path("api_report.json").write_text(
    json.dumps(report, indent=2),
    encoding="utf-8",
)
```
