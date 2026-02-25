"""Analyze domain usage across all data sources to identify inconsistencies."""

import json
from collections import defaultdict
from pathlib import Path

SOURCES_DIR = Path(__file__).parent.parent / "firstdata" / "sources"


def main() -> None:
    # Collect all domains
    all_domains = defaultdict(int)
    domain_files = defaultdict(list)

    for path in sorted(SOURCES_DIR.rglob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            for domain in data.get("domains", []):
                all_domains[domain] += 1
                domain_files[domain].append(str(path.relative_to(SOURCES_DIR)))
        except Exception as e:
            print(f"Error reading {path}: {e}")

    # Find case-insensitive duplicates
    print("=" * 80)
    print("DOMAIN USAGE ANALYSIS")
    print("=" * 80)
    print(f"\nTotal unique domains: {len(all_domains)}")
    print(f"Total sources scanned: {len(list(SOURCES_DIR.rglob('*.json')))}")

    # Group by lowercase version
    lowercase_groups = defaultdict(list)
    for domain in all_domains.keys():
        lowercase_groups[domain.lower()].append(domain)

    # Find inconsistencies
    print("\n" + "=" * 80)
    print("CASE INCONSISTENCIES DETECTED")
    print("=" * 80)

    inconsistencies = []
    for lower, variants in sorted(lowercase_groups.items()):
        if len(variants) > 1:
            inconsistencies.append((lower, variants))
            total_count = sum(all_domains[v] for v in variants)
            print(f"\n'{lower}' has {len(variants)} different capitalizations (total: {total_count} uses):")
            for variant in sorted(variants):
                count = all_domains[variant]
                print(f"  - '{variant}': {count} uses")
                # Show first 3 files as examples
                example_files = domain_files[variant][:3]
                for f in example_files:
                    print(f"      {f}")
                if len(domain_files[variant]) > 3:
                    print(f"      ... and {len(domain_files[variant]) - 3} more")

    if not inconsistencies:
        print("\n[OK] No case inconsistencies found!")
    else:
        print(f"\n[WARNING] Found {len(inconsistencies)} domain groups with case inconsistencies")

    # Suggest standard domains (lowercase)
    print("\n" + "=" * 80)
    print("SUGGESTED STANDARD DOMAINS (lowercase)")
    print("=" * 80)
    print("\nMost frequently used domains:")

    # Consolidate counts by lowercase
    consolidated = defaultdict(int)
    for domain, count in all_domains.items():
        consolidated[domain.lower()] += count

    # Sort by frequency
    sorted_domains = sorted(consolidated.items(), key=lambda x: -x[1])
    for domain, count in sorted_domains[:30]:
        print(f"  {domain:<40} ({count} uses)")

    # Export suggested standard list
    standard_domains = sorted([d for d, _ in sorted_domains])
    output_path = Path(__file__).parent.parent / "firstdata" / "schemas" / "suggested-standard-domains.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "domains": standard_domains,
            "note": "Auto-generated suggested standard domain list (lowercase normalized)"
        }, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Suggested standard domains exported to: {output_path.relative_to(Path(__file__).parent.parent)}")


if __name__ == "__main__":
    main()
