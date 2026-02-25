# Standard Domain Names Reference

**Version**: 1.0
**Last Updated**: 2026-02-25

## Purpose

This document defines the standard naming convention for the `domains` field in FirstData source metadata files.

## Naming Convention

**All domain names MUST use lowercase letters.**

### Rationale

- **Consistency**: Ensures uniform categorization across all 1000+ planned data sources
- **Searchability**: Simplifies programmatic filtering and search operations
- **Maintenance**: Reduces confusion and prevents duplicate categories
- **Internationalization**: Lowercase is more neutral across different language contexts

### Examples

✅ **Correct**:
```json
"domains": ["economics", "finance", "trade"]
```

❌ **Incorrect**:
```json
"domains": ["Economics", "Finance", "Trade"]
```

## Common Domains

Below are the most frequently used domains in the FirstData repository. This list is not exhaustive - you may use other domains as appropriate for your data source, but they **must be lowercase**.

### Top 30 Most Used Domains

| Domain | Description | Example Sources |
|--------|-------------|-----------------|
| `economics` | Economic data and indicators | World Bank, IMF, OECD |
| `health` | Healthcare, public health, medical data | WHO, CDC, PubMed |
| `environment` | Environmental monitoring, climate | NASA Earthdata, Copernicus |
| `education` | Educational statistics, assessments | PISA, IEA studies |
| `agriculture` | Agricultural production, food security | FAOSTAT, USDA |
| `finance` | Financial markets, banking | Central banks, BIS |
| `technology` | Tech industry, innovation | Patent offices, tech statistics |
| `trade` | International trade, customs | WTO, customs agencies |
| `demographics` | Population, census data | National statistical offices |
| `energy` | Energy production, consumption | IEA, EIA |
| `banking` | Banking sector statistics | Central banks |
| `manufacturing` | Industrial production | Industry associations |
| `development` | Economic development | Development banks |
| `social` | Social indicators, welfare | National statistics |
| `climate` | Climate data, meteorology | Weather agencies |
| `employment` | Labor market, unemployment | Labor statistics bureaus |
| `infrastructure` | Transport, utilities | Infrastructure agencies |
| `innovation` | R&D, patents | Patent offices, research agencies |
| `housing` | Real estate, construction | Housing agencies |
| `transportation` | Transport statistics | Transport authorities |
| `genomics` | Genetic data | Genome databases |
| `bioinformatics` | Biological data science | Bioinformatics repositories |
| `chemistry` | Chemical data | Chemical databases |
| `epidemiology` | Disease surveillance | Health agencies |
| `machine learning` | AI datasets | ML repositories |
| `industry` | Industry-specific data | Sector associations |
| `prices` | Price indices, inflation | Statistical agencies |
| `productivity` | Economic productivity | Research institutions |
| `monetary policy` | Central bank policy | Central banks |
| `securities` | Stock markets, bonds | Securities regulators |

## Multi-Word Domains

For multi-word concepts, use **lowercase with spaces** (not hyphens or underscores) for readability:

✅ **Correct**:
```json
"domains": ["machine learning", "climate change", "public health"]
```

❌ **Incorrect**:
```json
"domains": ["machine-learning", "Climate_Change", "PublicHealth"]
```

**Note**: Some legacy entries may use hyphens or underscores. These should be gradually migrated to the space-separated format.

## Domain Selection Guidelines

### 1. Use Existing Domains When Possible

Before creating a new domain, check:
- `firstdata/indexes/statistics.json` - see `by_domain` section
- `firstdata/schemas/suggested-standard-domains.json` - auto-generated list

### 2. Be Specific But Not Too Narrow

- ✅ Good: `renewable energy` (specific industry subdomain)
- ❌ Too narrow: `solar panel manufacturing` (overly specific)
- ❌ Too broad: `energy` when `renewable energy` is more accurate

### 3. Use 1-5 Domains Per Source

Most data sources should have 1-5 domain tags. More than 5 suggests the source may be too broad or domains are too specific.

### 4. Prefer General Over Specialized

When in doubt, use the more general domain:
- Use `health` rather than `epidemiology` unless the source is specifically focused on disease surveillance
- Use `finance` rather than `derivatives trading` unless that's the specific focus

## Validation

Domain consistency is automatically checked by:

```bash
# Manual check
make check-domains

# Full validation suite
make check
```

This check is also run automatically in CI/CD for all pull requests.

## Migration from Capitalized Domains

If you encounter source files with capitalized domains (e.g., `"Economics"`, `"Health"`), please update them to lowercase as part of your contribution:

```bash
# Find files with capitalized domains
python scripts/check_domains.py

# The script will identify all files needing updates
```

## Questions?

If you're unsure which domains to use for a data source:
1. Check similar sources in the same category
2. Review the top 30 list above
3. Ask in the project's GitHub issues

---

**See Also**:
- [Data Source Schema](datasource-schema.json)
- [AGENTS.md](../../AGENTS.md) - Contributor guidelines
- [Domain Analysis Script](../../scripts/analyze_domains.py)
