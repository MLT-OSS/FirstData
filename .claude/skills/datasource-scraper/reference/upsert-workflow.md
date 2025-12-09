# 数据源 Upsert 工作流程

## 概述

Skill 支持 **Upsert 语义**（类似 Python 的 `dict[key] = value`）：
- 如果数据源不存在 → **新建**
- 如果数据源已存在 → **更新**（智能合并）

**默认行为**：自动检测，无需用户指定操作类型。

---

## 完整流程

### 1. 检测现有数据源

在生成 JSON 数据后、保存文件前，搜索 `sources/` 所有子目录，查找是否已存在相同 `id` 的数据源文件。

**搜索范围**：
- `sources/china/**/*.json`
- `sources/international/**/*.json`
- `sources/countries/**/*.json`
- `sources/academic/**/*.json`
- `sources/sectors/**/*.json`

**注意**：忽略 `.backup` 后缀的备份文件。

---

### 2. 决定操作类型

- **未找到** → 执行**新建**操作（创建新文件）
- **找到** → 执行**更新**操作（智能合并）

---

### 3A. 新建数据源（CREATE）

标准新建流程：
1. 根据分类确定保存路径
2. 创建 JSON 文件
3. 验证文件
4. 报告创建成功

**输出示例**：
```
✅ 已创建 sources/international/health/who.json
📁 数据源 ID: who | ⭐ 质量: 4.8/5.0
🔗 URL: https://www.who.int/data
```

---

### 3B. 更新数据源（UPDATE）

更新流程包含以下步骤：

#### 3B.1 创建备份

**在任何修改前，必须先创建备份**：
- 备份文件名：`{原文件名}.backup`
- 每次更新覆盖旧备份（只保留最新）
- 如果合并失败，从备份恢复

示例：`pbc.json` → `pbc.json.backup`

#### 3B.2 智能合并数据

按照合并规则（见下文）合并现有数据和新抓取的数据。

#### 3B.3 验证合并结果

使用 `schemas/datasource-schema.json` 验证合并后的数据：
- ✅ **验证通过** → 保存更新
- ❌ **验证失败** → 中止操作，保留备份，不修改原文件

#### 3B.4 保存更新并报告

保存合并后的数据，生成变更摘要报告给用户。

---

## 数据合并规则

### 字段分类

| 字段类别 | 合并策略 | 字段示例 |
|---------|---------|---------|
| **不可变字段** | 保持不变 | `id` |
| **URL 字段** | 更新为新值 | `access.primary_url`, `organization.website`, `access.api.*` |
| **描述字段** | 选择更长/更详细的 | `description.en`, `description.zh` |
| **质量评分** | **保留现有值** ⚠️ | `quality.*` （手动评分 > 自动评分） |
| **数组字段** | 去重合并 | `tags`, `usage.use_cases`, `related_sources` |
| **时间范围** | 更新结束时间，保留起始 | `coverage.temporal.end_year` |
| **创建信息** | 保留原值 | `catalog_metadata.added_date`, `contributor` |
| **更新时间** | 设为当前日期 | `catalog_metadata.last_updated`, `verified_date` |

### 重要原则

1. **质量评分始终保留**：手动评分比自动抓取更准确，除非明确要求更新
2. **数组去重合并**：`tags`、`use_cases` 等数组字段，新旧数据去重后合并
3. **描述选优**：选择更详细的描述（通常是更长的）
4. **元数据追溯**：保留原始创建日期和贡献者，更新最后修改时间

---

## 变更报告

更新完成后，向用户报告变更摘要：

```
✅ 已更新 sources/china/finance/banking/pbc.json

📊 变更摘要：
  - 更新字段 (3):
    * access.primary_url: http://old → https://new
    * access.api.documentation: 已添加
    * catalog_metadata.last_updated: 2024-01-15 → 2025-12-09

  - 保留字段:
    * quality.* (所有质量评分)
    * catalog_metadata.contributor

  - 数组新增:
    * tags: banking, monetary-policy
    * usage.use_cases: Policy Making

  - 备份位置: pbc.json.backup
```

---

## 使用场景

### 场景 1：首次创建

```
用户输入: "抓取 https://www.example.org/data 数据源"
结果: 未找到现有文件 → 创建新文件
输出: ✅ 已创建 sources/international/economics/example-data.json
```

### 场景 2：更新现有数据源

```
用户输入: "抓取 https://www.who.int/data 数据源"
结果: 找到现有文件 → 备份 → 合并 → 更新
输出: ✅ 已更新 sources/international/health/who.json + 变更摘要
```

### 场景 3：自动 Upsert（推荐）

```
用户输入: "处理 https://www.pbc.gov.cn/ 数据源"  # 不指定操作类型
结果: 自动检测 → 找到现有文件 → 执行更新
输出: ✅ 已更新 sources/china/finance/banking/pbc.json
```

---

## 错误处理

### 验证失败

```
❌ 合并数据验证失败，操作已中止
错误: Missing required field: access.primary_url
💡 原文件未修改，备份已保留: pbc.json.backup
```

### 文件操作失败

```
❌ 文件操作失败: Permission denied
💡 从备份恢复: pbc.json.backup
```

---

## 工作流程图

```
开始 → 抓取信息 → 生成数据 → 提取ID
                                ↓
                        检测到已存在?
                    ↙ 是           否 ↘
              创建备份           确定路径
                  ↓                 ↓
              智能合并           创建新文件
                  ↓                 ↓
              验证结果           验证文件
                  ↓                 ↓
              保存更新           报告创建
                  ↓                 ↓
              报告变更            结束
                  ↓
                结束
```

---

## 注意事项

1. ⚠️ **质量评分不可覆盖**：除非明确要求，否则保留手动评分
2. 🔒 **ID 不可变更**：数据源 ID 在创建后不能修改
3. 📦 **只保留最新备份**：每次更新覆盖旧备份，不保留历史版本
4. ✅ **合并前必验证**：所有合并结果必须通过 schema 验证
5. 🚫 **备份文件被忽略**：验证脚本、索引生成器自动跳过 `.backup` 文件