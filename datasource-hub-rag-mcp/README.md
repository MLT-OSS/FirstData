# DataSource Hub RAG MCP Server

基于 RAG（检索增强生成）的 MCP 服务器，使用 Milvus 向量数据库和 OpenAI Embeddings 提供语义搜索能力。

## 概述

该 MCP 服务器使用向量嵌入和语义相似度来搜索数据源，与基于关键词的搜索相比具有以下优势：

**语义理解能力：**
- ✅ 同义词自动匹配：`"job"` = `"employment"` = `"occupation"`
- ✅ 概念理解：`"economic growth"` 能匹配 `"GDP"`, `"inflation"`, `"trade"`
- ✅ 缩写扩展：`"IMF"` 能匹配 `"International Monetary Fund"`
- ✅ 多语言语义对齐：`"失业率"` 和 `"unemployment rate"` 语义相似

## 技术栈

- **向量数据库**: Milvus (开源、高性能)
- **Embedding 模型**: OpenAI text-embedding-3-small (1536维)
- **相似度度量**: 余弦相似度 (Cosine Similarity)
- **MCP 框架**: FastMCP (Python)

## 前置要求

### 1. Milvus 数据库

**使用 Docker 运行 Milvus (推荐):**

```bash
# 使用 Docker Compose（推荐）
wget https://github.com/milvus-io/milvus/releases/download/v2.4.0/milvus-standalone-docker-compose.yml -O docker-compose.yml
docker-compose up -d

# 或使用单个 Docker 容器
docker run -d \
  --name milvus-standalone \
  -p 19530:19530 \
  -p 9091:9091 \
  -v $(pwd)/volumes/milvus:/var/lib/milvus \
  milvusdb/milvus:latest
```

**验证 Milvus 正在运行:**

```bash
curl http://localhost:9091/healthz
# 应该返回: {"status":"ok"}
```

### 2. OpenAI API Key

获取 OpenAI API key: https://platform.openai.com/api-keys

## 安装

### 1. 安装依赖

```bash
cd datasource-hub-rag-mcp
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，设置你的 OpenAI API key
# OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 构建向量索引

**首次使用时必须运行此步骤：**

```bash
python build_index.py
```

这个脚本会：
1. 加载所有数据源 JSON 文件
2. 为每个数据源生成 OpenAI embeddings
3. 将向量和元数据存储到 Milvus
4. 构建 IVF_FLAT 索引

**预期输出：**
```
======================================================================
DataSource Hub RAG - Index Builder
======================================================================

Loading datasources...
✓ Loaded 100 datasources

Connecting to Milvus at localhost:19530...
✓ Connected to Milvus

Creating collection: datasource_hub
✓ Collection created

Generating embeddings for 100 datasources...
(This may take a few minutes)

  Progress: 10/100 datasources inserted
  Progress: 20/100 datasources inserted
  ...
  Progress: 100/100 datasources inserted

✓ Inserted 100 datasources

Building vector index...
✓ Index built successfully

✓ Collection loaded and ready for search

======================================================================
Index building completed successfully!
======================================================================
```

**重要提示：**
- 首次索引构建可能需要 2-5 分钟（取决于数据源数量和网络速度）
- OpenAI API 调用费用约：100 个数据源 × 200 tokens × $0.02/1M ≈ **$0.0004**（几乎免费）

## 使用方法

### 运行 MCP 服务器

```bash
python server_rag.py
```

### Claude Desktop 配置

#### Stdio 模式（本地）

编辑 Claude Desktop 配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "datasource-hub-rag": {
      "command": "python",
      "args": [
        "/path/to/datasource-hub/datasource-hub-rag-mcp/server_rag.py"
      ],
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}
```

**重要：** 将 `/path/to/datasource-hub` 替换为实际路径。

## 工具说明

### `datasource_rag_search`

使用语义相似度搜索数据源。

**参数：**
- `query` (必需): 搜索查询，支持自然语言
- `limit` (可选): 返回结果数量，默认 5，范围 1-50
- `response_format` (可选): 输出格式，`"markdown"` (默认) 或 `"json"`
- `similarity_threshold` (可选): 最低相似度阈值 (0-1)，默认 0.5

**示例查询：**

```
英文：
- "Find youth unemployment data for China and USA"
- "Where can I get climate change data?"
- "I need financial market data with API access"

中文：
- "寻找中美青年失业率数据源"
- "哪里有气候变化的数据"
- "查找金融市场数据"
```

**返回格式：**

Markdown 格式（默认）：
```markdown
# Data Source Search Results (Semantic Search)

**Query**: climate change data
**Found**: 5 relevant data sources
**Method**: RAG with vector embeddings (Milvus + OpenAI)

---

## 1. NASA Earth Data (NASA 地球数据)

**Similarity**: 94.5%

Comprehensive climate and environmental data from NASA satellites...

### Quality Scores
- **Authority Level**: 5/5 ⭐
- **Average Score**: 4.8/5 ⭐

### Access
- **Primary URL**: https://earthdata.nasa.gov
- **Access Level**: public

...
```

JSON 格式：
```json
{
  "query": "climate change data",
  "method": "RAG (Milvus + OpenAI text-embedding-3-small)",
  "returned_count": 5,
  "similarity_threshold": 0.5,
  "data_sources": [
    {
      "id": "nasa-earthdata",
      "name": {
        "en": "NASA Earth Data",
        "zh": "NASA 地球数据"
      },
      "similarity_score": 0.945,
      ...
    }
  ]
}
```

## 性能对比

### 检索质量（相比关键词匹配）

| 查询类型 | 关键词匹配 | RAG 语义检索 |
|---------|-----------|-------------|
| 精确匹配 ("World Bank") | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 同义词 ("job" vs "employment") | ⭐ | ⭐⭐⭐⭐⭐ |
| 概念查询 ("economic indicators") | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 缩写扩展 ("GDP" → "国内生产总值") | ⭐ | ⭐⭐⭐⭐⭐ |

### 查询速度（100 个数据源）

| 操作 | 时间 | 备注 |
|------|------|------|
| 首次查询 | ~150ms | 包含 Embedding API 调用 |
| 后续查询 | ~120ms | API 调用 + Milvus 搜索 |
| 索引构建 | ~2-5分钟 | 一次性操作 |

## 成本估算

### OpenAI API 成本

**初始索引构建（一次性）：**
- 100 个数据源 × 200 tokens/条 = 20,000 tokens
- 成本: 20,000 / 1,000,000 × $0.02 = **$0.0004**

**运行时查询成本：**
- 每次查询约 20 tokens
- 成本: 20 / 1,000,000 × $0.02 = **$0.0000004**/次
- 月查询 10,000 次: **$0.004**/月

**总成本：** 几乎可忽略不计

## 故障排除

### 问题 1: "Failed to connect to Milvus"

**原因：** Milvus 未运行或连接配置错误

**解决方案：**
```bash
# 检查 Milvus 是否运行
docker ps | grep milvus

# 如果没有运行，启动 Milvus
docker-compose up -d

# 测试连接
curl http://localhost:9091/healthz
```

### 问题 2: "The vector index may not be built yet"

**原因：** 未运行 `build_index.py` 或索引构建失败

**解决方案：**
```bash
python build_index.py
```

### 问题 3: "Failed to generate embedding: Invalid API key"

**原因：** OpenAI API key 未设置或无效

**解决方案：**
```bash
# 检查 .env 文件
cat .env

# 确保包含有效的 API key
OPENAI_API_KEY=sk-...
```

### 问题 4: 搜索结果不相关

**原因：** similarity_threshold 设置过低

**解决方案：**
- 提高 `similarity_threshold` 参数 (默认 0.5)
- 推荐值：0.6-0.7 获得更精确的结果
- 或使用更具体的查询词

## 维护

### 更新索引（添加新数据源后）

```bash
# 重新运行索引构建脚本
python build_index.py
```

这会：
1. 删除旧的 collection
2. 重新扫描所有数据源
3. 生成新的 embeddings
4. 重建索引

### 监控 Milvus

```bash
# 查看 collection 统计
docker exec -it milvus-standalone milvus-cli

# 在 milvus-cli 中：
> show collections
> describe collection datasource_hub
```

## 与原有 MCP 的对比

| 特性 | 原有 MCP (关键词) | RAG MCP (语义) |
|------|------------------|----------------|
| **检索方式** | 关键词匹配 | 向量语义相似度 |
| **同义词支持** | ❌ | ✅ |
| **概念理解** | ❌ | ✅ |
| **查询速度** | 极快 (~2ms) | 较快 (~120ms) |
| **召回率** | 一般 | 优秀 |
| **精确匹配** | 优秀 | 优秀 |
| **成本** | 免费 | 几乎免费 (~$0.004/月) |
| **部署复杂度** | 简单 | 中等 (需要 Milvus) |

## 推荐使用场景

**使用 RAG MCP (语义搜索) 当：**
- ✅ 用户查询包含同义词或概念性词汇
- ✅ 需要理解缩写或专业术语
- ✅ 跨语言语义匹配（中英文混合查询）
- ✅ 探索性搜索，不确定精确关键词

**使用原有 MCP (关键词) 当：**
- ✅ 需要极快的响应速度（<5ms）
- ✅ 精确关键词匹配
- ✅ 无法部署 Milvus 或不想使用 OpenAI API
- ✅ 数据源数量较少（<100）

## 技术架构

```
用户查询 "climate change data"
    ↓
OpenAI Embedding API
    ↓
查询向量 [0.1, -0.3, 0.7, ..., 0.2]  (1536维)
    ↓
Milvus 向量数据库
    ├─ 余弦相似度计算
    ├─ IVF_FLAT 索引加速
    └─ 返回 Top-K 最相似结果
    ↓
混合评分 (70% 语义相似度 + 30% 质量分数)
    ↓
格式化输出 (Markdown/JSON)
```

## 参考资源

- **Milvus 文档**: https://milvus.io/docs
- **OpenAI Embeddings**: https://platform.openai.com/docs/guides/embeddings
- **MCP Protocol**: https://modelcontextprotocol.io

## 许可证

DataSource Hub 项目的一部分。

---

**Sources:**
- [Milvus Quickstart Documentation](https://milvus.io/docs/quickstart.md)
- [PyMilvus GitHub Repository](https://github.com/milvus-io/pymilvus)
- [Milvus Search API Reference](https://milvus.io/api-reference/pymilvus/v2.4.x/ORM/Collection/search.md)
