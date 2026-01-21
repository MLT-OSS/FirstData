#!/usr/bin/env python3
"""
FirstData - Metadata Validation Script
Validates JSON data source files against the schema
"""

import json
import re
import sys
from pathlib import Path

try:
    # import jsonschema
    from jsonschema import ValidationError, validate
except ImportError:
    print("❌ Error: jsonschema package not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)


class DataSourceValidator:
    """Validator for data source metadata files"""

    def __init__(self, schema_path: str | None = None):
        """Initialize validator with schema"""
        if schema_path is None:
            # Default to schemas/datasource-schema.json
            schema_path = Path(__file__).parent.parent / "schemas" / "datasource-schema.json"

        with open(schema_path, encoding="utf-8") as f:
            self.schema = json.load(f)

        self.errors = []
        self.warnings = []

    def validate_file(self, file_path: Path) -> tuple[bool, list[str], list[str]]:
        """
        Validate a single data source file

        Returns:
            (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        try:
            with open(file_path, encoding="utf-8") as f:
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

    def _validate_content(self, data: dict, file_path: Path):
        """Validate content-specific rules"""

        # Check URL formats (v2 schema)
        website = data.get("website", "")
        if website and not website.startswith(("http://", "https://")):
            self.errors.append(f"Invalid website URL format: {website}")

        data_url = data.get("data_url", "")
        if data_url and not data_url.startswith(("http://", "https://")):
            self.errors.append(f"Invalid data_url format: {data_url}")

        api_url = data.get("api_url")
        if api_url and not api_url.startswith(("http://", "https://")):
            self.errors.append(f"Invalid api_url format: {api_url}")

        # Check authority_level (v2 schema)
        authority_level = data.get("authority_level", "")
        valid_levels = ["government", "international", "market", "research", "commercial", "other"]
        if authority_level and authority_level not in valid_levels:
            self.errors.append(
                f"Invalid authority_level: {authority_level} (must be one of {valid_levels})"
            )

        # Check country code (ISO 3166-1)
        country = data.get("country")
        if country and country != "null" and not re.match(r"^[A-Z]{2}$", country):
            self.errors.append(f"Invalid country code: {country} (expected ISO 3166-1 alpha-2)")

        # Check country and geographic_scope consistency
        geo_scope = data.get("geographic_scope", "")
        if geo_scope in ["global", "regional"] and country:
            self.errors.append(
                f"geographic_scope='{geo_scope}' but country='{country}' (should be null)"
            )
        if geo_scope in ["national", "subnational"] and not country:
            self.warnings.append(
                f"geographic_scope='{geo_scope}' but country is null (should have a value)"
            )

        # Check ID format
        data_id = data.get("id", "")
        if not re.match(r"^[a-z0-9-]+$", data_id):
            self.errors.append(
                f"Invalid ID format: {data_id} (must be lowercase, hyphen-separated)"
            )

        # Check file naming convention
        expected_filename = f"{data_id}.json"
        actual_filename = file_path.name
        if actual_filename != expected_filename:
            self.warnings.append(
                f"Filename mismatch: expected '{expected_filename}', got '{actual_filename}'"
            )

        # Check bilingual completeness
        name = data.get("name", {})
        if "en" in name and "zh" not in name:
            self.warnings.append("Missing Chinese name (zh)")

        description = data.get("description", {})
        if "en" in description and "zh" not in description:
            self.warnings.append("Missing Chinese description (zh)")

        data_content = data.get("data_content", {})
        if data_content:
            en_count = len(data_content.get("en", []))
            zh_count = len(data_content.get("zh", []))
            if en_count != zh_count:
                self.warnings.append(
                    f"Data content language mismatch: {en_count} EN items vs {zh_count} ZH items"
                )

    def _validate_logic(self, data: dict):
        """Validate logical consistency"""

        # Check update_frequency validity
        update_freq = data.get("update_frequency", "")
        valid_frequencies = [
            "real-time",
            "daily",
            "weekly",
            "monthly",
            "quarterly",
            "annual",
            "irregular",
        ]
        if update_freq and update_freq not in valid_frequencies:
            self.warnings.append(f"Non-standard update_frequency: {update_freq}")

        # Check domains
        domains = data.get("domains", [])
        if not domains:
            self.warnings.append("No domains specified")

        # Check tags
        tags = data.get("tags", [])
        if not tags:
            self.warnings.append("No tags specified (will affect discoverability)")


def validate_directory(directory: Path, schema_path: str | None = None) -> dict:
    """
    Validate all JSON files in a directory

    Returns:
        Dictionary with validation results
    """
    validator = DataSourceValidator(schema_path)

    results = {"total": 0, "valid": 0, "invalid": 0, "files": []}

    json_files = sorted(directory.rglob("*.json"))

    # Exclude schema files
    json_files = [f for f in json_files if "schemas" not in f.parts and "indexes" not in f.parts]

    for json_file in json_files:
        results["total"] += 1
        is_valid, errors, warnings = validator.validate_file(json_file)

        file_result = {
            "path": str(json_file),
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
        }

        results["files"].append(file_result)

        if is_valid:
            results["valid"] += 1
        else:
            results["invalid"] += 1

    return results


def print_results(results: dict, verbose: bool = False):
    """Print validation results"""

    print("=" * 70)
    print("FirstData - Validation Report")
    print("=" * 70)
    print()

    print("Summary:")
    print(f"   Total files:   {results['total']}")
    print(f"   Valid:         {results['valid']}")
    print(f"   Invalid:       {results['invalid']}")
    print(f"   Success rate:  {results['valid'] / results['total'] * 100:.1f}%")
    print()

    # Show invalid files
    if results["invalid"] > 0:
        print("[INVALID] Invalid Files:")
        print("-" * 70)
        for file_result in results["files"]:
            if not file_result["valid"]:
                print(f"\nFile: {file_result['path']}")
                for error in file_result["errors"]:
                    print(f"   ERROR: {error}")
                if verbose and file_result["warnings"]:
                    for warning in file_result["warnings"]:
                        print(f"   WARN: {warning}")
        print()

    # Show warnings for valid files (if verbose)
    if verbose:
        files_with_warnings = [f for f in results["files"] if f["valid"] and f["warnings"]]
        if files_with_warnings:
            print("[WARNINGS] Valid Files with Warnings:")
            print("-" * 70)
            for file_result in files_with_warnings:
                print(f"\nFile: {file_result['path']}")
                for warning in file_result["warnings"]:
                    print(f"   WARN: {warning}")
            print()

    # Show all valid files (if verbose)
    if verbose and results["valid"] > 0:
        print("[VALID] Valid Files:")
        print("-" * 70)
        for file_result in results["files"]:
            if file_result["valid"]:
                warnings_count = len(file_result["warnings"])
                warning_str = f" ({warnings_count} warnings)" if warnings_count > 0 else ""
                print(f"   OK: {file_result['path']}{warning_str}")
        print()

    print("=" * 70)


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate FirstData metadata files",
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
        """,
    )

    parser.add_argument(
        "directory", nargs="?", default="sources", help="Directory to validate (default: sources)"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed output including warnings"
    )

    parser.add_argument(
        "--schema", help="Path to JSON schema file (default: schemas/datasource-schema.json)"
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
    if results["invalid"] > 0:
        sys.exit(1)
    else:
        print("[SUCCESS] All validations passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
