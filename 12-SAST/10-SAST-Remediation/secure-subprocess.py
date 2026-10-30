"""Illustrative constrained subprocess invocation."""

import subprocess

ALLOWED_REPORTS = {"daily.txt", "monthly.txt"}


def show_report(report_name):
    if report_name not in ALLOWED_REPORTS:
        raise ValueError("Unknown report")
    return subprocess.run(
        ["cat", f"/srv/reports/{report_name}"],
        shell=False,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
