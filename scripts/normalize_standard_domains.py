"""Normalize suggested-standard-domains.json by removing duplicates with hyphens/underscores."""

import json
from pathlib import Path

DOMAINS_FILE = Path(__file__).parent.parent / "firstdata" / "schemas" / "suggested-standard-domains.json"


def normalize_domain(domain: str) -> str:
    """Convert hyphens and underscores to spaces for normalization."""
    return domain.replace("-", " ").replace("_", " ")


def main() -> None:
    print("Normalizing suggested-standard-domains.json...")

    with open(DOMAINS_FILE, encoding="utf-8") as f:
        data = json.load(f)

    original_domains = data["domains"]
    print(f"Original count: {len(original_domains)}")

    # Normalize all domains to use spaces instead of hyphens/underscores
    normalized_domains = set()
    changes = []

    for domain in original_domains:
        normalized = normalize_domain(domain)
        normalized_domains.add(normalized)

        # Track what was changed
        if domain != normalized:
            changes.append((domain, normalized))

    # Extract unique normalized domains
    unique_domains = sorted(normalized_domains)

    print(f"After normalization: {len(unique_domains)}")
    print(f"Removed duplicates: {len(original_domains) - len(unique_domains)}")
    print(f"Changed (hyphens/underscores to spaces): {len(changes)}")

    # Update and save
    data["domains"] = unique_domains
    data["note"] = "Auto-generated standard domain list (lowercase, space-separated for multi-word terms)"

    with open(DOMAINS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")  # Add trailing newline

    print(f"\n[OK] Normalized domains saved to: {DOMAINS_FILE.name}")

    # Show some examples of what was changed
    if changes:
        print(f"\nExamples of normalized domains (first 10 of {len(changes)}):")
        for old, new in changes[:10]:
            print(f"  '{old}' -> '{new}'")


if __name__ == "__main__":
    main()
