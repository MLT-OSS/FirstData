"""
工具函数模块
"""

import json
import os
from pathlib import Path
from typing import Any

from anthropic import Anthropic
from config import REPO_ROOT, SOURCES_DIR


def load_all_datasources() -> list[dict[str, Any]]:
    """加载所有数据源"""
    datasources = []
    for root, _, files in os.walk(SOURCES_DIR):
        for file in files:
            if file.endswith(".json") and not file.startswith("."):
                file_path = Path(root) / file
                try:
                    with open(file_path, encoding="utf-8") as f:
                        data = json.load(f)
                        rel_path = file_path.relative_to(REPO_ROOT)
                        data["file_path"] = str(rel_path)
                        datasources.append(data)
                except (json.JSONDecodeError, Exception):
                    continue
    return datasources


def get_anthropic_client() -> Anthropic:
    """获取Anthropic客户端"""
    auth_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
    base_url = os.getenv("ANTHROPIC_BASE_URL")

    if not auth_token:
        raise ValueError("ANTHROPIC_AUTH_TOKEN not found in environment")

    if base_url:
        print(f"[INFO] Using custom Anthropic base URL: {base_url}")
        return Anthropic(api_key=auth_token, base_url=base_url)
    else:
        return Anthropic(api_key=auth_token)
