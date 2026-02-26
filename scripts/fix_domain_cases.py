"""Fix domain case inconsistencies by converting all domains to lowercase."""

import json
from pathlib import Path

SOURCES_DIR = Path(__file__).parent.parent / "firstdata" / "sources"


def main() -> None:
    print("Fixing domain case inconsistencies...")
    print("=" * 80)

    fixed_files = []
    unchanged_files = []
    errors = []

    for path in sorted(SOURCES_DIR.rglob("*.json")):
        rel_path = path.relative_to(SOURCES_DIR)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            original_domains = data.get("domains", [])
            if not original_domains:
                unchanged_files.append(str(rel_path))
                continue

            # Convert all domains to lowercase
            lowercase_domains = [d.lower() for d in original_domains]

            # Check if any changes were made
            if lowercase_domains != original_domains:
                data["domains"] = lowercase_domains

                # Write back with same formatting
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.write("\n")  # Add trailing newline

                print(f"[FIXED] {rel_path}")
                print(f"  Before: {original_domains}")
                print(f"  After:  {lowercase_domains}")
                print()

                fixed_files.append(str(rel_path))
            else:
                unchanged_files.append(str(rel_path))

        except Exception as e:
            error_msg = f"{rel_path}: {e}"
            errors.append(error_msg)
            print(f"[ERROR] {error_msg}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Fixed files:     {len(fixed_files)}")
    print(f"Unchanged files: {len(unchanged_files)}")
    print(f"Errors:          {len(errors)}")

    if fixed_files:
        print("\n[OK] Domain case inconsistencies have been fixed!")
        print("\nNext steps:")
        print("  1. Verify fixes: python scripts/check_domains.py")
        print("  2. Rebuild indexes: python scripts/build_indexes.py")
    else:
        print("\n[OK] No domain case inconsistencies found!")

    if errors:
        print("\n[WARNING] Some files had errors. Please review them manually.")


if __name__ == "__main__":
    main()
