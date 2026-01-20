# Use Python 3.11 slim image for minimal size
FROM python:3.11-slim AS runtime

# Environment variables for Python and pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

# Install runtime dependencies from requirements.txt via Tsinghua mirror
COPY datasource-hub-mcp/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt

# Copy application source
COPY datasource-hub-mcp/server.py /app/server.py

# Copy data sources directory from parent context
COPY sources /app/sources

# Expose MCP HTTP port for agent (8001)
EXPOSE 8001

# Health check - verify the server process is running
# Note: MCP servers don't have standard health endpoints, so we check if the process is alive
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ps aux | grep -v grep | grep server.py || exit 1

# Default command: start the Agent MCP server
CMD ["python", "server.py"]
