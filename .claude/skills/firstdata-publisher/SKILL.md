---
name: firstdata-publisher
description: Automated documentation sync using check_and_compare.py script. (1) Runs script to scan JSON files, compare with docs, and generate comparison_report.json with missing entries and stats mismatches. (2) Uses report recommendations to add missing entries in sources/*/README.md. (3) Updates progress stats in core docs. (4) Generates indexes. (5) Optional Git commit. MUST use script - no manual counting or git status. Use when syncing docs with actual datasources.
---
# 数据源发布管理器

专注于文档更新和版本控制。

**职责**：检测变化 → 更新文档 → 生成索引 → (可选)Git提交

---

## 工作流程（2步 + 1可选步骤）

### 1. 扫描数据源并对比文档差异

**目标**：获取sources目录下所有数据源信息，并对比文档中的条目和统计数字，识别缺失和错误。

**操作步骤**：

```bash
# 运行数据源检查和对比脚本
python3 .claude/skills/datasource-publisher/scripts/check_and_compare.py
```

**脚本输出**：

文件路径：`.claude/skills/datasource-publisher/scripts/comparison_report.json`

包含内容：

- `summary`: 各分类的实际数量、文档中的数量、差异对比
- `missing_in_docs`: 文档中缺失的数据源详细信息（按分类组织）
  - 每个数据源包含：`id`, `name_en`, `name_zh`, `authority`, `path`, `category`, `subcategory`
- `stats_mismatch`: 核心文档中统计数字错误的详情
- `recommendations`: 自动生成的更新建议
  - `add_entries`: 需要添加条目的文件和数据源列表
  - `update_stats`: 需要更新统计数字的文件

**使用方式**：

- 读取 `comparison_report.json` 获取完整的差异分析
- 使用 `recommendations` 字段获取具体的更新指令
- 使用 `missing_in_docs[category]` 获取需要添加的数据源信息
- 使用 `stats_mismatch` 获取需要更正的统计数字

**重要**：必须使用此脚本，不依赖git status，确保基于实际文件和文档对比更新。

#### 类别映射规则

根据JSON文件路径确定类别和对应的文档文件：

| JSON 文件路径                                  | 主类别 README                                     | 示例                 |
| ---------------------------------------------- | ------------------------------------------------- | -------------------- |
| `src/firstdata/sources/international/{sub}/` | `src/firstdata/sources/international/README.md` | international/health |
| `src/firstdata/sources/china/{domain}/`      | `src/firstdata/sources/china/README.md`         | china/finance        |
| `src/firstdata/sources/countries/{region}/`  | `src/firstdata/sources/countries/README.md`     | countries/asia       |
| `src/firstdata/sources/academic/{field}/`    | `src/firstdata/sources/academic/README.md`      | academic/economics   |
| `src/firstdata/sources/sectors/{industry}/`  | `src/firstdata/sources/sectors/README.md`       | sectors/energy       |

**注意**：从JSON文件路径可以直接推断出需要更新哪些文档文件。

---

### 2. 更新文档索引和状态

**重要**：按照2.1 → 2.2的顺序执行，不可跳过！

#### 2.1 检查并更新数据源列表索引（src/firstdata/sources/*/README.md）

**必须完成**：确保每个JSON文件在对应的 `sources/{category}/README.md` 中都有条目。

**操作步骤**：

1. **读取对比报告**：

   ```bash
   # 从步骤1生成的对比报告中读取缺失条目信息
   cat .claude/skills/datasource-publisher/scripts/comparison_report.json
   ```
2. **确定目标文件**：从 `recommendations` 中获取需要更新的文件列表

   - 筛选 `action == "add_entries"` 的建议
   - 获取 `file` 字段（如 `sources/china/README.md`）
   - 获取 `sources` 字段（需要添加的数据源列表）
3. **为每个分类添加缺失的条目**：

   - 读取 `missing_in_docs[category]` 获取该分类缺失的数据源
   - 读取对应的README文件
   - 根据 `subcategory` 定位到子领域章节（如 `### 📈 经济 Economics`）
   - 按以下格式添加缺失的数据源：

```markdown
#### {name_en} - {name_zh}
- **文件**: [{filename}]({relative_path_to_json}) {icon}
- **权威等级**: {authority_level}
- **数据格式**: {data_formats}
- **访问类型**: {access_level_zh}
- **涵盖**: {coverage_info}（从JSON的description或data_content提取）
- **特色**: {features}（从JSON的description或data_content提取）
```

4. **图标规则**（基于authority_level）：

   - `international`, `government` → `⭐💎`
   - `academic`, `research` → `⭐`
   - `industry`, `commercial` → 无图标
5. **访问类型映射**：

   - `open` → 开放
   - `academic` → 学术注册
   - `registration` → 需注册
   - `subscription` → 订阅
   - `controlled` → 受控访问

**重要**：

- 保留README现有的详细格式，不要改为简化格式
- 必须从JSON文件中读取完整信息（涵盖、特色等）
- filename从path中提取（如：`economics/worldbank.json`）
- 如果JSON中没有某些详细信息，可以简化为基本格式

**必须为每个数据源都检查并确保有条目，不可跳过！**

#### 2.2 更新核心进度统计（README.md, src/firstdata/sources/*/README.md）

**必须完成**：在完成2.1后，使用对比报告中的统计数字更新核心文档和分类README。

**数据来源**：

```bash
# 从对比报告读取统计数字和更新建议
# summary: 各分类的实际数量
# stats_mismatch: 需要更正的统计数字（包含分类README）
# recommendations: 自动生成的更新建议（筛选 action == "update_stats"）
cat .claude/skills/datasource-publisher/scripts/comparison_report.json
```

**更新内容**：

**README.md** - 根目录

- 徽章（第8行）：使用 `summary` 中计算的总数（将所有分类的 `actual` 相加）
  - `[![Data Sources](https://img.shields.io/badge/Data%20Sources-{total}%2F950+-blue.svg)]`
- 总体统计表格（~第106-111行）：
  - 总数据源：`{total} / 950+`（total = sum of all summary.*.actual）
  - 国际组织：`{summary.international.actual} / 100+`
  - 各国官方：`{summary.countries.actual} / 200+`
  - 中国数据源：`{summary.china.actual} / 488`
  - 学术研究：`{summary.academic.actual} / 50+`
  - 行业领域：`{summary.sectors.actual} / 150+`
- 已完成数据源标题（~第120, 142, 153, 159, 170行）：更新各分类数量

**src/firstdata/sources/china/README.md**

- 顶部统计（第3-5行）：
  - `**已完成**: {summary.china.actual}个`
  - `**进度**: {progress}%`（progress = (actual / 415) * 100）
- 进度条（第13行）：`当前完成: {summary.china.actual} 个`
- 分类表格（第26-45行）：使用实际的分类数量更新各领域的完成数和进度百分比

**src/firstdata/sources/sectors/README.md**

- 顶部统计（第4-6行）：
  - `**已完成**: {summary.sectors.actual}个`
  - `**进度**: {progress}%`（progress = (actual / 126) * 100）
- 进度条（第14行）：`当前完成: {summary.sectors.actual} 个`
- ISIC分类表格（第25-46行）：使用实际的ISIC分类数量更新各行业的完成数和进度百分比

**src/firstdata/sources/countries/README.md**

- 顶部统计（第13行）：`**JSON文件**: {summary.countries.actual}个数据源已创建`
- 进度条（第17行）：`当前完成: {summary.countries.actual} 个`

**重要**：确保所有文档中的数字与 `comparison_report.json` 的 `summary.*.actual` 完全一致！

---

### 3. 生成索引

```bash
python scripts/generate_indexes.py
```

生成 `indexes/all-sources.json` 等聚合文件。

---

### 4. Git提交（可选步骤）

**⚠️ 注意**：此步骤为可选。用户可以选择：

- ✅ **立即提交**：完成文档更新后直接提交到Git
- ⏸️ **稍后手动提交**：检查修改后再自行决定何时提交

#### 提交前检查清单

**如果选择提交，建议完成以下检查**：

- [ ] **步骤1完成**：已扫描所有JSON文件，了解实际数据源情况
- [ ] **步骤2.1完成**：src/firstdata/sources/{category}/README.md 中每个JSON文件都有对应条目
- [ ] **步骤2.2完成**：核心文档（README.md）的统计数字已更新
- [ ] **数据一致性**：所有文档中的数字与实际JSON文件数量一致
- [ ] **索引生成**：已运行 `python scripts/generate_indexes.py`

#### 执行提交（可选）

**只提交必要文件**：

```bash
# 只添加数据源相关文件（不添加其他文件）
git add src/firstdata/sources/ src/firstdata/indexes/ README.md

# 单个数据源
git commit -m "feat: 添加{name}数据源 ({id})

📊 数据源信息：
- 名称: {name_zh} ({name_en})
- 权威等级: {authority}
- 类别: {category}
"

# 批量
git commit -m "feat: 批量添加{领域}数据源 ({count}个)"

git push
```

**重要**：

- ❌ 不使用 `git add .`（避免提交临时文件、缓存等）
- ✅ 只添加数据源相关的文件和目录
- ✅ 确保不提交 `.claude/` 目录下的临时文件

## 关键原则

✅ **必须使用自动化脚本**：

- **步骤1必须运行**：`python3 .claude/skills/datasource-publisher/scripts/check_and_compare.py`
- 生成标准化对比报告：`.claude/skills/datasource-publisher/scripts/comparison_report.json`
- 所有后续步骤都基于此对比报告
- **禁止手动统计或使用git status**

✅ **基于实际数据源文件和文档对比进行更新**：

- 不依赖git status
- 扫描所有实际存在的JSON文件
- 对比文档中的现有条目
- 识别缺失和错误
- 确保文档与实际文件完全一致

✅ **必须全面更新（按顺序执行，不可跳过）**：

**步骤1** - 运行脚本扫描和对比：

- 执行 `check_and_compare.py`
- 生成 `comparison_report.json`
- 获取完整的数据源元数据和文档差异分析

**步骤2.1** - 数据源列表索引（5个 src/firstdata/sources/*/README.md）：

- src/firstdata/sources/international/README.md
- src/firstdata/sources/china/README.md
- src/firstdata/sources/countries/README.md
- src/firstdata/sources/academic/README.md
- src/firstdata/sources/sectors/README.md
- **验证每个JSON都有对应条目**

**步骤2.2** - 核心进度统计（1个）：

- README.md
- **基于实际统计数字更新**

**步骤3** - 生成索引：

- 运行 `python scripts/generate_indexes.py`
- 生成聚合索引文件

**步骤4（可选）** - Git提交：

- 用户可选择是否执行
- 如果执行，按照提交指南进行

**重要**：必须按2.1→2.2→3顺序执行，先确保索引完整，再更新统计！

❌ **不做什么**：

- 不获取数据
- 不生成JSON
- 不验证数据
- 不强制要求Git提交（由用户决定）

---

## 输出报告

```json
{
  "status": "success",
  "changes": {
    "new": ["intl-worldbank", "intl-imf"],
    "updated": []
  },
  "files_updated": [
    "README.md",
    "src/firstdata/sources/international/README.md"
  ],
  "git": {
    "executed": false,
    "note": "用户选择稍后手动提交"
  }
}
```

**注意**：如果用户选择执行Git提交，git字段将包含提交信息：

```json
{
  "git": {
    "executed": true,
    "commit": "abc123",
    "message": "feat: 批量添加国际组织数据源 (2个)",
    "pushed": true
  }
}
```
