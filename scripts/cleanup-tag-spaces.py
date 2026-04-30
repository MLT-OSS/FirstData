#!/usr/bin/env python3
"""Cleanup tags with whitespace: replace spaces with hyphens.

Preserves Chinese tags (schema allows mixed Chinese/English).
Only acts on tags that contain ASCII whitespace characters.
Lowercases the result to match project convention for English tags.
"""
import json
import re
import sys
from pathlib import Path

WHITESPACE_RE = re.compile(r'\s+')
HAN_RE = re.compile(r'[\u4e00-\u9fff]')

def clean_tag(tag: str) -> str:
    """Replace runs of whitespace with a single hyphen.

    - If tag contains Han characters, preserve case (Chinese phrases).
    - Otherwise lowercase (English phrases convention).
    - Strip leading/trailing hyphens after substitution.
    """
    new = WHITESPACE_RE.sub('-', tag).strip('-')
    if not HAN_RE.search(new):
        new = new.lower()
    return new

def process_file(path: Path) -> int:
    """Return number of tags modified in this file."""
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        print(f"SKIP {path}: parse error: {e}", file=sys.stderr)
        return 0
    tags = data.get('tags')
    if not isinstance(tags, list):
        return 0
    changed = 0
    new_tags = []
    seen = set()
    for t in tags:
        if not isinstance(t, str):
            new_tags.append(t)
            continue
        nt = clean_tag(t)
        if nt != t:
            changed += 1
        # Dedup after normalization
        if nt in seen:
            changed += 1  # removed duplicate
            continue
        seen.add(nt)
        new_tags.append(nt)
    if changed == 0:
        return 0
    data['tags'] = new_tags
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return changed

def main():
    root = Path('firstdata/sources')
    total_files = 0
    total_changes = 0
    for p in sorted(root.rglob('*.json')):
        c = process_file(p)
        if c > 0:
            total_files += 1
            total_changes += c
            print(f"FIX {p}: {c} tag change(s)")
    print(f"\nSummary: {total_changes} tag changes across {total_files} files")

if __name__ == '__main__':
    main()
