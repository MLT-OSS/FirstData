# Use Python 3.11 slim image for minimal size
# FROM python:3.11-slim AS runtime
FROM tbj7-xtiao-tcr1.tencentcloudcr.com/xtiao-release/python:3.11-slim AS runtime

# Environment variables for Python and pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple \
    UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple

WORKDIR /app

# Install uv for faster dependency installation
RUN pip install uv

# Copy pyproject.toml and uv.lock for dependency installation
COPY pyproject.toml uv.lock /app/

# Copy source code (needed for uv to install the package)
COPY src /app/src

# Install dependencies using uv (much faster than pip)
# --no-cache: don't cache downloads
# --system: install to system Python instead of venv
RUN cd /app && uv pip install --system --no-cache .

# Expose MCP HTTP port for agent (8001)
EXPOSE 8001

# Health check - verify the server process is running
# Note: MCP servers don't have standard health endpoints, so we check if the process is alive
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ps aux | grep -v grep | grep server.py || exit 1

# Note: Environment variables are loaded from .env file using python-dotenv
# The .env file should be mounted to /app/.env when running the container
# Example: docker run -v $(pwd)/.env:/app/.env ...

# Default command: start the Agent MCP server
CMD ["python", "/app/src/firstdata/mcp/server.py"]
