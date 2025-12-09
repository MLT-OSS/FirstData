# 工作流程示例

本文档提供完整的数据源抓取工作流程示例，展示如何应用两层降级策略。

## 示例 0: 名字输入（自动搜索官网）

**用户输入**: "请帮我收录 GenBank - 基因序列数据库"

**执行步骤**:

### 1. 识别输入类型

- 检测输入：不以 `http://` 或 `https://` 开头
- 判断为：**名字输入**
- 提取名字：`GenBank`

### 2. WebSearch 搜索官方网站

**构建搜索查询**：

```
主查询: "GenBank official website data"
辅助查询:
- "GenBank API documentation"
- "GenBank database download"
- "GenBank NCBI"
```

**搜索结果分析**：

```
找到以下 URL：
1. https://www.ncbi.nlm.nih.gov/genbank/
   - 域名：.nih.gov (美国国立卫生研究院)
   - 标题：GenBank Overview
   - 来源：NCBI (National Center for Biotechnology Information)

2. https://www.ddbj.nig.ac.jp/
   - 域名：.ac.jp (日本学术机构)
   - 标题：DNA Data Bank of Japan
   - 来源：DDBJ

3. https://en.wikipedia.org/wiki/GenBank
   - 域名：wikipedia.org
   - 类型：百科全书（排除）
```

### 3. AskUserQuestion 确认官网

使用 AskUserQuestion 工具询问用户：

```markdown
问题: "请确认要收录的官方网站"
选项:
1. https://www.ncbi.nlm.nih.gov/genbank/ (推荐)
   描述: NCBI GenBank - 美国国立生物技术信息中心，NIH官方数据库

2. https://www.ddbj.nig.ac.jp/
   描述: DDBJ - 日本 DNA 数据库，GenBank 的国际合作伙伴
```

**官网识别规则**：

优先级从高到低：
- ✅ 政府域名 (`.gov`, `.gov.cn`, `.go.jp`)
- ✅ 教育域名 (`.edu`, `.ac.uk`, `.edu.cn`)
- ✅ 知名国际组织 (`worldbank.org`, `who.int`, `imf.org`)
- ⚠️ 商业域名 (`.com`, `.org`) - 需验证
- ❌ 百科/博客 (`wikipedia.org`, `blog.*`) - 排除

### 4. 用户确认

用户选择：`https://www.ncbi.nlm.nih.gov/genbank/`

### 5. 继续标准流程

确认 URL 后，按照示例 1 的标准流程继续：
- WebFetch 获取网站内容
- 提取组织信息、数据内容
- 质量评估
- 生成 JSON
- 验证和保存

**最终输出**：`sources/academic/biology/genbank.json`

---

## 名字输入的常见场景

### 场景 1：中文名字

**用户输入**: "请收录 人民银行数据"

**搜索策略**：
```
中文查询: "人民银行 官方网站 数据"
英文查询: "People's Bank of China official data"
```

**识别结果**:
- ✅ `http://www.pbc.gov.cn/` (`.gov.cn` 政府域名)
- 自动确认（政府域名可信度高）

### 场景 2：缩写名字

**用户输入**: "请收录 WHO 数据"

**搜索策略**：
```
"WHO official website"
"World Health Organization data"
```

**识别结果**:
- ✅ `https://www.who.int/` (`.int` 国际组织域名)
- 自动确认

### 场景 3：多个候选

**用户输入**: "请收录 World Development Indicators"

**搜索结果**：
```
1. https://datatopics.worldbank.org/world-development-indicators/ (World Bank)
2. https://data.un.org/ (UN Data)
```

**处理**：使用 AskUserQuestion 让用户选择

### 场景 4：找不到明确官网

**用户输入**: "请收录 某小型地方统计局"

**搜索结果**：无明确 `.gov` 域名

**处理**：
```
⚠️ 未找到明确的官方网站

搜索到以下结果，但无法确定是否为官方网站：
- http://example.com/stats

请提供官方网站 URL，或确认以上 URL 是否正确。
```

---

## 示例 1: 使用 WebSearch + WebFetch（标准流程）

**用户输入**: "请抓取 https://www.who.int/data 并创建数据源条目"

**执行步骤**:

1. **第一层：WebSearch + WebFetch** - 结合搜索和直接访问：
   - **搜索**："WHO data/API/methodology" 等多角度搜索 → 获取概览和关键 URL
   - **验证**：WebFetch 访问 https://www.who.int/data → 提取详细内容
   - ✅ 成功获取所有必要信息

2. **质量评估**:
   - 基于搜索结果和已知信息评分
   - 权威性 5（全球最高卫生组织）、方法论 5、及时性 4、完整性 5、文档 5、引用 5

3. **生成和保存**:
   - 生成 JSON 并保存到 `sources/international/health/who.json`

4. **验证**:
   - Schema 验证: `python .claude/skills/datasource-scraper/scripts/validate.py sources/international/health/who.json`
   - 确保所有字段验证通过

5. **生成索引**:
   - 运行 `python .claude/skills/datasource-scraper/scripts/generate_indexes.py`
   - 更新项目索引文件

6. **更新 README**:
   - 在 `sources/international/README.md` 中添加 WHO 数据源条目（健康领域部分）

7. **报告结果**: 向用户报告成功及摘要信息

---

## 示例 2: 需要使用 Playwright（两层策略完整流程）

**用户输入**: "请抓取 https://data.stats.gov.cn 并创建数据源条目"

**执行步骤**:

1. **第一层：WebSearch + WebFetch**
   - **搜索**："国家统计局 data/API" → 获取基本信息
   - **验证**：WebFetch 访问 https://data.stats.gov.cn
   - ⚠️ 返回的 HTML 内容很少（<300 字符），检测到页面使用 JavaScript 动态加载
   - ⚠️ 数据类别列表信息不完整

2. **第二层：Playwright**（触发条件：JS 渲染页面）

   **告知用户**:
   ```
   ⚠️ 检测到访问困难，需要使用浏览器工具

   【遇到的问题】: 该页面使用 JavaScript 动态加载内容，
   WebFetch 只能获取到页面骨架，无法看到完整的数据分类目录。

   【解决方案】: 使用 Playwright 浏览器工具，等待页面完全加载

   【需要您的协助】: 通常不需要您的操作，我会自动等待页面加载完成

   【继续操作】: 现在开始使用浏览器工具...
   ```

   **操作流程**:
   - 🌐 打开页面: `browser_navigate`
   - ⏳ 等待 JS 执行: `browser_wait_for({ time: 3 })`
   - 📋 获取页面结构: `browser_snapshot`
   - 📸 截图验证: `browser_take_screenshot`
   - 🖱️ 展开数据分类菜单: `browser_click`
   - 📊 提取数据: `browser_evaluate` 执行 JS 提取所有数据类别
   - ✅ 关闭浏览器: `browser_close`

   **向用户反馈**:
   ```
   ✅ 浏览器提取完成
   📊 已获取以下信息：
   - 组织名称: 国家统计局
   - 数据类别: 23 个主要类别
   - 更新频率: 月度/季度/年度
   - 数据格式: Excel, CSV
   ```

4. **质量评估**:
   - 权威性 5、方法论 5、及时性 4、完整性 5、文档 4、引用 4

5. **生成和保存**:
   - 生成 JSON 并保存到 `sources/china/national/nbs-data.json`

6. **验证和索引**: 同示例 1

7. **报告结果**: 包含使用 Playwright 的额外说明

**两层策略应用总结**:
- 第一层提供了基础信息（30%），但发现技术限制（JS 渲染）
- 第二层成功获取完整信息（70%）
- 总耗时约 2 分钟（包括浏览器操作）

---

## 示例 3: Upsert 操作（更新现有数据源）

**用户输入**: "请抓取 https://www.pbc.gov.cn/ 数据源"

**执行步骤**:

1. **抓取网站信息**:
   - 使用 Web Search 获取中国人民银行最新信息
   - 提取 URL、数据门户、API 文档等信息

2. **生成数据和检测现有文件**:
   - 生成数据源 ID: `china-pbc`
   - 搜索 `sources/` 目录
   - ✅ **找到现有文件**: `sources/china/finance/banking/pbc.json`
   - 操作类型：**更新**

3. **读取现有数据**:
   - 加载 `pbc.json` 的当前内容
   - 创建日期: 2024-01-15
   - 贡献者: John Doe
   - 质量评分: 手动评估（5.0）

4. **创建备份**:
   ```
   📦 已创建备份: pbc.json.backup
   ```

5. **智能合并数据**:
   - **更新**: `access.primary_url` (http → https)
   - **添加**: `access.api.documentation` (新发现)
   - **保留**: 所有质量评分（手动评分优先）
   - **合并**: tags 数组去重（"banking" + "monetary-policy"）
   - **保留**: 原始创建日期和贡献者
   - **更新**: `last_updated` → 2025-12-09

6. **验证合并结果**:
   - Schema 验证: ✅ 通过
   - 完整性检查: ✅ 保持 100%

7. **保存更新**:
   - 覆盖原文件 `pbc.json`

8. **报告变更摘要**:
   ```
   ✅ 已更新 sources/china/finance/banking/pbc.json

   📊 变更摘要：

     - 更新字段 (3):
       * access.primary_url: http://www.pbc.gov.cn → https://www.pbc.gov.cn
       * access.api.documentation: 已添加
       * catalog_metadata.last_updated: 2024-01-15 → 2025-12-09

     - 保留字段:
       * quality.* (所有质量评分 = 5.0)
       * catalog_metadata.contributor = John Doe
       * catalog_metadata.added_date = 2024-01-15

     - 数组新增:
       * tags: monetary-policy (banking 已存在)

     - 备份位置: pbc.json.backup
   ```

9. **更新索引**（可选）:
   - 运行 `python .claude/skills/datasource-scraper/scripts/generate_indexes.py`

**关键要点**:
- ✅ 自动检测并执行更新操作（用户无需指定）
- ✅ 安全备份机制（.backup 文件）
- ✅ 智能合并，保留手动编辑的内容
- ✅ 清晰的变更报告

---

<!-- 更多 Playwright 使用场景（登录处理、交互内容提取等），详见 [playwright-workflow.md](playwright-workflow.md) -->
