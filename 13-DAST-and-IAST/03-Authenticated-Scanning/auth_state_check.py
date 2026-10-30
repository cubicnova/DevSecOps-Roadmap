"""Check whether a bearer token represents an authenticated lab user.

Set DAST_TEST_TOKEN in the environment. This script intentionally does not
print the token or the complete response body.
"""
import os
import requests

BASE_URL = os.getenv("DAST_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
TOKEN = os.getenv("DAST_TEST_TOKEN")

def main():
    if not TOKEN:
        raise SystemExit("Set DAST_TEST_TOKEN in the environment.")

    response = requests.get(
        f"{BASE_URL}/api/me",
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=10,
    )
    print("HTTP status:", response.status_code)

    if response.status_code == 200:
        try:
            payload = response.json()
        except ValueError:
            print("Unexpected non-JSON response; inspect securely.")
            return
        print("Authenticated identity marker present:", bool(payload.get("username")))
    elif response.status_code == 401:
        print("Not authenticated: token may be missing, invalid, or expired.")
    elif response.status_code == 403:
        print("Access denied: check the identity's permissions.")
    else:
        print("Unexpected response; inspect securely in the authorized lab.")

if __name__ == "__main__":
    main()
