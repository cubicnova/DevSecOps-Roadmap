"""Parse JSON and validate its structure; never unpickle untrusted input."""
import json


def parse_profile(serialized: str) -> dict[str, str]:
    try:
        data = json.loads(serialized)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError("Invalid JSON input") from error

    if not isinstance(data, dict):
        raise ValueError("Profile must be a JSON object")
    if set(data) != {"username", "display_name"}:
        raise ValueError("Profile must contain only username and display_name")
    if not all(isinstance(data[key], str) for key in ("username", "display_name")):
        raise ValueError("Profile fields must be strings")
    if len(data["username"]) > 64 or len(data["display_name"]) > 100:
        raise ValueError("Profile field exceeds maximum length")
    return data


if __name__ == "__main__":
    sample = '{"username": "alice", "display_name": "Alice"}'
    print(parse_profile(sample))
