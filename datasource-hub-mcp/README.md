# DataSource Hub MCP 服务器

一个模型上下文协议（MCP）服务器，为 DataSource Hub 仓库提供智能搜索能力。

## 概述

该 MCP 服务器使 AI 助手能够从精选的权威数据源集合中搜索和发现数据源，包括政府机构、国际组织、研究机构和商业提供商。

## 功能特性

### 工具：`datasource_search_sources`

基于自然语言查询搜索相关数据源。

**能力：**
- 跨名称、描述、标签、领域和内容的智能相关性评分
- 为每个数据源提供 6 维质量评估
- 支持 Markdown（人类可读）和 JSON（机器可读）输出格式
- 分页支持（每次查询 1-50 条结果）
- 自动响应截断以防止上下文过载

**搜索覆盖范围：**
- 数据源名称（中英文）
- 描述和文档
- 标签和关键词
- 主题领域（经济、健康、环境等）
- 数据内容类别
- 组织名称

**质量维度：**
- 权威性等级（1-5 星）
- 方法论透明度（1-5 星）
- 更新及时性（1-5 星）
- 数据完整性（1-5 星）
- 文档质量（1-5 星）
- 引用次数（1-5 星）

## 安装

1. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 运行服务器

#### 选项 1：Stdio 模式（本地集成）

```bash
python server_stdio.py
```

#### 选项 2：HTTP 模式（网络/Docker 部署）

```bash
python server_http.py
# 服务器将监听 http://0.0.0.0:8000/mcp
```

或使用 Docker：

```bash
# 重要：从父目录（datasource-hub）构建以包含 sources 目录
cd /path/to/datasource-hub
docker build -f datasource-hub-mcp/Dockerfile -t datasource-hub-mcp:latest .

# 运行容器
docker run -d -p 8000:8000 --name datasource-hub-mcp datasource-hub-mcp:latest

# 使用认证（推荐用于生产环境）
docker run -d -p 8000:8000 --env-file datasource-hub-mcp/.env --name datasource-hub-mcp datasource-hub-mcp:latest
```

### Claude Desktop 配置

#### Stdio 模式（本地）

添加到 Claude Desktop 配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "datasource-hub": {
      "command": "python",
      "args": ["/path/to/datasource-hub/datasource-hub-mcp/server_stdio.py"]
    }
  }
}
```

#### HTTP 模式（网络/Docker）

**无认证（本地开发）：**

```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

**使用 Bearer Token 认证（生产环境）：**

```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8000/mcp",
      "headers": {
        "Authorization": "Bearer your_secret_api_key_here"
      }
    }
  }
}
```

> **注意**：将 `your_secret_api_key_here` 替换为你在 `.env` 文件中设置的 `MCP_API_KEY` 值。

### 查询示例

1. **就业统计**：
   - 查询："youth unemployment China USA"
   - 找到：来自国家统计局和国际组织的劳动力统计数据

2. **气候数据**：
   - 查询："climate change temperature data"
   - 找到：来自 NASA、NOAA 和气候研究中心的环境数据集

3. **金融市场**：
   - 查询："stock market financial data API"
   - 找到：提供 API 访问的市场数据提供商

4. **人口统计**：
   - 查询："population demographics census"
   - 找到：人口普查数据和人口统计来源

## 输出格式

### Markdown 格式（默认）

人类可读格式，包含：
- 排名的数据源列表
- 带星级评分的质量分数
- 访问信息和 URL
- 覆盖详情（地理、时间、领域）
- JSON 元数据文件的直接链接
- 相关标签

### JSON 格式

机器可读的结构化数据，包含：
- 所有关键元数据字段
- 质量分数和计算平均值
- 每个结果的相关性分数
- 用于程序化访问的文件路径

## 开发

### 项目结构

```
datasource-hub-mcp/
├── server_stdio.py     # Stdio 模式 MCP 服务器
├── server_http.py      # HTTP 模式 MCP 服务器
├── README.md           # 本文件
├── requirements.txt    # Python 依赖
├── pyproject.toml      # 项目配置
├── Dockerfile          # Docker 部署
├── .env.example        # 环境变量模板
└── test/               # 测试文件
    ├── test_server.py  # 综合测试套件
    └── README.md       # 测试文档
```

### 核心函数

- `_load_all_datasources()`：从仓库加载所有 JSON 文件
- `_calculate_relevance_score()`：基于查询匹配为数据源评分
- `_calculate_quality_score()`：计算平均质量评级
- `_format_datasource_markdown()`：格式化输出供人类阅读
- `_format_datasource_json()`：格式化输出供程序化使用

## 技术细节

- **框架**：MCP Python SDK with FastMCP
- **输入验证**：Pydantic v2 模型
- **字符限制**：25,000 字符（超出时自动截断）
- **异步/等待**：完全异步支持以提高可扩展性
- **传输模式**：
  - **Stdio** (`server_stdio.py`)：适合本地集成 Claude Desktop
  - **HTTP** (`server_http.py`)：可流式 HTTP 模式，用于网络部署、Docker 和远程访问
- **HTTP 服务器**：Uvicorn + Starlette，支持 Bearer token 认证
- **认证**：通过 `MCP_API_KEY` 环境变量可选 Bearer token 认证

## 环境变量

在 HTTP 模式下运行时，你可以配置以下环境变量（参见 `.env.example`）：

- **`MCP_API_KEY`**（可选）：用于 Bearer token 认证的 API 密钥。如果设置，客户端必须提供 `Authorization: Bearer <token>` 标头。留空以禁用认证（本地开发）。

## 许可证

DataSource Hub 项目的一部分。
