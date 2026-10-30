"""Inspect HTTP response headers on an authorized local training target."""
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

TARGET = "http://127.0.0.1:3000/"  # Change only to an authorized lab URL.

def main():
    request = Request(TARGET, headers={"User-Agent": "DAST-Learning-Lab/1.0"})
    try:
        with urlopen(request, timeout=5) as response:
            print(f"HTTP status: {response.status}")
            for name, value in response.headers.items():
                print(f"{name}: {value}")
    except HTTPError as exc:
        print(f"HTTP error: {exc.code}")
    except URLError as exc:
        print(f"Connection error: {exc.reason}")

if __name__ == "__main__":
    main()
