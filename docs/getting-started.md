# Getting Started - 开发者快速开始指南

本文档面向开发者，介绍如何在本地运行和开发 FirstData MCP 服务。

## 🚀 快速启动 MCP 服务

### 方法 1：使用自动化脚本（推荐）

**这是最简单的启动方式，适合大多数开发者。**

```bash
# 1. 克隆项目
git clone <repository-url>
cd firstdata

# 2. 创建环境变量文件
cp .env.example .env
# 编辑 .env 文件，填入必要的 API keys

# 3. 运行启动脚本（自动构建镜像并启动容器）
bash ./scripts/rebuild-mcp.sh
```

**脚本会自动完成：**

- ✅ 清理旧容器和镜像
- ✅ 构建最新镜像
- ✅ 启动 MCP 服务容器
- ✅ 显示服务日志

**查看服务状态：**

```bash
# 查看实时日志
docker logs -f firstdata-mcp

# 检查容器状态
docker ps | grep firstdata-mcp
```

---

### 方法 2：手动 Docker 命令

如果你想完全手动控制：

```bash
# 1. 构建镜像
docker build -t firstdata-mcp:latest .

# 2. 启动容器（挂载 .env 文件）
docker run -d \
  --name firstdata-mcp \
  -v "$(pwd)/.env:/app/.env:ro" \
  -p 8001:8001 \
  --restart unless-stopped \
  firstdata-mcp:latest

# 3. 查看日志
docker logs -f firstdata-mcp
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
cd src/firstdata
uv run python -m mcp.server

# 或者使用 uvicorn 直接运行
uv run uvicorn mcp.server:app --host 0.0.0.0 --port 8001
```
