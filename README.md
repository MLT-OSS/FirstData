# FirstData 🌐

**[English](README.en.md)** | 中文 | **[日本語](README.ja.md)**

---

**全球最全面、最权威、最结构化的开源数据源知识库**

**The World's Most Comprehensive, Authoritative, and Structured Open Data Source Repository**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Sources](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/MLT-OSS/FirstData/refs/heads/main/assets/badges/sources-count.json)](./firstdata/sources/README.md)
[![Progress](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/MLT-OSS/FirstData/refs/heads/main/assets/badges/progress.json)](./firstdata/indexes/statistics.json)
[![Authority](https://img.shields.io/badge/Authority-Government%20%26%20International%20First-brightgreen.svg)](#)
[![MCP Server](https://img.shields.io/badge/MCP-AI%20Smart%20Search-purple.svg)](https://firstdata.deepminer.com.cn/)

---

## 🎯 为什么选择 FirstData?

### AI时代的事实防线：从"信息过载"到"真实稀缺"

在生成式 AI 重新塑造互联网的今天，**"信息"变得空前充沛，而"真实"正在变得稀缺**。

当噪音、拼贴与幻觉成为默认背景，**可信的一手证据（Primary Sources）不再只是参考资料，而是整个智能体系的地基**。

### 我们的目标：构建AI时代的可信底座

本项目旨在构建一个**面向全球的、权威的、结构化的 Primary Sources 知识库**。

我们系统性发掘并聚合跨领域高可信信源——覆盖科研学术、政务公开、法律法规、公司披露与财报、标准规范与行业权威资料等——**将分散、非标、难复用的原始内容，转化为可追溯、可验证、可引用的"核心事实（Core Facts）"**，并保留完整证据链与版本历史，确保每一条结论都能"回到原文"。

### 这是一道面向大模型时代的"事实防线"

✅ **为模型提供抗幻觉、抗投毒的可信底座**

- 计划覆盖1000+权威数据源（来源均为中外政府部门、国际组织、学术机构、行业权威协会）
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

| 特性                             | 我们的独特之处                                                                 | AI时代的价值                                               |
| -------------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| 🇨🇳**深度覆盖中国数据源** | **全球独家**：规划收录500+中国政府数据源，涵盖多个核心领域               | 填补全球数据源目录中的中国空白，为跨国研究提供可信中国数据 |
| 📊**结构化元数据体系**     | 完整元数据标准（访问URL、API接口、权威等级、更新频率、数据内容等），不只是链接 | 机器可读、可编程访问，支持自动化证据链构建                 |
| ⭐**权威等级分类**         | 政府、国际组织、研究机构、市场、商业等六类权威等级                             | 科学评估数据源可信度，为AI提供质量过滤依据                 |
| 🤖**AI智能搜索**           | 基于LLM驱动的数据源查询Agent，理解复杂多维度查询                               | 自然语言即可获取权威数据源，无需人工筛选                   |
| 🔌**MCP协议集成**          | 提供标准MCP Server，可集成到Claude Desktop、Cline等AI应用                      | 让任何AI应用都能访问权威数据源知识库                       |
| 🌍**中英双语支持**         | 所有元数据提供中英文版本                                                       | 连接全球数据生态，打破语言壁垒                             |
| 🔍**100%验证**             | 每个URL经过测试，每个数据源有完整文档，每个权威等级有依据                      | 确保数据源真实可用，避免断链和幻觉引用                     |

---

## 📊 数据源概览

### 覆盖范围

优先收录政府级与国际组织级权威数据源，同步覆盖顶级学术机构与行业权威来源：

| 类别              | 典型来源                                  |
| ----------------- | ----------------------------------------- |
| 🌍 **国际组织**   | 世界银行、IMF、OECD、WHO、FAO...          |
| 🇨🇳 **中国政府** | 人民银行、国家统计局、海关总署、证监会... |
| 🌎 **各国官方**   | 美国、加拿大、日本、英国、澳大利亚...     |
| 🎓 **学术机构**   | NBER、Penn World Table、PubMed...         |
| 🏭 **行业领域**   | 能源、金融、健康、气候...                 |

### 数据源列表

📄 浏览已收录的所有数据源：[firstdata/sources/README.md](firstdata/sources/README.md)

### 质量标准

每个收录的数据源均满足以下标准：

- ✅ **100% URL验证** — 每个链接都经过测试且可用
- ✅ **权威性优先** — 主要收录政府和国际组织数据源
- ✅ **元数据验证** — 所有JSON文件通过schema验证
- ✅ **双语文档** — 所有数据源提供中英文说明
- ✅ **证据链完整** — 提供从查询到原始数据的完整路径

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

**authority_level字段**：权威等级分类

- `government` - 政府机构
- `international` - 国际组织
- `research` - 研究机构
- `market` - 市场机构
- `commercial` - 商业机构
- `other` - 其他

**完整Schema**: 查看 [schemas/datasource-schema.json](schemas/datasource-schema.json)

## 🎯FirstData MCP

**连接自然语言与一手权威数据的"最后一公里"**

---

我们构建了权威数据源的结构化知识库，每个数据源都有完整的元数据、访问路径和权威性标识。但对于大多数用户来说，真正的挑战在于：如何在海量数据源中快速找到最合适的那一个？找到了数据源网站，如何在复杂的官方平台中准确定位目标数据？如何将这一切无缝集成到日常的 AI 工作流中？

**FirstData MCP** 正是为此而生——将静态的数据源知识库转化为动态的智能导航系统，让每个人都能轻松访问权威数据。

---

### 📖 为什么需要FirstData MCP？

在 LLM 时代，我们习惯了直接询问答案，但往往面临两个核心痛点：

❌ **痛点 1：数据来源不可考（幻觉风险）**

- AI 生成的数字可能过时、错误或完全虚构
- 缺乏原始证据链，无法追溯验证
- 二手引用层层转述，丢失原始上下文

❌ **痛点 2：专业数据库门槛高（难检索）**

- 政府、国际组织网站导航复杂，术语晦涩
- 不知道哪个数据源最权威、覆盖范围如何
- 即使找到官网，也不知道如何定位目标数据

### 💡 我们的解决方案

**本 MCP 服务构建从"模糊意图"到"精确数据路径"的完整闭环：**

它不直接生成可能过时的数字，而是作为一位**"权威数据向导"**，将用户引导至国家统计局、世界银行、行业白皮书等**可信一手信源（Primary Sources）**，并提供**具体到点击步骤的检索说明书**。

> **让数据回归权威，让检索不再迷路。**

---

### ✨ 核心功能

#### 1️⃣ 权威信源定位 (Source Locator)

**解决"去哪找？"的问题**

基于用户的自然语言提问（如："2023年中国新能源汽车出口量"），智能推荐最权威的一手数据源网站。

**功能亮点：**

- 🧠 **理解复杂查询**：自动识别地理+时间+领域+权威性等多维度需求
- 🎯 **智能推荐**：Top 3-5 最相关数据源，附带详细匹配理由
- 📊 **权威性保证**：所有推荐都标注权威等级（政府/国际组织/研究/市场等）
- 🔗 **即用信息**：直接提供访问 URL、API 文档、数据格式
- ✅ **证据链完整**：从查询到原始数据，每一步都可追溯
- 🌍 **全球覆盖**：数据源覆盖全球范围内的各大领域，兼顾广度和深度

**过滤营销号与二手引用，直达官网、官方报告或专业数据库。**

**使用示例：**

<details>
<summary><b>示例1：研究人员 - 发展中国家经济数据 📚</b></summary>

**场景**：

> "我想调研一下发展中国家的GDP信息用于经济增长研究"

**传统方式的问题**：

- ❌ Google搜索充斥着二手报道、博客文章、过时链接
- ❌ 不确定数据来源的权威性和方法论
- ❌ 花费数小时导航机构网站，仍可能找错数据

**使用 FirstData MCP：**

1. 🔍 **自然语言提问**："发展中国家GDP"
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

</details>

<details>
<summary><b>示例2：数据分析师 - 中国货币政策数据 💰</b></summary>

**场景**：

> "我需要中国近10年的M1、M2货币供应量和利率数据"

**传统方式的问题**：

- ❌ AI助手可能给出过时链接或二手网站
- ❌ 不清楚数据更新频率和历史覆盖范围
- ❌ 缺乏API访问信息，无法自动化获取

**MCP工作流程：**

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

</details>

<details>
<summary><b>示例3：政策制定者 - 全球气候数据 🌍</b></summary>

**场景**：

> "我需要权威的气候数据来支持政策决策，要有API访问的全球数据"

**风险**：

- ❌ 使用不可靠数据源可能导致政策失误
- ❌ 缺乏方法论透明度，无法评估数据质量
- ❌ 二手引用缺乏原始证据链

**MCP工作流程：**

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

**价值**：

- ✅ **证据链闭环**：从查询 → 推荐 → 原始数据 → 完整可追溯
- ✅ **方法论透明**：明确数据收集方法和质量标准
- ✅ **可复现研究**：其他研究者可基于相同数据源验证结论
- ✅ **降低政策风险**：从"不确定的决策依据"到"可验证的权威证据"

</details>

---

#### 2️⃣ 网站操作导航 (Site Pathfinder)

**解决"怎么找？"的问题**

针对结构复杂、术语晦涩的专业网站，提供手把手的操作路径说明书，从首页到目标数据的完整导航指引。

**功能亮点：**

- 📖 **逐步操作指引**：明确每一步的操作对象、关键界面元素、筛选条件设置
- 🎯 **多路径保障**：提供主路径 + 备选方案 + API 访问，每条路径都经过验证
- 🔍 **精准定位**：具体到按钮位置、筛选器设置、下载步骤，而非笼统描述
- 💡 **降低门槛**：非专业人士也能快速定位，从"数小时摸索"到"3-5分钟精准获取"
- 🔄 **定期更新**：人工验证网站变化，及时更新操作路径
- 🤖 **智能匹配**：基于用户查询意图，推荐最相关的操作指令

**为常用权威数据源提供详细的网站导航指引，精确定位数据位置。**

---

### 🚀 完整使用示例：智能检索 + 操作说明书一站式方案

**场景：查找新上市科技公司招股书进行投资研究**

**用户提问：**

> "我想研究国内最近上市的某家AI科技公司，需要找到他们的招股说明书，分析一下商业模式和财务状况"

**✅ 使用 FirstData MCP 的完整工作流：**

#### 📋 第一步：智能检索可信数据源

```
推荐数据源：

1. 香港交易及结算所有限公司 (HKEX)
   - 描述：港交所运营HKEXnews（披露易），提供上市公司招股书、
           年报、IPO信息和监管文件的官方平台
   - 访问地址：https://www.hkexnews.hk
   - 权威等级：market（市场机构）
   - 文档类型：招股说明书、年报、公告
   - 证据链：官方披露文件 → 可直接引用

2. 中国证券监督管理委员会 (CSRC)
   - 访问地址：http://www.csrc.gov.cn
   - 境外上市备案信息查询
   - 权威等级：government（政府机构）
```

**价值点：**

- ✅ **避免幻觉**：推荐的是官方披露平台，不是新闻网站
- ✅ **权威性保证**：明确标注数据源的权威等级
- ✅ **提供关键线索**：预先提供财务概要信息，帮助理解数据背景

#### 📖 第二步：获取网站操作说明书

MCP 内置了**操作说明书数据库**，涵盖常用权威数据源的网站导航和下载步骤。

**检索披露易（HKEXnews）网站操作指令：**

```
source: https://www.hkexnews.hk
operation: 如何查找新上市公司的招股说明书?
```

**说明书检索结果：**

```
网站操作说明书：

主路径（推荐）：
1. 访问香港交易所披露易网站首页 (https://www.hkexnews.hk)
2. 点击主导航栏中的 "NEW LISTINGS" 选项
3. 进入 New Listing Information 页面
4. 选择对应的市场板块（主板 Main Board 或创业板 GEM）
5. 在新上市公司列表中查找目标公司名称或股票代码
6. 点击对应的招股书下载链接（Prospectus）
7. 下载PDF文件即可

备选路径：
1. 访问香港交易所披露易网站首页
2. 使用搜索功能输入公司名称或股票代码
3. 在搜索结果中筛选文档类型为 "Prospectus"
4. 选择最新日期的招股说明书
5. 点击下载链接获取PDF文件
```

**价值点：**

- ✅ **即用指引**：提供逐步操作说明，无需人工摸索网站结构
- ✅ **多路径保障**：提供备选方案，确保能成功获取文档
- ✅ **降低门槛**：非专业人士也能快速定位官方文档

#### 📊 第三步：基于官方数据进行分析

**获取招股书后的研究分析框架：**

根据招股书披露的官方数据，可以进行系统性分析：

**1. 商业模式分析**

- **核心业务**：从招股书"业务概览"章节了解公司主营业务和收入来源
- **市场定位**：分析目标市场、客户群体和竞争优势
- **盈利模式**：识别收入结构、定价策略和变现路径

**2. 财务状况分析**

- **收入趋势**：查看历史财务数据，分析营收增长率和可持续性
- **盈利能力**：评估毛利率、净利率等关键指标
- **现金流**：研究经营活动现金流、融资用途和资金储备

**3. 风险因素评估**

- **业务风险**：招股书"风险因素"章节列出的主要风险
- **财务风险**：负债水平、流动性、偿债能力
- **行业风险**：市场竞争、技术变革、监管政策变化

**4. 投资价值判断**

- **成长潜力**：基于业务规划和市场前景评估增长空间
- **估值合理性**：对比同行业公司市盈率、市销率等指标
- **募资用途**：IPO资金使用计划是否与战略目标一致

**✅ 完整的证据链闭环：**

```
用户提出研究需求
  ↓
MCP 智能检索推荐权威数据源（港交所披露易）
  ↓
获取网站操作说明书（逐步导航指引）
  ↓
下载官方招股说明书（一手权威文档）
  ↓
基于官方披露数据进行系统性分析
  ↓
所有结论可回溯至原始文档验证
```

**核心价值：**

- ✅ **抗幻觉**：推荐的是港交所官方披露平台，而非新闻网站或 AI 生成内容
- ✅ **可验证**：完整证据链，任何人都可以沿着路径获取相同的原始数据
- ✅ **即用指引**：提供逐步操作说明，从"不知道在哪找"到"3-5分钟精准获取"
- ✅ **多路径保障**：主路径 + 备选方案 + 搜索功能，确保能成功下载文档

---

## 🚀 快速开始

### 集成 FirstData MCP

**将FirstData MCP配置到您的AI应用中，实现智能检索权威数据源和操作说明书导航**

支持多个平台：Claude Desktop、Cline (VS Code)、Zed、Cursor 等所有兼容 MCP 协议的 AI 应用。

---

#### 配置指南：根据你使用的平台选择

> **📝 重要提示**
>
> **申请 API Key（必需）**：在配置 MCP 服务器之前，请先访问 [FirstData API 申请](https://firstdata.deepminer.com.cn/) 申请免费的 API key。将下方所有配置示例中的 `<YOUR_FIRSTDATA_API_KEY>` 替换为你申请到的实际 API key。

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
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```

   > **提示**：`autoApprove` 字段可以让常用的只读工具自动执行，无需每次确认。
   >
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
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         },
         "enabled": true
       }
     }
   }
   ```

   > **注意**：Zed 使用 `context_servers` 而不是 `mcpServers`
   >
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
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```
3. **重启 Cursor** 以加载 MCP 服务器

</details>

<details>
<summary><b>Copilot / VS Code</b></summary>

**推荐方式：HTTP 服务器**

1. 参考 [VS Code MCP 配置指南](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server)
2. 添加配置到 VS Code MCP 设置：

   ```json
   {
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```

**使用 VS Code CLI：**

```bash
code --add-mcp '{"name":"firstdata","type":"streamable-http","url":"https://firstdata.deepminer.com.cn/mcp","headers":{"Authorization":"Bearer <YOUR_FIRSTDATA_API_KEY>"}}'
```

</details>

<details>
<summary><b>Copilot CLI</b></summary>

使用 HTTP 服务器方式连接：

```json
{
  "mcpServers": {
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
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

## 🤝 如何贡献

### 推荐新数据源

  发现了权威可信的数据源？欢迎向我们推荐！

  **推荐流程：**

1. [提交Issue](链接) 说明数据源信息和推荐理由
2. 我们会评估其权威性、数据质量和可信度
3. 通过评估后，将正式收录到数据源仓库

  **收录标准：**

- ✅ 政府官方数据源（国家级、省级、地方级）
- ✅ 国际组织官方数据
- ✅ 顶级学术机构和研究仓库
- ✅ 定期更新的权威行业数据

## 💬 Community and Support | 社区与支持

加入我们的社区，与数据研究者、开发者和贡献者交流！

**Join our community to connect with data researchers, developers, and contributors!**

### 微信交流群 | WeChat Group

<div align="center">
  <img src="assets/wechat-qrcode.png" alt="WeChat Group QR Code" width="300"/>
  <p><i>扫描二维码加入微信群 | Scan to join WeChat group</i></p>
</div>

> 💡 **提示**: 加入社区后，你可以：
> - 讨论数据源推荐和使用经验
> - 获取技术支持和最佳实践
> - 参与项目开发和贡献
> - 了解最新的数据源更新和功能发布

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MLT-OSS/FirstData&type=date&legend=top-left)](https://www.star-history.com/#MLT-OSS/FirstData&type=date&legend=top-left)

## 📄 许可协议

本项目采用 [MIT License](LICENSE) 开源。

---

<p align="center">
  <strong>打造AI时代的可信底座 | 让每一次深度思考都建立在可验证的事实之上</strong><br>
  <strong>Building the Trusted Foundation for AI Era | Every Deep Thought Based on Verifiable Facts</strong>
</p>

<p align="center">
  <sub>Made with ❤️ by the FirstData Community</sub>
</p>

<p align="center">
  <a href="#-为什么选择-firstdata">为什么</a> •
  <a href="#-核心优势">核心优势</a> •
  <a href="#-数据源概览">数据源概览</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-如何贡献">如何贡献</a>
</p>