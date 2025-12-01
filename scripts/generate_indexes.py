#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataSource Hub - Index Generation Script
Generates index files for browsing and searching data sources
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
from datetime import datetime


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
        json_files = sorted(self.sources_dir.rglob('*.json'))

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data['_file_path'] = str(json_file.relative_to(self.sources_dir))
                    self.sources.append(data)
            except Exception as e:
                print(f"WARNING: Failed to load {json_file}: {e}")

        print(f"Loaded {len(self.sources)} data sources")

    def _calculate_quality_score(self, quality: Dict) -> float:
        """Calculate average quality score"""
        scores = [
            quality.get('authority_level', 0),
            quality.get('methodology_transparency', 0),
            quality.get('update_timeliness', 0),
            quality.get('data_completeness', 0),
            quality.get('documentation_quality', 0)
        ]
        return round(sum(scores) / len(scores), 1) if scores else 0.0

    def generate_all_sources(self) -> Dict:
        """Generate all-sources.json with complete list"""
        all_sources = []

        for source in self.sources:
            quality_score = self._calculate_quality_score(source.get('quality', {}))

            entry = {
                'id': source['id'],
                'name': source['name'],
                'organization': source['organization']['name'],
                'organization_type': source['organization']['type'],
                'description': source.get('description', {}),
                'url': source['access']['primary_url'],
                'domains': source['coverage']['domains'],
                'geographic_scope': source['coverage']['geographic']['scope'],
                'update_frequency': source['coverage']['temporal'].get('update_frequency'),
                'quality_score': quality_score,
                'access_level': source['access']['access_level'],
                'indicators': source['coverage'].get('indicators'),
                'status': source['catalog_metadata']['status'],
                'file_path': source['_file_path']
            }

            all_sources.append(entry)

        # Sort by quality score (descending) then by name
        all_sources.sort(key=lambda x: (-x['quality_score'], x['name']['en']))

        result = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_sources': len(all_sources),
                'version': '1.0'
            },
            'sources': all_sources
        }

        return result

    def generate_by_domain(self) -> Dict:
        """Generate by-domain.json grouped by domain"""
        by_domain = defaultdict(list)

        for source in self.sources:
            domains = source['coverage']['domains']
            quality_score = self._calculate_quality_score(source.get('quality', {}))

            entry = {
                'id': source['id'],
                'name': source['name'],
                'organization': source['organization']['name'],
                'url': source['access']['primary_url'],
                'quality_score': quality_score,
                'file_path': source['_file_path']
            }

            for domain in domains:
                by_domain[domain].append(entry)

        # Sort sources within each domain
        for domain in by_domain:
            by_domain[domain].sort(key=lambda x: (-x['quality_score'], x['name']['en']))

        # Convert to regular dict and sort by domain name
        result = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_domains': len(by_domain),
                'total_sources': len(self.sources),
                'version': '1.0'
            },
            'domains': dict(sorted(by_domain.items()))
        }

        return result

    def generate_by_region(self) -> Dict:
        """Generate by-region.json grouped by geographic scope"""
        by_region = defaultdict(list)

        for source in self.sources:
            scope = source['coverage']['geographic']['scope']
            country = source['organization'].get('country')
            quality_score = self._calculate_quality_score(source.get('quality', {}))

            # Determine region key
            if scope == 'global':
                region_key = 'global'
            elif scope == 'national' and country:
                region_key = country
            elif scope == 'regional':
                regions = source['coverage']['geographic'].get('regions', ['regional'])
                region_key = regions[0] if regions else 'regional'
            else:
                region_key = scope

            entry = {
                'id': source['id'],
                'name': source['name'],
                'organization': source['organization']['name'],
                'url': source['access']['primary_url'],
                'quality_score': quality_score,
                'geographic_scope': scope,
                'file_path': source['_file_path']
            }

            by_region[region_key].append(entry)

        # Sort sources within each region
        for region in by_region:
            by_region[region].sort(key=lambda x: (-x['quality_score'], x['name']['en']))

        result = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_regions': len(by_region),
                'total_sources': len(self.sources),
                'version': '1.0'
            },
            'regions': dict(sorted(by_region.items()))
        }

        return result

    def generate_by_authority(self) -> Dict:
        """Generate by-authority.json grouped by quality score"""
        by_authority = {
            '5_star': [],
            '4_star': [],
            '3_star': [],
            '2_star': [],
            '1_star': []
        }

        for source in self.sources:
            quality_score = self._calculate_quality_score(source.get('quality', {}))

            entry = {
                'id': source['id'],
                'name': source['name'],
                'organization': source['organization']['name'],
                'url': source['access']['primary_url'],
                'quality_score': quality_score,
                'quality_breakdown': source.get('quality', {}),
                'file_path': source['_file_path']
            }

            # Categorize by rounded score
            if quality_score >= 4.5:
                by_authority['5_star'].append(entry)
            elif quality_score >= 3.5:
                by_authority['4_star'].append(entry)
            elif quality_score >= 2.5:
                by_authority['3_star'].append(entry)
            elif quality_score >= 1.5:
                by_authority['2_star'].append(entry)
            else:
                by_authority['1_star'].append(entry)

        # Sort within each category
        for category in by_authority:
            by_authority[category].sort(key=lambda x: (-x['quality_score'], x['name']['en']))

        result = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_sources': len(self.sources),
                'average_quality': round(sum(self._calculate_quality_score(s.get('quality', {})) for s in self.sources) / len(self.sources), 2) if self.sources else 0,
                'version': '1.0'
            },
            'by_rating': by_authority
        }

        return result

    def generate_statistics(self) -> Dict:
        """Generate statistics.json with overview statistics"""
        total_indicators = sum(s['coverage'].get('indicators', 0) for s in self.sources)
        avg_quality = sum(self._calculate_quality_score(s.get('quality', {})) for s in self.sources) / len(self.sources) if self.sources else 0

        # Count by organization type
        org_types = defaultdict(int)
        for source in self.sources:
            org_types[source['organization']['type']] += 1

        # Count by access level
        access_levels = defaultdict(int)
        for source in self.sources:
            access_levels[source['access']['access_level']] += 1

        # Count by status
        statuses = defaultdict(int)
        for source in self.sources:
            statuses[source['catalog_metadata']['status']] += 1

        # Count by update frequency
        frequencies = defaultdict(int)
        for source in self.sources:
            freq = source['coverage']['temporal'].get('update_frequency', 'unknown')
            frequencies[freq] += 1

        # Domain counts
        domain_counts = defaultdict(int)
        for source in self.sources:
            for domain in source['coverage']['domains']:
                domain_counts[domain] += 1

        result = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '1.0'
            },
            'overview': {
                'total_sources': len(self.sources),
                'total_indicators': total_indicators,
                'average_quality_score': round(avg_quality, 2),
                'active_sources': statuses.get('active', 0),
                'last_updated': datetime.now().strftime('%Y-%m-%d')
            },
            'by_organization_type': dict(org_types),
            'by_access_level': dict(access_levels),
            'by_status': dict(statuses),
            'by_update_frequency': dict(frequencies),
            'by_domain': dict(sorted(domain_counts.items(), key=lambda x: -x[1]))
        }

        return result

    def generate_all(self):
        """Generate all index files"""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        indexes = {
            'all-sources.json': self.generate_all_sources(),
            'by-domain.json': self.generate_by_domain(),
            'by-region.json': self.generate_by_region(),
            'by-authority.json': self.generate_by_authority(),
            'statistics.json': self.generate_statistics()
        }

        for filename, data in indexes.items():
            output_path = self.output_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Generated: {output_path}")

        print(f"\nSuccessfully generated {len(indexes)} index files!")


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate index files for DataSource Hub',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all indexes (default)
  python generate_indexes.py

  # Specify custom source directory
  python generate_indexes.py --sources ../sources

  # Specify custom output directory
  python generate_indexes.py --output ../public/indexes
        """
    )

    parser.add_argument(
        '--sources',
        default='sources',
        help='Source directory containing JSON files (default: sources)'
    )

    parser.add_argument(
        '--output',
        default='indexes',
        help='Output directory for index files (default: indexes)'
    )

    args = parser.parse_args()

    sources_dir = Path(args.sources)
    output_dir = Path(args.output)

    if not sources_dir.exists():
        print(f"❌ Error: Source directory not found: {sources_dir}")
        sys.exit(1)

    print("=" * 70)
    print("DataSource Hub - Index Generator")
    print("=" * 70)
    print(f"Source directory: {sources_dir}")
    print(f"Output directory: {output_dir}")
    print()

    generator = IndexGenerator(sources_dir, output_dir)
    generator.generate_all()

    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
