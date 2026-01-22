"""
FirstData MCP Server配置
"""

from pathlib import Path

# Version (keep in sync with pyproject.toml)
__version__ = "0.1.0"

# 路径配置
_SCRIPT_DIR = Path(__file__).parent
if (_SCRIPT_DIR / "sources").exists():
    SOURCES_DIR = _SCRIPT_DIR / "sources"
    REPO_ROOT = _SCRIPT_DIR
else:
    REPO_ROOT = _SCRIPT_DIR.parent
    SOURCES_DIR = REPO_ROOT / "sources"
