#!/usr/bin/env python3
"""Check every numbered module has a README.md."""
import sys, pathlib
missing = [str(d) for d in sorted(pathlib.Path('.').glob('[0-9][0-9]-*')) if not (d / 'README.md').exists()]
print('\n'.join(missing) or 'OK')
sys.exit(1 if missing else 0)
