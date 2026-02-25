"""Check for domain field inconsistencies across all source JSON files."""

import json
import sys
from collections import defaultdict
from pathlib import Path

SOURCES_DIR = Path(__file__).parent.parent / "firstdata" / "sources"


def normalize_domain(domain: str) -> str:
    """Normalize domain to lowercase for comparison."""
    return domain.lower()


def main() -> None:
    print("Checking domain consistency across all sources...")

    # Collect all domains and their files
    domain_variants = defaultdict(lambda: defaultdict(list))
    errors = []

    for path in sorted(SOURCES_DIR.rglob("*.json")):
        rel_path = path.relative_to(SOURCES_DIR)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            domains = data.get("domains", [])
            if not domains:
                errors.append(f"{rel_path}: Missing or empty 'domains' field")
                continue

            for domain in domains:
                normalized = normalize_domain(domain)
                domain_variants[normalized][domain].append(str(rel_path))

        except Exception as e:
            errors.append(f"{rel_path}: Error reading file - {e}")

    # Check for case inconsistencies
    inconsistencies = []
    for normalized, variants in sorted(domain_variants.items()):
        if len(variants) > 1:
            # Multiple capitalizations exist for the same domain
            files_affected = []
            for variant, paths in variants.items():
                files_affected.extend([(variant, p) for p in paths])

            inconsistencies.append({
                "normalized": normalized,
                "variants": dict(variants),
                "files": files_affected,
            })

    # Report findings
    if errors:
        print("\n[ERROR] File reading errors:")
        for error in errors:
            print(f"  - {error}")

    if inconsistencies:
        print(f"\n[FAIL] Found {len(inconsistencies)} domain(s) with case inconsistencies:\n")

        for item in inconsistencies:
            normalized = item["normalized"]
            variants = item["variants"]

            print(f"Domain '{normalized}' has {len(variants)} different capitalizations:")

            for variant, paths in sorted(variants.items()):
                print(f"  '{variant}' ({len(paths)} files):")
                for path in sorted(paths)[:3]:  # Show first 3 examples
                    print(f"    - {path}")
                if len(paths) > 3:
                    print(f"    ... and {len(paths) - 3} more")
            print()

        # Provide fix suggestions
        print("\n" + "=" * 80)
        print("RECOMMENDED FIX")
        print("=" * 80)
        print("\nAll domains should use lowercase to maintain consistency.")
        print("Please update the affected files to use the lowercase form.\n")

        print("Example fixes needed:")
        for item in inconsistencies[:10]:  # Show first 10 examples
            variants = list(item["variants"].keys())
            # Find the non-lowercase variants
            non_lowercase = [v for v in variants if v != item["normalized"]]
            if non_lowercase:
                print(f"  '{non_lowercase[0]}' -> '{item['normalized']}'")

        sys.exit(1)

    if not inconsistencies and not errors:
        print("\n[OK] All domain fields are consistent!")
        sys.exit(0)
    elif errors and not inconsistencies:
        sys.exit(1)


if __name__ == "__main__":
    main()
