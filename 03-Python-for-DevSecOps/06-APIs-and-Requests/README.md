# 06 — APIs and HTTP Requests with Python

Learn to communicate with web APIs using Python, inspect HTTP responses, send parameters and headers, work with JSON, and handle errors safely. These skills support DevSecOps automation, cloud integrations, security reporting, and defensive monitoring.

## Learning objectives

- Explain APIs, HTTP methods, status codes, headers, and JSON payloads.
- Make GET and POST requests using the `requests` library.
- Pass query parameters and request headers.
- Parse JSON responses and handle common errors and timeouts.
- Use sessions and configure request timeouts.
- Apply safe practices for credentials, TLS verification, and untrusted API responses.
- Build a small API-driven report using a public test API.

## Topics covered

| Topic | Key ideas | DevSecOps use case |
|---|---|---|
| API and HTTP basics | Endpoints, methods, status codes | Integrate security tools |
| GET requests | Retrieve data, query parameters | Fetch test records |
| POST requests | Submit JSON payloads | Submit a test event |
| Headers | `Accept`, `Content-Type`, authorization | Content negotiation and authentication |
| JSON | `response.json()`, `json=` | Parse structured responses |
| Response handling | `status_code`, `raise_for_status()` | Detect failed requests |
| Timeouts | Connect and read timeouts | Prevent indefinite waits |
| Sessions | Reuse connection settings | Repeated API requests |
| Pagination and rate limits | Page through results, HTTP 429 | Respect service limits |
| Secure API use | TLS verification, secret management, validation | Reduce integration risk |

## Prerequisites

- Python fundamentals, dictionaries, JSON, and exception handling.
- Python 3.10 or later recommended.
- Internet access for optional live API exercises.

## Setup

Install Requests and Jupyter:

```bash
python -m pip install requests jupyter
jupyter notebook
```

## Suggested learning path

1. Review [`examples.md`](examples.md).
2. Complete [`practical.ipynb`](practical.ipynb), starting with offline exercises.
3. Run live API exercises only when internet access is available.
4. Compare your work with [`solutions.md`](solutions.md).

## Mini project: API Security Event Reporter

Retrieve sample records from a test API, validate the response structure, count selected categories, and write a JSON report.

Use public test data and authorized endpoints only. Do not scan, fuzz, or send high-volume requests to third-party services without explicit permission.

## HTTP quick reference

| Method | Common purpose |
|---|---|
| `GET` | Retrieve a resource |
| `POST` | Submit data or create a resource |
| `PUT` | Replace a resource |
| `PATCH` | Partially update a resource |
| `DELETE` | Delete a resource |

| Status | Typical meaning |
|---|---|
| `200` | OK |
| `201` | Created |
| `204` | Success with no response body |
| `400` | Bad request |
| `401` | Authentication required or failed |
| `403` | Forbidden |
| `404` | Not found |
| `429` | Too many requests |
| `500` | Server error |

## Secure coding checklist

- Always set a reasonable timeout.
- Call `raise_for_status()` or explicitly check the status before trusting the response.
- Keep TLS certificate verification enabled (`verify=True`, the default).
- Never hardcode API keys or commit secrets to Git.
- Avoid printing authorization headers, tokens, or sensitive response data.
- Validate response content and types; successful HTTP status does not guarantee valid data.
- Respect API terms, rate limits, pagination rules, and authorization boundaries.
- Use only endpoints you own or are authorized to access.

## Completion checklist

- [ ] Explain common HTTP methods and status codes.
- [ ] Make a GET request with query parameters.
- [ ] Send JSON in a POST request.
- [ ] Parse and validate JSON responses.
- [ ] Handle timeout, connection, and HTTP errors.
- [ ] Explain API key hygiene, TLS verification, and rate limits.

## Further reading

- [Requests documentation](https://requests.readthedocs.io/en/latest/)
- [Requests quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
- [HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [JSONPlaceholder test API](https://jsonplaceholder.typicode.com/)
