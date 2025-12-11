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

#### 步骤 1：识别输入类型

- 如果输入以 `http://` 或 `https://` 开头 → **URL 输入**，直接使用
- 否则 → **名字输入**，使用 WebSearch 搜索官方网站，用 AskUserQuestion 确认 URL

#### 步骤 2：采用两层降级策略

##### 第一层：Web Search / WebFetch（主要策略）

结合使用 `WebSearch` 和 `WebFetch` 获取信息：

**Web Search 搜索**：
- "{组织名称} data/API/methodology/about" 等多角度搜索
- 快速获取概览信息和关键 URL

**WebFetch 验证**：
- 直接访问 URL 提取静态页面详细内容
- 获取组织信息、关键 URL、数据覆盖范围、更新频率、许可协议等

##### 第二层：Playwright 浏览器自动化

**触发条件**（满足任一即可）:
- JavaScript 渲染页面（WebFetch 返回内容很少或为空）
- 需要登录或认证才能查看内容
- 关键信息在交互式元素中（下拉菜单、折叠面板、Tab）
- 用户明确要求使用浏览器

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

**参考示例**: 现有的 sources/ 目录下的JSON文件

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
- 确保符合JSON格式规范

---

### 5. 保存文件

#### 确定保存路径

**使用 datasource-classifier Sub-Agent**（如果可用）:

调用 `@datasource-classifier` 确定最佳分类路径:
```
@datasource-classifier
请分析此数据源并确定分类路径:
- ID: {id}
- 组织: {organization.name} ({organization.type})
- 国家: {organization.country}
- 领域: {coverage.domains}
```

**快速参考**（无法使用 classifier 时）:
- 中国官方 → `sources/china/{domain}/{subdomain}/`
- 国际组织 → `sources/international/{domain}/`
- 学术机构 → `sources/academic/{domain}/`
- 其他国家 → `sources/countries/{continent}/{country}/`
- 行业部门 → `sources/sectors/{industry}/`

#### 保存操作

**直接覆盖模式**：

- 根据分类路径直接保存JSON文件
- 如果文件已存在，直接覆盖（不进行合并或备份）
- 文件命名：`{分类路径}/{数据源名称}.json`

**操作步骤**:
1. 确定保存路径（使用上述分类逻辑）
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

## 输出报告

执行完成后，输出标准化JSON报告：

```json
{
  "status": "success",
  "datasource_id": "intl-worldbank",
  "datasource_name": {
    "en": "World Bank",
    "zh": "世界银行"
  },
  "file_path": "sources/international/economics/worldbank.json",
  "operation": "create",
  "validation": {
    "schema": true,
    "url_check": true,
    "completeness": 0.95
  },
  "quality": {
    "authority_level": 5,
    "average_score": 4.8
  },
  "execution_time": "120s",
  "work_directory": "/tmp/ds-worldbank-xxx"
}
```

**失败时的报告**：
```json
{
  "status": "failed",
  "datasource_name": "World Bank",
  "error": "URL validation failed",
  "details": "primary_url returned 404",
  "file_path": null
}
```

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
- [quality-criteria.md](reference/quality-criteria.md) - 质量评分标准
<!-- - [data-acquisition.md](reference/data-acquisition.md) - 数据获取策略 -->
<!-- - [information-extraction.md](reference/information-extraction.md) - 信息提取指南 -->

---

**注意**: 本 skill 是从原 datasource-scraper 拆分出来的数据获取部分，专注于数据质量和验证，不涉及文档管理和版本控制。
