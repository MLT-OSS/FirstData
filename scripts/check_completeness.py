#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataSource Hub - Completeness Check Script
Checks metadata field completeness and calculates quality score
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class CompletenessChecker:
    """Check metadata completeness based on field categories"""

    # Field categories based on quality-criteria.md
    REQUIRED_FIELDS = [
        'id',
        'name',
        'name.en',
        'name.zh',
        'organization',
        'organization.name',
        'description',
        'description.en',
        'access',
        'access.primary_url',
        'access.access_level',
        'coverage',
        'coverage.geographic',
        'coverage.temporal',
        'coverage.domains',
        'data_characteristics',
        'quality',
        'quality.authority_level',
        'quality.methodology_transparency',
        'quality.update_timeliness',
        'quality.data_completeness',
        'quality.documentation_quality',
        'licensing',
        'catalog_metadata',
        'catalog_metadata.added_date',
        'catalog_metadata.last_updated',
        'catalog_metadata.status',
    ]

    RECOMMENDED_FIELDS = [
        'organization.country',
        'organization.website',
        'description.zh',  # For Chinese sources
        'coverage.geographic.scope',
        'coverage.geographic.countries',
        'coverage.temporal.start_year',
        'coverage.temporal.end_year',
        'coverage.temporal.update_frequency',
        'coverage.indicators',
        'access.api',
        'access.api.available',
        'access.download',
        'data_content',
        'data_content.en',
        'data_characteristics.types',
        'data_characteristics.formats',
        'data_characteristics.languages',
        'licensing.license',
        'licensing.commercial_use',
        'contact',
        'tags',
        'catalog_metadata.verified_date',
        'catalog_metadata.contributor',
    ]

    OPTIONAL_FIELDS = [
        'name.native',
        'organization.type',
        'access.api.documentation',
        'access.api.version',
        'access.api.authentication',
        'access.download.formats',
        'access.registration_required',
        'coverage.geographic.regions',
        'data_content.zh',
        'data_characteristics.granularity',
        'quality.citation_count',
        'licensing.attribution_required',
        'licensing.restrictions',
        'metadata',
        'metadata.standards_followed',
        'metadata.data_dictionary',
        'metadata.methodology_docs',
        'usage',
        'usage.use_cases',
        'related_sources',
        'contact.email',
        'contact.support_url',
    ]

    def __init__(self):
        self.data = None
        self.results = {
            'required': {'total': 0, 'present': 0, 'missing': []},
            'recommended': {'total': 0, 'present': 0, 'missing': []},
            'optional': {'total': 0, 'present': 0, 'missing': []}
        }

    def get_nested_field(self, data: Dict, field_path: str) -> Tuple[bool, any]:
        """Get value from nested dictionary using dot notation"""
        keys = field_path.split('.')
        value = data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return False, None

        # Field exists, check if it has meaningful value
        if value is None or value == '' or value == []:
            return False, None

        return True, value

    def check_fields(self, data: Dict, field_list: List[str], category: str):
        """Check if fields in the list are present"""
        for field in field_list:
            self.results[category]['total'] += 1
            exists, value = self.get_nested_field(data, field)

            if exists:
                self.results[category]['present'] += 1
            else:
                self.results[category]['missing'].append(field)

    def calculate_completeness(self) -> float:
        """Calculate overall completeness score using weighted formula"""
        req_pct = (self.results['required']['present'] /
                   self.results['required']['total'] * 100) if self.results['required']['total'] > 0 else 0

        rec_pct = (self.results['recommended']['present'] /
                   self.results['recommended']['total'] * 100) if self.results['recommended']['total'] > 0 else 0

        opt_pct = (self.results['optional']['present'] /
                   self.results['optional']['total'] * 100) if self.results['optional']['total'] > 0 else 0

        # Formula: Required(50%) + Recommended(35%) + Optional(15%)
        completeness = (req_pct * 0.50) + (rec_pct * 0.35) + (opt_pct * 0.15)

        return completeness

    def get_rating(self, completeness: float) -> Tuple[str, str]:
        """Get rating and badge based on completeness score"""
        if completeness >= 90:
            return "优秀", "⭐⭐⭐⭐⭐"
        elif completeness >= 80:
            return "良好", "⭐⭐⭐⭐"
        elif completeness >= 70:
            return "合格", "⭐⭐⭐"
        elif completeness >= 60:
            return "及格", "⭐⭐"
        else:
            return "不合格", "❌"

    def check_file(self, file_path: Path, verbose: bool = True) -> bool:
        """Check completeness of a single data source file"""
        if verbose:
            print(f"\n{'='*70}")
            print(f"检查文件: {file_path}")
            print(f"{'='*70}\n")

        # Load JSON file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ 错误: 无效的 JSON 格式: {e}")
            return False
        except Exception as e:
            print(f"❌ 错误: 无法读取文件: {e}")
            return False

        # Check fields by category
        self.check_fields(self.data, self.REQUIRED_FIELDS, 'required')
        self.check_fields(self.data, self.RECOMMENDED_FIELDS, 'recommended')
        self.check_fields(self.data, self.OPTIONAL_FIELDS, 'optional')

        # Calculate completeness
        completeness = self.calculate_completeness()
        rating, badge = self.get_rating(completeness)

        # Print results
        if verbose:
            req_pct = (self.results['required']['present'] /
                       self.results['required']['total'] * 100)
            rec_pct = (self.results['recommended']['present'] /
                       self.results['recommended']['total'] * 100)
            opt_pct = (self.results['optional']['present'] /
                       self.results['optional']['total'] * 100)

            print(f"必需字段: {req_pct:.0f}% ({self.results['required']['present']}/{self.results['required']['total']})")
            print(f"推荐字段: {rec_pct:.0f}% ({self.results['recommended']['present']}/{self.results['recommended']['total']})")
            print(f"可选字段: {opt_pct:.0f}% ({self.results['optional']['present']}/{self.results['optional']['total']})")
            print()
            print(f"总体完成度: {completeness:.1f}%")
            print(f"评级: {rating} {badge}")
            print()

            # Check minimum requirements
            meets_requirements = True
            if req_pct < 100:
                print(f"⚠️  警告: 必需字段未达到 100%")
                meets_requirements = False
            if rec_pct < 80:
                print(f"⚠️  警告: 推荐字段未达到 80%")
                meets_requirements = False
            if completeness < 70:
                print(f"❌ 错误: 总体完成度未达到最低标准 70%")
                meets_requirements = False

            if meets_requirements:
                print(f"✅ 满足最低收录标准")
            print()

            # Show missing required fields
            if self.results['required']['missing']:
                print(f"缺失的必需字段 ({len(self.results['required']['missing'])}):")
                for field in self.results['required']['missing']:
                    print(f"  - {field}")
                print()

            # Show missing recommended fields (top 5)
            if self.results['recommended']['missing']:
                missing_count = len(self.results['recommended']['missing'])
                print(f"缺失的推荐字段 ({missing_count}):")
                for field in self.results['recommended']['missing'][:5]:
                    print(f"  - {field}")
                if missing_count > 5:
                    print(f"  ... 还有 {missing_count - 5} 个")
                print()

            print(f"{'='*70}\n")

        # Return True if meets minimum requirements
        req_pct = (self.results['required']['present'] /
                   self.results['required']['total'] * 100)
        rec_pct = (self.results['recommended']['present'] /
                   self.results['recommended']['total'] * 100)

        return req_pct == 100 and rec_pct >= 80 and completeness >= 70


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Check metadata completeness for DataSource Hub files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check single file
  python check_completeness.py sources/china/finance/banking/pbc.json

  # Quiet mode (only show summary)
  python check_completeness.py sources/china/finance/banking/pbc.json -q

Completeness Formula:
  Completeness = (Required × 50%) + (Recommended × 35%) + (Optional × 15%)

Minimum Requirements:
  - Required fields: 100%
  - Recommended fields: ≥80%
  - Overall completeness: ≥70%
        """
    )

    parser.add_argument(
        'file',
        type=str,
        help='JSON file to check'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode (less verbose output)'
    )

    args = parser.parse_args()

    # Get file path
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ 错误: 文件不存在: {file_path}")
        sys.exit(1)

    if not file_path.is_file():
        print(f"❌ 错误: 路径不是文件: {file_path}")
        sys.exit(1)

    # Check completeness
    checker = CompletenessChecker()
    passed = checker.check_file(file_path, verbose=not args.quiet)

    if passed:
        print("✅ 完整性检查通过!")
        sys.exit(0)
    else:
        print("❌ 完整性检查未通过")
        sys.exit(1)


if __name__ == '__main__':
    main()
