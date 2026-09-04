#!/usr/bin/env python3
"""
Pretty-print one or more JSON files with 4-space indentation so that
`git diff` shows one line per changed field instead of one giant line.

Usage:
    format_json.py <file1.json> [file2.json ...]

Prints the list of files it actually rewrote. Files that are already
correctly formatted (or aren't valid JSON) are left untouched.
"""
import json
import sys
from pathlib import Path


def format_file(path):
    """Rewrite `path` as pretty-printed JSON in place.

    Returns True if the file's contents changed, False if it was already
    formatted (or wasn't valid JSON, in which case it's left alone).
    """
    original = path.read_text(encoding="utf-8")

    try:
        data = json.loads(original)
    except json.JSONDecodeError as exc:
        print(f"skip {path}: not valid JSON ({exc})", file=sys.stderr)
        return False

    # indent=4 puts every brace/field on its own line at 4 spaces per level.
    # ensure_ascii=False keeps unicode readable instead of \uXXXX-escaping it.
    formatted = json.dumps(data, indent=4, ensure_ascii=False) + "\n"

    if formatted == original:
        return False

    path.write_text(formatted, encoding="utf-8")
    return True


def main(argv):
    if not argv:
        print("usage: format_json.py <file.json> [more.json ...]", file=sys.stderr)
        return 1

    changed = []
    for raw_path in argv:
        path = Path(raw_path)
        if not path.exists():
            continue
        if format_file(path):
            changed.append(str(path))

    if changed:
        print("reformatted: " + ", ".join(changed))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
