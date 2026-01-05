#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataSource Hub - Metadata Validation Script
Validates JSON data source files against the schema
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import re
from datetime import datetime

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("❌ Error: jsonschema package not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)


class DataSourceValidator:
    """Validator for data source metadata files"""

    def __init__(self, schema_path: str = None):
        """Initialize validator with schema"""
        if schema_path is None:
            # Default to schemas/datasource-schema.json
            schema_path = Path(__file__).parent.parent / "schemas" / "datasource-schema.json"

        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)

        self.errors = []
        self.warnings = []

    def validate_file(self, file_path: Path) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a single data source file

        Returns:
            (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False, self.errors, self.warnings
        except Exception as e:
            self.errors.append(f"Error reading file: {e}")
            return False, self.errors, self.warnings

        # 1. Schema validation
        try:
            validate(instance=data, schema=self.schema)
        except ValidationError as e:
            self.errors.append(f"Schema validation failed: {e.message}")
            return False, self.errors, self.warnings

        # 2. Content validation
        self._validate_content(data, file_path)

        # 3. Logic validation
        self._validate_logic(data)

        return len(self.errors) == 0, self.errors, self.warnings

    def _validate_content(self, data: Dict, file_path: Path):
        """Validate content-specific rules"""

        # Check URL format
        url = data.get('access', {}).get('primary_url', '')
        if not url.startswith(('http://', 'https://')):
            self.errors.append(f"Invalid URL format: {url}")

        # Check quality ratings (1-5)
        quality = data.get('quality', {})
        for key in ['authority_level', 'methodology_transparency', 'update_timeliness',
                    'data_completeness', 'documentation_quality']:
            value = quality.get(key)
            if value is not None and not (1 <= value <= 5):
                self.errors.append(f"Quality rating '{key}' must be 1-5, got {value}")

        # Check date formats (YYYY-MM-DD)
        catalog_meta = data.get('catalog_metadata', {})
        for date_field in ['added_date', 'last_updated', 'verified_date']:
            date_str = catalog_meta.get(date_field)
            if date_str:
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                    self.errors.append(f"Invalid date format for '{date_field}': {date_str} (expected YYYY-MM-DD)")
                else:
                    try:
                        datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        self.errors.append(f"Invalid date value for '{date_field}': {date_str}")

        # Check language codes (ISO 639-1)
        languages = data.get('data_characteristics', {}).get('languages', [])
        for lang in languages:
            if not re.match(r'^[a-z]{2}$', lang):
                self.errors.append(f"Invalid language code: {lang} (expected ISO 639-1)")

        # Check country code (ISO 3166-1)
        country = data.get('organization', {}).get('country')
        if country and country != 'null' and not re.match(r'^[A-Z]{2}$', country):
            self.errors.append(f"Invalid country code: {country} (expected ISO 3166-1 alpha-2)")

        # Check ID format
        data_id = data.get('id', '')
        if not re.match(r'^[a-z0-9-]+$', data_id):
            self.errors.append(f"Invalid ID format: {data_id} (must be lowercase, hyphen-separated)")

        # Check file naming convention
        expected_filename = f"{data_id}.json"
        actual_filename = file_path.name
        if actual_filename != expected_filename:
            self.warnings.append(f"Filename mismatch: expected '{expected_filename}', got '{actual_filename}'")

        # Check bilingual completeness
        name = data.get('name', {})
        if 'en' in name and 'zh' not in name:
            self.warnings.append("Missing Chinese name (zh)")

        description = data.get('description', {})
        if 'en' in description and 'zh' not in description:
            self.warnings.append("Missing Chinese description (zh)")

        data_content = data.get('data_content', {})
        if data_content:
            en_count = len(data_content.get('en', []))
            zh_count = len(data_content.get('zh', []))
            if en_count != zh_count:
                self.warnings.append(f"Data content language mismatch: {en_count} EN items vs {zh_count} ZH items")

    def _validate_logic(self, data: Dict):
        """Validate logical consistency"""

        # Check temporal range
        temporal = data.get('coverage', {}).get('temporal', {})
        start_year = temporal.get('start_year')
        end_year = temporal.get('end_year')

        if start_year and end_year:
            if start_year > end_year:
                self.errors.append(f"Invalid temporal range: start_year ({start_year}) > end_year ({end_year})")

            current_year = datetime.now().year
            if end_year > current_year + 1:
                self.warnings.append(f"End year ({end_year}) is in the future")

        # Check status
        status = data.get('catalog_metadata', {}).get('status')
        if status == 'inactive' or status == 'deprecated':
            self.warnings.append(f"Data source status is '{status}'")

        # Check quality score average
        quality = data.get('quality', {})
        scores = [
            quality.get('authority_level', 0),
            quality.get('methodology_transparency', 0),
            quality.get('update_timeliness', 0),
            quality.get('data_completeness', 0),
            quality.get('documentation_quality', 0)
        ]
        avg_score = sum(scores) / len(scores) if scores else 0
        if avg_score < 3.0:
            self.warnings.append(f"Low average quality score: {avg_score:.1f}/5.0")


def validate_directory(directory: Path, schema_path: str = None) -> Dict:
    """
    Validate all JSON files in a directory

    Returns:
        Dictionary with validation results
    """
    validator = DataSourceValidator(schema_path)

    results = {
        'total': 0,
        'valid': 0,
        'invalid': 0,
        'files': []
    }

    json_files = sorted(directory.rglob('*.json'))

    # Exclude schema files
    json_files = [f for f in json_files if 'schemas' not in f.parts and 'indexes' not in f.parts]

    for json_file in json_files:
        results['total'] += 1
        is_valid, errors, warnings = validator.validate_file(json_file)

        file_result = {
            'path': str(json_file),
            'valid': is_valid,
            'errors': errors,
            'warnings': warnings
        }

        results['files'].append(file_result)

        if is_valid:
            results['valid'] += 1
        else:
            results['invalid'] += 1

    return results


def print_results(results: Dict, verbose: bool = False):
    """Print validation results"""

    print("=" * 70)
    print("DataSource Hub - Validation Report")
    print("=" * 70)
    print()

    print(f"Summary:")
    print(f"   Total files:   {results['total']}")
    print(f"   Valid:         {results['valid']}")
    print(f"   Invalid:       {results['invalid']}")
    print(f"   Success rate:  {results['valid']/results['total']*100:.1f}%")
    print()

    # Show invalid files
    if results['invalid'] > 0:
        print("[INVALID] Invalid Files:")
        print("-" * 70)
        for file_result in results['files']:
            if not file_result['valid']:
                print(f"\nFile: {file_result['path']}")
                for error in file_result['errors']:
                    print(f"   ERROR: {error}")
                if verbose and file_result['warnings']:
                    for warning in file_result['warnings']:
                        print(f"   WARN: {warning}")
        print()

    # Show warnings for valid files (if verbose)
    if verbose:
        files_with_warnings = [f for f in results['files'] if f['valid'] and f['warnings']]
        if files_with_warnings:
            print("[WARNINGS] Valid Files with Warnings:")
            print("-" * 70)
            for file_result in files_with_warnings:
                print(f"\nFile: {file_result['path']}")
                for warning in file_result['warnings']:
                    print(f"   WARN: {warning}")
            print()

    # Show all valid files (if verbose)
    if verbose and results['valid'] > 0:
        print("[VALID] Valid Files:")
        print("-" * 70)
        for file_result in results['files']:
            if file_result['valid']:
                warnings_count = len(file_result['warnings'])
                warning_str = f" ({warnings_count} warnings)" if warnings_count > 0 else ""
                print(f"   OK: {file_result['path']}{warning_str}")
        print()

    print("=" * 70)


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate DataSource Hub metadata files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate all sources
  python validate.py

  # Validate specific directory
  python validate.py sources/china

  # Validate with verbose output
  python validate.py -v

  # Use custom schema
  python validate.py --schema custom-schema.json
        """
    )

    parser.add_argument(
        'directory',
        nargs='?',
        default='sources',
        help='Directory to validate (default: sources)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output including warnings'
    )

    parser.add_argument(
        '--schema',
        help='Path to JSON schema file (default: schemas/datasource-schema.json)'
    )

    args = parser.parse_args()

    # Get directory path
    directory = Path(args.directory)
    if not directory.exists():
        print(f"❌ Error: Directory not found: {directory}")
        sys.exit(1)

    # Run validation
    results = validate_directory(directory, args.schema)

    # Print results
    print_results(results, args.verbose)

    # Exit with error code if validation failed
    if results['invalid'] > 0:
        sys.exit(1)
    else:
        print("[SUCCESS] All validations passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()
