#!/usr/bin/env python3
"""
FirstData MCP Server
提供数据源检索和访问指令生成服务
"""

import json
import os
from typing import Annotated

from config import __version__
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from tools_impl.tool_filter_sources_by_criteria import tool_filter_sources_by_criteria
from tools_impl.tool_get_instructions import tool_datasource_get_instructions
from tools_impl.tool_get_source_details import tool_get_source_details
from tools_impl.tool_list_sources_summary import tool_list_sources_summary
from tools_impl.tool_search_agent import datasource_search_agent
from tools_impl.tool_search_sources_by_keywords import tool_search_sources_by_keywords

# 加载环境变量
load_dotenv()

mcp = FastMCP("firstdata", host="0.0.0.0", port=8001)


@mcp.tool(
    name="datasource_list_sources",
    annotations={
        "title": "浏览数据源列表",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    },
)
async def datasource_list_sources(
    country: str = Field(
        default="",
        description="国家代码或名称，如 CN（中国）, US（美国）, Global（全球）。留空则返回所有国家",
    ),
    domain: str = Field(
        default="",
        description="领域，如 finance（金融）, health（健康）, economics（经济）, energy（能源）。留空则返回所有领域",
    ),
    limit: int = Field(default=50, ge=1, le=200, description="返回数量限制，默认50，最大200"),
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
            country=country if country else None, domain=domain if domain else None, limit=limit
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
        "idempotentHint": True,
    },
)
async def datasource_search_keywords(
    keywords: Annotated[
        list[str], Field(..., description='搜索关键词列表，如 ["GDP", "China", "statistics"]')
    ],
    search_fields: Annotated[
        list[str] | None,
        Field(
            default=None,
            description="搜索范围: name（名称）, description（描述）, tags（标签）, content（数据内容）, all（全部）",
        ),
    ] = None,
    limit: Annotated[int, Field(default=20, ge=1, le=100, description="返回数量限制，默认20")] = 20,
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
    if search_fields is None:
        search_fields = ["all"]

    try:
        results = tool_search_sources_by_keywords(
            keywords=keywords, search_fields=search_fields, limit=limit
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
        "idempotentHint": True,
    },
)
async def datasource_get_details(
    source_ids: Annotated[
        list[str], Field(..., description='数据源ID列表，如 ["china-pbc", "china-nbs"]')
    ],
    fields: Annotated[
        list[str] | None,
        Field(
            default=None,
            description="返回字段: all（全部）, description（描述）, domains（领域）, data_content（数据内容）",
        ),
    ] = None,
) -> str:
    """
    获取指定数据源的完整详细信息

    返回数据源的详细配置，包括描述、领域、数据内容、访问方式、权威级别等。

    **适用场景:**
    - 深入了解某个特定数据源
    - 对比多个候选数据源
    - 获取访问URL、API信息等详细信息

    **示例:**
    - 获取中国人民银行详情: source_ids=["china-pbc"]
    - 对比两个数据源: source_ids=["china-pbc", "china-nbs"]
    - 只获取访问信息: source_ids=["worldbank"], fields=["website", "data_url", "api_url"]

    **返回格式:** JSON字符串，包含完整的数据源配置
    """
    if fields is None:
        fields = ["all"]

    try:
        results = tool_get_source_details(source_ids=source_ids, fields=fields)
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool(
    name="datasource_filter",
    annotations={
        "title": "多条件筛选数据源",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    },
)
async def datasource_filter(
    geographic_scope: str = Field(
        default="", description="地理范围，如 China（中国）, Global（全球）, Asia（亚洲）"
    ),
    domain: str = Field(
        default="", description="领域，如 finance（金融）, health（健康）, economics（经济）"
    ),
    has_api: bool = Field(
        default=None,
        description="是否需要API访问。True=仅返回有API的数据源，False=仅返回无API的，None=不限制",
    ),
    update_frequency: str = Field(
        default="", description="更新频率，如 daily（每日）, monthly（每月）, quarterly（每季度）"
    ),
    authority_level: str = Field(
        default="",
        description="权威级别，如 government（政府）, international（国际组织）, research（研究机构）",
    ),
) -> str:
    """
    按多个条件组合精确筛选数据源

    支持地理范围、领域、API、更新频率、权威级别等多维度筛选，返回同时满足所有条件的数据源。

    **适用场景:**
    - 有明确的多个筛选条件
    - 需要满足特定约束（如必须有API）
    - 精确缩小搜索范围

    **示例:**
    - 有API的中国金融数据: geographic_scope="China", domain="finance", has_api=True
    - 政府机构数据源: authority_level="government"
    - 每日更新的数据源: update_frequency="daily"

    **返回格式:** JSON字符串，包含符合所有条件的数据源列表
    """
    try:
        # 构建筛选参数
        kwargs = {}
        if geographic_scope:
            kwargs["geographic_scope"] = geographic_scope
        if domain:
            kwargs["domain"] = domain
        if has_api is not None:
            kwargs["has_api"] = has_api
        if update_frequency:
            kwargs["update_frequency"] = update_frequency
        if authority_level:
            kwargs["authority_level"] = authority_level

        results = tool_filter_sources_by_criteria(**kwargs)
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool(
    name="datasource_search_llm_agent",
    annotations={
        "title": "LLM Agent智能数据源搜索",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def datasource_search_llm_agent(
    query: str = Field(
        ...,
        description=(
            "搜索指令字符串。请严格遵守以下构造规则：\n"
            "1. **【实体保留】**：如果用户提到了具体的实体（如'智谱AI'、'特斯拉'、'中国人民银行'），必须在Query中保留该名称，严禁泛化为通用类别（如'科技公司'、'央行'）。\n"
            "2. **【关键词提取】**：提取核心意图关键词（如'招股书'、'M2供应量'、'失业率'）。\n"
            "3. **【去指令化】**：移除所有对话式指令词（如'帮我找'、'分析一下'、'解释为什么'）。\n\n"
            "**示例**:\n"
            '  - 输入: "帮我找到智谱的最新的招股书，分析一下他们为什么亏损"\n'
            '  - ✅ 输出: "智谱AI 招股说明书 财务亏损原因 现金流"\n'
            '  - ❌ 错误: "中国科技公司IPO相关信息" (错误原因：实体丢失，过度泛化)\n\n'
            '  - 输入: "美国和欧洲的失业率统计数据"\n'
            '  - ✅ 输出: "美国 欧洲 失业率 统计数据"\n'
        ),
        min_length=2,
        max_length=1000,
    ),
    max_results: int = Field(
        default=5, description="返回的最大数据源数量。范围: 1-20。", ge=1, le=20
    ),
) -> str:
    """
    一个全功能的智能搜索Agent，专用于在数据源仓库中执行复杂的深度检索任务。

    该工具会自动制定搜索策略、扩展关键词并进行多源验证。

    **何时使用本Agent工具:**
    - ✅ **综合研报分析**: 用户的查询并不是简单的关键词匹配，而是需要深入理解需求（如"研究中国近10年的货币政策，特别是M1、M2货币供应量和利率数据"）。
    - ✅ **复杂/跨领域查询**: 涉及多步推理、跨数据源整合（如"气候变化对GDP的影响"）。
    - ✅ **特定实体深度调查**: 针对特定公司或政策的深度挖掘（如"谷歌公司的股价"），而非简单的列表浏览。
    - ✅ **模糊意图澄清**: 当用户输入不够专业，需要Agent智能推断行业术语时。

    **❌ 勿用场景 (请使用基础工具):**
    - 简单的关键词匹配 (-> datasource_search_keywords)
    - 快速浏览列表 (-> datasource_list_sources)
    - 已知ID获取详情 (-> datasource_get_details)

    **工作原理:**
    Agent会进行多轮思考（3-5轮），通过粗筛和精选，最终返回Top 3-5推荐数据源及其详细匹配理由。
    """
    try:
        result = datasource_search_agent(query, max_results)
        return result

    except Exception as e:
        return f"搜索失败: {e!s}"


@mcp.tool(
    name="datasource_get_instructions",
    annotations={
        "title": "获取数据源访问指令",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def datasource_get_instructions(
    source_id: str = Field(
        ..., description="数据源ID，从其他MCP工具获取（如 'hkex-news'、'china-pbc'）"
    ),
    operation: str = Field(
        ..., description="具体操作描述（如 '下载智谱AI的招股书'、'查询M2货币供应量'）"
    ),
    top_k: int = Field(default=3, ge=1, le=5, description="返回指令数量，默认3条"),
) -> str:
    """
    为访问指定数据源生成详细的URL访问操作指令

    该工具结合了数据源元数据和指令生成API，返回具体的网站操作步骤。

    **使用场景**:
    1. 先获取到具体使用什么数据源，通过 datasource_search_llm_agent 等检索方法获取到数据源ID
    2. 再用本工具获取该数据源的具体操作指令

    **示例**:
    - 获取香港交易所下载招股书的指令: source_id="hkex-news", operation="下载智谱AI的招股书"
    - 获取人民银行查询M2的指令: source_id="china-pbc", operation="查询M2货币供应量"

    **返回格式**: JSON字符串，包含访问指令、步骤说明和相关URL
    """
    try:
        result = await tool_datasource_get_instructions(
            source_id=source_id, operation=operation, top_k=top_k
        )
        return result
    except Exception as e:
        return json.dumps(
            {"error": f"获取指令失败: {e!s}", "success": False}, ensure_ascii=False, indent=2
        )


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
                {"error": "Missing or invalid Authorization header"}, status_code=401
            )

        token = auth_header[7:]  # 移除"Bearer "前缀

        if token != expected_key:
            return JSONResponse({"error": "Invalid API key"}, status_code=403)

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
        print(
            "[INFO] Authentication enabled. Clients must provide 'Authorization: Bearer <token>' header."
        )
    else:
        print("[WARN] MCP_API_KEY not set. Running without authentication.")

    print(f"[INFO] FirstData Agent MCP Server v{__version__}")
    print("[INFO] Starting HTTP server on http://0.0.0.0:8001")

    # 包装MCP app with认证中间件
    mcp_app = mcp.streamable_http_app()
    app = Starlette(
        routes=mcp_app.routes,
        middleware=[Middleware(BearerAuthMiddleware)],
        lifespan=mcp_app.router.lifespan_context,
    )

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)


if __name__ == "__main__":
    main()
