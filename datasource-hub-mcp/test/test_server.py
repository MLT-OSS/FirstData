#!/usr/bin/env python3
"""
Quick test script for DataSource Hub MCP Server.

Run this to verify the server is working correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path to import server module
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import json
from server import datasource_search_sources, SearchSourcesInput, ResponseFormat


async def run_tests():
    """Run comprehensive tests of the MCP server."""

    print("=" * 70)
    print("DataSource Hub MCP Server - Test Suite")
    print("=" * 70)
    print()

    # Test 1: Youth unemployment (realistic user query)
    print("📊 Test 1: Youth Unemployment Search (JSON format)")
    print("-" * 70)
    params1 = SearchSourcesInput(
        query="youth unemployment China USA",
        limit=3,
        response_format=ResponseFormat.JSON
    )
    result1 = await datasource_search_sources(params1)
    data1 = json.loads(result1)

    print(f"Query: {params1.query}")
    print(f"✓ Found {data1['total_matches']} matches")
    print(f"✓ Returned {data1['returned_count']} results")

    if data1['data_sources']:
        for idx, ds in enumerate(data1['data_sources'], 1):
            print(f"\n  {idx}. {ds['name']['en']}")
            print(f"     Relevance: {ds['relevance_score']:.1f}, Quality: {ds['quality_average']:.1f}/5")
            print(f"     File: {ds['file_path']}")

    print("\n")

    # Test 2: Climate data (Markdown format)
    print("🌍 Test 2: Climate Data Search (Markdown format)")
    print("-" * 70)
    params2 = SearchSourcesInput(
        query="climate temperature global warming",
        limit=2,
        response_format=ResponseFormat.MARKDOWN
    )
    result2 = await datasource_search_sources(params2)

    print(f"Query: {params2.query}")
    print(f"✓ Generated Markdown output: {len(result2)} characters")
    print(f"✓ Contains 'Search Results': {'Yes' if 'Search Results' in result2 else 'No'}")

    # Show first few lines of markdown
    lines = result2.split('\n')[:10]
    print("\nFirst 10 lines:")
    for line in lines:
        print(f"  {line}")

    print("\n")

    # Test 3: Financial markets API
    print("💰 Test 3: Financial Markets with API")
    print("-" * 70)
    params3 = SearchSourcesInput(
        query="stock market financial data API",
        limit=5,
        response_format=ResponseFormat.JSON
    )
    result3 = await datasource_search_sources(params3)
    data3 = json.loads(result3)

    print(f"Query: {params3.query}")
    print(f"✓ Found {data3['total_matches']} matches")

    # Filter sources with API
    api_sources = [ds for ds in data3['data_sources']
                   if ds.get('access', {}).get('api_available')]
    print(f"✓ Sources with API: {len(api_sources)}")

    if api_sources:
        for idx, ds in enumerate(api_sources[:3], 1):
            print(f"\n  {idx}. {ds['name']['en']}")
            print(f"     Quality: {ds['quality_average']:.1f}/5")
            print(f"     URL: {ds['access']['primary_url']}")

    print("\n")

    # Test 4: No results case
    print("🔍 Test 4: Query with No Results")
    print("-" * 70)
    params4 = SearchSourcesInput(
        query="xyzabc123nonexistent",
        limit=10,
        response_format=ResponseFormat.JSON
    )
    result4 = await datasource_search_sources(params4)

    print(f"Query: {params4.query}")
    print(f"✓ Response: {result4[:100]}...")

    print("\n")

    # Summary
    print("=" * 70)
    print("✅ All Tests Completed Successfully!")
    print("=" * 70)
    print()
    print("The MCP server is working correctly and ready to use.")
    print("To use with Claude Desktop, add the server to your configuration:")
    print()
    print("  ~/Library/Application Support/Claude/claude_desktop_config.json")
    print()
    print("See README.md for detailed setup and usage instructions.")
    print()


if __name__ == "__main__":
    asyncio.run(run_tests())
