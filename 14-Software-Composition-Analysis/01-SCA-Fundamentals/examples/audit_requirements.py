#!/usr/bin/env python3
"""Teaching helper: list exact name==version pins; not a resolver or scanner."""
from pathlib import Path
import re, sys

pattern = re.compile(r"^\s*([A-Za-z0-9_.-]+)==([A-Za-z0-9_.+-]+)\s*(?:#.*)?$")
path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("requirements.txt")
if not path.is_file():
    raise SystemExit(f"File not found: {path}")
print("Package,Version")
skipped = 0
for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    match = pattern.match(line)
    if match:
        print(f"{match.group(1)},{match.group(2)}")
    else:
        skipped += 1
        print(f"Skipped line {number}: not a simple exact pin", file=sys.stderr)
if skipped:
    print(f"Skipped {skipped} line(s); use a real resolver for full coverage.", file=sys.stderr)
