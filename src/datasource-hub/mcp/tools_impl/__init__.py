"""
Tools implementation package
"""

import sys
from pathlib import Path

_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

# Imports must come after sys.path modification
from .tool_filter_sources_by_criteria import tool_filter_sources_by_criteria  # noqa: E402
from .tool_get_instructions import tool_datasource_get_instructions  # noqa: E402
from .tool_get_source_details import tool_get_source_details  # noqa: E402
from .tool_list_sources_summary import tool_list_sources_summary  # noqa: E402
from .tool_search_sources_by_keywords import tool_search_sources_by_keywords  # noqa: E402

try:
    from .tool_search_agent import datasource_search_agent
except ImportError:
    datasource_search_agent = None

__all__ = [
    "tool_list_sources_summary",
    "tool_search_sources_by_keywords",
    "tool_get_source_details",
    "tool_filter_sources_by_criteria",
    "tool_datasource_get_instructions",
    "datasource_search_agent",
]
