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
import httpx

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
        用于精确缩小搜索范围，支持地理、时间、访问方式、领域等多维度筛选。

        参数:
        - geographic_scope: 可选，地理范围（如 "China", "Global", "Asia"）
        - domain: 可选，领域（如 "finance", "health", "economics", "energy"）
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
                "domain": {
                    "type": "string",
                    "description": "领域，如 finance, health, economics, energy"
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
    },
    {
        "name": "web_search",
        "description": """
        搜索最新新闻和信息，仅用于获取新闻线索，帮助了解当前热点事件。

        ⚠️ 重要约束：
        - 此工具返回的新闻内容**仅作为参考线索**，不应作为可信数据源
        - 新闻用于了解最新动态，帮助确定需要搜索哪些**权威数据源**
        - 最终推荐时必须推荐数据源，而非新闻链接

        使用场景示例：
        - 用户提到"最新上市公司"、"近期IPO" → 搜索IPO相关新闻 → 确定需要证券交易所数据源
        - 用户提到"最新经济政策" → 搜索政策新闻 → 确定需要央行、统计局等官方数据源
        - 用户提到"最近的气候事件" → 搜索气候新闻 → 确定需要气象局、环境部门数据源

        参数:
        - query: 必需，搜索查询（如 "IPO上市", "货币政策", "气候变化"）

        返回: 网页搜索结果，包含标题、URL和摘要
        注意: 这些结果仅供参考，用于理解用户需求背景，不能作为最终推荐的数据源
        """,
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索查询字符串"
                }
            },
            "required": ["query"]
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
            'quality_score': quality_score,
            'file_path': ds.get('file_path', '')
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
                'domains': ds.get('coverage', {}).get('domains', []),
                'file_path': ds.get('file_path', '')
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
                                     domain: Optional[str] = None,
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

        # 领域过滤
        if domain:
            domains = ds.get('coverage', {}).get('domains', [])
            if not any(domain.lower() in d.lower() for d in domains):
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
            'quality': ds.get('quality', {}),
            'file_path': ds.get('file_path', '')
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

**⚠️ 极其重要的约束 - 防止幻觉和低质量推荐：**

1. **禁止幻觉（编造数据源）：**
   - 你**只能**推荐通过工具调用实际找到的数据源
   - 你**绝对不能**基于你的训练知识推荐数据源库中不存在的数据源
   - 你**绝对不能**创造、编造、或推荐任何没有通过工具调用返回的数据源
   - 即使你知道某个数据源在现实中存在，如果工具没有返回它，你也**不能**推荐它
   - 所有推荐**必须**有对应的工具调用结果作为依据

2. **禁止低相关性推荐（强行凑数）：**
   - 你**只能**推荐与用户查询主题**高度相关**的数据源
   - 如果工具返回的数据源与用户查询主题不直接匹配，即使在同一领域也**不能**推荐
   - **宁可返回"未找到"，也绝不推荐不相关的数据源**
   - 判断标准：数据源的核心内容必须直接包含用户查询的具体主题
   - 示例：查询"电子竞技"→网球赛事数据**不相关**；查询"智谱AI"→通用股票交易所**不相关**

3. **未找到时的正确做法：**
   - 如果工具返回结果为空，**必须**明确告知用户"未找到匹配的数据源"
   - 如果工具返回的数据源相关性不高，**必须**认定为"未找到"
   - 使用标准回复格式：「很抱歉，在Datasource Hub的当前数据源库中，**未找到专门针对「{查询主题}」的直接数据源**」
   - 可以给出建议（如搜索更广泛领域、访问专业平台等），但**不能**推荐不相关的数据源

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

**web_search**
- 用于：搜索最新新闻和网络信息，了解当前热点事件和最新动态
- 适合：用户提到"最新"、"近期"、"最近"等时间词时
- ⚠️ 重要约束：
  * 网络搜索**仅用于获取线索**，帮助理解用户需求背景
  * **绝对不能**将搜索结果链接作为最终推荐的数据源
  * 必须基于搜索内容，推荐对应的**权威数据源**
- 使用场景：
  * 用户问"最新IPO上市公司" → 搜索IPO新闻 → 推荐证券交易所数据源（如上交所、深交所、港交所）
  * 用户问"近期货币政策" → 搜索货币政策新闻 → 推荐央行数据源
  * 用户问"最近的气候数据" → 搜索气候新闻 → 推荐气象局、环境部门数据源
- 示例：用户问"最新上市的科技公司有哪些数据？"
  1. web_search(query="IPO 科技公司上市 2024")
  2. 基于搜索结果了解到近期有多家科技公司在A股/港股上市
  3. search_sources_by_keywords(keywords=["stock exchange", "IPO", "listing"])
  4. 推荐：上海证券交易所、深圳证券交易所、香港交易所等数据源

=== 输出格式要求 ===

最终推荐**必须**使用以下Markdown表格格式：

## 推荐数据源

| # | 名称 | 描述 | 质量评分 | URL | API支持 | 访问级别 | JSON文件 |
|---|------|------|----------|-----|---------|----------|----------|
| 1 | 数据源中英文名称 | 简短描述（1-2句话，说明数据内容） | X.X/5星 | 完整URL | ✅/❌ | 免费/注册/付费 | /sources/path/to/file.json |
| 2 | ... | ... | ... | ... | ... | ... | ... |

**表格列说明**：
- **#**: 推荐排名（1-5）
- **名称**: 数据源完整名称（中英文）
- **描述**: 核心数据内容简述，1-2句话，突出最重要的信息
- **质量评分**: 根据quality字段计算平均分（如4.5/5星）
- **URL**: 数据源访问网址
- **API支持**: ✅表示有API，❌表示无API
- **访问级别**: 免费开放/需注册/付费等
- **JSON文件**: 数据源配置文件的相对路径，直接使用tool返回的file_path字段（格式：`/sources/...`）

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

| # | 名称 | 描述 | 质量评分 | URL | API支持 | 访问级别 | JSON文件 |
|---|------|------|----------|-----|---------|----------|----------|
| 1 | People's Bank of China<br>中国人民银行 | 提供M0/M1/M2货币供应量、基准利率、政策利率、市场利率等货币政策数据，覆盖1990-2024年 | 5.0/5星 | http://www.pbc.gov.cn | ❌ | 免费开放 | /sources/countries/asia/china/china-pbc.json |
| 2 | National Bureau of Statistics<br>国家统计局 | 提供GDP、投资、消费等宏观经济数据，可用于分析货币政策传导效果，月度/季度更新 | 4.8/5星 | http://www.stats.gov.cn | ❌ | 免费开放 | /sources/countries/asia/china/china-nbs.json |

**推荐理由**：
- **人民银行**：中央银行官方数据，权威性最高，直接提供M1/M2货币供应量和利率完整时间序列
- **国家统计局**：提供宏观经济背景数据，可与货币政策数据结合分析

=== 注意事项 ===

- 使用中文与用户沟通
- 不使用emoji
- 并行调用工具以提高效率
- 给出推荐后不要继续探索，直接结束
- **绝对禁止推荐工具未返回的数据源，即使你认为该数据源存在**
- **当搜索结果为空时，必须明确说明"未找到匹配的数据源"，而不是基于知识编造推荐**
- **重要：表格中必须包含"JSON文件"列，使用工具返回的file_path字段**
- **file_path格式：工具返回的路径格式为"sources/..."，在表格中需要添加前导斜杠，格式为 `/sources/...`**

**⚠️ 严格的相关性要求：**
- **只推荐与用户需求高度相关的数据源，绝对不能为了凑数而推荐不相关的数据源**
- **如果工具返回的数据源与用户查询的主题不匹配，必须认定为"未找到"**
- **判断标准：数据源的核心内容必须直接包含用户查询的主题，而不仅仅是领域相关**
- **示例：**
  * 用户查询"电子竞技赛事数据" → ATP/WTA网球数据**不相关**（虽然都是体育，但主题不同）
  * 用户查询"电子竞技赛事数据" → 加拿大统计局**不相关**（虽然可能包含体育统计，但不是电竞）
  * 用户查询"智谱AI招股书" → 通用IPO数据源**不相关**（需要专门包含智谱AI的数据源）

**未找到数据源时的标准回复格式：**
```
很抱歉，在Datasource Hub的当前数据源库中，**未找到专门针对「{用户查询主题}」的直接数据源**。

**建议：**
- 可以尝试搜索更广泛的相关领域数据源
- 如果需要这类数据，建议访问相关领域的官方网站或专业平台
```

**关于web_search工具的特别约束：**
- **web_search仅用于了解背景和最新动态，绝对不能作为可信数据源**
- **最终推荐必须是权威数据源（如政府机构、交易所、国际组织等），而不是搜索结果链接**
- **搜索内容仅供参考，用于判断用户需要哪类数据，然后搜索对应的官方数据源**
- 如果用户查询中包含"最新"、"近期"等时间词，可以先使用 web_search 了解动态，再推荐数据源
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


# MCP 会话缓存（简单的内存缓存）
_mcp_session_cache = {}

def _get_mcp_session(mcp_url: str, headers: dict) -> Optional[str]:
    """
    获取或创建 MCP 会话

    返回 session ID，如果失败返回 None
    """
    cache_key = mcp_url

    # 检查缓存
    if cache_key in _mcp_session_cache:
        session_id = _mcp_session_cache[cache_key]
        print(f"[INFO] Using cached MCP session: {session_id[:8]}...")
        return session_id

    # 初始化新会话
    try:
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "datasource-hub-agent",
                    "version": __version__
                }
            }
        }

        print(f"[INFO] Initializing MCP session...")

        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            response = client.post(
                mcp_url.rstrip('/'),
                json=init_payload,
                headers=headers
            )

            # 从响应头获取 session ID
            session_id = response.headers.get('mcp-session-id')

            if session_id:
                print(f"[INFO] MCP session initialized: {session_id[:8]}...")
                _mcp_session_cache[cache_key] = session_id
                return session_id
            else:
                # 尝试从响应体获取
                try:
                    result = response.json()
                    if "result" in result and isinstance(result["result"], dict):
                        session_id = result["result"].get("sessionId")
                        if session_id:
                            _mcp_session_cache[cache_key] = session_id
                            return session_id
                except:
                    pass

                print(f"[WARN] No session ID in response")
                return None

    except Exception as e:
        print(f"[ERROR] Failed to initialize MCP session: {e}")
        return None


def tool_web_search(query: str) -> List[Dict]:
    """
    网络搜索工具实现

    调用外部 HTTP MCP 服务器的 web_search 工具
    使用 MCP SSE (Server-Sent Events) 传输协议
    """
    mcp_url = os.getenv("WEB_SEARCH_MCP_URL")
    mcp_token = os.getenv("WEB_SEARCH_MCP_AUTH_TOKEN")

    if not mcp_url:
        print("[WARN] WEB_SEARCH_MCP_URL not configured, web_search unavailable")
        return [{
            "title": "Web Search 配置缺失",
            "snippet": "WEB_SEARCH_MCP_URL 环境变量未配置。请在 .env 文件中添加外部 MCP 服务器配置。",
            "url": "",
            "source": "system"
        }]

    try:
        # MCP SSE 协议要求的 headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        if mcp_token:
            headers["Authorization"] = f"Bearer {mcp_token}"

        # 获取或创建会话
        session_id = _get_mcp_session(mcp_url, headers)
        if session_id:
            headers["mcp-session-id"] = session_id

        # JSON-RPC 2.0 格式的工具调用请求
        payload = {
            "jsonrpc": "2.0",
            "id": int(time.time()),  # 使用时间戳作为请求 ID
            "method": "tools/call",
            "params": {
                "name": "web_search",
                "arguments": {
                    "query": query
                }
            }
        }

        print(f"[INFO] Calling external MCP web_search via JSON-RPC")
        print(f"[INFO] URL: {mcp_url}")
        print(f"[INFO] Query: {query}")

        # 同步 HTTP 调用
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            response = client.post(
                mcp_url.rstrip('/'),
                json=payload,
                headers=headers
            )

            # 如果返回 400 且提示 session 问题，清除缓存并重试
            if response.status_code == 400:
                try:
                    error_result = response.json()
                    if "error" in error_result and "session" in error_result["error"].get("message", "").lower():
                        print("[WARN] Session expired, retrying with new session...")
                        _mcp_session_cache.pop(mcp_url, None)

                        # 重新获取session并重试
                        session_id = _get_mcp_session(mcp_url, headers)
                        if session_id:
                            headers["mcp-session-id"] = session_id
                            response = client.post(
                                mcp_url.rstrip('/'),
                                json=payload,
                                headers=headers
                            )
                except:
                    pass

            response.raise_for_status()

            # 检查响应类型
            content_type = response.headers.get('content-type', '')

            # 处理 SSE 响应
            if 'text/event-stream' in content_type:
                print(f"[INFO] Received SSE stream response")
                # 解析 SSE 格式: "event: message\ndata: {json}\n\n"
                lines = response.text.split('\n')
                for line in lines:
                    if line.startswith('data: '):
                        json_data = line[6:]  # 移除 "data: " 前缀
                        try:
                            result = json.loads(json_data)
                            print(f"[INFO] Parsed SSE data: {json.dumps(result, ensure_ascii=False)[:200]}...")
                            break
                        except json.JSONDecodeError as e:
                            print(f"[WARN] Failed to parse SSE data: {e}")
                            continue
                else:
                    print(f"[ERROR] No valid SSE data found in response")
                    return [{"title": "解析错误", "snippet": "SSE响应中未找到有效数据", "url": "", "source": "system"}]
            else:
                # 标准 JSON 响应
                result = response.json()
                print(f"[INFO] MCP response: {json.dumps(result, ensure_ascii=False)[:200]}...")

            # 解析 JSON-RPC 响应
            if isinstance(result, dict):
                # 检查是否有错误
                if "error" in result:
                    error = result["error"]
                    print(f"[ERROR] MCP returned error: {error}")
                    return [{
                        "title": "MCP 调用错误",
                        "snippet": error.get("message", str(error)),
                        "url": "",
                        "source": "system"
                    }]

                # 获取结果
                if "result" in result:
                    rpc_result = result["result"]

                    # MCP 标准响应格式: {"content": [...], "isError": false}
                    if isinstance(rpc_result, dict) and "content" in rpc_result:
                        content = rpc_result["content"]

                        if isinstance(content, list) and len(content) > 0:
                            # 提取文本内容
                            first_content = content[0]
                            if isinstance(first_content, dict) and "text" in first_content:
                                try:
                                    # 尝试解析 JSON 文本
                                    return json.loads(first_content["text"])
                                except json.JSONDecodeError:
                                    # 如果不是 JSON，返回原始文本
                                    return [{
                                        "title": "Search Results",
                                        "snippet": first_content["text"],
                                        "url": "",
                                        "source": "web_search"
                                    }]

                        return content
                    else:
                        # 直接返回结果
                        return rpc_result if isinstance(rpc_result, list) else [rpc_result]

            return [{"title": "Unexpected Response", "snippet": str(result), "url": "", "source": "system"}]

    except httpx.HTTPError as e:
        print(f"[ERROR] HTTP error calling MCP service: {e}")
        return [{
            "title": "搜索服务调用失败",
            "snippet": f"HTTP 错误: {str(e)}。请检查 MCP 服务器配置和网络连接。",
            "url": "",
            "source": "system"
        }]
    except Exception as e:
        print(f"[ERROR] Unexpected error calling MCP service: {e}")
        import traceback
        traceback.print_exc()
        return [{
            "title": "搜索工具调用失败",
            "snippet": f"未知错误: {str(e)}",
            "url": "",
            "source": "system"
        }]


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
    elif tool_name == "web_search":
        return tool_web_search(**tool_input)
    else:
        return {"error": f"Unknown tool: {tool_name}"}


def datasource_search_agent(user_query: str, max_results: int = 5, max_iterations: int = 10) -> str:
    """
    LLM Agent搜索数据源

    Args:
        user_query: 用户查询
        max_results: 返回的最大数据源数量
        max_iterations: 最大工具调用轮次

    Returns:
        Agent的最终推荐结果
    """
    client = get_anthropic_client()
    model = os.getenv("QUERY_UNDERSTANDING_MODEL", "gemini-3-flash-preview")

    # 将 max_results 添加到系统提示中
    system_prompt = AGENT_SYSTEM_PROMPT + f"\n\n**本次查询限制**: 最多返回 {max_results} 个推荐数据源。"

    messages = [
        {
            "role": "user",
            "content": user_query
        }
    ]

    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        print(f"\n[Agent] === 第 {iteration} 轮迭代 ===")

        # 调用LLM
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            tools=AGENT_TOOLS,
            messages=messages
        )

        # 打印response的内容块
        print(f"[Agent] Response包含 {len(response.content)} 个内容块:")
        for i, block in enumerate(response.content):
            print(f"[Agent]   块{i+1}: type={block.type}")
            if block.type == "text":
                print(f"[Agent]       text内容: {block.text[:100]}...")
            elif hasattr(block, 'name'):
                print(f"[Agent]       工具名称: {block.name}")

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

                    # 执行工具（web_search由Anthropic API自动处理，这里只处理本地工具）
                    result = execute_tool(block.name, block.input)

                    # 打印工具结果（用于调试）
                    if block.name == "web_search":
                        print(f"[Agent] ⚠️ web_search由Anthropic API处理，结果将在API响应中返回")
                    else:
                        print(f"[Agent] 工具返回结果: {json.dumps(result, ensure_ascii=False)[:200]}...")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })

            # 打印所有工具结果
            print(f"\n[Agent] 收集到 {len(tool_results)} 个工具结果:")
            for i, tr in enumerate(tool_results):
                print(f"[Agent]   结果{i+1}: tool_use_id={tr['tool_use_id']}")
                content = tr['content']
                # 尝试解析JSON以美化输出
                try:
                    parsed = json.loads(content)
                    print(f"[Agent]       内容: {json.dumps(parsed, ensure_ascii=False, indent=2)[:500]}...")
                except:
                    print(f"[Agent]       内容(原始): {content[:500]}...")

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
        description=(
            "自然语言数据需求描述，支持从简单关键词到复杂多维度查询\n\n"
            "**格式**: 2-1000字符的自然语言文本\n\n"
            "**复杂查询示例**:\n"
            "  - \"我需要研究中国近10年的货币政策，特别是M1、M2货币供应量和利率数据\"\n"
            "  - \"寻找有API访问的全球气候变化数据，需要包含温度和降水量\"\n"
            "  - \"美国和欧洲的失业率统计数据，要求权威性高、更新及时\"\n\n"
            "**简单查询示例**:\n"
            "  - \"GDP数据\"\n"
            "  - \"中国人民银行\"\n"
            "  - \"世界银行发展指标\"\n\n"
            "**建议**: 查询越具体（包含地理范围、时间、领域等），推荐结果越精准"
        ),
        min_length=2,
        max_length=1000
    )

    max_results: int = Field(
        default=5,
        description=(
            "返回的最大数据源数量\n\n"
            "**默认值**: 5\n"
            "**范围**: 1-20\n"
            "**说明**: 控制返回的推荐数据源数量，防止结果过多占用上下文窗口"
        ),
        ge=1,
        le=20
    )


# 初始化FastMCP（HTTP模式）
mcp = FastMCP(
    "datasource_hub",
    host="0.0.0.0",
    port=8001
)


# ============================================================================
# 独立MCP工具定义（直接暴露给Claude Code）
# ============================================================================

@mcp.tool(
    name="datasource_list_sources",
    annotations={
        "title": "浏览数据源列表",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True
    }
)
async def datasource_list_sources(
    country: str = Field(
        default="",
        description="国家代码或名称，如 CN（中国）, US（美国）, Global（全球）。留空则返回所有国家"
    ),
    domain: str = Field(
        default="",
        description="领域，如 finance（金融）, health（健康）, economics（经济）, energy（能源）。留空则返回所有领域"
    ),
    limit: int = Field(
        default=50,
        ge=1,
        le=200,
        description="返回数量限制，默认50，最大200"
    )
) -> str:
    """
    快速浏览数据源列表

    用于快速了解某个国家或领域有哪些数据源。返回概要信息，包括数据源名称、国家、领域和质量评分。

    **适用场景:**
    - 探索某个国家有哪些数据源
    - 浏览某个领域的所有数据源
    - 快速了解数据源全貌

    **示例:**
    - 查看中国的金融数据源: country="CN", domain="finance"
    - 浏览所有全球数据源: country="Global"
    - 获取所有健康领域数据源: domain="health"

    **返回格式:** JSON字符串，包含数据源列表
    """
    try:
        results = tool_list_sources_summary(
            country=country if country else None,
            domain=domain if domain else None,
            limit=limit
        )
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool(
    name="datasource_search_keywords",
    annotations={
        "title": "关键词搜索数据源",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True
    }
)
async def datasource_search_keywords(
    keywords: List[str] = Field(
        ...,
        description="搜索关键词列表，如 [\"GDP\", \"China\", \"statistics\"]"
    ),
    search_fields: List[str] = Field(
        default=["all"],
        description="搜索范围: name（名称）, description（描述）, tags（标签）, content（数据内容）, all（全部）"
    ),
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="返回数量限制，默认20"
    )
) -> str:
    """
    使用关键词精确搜索数据源

    在数据源的名称、描述、标签和内容中搜索指定关键词，按匹配得分排序返回结果。

    **适用场景:**
    - 知道明确的关键词（如"GDP"、"人民银行"）
    - 快速定位特定数据源
    - 搜索特定概念或指标

    **示例:**
    - 搜索GDP数据: keywords=["GDP", "economic growth"]
    - 搜索中国人民银行: keywords=["People's Bank", "China", "PBC"]
    - 只在名称中搜索: keywords=["World Bank"], search_fields=["name"]

    **返回格式:** JSON字符串，包含匹配的数据源及匹配得分
    """
    try:
        results = tool_search_sources_by_keywords(
            keywords=keywords,
            search_fields=search_fields,
            limit=limit
        )
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool(
    name="datasource_get_details",
    annotations={
        "title": "获取数据源详细信息",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True
    }
)
async def datasource_get_details(
    source_ids: List[str] = Field(
        ...,
        description="数据源ID列表，如 [\"china-pbc\", \"china-nbs\"]"
    ),
    fields: List[str] = Field(
        default=["all"],
        description="返回字段: all（全部）, description（描述）, coverage（覆盖范围）, quality（质量）, access（访问方式）"
    )
) -> str:
    """
    获取指定数据源的完整详细信息

    返回数据源的详细配置，包括描述、覆盖范围、数据内容、访问方式、质量评分等。

    **适用场景:**
    - 深入了解某个特定数据源
    - 对比多个候选数据源
    - 获取访问URL、API信息等详细信息

    **示例:**
    - 获取中国人民银行详情: source_ids=["china-pbc"]
    - 对比两个数据源: source_ids=["china-pbc", "china-nbs"]
    - 只获取访问信息: source_ids=["worldbank"], fields=["access", "quality"]

    **返回格式:** JSON字符串，包含完整的数据源配置
    """
    try:
        results = tool_get_source_details(
            source_ids=source_ids,
            fields=fields
        )
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool(
    name="datasource_filter",
    annotations={
        "title": "多条件筛选数据源",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True
    }
)
async def datasource_filter(
    geographic_scope: str = Field(
        default="",
        description="地理范围，如 China（中国）, Global（全球）, Asia（亚洲）"
    ),
    domain: str = Field(
        default="",
        description="领域，如 finance（金融）, health（健康）, economics（经济）"
    ),
    has_api: bool = Field(
        default=None,
        description="是否需要API访问。True=仅返回有API的数据源，False=仅返回无API的，None=不限制"
    ),
    update_frequency: str = Field(
        default="",
        description="更新频率，如 daily（每日）, monthly（每月）, quarterly（每季度）"
    ),
    min_quality_score: float = Field(
        default=0.0,
        ge=0.0,
        le=5.0,
        description="最低质量评分（0-5分）"
    )
) -> str:
    """
    按多个条件组合精确筛选数据源

    支持地理范围、领域、API、更新频率、质量评分等多维度筛选，返回同时满足所有条件的数据源。

    **适用场景:**
    - 有明确的多个筛选条件
    - 需要满足特定约束（如必须有API）
    - 精确缩小搜索范围

    **示例:**
    - 有API的中国金融数据: geographic_scope="China", domain="finance", has_api=True
    - 高质量全球数据: geographic_scope="Global", min_quality_score=4.5
    - 每日更新的数据源: update_frequency="daily"

    **返回格式:** JSON字符串，包含符合所有条件的数据源列表
    """
    try:
        # 构建筛选参数
        kwargs = {}
        if geographic_scope:
            kwargs['geographic_scope'] = geographic_scope
        if domain:
            kwargs['domain'] = domain
        if has_api is not None:
            kwargs['has_api'] = has_api
        if update_frequency:
            kwargs['update_frequency'] = update_frequency
        if min_quality_score > 0:
            kwargs['min_quality_score'] = min_quality_score

        results = tool_filter_sources_by_criteria(**kwargs)
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# ============================================================================
# Agent工具（智能搜索）
# ============================================================================

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
async def datasource_search_llm_agent(
    query: str = Field(
        ...,
        description=(
            "自然语言数据需求描述，支持从简单关键词到复杂多维度查询\n\n"
            "**格式**: 2-1000字符的自然语言文本\n\n"
            "**复杂查询示例**:\n"
            "  - \"我需要研究中国近10年的货币政策，特别是M1、M2货币供应量和利率数据\"\n"
            "  - \"寻找有API访问的全球气候变化数据，需要包含温度和降水量\"\n"
            "  - \"美国和欧洲的失业率统计数据，要求权威性高、更新及时\"\n\n"
            "**简单查询示例**:\n"
            "  - \"GDP数据\"\n"
            "  - \"中国人民银行\"\n"
            "  - \"世界银行发展指标\"\n\n"
            "**建议**: 查询越具体（包含地理范围、时间、领域等），推荐结果越精准"
        ),
        min_length=2,
        max_length=1000
    ),
    max_results: int = Field(
        default=5,
        description=(
            "返回的最大数据源数量\n\n"
            "**默认值**: 5\n"
            "**范围**: 1-20\n"
            "**说明**: 控制返回的推荐数据源数量，防止结果过多占用上下文窗口"
        ),
        ge=1,
        le=20
    )
) -> str:
    """
    LLM Agent驱动的智能数据源搜索工具（高级功能）

    这是一个完全由LLM驱动的智能搜索Agent。能够理解复杂的自然语言查询，
    自主决策使用哪些工具，通过多步探索逐步缩小范围，最终给出精准推荐和详细理由。

    **🆚 与基础工具的对比:**

    本MCP提供5个工具，分为两类：

    1. **基础工具（快速）** - 响应时间 1-3 秒
       - datasource_list_sources: 浏览数据源列表
       - datasource_search_keywords: 关键词搜索
       - datasource_get_details: 获取详细信息
       - datasource_filter: 多条件筛选

    2. **Agent工具（智能）** - 响应时间 10-30 秒
       - datasource_search_llm_agent: 本工具

    **何时使用基础工具:**
    - 明确知道要搜索什么关键词 → 使用 datasource_search_keywords
    - 想浏览某个国家/领域的数据源 → 使用 datasource_list_sources
    - 已知数据源ID，需要详细信息 → 使用 datasource_get_details
    - 有明确的筛选条件 → 使用 datasource_filter

    **何时使用本Agent工具:**
    - ✅ 复杂的数据需求描述
      示例："我需要研究中国近10年的货币政策，特别是M1、M2货币供应量和利率数据，最好是官方权威数据"
    - ✅ 需要多维度组合筛选（地理、时间、领域、质量要求等）
      示例："寻找有API访问的全球气候变化数据，需要包含温度和降水量"
    - ✅ 希望获得详细的推荐理由和使用建议
    - ✅ 不确定具体关键词，用自然语言描述需求
      示例："美国和欧洲的失业率统计数据，要求权威性高、更新及时"
    - ✅ 需要Agent自动决策和探索

    **❌ 不建议使用本Agent的场景（请用基础工具）:**
    - 极简查询（如"GDP数据"） → 改用 datasource_search_keywords(["GDP"])
    - 快速浏览 → 改用 datasource_list_sources
    - 对响应时间敏感 → 改用基础工具

    **工作原理:**
    Agent会自主制定搜索策略，通过多步探索（粗筛 → 精选 → 深入分析）逐步缩小范围，
    最终给出Top 3-5推荐数据源，并附带详细的匹配理由和使用建议。

    **返回值类型:**
    str - 纯文本字符串，使用Markdown格式化

    **返回内容结构:**
    返回的字符串包含以下Markdown格式的内容块：

    1. **推荐数据源表格** - Top 3-5个推荐数据源的结构化信息
       列包括：# (排名)、名称、描述、质量评分、URL、API支持、访问级别、JSON文件

    2. **推荐理由** - 详细说明每个数据源为什么匹配用户需求

    3. **使用建议**（可选）- 如何获取和使用这些数据源

    **返回示例:**
    ```markdown
    ## 推荐数据源

    | # | 名称 | 描述 | 质量评分 | URL | API支持 | 访问级别 | JSON文件 |
    |---|------|------|----------|-----|---------|----------|----------|
    | 1 | World Bank Open Data<br>世界银行开放数据 | 全球经济发展指标 | 4.8/5星 | https://data.worldbank.org | ✅ | 免费 | /sources/international/economics/worldbank.json |

    **推荐理由**：
    - World Bank提供全球最权威的发展指标数据，覆盖200+国家...
    ```

    注意：返回的是纯文本字符串，不是JSON对象。客户端应直接展示为Markdown内容。

    **性能提示:**
    ⏱️ 首次调用需要加载所有数据源（约5-10秒，取决于数据源数量）
    ⏱️ Agent会进行多轮LLM调用（通常3-5轮），总耗时约10-30秒
    ⏱️ 适合复杂查询，简单查询可能响应较慢但结果更精准
    """
    try:
        result = datasource_search_agent(query, max_results)
        return result

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
