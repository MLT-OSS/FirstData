---
name: datasource-scraper
description: Extract or update datasource information from websites and convert to DataSource Hub JSON format. Supports upsert semantics - automatically creates new entries or updates existing ones. Use when the user provides a data source URL or name (e.g., "GenBank", "World Bank", "人民银行"). Outputs a validated JSON file following datasource-schema.json standard with quality assessment.
---

# 数据源抓取器

从网站提取数据源信息并转换为 DataSource Hub 标准 JSON 格式。

**支持 Upsert 操作**：无论数据源是否已存在，都可以使用同一流程处理（自动创建或更新）。

---

## ⚠️ 重要：必须严格遵循完整的10步流程
**🔴 关键原则：每个数据源必须完成全部10个步骤后，才能处理下一个数据源**

### 严禁的错误做法 ❌
- ❌ 批量处理：先完成多个数据源的JSON生成，再统一更新文档
- ❌ 跳过步骤：完成验证后直接提交Git，跳过文档更新
- ❌ 延迟更新：所有数据源完成后再批量补充README和进度文件

### 正确的执行方式 ✅
对于**每一个**数据源，必须按顺序完成：

1. ✅ 获取网站内容
2. ✅ 信息提取
3. ✅ 质量评估
4. ✅ 生成JSON
5. ✅ Upsert操作（检测并创建/更新）
6. ✅ **验证（三项必须全部执行）**
7. ✅ 生成索引
8. ✅ **更新文档（必须立即执行，不得延后）**
   - 更新一级目录README
   - 更新任务清单文件（标记为完成）
   - 更新5个进度统计文件
9. ✅ **提交前检查清单（必须验证所有更新完成）**
10. ✅ 自动推送到Git

**完成上述10步后，再开始处理下一个数据源。**

---

## 核心工作流程

### 1. 获取网站内容

#### 步骤 1：识别输入类型

- 如果输入以 `http://` 或 `https://` 开头 → **URL 输入**，直接使用
- 否则 → **名字输入**，使用 WebSearch 搜索官方网站，用 AskUserQuestion 确认 URL

<!-- **详细流程**：参见 [workflow-examples.md](reference/workflow-examples.md) -->

#### 步骤 2：采用两层降级策略

##### 第一层：Web Search / WebFetch（主要策略）

结合使用 `WebSearch` 和 `WebFetch` 获取信息：

**Web Search 搜索**：
- "{组织名称} data/API/methodology/about" 等多角度搜索
- 快速获取概览信息和关键 URL
- 
**WebFetch 验证**：
- 直接访问 URL 提取静态页面详细内容
- 获取组织信息、关键 URL、数据覆盖范围、更新频率、许可协议等

##### 第二层：Playwright 浏览器自动化

**触发条件**（满足任一即可）:
- JavaScript 渲染页面（WebFetch 返回内容很少或为空）
- 需要登录或认证才能查看内容
- 关键信息在交互式元素中（下拉菜单、折叠面板、Tab）
- 用户明确要求使用浏览器

<!-- **详细操作流程**: 见 [data-acquisition.md](reference/data-acquisition.md) -->

**降级策略**:
```
第一层: WebSearch + WebFetch（静态内容）
  ↓ 如遇 JS 渲染/需要登录/交互内容
第二层: Playwright（浏览器自动化）→ 告知用户 → 持续反馈
```

---

### 2. 信息提取

从网页提取以下信息填充 JSON：

**核心字段**：
- **基础信息**: id, name (多语言), organization, description
- **访问信息**: primary_url, API, download options, access_level
- **覆盖范围**: geographic, temporal, domains, indicators
- **数据内容**: 分类列表（中英双语）
- **数据特征**: types, granularity, formats, languages
- **质量评估**: 6 个维度评分
- **许可协议**: license, commercial_use, restrictions
- **其他**: metadata standards, usage, contact, tags

**详细字段说明**: 见 [datasource-schema.json](reference/datasource-schema.json)

**不确定信息的处理**：
- **可选字段**：如果无法获取，直接删除该字段
- **允许 null 的字段**：可以设为 `null`
- **不允许 null 的字段**：必须提供有效值或删除字段
- **必填字段**：必须提供有效值，可以向用户询问

**参考示例**:
- `sources/china/national/nbs.json` - 国家统计局
- `sources/china/finance/banking/pbc.json` - 中国人民银行
- `sources/international/economics/worldbank.json` - 世界银行
---

### 3. 质量评估

按 1-5 星评分以下 6 个维度：
- `authority_level` - 来源权威性
- `methodology_transparency` - 方法论透明度
- `update_timeliness` - 更新及时性
- `data_completeness` - 数据完整性
- `documentation_quality` - 文档质量
- `citation_count` - 引用频次

**评分标准**: 见 [quality-criteria.md](reference/quality-criteria.md)

**评分原则**:
- 保守评估，有依据
- 只有真正顶级官方来源才给 5 星
- 生成时说明评分理由

---

### 4. 生成 JSON

- 参考 schema 文件: `reference/datasource-schema.json`
- 填充所有必填字段，尽可能填充可选字段

---

### 5. Upsert 操作（自动检测创建或更新）

**自动检测逻辑**：在保存文件前，使用生成的 `id` 字段在 `sources/` 目录中搜索现有文件：

- **未找到** → **创建新文件**（标准新建流程）
- **找到** → **更新文件**（智能合并 + 备份）

#### 更新操作要点

如果检测到已存在相同 ID 的数据源：

1. **创建备份**：`{文件名}.backup`（覆盖旧备份）
2. **智能合并**：
   - 更新 URL、API 文档等新信息
   - 合并 tags、use_cases 等数组字段（去重）
   - 保留原始创建日期和贡献者信息
3. **验证后保存**：合并结果通过 schema 验证后才更新
4. **删除备份**：验证成功后删除备份文件
5. **报告变更**：向用户展示哪些字段更新了、哪些保留了

<!-- **详细 Upsert 流程**: 见 [upsert-workflow.md](reference/upsert-workflow.md) -->

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
datasource-classifier 会返回推荐路径、分类理由和替代方案。

**快速参考**（无法使用 classifier 时）:
- 中国官方 → `sources/china/{domain}/{subdomain}/`
- 国际组织 → `sources/international/{domain}/`
- 学术机构 → `sources/academic/{domain}/`
- 其他国家 → `sources/countries/{continent}/{country}/`

<!-- **详细分类规则**: 见 `.claude/agents/datasource-classifier.md` 或 [upsert-workflow.md](reference/upsert-workflow.md) -->

---

### 6. 验证 ⚠️ 必须执行所有三项验证

**🔴 重要：以下三项验证必须全部执行，不可跳过任何一项！且每一项都需要打印结果**

#### 6.1 Schema 验证 ✅ 必须

```bash
python .claude/skills/datasource-scraper/scripts/validate.py sources/path/to/file.json --schema reference/datasource-schema.json
```
**必须通过**：JSON 格式符合 datasource-schema.json 标准

---

#### 6.2 URL 可访问性验证 ✅ 必须

```bash
python .claude/skills/datasource-scraper/scripts/verify_urls.py sources/path/to/file.json
```

验证字段：`primary_url`（必需）、`organization.website`、`api.documentation`、`support_url` 
**必须通过**：所有 URL 返回 200 状态码

---

#### 6.3 完整性检查 ✅ 必须

```bash
python scripts/check_completeness.py sources/path/to/file.json
```

**最低要求**：
- 必需字段: 100%
- 推荐字段: ≥80%
- 总体完成度: ≥70%

**如果不达标**: 补充缺失字段后重新检查

---

<!-- **详细验证指南**: 见 [validation-guide.md](reference/validation-guide.md) -->

⚠️ **验证检查点**：只有三项验证全部完成后，才能进入下一步

---

### 7. 生成索引

```bash
# 测试新数据源
python scripts/generate_indexes.py --test sources/path/to/file.json

# 生成完整索引
python .claude/skills/datasource-scraper/scripts/generate_indexes.py
```

生成 all-sources.json, by-domain.json, by-country.json, stats.json 等索引文件。

---

### 8. 更新文档

#### 8.1 更新一级目录 README

根据数据源所在的主类别，更新对应的一级目录 README 文件：

| 数据源类别 | README 文件路径 |
|-----------|----------------|
| 中国数据源 | `sources/china/README.md` |
| 国际数据源 | `sources/international/README.md` |
| 各国数据源 | `sources/countries/README.md` |
| 学术数据源 | `sources/academic/README.md` |
| 行业数据源 | `sources/sectors/README.md` |

**注意**: 仅在一级目录下维护 README 文件，子目录不需要 README。

添加数据源条目，包含：数据源名称、ID、权威性评分、数据格式、访问类型、相对路径链接。

#### 8.2 更新任务清单

在对应的任务文件中将任务状态从 `📋` 改为 `✅`：

| 数据源类别 | 任务文件路径 |
|-----------|-------------|
| 中国数据源 | `tasks/china/{领域}.md` |
| 国际组织 | `tasks/international.md` |
| 各国官方 | `tasks/countries.md` |
| 学术研究 | `tasks/academic.md` |
| 行业领域 | `tasks/sectors.md` |

#### 8.3 更新进度统计

同步更新以下 5 个文件中的统计情况（保持所有统计一致）：

1. **根目录 README**（`README.md`）：Badge 徽章 + 总体统计表格 + 已完成数据源列表
2. **一级目录 README**（`sources/{category}/README.md`）：已收录数量 + 已收录数据源列表
3. **任务清单 README**（`tasks/README.md`）：总进度 + 分类表
4. **中国数据源 README**（`tasks/china/README.md`，仅中国数据源）：领域统计
5. **项目路线图**（`ROADMAP.md`）：总进度 + 类别表格 + 里程碑进度

**更新原则**：
- 所有统计数字必须同步更新，保持一致性
- 进度百分比四舍五入到整数
- 平均质量 = 所有数据源质量评分的平均值

**详细更新指南**: 见 [documentation-update.md](reference/documentation-update.md)

---

### 9. 提交前检查清单 🔴 强制执行

**⚠️ 以下所有检查项必须全部完成，否则不允许提交到 Git！**

#### ✅ 文件验证（必须全部通过）
- [ ] Schema 验证通过
- [ ] 完整性 ≥70%（必需字段 100%，推荐字段 ≥80%）
- [ ] URL 可访问（primary_url 必须验证）

#### ✅ 文档更新（必须全部完成）
- [ ] 更新领域 README
- [ ] 任务文件标记完成（📋 → ✅）
- [ ] 更新进度统计（5 个文件：README.md, tasks/README.md, ROADMAP.md, sources/{category}/README.md, tasks/china/README.md）

#### ✅ 质量检查（必须符合标准）
- [ ] 必需字段完整
- [ ] 双语内容完整（中国/国际数据源）
- [ ] 评分有据
- [ ] 分类正确

#### ⭕ 索引生成（可选）
- [ ] 测试索引生成
- [ ] 新数据源出现在索引中

#### ✅ 最终确认（必须检查）
- [ ] 文件保存在正确目录
- [ ] 命名规范（使用 datasource ID）
- [ ] 无 TODO 占位符

<!-- **详细检查清单**: 见 [git-workflow.md](reference/git-workflow.md) -->

---

### 10. 自动推送到 Git

在完成所有验证和文档更新后，自动提交并推送更改。注意⚠️：一定要添加所有更改：git add .

**执行步骤**：
```bash
# 1. 添加所有更改
git add .

# 2. 创建提交（根据操作类型选择消息）
# 新增：
git commit -m "feat: 添加{数据源名称}数据源 ({datasource-id})"
# 更新：
git commit -m "update: 更新{数据源名称}数据源 ({datasource-id})"

# 3. 推送到远程仓库
git push origin feat/auto-push-git
```

**提交消息格式**：
- 新增数据源：`feat: 添加{name} ({id})`
- 更新数据源：`update: 更新{name} ({id})`
- 批量操作：`feat: 批量添加{领域}数据源 ({count}个)`

<!-- **详细 Git 工作流程**: 见 [git-workflow.md](reference/git-workflow.md) -->

---

## 双语要求

- **中国数据源**: 必须提供中英双语（name, description, data_content）
- **国际数据源**: 至少提供英文，如有中文版则补充

---

## 关键原则

1. **准确性优先**: 必须实际访问网站提取信息，不编造数据
2. **URL 可访问**: 所有 URL 必须是真实可访问的地址
3. **质量有据**: 评分基于实际观察，不是猜测
4. **谨慎处理**: 不确定的信息标记为 null 或向用户询问

---

## 输出报告格式

根据操作类型（创建或更新）使用不同的报告格式。

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
  - 更新字段 ({数量}): {字段名}: {旧值} → {新值}
  - 保留字段: quality.* (所有质量评分), contributor, created_date
  - 数组新增: tags, use_cases
  - 备份位置: {filename}.backup
```

<!-- **详细报告格式**: 见 [reporting-format.md](reference/reporting-format.md) -->

---

## 工作流程示例
详细的工作流程示例请参见：[workflow-examples.md](reference/workflow-examples.md)

包括：
- **示例 1**: 使用 Web Search 的标准流程（WHO 数据源）
- **示例 2**: 使用 Playwright 的完整流程（国家统计局）

每个示例都展示了从用户输入到最终完成的完整步骤。

---

<!-- ## Reference 文档索引

- [workflow-examples.md](reference/workflow-examples.md) - 完整工作流程示例（端到端）
- [data-acquisition.md](reference/data-acquisition.md) - 数据获取策略（步骤 1：包含 Playwright 指南）
- [information-extraction.md](reference/information-extraction.md) - 信息提取与 Schema 字段（步骤 2）
- [quality-criteria.md](reference/quality-criteria.md) - 质量评分标准（步骤 3）
- [upsert-workflow.md](reference/upsert-workflow.md) - Upsert 操作与目录结构（步骤 5）
- [validation-guide.md](reference/validation-guide.md) - 三项验证详细指南（步骤 6）
- [documentation-update.md](reference/documentation-update.md) - 文档更新详细指南（步骤 8）
- [git-workflow.md](reference/git-workflow.md) - Git 工作流程和提交检查清单（步骤 9-10）
- [reporting-format.md](reference/reporting-format.md) - 输出报告格式详细说明（通用） -->
