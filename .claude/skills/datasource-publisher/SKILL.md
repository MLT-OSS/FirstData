---
name: datasource-publisher
description: Automated documentation sync using extract_sources_info.py script. (1) Runs script to scan all JSON files and generate sources_report.json. (2) Uses report to verify/update source indexes in sources/*/README.md. (3) Marks tasks complete in tasks/*.md. (4) Updates progress stats in core docs using report data. (5) Generates indexes. (6) Commits to Git. MUST use script - no manual counting or git status. Use when syncing docs with actual datasources.
---

# 数据源发布管理器

专注于文档更新和版本控制。

**职责**：检测变化 → 更新文档 → 生成索引 → Git提交

---

## 工作流程（4步）

### 1. 扫描所有数据源并读取元数据

**目标**：获取sources目录下所有数据源的完整信息。

**操作步骤**：

```bash
# 运行数据源信息提取脚本
python3 .claude/skills/datasource-publisher/scripts/extract_sources_info.py
```

**脚本输出**：

文件路径：`.claude/skills/datasource-publisher/scripts/sources_report.json`

包含内容：
- `total`: 总数据源数量
- `by_category`: 各分类数量统计（international/china/countries/academic/sectors）
- `by_subcategory`: 按子分类组织的完整数据源列表，每个数据源包含：
  - `id`: 数据源ID
  - `name_en`: 英文名称
  - `name_zh`: 中文名称
  - `authority`: 权威性评分
  - `path`: JSON文件相对路径

**使用方式**：
- 读取 `sources_report.json` 获取完整数据源信息
- 根据分类和子分类定位需要更新的README
- 使用数据源信息生成标准格式的README条目

**重要**：必须使用此脚本，不依赖git status，确保基于实际文件更新文档。

#### 类别映射规则

根据JSON文件路径确定类别和对应的文档文件：

| JSON 文件路径 | 主类别 README | 任务清单文件 | 示例 |
|--------------|--------------|------------|------|
| `sources/international/{sub}/` | `sources/international/README.md` | `tasks/international.md` | international/health |
| `sources/china/{domain}/` | `sources/china/README.md` | `tasks/china/{domain}.md` | china/finance |
| `sources/countries/{region}/` | `sources/countries/README.md` | `tasks/countries.md` | countries/asia |
| `sources/academic/{field}/` | `sources/academic/README.md` | `tasks/academic.md` | academic/economics |
| `sources/sectors/{industry}/` | `sources/sectors/README.md` | `tasks/sectors.md` | sectors/energy |

**注意**：从JSON文件路径可以直接推断出需要更新哪些文档文件。

---

### 2. 更新文档索引和状态

**重要**：按照2.1 → 2.2 → 2.3的顺序执行，不可跳过！

#### 2.1 检查并更新数据源列表索引（sources/*/README.md）

**必须完成**：确保每个JSON文件在对应的 `sources/{category}/README.md` 中都有条目。

**操作步骤**：

1. **读取脚本输出**：
   ```bash
   # 从步骤1生成的报告中读取数据源信息
   cat .claude/skills/datasource-publisher/scripts/sources_report.json
   ```

2. **确定目标文件**：根据category确定要更新的README
   - `international` → `sources/international/README.md`
   - `china` → `sources/china/README.md`
   - `countries` → `sources/countries/README.md`
   - `academic` → `sources/academic/README.md`
   - `sectors` → `sources/sectors/README.md`

3. **为每个分类更新README**：
   - 读取 `by_subcategory[category]` 获取该分类的所有子分类和数据源
   - 读取对应的README文件
   - 定位到子领域章节（如 `### 经济 | Economics`）
   - 检查每个数据源是否已有条目
   - 如缺失，按以下格式添加：

```markdown
### 子领域名称

N. **{name_en}** (`{id}`) ⭐💎
   - 权威性：{authority}
   - 数据格式：{data_formats}
   - 访问类型：{access_level}
   - [查看详情]({relative_path})
```

4. **图标规则**：
   - authority >= 5.0: `⭐💎`
   - authority >= 4.5: `⭐`
   - authority < 4.5: 无图标

5. **访问类型映射**：
   - `open` → 开放
   - `academic` → 学术注册
   - `registration` → 需注册
   - `subscription` → 订阅
   - `controlled` → 受控访问

**必须为每个数据源都检查并确保有条目，不可跳过！**

#### 2.2 检查并更新任务完成状态（tasks/*.md）

**必须完成**：确保每个JSON文件对应的任务在 `tasks/{category}.md` 中标记为完成（✅）。

**操作步骤**：

1. **读取脚本输出**：
   - 从 `sources_report.json` 的 `by_category` 获取各分类的数据源列表
   - 使用 `name_en` 和 `name_zh` 定位任务行

2. **确定目标文件**：根据category确定任务文件
   - `international` → `tasks/international.md`
   - `china` → `tasks/china/{具体领域}.md`（根据subcategory确定）
   - `countries` → `tasks/countries.md`
   - `academic` → `tasks/academic.md`
   - `sectors` → `tasks/sectors.md`

3. **为每个数据源标记完成**：
   - 读取对应的任务文件
   - 使用 `name_en` 或 `name_zh` 搜索任务行
   - 检查行首是否为 `📋`
   - 如果是 `📋`，替换为 `✅`

```markdown
# 修改前
- 📋 World Bank - 世界银行

# 修改后
- ✅ World Bank - 世界银行 ⭐💎
```

4. **更新分类统计**：
   - 更新任务文件顶部的完成数量
   - 更新各子领域的进度百分比
   - 使用 `by_category` 中的统计数字

**必须为每个数据源都检查并确保标记为完成，不可跳过！**


#### 2.3 更新核心进度统计（README.md, tasks/README.md, ROADMAP.md）

**必须完成**：在完成2.1和2.2后，使用脚本统计数字更新核心文档。

**数据来源**：
```bash
# 从脚本输出读取统计数字
# total: 总数据源数量
# by_category: 各分类数量
cat .claude/skills/datasource-publisher/scripts/sources_report.json | jq '.by_category'
```

**更新内容**：

**README.md** - 根目录
- 徽章（第8行）：`[![Data Sources](https://img.shields.io/badge/Data%20Sources-{total}%2F950+-blue.svg)]`
- 总体统计表格（~第106-111行）：
  - 总数据源：`{total} / 950+`
  - 国际组织：`{by_category.international} / 100+`
  - 各国官方：`{by_category.countries} / 200+`
  - 中国数据源：`{by_category.china} / 488`
  - 学术研究：`{by_category.academic} / 50+`
  - 行业领域：`{by_category.sectors} / 150+`
- 已完成数据源标题（~第120, 142, 153, 159, 170行）：更新各分类数量

**tasks/README.md**
- 顶部总进度（第4行）：`**总进度**: {total}/950+ ({progress}%)`
- 分类表格（~第16-21行）：使用 `by_category` 数字更新完成列

**ROADMAP.md**
- 顶部总进度（第4行）：`**总体进度**: {total}/950+ ({progress}%)`
- 进度条（第13行）：根据 `progress = (total / 950) * 100` 计算
  - 每5%一个▓符号，共20个字符
  - 例如：11% = ▓▓░░░░░░░░░░░░░░░░░░
- 分类表格（~第18-23行）：使用 `by_category` 数字更新完成列

**重要**：确保所有文档中的数字与 `sources_report.json` 完全一致！

---

### 3. 生成索引

```bash
python scripts/generate_indexes.py
```

生成 `indexes/all-sources.json` 等聚合文件。

---

### 4. Git提交

#### 提交前检查清单

**必须全部完成才能提交！**

- [ ] **步骤1完成**：已扫描所有JSON文件，了解实际数据源情况
- [ ] **步骤2.1完成**：sources/{category}/README.md 中每个JSON文件都有对应条目
- [ ] **步骤2.2完成**：tasks/*.md 中每个数据源都标记为完成（✅）
- [ ] **步骤2.3完成**：核心文档（README.md, tasks/README.md, ROADMAP.md）的统计数字已更新
- [ ] **数据一致性**：所有文档中的数字与实际JSON文件数量一致
- [ ] **索引生成**：已运行 `python scripts/generate_indexes.py`

#### 执行提交

```bash
git add .

# 单个数据源
git commit -m "feat: 添加{name}数据源 ({id})

📊 数据源信息：
- 类别: {category}
- 质量: {score}/5.0

🤖 Generated with Claude Code"

# 批量
git commit -m "feat: 批量添加{领域}数据源 ({count}个)"

git push origin feat/batch_file_isolate
```


## 关键原则

✅ **必须使用自动化脚本**：
- **步骤1必须运行**：`python3 .claude/skills/datasource-publisher/scripts/extract_sources_info.py`
- 生成标准化报告：`.claude/skills/datasource-publisher/scripts/sources_report.json`
- 所有后续步骤都基于此报告
- **禁止手动统计或使用git status**

✅ **基于实际数据源文件进行更新**：
- 不依赖git status
- 扫描所有实际存在的JSON文件
- 确保文档与实际文件完全一致

✅ **必须全面更新（按顺序执行，不可跳过）**：

**步骤1** - 运行脚本扫描：
- 执行 `extract_sources_info.py`
- 生成 `sources_report.json`
- 获取完整的数据源元数据

**步骤2.1** - 数据源列表索引（5个sources/*/README.md）：
- sources/international/README.md
- sources/china/README.md
- sources/countries/README.md
- sources/academic/README.md
- sources/sectors/README.md
- **验证每个JSON都有对应条目**

**步骤2.2** - 任务完成状态（5+个tasks/*.md）：
- tasks/international.md
- tasks/countries.md
- tasks/china/{领域}.md
- tasks/academic.md
- tasks/sectors.md
- **验证每个数据源都标记为✅**

**步骤2.3** - 核心进度统计（3个）：
- README.md
- tasks/README.md
- ROADMAP.md
- **基于实际统计数字更新**

**重要**：必须按2.1→2.2→2.3顺序执行，先确保索引完整，再更新统计！

❌ **不做什么**：
- 不获取数据
- 不生成JSON
- 不验证数据

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
    "tasks/README.md",
    "ROADMAP.md",
    "sources/international/README.md",
    "tasks/international.md"
  ],
  "git": {
    "commit": "abc123",
    "message": "feat: 批量添加国际组织数据源 (2个)",
    "pushed": true
  }
}
```
