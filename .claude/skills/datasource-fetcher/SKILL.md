---
name: datasource-fetcher
description: Extract datasource information from websites and generate validated JSON files (steps 1-6 only). Designed for isolated execution in temporary directories - focuses purely on data acquisition and validation without touching documentation or Git. Uses direct overwrite mode (no merging with existing files) and outputs standardized JSON reports. Use for batch processing where each datasource runs in isolation, or for standalone data fetching.
---

# 数据源获取器 (Datasource Fetcher)

纯粹的数据源获取和验证工具，专注于数据质量。

**核心特点**：
- ✅ 只负责数据获取（步骤1-6）
- ✅ 不涉及文档更新
- ✅ 不涉及Git操作
- ✅ 可在任何目录独立运行
- ✅ 输出标准化JSON报告

---

## 工作流程（6步）

### 1. 获取网站内容

#### 步骤 1：确认输入数据源

用户会输入数据源的名称（可能包括中英文）以及所属的类别，识别数据源。

**输入格式**：
- 数据源名称（中文/英文）
- 类别信息（主类别/子类别）

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

### 2. json填充

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

**参考示例**: 现有的 sources/ 目录下的JSON文件，如果要进行参考。只使用一个示例，避免混淆。

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

- 参考 schema 文件: [datasource-schema.json](reference/datasource-schema.json)
- 填充所有必填字段，尽可能填充可选字段
- 确保符合JSON格式规范

---

### 5. 保存文件

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

如果步骤1中用户未提供类别信息且可用classifier，调用 `@datasource-classifier`：

```
@datasource-classifier
请分析此数据源并确定分类路径:
- ID: {id}
- 组织: {organization.name} ({organization.type})
- 国家: {organization.country}
- 领域: {coverage.domains}
```

#### 保存操作

**直接覆盖模式**：

- 根据分类路径直接保存JSON文件
- 如果文件已存在，直接覆盖（不进行合并或备份）
- 文件命名：`{分类路径}/{数据源名称}.json`

**操作步骤**:
1. 使用步骤1中记住的类别信息确定保存路径
2. 创建必要的目录结构
3. 直接写入JSON文件（覆盖已有文件）
4. 报告保存位置

---

### 6. 验证 ⚠️ 必须执行所有三项验证

**🔴 重要：以下三项验证必须全部执行，不可跳过任何一项！**

**⚠️ 验证脚本位置**：使用当前工作目录中的 `scripts/` 目录

#### 6.1 Schema 验证 ✅ 必须

```bash
python scripts/validate.py sources/path/to/file.json --schema .claude/skills/datasource-fetcher/reference/datasource-schema.json
```
**必须通过**：JSON 格式符合 datasource-schema.json 标准

#### 6.2 URL 可访问性验证 ✅ 必须

```bash
python scripts/verify_urls.py sources/path/to/file.json
```

验证字段：`primary_url`（必需）、`organization.website`、`api.documentation`、`support_url`
**必须通过**：所有 URL 返回 200 状态码

#### 6.3 完整性检查 ✅ 必须

```bash
python scripts/check_completeness.py sources/path/to/file.json
```

**最低要求**：
- 必需字段: 100%
- 推荐字段: ≥80%
- 总体完成度: ≥70%

**说明**：所有验证脚本位于当前工作目录的 `scripts/` 目录，由批处理脚本自动复制到临时工作目录。

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
5. **不做额外操作**:
   - ❌ 不更新文档
   - ❌ 不提交Git
   - ❌ 不生成索引
   - ✅ 只生成和验证JSON文件

---

## 与完整流程的关系

```
完整数据源处理流程：
┌─────────────────────────────────────┐
│ datasource-fetcher (本skill)        │ ← 步骤 1-6
│ - 获取数据                          │
│ - 生成JSON                          │
│ - 验证                              │
└─────────────────────────────────────┘
           ↓ (JSON文件)
┌─────────────────────────────────────┐
│ datasource-publisher (另一个skill)  │ ← 步骤 7-10
│ - 生成索引                          │
│ - 更新文档                          │
│ - Git提交                           │
└─────────────────────────────────────┘
```

---

## Reference 文档

- [datasource-schema.json](reference/datasource-schema.json) - JSON Schema 标准

---

**注意**: 本 skill 是从原 datasource-scraper 拆分出来的数据获取部分，专注于数据质量和验证，不涉及文档管理和版本控制。
