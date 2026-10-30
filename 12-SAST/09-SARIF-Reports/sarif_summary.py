#!/usr/bin/env python3
"""Print a concise summary of findings in a SARIF 2.1.0 JSON file."""

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sarif_file", type=Path)
    args = parser.parse_args()

    with args.sarif_file.open(encoding="utf-8") as handle:
        report = json.load(handle)

    if report.get("version") != "2.1.0":
        raise SystemExit("Expected SARIF version 2.1.0")

    totals = Counter()
    for run in report.get("runs", []):
        driver = run.get("tool", {}).get("driver", {})
        print(f"Tool: {driver.get('name', 'unknown')}")
        for result in run.get("results", []):
            level = result.get("level", "none")
            totals[level] += 1
            message = result.get("message", {}).get("text", "")
            rule_id = result.get("ruleId", "unknown")
            locations = result.get("locations", [])
            first = locations[0].get("physicalLocation", {}) if locations else {}
            uri = first.get("artifactLocation", {}).get("uri", "unknown")
            line = first.get("region", {}).get("startLine", "?")
            print(f"- {level}: {rule_id} at {uri}:{line} — {message}")

    print("Summary:")
    for level, count in sorted(totals.items()):
        print(f"  {level}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
