.PHONY: validate check-ids check build-indexes help

help:
	@echo "Usage:"
	@echo "  make validate       Validate all source JSON files against the schema"
	@echo "  make check-ids      Check for duplicate IDs across all source files"
	@echo "  make check          Run all checks (validate + check-ids)"
	@echo "  make build-indexes  Rebuild all index and badge files"

validate:
	@echo "Validating source JSON files..."
	@find firstdata/sources -name "*.json" | xargs uv run check-jsonschema \
		--schemafile firstdata/schemas/datasource-schema.json
	@echo "✅ All files are valid."

check-ids:
	@echo "Checking for duplicate IDs..."
	@uv run python scripts/check_ids.py

check: validate check-ids

build-indexes:
	@echo "Building indexes and badges..."
	@uv run python scripts/build_indexes.py
