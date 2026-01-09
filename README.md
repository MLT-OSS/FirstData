# DataSource Hub 🌐

**全球最全面、最权威、最结构化的开源数据源知识库**

**The World's Most Comprehensive, Authoritative, and Structured Open Data Source Repository**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![数据源数量](https://img.shields.io/badge/数据源-126%2F950+-blue.svg)](tasks/README.md)
[![完成进度](https://img.shields.io/badge/进度-13%25-yellow.svg)](ROADMAP.md)
[![权威性](https://img.shields.io/badge/权威性-政府与国际组织优先-brightgreen.svg)](#)
[![MCP服务器](https://img.shields.io/badge/MCP-AI智能搜索-purple.svg)](datasource-hub-mcp/)

---

## 🎯 为什么选择 DataSource Hub?

### AI时代的事实防线：从"信息过载"到"真实稀缺"

在生成式 AI 重新塑造互联网的今天，**"信息"变得空前充沛，而"真实"正在变得稀缺**。

当噪音、拼贴与幻觉成为默认背景，**可信的一手证据（Primary Sources）不再只是参考资料，而是整个智能体系的地基**。

### 我们的使命：构建AI时代的可信底座

本项目旨在构建一个**面向全球的、权威的、结构化的 Primary Sources 知识库**。

我们系统性发掘并聚合跨领域高可信信源——覆盖科研学术、政务公开、法律法规、公司披露与财报、标准规范与行业权威资料等——**将分散、非标、难复用的原始内容，转化为可追溯、可验证、可引用的"核心事实（Core Facts）"**，并保留完整证据链与版本历史，确保每一条结论都能"回到原文"。

### 这是一道面向大模型时代的"事实防线"

✅ **为模型提供抗幻觉、抗投毒的可信底座**
   - 计划覆盖950+权威数据源（来源均为中外政府部门、国际组织、学术机构、行业权威协会）
   - 100%的URL验证，确保链接可用

✅ **为 Deep Research 提供可计算、可复查的证据链闭环**
   - 结构化元数据体系，包含完整访问路径
   - 支持编程访问，实现自动化证据追溯

✅ **让 AI 从"模糊概括二手信息"升级为"基于原文证据的严谨推理与引用"**
   - MCP智能Agent理解复杂查询，精准推荐权威数据源
   - 提供直达原始数据的完整路径（URL、API、下载方式）
   - 附带使用案例和引用示例，确保正确使用

> **In the GenAI era, Clean Data > Big Model.**
>
> **让每一次深度思考，都建立在可以被验证的事实之上。**

---

## 🚀 核心优势

| 特性 | 我们的独特之处 | AI时代的价值 |
|------|---------------|-------------|
| 🇨🇳 **深度覆盖中国数据源** | **全球独家**：规划收录488+中国政府数据源，涵盖多个核心领域 | 填补全球数据源目录中的中国空白，为跨国研究提供可信中国数据 |
| 📊 **结构化元数据体系** | 完整元数据标准（访问URL、API接口、权威等级、更新频率、数据内容等），不只是链接 | 机器可读、可编程访问，支持自动化证据链构建 |
| ⭐ **权威等级分类** | 政府、国际组织、研究机构、市场、商业等六类权威等级 | 科学评估数据源可信度，为AI提供质量过滤依据 |
| 🤖 **AI智能搜索** | 基于LLM驱动的数据源查询Agent，理解复杂多维度查询 | 自然语言即可获取权威数据源，无需人工筛选 |
| 🔌 **MCP协议集成** | 提供标准MCP Server，可集成到Claude Desktop、Cline等AI应用 | 让任何AI应用都能访问权威数据源知识库 |
| 🌍 **中英双语支持** | 所有元数据提供中英文版本 | 连接全球数据生态，打破语言壁垒 |
| 🔍 **100%验证** | 每个URL经过测试，每个数据源有完整文档，每个权威等级有依据 | 确保数据源真实可用，避免断链和幻觉引用 |

---

## 💡 使用场景：在AI时代避免幻觉，基于可信数据进行推理

### 案例1：研究人员 - 发展中国家经济数据 📚

**场景**：
> "我需要发展中国家的GDP数据用于经济增长研究"

**传统方式的问题**：
- ❌ Google搜索充斥着二手报道、博客文章、过时链接
- ❌ 不确定数据来源的权威性和方法论
- ❌ 花费数小时导航机构网站，仍可能找错数据

**使用 DataSource Hub + MCP Agent：**

1. 🔍 **自然语言提问**："发展中国家GDP数据，需要有API访问"
2. 🎯 **Agent自动筛选**：世界银行、IMF、区域开发银行
3. 📊 **对比权威等级**：国际组织、政府机构等权威性分类

**返回结果：**
```
📋 推荐数据源：

1. 世界银行 World Development Indicators
   - API：支持（完整文档）
   - 覆盖范围：217个国家和地区
   - 时间范围：1960年至今
   - 权威等级：international（国际组织）
   - 证据链：世界银行官方 → 一手数据 → 可追溯

2. IMF World Economic Outlook
   - API：支持
   - 覆盖范围：全球194个经济体
   - 更新频率：季度
   - 权威等级：international（国际组织）
```

**价值**：
- ✅ 从"不确定的搜索"到"基于权威证据的研究"
- ✅ 节省数小时筛选时间
- ✅ 避免使用错误数据源导致研究结论偏差

---

### 案例2：数据分析师 - 中国货币政策数据 💰

**场景**：
> "我需要中国近10年的M1、M2货币供应量和利率数据"

**传统方式的问题**：
- ❌ AI助手可能给出过时链接或二手网站
- ❌ 不清楚数据更新频率和历史覆盖范围
- ❌ 缺乏API访问信息，无法自动化获取

**MCP Agent推荐数据源的工作流程：**

1. 🔍 **识别关键词**：中国 + 货币政策 + M1/M2 + 10年时间范围
2. 🎯 **筛选条件**：国家=CN + 领域=金融 + 时间覆盖≥10年
3. 📊 **推荐Top数据源**（附带证据链）

**返回结果：**
```
📋 推荐数据源：

1. 中国人民银行 (PBC)
   - 数据门户：http://www.pbc.gov.cn/diaochatongjisi/
   - API文档：有官方接口
   - 更新频率：月度
   - 历史覆盖：1990年至今
   - 权威等级：government（政府机构）
   - 证据链：中国央行官方 → 一手数据 → 可追溯

   📈 可获取数据：
   - M0、M1、M2货币供应量（月度）
   - 存贷款基准利率
   - 银行间同业拆借利率
```

**价值**：
- ✅ **抗幻觉**：确保数据来自官方权威机构
- ✅ **可计算**：提供API访问，支持自动化数据获取
- ✅ **可复查**：完整元数据，任何人都可验证数据来源

---

### 案例3：AI应用开发者 - 上市公司披露文件 📊

**场景**：
> "我的AI助手需要查找某家公司的招股说明书和财务披露信息，在哪里能找到官方权威版本？"

**如果使用普通AI助手的问题**：
- ❌ 可能给出过时或错误的链接
- ❌ 可能推荐二手新闻网站，而非官方来源
- ❌ 无法确保数据的权威性和完整性
- ❌ **幻觉风险**：LLM可能编造数据源或统计数字

**使用 DataSource Hub MCP Agent：**

1. 🔍 **理解需求**：企业披露文件 + 招股说明书 + 官方来源
2. 🎯 **推荐权威数据源**（不是新闻链接！）：
   - **证券交易所** - 上市公司官方披露平台
   - **证券监管机构** - 政府监管备案信息

**返回结果：**
```
📋 推荐数据源：

1. 香港交易所 (HKEX)
   - 访问地址：https://www.hkexnews.hk
   - 文档类型：招股说明书、年报、公告
   - 权威等级：market（市场机构）
   - 证据链：官方披露文件 → 可直接引用

2. 中国证监会 (CSRC)
   - 访问地址：http://www.csrc.gov.cn
   - 境外上市备案信息查询
   - 权威等级：government（政府机构）
```

**集成到你的AI应用：**
1. **集成MCP Server**到你的AI应用
2. **自动调用**权威数据源搜索工具
3. **返回结果**附带完整元数据和权威等级标识
4. **用户可验证**：提供原始数据链接，支持"回到原文"

**价值**：
- ✅ **避免幻觉**：提供官方权威来源，不是AI编造
- ✅ **可验证**：提供直达链接，用户可"回到原文"
- ✅ **完整证据链**：从查询 → 权威数据源 → 原始文件
- ✅ **提升应用可信度**：从"AI幻觉"到"基于证据的AI推理"

---

### 案例4：政策制定者 - 全球气候数据 🌍

**场景**：
> "我需要权威的气候数据来支持政策决策，要有API访问的全球数据"

**风险**：
- ❌ 使用不可靠数据源可能导致政策失误
- ❌ 缺乏方法论透明度，无法评估数据质量
- ❌ 二手引用缺乏原始证据链

**MCP Agent工作流程：**

1. 🔍 **多维度筛选**：地理范围=全球 + 领域=气候 + 有API + 高权威性
2. 🎯 **推荐符合条件的数据源**
3. 📊 **按权威等级排序**（优先推荐政府和国际组织）
4. 📋 **提供完整证据链**

**返回结果：**
```
📋 推荐数据源：

1. NASA Earthdata
   - 覆盖范围：全球
   - API：支持（完整文档）
   - 数据类型：卫星观测、气候模型
   - 权威等级：government（政府机构）
   - 更新频率：实时/日度
   - 证据链：NASA官方 → 卫星数据 → 可验证

2. NOAA Climate Data Online
   - 覆盖范围：全球
   - API：支持
   - 更新频率：实时/日度
   - 权威等级：government（政府机构）
   - 证据链：美国政府 → 气象监测 → 可追溯
```

**使用 DataSource Hub：**
- 按 `domains: ["climate"]` 和 `authority_level: "government"` 筛选
- 所有数据源都有：
  - 政府官方背书
  - 严格的方法论文档
  - 完整的元数据和权威性标识
  - 可追溯的证据链

**价值**：
- ✅ **证据链闭环**：从查询 → 推荐 → 原始数据 → 完整可追溯
- ✅ **方法论透明**：明确数据收集方法和质量标准
- ✅ **可复现研究**：其他研究者可基于相同数据源验证结论
- ✅ **降低政策风险**：从"不确定的决策依据"到"可验证的权威证据"

---

### ✨ MCP Agent的核心优势：构建AI时代的可信底座

- 🧠 **理解复杂查询**：地理+时间+领域+权威性等多维度需求
- 🎯 **智能推荐**：Top 3-5最相关数据源，附带详细理由
- 📊 **权威性保证**：所有推荐都标注权威等级（政府/国际组织/研究/市场等）
- 🔗 **即用信息**：直接提供访问URL、API文档、数据示例
- ✅ **证据链完整**：从查询到原始数据，每一步都可追溯
- 🌐 **实时信息增强**：通过web search获取最新动态（仅作时效信息补充）

---

## 🚀 快速开始

### 推荐方式：使用MCP智能搜索 🤖

**DataSource Hub 提供检索数据源的MCP，其中使用Agent检索你最需要的可信权威数据源。**

支持多个平台：Claude Desktop、Cline (VS Code)、Zed、Cursor 等所有兼容 MCP 协议的 AI 应用。

---

#### 配置指南：根据你使用的平台选择

> **📝 重要提示**
>
> **申请 API Key（必需）**：在配置 MCP 服务器之前，请先访问 [https://always1172.github.io/](https://always1172.github.io/) 申请免费的 API key。所有配置中的 `your_mcp_api_key_here` 需要替换为你申请到的 API key。

---

<details>
<summary><b>Claude Desktop</b></summary>

**手动 JSON 配置**

1. **找到配置文件**：
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **添加配置**：
   ```json
   {
     "mcpServers": {
       "datasource-hub": {
         "type": "http",
         "url": "http://localhost:8001/mcp",
         "headers": {
           "Authorization": "Bearer your_mcp_api_key_here"
         }
       }
     }
   }
   ```

3. **重启 Claude Desktop** 使配置生效

</details>

<details>
<summary><b>Cline (VS Code 扩展)</b></summary>

1. **打开 Cline MCP 设置**：
   - 在 VS Code 中打开 Cline
   - 点击设置图标 → **Advanced MCP settings**
   - 或直接编辑 `cline_mcp_settings.json`

2. **添加配置**：
   ```json
   {
     "mcpServers": {
       "datasource-hub": {
         "type": "http",
         "url": "http://localhost:8001/mcp",
         "headers": {
           "Authorization": "Bearer your_mcp_api_key_here"
         },
         "disabled": false,
         "autoApprove": [
           "datasource_list_sources",
           "datasource_search_keywords"
         ]
       }
     }
   }
   ```

   > **提示**：`autoApprove` 字段可以让常用的只读工具自动执行，无需每次确认。

3. **保存配置**后，Cline 会自动加载 MCP 服务器

参考：[Cline MCP 配置文档](https://docs.cline.bot/mcp/configuring-mcp-servers)

</details>

<details>
<summary><b>Zed 编辑器</b></summary>

1. **创建配置文件**：
   - 在项目根目录创建 `.zed/settings.json`
   - 或使用全局配置：`~/.config/zed/settings.json`

2. **添加配置**：
   ```json
   {
     "context_servers": {
       "datasource-hub": {
         "type": "http",
         "url": "http://localhost:8001/mcp",
         "headers": {
           "Authorization": "Bearer your_mcp_api_key_here"
         },
         "enabled": true
       }
     }
   }
   ```

   > **注意**：Zed 使用 `context_servers` 而不是 `mcpServers`

3. **重新加载 Zed** 或重启项目以应用配置

</details>

<details>
<summary><b>Cursor 编辑器</b></summary>

1. **打开 Cursor 设置**：
   - `Cmd/Ctrl + Shift + P` → 搜索 "MCP Settings"
   - 或进入 `Cursor Settings` → `MCP` → `New MCP Server`

2. **添加配置**：
   ```json
   {
     "mcpServers": {
       "datasource-hub": {
         "type": "http",
         "url": "http://localhost:8001/mcp",
         "headers": {
           "Authorization": "Bearer your_mcp_api_key_here"
         }
       }
     }
   }
   ```

3. **重启 Cursor** 以加载 MCP 服务器

</details>

<details>
<summary><b>Docker 部署（生产环境推荐）</b></summary>

如果你想部署自己的 MCP 服务器实例：

```bash
# 拉取镜像
docker pull datasource-hub/mcp-server:latest

# 运行服务器
docker run -d \
  -p 8001:8001 \
  -e DATASOURCE_HUB_API_KEY=your_secret_key \
  --name datasource-hub-mcp \
  datasource-hub/mcp-server:latest

# 然后在客户端使用 HTTP 配置
```

使用 HTTP 方式的配置（所有平台通用）：
```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_secret_key"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Copilot / VS Code</b></summary>

**推荐方式：HTTP 服务器**

1. 参考 [VS Code MCP 配置指南](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server)

2. 添加配置到 VS Code MCP 设置：
   ```json
   {
     "mcpServers": {
       "datasource-hub": {
         "type": "http",
         "url": "http://localhost:8001/mcp",
         "headers": {
           "Authorization": "Bearer your_mcp_api_key_here"
         }
       }
     }
   }
   ```

**使用 VS Code CLI：**
```bash
code --add-mcp '{"name":"datasource-hub","type":"http","url":"http://localhost:8001/mcp","headers":{"Authorization":"Bearer your_mcp_api_key_here"}}'
```

</details>

<details>
<summary><b>Copilot CLI</b></summary>

使用 HTTP 服务器方式连接：

```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Windsurf</b></summary>

1. **打开 Windsurf MCP 配置**：
   - 参考 [Windsurf MCP 配置指南](https://docs.windsurf.com/windsurf/cascade/mcp#mcp-config-json)

2. **添加配置**：
   ```json
   {
     "mcpServers": {
       "datasource-hub": {
         "type": "http",
         "url": "http://localhost:8001/mcp",
         "headers": {
           "Authorization": "Bearer your_mcp_api_key_here"
         }
       }
     }
   }
   ```

</details>

<details>
<summary><b>JetBrains AI Assistant & Junie</b></summary>

1. **打开 JetBrains IDE 设置**：
   - 进入 `Settings | Tools | AI Assistant | Model Context Protocol (MCP)`
   - 或 `Settings | Tools | Junie | MCP Settings`

2. **点击 `Add` 并添加以下配置**：
   ```json
   {
     "mcpServers": {
       "datasource-hub": {
         "type": "http",
         "url": "http://localhost:8001/mcp",
         "headers": {
           "Authorization": "Bearer your_mcp_api_key_here"
         }
       }
     }
   }
   ```

</details>

<details>
<summary><b>Warp Terminal</b></summary>

1. **打开 Warp 设置**：
   - 进入 `Settings | AI | Manage MCP Servers`

2. **点击 `+ Add` 添加 MCP 服务器**：
   ```json
   {
     "mcpServers": {
       "datasource-hub": {
         "type": "http",
         "url": "http://localhost:8001/mcp",
         "headers": {
           "Authorization": "Bearer your_mcp_api_key_here"
         }
       }
     }
   }
   ```

参考：[Warp MCP 配置文档](https://docs.warp.dev/knowledge-and-collaboration/mcp#adding-an-mcp-server)

</details>

<details>
<summary><b>Gemini CLI</b></summary>

参考 [Gemini CLI MCP 配置指南](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md)，使用以下配置：

```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Gemini Code Assist</b></summary>

参考 [Gemini Code Assist MCP 配置指南](https://cloud.google.com/gemini/docs/codeassist/use-agentic-chat-pair-programmer#configure-mcp-servers)，使用以下配置：

```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Factory CLI (Droid)</b></summary>

参考 [Factory CLI MCP 配置文档](https://docs.factory.ai/cli/configuration/mcp)，使用以下配置：

```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Qoder & Qoder CLI</b></summary>

1. 打开 **Qoder Settings**
2. 进入 `MCP Server` → `+ Add`
3. 添加以下配置：
   ```json
   {
     "mcpServers": {
       "datasource-hub": {
         "type": "http",
         "url": "http://localhost:8001/mcp",
         "headers": {
           "Authorization": "Bearer your_mcp_api_key_here"
         }
       }
     }
   }
   ```

参考：[Qoder MCP 配置文档](https://docs.qoder.com/user-guide/chat/model-context-protocol)

</details>

<details>
<summary><b>Kiro</b></summary>

**方式一：通过 Kiro Settings**
1. 打开 **Kiro Settings**
2. 进入 `Configure MCP` → `Open Workspace or User MCP Config`

**方式二：通过 Activity Bar**
1. 从 IDE **Activity Bar** 选择 `Kiro`
2. 进入 `MCP Servers` → `Click Open MCP Config`

**配置内容：**
```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

</details>

<details>
<summary><b>OpenCode</b></summary>

1. **创建或编辑配置文件**：
   - 路径：`~/.config/opencode/opencode.json`
   - 如果文件不存在，请创建它

2. **添加以下配置**：
   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "mcpServers": {
       "datasource-hub": {
         "type": "http",
         "url": "http://localhost:8001/mcp",
         "headers": {
           "Authorization": "Bearer your_mcp_api_key_here"
         }
       }
     }
   }
   ```

参考：[OpenCode MCP 配置文档](https://opencode.ai/docs/mcp-servers)

</details>

<details>
<summary><b>Visual Studio</b></summary>

参考 Visual Studio MCP 配置文档，使用以下配置：

```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Codex</b></summary>

参考 [Codex MCP 配置指南](https://github.com/openai/codex/blob/main/docs/advanced.md#model-context-protocol-mcp)，使用以下配置：

```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Amp</b></summary>

参考 [Amp MCP 配置文档](https://ampcode.com/manual#mcp)，使用以下配置：

```json
{
  "mcpServers": {
    "datasource-hub": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

</details>

---

#### 使用说明

**配置完成后**，你可以在支持 MCP 的 AI 平台中直接用自然语言提问：

**示例提问**：
- "帮我找到中国人民银行的M2货币供应量数据源"
- "我需要有API访问的全球气候数据，推荐权威来源"
- "查找香港交易所的上市公司披露信息"
- "发展中国家的GDP数据在哪里可以找到？"

检索 Agent 会为你查找并推荐最权威的数据源。


<!-- **📖 完整MCP使用指南和部署说明：** [datasource-hub-mcp/README.md](datasource-hub-mcp/README.md) -->

---

### 其他使用方式

#### 方式一：直接浏览仓库

```bash
# 克隆仓库
git clone https://code.mlamp.cn/0003432/datasource-hub.git
cd datasource-hub

# 按类别浏览
ls sources/china/          # 中国政府数据
ls sources/international/  # 国际组织数据
ls sources/academic/       # 学术机构数据
ls sources/sectors/        # 行业特定数据

# 查看数据源详情
cat sources/china/finance/banking/pbc.json | jq
```

#### 方式二：编程访问

```python
import json
from pathlib import Path

# 加载所有数据源
def load_all_sources():
    sources = []
    for json_file in Path('sources').rglob('*.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            sources.append(json.load(f))
    return sources

# 按条件查找数据源
def find_sources(domain=None, country=None, has_api=None):
    all_sources = load_all_sources()
    results = all_sources

    if domain:
        results = [s for s in results if domain in s['coverage']['domains']]

    if country:
        results = [s for s in results
                  if s['organization'].get('country') == country]

    if has_api is not None:
        results = [s for s in results
                  if s['access']['api']['available'] == has_api]

    return results

# 示例：查找所有有API的中国数据源
chinese_api_sources = find_sources(country='CN', has_api=True)
for source in chinese_api_sources:
    print(f"{source['name']['zh']}: {source['access']['api']['documentation']}")
```

---

## 📊 数据源概览

### 当前统计

| 类别 | 数量 | 覆盖内容 |
|------|------|----------|
| 🌍 **国际组织** | 28 / 100+ | 世界银行、IMF、OECD、WHO、FAO... |
| 🇨🇳 **中国政府** | 19 / 488 | 人民银行、国家统计局、海关总署、证监会... |
| 🌎 **各国官方** | 24 / 200+ | 美国、加拿大、日本、英国、澳大利亚... |
| 🎓 **学术机构** | 26 / 50+ | NBER、Penn World Table、PubMed... |
| 🏭 **行业领域** | 29 / 150+ | 能源、金融、健康、气候... |
| **合计** | **126 / 950+** | **完成度13%** |

### 已完成数据源 | Completed Sources

#### 🌍 国际组织 (28个)
📄 **详细信息**: [sources/international/README.md](sources/international/README.md)

#### 🇨🇳 中国数据源 (19个)
📄 **详细信息**: [sources/china/README.md](sources/china/README.md)

#### 🌎 各国官方 (24个)
📄 **详细信息**: [sources/countries/README.md](sources/countries/README.md)

#### 🎓 学术研究 (26个)
📄 **详细信息**: [sources/academic/README.md](sources/academic/README.md)

#### 🏭 行业领域 (29个)
📄 **详细信息**: [sources/sectors/README.md](sources/sectors/README.md)

---

### 质量保证：确保每个数据源都是可信底座

- ✅ **100% URL验证** - 每个链接都经过测试且可用
- ✅ **权威性优先** - 主要收录政府和国际组织数据源
- ✅ **元数据验证** - 所有JSON文件通过schema验证
- ✅ **双语文档** - 所有数据源提供中英文说明
- ✅ **证据链完整** - 提供从查询到原始数据的完整路径

---

## 📐 元数据结构

每个数据源包含 **结构化元数据**，支持机器可读和自动化证据链构建：

### 核心信息
- **唯一ID**：小写、连字符分隔的标识符
- **名称**：英文、中文和本地语言名称
- **组织**：名称、类型、国家、官方网站
- **描述**：详细的双语描述

### 访问与发现
- **主要URL**：主数据门户
- **API信息**：可用性、文档、认证要求
- **下载选项**：批量下载、支持格式（CSV、Excel、JSON等）
- **访问级别**：开放、需注册、学术、商业、受限

### 覆盖详情
- **地理范围**：全球、区域、国家、次国家级
- **国家/地区**：具体覆盖区域
- **时间范围**：起始年份、结束年份、更新频率
- **领域**：经济、健康、气候、能源等
- **数据内容**：具体数据类别和内容描述

### 权威性标识 - AI时代的可信度保障
- **authority_level**：权威等级分类
  - `government` - 政府机构
  - `international` - 国际组织
  - `research` - 研究机构
  - `market` - 市场机构
  - `commercial` - 商业机构
  - `other` - 其他

**完整Schema**: 查看 [schemas/datasource-schema.json](schemas/datasource-schema.json)

---

## 🤝 如何贡献

我们欢迎全球社区的贡献！目前规划了 **850+数据源**，涵盖：

- 488个中国政府数据源（部委、省级部门）
- 100+国际组织
- 200+各国统计局
- 50+学术研究机构
- 150+行业特定数据门户

### 步骤1：选择任务

浏览 [任务清单](tasks/README.md)：
- [中国政府数据源](tasks/china/) - 16个领域的488个数据源
- [国际组织](tasks/international.md) - 100+数据源
- [各国官方](tasks/countries.md) - 200+国家级数据源
- [学术机构](tasks/academic.md) - 50+研究机构
- [行业领域](tasks/sectors.md) - 150+领域特定数据源

### 步骤2：认领任务

1. 找到未认领的数据源（标记为⬜）
2. 使用[任务认领模板](.github/ISSUE_TEMPLATE/claim-task.md)创建Issue
3. 等待维护者确认（24小时内）
4. 任务分配成功！🎉

### 步骤3：收集数据源信息

遵循[数据收录指南](docs/data-collection-guide.md)：

**阶段1：基本信息（30分钟）**
- 组织名称、国家、官方网站
- 主数据门户URL
- 中英文简要描述

**阶段2：访问详情（30分钟）**
- 检查API可用性和文档
- 确定下载选项和格式
- 判断访问级别（开放/注册/学术）

**阶段3：覆盖范围分析（45分钟）**
- 地理范围和覆盖国家
- 时间范围（起始年份、结束年份、更新频率）
- 主题领域和数据内容

**阶段4：权威性评估（15分钟）**
确定数据源的权威等级：
- `government` - 政府机构（国家部委、监管机构等）
- `international` - 国际组织（联合国、世界银行、IMF等）
- `research` - 研究机构（大学、研究院所等）
- `market` - 市场机构（交易所、行业协会等）
- `commercial` - 商业机构（付费数据服务等）
- `other` - 其他类型

**阶段5：验证（15分钟）**
- 运行 `python scripts/validate.py sources/path/to/your-file.json`
- 修复任何schema验证错误
- 测试所有URL

**总耗时：每个数据源约2小时**

### 步骤4：提交Pull Request

```bash
# 创建分支
git checkout -b add-datasource-your-source-name

# 在适当的目录添加JSON文件
# 示例: sources/china/finance/securities/your-source.json

# 验证
python scripts/validate.py sources/path/to/your-file.json

# 提交并附上描述性消息
git add sources/path/to/your-file.json
git commit -m "添加[组织名称]数据源

- 添加了[组织名称]的元数据
- 权威等级: [government/international/research/market/commercial/other]
- 覆盖[领域]从[起始年份]至今
- [有API / 无API]"

# 推送并创建PR
git push origin add-datasource-your-source-name
```

### 步骤5：审核与合并

- 维护者将在3个工作日内审核
- 处理任何反馈或验证错误
- 批准后，你的贡献将被合并！🎊
- 你将在致谢中被列出

### 贡献准则

**✅ 我们接受：**
- 政府官方数据源（国家级、省级、地方级）
- 国际组织官方数据
- 顶级学术机构和研究仓库
- 定期更新的权威行业数据
- 对现有元数据的改进

**❌ 我们不接受：**
- 纯商业数据（无免费层级）
- 个人或小型非官方组织数据
- 长期未维护的数据源（>3年无更新）
- 无官方文档的数据源
- 重复或冗余的数据源

**文档资源：**
- [完整贡献指南](docs/CONTRIBUTING.md) - 详细的贡献流程
- [数据收录指南](docs/data-collection-guide.md) - 数据源收录工作流

---

### 验证脚本

```bash
# 验证单个文件
python scripts/validate.py sources/china/finance/banking/pbc.json

# 验证所有文件
find sources -name "*.json" -exec python scripts/validate.py {} \;
```

### 生成索引

```bash
# 自动生成类别索引和统计
python scripts/generate_indexes.py

# 输出：
# - indexes/by-country.json
# - indexes/by-domain.json
# - indexes/by-authority-level.json
```

---

[![Star History Chart](https://api.star-history.com/svg?repos=jiangwenzhe/datasource-hub&type=Date&theme=dark&width=800&height=400)](https://star-history.com/#jiangwenzhe/datasource-hub&Date)


## 📞 联系与支持

- **项目主页**：https://code.mlamp.cn/0003432/datasource-hub
- **问题反馈**：https://code.mlamp.cn/0003432/datasource-hub/issues
- **任务认领**：[创建Issue](.github/ISSUE_TEMPLATE/claim-task.md)
- **讨论区**：[GitHub Discussions](https://code.mlamp.cn/0003432/datasource-hub/discussions)

---

## 📄 许可协议

本项目采用 [MIT License](LICENSE) 开源。

各个数据源有其自己的许可条款 - 请查看每个JSON文件中的 `licensing` 字段。

---

## 🙏 致谢

**灵感来源：**
- [OpenMetadata](https://github.com/open-metadata/OpenMetadata) - 数据目录平台
- SDMX - 统计数据和元数据交换标准
- [Awesome Public Datasets](https://github.com/awesomedata/awesome-public-datasets)

**感谢：**
- 所有维护开放数据的政府机构和国际组织
- 帮助构建这个知识库的贡献者
- 开源和开放数据社区

---

<p align="center">
  <strong>打造AI时代的可信底座 | 让每一次深度思考都建立在可验证的事实之上</strong><br>
  <strong>Building the Trusted Foundation for AI Era | Every Deep Thought Based on Verifiable Facts</strong>
</p>

<p align="center">
  <sub>Made with ❤️ by the DataSource Hub Community</sub>
</p>

<p align="center">
  <a href="#-为什么选择-datasource-hub">为什么</a> •
  <a href="#-核心优势">核心优势</a> •
  <a href="#-使用场景在ai时代避免幻觉基于证据推理">使用场景</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-如何贡献">如何贡献</a> •
  <a href="#-发展路线图">路线图</a>
</p>
