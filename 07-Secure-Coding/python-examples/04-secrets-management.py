"""Load a secret from the environment without printing its value."""
import os


def get_api_key() -> str:
    api_key = os.environ.get("DEMO_API_KEY")
    if not api_key or not api_key.strip():
        raise RuntimeError("DEMO_API_KEY is not configured")
    return api_key


if __name__ == "__main__":
    try:
        get_api_key()
        print("API key is configured; value not displayed.")
    except RuntimeError as error:
        print(error)
