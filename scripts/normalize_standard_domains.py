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

    # Build a map from normalized -> preferred form (with spaces)
    domain_map = {}
    for domain in original_domains:
        normalized = normalize_domain(domain)

        # Prefer space-separated version
        if normalized not in domain_map:
            domain_map[normalized] = domain
        else:
            # If we already have this normalized form, prefer the one with spaces
            existing = domain_map[normalized]
            # Count separators: spaces=0, hyphens/underscores=1
            domain_score = domain.count("-") + domain.count("_")
            existing_score = existing.count("-") + existing.count("_")

            # Prefer the one with fewer hyphens/underscores (more spaces)
            if domain_score < existing_score:
                domain_map[normalized] = domain

    # Extract unique domains (prefer space-separated)
    unique_domains = sorted(set(domain_map.values()))

    print(f"After normalization: {len(unique_domains)}")
    print(f"Removed: {len(original_domains) - len(unique_domains)} duplicates")

    # Update and save
    data["domains"] = unique_domains
    data["note"] = "Auto-generated standard domain list (lowercase, space-separated for multi-word terms)"

    with open(DOMAINS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")  # Add trailing newline

    print(f"\n[OK] Normalized domains saved to: {DOMAINS_FILE.name}")

    # Show some examples of what was deduplicated
    print("\nExamples of deduplicated domains:")
    for normalized, preferred in sorted(domain_map.items())[:10]:
        # Check if this normalized form had multiple variants in original
        variants = [d for d in original_domains if normalize_domain(d) == normalized]
        if len(variants) > 1:
            print(f"  {normalized}:")
            for v in variants:
                marker = " [KEPT]" if v == preferred else " [removed]"
                print(f"    - '{v}'{marker}")


if __name__ == "__main__":
    main()
