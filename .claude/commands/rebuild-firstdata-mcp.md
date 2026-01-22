---
description: 重新构建 FirstData MCP Docker 镜像并重启容器
allowed-tools: Bash(docker:*), Bash(sleep:*), Bash(mkdir:*), TodoWrite, AskUserQuestion
model: sonnet
category: deployment
---

## 功能说明

完整的 MCP (Model Context Protocol) 服务重新构建流程，包括：
1. 清理旧的 Docker 镜像和容器
2. 从 Dockerfile 重新构建镜像
3. 启动新容器并配置环境变量
4. 验证服务健康状态

适用于代码更新后需要重新部署 MCP 服务的场景。

## 执行步骤

### 1. 创建任务跟踪列表

使用 `TodoWrite` 创建以下任务：
- 停止并删除旧容器
- 删除旧镜像
- 执行 Docker build 构建新镜像
- 验证镜像构建成功
- 启动新容器
- 测试 MCP 服务运行状态

### 2. 清理旧的 Docker 资源

```bash
# 停止并删除旧容器（如果存在）
docker stop firstdata-mcp 2>/dev/null || true
docker rm firstdata-mcp 2>/dev/null || true

# 删除旧镜像（所有可能的标签）
docker rmi firstdata-mcp:latest firstdata-mcp-agent:latest 2>/dev/null || true
```

**注意**: 使用 `|| true` 确保即使容器或镜像不存在也不会报错。

### 3. 构建新的 Docker 镜像

```bash
# 在项目根目录执行
docker build -t firstdata-mcp:latest .
```

**构建参数说明**:
- `-t firstdata-mcp:latest`: 设置镜像标签
- `.`: 构建上下文为当前目录（项目根目录）

**Dockerfile 位置**: `/Users/mlamp/project/firstdata/Dockerfile`

**构建超时**: 设置为 300000ms (5分钟) 以应对较慢的网络环境

**构建特点**:
- 使用 Python 3.11-slim 基础镜像
- 使用 `uv` 进行快速依赖安装
- 从 `src/firstdata/` 复制源代码
- 不包含 .env 文件（通过 .dockerignore 排除）

### 4. 验证镜像构建

```bash
docker images | grep firstdata-mcp
```

检查输出确认镜像已成功创建，应显示类似：
```
firstdata-mcp    latest    [IMAGE_ID]    [时间]    [大小]
```

### 5. 启动新容器

```bash
docker run -d \
  --name firstdata-mcp \
  --env-file .env \
  -p 8001:8001 \
  --restart unless-stopped \
  firstdata-mcp:latest
```

**容器配置说明**:
- `--name firstdata-mcp`: 容器名称
- `--env-file .env`: 加载根目录的环境变量文件
- `-p 8001:8001`: 端口映射（宿主机:容器）
- `--restart unless-stopped`: 自动重启策略
- `-d`: 后台运行（detached mode）

**必需的环境变量** (.env 文件中必须包含):
- `ANTHROPIC_AUTH_TOKEN`: Anthropic API 密钥（必需）
- `ANTHROPIC_BASE_URL`: Anthropic API 基础 URL（可选）
- `MCP_API_KEY`: MCP 服务认证密钥（可选，用于客户端认证）
- `WEB_SEARCH_MCP_URL`: 外部 Web Search MCP 服务 URL
- `WEB_SEARCH_TOKEN`: Web Search 服务认证令牌
- `QUERY_UNDERSTANDING_MODEL`: LLM 模型名称（默认: gemini-3-flash-preview）

### 6. 验证服务状态

**步骤 6.1**: 查看容器启动日志
```bash
sleep 3
docker logs firstdata-mcp
```

**期望输出**:
```
[INFO] Authentication enabled. Clients must provide 'Authorization: Bearer <token>' header.
[INFO] FirstData Agent MCP Server v0.1.0
[INFO] Starting HTTP server on http://0.0.0.0:8001
INFO:     Started server process [1]
INFO:     Waiting for application startup.
StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

**步骤 6.2**: 验证环境变量加载
```bash
docker exec firstdata-mcp printenv | grep -E "(ANTHROPIC|MCP_API_KEY|WEB_SEARCH)" | sort
```

**期望输出**:
```
ANTHROPIC_AUTH_TOKEN=sk-...
ANTHROPIC_BASE_URL=https://...
MCP_API_KEY=...
WEB_SEARCH_MCP_URL=https://...
WEB_SEARCH_TOKEN=...
```

**步骤 6.3**: 检查容器运行状态
```bash
docker ps --filter "name=firstdata-mcp" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**步骤 6.4**: 测试健康检查（可选）
```bash
# 等待健康检查启动
sleep 10

# 查看健康状态
docker inspect firstdata-mcp --format='{{.State.Health.Status}}'
```

**注意**: 健康检查基于进程检测，如果显示错误但服务正常运行，可忽略。

### 7. 更新任务状态

在每个步骤完成后，使用 `TodoWrite` 更新对应任务的状态为 `completed`。

## 输出

命令执行完成后，应显示：

```
✅ MCP 服务重新构建完成！

📦 镜像信息:
   - 镜像名称: firstdata-mcp:latest
   - 镜像 ID: [显示实际 ID]
   - 镜像大小: ~300MB

🚀 容器状态:
   - 容器名称: firstdata-mcp
   - 运行状态: Up [时间] (healthy/starting)
   - 端口映射: 0.0.0.0:8001->8001/tcp

📝 服务日志:
   [显示最近日志]

💡 后续操作:
   - 测试 MCP 连接: /mcp
   - 查看日志: docker logs -f firstdata-mcp
   - 停止服务: docker stop firstdata-mcp
   - 重启服务: docker restart firstdata-mcp
```

## 错误处理

### 情况 1: 构建失败

如果 Docker build 失败，检查：
- Dockerfile 语法是否正确
- 依赖包是否可访问（网络问题，检查清华镜像源）
- 构建上下文是否包含必要文件（pyproject.toml, uv.lock, src/）
- uv 安装是否成功

**调试命令**:
```bash
# 查看构建详细输出
docker build -t firstdata-mcp:latest . 2>&1 | tee build.log

# 检查构建上下文内容
docker build -t firstdata-mcp:latest . --progress=plain
```

### 情况 2: 容器启动失败

如果容器无法启动，检查：
- `.env` 文件是否存在于项目根目录
- `.env` 文件中是否包含所有必需的环境变量
- 端口 8001 是否被占用
- `ANTHROPIC_AUTH_TOKEN` 是否配置正确

**调试命令**:
```bash
# 查看详细错误日志
docker logs firstdata-mcp

# 检查端口占用
lsof -i :8001

# 验证 .env 文件内容（隐藏敏感信息）
cat .env | sed 's/=.*/=***/'

# 手动验证环境变量
docker run --rm --env-file .env firstdata-mcp:latest printenv | grep ANTHROPIC
```

### 情况 3: 环境变量未加载

**症状**: 日志显示 `ANTHROPIC_AUTH_TOKEN not found in environment`

**原因**: .env 文件格式问题或包含空行

**解决方案**:
```bash
# 检查 .env 文件是否有空行
cat -A .env

# 确保 .env 文件没有空行，每行格式为 KEY=VALUE
# 正确格式示例:
MCP_API_KEY=your_key_here
ANTHROPIC_AUTH_TOKEN=sk-ant-xxx
ANTHROPIC_BASE_URL=https://api.anthropic.com
```

### 情况 4: 健康检查失败

如果长时间显示 `health: starting` 或 `unhealthy`：
- 检查服务是否正常监听 8001 端口
- 查看日志中是否有错误信息
- 验证 server.py 是否正常启动

**注意**: 由于 python:3.11-slim 不包含 `ps` 命令，健康检查可能显示错误，但不影响服务运行。

## 使用示例

```bash
# 直接执行重新构建
/rebuild-datasource-mcp
```

## 注意事项

1. **数据持久化**: 数据源 JSON 文件打包在镜像中（从 `src/firstdata/sources/`），重启容器不会丢失数据

2. **环境变量安全**:
   - `.env` 文件包含敏感信息（API keys），已通过 `.gitignore` 排除
   - `.env` 文件不会被打包到 Docker 镜像中（通过 `.dockerignore` 排除）
   - 使用 `--env-file` 方式加载，环境变量在 `docker inspect` 中可见

3. **构建时间**:
   - 首次构建可能需要 2-3 分钟（下载依赖）
   - 后续构建利用缓存，通常 30 秒内完成

4. **端口冲突**: 如果 8001 端口被占用，需要先停止占用该端口的服务

5. **网络要求**: 构建过程需要访问：
   - PyPI 镜像源（默认使用清华镜像：https://pypi.tuna.tsinghua.edu.cn/simple）
   - Docker Hub（拉取基础镜像）

6. **项目结构要求**:
   - Dockerfile 必须在项目根目录
   - .env 文件必须在项目根目录
   - 源代码在 `src/firstdata/` 目录
   - pyproject.toml 和 uv.lock 在项目根目录

## 相关命令

- 查看 MCP 服务状态: `docker ps | grep firstdata-mcp`
- 查看实时日志: `docker logs -f firstdata-mcp`
- 停止服务: `docker stop firstdata-mcp`
- 重启服务: `docker restart firstdata-mcp`
- 进入容器调试: `docker exec -it firstdata-mcp bash`
- 查看容器环境变量: `docker exec firstdata-mcp printenv`

## 文件结构参考

```
firstdata/
├── Dockerfile                    # Docker 构建文件（根目录）
├── .env                         # 环境变量配置（根目录，不提交到 Git）
├── .dockerignore                # Docker 忽略文件（排除 .env）
├── pyproject.toml               # Python 项目配置
├── uv.lock                      # uv 依赖锁定文件
└── src/
    └── firstdata/
        ├── mcp/
        │   └── server.py        # MCP 服务器入口
        ├── sources/             # 数据源 JSON 文件
        ├── schemas/             # JSON Schema 定义
        └── utils/               # 工具脚本
```
