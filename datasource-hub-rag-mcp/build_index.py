#!/usr/bin/env python3
"""
DataSource Hub RAG - Index Builder

This script builds the vector index for the DataSource Hub repository.
It loads all datasources, generates embeddings using OpenAI, and stores them in Milvus.

Usage:
    python build_index.py

Environment Variables:
    OPENAI_API_KEY - OpenAI API key for embeddings
    MILVUS_HOST - Milvus server host (default: localhost)
    MILVUS_PORT - Milvus server port (default: 19530)
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    utility
)

# Load environment variables
load_dotenv()

# Constants
REPO_ROOT = Path(__file__).parent.parent
SOURCES_DIR = REPO_ROOT / "sources"
EMBEDDING_DIM = 1536  # OpenAI text-embedding-3-small dimension
MILVUS_COLLECTION_NAME = os.getenv("MILVUS_COLLECTION_NAME", "datasource_hub")

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _load_all_datasources() -> List[Dict[str, Any]]:
    """Load all data source JSON files from the repository."""
    datasources = []

    if not SOURCES_DIR.exists():
        print(f"Error: Sources directory not found: {SOURCES_DIR}")
        sys.exit(1)

    for root, _, files in os.walk(SOURCES_DIR):
        for file in files:
            if file.endswith('.json') and not file.startswith('.'):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        rel_path = file_path.relative_to(REPO_ROOT)
                        data['file_path'] = str(rel_path)
                        datasources.append(data)
                except (json.JSONDecodeError, Exception) as e:
                    print(f"Warning: Failed to load {file_path}: {e}")
                    continue

    return datasources


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


def build_text_for_embedding(ds: Dict[str, Any]) -> str:
    """
    Build text representation for embedding.

    This combines multiple fields with strategic weighting:
    - Name appears multiple times (highest weight)
    - Description included once
    - Tags and domains included for categorization
    - Organization name for context
    """
    parts = []

    # Name (重复多次以增加权重)
    name_en = ds.get("name", {}).get("en", "")
    name_zh = ds.get("name", {}).get("zh", "")
    if name_en:
        parts.append(f"Name: {name_en}")
        parts.append(name_en)  # Repeat for emphasis
        parts.append(name_en)  # Repeat again
    if name_zh:
        parts.append(f"名称: {name_zh}")
        parts.append(name_zh)  # Repeat for emphasis

    # Description
    desc_en = ds.get("description", {}).get("en", "")
    desc_zh = ds.get("description", {}).get("zh", "")
    if desc_en:
        parts.append(f"Description: {desc_en}")
    if desc_zh:
        parts.append(f"描述: {desc_zh}")

    # Tags
    tags = ds.get("tags", [])
    if tags:
        parts.append(f"Tags: {', '.join(tags)}")

    # Domains
    domains = ds.get("coverage", {}).get("domains", [])
    if domains:
        parts.append(f"Domains: {', '.join(domains)}")

    # Data content
    data_content_en = ds.get("data_content", {}).get("en", [])
    data_content_zh = ds.get("data_content", {}).get("zh", [])
    if data_content_en:
        parts.append(f"Content: {', '.join(data_content_en[:5])}")  # Limit to 5
    if data_content_zh:
        parts.append(f"内容: {', '.join(data_content_zh[:5])}")

    # Organization
    org_name = ds.get("organization", {}).get("name", "")
    if org_name:
        parts.append(f"Organization: {org_name}")

    return "\n".join(parts)


def create_milvus_collection():
    """Create Milvus collection with schema."""
    # Define collection schema
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="datasource_id", dtype=DataType.VARCHAR, max_length=100),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
        FieldSchema(name="name_en", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="name_zh", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="description_en", dtype=DataType.VARCHAR, max_length=2000),
        FieldSchema(name="tags", dtype=DataType.VARCHAR, max_length=1000),
        FieldSchema(name="domains", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="quality_score", dtype=DataType.FLOAT),
        FieldSchema(name="file_path", dtype=DataType.VARCHAR, max_length=200),
        FieldSchema(name="full_data", dtype=DataType.VARCHAR, max_length=65535),  # JSON string
    ]

    schema = CollectionSchema(
        fields=fields,
        description="DataSource Hub vector search collection"
    )

    # Drop existing collection if it exists
    if utility.has_collection(MILVUS_COLLECTION_NAME):
        print(f"Dropping existing collection: {MILVUS_COLLECTION_NAME}")
        utility.drop_collection(MILVUS_COLLECTION_NAME)

    # Create collection
    print(f"Creating collection: {MILVUS_COLLECTION_NAME}")
    collection = Collection(
        name=MILVUS_COLLECTION_NAME,
        schema=schema
    )

    return collection


def build_index(collection: Collection):
    """Build IVF_FLAT index for vector search."""
    print("Building vector index...")

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "COSINE",  # Cosine similarity
        "params": {"nlist": 128}
    }

    collection.create_index(
        field_name="embedding",
        index_params=index_params
    )

    print("Index built successfully")


def main():
    """Main function to build the vector index."""
    print("="*70)
    print("DataSource Hub RAG - Index Builder")
    print("="*70)
    print()

    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it in .env file or export it")
        sys.exit(1)

    # Load datasources
    print("Loading datasources...")
    datasources = _load_all_datasources()
    print(f"✓ Loaded {len(datasources)} datasources")
    print()

    # Connect to Milvus
    milvus_host = os.getenv("MILVUS_HOST", "localhost")
    milvus_port = os.getenv("MILVUS_PORT", "19530")
    milvus_user = os.getenv("MILVUS_USER", "")
    milvus_password = os.getenv("MILVUS_PASSWORD", "")

    print(f"Connecting to Milvus at {milvus_host}:{milvus_port}...")

    try:
        connections.connect(
            alias="default",
            host=milvus_host,
            port=milvus_port,
            user=milvus_user,
            password=milvus_password
        )
        print("✓ Connected to Milvus")
    except Exception as e:
        print(f"Error connecting to Milvus: {e}")
        print("\nMake sure Milvus is running:")
        print("  Docker: docker run -d -p 19530:19530 milvusdb/milvus:latest")
        sys.exit(1)

    print()

    # Create collection
    collection = create_milvus_collection()
    print("✓ Collection created")
    print()

    # Generate embeddings and insert data
    print(f"Generating embeddings for {len(datasources)} datasources...")
    print("(This may take a few minutes)")
    print()

    batch_size = 10
    total_inserted = 0

    for i in range(0, len(datasources), batch_size):
        batch = datasources[i:i+batch_size]

        # Prepare data for this batch
        embeddings = []
        datasource_ids = []
        names_en = []
        names_zh = []
        descriptions_en = []
        tags_list = []
        domains_list = []
        quality_scores = []
        file_paths = []
        full_data_list = []

        for ds in batch:
            # Build text for embedding
            text = build_text_for_embedding(ds)

            # Generate embedding
            try:
                response = openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                embedding = response.data[0].embedding
            except Exception as e:
                print(f"Warning: Failed to generate embedding for {ds.get('id')}: {e}")
                continue

            # Prepare data
            embeddings.append(embedding)
            datasource_ids.append(ds.get('id', ''))
            names_en.append(ds.get('name', {}).get('en', ''))
            names_zh.append(ds.get('name', {}).get('zh', ''))
            descriptions_en.append(ds.get('description', {}).get('en', '')[:2000])  # Truncate
            tags_list.append(','.join(ds.get('tags', []))[:1000])
            domains_list.append(','.join(ds.get('coverage', {}).get('domains', []))[:500])
            quality_scores.append(_calculate_quality_score(ds))
            file_paths.append(ds.get('file_path', ''))
            full_data_list.append(json.dumps(ds, ensure_ascii=False)[:65535])  # Truncate

        # Insert batch
        if embeddings:
            entities = [
                datasource_ids,
                embeddings,
                names_en,
                names_zh,
                descriptions_en,
                tags_list,
                domains_list,
                quality_scores,
                file_paths,
                full_data_list
            ]

            collection.insert(entities)
            total_inserted += len(embeddings)
            print(f"  Progress: {total_inserted}/{len(datasources)} datasources inserted")

    print()
    print(f"✓ Inserted {total_inserted} datasources")
    print()

    # Build index
    build_index(collection)
    print()

    # Load collection for searching
    collection.load()
    print("✓ Collection loaded and ready for search")
    print()

    print("="*70)
    print("Index building completed successfully!")
    print("="*70)
    print()
    print("Next steps:")
    print("  1. Start the MCP server: python server_rag.py")
    print("  2. Configure Claude Desktop to use the RAG server")
    print()


if __name__ == "__main__":
    main()
