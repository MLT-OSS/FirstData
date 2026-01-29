import json
import os
import time
from datetime import datetime
from typing import Any

import httpx
from config import __version__
from utils import get_anthropic_client

from .tool_filter_sources_by_criteria import tool_filter_sources_by_criteria
from .tool_get_source_details import tool_get_source_details
from .tool_list_sources_summary import tool_list_sources_summary
from .tool_search_sources_by_keywords import tool_search_sources_by_keywords

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
                "country": {"type": "string", "description": "国家代码或名称，如 CN, US, Global"},
                "domain": {"type": "string", "description": "领域，如 finance, health, economics"},
                "limit": {"type": "integer", "description": "返回数量限制", "default": 50},
            },
        },
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
                    "description": "搜索关键词列表",
                },
                "search_fields": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["name", "description", "tags", "content", "all"],
                    },
                    "description": "搜索范围",
                    "default": ["all"],
                },
                "limit": {"type": "integer", "description": "返回数量限制", "default": 20},
            },
            "required": ["keywords"],
        },
    },
    {
        "name": "get_source_details",
        "description": """
        获取指定数据源的完整详细信息。
        用于深入了解候选数据源的具体内容、覆盖范围、权威级别等。

        参数:
        - source_ids: 必需，数据源ID列表（如 ["china-pbc", "china-nbs"]）
        - fields: 可选，返回哪些字段，默认返回全部

        返回: 数据源的完整信息，包括描述、访问方式、覆盖范围、数据内容、权威级别等
        """,
        "input_schema": {
            "type": "object",
            "properties": {
                "source_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "数据源ID列表",
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "返回字段，如 ['description', 'coverage', 'quality']",
                    "default": ["all"],
                },
            },
            "required": ["source_ids"],
        },
    },
    {
        "name": "filter_sources_by_criteria",
        "description": """
        按多个条件组合筛选数据源。
        用于精确缩小搜索范围，支持地理、领域、访问方式、权威级别等多维度筛选。

        参数:
        - geographic_scope: 可选，地理范围（如 "China", "Global", "Asia"）
        - domain: 可选，领域（如 "finance", "health", "economics", "energy"）
        - has_api: 可选，是否需要API访问
        - update_frequency: 可选，更新频率（如 "monthly", "daily"）
        - authority_level: 可选，权威级别（如 "government", "international", "research"）

        返回: 符合条件的数据源列表
        """,
        "input_schema": {
            "type": "object",
            "properties": {
                "geographic_scope": {"type": "string", "description": "地理范围"},
                "domain": {
                    "type": "string",
                    "description": "领域，如 finance, health, economics, energy",
                },
                "has_api": {"type": "boolean", "description": "是否需要API"},
                "update_frequency": {"type": "string", "description": "更新频率"},
                "authority_level": {
                    "type": "string",
                    "description": "权威级别: government, international, market, research, commercial, other",
                },
            },
        },
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
            "properties": {"query": {"type": "string", "description": "搜索查询字符串"}},
            "required": ["query"],
        },
    },
]

AGENT_SYSTEM_PROMPT = """你是FirstData的数据源搜索专家。你擅长通过逐步探索和分析，帮助用户找到最合适的权威数据源。

当前的日期是: {current_date}

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
   - 使用标准回复格式：「很抱歉，在FirstData的当前数据源库中，**未找到专门针对「{查询主题}」的直接数据源**」
   - 可以给出建议（如搜索更广泛领域、访问专业平台等），但**不能**推荐不相关的数据源

=== 工作流程建议 ===

1. **理解意图与web_search决策**
   - 分析用户查询的核心需求
   - 识别关键要素：地理范围、领域、时间范围、数据类型等

   **⚠️ 关键决策点：是否需要先web_search？**
   - 如果满足以下任一条件，**必须先调用web_search**：
     * 用户提到"最新"/"近期"/"最近"/"今年" + 具体主题/公司/事件
     * 用户询问特定公司/机构的当前状态（如"智谱的招股书"）
     * 用户查询时间敏感的信息

   - **web_search工作流程**：
     1. 先调用 web_search 了解最新动态
     2. 基于搜索结果确定需要哪类权威数据源
     3. 在数据源库中搜索对应的官方数据源
     4. 推荐权威数据源（而非新闻链接）

   - 判断查询的复杂度

2. **制定策略**
   - **如果第1步决定需要web_search**：
     * 先搜索新闻获取最新信息
     * 基于最新信息判断需要什么类型的数据源
     * 再在数据源库中搜索
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

- ⚠️ **强制使用场景**（必须先调用web_search）：
  * 用户提到"最新"+"具体主题"（如"最新IPO"、"最新招股书"、"最新政策"）
  * 用户询问特定公司/机构/事件的近期信息（如"智谱的招股书"、"特斯拉的财报"）
  * 用户查询时间敏感的数据（如"近期"、"最近"、"今年"、"2025年"）

- **标准工作流程**（包含web_search时）：
  1. **第一步**：web_search 了解最新动态和背景
  2. **第二步**：分析搜索结果，理解当前状况（如某公司在哪个交易所上市）
  3. **第三步**：基于第二步的理解，在数据源库中搜索对应的官方数据源
  4. **第四步**：推荐权威数据源（如交易所、政府机构等）

- **完整示例**：
  用户："智谱的最新招股书"
  1. web_search(query="智谱AI 招股书 IPO 2025")
  2. 从搜索结果发现：智谱已在2025年12月在香港交易所递交招股书
  3. search_sources_by_keywords(keywords=["Hong Kong", "HKEX", "stock exchange"])
  4. 推荐：香港交易所(HKEX)数据源，说明可以在此查看智谱AI的招股书

- ⚠️ 重要约束：
  * 网络搜索**仅用于获取线索**，帮助理解用户需求背景
  * **绝对不能**将搜索结果链接作为最终推荐的数据源
  * 必须基于搜索内容，推荐对应的**权威数据源**


=== 输出格式要求 ===

最终推荐**必须**使用以下Markdown表格格式：

## 推荐数据源

| # | 名称 | 描述 | 权威级别 | URL | API支持 | 访问级别 | JSON文件 |
|---|------|------|----------|-----|---------|----------|----------|
| 1 | 数据源中英文名称 | 简短描述（1-2句话，说明数据内容） | government/international/research等 | 完整URL | ✅/❌ | 免费/注册/付费 | /sources/path/to/file.json |
| 2 | ... | ... | ... | ... | ... | ... | ... |

**表格列说明**：
- **#**: 推荐排名（1-5）
- **名称**: 数据源完整名称（中英文）
- **描述**: 核心数据内容简述，1-2句话，突出最重要的信息
- **权威级别**: authority_level字段值（government, international, market, research, commercial, other）
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

| # | 名称 | 描述 | 权威级别 | URL | API支持 | 访问级别 | JSON文件 |
|---|------|------|----------|-----|---------|----------|----------|
| 1 | People's Bank of China<br>中国人民银行 | 提供M0/M1/M2货币供应量、基准利率、政策利率、市场利率等货币政策数据，覆盖1990-2024年 | government | http://www.pbc.gov.cn | ❌ | 免费开放 | /sources/countries/asia/china/china-pbc.json |
| 2 | National Bureau of Statistics<br>国家统计局 | 提供GDP、投资、消费等宏观经济数据，可用于分析货币政策传导效果，月度/季度更新 | government | http://www.stats.gov.cn | ❌ | 免费开放 | /sources/countries/asia/china/china-nbs.json |

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
很抱歉，在FirstData的当前数据源库中，**未找到专门针对「{用户查询主题}」的直接数据源**。

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


# MCP 会话缓存（简单的内存缓存）
_mcp_session_cache = {}


def _get_mcp_session(mcp_url: str, headers: dict) -> str | None:
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
                "clientInfo": {"name": "firstdata-agent", "version": __version__},
            },
        }

        print("[INFO] Initializing MCP session...")

        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            response = client.post(mcp_url.rstrip("/"), json=init_payload, headers=headers)

            # 从响应头获取 session ID
            session_id = response.headers.get("mcp-session-id")

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
                except (json.JSONDecodeError, KeyError, TypeError):
                    pass

                print("[WARN] No session ID in response")
                return None

    except Exception as e:
        print(f"[ERROR] Failed to initialize MCP session: {e}")
        return None


def tool_web_search(query: str) -> list[dict]:  # noqa: PLR0915
    """
    网络搜索工具实现

    调用外部 HTTP MCP 服务器的 web_search 工具
    使用 MCP SSE (Server-Sent Events) 传输协议
    """
    mcp_url = os.getenv("WEB_SEARCH_MCP_URL")
    mcp_token = os.getenv("WEB_SEARCH_MCP_AUTH_TOKEN")

    if not mcp_url:
        print("[WARN] WEB_SEARCH_MCP_URL not configured, web_search unavailable")
        return [
            {
                "title": "Web Search 配置缺失",
                "snippet": "WEB_SEARCH_MCP_URL 环境变量未配置。请在 .env 文件中添加外部 MCP 服务器配置。",
                "url": "",
                "source": "system",
            }
        ]

    try:
        # MCP SSE 协议要求的 headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
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
            "params": {"name": "web_search", "arguments": {"query": query}},
        }

        print("[INFO] Calling external MCP web_search via JSON-RPC")
        print(f"[INFO] URL: {mcp_url}")
        print(f"[INFO] Query: {query}")

        # 同步 HTTP 调用
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            response = client.post(mcp_url.rstrip("/"), json=payload, headers=headers)

            # 如果返回 400 且提示 session 问题，清除缓存并重试
            if response.status_code == 400:
                try:
                    error_result = response.json()
                    if (
                        "error" in error_result
                        and "session" in error_result["error"].get("message", "").lower()
                    ):
                        print("[WARN] Session expired, retrying with new session...")
                        _mcp_session_cache.pop(mcp_url, None)

                        # 重新获取session并重试
                        session_id = _get_mcp_session(mcp_url, headers)
                        if session_id:
                            headers["mcp-session-id"] = session_id
                            response = client.post(
                                mcp_url.rstrip("/"), json=payload, headers=headers
                            )
                except (json.JSONDecodeError, KeyError, TypeError, httpx.HTTPError):
                    pass

            response.raise_for_status()

            # 检查响应类型
            content_type = response.headers.get("content-type", "")

            # 处理 SSE 响应
            if "text/event-stream" in content_type:
                print("[INFO] Received SSE stream response")
                # 解析 SSE 格式: "event: message\ndata: {json}\n\n"
                lines = response.text.split("\n")
                for line in lines:
                    if line.startswith("data: "):
                        json_data = line[6:]  # 移除 "data: " 前缀
                        try:
                            result = json.loads(json_data)
                            print(
                                f"[INFO] Parsed SSE data: {json.dumps(result, ensure_ascii=False)[:200]}..."
                            )
                            break
                        except json.JSONDecodeError as e:
                            print(f"[WARN] Failed to parse SSE data: {e}")
                            continue
                else:
                    print("[ERROR] No valid SSE data found in response")
                    return [
                        {
                            "title": "解析错误",
                            "snippet": "SSE响应中未找到有效数据",
                            "url": "",
                            "source": "system",
                        }
                    ]
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
                    return [
                        {
                            "title": "MCP 调用错误",
                            "snippet": error.get("message", str(error)),
                            "url": "",
                            "source": "system",
                        }
                    ]

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
                                    return [
                                        {
                                            "title": "Search Results",
                                            "snippet": first_content["text"],
                                            "url": "",
                                            "source": "web_search",
                                        }
                                    ]

                        return content
                    else:
                        # 直接返回结果
                        return rpc_result if isinstance(rpc_result, list) else [rpc_result]

            return [
                {
                    "title": "Unexpected Response",
                    "snippet": str(result),
                    "url": "",
                    "source": "system",
                }
            ]

    except httpx.HTTPError as e:
        print(f"[ERROR] HTTP error calling MCP service: {e}")
        return [
            {
                "title": "搜索服务调用失败",
                "snippet": f"HTTP 错误: {e!s}。请检查 MCP 服务器配置和网络连接。",
                "url": "",
                "source": "system",
            }
        ]
    except Exception as e:
        print(f"[ERROR] Unexpected error calling MCP service: {e}")
        import traceback

        traceback.print_exc()
        return [
            {
                "title": "搜索工具调用失败",
                "snippet": f"未知错误: {e!s}",
                "url": "",
                "source": "system",
            }
        ]


def execute_tool(tool_name: str, tool_input: dict) -> Any:
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


def datasource_search_agent(user_query: str, max_results: int = 5, max_iterations: int = 10) -> str:  # noqa: PLR0915
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
    base_url = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")

    # 日志：显示使用的模型和API配置
    print("\n[Agent] ========== Agent Search Started ==========")
    print(f"[Agent] Model: {model}")
    print(f"[Agent] API Base URL: {base_url}")
    print(f"[Agent] User Query: {user_query}")
    print(f"[Agent] Max Results: {max_results}")
    print(f"[Agent] Max Iterations: {max_iterations}")
    print("[Agent] ===========================================\n")

    # 将 max_results 添加到系统提示中，并填充当前日期
    current_date = datetime.now().strftime("%Y年%m月%d日")
    system_prompt = (
        AGENT_SYSTEM_PROMPT.format(current_date=current_date) + f"\n\n**本次查询限制**: 最多返回 {max_results} 个推荐数据源。"
    )

    messages = [{"role": "user", "content": user_query}]

    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        print(f"\n[Agent] === 第 {iteration} 轮迭代 ===")
        print(f"[Agent] 调用LLM模型: {model}")

        # 调用LLM
        response = client.messages.create(
            model=model, max_tokens=4096, system=system_prompt, tools=AGENT_TOOLS, messages=messages
        )

        # 打印response的内容块
        print(f"[Agent] Response包含 {len(response.content)} 个内容块:")
        for i, block in enumerate(response.content):
            print(f"[Agent]   块{i + 1}: type={block.type}")
            if block.type == "text":
                print(f"[Agent]       text内容: {block.text[:100]}...")
            elif hasattr(block, "name"):
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
            messages.append({"role": "assistant", "content": response.content})

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
                        print("[Agent] ⚠️ web_search由Anthropic API处理，结果将在API响应中返回")
                    else:
                        print(
                            f"[Agent] 工具返回结果: {json.dumps(result, ensure_ascii=False)[:200]}..."
                        )

                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result, ensure_ascii=False),
                        }
                    )

            # 打印所有工具结果
            print(f"\n[Agent] 收集到 {len(tool_results)} 个工具结果:")
            for i, tr in enumerate(tool_results):
                print(f"[Agent]   结果{i + 1}: tool_use_id={tr['tool_use_id']}")
                content = tr["content"]
                # 尝试解析JSON以美化输出
                try:
                    parsed = json.loads(content)
                    print(
                        f"[Agent]       内容: {json.dumps(parsed, ensure_ascii=False, indent=2)[:500]}..."
                    )
                except (json.JSONDecodeError, TypeError):
                    print(f"[Agent]       内容(原始): {content[:500]}...")

            # 添加工具结果
            messages.append({"role": "user", "content": tool_results})
        else:
            # 其他停止原因
            return f"Agent stopped unexpectedly: {response.stop_reason}"

    return "达到最大迭代次数，Agent未能完成任务"


# def datasource_search_agent(user_query: str, max_results: int = 5, max_iterations: int = 10) -> str:
#     """
#     LLM Agent搜索数据源

#     Args:
#         user_query: 用户查询
#         max_results: 返回的最大数据源数量
#         max_iterations: 最大工具调用轮次

#     Returns:
#         Agent的最终推荐结果
#     """
#     # 创建 ChatAnthropic 实例（支持通过 LiteLLM 代理的 Gemini）
#     model_name = os.getenv("QUERY_UNDERSTANDING_MODEL", "gemini-3-flash-preview")
#     base_url = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
#     api_key = os.getenv("ANTHROPIC_AUTH_TOKEN")

#     print(f"[Agent] 初始化模型: {model_name}")
#     print(f"[Agent] Base URL: {base_url}")

#     llm = ChatAnthropic(
#         model=model_name,
#         api_key=api_key,
#         base_url=base_url,
#         max_tokens=4096
#     )

#     # 创建 agent
#     agent = create_agent(
#         model=llm,
#         system_prompt=AGENT_SYSTEM_PROMPT + f"\n\n**本次查询限制**: 最多返回 {max_results} 个推荐数据源。",
#         tools=AGENT_TOOLS
#     )

#     inputs = {"messages": [{"role": "user", "content": user_query}]}

#     response = agent.invoke(inputs, config={"recursion_limit": max_iterations})
#     print(f"[Agent] Final response: {type(response)}")
#     print(f"[Agent] Response keys: {response.keys() if hasattr(response, 'keys') else 'N/A'}")
#     print(f"[Agent] Response preview: {str(response)[:500]}...")

#     return response
