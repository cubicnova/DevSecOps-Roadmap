"""Create a uniquely named temporary file safely."""
import tempfile
from pathlib import Path


def write_report(content: str) -> Path:
    """Create a temporary report; caller is responsible for cleanup."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="secure-report-",
        suffix=".txt",
        delete=False,
    ) as report:
        report.write(content)
        return Path(report.name)


if __name__ == "__main__":
    report_path = write_report("Security exercise completed.")
    print("Report created:", report_path)
    print("Remove the file after reviewing the exercise.")
