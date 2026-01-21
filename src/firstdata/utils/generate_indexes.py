#!/usr/bin/env python3
"""
FirstData - Index Generation Script
Generates index files for browsing and searching data sources
"""

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class IndexGenerator:
    """Generate various index files from data source metadata"""

    def __init__(self, sources_dir: Path, output_dir: Path):
        """Initialize generator"""
        self.sources_dir = sources_dir
        self.output_dir = output_dir
        self.sources = []

        # Load all data sources
        self._load_sources()

    def _load_sources(self):
        """Load all JSON data source files"""
        json_files = sorted(self.sources_dir.rglob("*.json"))

        for json_file in json_files:
            try:
                with open(json_file, encoding="utf-8") as f:
                    data = json.load(f)
                    data["_file_path"] = str(json_file.relative_to(self.sources_dir))
                    self.sources.append(data)
            except Exception as e:
                print(f"WARNING: Failed to load {json_file}: {e}")

        print(f"Loaded {len(self.sources)} data sources")

    # Note: quality_score and completeness_score removed in v2.0 schema

    def generate_all_sources(self) -> dict:
        """Generate all-sources.json with complete list"""
        all_sources = []

        for source in self.sources:
            entry = {
                "id": source["id"],
                "name": source["name"],
                "description": source.get("description", {}),
                "website": source.get("website", ""),
                "data_url": source.get("data_url", ""),
                "api_url": source.get("api_url"),
                "authority_level": source.get("authority_level", ""),
                "country": source.get("country"),
                "domains": source.get("domains", []),
                "geographic_scope": source.get("geographic_scope", ""),
                "update_frequency": source.get("update_frequency"),
                "has_api": source.get("api_url") is not None,
                "tags": source.get("tags", []),
                "file_path": source["_file_path"],
            }

            all_sources.append(entry)

        # Sort by name
        all_sources.sort(key=lambda x: x["name"].get("en", ""))

        result = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_sources": len(all_sources),
                "version": "2.0",
                "schema_version": "v2.0.0",
            },
            "sources": all_sources,
        }

        return result

    def generate_by_domain(self) -> dict:
        """Generate by-domain.json grouped by domain"""
        by_domain = defaultdict(list)

        for source in self.sources:
            domains = source.get("domains", [])

            entry = {
                "id": source["id"],
                "name": source["name"],
                "authority_level": source.get("authority_level", ""),
                "data_url": source.get("data_url", ""),
                "has_api": source.get("api_url") is not None,
                "file_path": source["_file_path"],
            }

            for domain in domains:
                by_domain[domain].append(entry)

        # Sort sources within each domain by name
        for domain in by_domain:
            by_domain[domain].sort(key=lambda x: x["name"].get("en", ""))

        # Convert to regular dict and sort by domain name
        result = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_domains": len(by_domain),
                "total_sources": len(self.sources),
                "version": "2.0",
            },
            "domains": dict(sorted(by_domain.items())),
        }

        return result

    def generate_by_region(self) -> dict:
        """Generate by-region.json grouped by geographic scope"""
        by_region = defaultdict(list)

        for source in self.sources:
            scope = source.get("geographic_scope", "")
            country = source.get("country")

            # Determine region key
            if scope == "global":
                region_key = "global"
            elif scope == "national" and country:
                region_key = country
            elif scope == "regional":
                region_key = "regional"
            else:
                region_key = scope or "unknown"

            entry = {
                "id": source["id"],
                "name": source["name"],
                "authority_level": source.get("authority_level", ""),
                "data_url": source.get("data_url", ""),
                "has_api": source.get("api_url") is not None,
                "geographic_scope": scope,
                "file_path": source["_file_path"],
            }

            by_region[region_key].append(entry)

        # Sort sources within each region by name
        for region in by_region:
            by_region[region].sort(key=lambda x: x["name"].get("en", ""))

        result = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_regions": len(by_region),
                "total_sources": len(self.sources),
                "version": "2.0",
            },
            "regions": dict(sorted(by_region.items())),
        }

        return result

    def generate_by_authority(self) -> dict:
        """Generate by-authority.json grouped by authority level"""
        by_authority = {
            "government": [],
            "international": [],
            "market": [],
            "research": [],
            "commercial": [],
            "other": [],
        }

        for source in self.sources:
            authority_level = source.get("authority_level", "other")

            entry = {
                "id": source["id"],
                "name": source["name"],
                "authority_level": authority_level,
                "data_url": source.get("data_url", ""),
                "has_api": source.get("api_url") is not None,
                "geographic_scope": source.get("geographic_scope", ""),
                "file_path": source["_file_path"],
            }

            # Categorize by authority level
            if authority_level in by_authority:
                by_authority[authority_level].append(entry)
            else:
                by_authority["other"].append(entry)

        # Sort within each category by name
        for sources in by_authority.values():
            sources.sort(key=lambda x: x["name"].get("en", ""))

        # Count sources by authority level
        authority_counts = {k: len(v) for k, v in by_authority.items()}

        result = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_sources": len(self.sources),
                "authority_counts": authority_counts,
                "version": "2.0",
            },
            "by_authority_level": by_authority,
        }

        return result

    def generate_statistics(self) -> dict:
        """Generate statistics.json with overview statistics"""
        # Count by authority level
        authority_levels = defaultdict(int)
        for source in self.sources:
            authority_levels[source.get("authority_level", "other")] += 1

        # Count by geographic scope
        geo_scopes = defaultdict(int)
        for source in self.sources:
            geo_scopes[source.get("geographic_scope", "unknown")] += 1

        # Count by update frequency
        frequencies = defaultdict(int)
        for source in self.sources:
            freq = source.get("update_frequency", "unknown")
            frequencies[freq] += 1

        # Count by access level (if exists in v2 schema)
        access_levels = defaultdict(int)
        for source in self.sources:
            access_level = source.get("access_level", "unknown")
            access_levels[access_level] += 1

        # Domain counts
        domain_counts = defaultdict(int)
        for source in self.sources:
            for domain in source.get("domains", []):
                domain_counts[domain] += 1

        # API availability
        api_count = sum(1 for s in self.sources if s.get("api_url") is not None)

        result = {
            "metadata": {"generated_at": datetime.now().isoformat(), "version": "2.0"},
            "overview": {
                "total_sources": len(self.sources),
                "sources_with_api": api_count,
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
            },
            "by_authority_level": dict(authority_levels),
            "by_geographic_scope": dict(geo_scopes),
            "by_access_level": dict(access_levels),
            "by_update_frequency": dict(frequencies),
            "by_domain": dict(sorted(domain_counts.items(), key=lambda x: -x[1])),
        }

        return result

    def generate_all(self):
        """Generate all index files"""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        indexes = {
            "all-sources.json": self.generate_all_sources(),
            "by-domain.json": self.generate_by_domain(),
            "by-region.json": self.generate_by_region(),
            "by-authority.json": self.generate_by_authority(),
            "statistics.json": self.generate_statistics(),
        }

        for filename, data in indexes.items():
            output_path = self.output_dir / filename
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Generated: {output_path}")

        print(f"\nSuccessfully generated {len(indexes)} index files!")


def main():  # noqa: PLR0915
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate index files for FirstData",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all indexes (default)
  python generate_indexes.py

  # Test a single datasource file
  python generate_indexes.py --test sources/china/finance/banking/pbc.json

  # Specify custom source directory
  python generate_indexes.py --sources ../sources

  # Specify custom output directory
  python generate_indexes.py --output ../public/indexes
        """,
    )

    parser.add_argument(
        "--sources",
        default="sources",
        help="Source directory containing JSON files (default: sources)",
    )

    parser.add_argument(
        "--output", default="indexes", help="Output directory for index files (default: indexes)"
    )

    parser.add_argument(
        "--test",
        type=str,
        metavar="FILE",
        help="Test mode: verify a single datasource file can be indexed",
    )

    args = parser.parse_args()

    # Test mode: verify single file
    if args.test:
        test_file = Path(args.test)
        if not test_file.exists():
            print(f"❌ Error: Test file not found: {test_file}")
            sys.exit(1)

        print("=" * 70)
        print("FirstData - Index Test Mode")
        print("=" * 70)
        print(f"Testing file: {test_file}\n")

        # Try to load the file
        try:
            with open(test_file, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON格式错误: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 无法读取文件: {e}")
            sys.exit(1)

        # Verify required fields for indexing (v2.0 schema)
        required_index_fields = ["id", "name", "authority_level"]
        missing_fields = []

        for field in required_index_fields:
            if field not in data:
                missing_fields.append(field)

        if missing_fields:
            print(f"❌ 缺少索引必需字段: {', '.join(missing_fields)}")
            sys.exit(1)

        # Extract key information
        datasource_id = data.get("id")
        name_en = data.get("name", {}).get("en", "N/A")
        name_zh = data.get("name", {}).get("zh", "N/A")
        authority_level = data.get("authority_level", "N/A")
        geographic_scope = data.get("geographic_scope", "N/A")
        has_api = data.get("api_url") is not None
        domains = ", ".join(data.get("domains", []))

        print("✅ 文件格式正确")
        print("\n数据源信息:")
        print(f"  ID: {datasource_id}")
        print(f"  名称 (EN): {name_en}")
        print(f"  名称 (ZH): {name_zh}")
        print(f"  权威级别: {authority_level}")
        print(f"  地理范围: {geographic_scope}")
        print(f"  API支持: {'是' if has_api else '否'}")
        print(f"  领域: {domains if domains else 'N/A'}")
        print("\n✅ 该数据源可以正确加入索引")
        print("=" * 70)
        sys.exit(0)

    sources_dir = Path(args.sources)
    output_dir = Path(args.output)

    if not sources_dir.exists():
        print(f"❌ Error: Source directory not found: {sources_dir}")
        sys.exit(1)

    print("=" * 70)
    print("FirstData - Index Generator")
    print("=" * 70)
    print(f"Source directory: {sources_dir}")
    print(f"Output directory: {output_dir}")
    print()

    generator = IndexGenerator(sources_dir, output_dir)
    generator.generate_all()

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
