---
name: datasource-scraper
description: Extract or update datasource information from websites and convert to DataSource Hub JSON format. Supports upsert semantics - automatically creates new entries or updates existing ones. Use when the user provides a data source URL or name (e.g., "GenBank", "World Bank", "人民银行"). Outputs a validated JSON file following datasource-schema.json standard with quality assessment.
---

# 数据源抓取器

从网站提取数据源信息并转换为 DataSource Hub 标准 JSON 格式。

**支持 Upsert 操作**：无论数据源是否已存在，都可以使用同一流程处理（自动创建或更新）。

**支持两种输入形式**：
- **URL 形式**：`http://www.pbc.gov.cn/`
- **名字形式**：`GenBank - 基因序列数据库`、`人民银行数据`、`World Bank`

## 核心工作流程

### 1. 获取网站内容

**步骤 1：识别输入类型**

- 如果输入以 `http://` 或 `https://` 开头 → **URL 输入**，直接使用
- 否则 → **名字输入**，使用 WebSearch 搜索官方网站，用 AskUserQuestion 确认 URL

**详细流程**：参见 [workflow-examples.md](reference/workflow-examples.md) 中的"名字输入示例"

**步骤 2：采用两层降级策略**

确定 URL 后，根据页面复杂度选择合适的工具。

#### 第一层：Web Search / WebFetch（主要策略）

结合使用 `WebSearch` 和 `WebFetch` 获取信息：

**Web Search 搜索**：
- "{组织名称} data/API/methodology/about" 等多角度搜索
- 快速获取概览信息和关键 URL

**WebFetch 验证**：
- 直接访问用户提供的 URL 或搜索中发现的页面
- 提取静态页面详细内容

**提取目标信息**：
- 组织信息（名称、类型、描述）
- 关键 URL（主页、数据门户、API 文档）
- 数据覆盖范围、更新频率、许可协议
- API 可用性和认证方式

#### 第二层：Playwright 浏览器自动化（JS 渲染页面）

当前两层无法获取足够信息时使用。**详见 [Playwright 工作流程](reference/playwright-workflow.md)**

**触发条件**（满足任一即可）:
- JavaScript 渲染页面（WebFetch 返回内容很少或为空）
- 需要登录或认证才能查看内容
- 关键信息在交互式元素中（下拉菜单、折叠面板、Tab）
- 用户明确要求使用浏览器

**⚠️ 使用前必须告知用户**:

使用以下模板向用户说明：
```
⚠️ 检测到访问困难，需要使用浏览器工具

【遇到的问题】: [具体描述问题，如：页面使用 JavaScript 动态加载/需要登录/内容隐藏在交互菜单中]

【解决方案】: 使用 Playwright 浏览器工具

【需要您的协助】: [列出可能需要的用户操作，如：手动登录/完成验证码]

【继续操作】: 现在开始使用浏览器工具...
```

**详细操作流程**: 见 [reference/playwright-workflow.md](reference/playwright-workflow.md)

**降级策略**:
```
第一层: WebSearch + WebFetch（静态内容）
  ↓ JS 渲染/需要登录/交互内容
第二层: Playwright（浏览器自动化）→ 告知用户 → 持续反馈
```

### 2. 信息提取
从网页提取以下信息填充 JSON：
- **基础信息**: id, name (多语言), organization, description
- **访问信息**: primary_url, API, download options, access_level
- **覆盖范围**: geographic, temporal, domains, indicators
- **数据内容**: 分类列表（中英双语）
- **数据特征**: types, granularity, formats, languages
- **质量评估**: 6 个维度评分（见 quality-criteria.md）
- **许可协议**: license, commercial_use, restrictions
- **其他**: metadata standards, usage, contact, tags

**详细字段说明**: 见 [schema-fields.md](reference/schema-fields.md)

### 3. 质量评估
按 1-5 星评分以下 6 个维度：
- authority_level - 来源权威性
- methodology_transparency - 方法论透明度
- update_timeliness - 更新及时性
- data_completeness - 数据完整性
- documentation_quality - 文档质量
- citation_count - 引用频次

**评分标准**: 见 [quality-criteria.md](reference/quality-criteria.md)

**评分原则**:
- 保守评估，有依据
- 只有真正顶级官方来源才给 5 星
- 生成时说明评分理由

### 4. 生成 JSON
- 参考 schema 文件: `schemas/datasource-schema.json`
- 填充所有必填字段
- 尽可能填充可选字段

**不确定信息的处理**：
- **可选字段**（非 required）：如果无法获取，直接删除该字段
- **允许 null 的字段**（schema 中类型为 `["string", "null"]`）：可以设为 `null`
- **不允许 null 的字段**（schema 中类型为 `"string"`）：必须提供有效值或删除字段
- **必填字段**（在 required 列表中）：必须提供有效值，可以向用户询问

**参考示例**:
- `sources/china/national/nbs.json` - 国家统计局
- `sources/china/finance/banking/pbc.json` - 中国人民银行
- `sources/international/economics/worldbank.json` - 世界银行

### 5. Upsert 操作（自动检测创建或更新）

**Skill 支持 Upsert 语义**：无论数据源是否已存在，都可以使用同一流程处理（类似 `dict[key] = value`）。

#### 自动检测逻辑

在保存文件前，使用生成的 `id` 字段在所有 `sources/` 目录中搜索现有文件：

- **未找到** → **创建新文件**（标准新建流程）
- **找到** → **更新文件**（智能合并 + 备份）

#### 更新操作要点

如果检测到已存在相同 ID 的数据源：

1. **创建备份**：`{文件名}.backup` （覆盖旧备份）
2. **智能合并**：
   - 更新 URL、API 文档等新信息
   - **保留手动质量评分**（不覆盖）
   - 合并 tags、use_cases 等数组字段（去重）
   - 保留原始创建日期和贡献者信息
3. **验证后保存**：合并结果通过 schema 验证后才更新
4. **报告变更**：向用户展示哪些字段更新了、哪些保留了

#### 确定保存路径

**使用 datasource-classifier Sub-Agent**:

在保存前,调用 `@datasource-classifier` 确定最佳分类路径:
```
@datasource-classifier
请分析此数据源并确定分类路径:
- ID: {id}
- 组织: {organization.name} ({organization.type})
- 国家: {organization.country}
- 领域: {coverage.domains}
```

datasource-classifier 会返回:
- 推荐路径 (如 `sources/china/finance/banking/pbc.json` 或 `sources/countries/north-america/canada/statcan.json`)
- 分类理由和置信度
- 替代方案(如适用)

**快速参考** (无法使用classifier时):
- 中国官方 → `sources/china/{domain}/{subdomain}/`
- 国际组织 → `sources/international/{domain}/`
- 学术机构 → `sources/academic/{domain}/`
- 其他国家 → `sources/countries/{continent}/{country}/`

**详细分类规则**: 见 `.claude/agents/datasource-classifier.md`
**Upsert 流程**: 见 [upsert-workflow.md](reference/upsert-workflow.md)
**目录结构**: 见 [directory-structure.md](reference/directory-structure.md)

### 6. 验证

**Schema 验证**:

使用 skill 内置的验证脚本验证 JSON 文件的格式：

```bash
# 从项目根目录运行
python .claude/skills/datasource-scraper/scripts/validate.py sources/path/to/file.json --schema schemas/datasource-schema.json
```

**URL 可访问性验证**:

使用 URL 验证脚本检查所有 URL 是否可访问：

```bash
# 从项目根目录运行
python .claude/skills/datasource-scraper/scripts/verify_urls.py sources/path/to/file.json
```

验证的 URL 字段包括：
- `access.primary_url` - 主要访问 URL（必需）
- `organization.website` - 组织网站 URL
- `access.api.documentation` - API 文档 URL
- `contact.support_url` - 支持/帮助 URL

验证 primary_url, organization.website, API文档等URL的可访问性。确保关键URL验证通过。

**完整性检查**:

```bash
python scripts/check_completeness.py sources/path/to/file.json
```

最低要求: 必需字段100%, 推荐字段≥80%, 总体≥70%

### 7. 生成索引

```bash
# 测试新数据源
python scripts/generate_indexes.py --test sources/path/to/file.json

# 生成完整索引
python .claude/skills/datasource-scraper/scripts/generate_indexes.py
```

生成all-sources.json, by-domain.json, by-country.json, stats.json等索引文件。

### 8. 更新文档

**更新一级目录 README**:

根据数据源所在的主类别，更新对应的一级目录 README 文件：

- 中国数据源：更新 `sources/china/README.md`
- 国际数据源：更新 `sources/international/README.md`
- 各国数据源：更新 `sources/countries/README.md`
- 学术数据源：更新 `sources/academic/README.md`
- 行业数据源：更新 `sources/sectors/README.md`

**注意**: 仅在一级目录（china, international, countries, academic, sectors）下维护 README 文件，子目录不需要 README。

在 README 中添加数据源条目，包含：
- 数据源名称和 ID
- 权威性评分
- 支持的数据格式
- 访问类型（开放/注册/受限）
- 指向 JSON 文件的相对路径

**示例**（`sources/china/README.md`）:
```markdown
### 金融财政 | Finance

#### 银行监管

1. **中国人民银行** (`china-pbc`) ⭐💎
   - 权威性：5.0
   - 数据格式：JSON, Excel, PDF
   - 访问类型：开放
   - [查看详情](finance/banking/pbc.json)

2. **国家金融监督管理总局** (`china-nfra`) ⭐💎
   - 权威性：5.0
   - 数据格式：Excel, PDF
   - 访问类型：开放
   - [查看详情](finance/banking/nfra.json)
```

**更新任务清单**:

在对应任务文件中标记完成状态。

例如，在 `tasks/china/finance.md` 中：

```markdown
### ✅ 1.2 国家金融监督管理总局 (`china-nfra`)
- **状态**: ✅ 已完成
- **完成日期**: 2025-12-04
- **文件**: `sources/china/finance/banking/nfra.json`
- **贡献者**: DataSource Hub Team
- **权威性**: 5.0
- **URL**: https://www.nfra.gov.cn/
```

**更新进度统计**:

根据数据源所属类别，更新以下统计文件中的数字（保持所有统计一致）：

**1. 根目录 README**（`README.md`）:
- 更新 badge 徽章（第8-10行）：
  - `Data Sources-57/950+` → `Data Sources-58/950+`
  - `Progress-6%` → 重新计算百分比
  - `Avg Quality-4.9/5.0` → 重新计算平均质量
- 更新总体统计表格（第106-111行）：
  - `| **总数据源** | 57 / 950+ | 6% |` → `| **总数据源** | 58 / 950+ | 6% |`
  - 更新对应类别行（国际/各国/中国/学术/行业）

**2. 一级目录 README**（`sources/{category}/README.md`）:
- 更新"已收录"数量（统计信息部分）
- 示例：`- **已收录**: 0` → `- **已收录**: 1`

**3. 任务清单 README**（`tasks/README.md`）:
- 更新对应类别的"完成"和"进度"列（第16-20行表格）
- 更新"总进度"（第4行）：`**总进度**: 57/950+ (6%)` → `**总进度**: 58/950+ (6%)`

**4. 中国数据源 README**（`tasks/china/README.md`，仅中国数据源需更新）:
- 更新对应领域的"完成"和"进度"列（第25-42行表格）
- 更新总体统计（第3-5行）：`**已完成**: 6个` → `**已完成**: 7个`

**5. 项目路线图**（`ROADMAP.md`）:
- 更新总体进度（第4行）：`**总体进度**: 57/950+ (6%)` → `**总体进度**: 58/950+ (6%)`
- 更新类别进度表格（第16-23行）
- 更新当前里程碑进度（如 `M1: 🚧 进行中 (57/100)` → `🚧 进行中 (58/100)`）

**更新原则**:
- 所有统计数字必须同步更新，保持一致性
- 进度百分比四舍五入到整数
- 平均质量 = 所有数据源质量评分的平均值

### 9. 提交前检查清单

- **文件验证**: Schema验证通过 | 完整性≥70% | URL可访问(primary_url必验)
- **文档更新**: 更新领域README | 任务文件标记完成 | 更新进度统计
- **质量检查**: 必需字段完整 | 双语内容完整 | 评分有据 | 分类正确
- **索引生成**(可选): 测试索引生成 | 新数据源出现在索引中
- **最终确认**: 文件保存在正确目录 | 命名规范 | 无TODO占位符

### 10. 自动推送到 GitLab

在完成所有验证和文档更新后，自动提交并推送更改。

**触发条件**：
- 新数据源创建成功且验证通过
- 数据源更新完成且验证通过
- 索引文件和文档已更新

**执行步骤**：
```bash
# 1. 添加所有更改
git add .

# 2. 创建提交（根据操作类型选择消息）
# 创建: git commit -m "feat: 添加{数据源名称}数据源 ({datasource-id})"
# 更新: git commit -m "update: 更新{数据源名称}数据源 ({datasource-id})"

# 3. 推送到远程仓库
git push origin feat/auto-push-git
```

**提交消息格式**：
- 新增数据源：`feat: 添加{name} ({id})`
- 更新数据源：`update: 更新{name} ({id})`
- 批量操作：`feat: 批量添加{领域}数据源 ({count}个)`

**注意事项**：
- 推送前确保所有验证通过；使用规范的提交消息；自动推送到当前分支

## 双语要求

- **中国数据源**: 必须提供中英双语（name, description, data_content）
- **国际数据源**: 至少提供英文，如有中文版则补充

## 关键原则

1. **准确性优先**: 必须实际访问网站提取信息，不编造数据
2. **URL 可访问**: 所有 URL 必须是真实可访问的地址
3. **质量有据**: 评分基于实际观察，不是猜测
4. **谨慎处理**: 不确定的信息标记为 null 或向用户询问

## 输出报告格式

根据操作类型（创建或更新）使用不同的报告格式：

### 创建操作报告

```
✅ 已创建 sources/{path}/{filename}.json

📁 数据源 ID: {datasource-id}
⭐ 平均质量评分: {score}/5.0
🔗 主要 URL: {primary_url}
📊 覆盖范围: {geographic scope}, {countries/regions}
📅 时间跨度: {start_year}-{end_year}
✅ Schema 验证: 通过

主要数据内容：
- {类别1} - {说明}
- {类别2} - {说明}
- {类别3} - {说明}
```

### 更新操作报告

```
✅ 已更新 sources/{path}/{filename}.json

📊 变更摘要：

  - 更新字段 ({数量}):
    * {字段名}: {旧值} → {新值}
    * {字段名}: 已添加
    * catalog_metadata.last_updated: {旧日期} → {新日期}

  - 保留字段:
    * quality.* (所有质量评分)
    * catalog_metadata.contributor
    * {其他保留的字段}

  - 数组新增:
    * tags: {新增的标签}
    * usage.use_cases: {新增的用例}

  - 备份位置: {filename}.backup
```

## 工作流程示例

详细的工作流程示例请参见：[reference/workflow-examples.md](reference/workflow-examples.md)

包括：
- **示例 1**: 使用 Web Search 的标准流程（WHO 数据源）
- **示例 2**: 使用 Playwright 的三层策略完整流程（国家统计局）

每个示例都展示了从用户输入到最终完成的完整步骤，包括工具选择、质量评估、验证和文档更新等环节。

如果需要更多 Playwright 使用场景（登录处理、交互内容提取等），详见 [playwright-workflow.md](playwright-workflow.md)