#!/usr/bin/env python3
"""
DataSource Hub - Search and discover authoritative data sources.

This MCP server helps you find high-quality data sources from 100+ curated sources
including government agencies, international organizations, research institutions,
and commercial providers across economics, health, climate, finance, and more domains.

Use this server when you need to find where to get data, not the data itself.
"""

import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("datasource_hub")

# Constants
REPO_ROOT = Path(__file__).parent.parent  # Go up to datasource-hub root
SOURCES_DIR = REPO_ROOT / "sources"
CHARACTER_LIMIT = 25000  # Maximum response size in characters

# Enums
class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


# Pydantic Models for Input Validation
class SearchSourcesInput(BaseModel):
    """Input model for data source search operations."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    query: str = Field(
        ...,
        description="Search query to find relevant data sources (e.g., 'youth unemployment China USA', 'climate data', 'financial markets')",
        min_length=2,
        max_length=500
    )
    limit: Optional[int] = Field(
        default=10,
        description="Maximum number of results to return",
        ge=1,
        le=50
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace only")
        return v.strip()


# Shared utility functions
def _load_all_datasources() -> List[Dict[str, Any]]:
    """
    Load all data source JSON files from the repository.

    Returns:
        List of datasource dictionaries with added 'file_path' field
    """
    datasources = []

    # Walk through all subdirectories in sources/
    for root, _, files in os.walk(SOURCES_DIR):
        for file in files:
            if file.endswith('.json') and not file.startswith('.'):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Add relative file path for reference
                        rel_path = file_path.relative_to(REPO_ROOT)
                        data['file_path'] = str(rel_path)
                        datasources.append(data)
                except (json.JSONDecodeError, Exception):
                    # Skip files that can't be parsed
                    continue

    return datasources


def _calculate_relevance_score(datasource: Dict[str, Any], query: str) -> float:
    """
    Calculate relevance score for a datasource given a search query.

    Higher scores indicate better matches. Scoring criteria:
    - Exact match in name: +10 points
    - Partial match in name: +5 points
    - Match in description: +3 points
    - Match in tags: +2 points per tag
    - Match in domains: +2 points per domain
    - Match in data_content: +1 point per match

    Args:
        datasource: The datasource dictionary
        query: The search query string

    Returns:
        Relevance score (float)
    """
    score = 0.0
    query_lower = query.lower()
    query_terms = set(query_lower.split())

    # Helper function to check if any query term matches text
    def contains_term(text) -> bool:
        if not text or not isinstance(text, str):
            return False
        text_lower = text.lower()
        return any(term in text_lower for term in query_terms) or query_lower in text_lower

    # Check name (highest priority)
    name = datasource.get('name', {})
    name_en = name.get('en', '')
    name_zh = name.get('zh', '')

    if query_lower in name_en.lower() or query_lower in name_zh.lower():
        score += 10  # Exact match
    elif contains_term(name_en) or contains_term(name_zh):
        score += 5  # Partial match

    # Check description
    description = datasource.get('description', {})
    desc_en = description.get('en', '')
    desc_zh = description.get('zh', '')

    if contains_term(desc_en) or contains_term(desc_zh):
        score += 3

    # Check tags
    tags = datasource.get('tags', [])
    for tag in tags:
        if contains_term(tag):
            score += 2

    # Check domains
    domains = datasource.get('coverage', {}).get('domains', [])
    for domain in domains:
        if contains_term(domain):
            score += 2

    # Check data_content
    data_content = datasource.get('data_content', {})
    content_en = data_content.get('en', [])
    content_zh = data_content.get('zh', [])

    for content in content_en + content_zh:
        if contains_term(content):
            score += 1

    # Check organization name
    org_name = datasource.get('organization', {}).get('name', '')
    if contains_term(org_name):
        score += 2

    return score


def _calculate_quality_score(datasource: Dict[str, Any]) -> float:
    """
    Calculate overall quality score from the 6 quality dimensions.

    Args:
        datasource: The datasource dictionary

    Returns:
        Average quality score (1-5)
    """
    quality = datasource.get('quality', {})
    dimensions = [
        quality.get('authority_level', 0),
        quality.get('methodology_transparency', 0),
        quality.get('update_timeliness', 0),
        quality.get('data_completeness', 0),
        quality.get('documentation_quality', 0),
        quality.get('citation_count', 0)
    ]

    valid_scores = [s for s in dimensions if s > 0]
    if not valid_scores:
        return 0.0

    return sum(valid_scores) / len(valid_scores)


def _format_datasource_markdown(datasource: Dict[str, Any], rank: int) -> str:
    """
    Format a single datasource as markdown.

    Args:
        datasource: The datasource dictionary
        rank: The ranking number for display

    Returns:
        Formatted markdown string
    """
    lines = []

    # Header with rank and name
    name_en = datasource.get('name', {}).get('en', 'Unknown')
    name_zh = datasource.get('name', {}).get('zh', '')
    if name_zh and name_zh != name_en:
        lines.append(f"## {rank}. {name_en} ({name_zh})")
    else:
        lines.append(f"## {rank}. {name_en}")

    lines.append("")

    # Description
    desc_en = datasource.get('description', {}).get('en', '')
    if desc_en:
        # Truncate long descriptions
        if len(desc_en) > 300:
            desc_en = desc_en[:297] + "..."
        lines.append(desc_en)
        lines.append("")

    # Quality scores
    quality = datasource.get('quality', {})
    lines.append("### Quality Scores")
    lines.append(f"- **Authority Level**: {quality.get('authority_level', 'N/A')}/5 ⭐")
    lines.append(f"- **Methodology Transparency**: {quality.get('methodology_transparency', 'N/A')}/5 ⭐")
    lines.append(f"- **Update Timeliness**: {quality.get('update_timeliness', 'N/A')}/5 ⭐")
    lines.append(f"- **Data Completeness**: {quality.get('data_completeness', 'N/A')}/5 ⭐")
    lines.append(f"- **Documentation Quality**: {quality.get('documentation_quality', 'N/A')}/5 ⭐")
    lines.append(f"- **Citation Count**: {quality.get('citation_count', 'N/A')}/5 ⭐")
    quality_avg = _calculate_quality_score(datasource)
    lines.append(f"- **Average Score**: {quality_avg:.1f}/5 ⭐")
    lines.append("")

    # Access information
    access = datasource.get('access', {})
    lines.append("### Access")
    lines.append(f"- **Primary URL**: {access.get('primary_url', 'N/A')}")
    lines.append(f"- **Access Level**: {access.get('access_level', 'N/A')}")

    api = access.get('api', {})
    if api.get('available'):
        lines.append(f"- **API Available**: Yes")
        if api.get('documentation'):
            lines.append(f"  - Documentation: {api['documentation']}")
    lines.append("")

    # Coverage
    coverage = datasource.get('coverage', {})
    geographic = coverage.get('geographic', {})
    temporal = coverage.get('temporal', {})

    lines.append("### Coverage")
    lines.append(f"- **Geographic Scope**: {geographic.get('scope', 'N/A')}")

    if temporal.get('start_year') or temporal.get('end_year'):
        start = temporal.get('start_year', 'N/A')
        end = temporal.get('end_year', 'N/A')
        lines.append(f"- **Time Period**: {start} - {end}")

    if temporal.get('update_frequency'):
        lines.append(f"- **Update Frequency**: {temporal['update_frequency']}")

    domains = coverage.get('domains', [])
    if domains:
        lines.append(f"- **Domains**: {', '.join(domains[:5])}")

    lines.append("")

    # JSON file reference
    file_path = datasource.get('file_path', '')
    if file_path:
        lines.append(f"### JSON File")
        lines.append(f"`{file_path}`")
        lines.append("")

    # Tags
    tags = datasource.get('tags', [])
    if tags:
        lines.append(f"**Tags**: {', '.join(tags[:10])}")
        lines.append("")

    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def _format_datasource_json(datasource: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a datasource for JSON output (extract key fields).

    Args:
        datasource: The full datasource dictionary

    Returns:
        Simplified datasource dictionary with key fields
    """
    return {
        "id": datasource.get('id'),
        "name": datasource.get('name'),
        "description": datasource.get('description'),
        "organization": datasource.get('organization'),
        "access": {
            "primary_url": datasource.get('access', {}).get('primary_url'),
            "access_level": datasource.get('access', {}).get('access_level'),
            "api_available": datasource.get('access', {}).get('api', {}).get('available'),
        },
        "coverage": {
            "geographic_scope": datasource.get('coverage', {}).get('geographic', {}).get('scope'),
            "temporal": datasource.get('coverage', {}).get('temporal'),
            "domains": datasource.get('coverage', {}).get('domains'),
        },
        "quality": datasource.get('quality'),
        "quality_average": _calculate_quality_score(datasource),
        "file_path": datasource.get('file_path'),
        "tags": datasource.get('tags', [])
    }


# Tool definitions
@mcp.tool(
    name="datasource_search_sources",
    annotations={
        "title": "Search for Authoritative Data Sources",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def datasource_search_sources(params: SearchSourcesInput) -> str:
    """
    Search for authoritative data sources by topic, domain, country, or data type.

    **USE THIS TOOL WHEN users ask about:**
    - Finding data sources (e.g., "where can I get data on...", "find datasets about...")
    - Locating statistics or datasets (e.g., "I need statistics on...", "search for data on...")
    - Discovering authoritative sources (e.g., "what are good sources for...", "official data on...")
    - Chinese queries: "寻找数据源", "哪里有...的数据", "查找...数据集", "搜索数据"

    **COMMON TRIGGER PHRASES:**
    - "Find data sources for [topic]"
    - "Where can I get data about [topic]"
    - "Search for datasets on [topic]"
    - "I need statistics/data on [topic]"
    - "寻找/查找 [主题] 数据源"
    - "哪里有 [主题] 的数据"

    This tool searches 100+ curated data sources from government agencies, international
    organizations, research institutions, and commercial providers. It matches queries against
    data source names, descriptions, tags, domains, and content categories.

    **Search Coverage:**
    - Domains: Economics, Health, Climate, Finance, Education, Energy, Demographics, Trade, etc.
    - Geographies: China, USA, Global, Regional (EU, Asia, Africa, etc.)
    - Types: Official statistics, Research data, Market data, Environmental data, Social surveys

    **Quality Assessment (6 dimensions, 1-5 stars):**
    - Authority Level, Methodology Transparency, Update Timeliness
    - Data Completeness, Documentation Quality, Citation Count

    Args:
        params (SearchSourcesInput): Search parameters
            - query (str, required): Topic, domain, country, or keywords (2-500 characters)
            - limit (int, optional): Max results to return (1-50, default: 10)
            - response_format (str, optional): "markdown" (default, human-readable) or "json" (machine-readable)

    Returns:
        str: Ranked list of data sources with quality ratings, access info, and coverage details

    Examples:
        **English queries:**
        - "Find youth unemployment data for China and USA" → query: "youth unemployment China USA"
        - "Where can I get climate change data?" → query: "climate change temperature"
        - "I need financial market data with API access" → query: "financial markets API"
        - "Search for population census data" → query: "population census demographics"
        - "Official statistics from US government" → query: "USA government statistics"

        **Chinese queries (中文查询):**
        - "寻找中美青年失业率数据源" → query: "youth unemployment China USA"
        - "哪里有气候变化的数据" → query: "climate change data"
        - "查找金融市场数据" → query: "financial market data"
        - "搜索人口统计数据" → query: "population demographics"
        - "中国官方经济数据在哪里" → query: "China official economic data"

        **DO NOT use when:**
        - User wants actual data values (this tool finds DATA SOURCES, not data itself)
        - User wants to modify or add data sources (read-only tool)
        - User asks general questions not related to finding data sources

    Error Handling:
        - Returns clear message if no matches found - suggest broader search terms
        - Validates query length (2-500 characters) and provides helpful error messages
        - Auto-truncates large result sets to prevent overwhelming responses
    """
    try:
        # Load all data sources
        all_datasources = _load_all_datasources()

        if not all_datasources:
            return "Error: No data sources found in the repository. Please check the sources directory."

        # Calculate relevance scores for all datasources
        scored_datasources = []
        for ds in all_datasources:
            relevance = _calculate_relevance_score(ds, params.query)
            if relevance > 0:  # Only include sources with some relevance
                quality_avg = _calculate_quality_score(ds)
                scored_datasources.append({
                    'datasource': ds,
                    'relevance_score': relevance,
                    'quality_score': quality_avg
                })

        if not scored_datasources:
            return f"No data sources found matching '{params.query}'. Try broader search terms or different keywords."

        # Sort by relevance score (primary) and quality score (secondary)
        scored_datasources.sort(
            key=lambda x: (x['relevance_score'], x['quality_score']),
            reverse=True
        )

        # Limit results
        top_results = scored_datasources[:params.limit]

        # Format output based on requested format
        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [
                f"# Data Source Search Results",
                f"",
                f"**Query**: {params.query}",
                f"**Found**: {len(scored_datasources)} relevant data sources (showing top {len(top_results)})",
                f"",
                f"---",
                f"",
                f"## 📊 Summary Table",
                f"",
            ]

            # Add summary table
            table_header = "| # | Name | Quality | URL | Access | API | File Path |"
            table_sep = "|---|------|---------|-----|--------|-----|-----------|"
            lines.append(table_header)
            lines.append(table_sep)

            for idx, item in enumerate(top_results, 1):
                ds = item['datasource']
                name_en = ds.get('name', {}).get('en', 'Unknown')
                name_zh = ds.get('name', {}).get('zh', '')

                # Truncate long names
                if len(name_en) > 40:
                    name_en = name_en[:37] + "..."

                # Add Chinese name in parentheses if different
                if name_zh and name_zh != name_en:
                    if len(name_zh) > 20:
                        name_zh = name_zh[:17] + "..."
                    display_name = f"{name_en} ({name_zh})"
                else:
                    display_name = name_en

                # Truncate if still too long
                if len(display_name) > 50:
                    display_name = display_name[:47] + "..."

                quality_score = item['quality_score']
                quality_str = f"{quality_score:.1f}/5 ⭐"

                # Get URL
                url = ds.get('access', {}).get('primary_url', 'N/A')
                # Make URL clickable
                if url != 'N/A':
                    url_str = f"[Link]({url})"
                else:
                    url_str = "N/A"

                access_level = ds.get('access', {}).get('access_level', 'N/A')

                api_available = ds.get('access', {}).get('api', {}).get('available', False)
                api_str = "✅" if api_available else "❌"

                file_path = ds.get('file_path', 'N/A')
                # Make file path a code snippet
                file_link = f"`{file_path}`"

                table_row = f"| {idx} | {display_name} | {quality_str} | {url_str} | {access_level} | {api_str} | {file_link} |"
                lines.append(table_row)

            lines.append("")
            lines.append("---")
            lines.append("")

            # Optional: Uncomment below to add detailed information
            # lines.append("## 📝 Detailed Information")
            # lines.append("")
            # for idx, item in enumerate(top_results, 1):
            #     ds = item['datasource']
            #     lines.append(_format_datasource_markdown(ds, idx))

            result = "\n".join(lines)

            # Check character limit
            if len(result) > CHARACTER_LIMIT:
                # Reduce number of results
                reduced_count = max(1, len(top_results) // 2)
                lines = [
                    f"# Data Source Search Results",
                    f"",
                    f"**Query**: {params.query}",
                    f"**Found**: {len(scored_datasources)} relevant data sources",
                    f"",
                    f"⚠️ **Note**: Results truncated to fit response limit. Showing top {reduced_count} of {len(top_results)} results.",
                    f"Use a more specific query to get better targeted results.",
                    f"",
                    f"---",
                    f"",
                    f"## 📊 Summary Table",
                    f"",
                ]

                # Add summary table for reduced results
                table_header = "| # | Name | Quality | URL | Access | API | File Path |"
                table_sep = "|---|------|---------|-----|--------|-----|-----------|"
                lines.append(table_header)
                lines.append(table_sep)

                for idx, item in enumerate(top_results[:reduced_count], 1):
                    ds = item['datasource']
                    name_en = ds.get('name', {}).get('en', 'Unknown')
                    name_zh = ds.get('name', {}).get('zh', '')

                    if len(name_en) > 40:
                        name_en = name_en[:37] + "..."

                    if name_zh and name_zh != name_en:
                        if len(name_zh) > 20:
                            name_zh = name_zh[:17] + "..."
                        display_name = f"{name_en} ({name_zh})"
                    else:
                        display_name = name_en

                    if len(display_name) > 50:
                        display_name = display_name[:47] + "..."

                    quality_score = item['quality_score']
                    quality_str = f"{quality_score:.1f}/5 ⭐"

                    url = ds.get('access', {}).get('primary_url', 'N/A')
                    if url != 'N/A':
                        url_str = f"[Link]({url})"
                    else:
                        url_str = "N/A"

                    access_level = ds.get('access', {}).get('access_level', 'N/A')

                    api_available = ds.get('access', {}).get('api', {}).get('available', False)
                    api_str = "✅" if api_available else "❌"

                    file_path = ds.get('file_path', 'N/A')
                    file_link = f"`{file_path}`"

                    table_row = f"| {idx} | {display_name} | {quality_str} | {url_str} | {access_level} | {api_str} | {file_link} |"
                    lines.append(table_row)

                lines.append("")
                lines.append("---")
                lines.append("")

                # Optional: Uncomment below to add detailed information
                # lines.append("## 📝 Detailed Information")
                # lines.append("")
                # for idx, item in enumerate(top_results[:reduced_count], 1):
                #     ds = item['datasource']
                #     lines.append(_format_datasource_markdown(ds, idx))

                result = "\n".join(lines)

            return result

        else:  # JSON format
            json_results = {
                "query": params.query,
                "total_matches": len(scored_datasources),
                "returned_count": len(top_results),
                "data_sources": [
                    {
                        **_format_datasource_json(item['datasource']),
                        "relevance_score": item['relevance_score'],
                    }
                    for item in top_results
                ]
            }

            return json.dumps(json_results, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error: An unexpected error occurred while searching data sources: {type(e).__name__} - {str(e)}"


if __name__ == "__main__":
    mcp.run()
