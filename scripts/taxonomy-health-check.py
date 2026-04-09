#!/usr/bin/env python3
"""
Taxonomy Health Check for FirstData
====================================
Detects structural issues in the sources/ taxonomy:
  1. Duplicate paths — same country/entity in multiple L1 locations
  2. Orphan L1 — top-level categories with ≤2 files (likely misplaced)
  3. Directory underscore violations — should be kebab-case
  4. Domain format inconsistency — same concept in different formats

Output: JSON report + human-readable summary to stdout.

Usage:
  python scripts/taxonomy-health-check.py [--json] [--ci]

  --json   Print only JSON report (for CI integration)
  --ci     Exit with code 1 if any blocking issues found
"""

import json
import sys
import os
import re
from pathlib import Path
from collections import defaultdict

def find_sources_dir():
    """Find the firstdata/sources directory."""
    # Try relative to script location
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir.parent / "firstdata" / "sources",
        Path.cwd() / "firstdata" / "sources",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    print("ERROR: Cannot find firstdata/sources/ directory", file=sys.stderr)
    sys.exit(2)


def load_all_sources(sources_dir):
    """Load all JSON source files."""
    sources = []
    for json_file in sorted(sources_dir.rglob("*.json")):
        if json_file.name == "_index.json":
            continue
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            rel = json_file.relative_to(sources_dir)
            sources.append({
                "file": str(rel),
                "path_parts": list(rel.parts),
                "id": data.get("id", ""),
                "name": data.get("name", ""),
                "domains": data.get("domains", []),
            })
        except (json.JSONDecodeError, OSError) as e:
            print(f"WARNING: Failed to parse {json_file}: {e}", file=sys.stderr)
    return sources


def check_duplicate_paths(sources):
    """
    Detect country/entity-level duplicates: same country scattered across
    multiple L1 directories.

    Two sub-checks:
    a) Country L1 orphans — top-level dirs like india/, japan/ that duplicate
       entries already under countries/
    b) Country alias conflicts — e.g., us/ vs usa/ vs countries/us/ vs
       countries/north-america/usa/

    Does NOT flag subject categories (agriculture, finance, etc.) that
    naturally appear under multiple country/org trees.
    """
    # Known country aliases to group together
    COUNTRY_ALIASES = {
        "us": "united-states",
        "usa": "united-states",
        "cn": "china",
        "hk": "hong-kong",
        "uk": "united-kingdom",
    }

    # R4 consensus: final top-level = country dirs + international/
    # academic/ and sectors/ are NOT legitimate L1 — should be dispersed
    # into country directories. Only countries/ and international/ survive.
    LEGITIMATE_L1 = {"countries", "international"}

    # Step 1: Build country → {path_prefix: [files]} from L1 dirs
    l1_dirs = set()
    for s in sources:
        l1_dirs.add(s["path_parts"][0])

    # Candidate country L1s: top-level dirs not in LEGITIMATE_L1
    candidate_countries = {d for d in l1_dirs - LEGITIMATE_L1
                          if d not in ("academic", "sectors", "regional")}

    # Step 2: For each candidate, find all paths where this country appears
    duplicates = []

    # Group candidates by normalized name
    country_groups = defaultdict(set)  # norm_name → {l1_dir_name, ...}
    for c in candidate_countries:
        norm = COUNTRY_ALIASES.get(c, c)
        country_groups[norm].add(c)

    for norm_name, l1_names in sorted(country_groups.items()):
        paths = {}

        # Files directly under these L1 dirs
        for l1 in l1_names:
            prefix = l1 + "/"
            files = [s["file"] for s in sources if s["path_parts"][0] == l1]
            if files:
                paths[prefix] = files

        # Files under countries/ tree that match this country
        search_names = l1_names | {norm_name}
        for s in sources:
            if s["path_parts"][0] != "countries":
                continue
            # Check if any path part matches our country names
            for part in s["path_parts"][1:-1]:
                part_norm = COUNTRY_ALIASES.get(part, part)
                if part_norm == norm_name or part in search_names:
                    # Build the path prefix up to this country folder
                    idx = s["path_parts"].index(part)
                    prefix = "/".join(s["path_parts"][:idx+1]) + "/"
                    paths.setdefault(prefix, [])
                    if s["file"] not in paths[prefix]:
                        paths[prefix].append(s["file"])

        if len(paths) > 1:
            total = sum(len(f) for f in paths.values())
            entry = {
                "entity": norm_name,
                "paths": {},
                "total_files": total
            }
            for prefix, files in sorted(paths.items()):
                entry["paths"][prefix] = {
                    "count": len(files),
                    "files": sorted(files)
                }
            duplicates.append(entry)

    return duplicates


def check_illegitimate_l1(sources):
    """
    Find L1 directories that violate R4 consensus.

    R4 three-party consensus (taxonomy design study round 4):
      Decision: academic/ and sectors/ do NOT remain as top-level directories;
      they should be dispersed into country directories by geographic affiliation.
      Final top-level structure: country directories + international/
      Only `countries/` and `international/` are legitimate L1 directories.

    Everything else (academic/, sectors/, china/, india/, etc.) should be
    dispersed into the country tree.
    """
    # See R4 consensus above. This is NOT arbitrary — changing this set
    # requires a new three-party decision.
    LEGITIMATE_L1 = {"countries", "international"}

    l1_counts = defaultdict(list)
    for s in sources:
        l1 = s["path_parts"][0]
        l1_counts[l1].append(s["file"])

    illegitimate = []
    for l1, files in sorted(l1_counts.items()):
        if l1 not in LEGITIMATE_L1:
            illegitimate.append({
                "l1": l1,
                "file_count": len(files),
                "category": _classify_l1(l1),
                "files": sorted(files) if len(files) <= 5 else sorted(files)[:5] + [f"... and {len(files)-5} more"]
            })
    return illegitimate


def _classify_l1(l1_name):
    """Classify why an L1 directory is illegitimate."""
    country_names = {
        "china", "india", "japan", "singapore", "thailand",
        "us", "usa", "cn", "hk", "uk",
    }
    if l1_name in country_names:
        return "country-orphan"
    if l1_name in ("academic", "sectors"):
        return "non-geographic-axis"
    if l1_name == "regional":
        return "scope-axis"
    return "unknown"


def check_directory_underscores(sources_dir):
    """Find directory names containing underscores (should be kebab-case)."""
    violations = defaultdict(list)
    for json_file in sources_dir.rglob("*.json"):
        if json_file.name == "_index.json":
            continue
        rel = json_file.relative_to(sources_dir)
        for part in rel.parts[:-1]:
            if "_" in part:
                violations[part].append(str(rel))

    return [
        {
            "directory": dirname,
            "suggested": dirname.replace("_", "-"),
            "affected_files": len(files),
            "files": sorted(files)
        }
        for dirname, files in sorted(violations.items())
    ]


def check_domain_format_conflicts(sources):
    """Find domain values where the same concept uses different formatting."""
    # Collect all domain values
    all_domains = []
    for s in sources:
        for d in s["domains"]:
            all_domains.append(d)

    # Normalize and group
    normalized = defaultdict(lambda: defaultdict(int))
    for d in all_domains:
        norm = d.lower().replace("-", " ").replace("_", " ").strip()
        normalized[norm][d] += 1

    conflicts = []
    for concept, variants in sorted(normalized.items()):
        if len(variants) > 1:
            conflicts.append({
                "concept": concept,
                "variants": dict(sorted(variants.items())),
                "total_occurrences": sum(variants.values())
            })

    # Summary stats
    total = len(all_domains)
    has_space = sum(1 for d in all_domains if " " in d)
    has_hyphen = sum(1 for d in all_domains if "-" in d)
    has_underscore = sum(1 for d in all_domains if "_" in d)
    single_word = total - has_space - has_hyphen - has_underscore + \
                  sum(1 for d in all_domains if " " in d and "-" in d)

    format_stats = {
        "total_entries": total,
        "with_spaces": has_space,
        "with_hyphens": has_hyphen,
        "with_underscores": has_underscore,
        "conflict_groups": len(conflicts),
    }

    return conflicts, format_stats


def main():
    json_only = "--json" in sys.argv
    ci_mode = "--ci" in sys.argv

    sources_dir = find_sources_dir()
    sources = load_all_sources(sources_dir)

    # Run all checks
    duplicate_paths = check_duplicate_paths(sources)
    illegitimate_l1 = check_illegitimate_l1(sources)
    dir_underscores = check_directory_underscores(sources_dir)
    domain_conflicts, domain_stats = check_domain_format_conflicts(sources)

    # Count misplaced files
    misplaced_files = sum(item["file_count"] for item in illegitimate_l1)

    # Build report
    import datetime
    report = {
        "scan_date": datetime.date.today().isoformat(),
        "total_sources": len(sources),
        "checks": {
            "duplicate_paths": {
                "count": len(duplicate_paths),
                "severity": "warning",
                "items": duplicate_paths
            },
            "illegitimate_l1": {
                "count": len(illegitimate_l1),
                "severity": "error",
                "description": "L1 dirs violating R4 consensus (only countries/ + international/ are legitimate)",
                "misplaced_files": misplaced_files,
                "items": illegitimate_l1
            },
            "directory_underscores": {
                "count": len(dir_underscores),
                "severity": "error",
                "items": dir_underscores
            },
            "domain_format_conflicts": {
                "count": len(domain_conflicts),
                "severity": "info",
                "stats": domain_stats,
                "items": domain_conflicts
            }
        },
        "summary": {
            "errors": len(dir_underscores) + len(illegitimate_l1),
            "warnings": len(duplicate_paths),
            "info": len(domain_conflicts),
            "pass": len(dir_underscores) == 0 and len(illegitimate_l1) == 0
        }
    }

    if json_only:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        # Human-readable summary
        print("=" * 60)
        print("  FirstData Taxonomy Health Check")
        print(f"  Sources scanned: {len(sources)}")
        print("=" * 60)

        # Check 1: Duplicate paths
        print(f"\n🔴 Duplicate Paths: {len(duplicate_paths)} entities")
        for dp in duplicate_paths:
            print(f"\n  [{dp['entity']}] — {dp['total_files']} files across {len(dp['paths'])} paths:")
            for path, info in dp["paths"].items():
                print(f"    {path} → {info['count']} file(s)")

        # Check 2: Illegitimate L1 (R4 consensus)
        print(f"\n🔴 Illegitimate L1 Directories: {len(illegitimate_l1)} ({misplaced_files} files misplaced)")
        print(f"   R4 consensus: only countries/ + international/ are legitimate")
        for item in illegitimate_l1:
            tag = {"country-orphan": "🌍", "non-geographic-axis": "📁", "scope-axis": "🔲"}.get(item["category"], "❓")
            files_display = item["files"] if item["file_count"] <= 5 else f"{item['files'][:3]}... ({item['file_count']} total)"
            print(f"  {tag} {item['l1']}/ → {item['file_count']} file(s) [{item['category']}]")

        # Check 3: Directory underscores
        print(f"\n🔴 Directory Underscore Violations: {len(dir_underscores)}")
        for v in dir_underscores:
            print(f"  {v['directory']}/ → {v['suggested']}/ ({v['affected_files']} files)")

        # Check 4: Domain format conflicts
        print(f"\n📊 Domain Format Stats:")
        print(f"  Total entries: {domain_stats['total_entries']}")
        print(f"  With spaces:  {domain_stats['with_spaces']} ({100*domain_stats['with_spaces']/domain_stats['total_entries']:.1f}%)")
        print(f"  With hyphens: {domain_stats['with_hyphens']} ({100*domain_stats['with_hyphens']/domain_stats['total_entries']:.1f}%)")
        print(f"  Conflicting format groups: {domain_stats['conflict_groups']}")
        if domain_conflicts:
            print(f"\n  Top conflicts:")
            for c in domain_conflicts[:10]:
                variants = ", ".join(f'"{v}"' for v in c["variants"])
                print(f"    {c['concept']}: [{variants}]")
            if len(domain_conflicts) > 10:
                print(f"    ... and {len(domain_conflicts) - 10} more")

        # Summary
        print("\n" + "=" * 60)
        s = report["summary"]
        status = "✅ PASS" if s["pass"] else "❌ FAIL"
        print(f"  {status} | Errors: {s['errors']} | Warnings: {s['warnings']} | Info: {s['info']}")
        print("=" * 60)

    # CI exit code
    if ci_mode and not report["summary"]["pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
