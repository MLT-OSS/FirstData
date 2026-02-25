"""Check for duplicate IDs across all source JSON files."""

import json
import sys
from pathlib import Path

SOURCES_DIR = Path(__file__).parent.parent / "firstdata" / "sources"


def main() -> None:
    seen: dict[str, Path] = {}
    errors: list[str] = []

    for path in sorted(SOURCES_DIR.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        id_ = data.get("id")
        if id_ in seen:
            errors.append(f"Duplicate id '{id_}' in:\n  {seen[id_]}\n  {path}")
        else:
            seen[id_] = path

    if errors:
        print("❌ Duplicate IDs found:")
        for e in errors:
            print(e)
        sys.exit(1)

    print(f"✅ All {len(seen)} IDs are unique.")


if __name__ == "__main__":
    main()
