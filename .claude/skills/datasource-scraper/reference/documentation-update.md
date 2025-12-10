# 文档更新指南

在完成数据源验证后，需要更新项目文档以反映新的数据源。

## 更新流程概览

```
1. 更新一级目录 README
   ↓
2. 更新任务清单
   ↓
3. 更新进度统计（5个文件）
   ↓
4. 验证所有统计数字一致
```

---

## 1. 更新一级目录 README

### 确定要更新的 README

根据数据源所在的主类别，更新对应的一级目录 README 文件：

| 数据源类别 | README 文件路径 |
|-----------|----------------|
| 中国数据源 | `sources/china/README.md` |
| 国际数据源 | `sources/international/README.md` |
| 各国数据源 | `sources/countries/README.md` |
| 学术数据源 | `sources/academic/README.md` |
| 行业数据源 | `sources/sectors/README.md` |

**注意**：仅在一级目录下维护 README 文件，子目录不需要 README。

### 添加数据源条目

在对应的领域章节下添加新的数据源条目。

#### 条目格式

```markdown
### {领域名称} | {英文名}

#### {子领域}（如适用）

{序号}. **{数据源名称}** (`{datasource-id}`) {徽章}
   - 权威性：{authority_level}/5.0
   - 数据格式：{formats}
   - 访问类型：{access_level}
   - [查看详情]({相对路径})
```

#### 徽章说明

- `⭐` - 权威性 ≥ 4.5
- `💎` - 官方数据源（organization.type = "government" 或 "international_organization"）
- `🔓` - 完全开放访问（access_level = "open"）
- `🔐` - 需要注册（access_level = "registration_required"）

#### 示例 1：中国数据源

**文件**：`sources/china/README.md`

```markdown
### 金融财政 | Finance

#### 银行监管

1. **中国人民银行** (`china-pbc`) ⭐💎🔓
   - 权威性：5.0/5.0
   - 数据格式：JSON, Excel, PDF
   - 访问类型：开放
   - [查看详情](finance/banking/pbc.json)

2. **国家金融监督管理总局** (`china-nfra`) ⭐💎🔓
   - 权威性：5.0/5.0
   - 数据格式：Excel, PDF
   - 访问类型：开放
   - [查看详情](finance/banking/nfra.json)
```

#### 示例 2：各国数据源

**文件**：`sources/countries/README.md`

```markdown
### 北美洲 | North America

#### 美国 | United States

1. **美国人口普查局** (`usa-census-bureau`) ⭐💎🔓
   - 权威性：5.0/5.0
   - 数据格式：CSV, JSON, Excel
   - 访问类型：开放
   - [查看详情](north-america/usa/census-bureau.json)

2. **美国国家经济研究局** (`usa-nber`) ⭐🔓
   - 权威性：4.8/5.0
   - 数据格式：Excel, Stata, CSV
   - 访问类型：开放
   - [查看详情](north-america/usa/nber.json)
```

---

## 2. 更新任务清单

在对应的任务文件中将任务状态从 `📋` 改为 `✅`。

### 任务文件映射

| 数据源类别 | 任务文件路径 |
|-----------|-------------|
| 中国数据源 | `tasks/china/{领域}.md` (如 `tasks/china/finance.md`) |
| 国际组织 | `tasks/international.md` |
| 各国官方 | `tasks/countries.md` |
| 学术研究 | `tasks/academic.md` |
| 行业领域 | `tasks/sectors.md` |

### 标记方式

**之前**：
```markdown
- 📋 World Bank Open Data - 世界银行开放数据
```

**之后**：
```markdown
- ✅ World Bank Open Data - 世界银行开放数据
```

---

## 3. 更新进度统计

所有统计数字必须同步更新，保持一致性。需要更新以下 5 个文件：

### 3.1 根目录 README (`README.md`)

#### 更新位置 1：Badge 徽章（第 8-10 行）

**之前**：
```markdown
![Data Sources](https://img.shields.io/badge/Data_Sources-57/950+-blue)
![Progress](https://img.shields.io/badge/Progress-6%25-yellow)
![Avg Quality](https://img.shields.io/badge/Avg_Quality-4.9/5.0-brightgreen)
```

**之后**（假设新增 1 个数据源，质量评分 4.8）：
```markdown
![Data Sources](https://img.shields.io/badge/Data_Sources-58/950+-blue)
![Progress](https://img.shields.io/badge/Progress-6%25-yellow)
![Avg Quality](https://img.shields.io/badge/Avg_Quality-4.9/5.0-brightgreen)
```

**计算方式**：
- 数据源数量：简单 +1
- 进度百分比：`(新总数 / 950) * 100`，四舍五入
- 平均质量：`(旧总分 + 新评分) / 新总数`，保留一位小数

#### 更新位置 2：总体统计表格（第 106-111 行）

**之前**：
```markdown
| **总数据源** | 57 / 950+ | 6% |
| 国际组织 | 10 / 150+ | 7% |
| 各国官方 | 8 / 400+ | 2% |
```

**之后**（假设新增国际数据源）：
```markdown
| **总数据源** | 58 / 950+ | 6% |
| 国际组织 | 11 / 150+ | 7% |
| 各国官方 | 8 / 400+ | 2% |
```

### 3.2 一级目录 README (`sources/{category}/README.md`)

更新"已收录"数量。

**示例**（`sources/countries/README.md`）：

**之前**：
```markdown
## 统计信息

- **已收录**: 8 个数据源
- **覆盖地区**: 北美、欧洲、亚洲
```

**之后**：
```markdown
## 统计信息

- **已收录**: 9 个数据源
- **覆盖地区**: 北美、欧洲、亚洲
```

### 3.3 任务清单 README (`tasks/README.md`)

#### 更新位置 1：总进度（第 4 行）

**之前**：
```markdown
**总进度**: 57/950+ (6%)
```

**之后**：
```markdown
**总进度**: 58/950+ (6%)
```

#### 更新位置 2：分类进度表格（第 16-20 行）

**之前**：
```markdown
| 国际组织 | 150+ | 10 | 7% | [查看详情](international.md) |
```

**之后**：
```markdown
| 国际组织 | 150+ | 11 | 7% | [查看详情](international.md) |
```

### 3.4 中国数据源任务清单（`tasks/china/README.md`，仅中国数据源）

如果是中国数据源，需要额外更新此文件。

#### 更新位置 1：总体统计（第 3-5 行）

**之前**：
```markdown
**已完成**: 6个
**总计划**: 50+个
**进度**: 12%
```

**之后**：
```markdown
**已完成**: 7个
**总计划**: 50+个
**进度**: 14%
```

#### 更新位置 2：领域进度表格（第 25-42 行）

**之前**：
```markdown
| 金融财政 | 2 | 4% |
```

**之后**：
```markdown
| 金融财政 | 3 | 6% |
```

### 3.5 项目路线图（`ROADMAP.md`）

#### 更新位置 1：总体进度（第 4 行）

**之前**：
```markdown
**总体进度**: 57/950+ (6%)
```

**之后**：
```markdown
**总体进度**: 58/950+ (6%)
```

#### 更新位置 2：类别进度表格（第 16-23 行）

**之前**：
```markdown
| 国际组织 | 10/150+ | 7% |
```

**之后**：
```markdown
| 国际组织 | 11/150+ | 7% |
```

#### 更新位置 3：当前里程碑进度（如第 30 行）

**之前**：
```markdown
**M1: 基础数据源收集** 🚧 进行中 (57/100)
```

**之后**：
```markdown
**M1: 基础数据源收集** 🚧 进行中 (58/100)
```

---

## 4. 更新原则

### 一致性检查

所有统计数字必须保持一致：
- 总数据源数量在所有文件中相同
- 各类别数据源之和 = 总数据源数量
- 进度百分比计算准确

### 计算公式

**进度百分比**：
```
进度 = (完成数量 / 计划数量) × 100，四舍五入到整数
```

**平均质量评分**：
```
平均质量 = 所有数据源质量评分之和 / 数据源总数，保留一位小数
```

### 更新检查清单

完成后使用此清单验证：

- [ ] `README.md` - Badge 和总体统计表格
- [ ] `sources/{category}/README.md` - 已收录数量
- [ ] `tasks/README.md` - 总进度和分类表格
- [ ] `tasks/china/README.md` - 中国数据源统计（仅中国数据源）
- [ ] `ROADMAP.md` - 总进度、类别表格、里程碑进度
- [ ] 所有数字一致且计算正确

---

## 常见问题

### Q1: 如何确定数据源属于哪个类别？
**A**: 使用 `@datasource-classifier` sub-agent 或参考数据源文件的保存路径。

### Q2: 进度百分比如何计算？
**A**: `(完成数量 / 计划数量) × 100`，四舍五入到整数。例如：`(58 / 950) × 100 = 6.1% ≈ 6%`

### Q3: 如果忘记更新某个文件会怎样？
**A**: 统计数据会不一致，影响项目进度跟踪。建议使用更新检查清单确保所有文件都更新。

### Q4: 平均质量评分如何计算？
**A**: 所有数据源的质量评分之和除以数据源总数，保留一位小数。需要重新计算而非简单平均。
