"""Compare alert counts in two ZAP JSON reports.

The ZAP report schema can vary by template/version. Review the exported JSON
and adapt the extraction logic before using this for automation.
"""
import json
import sys
from collections import Counter

def load_report(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)

def summarize(report):
    counts = Counter()
    for site in report.get("site", []):
        for alert in site.get("alerts", []):
            counts[alert.get("riskdesc", "Unknown")] += 1
    return counts

def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python compare_alert_counts.py previous.json current.json")
    previous = summarize(load_report(sys.argv[1]))
    current = summarize(load_report(sys.argv[2]))
    print("Previous:", dict(previous))
    print("Current: ", dict(current))
    print("Note: counts are not unique vulnerability counts or severity validation.")

if __name__ == "__main__":
    main()
