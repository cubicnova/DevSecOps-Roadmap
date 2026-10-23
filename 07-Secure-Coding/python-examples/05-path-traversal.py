"""Basic path-containment check for a controlled educational lab."""
from pathlib import Path


def read_allowed_file(base_directory: Path, filename: str) -> str:
    """Read a file whose resolved path is inside the permitted directory."""
    base = base_directory.resolve()
    requested = (base / filename).resolve()
    try:
        requested.relative_to(base)
    except ValueError as error:
        raise ValueError("Access outside the permitted directory denied") from error

    if not requested.is_file():
        raise ValueError("Requested file does not exist")
    return requested.read_text(encoding="utf-8")


if __name__ == "__main__":
    root = Path("sample-files")
    root.mkdir(exist_ok=True)
    (root / "welcome.txt").write_text("Safe example", encoding="utf-8")
    print(read_allowed_file(root, "welcome.txt"))
