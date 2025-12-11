---
name: datasource-publisher
description: Detect changes in sources directory and publish updates across all documentation (steps 7-10). Updates 13 files including core progress docs (README.md, tasks/README.md, ROADMAP.md), category READMEs (sources/*/README.md), and task checklists (tasks/*.md). Generates indexes and commits to Git. Use after datasource-fetcher completes, or independently when sources directory has manual updates.
---

# 数据源发布管理器

专注于文档更新和版本控制。

**职责**：检测变化 → 更新文档 → 生成索引 → Git提交

---

## 工作流程（4步）

### 1. 检测变化

扫描sources目录，识别新增/修改的数据源：

```bash
# 统计各分类数量
find sources/{international,china,countries,academic,sectors} -name "*.json" | wc -l

# 检测新增（对比git status）
git status --porcelain sources/
```

读取每个JSON文件获取：数据源ID、名称、类别、质量评分等信息。

---

### 2. 更新文档

#### 2.1 核心进度文档（3个）

**README.md** - 根目录
- 徽章（第8-10行）：Data Sources, Progress, Quality
- 总体统计表格（~第106-111行）
- 更新已完成数据源标题（~第120, 142, 153，159，170行）注意：此处一定要更新！
<!-- - 项目状态表格（~第358-361行） -->

**tasks/README.md**
- 顶部总进度（第3-4行）
- 分类表格（~第16-21行）

**ROADMAP.md**
- 顶部总进度（第3-4行）
- 进度条（~第12行）：▓▓░░ 20个字符
- 分类表格（~第18-23行）

#### 2.2 数据源列表文档（5个）

**sources/{category}/README.md** - 添加新数据源条目

根据数据源类别，在对应README中添加：

```markdown
### 领域名称

1. **数据源名称** (`id`) ⭐💎
   - 权威性：X.X
   - 数据格式：CSV, JSON, Excel
   - 访问类型：开放
   - [查看详情](相对路径.json)
```

需要更新的文件：
- `sources/international/README.md`
- `sources/china/README.md`
- `sources/countries/README.md`
- `sources/academic/README.md`
- `sources/sectors/README.md`

#### 2.3 任务清单状态（5个）

**tasks/{category}.md** - 标记任务完成

找到对应数据源的任务行，将 `📋` 改为 `✅`：

```markdown
# 修改前
- 📋 World Bank - 世界银行

# 修改后
- ✅ World Bank - 世界银行
```

需要更新的文件：
- `tasks/international.md`
- `tasks/countries.md`
- `tasks/china/{领域}.md`
- `tasks/academic.md`
- `tasks/sectors.md`

---

### 3. 生成索引

```bash
python scripts/generate_indexes.py
```

生成 `indexes/all-sources.json` 等聚合文件。

---

### 4. Git提交

#### 检查清单

- [ ] 3个核心文档已更新进度数字
- [ ] sources/{category}/README.md 已添加新数据源
- [ ] tasks/*.md 已标记任务完成
- [ ] 所有数字一致

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

git push origin feat/batch_file_isolated
```

---

## 文档更新详解

### 如何添加数据源到 sources/*/README.md

1. 确定数据源类别和子领域
2. 在对应README找到子领域章节（如 ### 经济 | Economics）
3. 在列表末尾添加新条目，编号递增
4. 格式：名称(ID) 权威性 + 4项元数据 + 链接

### 如何标记 tasks/*.md 任务完成

1. 根据数据源ID在任务文件中搜索
2. 找到对应行（通常包含数据源名称）
3. 将行首的 📋 改为 ✅
4. 如果有进度百分比，同步更新

---

## 关键原则

✅ **全面更新**：
- 进度统计（3个文件）
- 数据源列表（5个sources/*/README.md）
- 任务状态（5个tasks/*.md）

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
