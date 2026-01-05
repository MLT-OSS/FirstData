# Project Context

## Purpose

**DataSource Hub** is the world's most comprehensive, authoritative, and structured open data source knowledge base. The project aims to help researchers, data analysts, policymakers, and developers quickly discover and access high-quality official data sources worldwide.

### Core Mission
- Create a centralized, structured metadata repository for authoritative data sources globally
- Provide deep coverage of Chinese official data sources (488 planned sources across 16 national domains)
- Establish a standardized 6-dimension quality rating system for data source evaluation
- Enable the data community to efficiently discover, access, and utilize official statistical data

### Key Differentiators
1. **Depth over Breadth**: Focus on authoritative official data sources with comprehensive 40+ field metadata
2. **China Coverage**: Global-leading deep coverage of Chinese government data sources (16 domains, 34 provinces)
3. **Quality Standards**: Rigorous 6-dimension quality assessment (authority, methodology, timeliness, completeness, documentation, citation)
4. **Professional Target**: Built for data professionals (analysts, researchers, developers), not general public

### Current Status
- **Total Data Sources**: 10/950+ planned (1% complete)
- **Quality Score**: 4.9/5.0 average (all sources are highly authoritative)
- **Milestone**: M0 (Project Initialization) ✅ Complete, M1 (High Priority Sources) 🚧 In Progress

## Tech Stack

### Core Technologies
- **Python 3.8+** - Primary scripting language for validation, automation, and tooling
- **JSON** - Data format for all metadata files (human-readable, version-control friendly)
- **JSON Schema (Draft-07)** - Strict schema validation for data quality
- **Git + GitHub** - Version control and collaboration platform
- **GitHub Actions** - CI/CD for automated validation and testing
- **Markdown** - Documentation format

### Key Python Dependencies
- `jsonschema` - JSON Schema validation
- `requests` - URL validation and accessibility checking
- Standard library: `json`, `pathlib`, `datetime`, `re`

### File Formats
- **Metadata**: `.json` files (UTF-8, 2-space indentation, LF line endings)
- **Documentation**: `.md` files (Markdown, bilingual Chinese/English)
- **Schema**: `.json` (JSON Schema Draft-07)

### Tools & Scripts
- `scripts/validate.py` - JSON schema and content validation
- `scripts/check_completeness.py` - Metadata completeness checking
- `scripts/generate_indexes.py` - Automated index generation
- Future: URL verification, CSV/Excel export tools

## Project Conventions

### Code Style

#### File Naming
- **Lowercase kebab-case**: All file names use lowercase with hyphens
  - Good: `world-bank.json`, `national-bureau-statistics.json`
  - Bad: `WorldBank.json`, `national_bureau_statistics.json`
- **Semantic naming**: File names should reflect the data source name or abbreviation
- **No special characters**: Only alphanumeric and hyphens allowed

#### JSON Formatting
- **Indentation**: 2 spaces (no tabs)
- **Encoding**: UTF-8 (no BOM)
- **Line endings**: Unix-style (LF)
- **Field ordering**: Alphabetical by key (with exceptions for id, name at top)
- **No trailing commas**: JSON spec compliance
- **Quote style**: Double quotes for all strings

#### Naming Conventions
- **IDs**: `lowercase-hyphen-format` (e.g., `china-nbs`, `world-bank`)
- **Field names**: `snake_case` (e.g., `authority_level`, `primary_url`)
- **Bilingual fields**: Nested objects with `en` and `zh` keys
  ```json
  "name": {
    "en": "English Name",
    "zh": "中文名称"
  }
  ```

#### Python Code Style
- Follow PEP 8 style guide
- UTF-8 encoding with shebang: `#!/usr/bin/env python3`
- Type hints where applicable
- Docstrings for all classes and functions

### Architecture Patterns

#### Data-First Architecture
- **JSON files as source of truth**: All data sources stored as validated JSON files
- **Schema-driven**: Strict JSON Schema (40+ fields) enforces data quality
- **File-based storage**: Git-friendly, no database required for core functionality
- **Static generation**: Indexes generated from source files, not stored separately

#### Directory Structure Pattern
```
sources/{category}/{subcategory}/{id}.json
```
Examples:
- `sources/china/finance/banking/pbc.json`
- `sources/international/economics/worldbank.json`
- `sources/academic/economics/nber.json`

#### Metadata Pattern
Every data source follows a consistent structure:
1. **Identification**: id, name (bilingual), organization
2. **Description**: Detailed bilingual descriptions
3. **Access Information**: URLs, API details, authentication requirements
4. **Coverage**: Geographic, temporal, domain coverage
5. **Data Content**: Detailed enumeration of available data categories
6. **Quality Assessment**: 6-dimension rating (1-5 scale)
7. **Licensing**: Usage terms and restrictions
8. **Catalog Metadata**: Added date, status, contributor

#### Quality Rating System (6 Dimensions)
1. **authority_level** (1-5): Source credibility and institutional authority
2. **methodology_transparency** (1-5): Clarity of data collection methods
3. **update_timeliness** (1-5): Frequency and reliability of updates
4. **data_completeness** (1-5): Coverage and missing data percentage
5. **documentation_quality** (1-5): User guides, API docs, data dictionaries
6. **citation_count** (1-5): Citation frequency and academic impact

### Testing Strategy

#### Validation Layers
1. **JSON Format Validation**
   - Valid JSON syntax
   - UTF-8 encoding check
   - Line ending consistency

2. **Schema Validation**
   - Required fields completeness (100%)
   - Field type correctness
   - Enum value validity
   - Using `jsonschema` library with Draft-07 schema

3. **Content Validation**
   - URL format verification (must start with http:// or https://)
   - Quality ratings within range (1-5)
   - Date format compliance (YYYY-MM-DD, ISO 8601)
   - Language codes (ISO 639-1)
   - Country codes (ISO 3166-1)

4. **Logic Validation**
   - Temporal consistency (start_year ≤ end_year ≤ current year)
   - Reference integrity (related_sources IDs exist)
   - Domain/region taxonomy consistency

5. **URL Accessibility Testing**
   - HTTP status code checking (200, 301/302, 404, 5xx)
   - Timeout handling (10 second limit)
   - Regular automated checks via GitHub Actions

#### Quality Thresholds
- **Required fields**: 100% completeness mandatory
- **Recommended fields**: ≥80% completeness expected
- **Overall completeness**: ≥70% for acceptance
- **URL validity**: 98%+ uptime expected

#### Continuous Integration
- GitHub Actions runs validation on every PR
- Automated checks include:
  - JSON syntax validation
  - Schema compliance
  - File naming conventions
  - Completeness scoring

### Git Workflow

#### Branching Strategy
- **Main branch**: `master` - Production-ready, stable codebase
- **Feature branches**: `feat/{description}` - New data sources or features
  - Example: `feat/add-world-bank-datasource`
  - Example: `feat/improve-validation-script`
- **Fix branches**: `fix/{description}` - Bug fixes or corrections
  - Example: `fix/update-broken-url-pbc`
- **Doc branches**: `docs/{description}` - Documentation improvements

#### Commit Conventions
- Use clear, descriptive commit messages
- Format: `<type>: <description>`
  - `feat`: New data source or feature
  - `fix`: Bug fix or correction
  - `docs`: Documentation changes
  - `refactor`: Code refactoring
  - `test`: Testing improvements
  - `chore`: Maintenance tasks

Examples:
```
feat: add World Bank data source
fix: update broken URL for People's Bank of China
docs: improve data collection guide
refactor: optimize validation script performance
```

#### Pull Request Process
1. **Fork** the repository
2. **Create branch** from `master`
3. **Make changes** following conventions
4. **Run validation** locally: `python scripts/validate.py {file}`
5. **Commit changes** with clear messages
6. **Push** to your fork
7. **Create PR** with:
   - Descriptive title
   - Summary of changes
   - Link to related issue (if applicable)
   - Validation results
8. **Address review** feedback
9. **Merge** after approval (squash and merge preferred)

#### Task Claiming Process
1. Browse [tasks/README.md](../tasks/README.md)
2. Select an unclaimed task (marked 📋 待开始)
3. Create an issue using claim-task template
4. Wait for maintainer approval (within 24 hours)
5. Complete within reasonable timeframe (2-4 weeks typical)
6. Submit PR referencing the claim issue

## Domain Context

### Data Source Categories
The project organizes data sources into several major categories:

1. **International Organizations** (100+ planned)
   - Economics: World Bank, IMF, OECD, WTO
   - Health: WHO, UNICEF, Global Burden of Disease
   - Environment: UNEP, IPCC, WMO
   - Social Development: UNDP, ILO, UNESCO
   - Statistics: UNdata, UN Population Division

2. **Countries** (200+ planned)
   - Focus on G20 nations and major economies
   - Emphasis on official statistical agencies, central banks, government ministries

3. **China Data Sources** (488 planned) - **Core Differentiator**
   - 16 national-level ministry domains (finance, economy, agriculture, health, etc.)
   - 34 provincial/municipal administrative regions
   - Research institutions and industry associations
   - Deepest coverage of Chinese official data globally

4. **Academic Research** (50+ planned)
   - Comprehensive repositories: ICPSR, Harvard Dataverse, Figshare
   - Domain-specific: NBER, Penn World Table, DHS
   - Research-grade datasets with peer review

5. **Sector-Specific** (150+ planned)
   - Energy, technology, education, agriculture, finance
   - Industry associations and professional organizations

### Data Source Quality Criteria

**Inclusion Standards** (Must meet ALL):
- ✅ Official or authoritative institutional source
- ✅ Publicly accessible (open or registration-based)
- ✅ Active maintenance and updates
- ✅ Clear licensing and usage terms
- ✅ Documented methodology or data dictionary

**Exclusion Criteria**:
- ❌ Personal blogs or non-official compilations
- ❌ Fully paid commercial data with no free tier
- ❌ Abandoned sources (>3 years without update)
- ❌ Broken or inaccessible websites
- ❌ Unverifiable or dubious data quality

### Metadata Standards

The project implements a comprehensive 40+ field metadata schema:
- **Bilingual support**: Chinese and English for all key fields
- **Structured taxonomy**: Standardized domain and region classifications
- **Access details**: API availability, authentication, download formats
- **Temporal coverage**: Historical range and update frequency
- **Quality metrics**: Transparent 6-dimension assessment
- **Usage information**: Licensing, citation format, use cases

## Important Constraints

### Technical Constraints
1. **Static Files Only**: Current implementation uses JSON files without a database
   - Scalability limit: Performance may degrade beyond ~5000 sources
   - Future migration to database may be needed for advanced search

2. **Manual Curation**: Data source discovery and metadata collection is manual
   - No automated web scraping or discovery
   - Quality over automation approach

3. **Validation Limits**: URL checking has inherent limitations
   - Some sites may block automated checks
   - Rate limiting may affect batch validation
   - VPN/regional access issues for China sources

4. **Python Dependency**: Validation tools require Python 3.8+
   - Contributors must have Python environment set up
   - Future consideration: Web-based validation tool

### Content Constraints
1. **Language Support**: Primary focus on Chinese and English
   - Other languages added opportunistically
   - Non-English/Chinese sources require translation effort

2. **Update Frequency**: Metadata updates lag actual data source changes
   - Quarterly review cycle for all sources
   - Community reports for broken links appreciated

3. **Scope Limitation**: Only metadata, not actual data
   - No data hosting or mirroring
   - No data cleaning or transformation services
   - Only provides pointers to authoritative sources

### Quality Constraints
1. **Subjectivity in Ratings**: Quality scores have inherent subjectivity
   - Mitigated by detailed rubrics and reviewer consensus
   - Scores may be debated and updated based on feedback

2. **Completeness Trade-offs**: Some fields may be impossible to fill
   - Older sources may lack API or modern documentation
   - Balance between completeness and coverage

## External Dependencies

### Data Source Providers
- **International Organizations**: UN agencies, World Bank, IMF, OECD, etc.
- **National Governments**: Statistical bureaus, central banks, ministries
- **Academic Institutions**: Universities, research centers, data repositories

### Critical Success Dependencies
1. **URL Stability**: Data sources must maintain stable URLs
   - Mitigation: Regular URL validation, community monitoring
   - Historical URL tracking for changes

2. **Open Access Policies**: Sources must remain publicly accessible
   - Risk: Policy changes making data restricted
   - Mitigation: Prioritize legally mandated open data

3. **Community Engagement**: Project success depends on contributor community
   - Need for domain experts to validate metadata
   - Maintainer availability for review and guidance

### Technical Dependencies
- **GitHub Infrastructure**: Repository hosting, Actions, Pages
- **Python Ecosystem**: jsonschema, requests libraries
- **JSON Schema Standard**: Draft-07 specification compliance

### No External API Dependencies
- Project is self-contained and can run offline
- No reliance on external validation services
- Only dependency is Python runtime and libraries
