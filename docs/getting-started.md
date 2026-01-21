# Getting Started - 开发者快速开始指南

本文档面向开发者，介绍如何在本地运行和开发 DataSource Hub MCP 服务。

---

## ⚠️ 重要提醒

> **请注意：** `.env` 文件中的每一行配置之间**不要添加空行**，否则会导致 Docker 容器无法正确读取环境变量！
>
> ❌ **错误示例**（行间有空行）：
> ```bash
> MCP_API_KEY=xxx
>
> ANTHROPIC_API_KEY=yyy
> ```
>
> ✅ **正确示例**（紧凑格式）：
> ```bash
> MCP_API_KEY=xxx
> ANTHROPIC_API_KEY=yyy
> INSTRUCTION_API_URL=https://example.com
> ```

---

## 📋 前置要求

- Docker 20.10+
- Git
- （可选）Python 3.12+ 和 uv（用于本地开发）

---

## 🚀 快速启动 MCP 服务

### 方法 1：使用自动化脚本（推荐）

**这是最简单的启动方式，适合大多数开发者。**

```bash
# 1. 克隆项目
git clone <repository-url>
cd datasource-hub

# 2. 创建环境变量文件
cp .env.example .env
# 编辑 .env 文件，填入必要的 API keys

# 3. 运行启动脚本（自动构建镜像并启动容器）
./scripts/rebuild-mcp.sh
```

**脚本会自动完成：**
- ✅ 清理旧容器和镜像
- ✅ 构建最新镜像
- ✅ 启动 MCP 服务容器
- ✅ 显示服务日志

**查看服务状态：**
```bash
# 查看实时日志
docker logs -f datasource-hub-mcp

# 检查容器状态
docker ps | grep datasource-hub-mcp
```

---

### 方法 2：手动 Docker 命令

如果你想完全手动控制：

```bash
# 1. 构建镜像
docker build -t datasource-hub-mcp:latest .

# 2. 启动容器
docker run -d \
  --name datasource-hub-mcp \
  --env-file .env \
  -p 8001:8001 \
  --restart unless-stopped \
  datasource-hub-mcp:latest

# 3. 查看日志
docker logs -f datasource-hub-mcp
```

---

## 🧪 本地开发模式（无 Docker）

如果你想在本地直接运行 Python 代码进行开发：

```bash
# 1. 安装 uv（如果还没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 安装依赖
uv sync

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 4. 运行 MCP 服务
cd src/datasource-hub
uv run python -m mcp.server

# 或者使用 uvicorn 直接运行
uv run uvicorn mcp.server:app --host 0.0.0.0 --port 8001
```

---

## 🔧 环境变量配置

`.env` 文件中的关键配置项：

```bash
# MCP Server 认证（可选）
MCP_API_KEY=your-secret-key-here

# Anthropic API（用于 LLM Agent 搜索）
ANTHROPIC_API_KEY=sk-ant-xxx

# 指令生成 API（可选，用于 get_instructions 工具）
INSTRUCTION_API_URL=https://mingjing.mininglamp.com/api/mano-plan/instruction/v1

# Web 搜索 MCP（可选，用于 Agent 的网络搜索）
WEB_SEARCH_MCP_URL=http://localhost:8002/mcp
WEB_SEARCH_MCP_KEY=your-web-search-key
```
---