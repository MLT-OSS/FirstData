#!/usr/bin/env python
"""Quick view script for China data source samples"""

import json
from pathlib import Path


def view_samples():
    print("=" * 50)
    print("China Data Sources - Sample Overview")
    print("=" * 50)
    print()

    # Find all JSON files
    json_files = sorted(Path(".").rglob("*.json"))

    for json_file in json_files:
        try:
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)

            # Calculate average quality score
            quality = data["quality"]
            avg_quality = (
                quality["authority_level"]
                + quality["methodology_transparency"]
                + quality["update_timeliness"]
                + quality["data_completeness"]
                + quality["documentation_quality"]
            ) / 5.0

            print(f"📄 File: {json_file}")
            print(f"   ID: {data['id']}")
            print(f"   Name (EN): {data['name']['en']}")
            print(f"   Name (ZH): {data['name']['zh']}")
            print(f"   Authority: {'⭐' * int(avg_quality)} ({avg_quality:.1f}/5.0)")
            print(f"   URL: {data['access']['primary_url']}")
            print(f"   Status: {data['catalog_metadata']['status']}")
            print(f"   Indicators: {data['coverage'].get('indicators', 'N/A')}")
            print("   " + "-" * 46)

        except Exception as e:
            print(f"❌ Error reading {json_file}: {e}")
            print("   " + "-" * 46)

    print()
    print(f"Total: {len(json_files)} data sources")
    print("=" * 50)


if __name__ == "__main__":
    view_samples()
