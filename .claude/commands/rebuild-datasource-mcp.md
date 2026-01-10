---
description: 重新构建 DataSource Hub MCP Docker 镜像并重启容器
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
docker stop datasource-hub-agent 2>/dev/null || true
docker rm datasource-hub-agent 2>/dev/null || true

# 删除旧镜像
docker rmi datasource-hub-mcp-agent:latest datasource-hub-mcp:latest 2>/dev/null || true
```

**注意**: 使用 `|| true` 确保即使容器或镜像不存在也不会报错。

### 3. 构建新的 Docker 镜像

```bash
docker build -f datasource-hub-mcp/Dockerfile -t datasource-hub-mcp-agent:latest .
```

**构建参数说明**:
- `-f datasource-hub-mcp/Dockerfile`: 指定 Dockerfile 路径
- `-t datasource-hub-mcp-agent:latest`: 设置镜像标签
- `.`: 构建上下文为当前目录

**构建超时**: 设置为 300000ms (5分钟) 以应对较慢的网络环境

### 4. 验证镜像构建

```bash
docker images | grep datasource-hub-mcp-agent
```

检查输出确认镜像已成功创建。

### 5. 启动新容器

```bash
docker run -d \
  --name datasource-hub-agent \
  --env-file datasource-hub-mcp/.env \
  -p 8001:8001 \
  --restart unless-stopped \
  datasource-hub-mcp-agent:latest
```

**容器配置说明**:
- `--name datasource-hub-agent`: 容器名称
- `--env-file datasource-hub-mcp/.env`: 加载环境变量
- `-p 8001:8001`: 端口映射
- `--restart unless-stopped`: 自动重启策略
- `-d`: 后台运行

### 6. 验证服务状态

**步骤 6.1**: 查看容器日志
```bash
docker logs --tail 20 datasource-hub-agent
```

**期望输出**:
```
[INFO] Authentication enabled. Clients must provide 'Authorization: Bearer <token>' header.
[INFO] DataSource Hub Agent MCP Server v0.1.0
[INFO] Starting HTTP server on http://0.0.0.0:8001
INFO:     Uvicorn running on http://0.0.0.0:8001
```

**步骤 6.2**: 检查容器健康状态
```bash
# 等待健康检查启动
sleep 10

# 查看容器状态
docker ps --filter "name=datasource-hub-agent" --format "table {{.Names}}\t{{.Status}}"
```

**步骤 6.3**: 如果需要详细健康检查信息
```bash
docker inspect datasource-hub-agent --format='{{json .State.Health}}' | python3 -m json.tool
```

**注意**: 如果健康检查显示 `ps: not found` 错误，这是预期的（python:3.11-slim 镜像不包含 ps 命令），但不影响服务运行。

### 7. 更新任务状态

在每个步骤完成后，使用 `TodoWrite` 更新对应任务的状态为 `completed`。

## 输出

命令执行完成后，应显示：

```
✅ MCP 服务重新构建完成！

📦 镜像信息:
   - 镜像名称: datasource-hub-mcp-agent:latest
   - 镜像 ID: [显示实际 ID]

🚀 容器状态:
   - 容器名称: datasource-hub-agent
   - 运行状态: Up [时间] (health: starting/healthy)
   - 端口映射: 0.0.0.0:8001->8001/tcp

📝 服务日志:
   [显示最近 20 行日志]

💡 后续操作:
   - 测试 MCP 连接: /mcp
   - 查看日志: docker logs -f datasource-hub-agent
   - 停止服务: docker stop datasource-hub-agent
```

## 错误处理

### 情况 1: 构建失败

如果 Docker build 失败，检查：
- Dockerfile 语法是否正确
- 依赖包是否可访问（网络问题）
- 构建上下文是否包含必要文件

### 情况 2: 容器启动失败

如果容器无法启动，检查：
- `.env` 文件是否存在且配置正确
- 端口 8001 是否被占用
- 环境变量是否包含必需的认证信息

**调试命令**:
```bash
# 查看详细错误日志
docker logs datasource-hub-agent

# 检查端口占用
lsof -i :8001
```

### 情况 3: 健康检查失败

如果长时间显示 `health: starting` 或 `unhealthy`：
- 检查服务是否正常监听 8001 端口
- 查看日志中是否有错误信息
- 验证环境变量配置（特别是 ANTHROPIC_AUTH_TOKEN）

## 使用示例

```bash
# 直接执行重新构建
/rebuild-datasource-mcp
```

## 注意事项

1. **数据持久化**: 当前配置不包含数据卷挂载，重启容器不会丢失数据源 JSON 文件（它们打包在镜像中）

2. **环境变量安全**: `.env` 文件包含敏感信息（API keys），确保不要提交到 Git

3. **构建时间**: 首次构建可能需要几分钟下载依赖，后续构建会利用缓存加速

4. **端口冲突**: 如果 8001 端口被占用，需要先停止占用该端口的服务

5. **网络要求**: 构建过程需要访问 PyPI 镜像源（默认使用清华镜像）

## 相关命令

- 查看 MCP 服务状态: `docker ps | grep datasource-hub-agent`
- 查看实时日志: `docker logs -f datasource-hub-agent`
- 停止服务: `docker stop datasource-hub-agent`
- 重启服务: `docker restart datasource-hub-agent`
