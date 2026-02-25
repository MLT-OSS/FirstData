"""Generate aggregated index files from individual data source JSON files."""

import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SOURCES_DIR = REPO_ROOT / "firstdata" / "sources"
INDEXES_DIR = REPO_ROOT / "firstdata" / "indexes"
BADGES_DIR = REPO_ROOT / "firstdata" / "badges"

SCHEMA_VERSION = "2.0"
TARGET_TOTAL = 1000


def load_sources() -> list[dict]:
    sources = []
    for path in sorted(SOURCES_DIR.rglob("*.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        data["has_api"] = data.get("api_url") is not None
        data["file_path"] = str(path.relative_to(SOURCES_DIR))
        sources.append(data)
    return sources


def summary_entry(source: dict) -> dict:
    """Compact representation used in grouped indexes."""
    entry = {
        "id": source["id"],
        "name": source["name"],
        "authority_level": source["authority_level"],
        "data_url": source["data_url"],
        "has_api": source["has_api"],
        "file_path": source["file_path"],
    }
    if "geographic_scope" in source:
        entry["geographic_scope"] = source["geographic_scope"]
    return entry


def build_all_sources(sources: list[dict], now: str) -> dict:
    return {
        "metadata": {
            "generated_at": now,
            "total_sources": len(sources),
            "version": SCHEMA_VERSION,
            "schema_version": "v2.0.0",
        },
        "sources": sources,
    }


def build_by_authority(sources: list[dict], now: str) -> dict:
    groups: dict[str, list] = defaultdict(list)
    for s in sources:
        groups[s["authority_level"]].append(summary_entry(s))

    counts = {level: len(items) for level, items in groups.items()}

    return {
        "metadata": {
            "generated_at": now,
            "total_sources": len(sources),
            "authority_counts": counts,
            "version": SCHEMA_VERSION,
        },
        "by_authority_level": dict(groups),
    }


def build_by_domain(sources: list[dict], now: str) -> dict:
    groups: dict[str, list] = defaultdict(list)
    for s in sources:
        for domain in s.get("domains", []):
            groups[domain].append(summary_entry(s))

    return {
        "metadata": {
            "generated_at": now,
            "total_domains": len(groups),
            "total_sources": len(sources),
            "version": SCHEMA_VERSION,
        },
        "domains": dict(sorted(groups.items())),
    }


def build_by_region(sources: list[dict], now: str) -> dict:
    groups: dict[str, list] = defaultdict(list)
    for s in sources:
        country = s.get("country")
        if country:
            groups[country].append(summary_entry(s))

    return {
        "metadata": {
            "generated_at": now,
            "total_regions": len(groups),
            "total_sources": len(sources),
            "version": SCHEMA_VERSION,
        },
        "regions": dict(sorted(groups.items())),
    }


def build_statistics(sources: list[dict], now: str) -> dict:
    by_authority: dict[str, int] = defaultdict(int)
    by_scope: dict[str, int] = defaultdict(int)
    by_frequency: dict[str, int] = defaultdict(int)
    by_domain: dict[str, int] = defaultdict(int)

    for s in sources:
        by_authority[s["authority_level"]] += 1
        if scope := s.get("geographic_scope"):
            by_scope[scope] += 1
        if freq := s.get("update_frequency"):
            by_frequency[freq] += 1
        for domain in s.get("domains", []):
            by_domain[domain] += 1

    sources_with_api = sum(1 for s in sources if s["has_api"])

    return {
        "metadata": {
            "generated_at": now,
            "version": SCHEMA_VERSION,
        },
        "overview": {
            "total_sources": len(sources),
            "sources_with_api": sources_with_api,
            "last_updated": now[:10],
        },
        "by_authority_level": dict(by_authority),
        "by_geographic_scope": dict(by_scope),
        "by_update_frequency": dict(by_frequency),
        "by_domain": dict(sorted(by_domain.items(), key=lambda x: -x[1])),
    }


def build_badges(sources: list[dict]) -> list[tuple[Path, dict]]:
    total = len(sources)
    pct = round(total / TARGET_TOTAL * 100)
    color = "red" if pct < 10 else "yellow" if pct < 50 else "green"

    return [
        (
            BADGES_DIR / "sources-count.json",
            {
                "schemaVersion": 1,
                "label": "数据源",
                "message": f"{total}/{TARGET_TOTAL}+",
                "color": "blue",
            },
        ),
        (
            BADGES_DIR / "progress.json",
            {
                "schemaVersion": 1,
                "label": "进度",
                "message": f"{pct}%",
                "color": color,
            },
        ),
    ]


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {path.relative_to(REPO_ROOT)}")


def main() -> None:
    print("Loading sources...")
    sources = load_sources()
    print(f"  Found {len(sources)} source files")

    now = datetime.now(timezone.utc).isoformat()

    print("Building indexes...")
    write_json(INDEXES_DIR / "all-sources.json", build_all_sources(sources, now))
    write_json(INDEXES_DIR / "by-authority.json", build_by_authority(sources, now))
    write_json(INDEXES_DIR / "by-domain.json", build_by_domain(sources, now))
    write_json(INDEXES_DIR / "by-region.json", build_by_region(sources, now))
    write_json(INDEXES_DIR / "statistics.json", build_statistics(sources, now))

    print("Building badges...")
    for path, data in build_badges(sources):
        write_json(path, data)

    print("Done.")


if __name__ == "__main__":
    main()
