#!/usr/bin/env python3
"""
DataSource Hub RAG MCP Server - Semantic Search with Milvus & OpenAI

A Model Context Protocol (MCP) server that provides semantic search capabilities
for the DataSource Hub repository using RAG (Retrieval-Augmented Generation).

This server uses:
- Milvus for vector storage and similarity search
- OpenAI text-embedding-3-small for generating embeddings
- Cosine similarity for semantic matching

The server enables AI assistants to find data sources based on semantic similarity
rather than keyword matching, improving recall for related concepts and synonyms.
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from openai import OpenAI
from pymilvus import connections, Collection

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("datasource_hub_rag_mcp")

# Constants
REPO_ROOT = Path(__file__).parent.parent
EMBEDDING_DIM = 1536  # OpenAI text-embedding-3-small dimension
CHARACTER_LIMIT = 25000  # Maximum response size in characters
MILVUS_COLLECTION_NAME = os.getenv("MILVUS_COLLECTION_NAME", "datasource_hub")

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Global Milvus collection (loaded on startup)
milvus_collection: Optional[Collection] = None


# Enums
class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


# Pydantic Models for Input Validation
class SearchSourcesInput(BaseModel):
    """Input model for RAG-based data source search operations."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    query: str = Field(
        ...,
        description="Search query to find relevant data sources using semantic similarity (e.g., 'youth unemployment China USA', 'climate data', 'financial markets')",
        min_length=2,
        max_length=500
    )
    limit: Optional[int] = Field(
        default=5,
        description="Maximum number of results to return",
        ge=1,
        le=50
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )
    similarity_threshold: Optional[float] = Field(
        default=0.5,
        description="Minimum similarity score (0-1). Lower values return more results but may be less relevant",
        ge=0.0,
        le=1.0
    )

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace only")
        return v.strip()


# Shared utility functions
def _initialize_milvus():
    """Initialize connection to Milvus and load collection."""
    global milvus_collection

    if milvus_collection is not None:
        return  # Already initialized

    milvus_host = os.getenv("MILVUS_HOST", "localhost")
    milvus_port = os.getenv("MILVUS_PORT", "19530")
    milvus_user = os.getenv("MILVUS_USER", "")
    milvus_password = os.getenv("MILVUS_PASSWORD", "")

    try:
        connections.connect(
            alias="default",
            host=milvus_host,
            port=milvus_port,
            user=milvus_user,
            password=milvus_password
        )

        milvus_collection = Collection(MILVUS_COLLECTION_NAME)
        milvus_collection.load()

    except Exception as e:
        raise RuntimeError(
            f"Failed to connect to Milvus at {milvus_host}:{milvus_port}. "
            f"Error: {e}. Make sure Milvus is running and the collection is created."
        )


def _calculate_quality_score(datasource: Dict[str, Any]) -> float:
    """Calculate overall quality score from the 6 quality dimensions."""
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


def _format_datasource_markdown(datasource: Dict[str, Any], rank: int, similarity: float) -> str:
    """Format a single datasource as markdown."""
    lines = []

    # Header with rank and name
    name_en = datasource.get('name', {}).get('en', 'Unknown')
    name_zh = datasource.get('name', {}).get('zh', '')
    if name_zh and name_zh != name_en:
        lines.append(f"## {rank}. {name_en} ({name_zh})")
    else:
        lines.append(f"## {rank}. {name_en}")

    lines.append("")
    lines.append(f"**Similarity**: {similarity:.2%}")
    lines.append("")

    # Description
    desc_en = datasource.get('description', {}).get('en', '')
    if desc_en:
        if len(desc_en) > 300:
            desc_en = desc_en[:297] + "..."
        lines.append(desc_en)
        lines.append("")

    # Quality scores
    quality = datasource.get('quality', {})
    quality_avg = _calculate_quality_score(datasource)
    lines.append("### Quality Scores")
    lines.append(f"- **Authority Level**: {quality.get('authority_level', 'N/A')}/5 ⭐")
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
    lines.append("")

    # Coverage
    coverage = datasource.get('coverage', {})
    domains = coverage.get('domains', [])
    if domains:
        lines.append(f"**Domains**: {', '.join(domains[:5])}")
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
    """Format a datasource for JSON output (extract key fields)."""
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
            "domains": datasource.get('coverage', {}).get('domains'),
        },
        "quality": datasource.get('quality'),
        "quality_average": _calculate_quality_score(datasource),
        "file_path": datasource.get('file_path'),
        "tags": datasource.get('tags', [])
    }


# Tool definitions
@mcp.tool(
    name="datasource_rag_search",
    annotations={
        "title": "Search Data Sources with Semantic Similarity (RAG)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def datasource_rag_search(params: SearchSourcesInput) -> str:
    """
    Search for authoritative data sources using semantic similarity (RAG with Milvus + OpenAI).

    **USE THIS TOOL WHEN users ask about:**
    - Finding data sources (e.g., "where can I get data on...", "find datasets about...")
    - Locating statistics or datasets (e.g., "I need statistics on...", "search for data on...")
    - Discovering authoritative sources (e.g., "what are good sources for...", "official data on...")
    - Chinese queries: "寻找数据源", "哪里有...的数据", "查找...数据集", "搜索数据"

    **HOW IT WORKS:**
    This tool uses semantic search with vector embeddings to find relevant data sources.
    Unlike keyword matching, it understands concepts and synonyms:
    - "employment" matches "job market", "labor force", "unemployment rate"
    - "climate" matches "temperature", "weather", "global warming"
    - "GDP" matches "economic growth", "国内生产总值"

    **COMMON TRIGGER PHRASES:**
    - "Find data sources for [topic]"
    - "Where can I get data about [topic]"
    - "Search for datasets on [topic]"
    - "I need statistics/data on [topic]"
    - "寻找/查找 [主题] 数据源"

    This tool searches 100+ curated data sources from government agencies, international
    organizations, research institutions, and commercial providers using semantic similarity.

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
            - limit (int, optional): Max results to return (1-50, default: 5)
            - response_format (str, optional): "markdown" (default) or "json"
            - similarity_threshold (float, optional): Minimum similarity score 0-1 (default: 0.5)

    Returns:
        str: Ranked list of data sources with similarity scores, quality ratings, and access info

        **IMPORTANT OUTPUT INSTRUCTIONS:**
        - The tool returns a pre-formatted markdown or JSON response
        - You MUST output the ENTIRE returned content EXACTLY as-is
        - DO NOT summarize, reformat, or re-interpret the results
        - Simply present the complete output from this tool directly to the user

    Examples:
        **English queries:**
        - "Find youth unemployment data for China and USA" → query: "youth unemployment China USA"
        - "Where can I get climate change data?" → query: "climate change temperature"
        - "I need financial market data with API access" → query: "financial markets API"
        - "Search for population census data" → query: "population census demographics"

        **Chinese queries (中文查询):**
        - "寻找中美青年失业率数据源" → query: "youth unemployment China USA"
        - "哪里有气候变化的数据" → query: "climate change data"

    Error Handling:
        - Returns clear message if no matches found above similarity threshold
        - Suggests lowering similarity_threshold if needed
        - Provides connection error guidance if Milvus is unavailable
    """
    try:
        # Initialize Milvus connection if needed
        _initialize_milvus()

        if milvus_collection is None:
            return (
                "Error: Milvus collection not available. The vector index may not be built yet. "
                "Please run: python build_index.py"
            )

        # Generate embedding for query
        try:
            response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=params.query
            )
            query_vector = response.data[0].embedding
        except Exception as e:
            return f"Error: Failed to generate embedding: {str(e)}. Check OPENAI_API_KEY."

        # Search in Milvus
        search_params = {
            "metric_type": "COSINE",
            "params": {"nprobe": 10}
        }

        try:
            results = milvus_collection.search(
                data=[query_vector],
                anns_field="embedding",
                param=search_params,
                limit=params.limit * 2,  # Fetch more for filtering
                output_fields=["full_data", "quality_score", "name_en", "name_zh"]
            )
        except Exception as e:
            return f"Error: Milvus search failed: {str(e)}"

        # Filter by similarity threshold and prepare results
        filtered_results = []
        for hit in results[0]:
            similarity = hit.score  # Cosine similarity (0-1, higher is better)

            if similarity >= params.similarity_threshold:
                try:
                    datasource = json.loads(hit.entity.get('full_data'))
                    filtered_results.append({
                        'datasource': datasource,
                        'similarity': similarity,
                        'quality_score': hit.entity.get('quality_score', 0)
                    })
                except json.JSONDecodeError:
                    continue

        # Limit to requested number
        filtered_results = filtered_results[:params.limit]

        if not filtered_results:
            return (
                f"No data sources found matching '{params.query}' with similarity >= {params.similarity_threshold:.0%}. "
                f"Try lowering the similarity_threshold or use broader search terms."
            )

        # Format output based on requested format
        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [
                f"# Data Source Search Results (Semantic Search)",
                f"",
                f"**Query**: {params.query}",
                f"**Found**: {len(filtered_results)} relevant data sources",
                f"**Method**: RAG with vector embeddings (Milvus + OpenAI)",
                f"",
                f"---",
                f"",
            ]

            # Add results
            for idx, item in enumerate(filtered_results, 1):
                ds = item['datasource']
                similarity = item['similarity']
                lines.append(_format_datasource_markdown(ds, idx, similarity))

            result = "\n".join(lines)

            # Check character limit
            if len(result) > CHARACTER_LIMIT:
                reduced_count = max(1, len(filtered_results) // 2)
                lines = [
                    f"# Data Source Search Results (Semantic Search)",
                    f"",
                    f"**Query**: {params.query}",
                    f"**Found**: {len(filtered_results)} relevant data sources",
                    f"",
                    f"⚠️ **Note**: Results truncated to fit response limit. Showing top {reduced_count} results.",
                    f"",
                    f"---",
                    f"",
                ]

                for idx, item in enumerate(filtered_results[:reduced_count], 1):
                    ds = item['datasource']
                    similarity = item['similarity']
                    lines.append(_format_datasource_markdown(ds, idx, similarity))

                result = "\n".join(lines)

            return result

        else:  # JSON format
            json_results = {
                "query": params.query,
                "method": "RAG (Milvus + OpenAI text-embedding-3-small)",
                "returned_count": len(filtered_results),
                "similarity_threshold": params.similarity_threshold,
                "data_sources": [
                    {
                        **_format_datasource_json(item['datasource']),
                        "similarity_score": item['similarity'],
                    }
                    for item in filtered_results
                ]
            }

            return json.dumps(json_results, indent=2, ensure_ascii=False)

    except RuntimeError as e:
        return str(e)
    except Exception as e:
        return f"Error: An unexpected error occurred: {type(e).__name__} - {str(e)}"


if __name__ == "__main__":
    # Check required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it in .env file or export it")
        exit(1)

    # Initialize Milvus connection
    try:
        _initialize_milvus()
        print(f"✓ Connected to Milvus collection: {MILVUS_COLLECTION_NAME}")
    except RuntimeError as e:
        print(f"Warning: {e}")
        print("The server will start but searches will fail until Milvus is available.")

    # Run the MCP server
    mcp.run()
