# DataSource Hub MCP 服务器

**版本**: 0.1.0
**传输协议**: HTTP (Streamable HTTP)
**框架**: MCP Python SDK (FastMCP)

一个由LLM驱动的智能数据源发现MCP服务器。不同于传统的关键词搜索,该服务器使用Claude Sonnet 4.5自主探索100+精选的权威数据源,理解复杂的自然语言查询,并给出详细的推荐理由。

## 概述

该MCP服务器使AI助手能够从政府机构、国际组织、研究机构和商业提供商的数据源集合中发现和推荐高质量数据源。服务器采用智能Agent架构:

- **理解意图**: 处理多维度的自然语言查询
- **自主探索**: 使用内部工具自主制定搜索策略
- **渐进精炼**: 通过迭代过滤缩小结果范围(粗筛 → 聚焦 → 详细分析)
- **智能推荐**: 返回Top 3-5数据源并附带详细理由

## 架构设计

### Agent架构

服务器实现了**Agent化架构**:

1. **用户查询** → 单个MCP工具 (`datasource_search_llm_agent`)
2. **内部Agent** → 四个专用内部工具用于自主探索
3. **LLM引擎** → Claude Sonnet 4.5编排多步搜索工作流
4. **精选数据** → 100+经过验证的数据源,包含6维度质量评分

### Agent内部工具(不通过MCP暴露)

内部Agent拥有四个专用工具:

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| `list_sources_summary` | 按国家/领域浏览数据源 | "有哪些中国的经济数据?" |
| `search_sources_by_keywords` | 在名称/描述/标签中关键词匹配 | "查找'货币政策'和'M1/M2'" |
| `filter_sources_by_criteria` | 多条件筛选(地理、API、时间范围、质量) | "API访问 + 中国 + 金融 + 10年" |
| `get_source_details` | 获取完整数据源元数据 | 对比最终3-5个候选源 |

## MCP工具

### `datasource_search_llm_agent`

**类型**: 只读、非幂等、开放世界
**用途**: 通过自然语言查询进行智能数据源发现

#### 参数

```typescript
{
  query: string  // 自然语言数据需求描述 (2-1000字符)
               // 示例: "中国近10年货币政策M1M2数据"
               //      "有API访问的全球气候数据"
}
```

#### 返回值

```
string  // Markdown格式的推荐结果,包括:
        // - Top 3-5数据源,按相关性排序
        // - 每个数据源的详细推荐理由
        // - 访问信息和使用指南
        // - 性能统计(搜索耗时、版本)
```

#### 使用示例

**复杂查询**:
```
查询: "我需要研究中国近10年的货币政策,特别是M1、M2货币供应量和利率数据"

Agent工作流:
1. 筛选: 中国 + 金融领域 + 10年时间范围
2. 搜索: 关键词 "货币政策", "M1", "M2", "利率"
3. 详情: 获取候选源的完整元数据
4. 推荐: 中国人民银行、国家统计局

输出: Markdown报告,包含详细推荐
```

**简单查询**:
```
查询: "中国人民银行的数据"

Agent工作流:
1. 直接关键词搜索"中国人民银行"
2. 返回: 单个数据源的完整详情
```

## 安装部署

### 依赖要求

```bash
# Python 3.11+
pip install -r requirements.txt
```

**核心依赖**:
- `mcp>=1.9.2` - MCP Python SDK
- `pydantic>=2.12.3` - 输入验证
- `anthropic>=0.39.0` - Claude API客户端
- `uvicorn>=0.30.0` - HTTP服务器
- `starlette>=0.37.0` - Web框架
- `python-dotenv>=1.0.0` - 环境变量配置

### 环境配置

创建`.env`文件:

```bash
# 必需: Anthropic API密钥
ANTHROPIC_AUTH_TOKEN=sk-ant-xxx

# 可选: 自定义API网关 (默认: https://api.anthropic.com)
ANTHROPIC_BASE_URL=https://api.anthropic.com

# 可选: 模型选择 (默认: claude-sonnet-4-5-20250929)
QUERY_UNDERSTANDING_MODEL=claude-sonnet-4-5-20250929

# 可选: MCP服务器认证 (留空 = 无认证)
MCP_API_KEY=
```

## 部署方式

### 方式一: Docker部署(推荐)

从datasource-hub父目录构建:

```bash
cd /path/to/datasource-hub

# 构建镜像
docker build -f datasource-hub-mcp/Dockerfile -t datasource-hub-mcp-agent:latest .

# 运行容器
docker run -d \
  -p 8001:8001 \
  --env-file datasource-hub-mcp/.env \
  --name datasource-hub-agent \
  datasource-hub-mcp-agent:latest

# 查看日志
docker logs -f datasource-hub-agent

# 停止并删除
docker stop datasource-hub-agent && docker rm datasource-hub-agent
```

### 方式二: 本地运行

```bash
cd datasource-hub-mcp

# 确保.env已配置
python server.py

# 服务器监听 http://0.0.0.0:8001
```

## Claude Desktop集成

添加到Claude Desktop配置文件:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**无认证**:
```json
{
  "mcpServers": {
    "datasource-hub-agent": {
      "type": "http",
      "url": "http://localhost:8001/mcp"
    }
  }
}
```

**带认证**:
```json
{
  "mcpServers": {
    "datasource-hub-agent": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

## 数据源覆盖范围

### 地理覆盖
- **中国**: 人民银行、国家统计局、海关总署等
- **美国**: 劳工统计局、人口普查局、美联储等
- **全球**: 世界银行、IMF、OECD、WHO等
- **区域**: 欧盟、亚太、非洲相关数据源

### 领域覆盖
- **经济**: GDP、贸易、投资、就业
- **金融**: 货币政策、汇率、市场数据
- **健康**: 疾病监测、医疗统计
- **气候**: 温度、排放、环境指标
- **能源**: 生产、消费、价格
- **人口**: 人口、迁移、生命统计

### 质量评估(6个维度)

每个数据源都有1-5星评分:

1. **权威性等级** - 来源可信度和官方地位
2. **方法论透明度** - 数据收集方法的文档化程度
3. **更新及时性** - 更新频率和可靠性
4. **数据完整性** - 覆盖的广度和深度
5. **文档质量** - API文档、元数据、用户指南
6. **引用次数** - 学术和专业领域的使用情况

## 性能特征

| 指标 | 数值 | 说明 |
|------|------|------|
| **首次加载** | 1-2秒 | 加载100+数据源到内存 |
| **Agent搜索** | 3-10秒 | 多次LLM调用,取决于查询复杂度 |
| **Token使用** | 10-30K tokens/查询 | 根据查询复杂度和迭代次数变化 |
| **最大迭代** | 10次 | Agent自我修正限制 |
| **传输协议** | HTTP | 端口8001,支持认证 |

**成本考虑**:
- 每次查询会多次调用Claude Sonnet 4.5
- 复杂查询成本高于简单查找
- 适合需要智能推荐的场景

**使用场景**:
- ✅ 复杂的多条件查询
- ✅ 不确定使用哪个数据源
- ✅ 需要详细的推荐理由
- ❌ 简单的ID查找(直接数据库访问更合适)
- ❌ 高频自动化查询(考虑缓存)

## 安全与认证

### 输入验证
- 所有输入通过Pydantic模型验证
- 查询长度限制(2-1000字符)
- 无命令注入或路径遍历风险

### API认证
- **Anthropic API**: 需要环境变量`ANTHROPIC_AUTH_TOKEN`
- **MCP服务器**: 可选的`MCP_API_KEY`用于Bearer token认证
- Token永不记录或在错误消息中暴露

### 数据隐私
- 仅只读操作
- 除查询文本外不收集PII
- 所有数据源元数据均为公开信息
- 无用户跟踪或分析

## 开发与调试

### 项目结构

```
datasource-hub-mcp/
├── server.py             # 主MCP服务器 + Agent实现
├── requirements.txt      # Python依赖
├── pyproject.toml        # 项目元数据
├── Dockerfile            # Docker容器定义
├── .env.example          # 环境变量模板
├── .env                  # 环境配置(已忽略git)
└── README.md            # 本文件
```

### 调试技巧

```bash
# 查看容器日志
docker logs -f datasource-hub-agent

# 测试API密钥配置
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Token:', os.getenv('ANTHROPIC_AUTH_TOKEN')[:10])"

# 验证数据源文件
cd /path/to/datasource-hub
python -c "import json; from pathlib import Path; print('有效数据源:', len(list(Path('sources').rglob('*.json'))))"

# 代码修改后重新构建
docker stop datasource-hub-agent && docker rm datasource-hub-agent
docker build -f datasource-hub-mcp/Dockerfile -t datasource-hub-mcp-agent:latest .
docker run -d -p 8001:8001 --env-file datasource-hub-mcp/.env --name datasource-hub-agent datasource-hub-mcp-agent:latest
```

### 日志输出

服务器日志输出到stderr(Docker自动捕获):
- `[INFO]` - 服务器启动和配置信息
- `[WARN]` - 缺少可选配置(如无MCP_API_KEY)
- `[Agent]` - 内部工具调用和参数(用于调试Agent行为)

## 扩展服务器

### 添加新数据源

1. 在`sources/`目录创建符合schema的JSON文件
2. 重新构建Docker镜像或重启本地服务器
3. Agent自动加载新数据源

### 自定义Agent行为

编辑`server.py`中的`AGENT_SYSTEM_PROMPT`以:
- 改变搜索策略(如总是优先考虑质量而非相关性)
- 调整输出格式
- 添加特定领域的指令

### 更换LLM模型

更新`.env`文件:
```bash
# 切换到Claude Haiku以获得更快/更便宜的响应
QUERY_UNDERSTANDING_MODEL=claude-3-5-haiku-20241022

# 切换到Opus以获得最高质量
QUERY_UNDERSTANDING_MODEL=claude-opus-4-5-20251101
```

## 常见问题

**Q: 为什么使用Agent而不是简单的关键词搜索?**
A: Agent能理解多维度需求(地理+时间+领域+质量)并提供详细理由,不仅仅是排序列表。

**Q: 可以用于实时应用吗?**
A: 不推荐。3-10秒的响应时间适合人工参与的工作流,不适合高频自动化。

**Q: 如何控制成本?**
A: 每次查询消耗10-30K tokens。仅用于复杂查询,尽可能缓存结果,或考虑切换到Haiku模型。

**Q: 支持中英文以外的语言吗?**
A: 支持,Agent系统提示是中文但处理两种语言。可修改提示以支持其他语言。

**Q: 可以添加自定义数据源吗?**
A: 可以,按照schema在`sources/`目录添加JSON文件。参考现有数据源示例。

**Q: 如果Agent出错怎么办?**
A: Agent有10次迭代限制,会返回部分结果。检查日志查看工具调用详情。

## MCP最佳实践合规性

本服务器遵循MCP协议标准:

- ✅ **服务器命名**: 使用描述性命名模式
- ✅ **工具注解**: 正确的readOnlyHint、destructiveHint、openWorldHint
- ✅ **输入验证**: 带约束的Pydantic模型
- ✅ **类型安全**: 全面的类型提示
- ✅ **错误处理**: 优雅的失败和清晰的消息
- ✅ **文档**: 全面的工具文档字符串
- ✅ **传输协议**: 通过FastMCP支持HTTP/SSE
- ✅ **安全**: 无敏感数据暴露,输入清理

## 许可证

DataSource Hub项目的一部分。

## 技术支持

如有问题或疑问:
- GitHub Issues: [datasource-hub/issues](https://github.com/your-org/datasource-hub/issues)
- 检查日志: `docker logs datasource-hub-agent`
- 环境验证: 确保正确设置`ANTHROPIC_AUTH_TOKEN`

---

**技术栈**:
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - 官方MCP Python SDK
- [Claude AI](https://www.anthropic.com/claude) - Anthropic的Claude AI模型
- [FastMCP](https://github.com/modelcontextprotocol/python-sdk#fastmcp) - 高级MCP服务器框架
