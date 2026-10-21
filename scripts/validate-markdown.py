#!/usr/bin/env python3
"""Validate that every markdown file is non-empty and starts with a heading."""
import sys, pathlib
bad = [str(p) for p in pathlib.Path('.').rglob('*.md') if not p.read_text(encoding='utf-8').lstrip().startswith(('#', '---'))]
print('\n'.join(bad) or 'OK')
sys.exit(1 if bad else 0)
