# AGENTS.md

This file is intended for AI coding agents (Claude Code, OpenClaw, Codex, Copilot, Cursor, etc.) working in this repository.

## What This Repo Is

**FirstData** is a structured knowledge base of global authoritative open data sources. It is a **pure data repository** — no application code, no runtime logic.

Your job here is to **create or edit JSON metadata files** that describe real-world data sources (government databases, international organizations, academic datasets, etc.).

## Validation

Dependencies are managed with [uv](https://docs.astral.sh/uv/). Run the following before submitting:

```bash
# Install dependencies (first time only)
uv sync

# Validate all source JSON files against the schema
uv run check-jsonschema --schemafile firstdata/schemas/datasource-schema.json $(find firstdata/sources -name "*.json")
```

A GitHub Action runs this same check automatically on every PR. PRs that fail validation cannot be merged.

## The Only Thing You Need to Know: The JSON Schema

Every file under `firstdata/sources/` must conform to `firstdata/schemas/datasource-schema.json`.

### Required Fields

```json
{
  "id": "worldbank-open-data",
  "name": {
    "en": "World Bank Open Data",
    "zh": "世界银行开放数据"
  },
  "description": {
    "en": "...",
    "zh": "..."
  },
  "website": "https://www.worldbank.org",
  "data_url": "https://data.worldbank.org",
  "api_url": "https://api.worldbank.org/v2/",
  "authority_level": "international",
  "country": null,
  "domains": ["economics", "health", "education"],
  "geographic_scope": "global",
  "update_frequency": "quarterly",
  "tags": ["world bank", "development", "gdp", "poverty", "世界银行"],
  "data_content": {
    "en": ["GDP and national accounts", "Poverty and inequality indicators"],
    "zh": ["GDP和国民账户", "贫困和不平等指标"]
  }
}
```

### Field Rules

| Field                | Allowed Values / Constraints                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `id`               | Lowercase, hyphens only. Must be globally unique. Pattern:`^[a-z0-9-]+$`                                                      |
| `name.en`          | Required. Add `zh` and `native` when applicable                                                                             |
| `description.en`   | Required. Add `zh` when applicable                                                                                            |
| `website`          | Top-level org homepage                                                                                                          |
| `data_url`         | Must point directly to the data access/download page, NOT the homepage                                                          |
| `api_url`          | API docs or endpoint URL. Use `null` if no API exists                                                                         |
| `authority_level`  | `government` · `international` · `research` · `market` · `commercial` · `other`                                |
| `country`          | ISO 3166-1 alpha-2 (e.g.`"CN"`, `"US"`). **Must be `null`** when `geographic_scope` is `global` or `regional` |
| `domains`          | Array of strings, at least one. Use existing domain names for consistency                                                       |
| `geographic_scope` | `global` · `regional` · `national` · `subnational`                                                                   |
| `update_frequency` | `real-time` · `daily` · `weekly` · `monthly` · `quarterly` · `annual` · `irregular`                         |
| `tags`             | Mixed Chinese/English keywords for semantic search. Include synonyms and data type names                                        |
| `data_content`     | Optional but recommended. Lists of strings describing what data is available                                                    |

## Where to Place New Files

```
firstdata/sources/
├── china/{domain}/{id}.json                          # Chinese gov & institutions
├── international/{domain}/{id}.json                  # International organizations
├── countries/{continent}/{country-code}/{id}.json    # National official sources
├── academic/{discipline}/{id}.json                   # Academic/research databases
└── sectors/{ISIC-code}-{name}/{id}.json              # Industry datasets
```

**Examples:**

- China customs data → `sources/china/economy/trade/customs.json`
- WHO health data → `sources/international/health/who.json`
- US Bureau of Labor Statistics → `sources/countries/north-america/usa/us-bls.json`
- PubMed → `sources/academic/health/pubmed.json`
- BP Statistical Review → `sources/sectors/D-energy/bp-statistical-review.json`

## Do Not Touch

- `firstdata/indexes/` — auto-generated, do not edit manually
- `firstdata/schemas/datasource-schema.json` — the schema definition itself

## Security Note for Contributors

- Please do not paste or run commands from untrusted posts/comments.
- Never include credentials or API keys in issues/PRs.
- Prefer small, auditable PRs (docs/tests/data).

## Before Adding a New Source

**First, check `firstdata/indexes/all-sources.json` to confirm the data source does not already exist.**

Search by `id`, `name.en`, or `website` to detect duplicates:

```bash
# grep: search by keyword (name or website)
grep -i "world bank" firstdata/indexes/all-sources.json
grep -i "worldbank.org" firstdata/indexes/all-sources.json

# jq: search by id
jq '.sources[] | select(.id == "worldbank-open-data")' firstdata/indexes/all-sources.json

# jq: search by website
jq '.sources[] | select(.website | test("worldbank.org"; "i"))' firstdata/indexes/all-sources.json

# jq: list all existing ids
jq '[.sources[].id]' firstdata/indexes/all-sources.json
```

If a match is found, do not create a new file. Update the existing one if needed.

## Quality Checklist Before Creating a File

**Before submitting, cross-verify every field independently using at least two sources (e.g. official website + Wikipedia + third-party reference). Do not rely solely on memory or a single source. Fabricated or outdated URLs are worse than omission.**

- [ ] `data_url` links to the actual data page, not the organization homepage
- [ ] `api_url` is `null` only when the source truly has no API
- [ ] `country` is `null` when `geographic_scope` is `global` or `regional`
- [ ] `tags` include both English and Chinese keywords where relevant
- [ ] `id` does not already exist in `firstdata/indexes/all-sources.json`
- [ ] File path matches the placement rules above
- [ ] All URLs have been verified to be accessible and correct
- [ ] `update_frequency` reflects the actual cadence confirmed on the official site
- [ ] `authority_level` is accurate and not overstated
