#!/usr/bin/env python3
"""
纯LLM驱动的数据源搜索Agent
使用Explore Subagent的设计思想：LLM自主决策使用工具，逐步缩小搜索范围
"""

# Version (keep in sync with pyproject.toml)
__version__ = "0.1.0"

import os
import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request

# 加载环境变量
load_dotenv()

# 配置
_SCRIPT_DIR = Path(__file__).parent
if (_SCRIPT_DIR / "sources").exists():
    SOURCES_DIR = _SCRIPT_DIR / "sources"
    REPO_ROOT = _SCRIPT_DIR
else:
    REPO_ROOT = _SCRIPT_DIR.parent
    SOURCES_DIR = REPO_ROOT / "sources"


# ============================================================================
# 数据源加载
# ============================================================================

def _load_all_datasources() -> List[Dict[str, Any]]:
    """加载所有数据源"""
    datasources = []
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
                except (json.JSONDecodeError, Exception):
                    continue
    return datasources


# ============================================================================
# Agent工具定义
# ============================================================================

AGENT_TOOLS = [
    {
        "name": "list_sources_summary",
        "description": """
        列出所有数据源的概要信息（ID、名称、国家、领域）。
        用于快速浏览可用数据源，了解整体情况。

        参数:
        - country: 可选，按国家代码过滤（如 "CN", "US", "Global"）
        - domain: 可选，按领域过滤（如 "finance", "health", "economics"）
        - limit: 可选，返回数量限制（默认50）

        返回: 数据源列表，每个包含 id, name, country, domains
        """,
        "input_schema": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "国家代码或名称，如 CN, US, Global"
                },
                "domain": {
                    "type": "string",
                    "description": "领域，如 finance, health, economics"
                },
                "limit": {
                    "type": "integer",
                    "description": "返回数量限制",
                    "default": 50
                }
            }
        }
    },
    {
        "name": "search_sources_by_keywords",
        "description": """
        在数据源的名称、描述、标签、内容中搜索关键词。
        用于根据用户查询的关键概念快速找到相关数据源。

        参数:
        - keywords: 必需，搜索关键词列表
        - search_fields: 可选，搜索范围 ["name", "description", "tags", "content"]，默认全部
        - limit: 可选，返回数量限制（默认20）

        返回: 匹配的数据源列表，包含 id, name, matched_fields（哪些字段匹配了）
        """,
        "input_schema": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "搜索关键词列表"
                },
                "search_fields": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["name", "description", "tags", "content", "all"]
                    },
                    "description": "搜索范围",
                    "default": ["all"]
                },
                "limit": {
                    "type": "integer",
                    "description": "返回数量限制",
                    "default": 20
                }
            },
            "required": ["keywords"]
        }
    },
    {
        "name": "get_source_details",
        "description": """
        获取指定数据源的完整详细信息。
        用于深入了解候选数据源的具体内容、覆盖范围、质量评分等。

        参数:
        - source_ids: 必需，数据源ID列表（如 ["china-pbc", "china-nbs"]）
        - fields: 可选，返回哪些字段，默认返回全部

        返回: 数据源的完整信息，包括描述、访问方式、覆盖范围、数据内容、质量评分等
        """,
        "input_schema": {
            "type": "object",
            "properties": {
                "source_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "数据源ID列表"
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "返回字段，如 ['description', 'coverage', 'quality']",
                    "default": ["all"]
                }
            },
            "required": ["source_ids"]
        }
    },
    {
        "name": "filter_sources_by_criteria",
        "description": """
        按多个条件组合筛选数据源。
        用于精确缩小搜索范围，支持地理、时间、访问方式等多维度筛选。

        参数:
        - geographic_scope: 可选，地理范围（如 "China", "Global", "Asia"）
        - has_api: 可选，是否需要API访问
        - update_frequency: 可选，更新频率（如 "monthly", "daily"）
        - min_quality_score: 可选，最低质量评分（0-5）
        - time_range: 可选，时间范围 {"start_year": 2000, "end_year": 2024}

        返回: 符合条件的数据源列表
        """,
        "input_schema": {
            "type": "object",
            "properties": {
                "geographic_scope": {
                    "type": "string",
                    "description": "地理范围"
                },
                "has_api": {
                    "type": "boolean",
                    "description": "是否需要API"
                },
                "update_frequency": {
                    "type": "string",
                    "description": "更新频率"
                },
                "min_quality_score": {
                    "type": "number",
                    "description": "最低质量评分（0-5）"
                },
                "time_range": {
                    "type": "object",
                    "properties": {
                        "start_year": {"type": "integer"},
                        "end_year": {"type": "integer"}
                    },
                    "description": "时间范围"
                }
            }
        }
    }
]


# ============================================================================
# 工具实现
# ============================================================================

def tool_list_sources_summary(country: Optional[str] = None,
                              domain: Optional[str] = None,
                              limit: int = 50) -> List[Dict]:
    """列出数据源概要"""
    all_sources = _load_all_datasources()
    results = []

    for ds in all_sources:
        # 过滤国家
        if country:
            org_country = ds.get('organization', {}).get('country') or ''
            geo_regions = ds.get('coverage', {}).get('geographic', {}).get('regions', [])
            geo_scope = ds.get('coverage', {}).get('geographic', {}).get('scope', '')

            country_match = (
                (org_country and country.upper() in org_country.upper()) or
                any(country.lower() in str(r).lower() for r in geo_regions) or
                (country.lower() == 'global' and 'global' in geo_scope.lower())
            )
            if not country_match:
                continue

        # 过滤领域
        if domain:
            domains = ds.get('coverage', {}).get('domains', [])
            if not any(domain.lower() in d.lower() for d in domains):
                continue

        # 计算质量评分，只使用数字类型的值
        quality = ds.get('quality', {})
        numeric_values = [v for v in quality.values() if isinstance(v, (int, float))]
        quality_score = sum(numeric_values) / len(numeric_values) if numeric_values else 0

        results.append({
            'id': ds['id'],
            'name': ds['name'],
            'country': ds.get('organization', {}).get('country', ''),
            'domains': ds.get('coverage', {}).get('domains', []),
            'quality_score': quality_score
        })

        if len(results) >= limit:
            break

    return results


def tool_search_sources_by_keywords(keywords: List[str],
                                     search_fields: List[str] = ["all"],
                                     limit: int = 20) -> List[Dict]:
    """关键词搜索"""
    all_sources = _load_all_datasources()
    results = []

    for ds in all_sources:
        matched_fields = []
        score = 0

        for keyword in keywords:
            kw_lower = keyword.lower()

            # 搜索名称
            if "name" in search_fields or "all" in search_fields:
                name_en = ds.get('name', {}).get('en', '').lower()
                name_zh = ds.get('name', {}).get('zh', '').lower()
                if kw_lower in name_en or kw_lower in name_zh:
                    matched_fields.append('name')
                    score += 10

            # 搜索描述
            if "description" in search_fields or "all" in search_fields:
                desc_en = ds.get('description', {}).get('en', '').lower()
                desc_zh = ds.get('description', {}).get('zh', '').lower()
                if kw_lower in desc_en or kw_lower in desc_zh:
                    if 'description' not in matched_fields:
                        matched_fields.append('description')
                    score += 5

            # 搜索标签
            if "tags" in search_fields or "all" in search_fields:
                tags = ds.get('tags', [])
                if any(kw_lower in str(tag).lower() for tag in tags):
                    if 'tags' not in matched_fields:
                        matched_fields.append('tags')
                    score += 3

            # 搜索内容
            if "content" in search_fields or "all" in search_fields:
                content_en = ds.get('data_content', {}).get('en', [])
                content_zh = ds.get('data_content', {}).get('zh', [])
                all_content = ' '.join(content_en + content_zh).lower()
                if kw_lower in all_content:
                    if 'content' not in matched_fields:
                        matched_fields.append('content')
                    score += 2

        if matched_fields:
            results.append({
                'id': ds['id'],
                'name': ds['name'],
                'matched_fields': list(set(matched_fields)),
                'match_score': score,
                'domains': ds.get('coverage', {}).get('domains', [])
            })

    # 按得分排序
    results.sort(key=lambda x: x['match_score'], reverse=True)
    return results[:limit]


def tool_get_source_details(source_ids: List[str],
                            fields: List[str] = ["all"]) -> List[Dict]:
    """获取详细信息"""
    all_sources = _load_all_datasources()
    results = []

    for source_id in source_ids:
        ds = next((s for s in all_sources if s['id'] == source_id), None)
        if not ds:
            results.append({'id': source_id, 'error': 'Not found'})
            continue

        if "all" in fields:
            results.append(ds)
        else:
            filtered = {'id': ds['id'], 'name': ds['name']}
            for field in fields:
                if field in ds:
                    filtered[field] = ds[field]
            results.append(filtered)

    return results


def tool_filter_sources_by_criteria(geographic_scope: Optional[str] = None,
                                     has_api: Optional[bool] = None,
                                     update_frequency: Optional[str] = None,
                                     min_quality_score: Optional[float] = None,
                                     time_range: Optional[Dict] = None) -> List[Dict]:
    """条件筛选"""
    all_sources = _load_all_datasources()
    results = []

    for ds in all_sources:
        # 地理范围
        if geographic_scope:
            org_country = ds.get('organization', {}).get('country') or ''
            geo_regions = ds.get('coverage', {}).get('geographic', {}).get('regions', []) or []
            geo_scope = ds.get('coverage', {}).get('geographic', {}).get('scope', '') or ''

            geo_match = (
                (org_country and geographic_scope.upper() in org_country.upper()) or
                any(geographic_scope.lower() in str(r).lower() for r in geo_regions) or
                geographic_scope.lower() in geo_scope.lower()
            )
            if not geo_match:
                continue

        # API需求
        if has_api is not None:
            has_api_access = ds.get('access', {}).get('api', {}).get('available', False)
            if has_api_access != has_api:
                continue

        # 更新频率
        if update_frequency:
            freq = ds.get('coverage', {}).get('temporal', {}).get('update_frequency', '')
            if update_frequency.lower() not in freq.lower():
                continue

        # 质量评分 - 只使用数字类型的值
        if min_quality_score is not None:
            quality = ds.get('quality', {})
            if quality:
                numeric_values = [v for v in quality.values() if isinstance(v, (int, float))]
                if numeric_values:
                    avg_score = sum(numeric_values) / len(numeric_values)
                    if avg_score < min_quality_score:
                        continue
                else:
                    # 没有数字质量值，跳过此数据源
                    continue

        # 时间范围
        if time_range:
            temporal = ds.get('coverage', {}).get('temporal', {})
            start_year = temporal.get('start_year', 0)
            end_year = temporal.get('end_year', 9999)

            if time_range.get('start_year') and start_year > time_range['start_year']:
                continue
            if time_range.get('end_year') and end_year < time_range['end_year']:
                continue

        results.append({
            'id': ds['id'],
            'name': ds['name'],
            'country': ds.get('organization', {}).get('country', ''),
            'domains': ds.get('coverage', {}).get('domains', []),
            'has_api': ds.get('access', {}).get('api', {}).get('available', False),
            'quality': ds.get('quality', {})
        })

    return results


# ============================================================================
# Agent System Prompt
# ============================================================================

AGENT_SYSTEM_PROMPT = """你是DataSource Hub的数据源搜索专家。你擅长通过逐步探索和分析，帮助用户找到最合适的权威数据源。

=== 核心原则 ===

你是一个**只读搜索Agent**，专注于：
- 理解用户的数据需求
- 自主决策使用哪些工具
- 逐步缩小搜索范围
- 深入分析候选数据源
- 给出精准推荐和详细理由

你**不能**：
- 修改任何数据源文件
- 创建新的数据源
- 删除或移动文件

=== 工作流程建议 ===

1. **理解意图**
   - 分析用户查询的核心需求
   - 识别关键要素：地理范围、领域、时间范围、数据类型等
   - 判断查询的复杂度

2. **制定策略**
   - 简单查询：直接关键词搜索
   - 复杂查询：先用条件筛选缩小范围，再关键词精确匹配
   - 不确定查询：先浏览概要了解可用数据源

3. **逐步探索**（类似漏斗）
   - 第一步：粗筛（按国家/领域）→ 100+ 缩减到 20-30
   - 第二步：关键词搜索 → 20-30 缩减到 5-10
   - 第三步：获取详情深入分析 → 5-10 选出 Top 3

4. **并行优化**
   - 当需要多个独立信息时，并行调用工具
   - 例如：同时搜索多个关键词组合
   - 例如：同时获取多个候选源的详情

5. **给出推荐**
   - 按相关度排序推荐 Top 3-5
   - 清晰说明每个数据源的优势
   - 解释为什么它匹配用户需求

=== 工具使用指南 ===

**list_sources_summary**
- 用于：快速浏览、了解某个国家/领域有哪些数据源
- 适合：用户查询较宽泛时先探索
- 示例：用户问"有哪些中国的经济数据？" → list_sources_summary(country="CN", domain="economics")

**search_sources_by_keywords**
- 用于：根据关键概念快速定位
- 适合：用户有明确关键词时
- 示例：用户问"货币供应量M1M2" → search_sources_by_keywords(keywords=["monetary", "M1", "M2", "money supply"])

**filter_sources_by_criteria**
- 用于：精确筛选，多条件组合
- 适合：用户有特定要求（需要API、特定时间范围、高质量）
- 示例：用户问"需要有API的中国金融数据" → filter_sources_by_criteria(geographic_scope="China", has_api=True, domain="finance")

**get_source_details**
- 用于：深入了解候选数据源
- 适合：缩小到少数候选后，获取完整信息对比
- 示例：初选出3个候选 → get_source_details(["china-pbc", "china-nbs", "china-customs"])

=== 输出格式要求 ===

最终推荐**必须**使用以下Markdown表格格式：

## 推荐数据源

| # | 名称 | 描述 | 质量评分 | URL | API支持 | 访问级别 |
|---|------|------|----------|-----|---------|----------|
| 1 | 数据源中英文名称 | 简短描述（1-2句话，说明数据内容） | X.X/5星 | 完整URL | ✅/❌ | 免费/注册/付费 |
| 2 | ... | ... | ... | ... | ... | ... |

**表格列说明**：
- **#**: 推荐排名（1-5）
- **名称**: 数据源完整名称（中英文）
- **描述**: 核心数据内容简述，1-2句话，突出最重要的信息
- **质量评分**: 根据quality字段计算平均分（如4.5/5星）
- **URL**: 数据源访问网址
- **API支持**: ✅表示有API，❌表示无API
- **访问级别**: 免费开放/需注册/付费等

表格之后，可以添加**补充说明**（可选）：
- 推荐理由概述
- 数据覆盖范围
- 使用建议

=== 示例 ===

**用户查询**："我需要研究中国近10年的货币政策，特别是M1、M2货币供应量和利率数据"

**你的思考过程**：
1. 关键要素：地理=中国、领域=金融/货币政策、时间=近10年、关键词=M1/M2/利率
2. 策略：先按地理+领域筛选，再用关键词精确匹配
3. 探索步骤：
   - 筛选中国+金融领域数据源
   - 搜索"monetary policy, M1, M2, interest rate"
   - 获取候选详情对比

**工具调用序列**：
1. filter_sources_by_criteria(geographic_scope="China", time_range={"start_year": 2014})
2. search_sources_by_keywords(keywords=["monetary policy", "M1", "M2", "money supply", "interest rate"])
3. get_source_details(["china-pbc", "china-nbs"])

**最终输出**：

## 推荐数据源

| # | 名称 | 描述 | 质量评分 | URL | API支持 | 访问级别 |
|---|------|------|----------|-----|---------|----------|
| 1 | People's Bank of China<br>中国人民银行 | 提供M0/M1/M2货币供应量、基准利率、政策利率、市场利率等货币政策数据，覆盖1990-2024年 | 5.0/5星 | http://www.pbc.gov.cn | ❌ | 免费开放 |
| 2 | National Bureau of Statistics<br>国家统计局 | 提供GDP、投资、消费等宏观经济数据，可用于分析货币政策传导效果，月度/季度更新 | 4.8/5星 | http://www.stats.gov.cn | ❌ | 免费开放 |

**推荐理由**：
- **人民银行**：中央银行官方数据，权威性最高，直接提供M1/M2货币供应量和利率完整时间序列
- **国家统计局**：提供宏观经济背景数据，可与货币政策数据结合分析

=== 注意事项 ===

- 使用中文与用户沟通
- 不使用emoji
- 并行调用工具以提高效率
- 给出推荐后不要继续探索，直接结束
- 如果没有找到合适的数据源，诚实告知并建议更宽泛的搜索词
"""


# ============================================================================
# Agent执行
# ============================================================================

def get_anthropic_client():
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


def execute_tool(tool_name: str, tool_input: Dict) -> Any:
    """执行工具调用"""
    if tool_name == "list_sources_summary":
        return tool_list_sources_summary(**tool_input)
    elif tool_name == "search_sources_by_keywords":
        return tool_search_sources_by_keywords(**tool_input)
    elif tool_name == "get_source_details":
        return tool_get_source_details(**tool_input)
    elif tool_name == "filter_sources_by_criteria":
        return tool_filter_sources_by_criteria(**tool_input)
    else:
        return {"error": f"Unknown tool: {tool_name}"}


def datasource_search_agent(user_query: str, max_iterations: int = 10) -> str:
    """
    LLM Agent搜索数据源

    Args:
        user_query: 用户查询
        max_iterations: 最大工具调用轮次

    Returns:
        Agent的最终推荐结果
    """
    client = get_anthropic_client()
    model = os.getenv("QUERY_UNDERSTANDING_MODEL", "claude-sonnet-4-5-20250929")

    messages = [
        {
            "role": "user",
            "content": user_query
        }
    ]

    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        # 调用LLM
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=AGENT_SYSTEM_PROMPT,
            tools=AGENT_TOOLS,
            messages=messages
        )

        # 检查是否需要工具调用
        if response.stop_reason == "end_turn":
            # Agent完成，返回最终结果
            final_text = ""
            for block in response.content:
                if block.type == "text":
                    final_text += block.text
            return final_text

        # 处理工具调用
        if response.stop_reason == "tool_use":
            # 添加assistant消息
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            # 执行所有工具调用
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"[Agent] 调用工具: {block.name}")
                    print(f"[Agent] 参数: {json.dumps(block.input, ensure_ascii=False)}")

                    # 执行工具
                    result = execute_tool(block.name, block.input)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })

            # 添加工具结果
            messages.append({
                "role": "user",
                "content": tool_results
            })
        else:
            # 其他停止原因
            return f"Agent stopped unexpectedly: {response.stop_reason}"

    return "达到最大迭代次数，Agent未能完成任务"


# ============================================================================
# MCP服务器初始化
# ============================================================================

# Pydantic输入模型
class AgentSearchInput(BaseModel):
    """Agent搜索输入模型"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    query: str = Field(
        ...,
        description="用户的数据需求描述，可以是自然语言查询",
        min_length=2,
        max_length=1000
    )


# 初始化FastMCP（HTTP模式）
mcp = FastMCP(
    "datasource_hub_agent",
    host="0.0.0.0",
    port=8001
)


@mcp.tool(
    name="datasource_search_llm_agent",
    annotations={
        "title": "LLM Agent智能数据源搜索",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def datasource_search_llm_agent(params: AgentSearchInput) -> str:
    """
    LLM Agent驱动的智能数据源搜索工具

    这是一个完全由LLM驱动的智能搜索Agent。与传统关键词搜索不同，
    Agent能够理解复杂的自然语言查询，自主决策使用哪些工具，
    通过多步探索逐步缩小范围，最终给出精准推荐和详细理由。

    **适用场景:**
    - 复杂的数据需求描述（例如："我需要研究中国近10年的货币政策"）
    - 需要多维度组合筛选（地理、时间、领域、质量要求等）
    - 希望获得详细的推荐理由和使用建议
    - 不确定具体关键词，用自然语言描述需求

    **Agent能力:**
    - 自主制定搜索策略
    - 逐步探索：粗筛 → 精选 → 深入分析
    - 并行优化：同时调用多个工具提高效率
    - 智能推荐：Top 3-5数据源，附带详细理由

    **与普通搜索的区别:**
    - 普通搜索：关键词匹配 + 评分排序
    - Agent搜索：理解意图 + 多步探索 + 推理决策

    Args:
        params (AgentSearchInput): 搜索参数
            - query (str, required): 自然语言查询，描述数据需求 (2-1000字符)

    Returns:
        str: Agent的推荐结果，包含：
            - Top 3-5 推荐数据源
            - 每个数据源的详细推荐理由
            - 使用建议
            - 性能统计信息

    Examples:
        **复杂查询:**
        - "我需要研究中国近10年的货币政策，特别是M1、M2货币供应量和利率数据"
        - "寻找有API访问的全球气候变化数据，需要包含温度和降水量"
        - "美国和欧洲的失业率统计数据，要求权威性高、更新及时"

        **简单查询:**
        - "中国人民银行的数据"
        - "世界银行发展指标"
        - "美国劳工统计局"

    注意:
        - 首次调用需要加载所有数据源，可能需要几秒钟
        - Agent会进行多轮LLM调用，耗时比普通搜索长
        - 适合复杂查询，简单查询建议使用 datasource_search_sources
    """
    try:
        start_time = time.time()
        result = datasource_search_agent(params.query)
        elapsed = time.time() - start_time

        # 添加性能统计和版本信息
        footer = f"\n\n---\n\n*搜索耗时: {elapsed:.2f}秒 | 由LLM Agent自主探索完成 | DataSource Hub MCP v{__version__}*"

        return result + footer

    except Exception as e:
        return f"搜索失败: {str(e)}"


# ============================================================================
# HTTP认证中间件
# ============================================================================

class BearerAuthMiddleware(BaseHTTPMiddleware):
    """Bearer Token认证中间件"""

    async def dispatch(self, request: Request, call_next):
        # 读取环境变量中的API Key
        expected_key = os.getenv("MCP_API_KEY", "")

        # 如果未设置API Key，跳过认证
        if not expected_key:
            return await call_next(request)

        # 提取Authorization header
        auth_header = request.headers.get("Authorization", "")

        # 验证Bearer token
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                {"error": "Missing or invalid Authorization header"},
                status_code=401
            )

        token = auth_header[7:]  # 移除"Bearer "前缀

        if token != expected_key:
            return JSONResponse(
                {"error": "Invalid API key"},
                status_code=403
            )

        # Token有效，继续处理
        return await call_next(request)


# ============================================================================
# 启动服务器
# ============================================================================

def main():
    """主函数：启动MCP服务器"""
    # 检查认证配置
    api_key = os.getenv("MCP_API_KEY")
    if api_key:
        print(f"[INFO] Authentication enabled. Clients must provide 'Authorization: Bearer <token>' header.")
    else:
        print("[WARN] MCP_API_KEY not set. Running without authentication.")

    print(f"[INFO] DataSource Hub Agent MCP Server v{__version__}")
    print(f"[INFO] Starting HTTP server on http://0.0.0.0:8001")

    # 包装MCP app with认证中间件
    mcp_app = mcp.streamable_http_app()
    app = Starlette(
        routes=mcp_app.routes,
        middleware=[Middleware(BearerAuthMiddleware)],
        lifespan=mcp_app.router.lifespan_context
    )

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)


if __name__ == "__main__":
    main()
