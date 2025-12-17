#!/usr/bin/env python3
"""
Test script to verify Milvus connection and collection status.

Usage:
    python test_connection.py
"""

import os
from dotenv import load_dotenv
from pymilvus import connections, utility, Collection

load_dotenv()


def test_connection():
    """Test connection to Milvus and check collection status."""
    print("="*70)
    print("DataSource Hub RAG - Connection Test")
    print("="*70)
    print()

    # Configuration
    milvus_host = os.getenv("MILVUS_HOST", "localhost")
    milvus_port = os.getenv("MILVUS_PORT", "19530")
    milvus_user = os.getenv("MILVUS_USER", "")
    milvus_password = os.getenv("MILVUS_PASSWORD", "")
    collection_name = os.getenv("MILVUS_COLLECTION_NAME", "datasource_hub")

    print(f"Milvus Host: {milvus_host}")
    print(f"Milvus Port: {milvus_port}")
    print(f"Collection: {collection_name}")
    print()

    # Test connection
    print("Testing connection...")
    try:
        connections.connect(
            alias="default",
            host=milvus_host,
            port=milvus_port,
            user=milvus_user,
            password=milvus_password,
            timeout=5
        )
        print("✓ Connected to Milvus successfully")
    except Exception as e:
        print(f"✗ Failed to connect to Milvus: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Check if Milvus is running:")
        print("     docker ps | grep milvus")
        print("  2. If not running, start Milvus:")
        print("     docker-compose up -d")
        print("  3. Test Milvus health:")
        print("     curl http://localhost:9091/healthz")
        return False

    print()

    # Check if collection exists
    print(f"Checking collection '{collection_name}'...")
    if not utility.has_collection(collection_name):
        print(f"✗ Collection '{collection_name}' does not exist")
        print()
        print("Next steps:")
        print("  1. Build the index:")
        print("     python build_index.py")
        return False

    print(f"✓ Collection '{collection_name}' exists")
    print()

    # Get collection info
    collection = Collection(collection_name)

    # Get number of entities
    print("Collection Statistics:")
    collection.load()
    num_entities = collection.num_entities
    print(f"  - Total data sources: {num_entities}")

    # Get schema
    schema = collection.schema
    print(f"  - Vector dimension: {EMBEDDING_DIM}")
    print(f"  - Fields: {len(schema.fields)}")

    # Check if collection is loaded
    load_state = utility.load_state(collection_name)
    print(f"  - Load state: {load_state}")

    print()
    print("="*70)
    print("✅ All checks passed! The RAG MCP server is ready to use.")
    print("="*70)
    print()
    print("Next steps:")
    print("  1. Start the MCP server: python server_rag.py")
    print("  2. Configure Claude Desktop with the server path")
    print()

    return True


if __name__ == "__main__":
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set in environment")
        print("The server will not be able to generate embeddings for queries.")
        print()

    EMBEDDING_DIM = 1536
    test_connection()
