#!/bin/bash
set -e

# 切换到项目根目录
cd "$(dirname "$0")/.."

CONTAINER_NAME="firstdata-mcp"
IMAGE_NAME="firstdata-mcp:latest"

echo "🔄 开始重建 MCP 服务..."

# 1. 删除旧容器和镜像
echo "📦 清理旧容器和镜像..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true
docker rmi $IMAGE_NAME firstdata-mcp-agent:latest 2>/dev/null || true

# 2. 构建新镜像
echo "🔨 构建新镜像..."
docker build -t $IMAGE_NAME .

# 3. 启动新容器（挂载 .env 文件）
echo "🚀 启动新容器..."
docker run -d \
  --name $CONTAINER_NAME \
  -v "$(pwd)/.env:/app/.env:ro" \
  -p 8001:8001 \
  --restart unless-stopped \
  $IMAGE_NAME

# 4. 验证服务状态
echo "✅ 等待服务启动..."
sleep 3
docker logs $CONTAINER_NAME

echo ""
echo "✅ 重建完成！"
echo "查看日志: docker logs -f $CONTAINER_NAME"
