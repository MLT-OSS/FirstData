---
name: datasource-scraper
description: Extract or update datasource information from websites and convert to DataSource Hub JSON format. Supports upsert semantics - automatically creates new entries or updates existing ones. Use when the user provides a data source URL or name (e.g., "GenBank", "World Bank", "人民银行"). Outputs a validated JSON file following datasource-schema.json standard with authority level determination.
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
3. ✅ 确定权威等级
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

用户会输入数据源的名称（可能包括中英文）以及所属的类别，识别数据源。

**输入格式**：
- 数据源名称（中文/英文）或 URL
- 类别信息（主类别/子类别）

**识别逻辑**：
- 如果输入以 `http://` 或 `https://` 开头 → **URL 输入**，直接使用
- 否则 → **名字输入**，使用 WebSearch 搜索官方网站，用 AskUserQuestion 确认 URL

**重要**：记住用户输入的类别信息，在步骤5保存文件时会使用。

#### 步骤 2：采用两层策略获取页面内容

##### 第一层：Web Search 定位官网

使用 `WebSearch` 工具定位**该数据源权威的官方网站**：

- 搜索数据源的官方网站链接
- 确认网站的权威性和可靠性
- 获取主要页面URL

##### 第二层：WebFetch 或 Playwright 获取页面内容

根据网站特征选择合适的工具获取页面内容：

**方案 A：WebFetch**

适用于静态网页或服务端渲染的页面：
- 直接获取HTML内容
- 提取组织信息、关键 URL、数据覆盖范围、更新频率、许可协议等
- 速度快，资源消耗少

**方案 B：Playwright**

在以下情况使用 Playwright 浏览器自动化：
- JavaScript 渲染页面（WebFetch 返回内容很少或为空）
- 需要登录或认证才能查看内容
- 关键信息在交互式元素中（下拉菜单、折叠面板、Tab）
- 用户明确要求使用浏览器

---

### 2. 信息提取

从网页提取以下信息填充 JSON：

**核心字段**：
- **基础信息**: id, name (多语言), description
- **访问信息**: website, data_url, api_url (如有)
- **权威等级**: authority_level (government/international/research/market/commercial/other)
- **覆盖范围**: geographic_scope, country, domains, update_frequency
- **数据内容**: data_content 列表（中英双语）
- **搜索标签**: tags (中英文关键词、同义词)

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

### 3. 确定权威等级

根据数据源的组织类型确定 `authority_level` 字段值：

**可选值**：
- `government` - 政府机构（国家统计局、央行、监管机构等）
- `international` - 国际组织（联合国、世界银行、OECD等）
- `research` - 研究机构（大学、科研院所、学术联盟等）
- `market` - 市场机构（交易所、行业协会、评级机构等）
- `commercial` - 商业机构（数据服务商、咨询公司等）
- `other` - 其他类型

**判断原则**:
- 根据组织的官方性质和定位选择
- 政府和国际组织具有最高权威性
- 学术研究机构注重方法论严谨性
- 市场和商业机构提供行业专业数据
- 说明选择该等级的依据

---

### 4. 生成 JSON

- 参考 schema 文件: 见 [datasource-schema.json](reference/datasource-schema.json)
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

**优先级1：使用步骤1中记住的类别信息**（推荐）

使用步骤1中用户输入的类别信息（主类别/子类别）直接构建保存路径：

```
sources/{主类别}/{子类别}/{数据源ID}.json
```

例如：
- 输入类别：`international/health`
- 数据源ID：`who-gho`
- 保存路径：`sources/international/health/who-gho.json`

**类别路径映射表**（参考）：

| 主类别 | 子类别示例 | 完整路径示例 |
|-------|----------|-------------|
| international | health, economics, trade, energy, environment | `sources/international/{sub_cat}/` |
| countries | north-america, europe, asia, oceania, south-america, africa | `sources/countries/{sub_cat}/` |
| academic | economics, health, environment, social, biology, physics_chemistry | `sources/academic/{sub_cat}/` |
| sectors | energy, innovation_patents, education, agriculture_food, finance_markets | `sources/sectors/{sub_cat}/` |
| china | national, finance, economy, etc. | `sources/china/{sub_cat}/` |

**优先级2：使用 datasource-classifier Sub-Agent**（仅在步骤1无类别信息时）

如果步骤1中用户未提供类别信息，调用 `@datasource-classifier` 确定分类路径：

```
@datasource-classifier
请分析此数据源并确定分类路径:
- ID: {id}
- 组织: {organization.name} ({organization.type})
- 国家: {organization.country}
- 领域: {coverage.domains}
```

datasource-classifier 会返回推荐路径、分类理由和替代方案。

**优先级3：快速参考**（无法使用前两种方法时）

- 中国官方 → `sources/china/{domain}/{subdomain}/`
- 国际组织 → `sources/international/{domain}/`
- 学术机构 → `sources/academic/{domain}/`
- 其他国家 → `sources/countries/{continent}/{country}/`

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

#### 🚀 自动化脚本（推荐优先使用）

**第一步：运行自动化脚本更新所有进度统计**

在手动更新8.1和8.2之前，先运行自动化脚本更新所有进度统计数字：

```bash
# 自动更新所有进度统计文件（8.3 步骤）
python .claude/skills/datasource-scraper/scripts/update_all_docs.py

# 先预览变更，不实际修改（推荐先运行）
python .claude/skills/datasource-scraper/scripts/update_all_docs.py --dry-run

# 查看详细执行信息
python .claude/skills/datasource-scraper/scripts/update_all_docs.py --verbose
```

**脚本自动完成的任务（8.3 进度统计）：**

✅ **README.md** 更新：
- 徽章数字（Data Sources, Progress, Quality Rating）
- 总体统计表格（5个分类的当前数/进度）
- 已完成数据源列表的数量标题
- 项目状态表格（总进度、完成度、更新日期、质量评分）

✅ **tasks/README.md** 更新：
- 顶部总进度信息
- 按类别浏览表格（5个分类的完成数/进度）

✅ **ROADMAP.md** 更新：
- 顶部总进度信息
- 进度条可视化
- 总体进度概览表格（5个分类的完成数/进度）

**仍需手动完成的任务：**
- ⚠️ 8.1: 一级目录 README 数据源条目添加
- ⚠️ 8.2: 任务清单状态标记更新（📋 → ✅）
- ⚠️ 8.3.2: sources/{category}/README.md 数据源列表更新
- ⚠️ 8.3.4: tasks/china/README.md 领域统计更新（仅中国数据源）

**执行顺序建议：**
1. ✅ 运行自动化脚本（更新所有进度统计）
2. 📝 手动完成8.1（添加数据源条目）
3. 📝 手动完成8.2（标记任务状态）
4. 📝 如有需要，手动补充8.3.2和8.3.4

---

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

添加数据源条目，包含：数据源名称、ID、权威等级、数据格式、访问类型、相对路径链接。

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
- [ ] 权威等级准确（根据组织性质确定）
- [ ] 分类正确

#### ⭕ 索引生成（可选）
- [ ] 测试索引生成
- [ ] 新数据源出现在索引中

#### ✅ 最终确认（必须检查）
- [ ] 文件保存在正确目录
- [ ] 命名规范（使用 datasource ID）
- [ ] 无 TODO 占位符

---

### 10. 自动推送到 Git

在完成所有验证和文档更新后，自动提交并推送更改。

**只提交必要文件**：

```bash
# 只添加数据源相关文件（不添加其他文件）
git add sources/ tasks/ README.md ROADMAP.md indexes/

# 创建提交（根据操作类型选择消息）
# 新增：
git commit -m "feat: 添加{数据源名称}数据源 ({datasource-id})

📊 数据源信息：
- 类别: {category}
- 权威等级: {authority_level}
"

# 更新：
git commit -m "update: 更新{数据源名称}数据源 ({datasource-id})"

# 批量：
git commit -m "feat: 批量添加{领域}数据源 ({count}个)"

# 推送到远程仓库
git push
```

**重要**：
- ❌ 不使用 `git add .`（避免提交临时文件、缓存等）
- ✅ 只添加数据源相关的文件和目录
- ✅ 确保不提交 `.claude/` 目录下的临时文件

**提交消息格式**：
- 新增数据源：`feat: 添加{name} ({id})`
- 更新数据源：`update: 更新{name} ({id})`
- 批量操作：`feat: 批量添加{领域}数据源 ({count}个)`

---

## 双语要求

- **中国数据源**: 必须提供中英双语（name, description, data_content）
- **国际数据源**: 至少提供英文，如有中文版则补充

---

## 关键原则

1. **准确性优先**: 必须实际访问网站提取信息，不编造数据
2. **URL 可访问**: 所有 URL 必须是真实可访问的地址
3. **权威等级准确**: 根据组织实际性质确定 authority_level，有依据
4. **谨慎处理**: 不确定的信息标记为 null 或向用户询问

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
