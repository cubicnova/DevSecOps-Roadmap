"""Use a fixed allowlist of subprocess argument lists."""
import subprocess

ALLOWED_ACTIONS = {
    "status": ["git", "status", "--short"],
    "branch": ["git", "branch", "--show-current"],
}


def run_action(action: str) -> str:
    if action not in ALLOWED_ACTIONS:
        raise ValueError("Unsupported action")
    result = subprocess.run(
        ALLOWED_ACTIONS[action],
        shell=False,
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    return result.stdout


if __name__ == "__main__":
    selected_action = input("Choose status or branch: ").strip()
    try:
        print(run_action(selected_action))
    except ValueError:
        print("Unsupported action")
    except (subprocess.SubprocessError, OSError) as error:
        print("Action failed:", type(error).__name__)
