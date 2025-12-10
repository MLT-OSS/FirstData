# 验证指南

数据源文件在保存后必须经过三项验证，确保质量和可用性。

## 验证流程概览

⚠️ **重要：以下三项验证必须全部执行，不可跳过任何一项！**

```
Schema 验证 → URL 可访问性验证 → 完整性检查 → 通过 → 生成索引
    ↓              ↓                  ↓
  失败           失败               失败
    ↓              ↓                  ↓
  修复 JSON     修复或确认 URL      补充字段
```

---

## 1. Schema 验证 ✅ 必须

### 目的
确保 JSON 文件格式符合 `datasource-schema.json` 标准。

### 验证命令

```bash
# 从项目根目录运行
python .claude/skills/datasource-scraper/scripts/validate.py sources/path/to/file.json --schema schemas/datasource-schema.json
```

### 验证内容
- 所有必需字段存在
- 字段类型正确（字符串、数组、对象等）
- 枚举值在允许的范围内
- 嵌套结构符合 schema 定义

### 常见错误

#### 错误 1：缺少必需字段
```
Error: Required field 'id' is missing
```
**解决方案**：在 JSON 中添加缺失的字段。

#### 错误 2：字段类型不匹配
```
Error: Field 'coverage.geographic.scope' must be one of: global, regional, national, local
```
**解决方案**：使用正确的枚举值。

#### 错误 3：不允许 null 的字段设为 null
```
Error: Field 'name.en' cannot be null
```
**解决方案**：提供有效值或删除该字段（如果是可选字段）。

### 处理不确定信息

- **可选字段**（非 required）：如果无法获取，直接删除该字段
- **允许 null 的字段**（schema 中类型为 `["string", "null"]`）：可以设为 `null`
- **不允许 null 的字段**（schema 中类型为 `"string"`）：必须提供有效值或删除字段
- **必填字段**（在 required 列表中）：必须提供有效值，可以向用户询问

---

## 2. URL 可访问性验证 ✅ 必须

### 目的
确保数据源中的所有 URL 是真实可访问的地址，避免死链接。

### 验证命令

```bash
# 从项目根目录运行
python .claude/skills/datasource-scraper/scripts/verify_urls.py sources/path/to/file.json
```

### 验证的 URL 字段

| 字段路径 | 重要性 | 说明 |
|---------|--------|------|
| `access.primary_url` | **必须验证** | 主要访问 URL，必须确认有效 |
| `organization.website` | 建议验证 | 组织官网 URL |
| `access.api.documentation` | 建议验证 | API 文档 URL |
| `contact.support_url` | 建议验证 | 支持/帮助 URL |

### 验证结果处理

#### 成功（200 OK）
```
✅ access.primary_url: https://www.example.com (200 OK)
```
URL 验证通过，可以继续。

#### 失败（403 Forbidden / Timeout）
```
⚠️ access.primary_url: https://www.example.com (403 Forbidden)
```

**重要说明**：自动验证失败不代表 URL 无效！某些网站会阻止自动化请求。

**解决方案**：通过其他方式手动确认 URL 有效性：

1. **浏览器访问**：手动打开 URL，确认页面存在
2. **权威引用**：
   - GitHub 官方仓库引用
   - 维基百科链接
   - 学术论文引用
   - 第三方数据目录（如 data.gov）
3. **搜索引擎**：通过 WebSearch 确认 URL 出现在官方文档中

#### 最低要求
- **至少 `primary_url` 必须验证通过或手动确认有效**
- 其他 URL 建议验证，但不是强制要求

---

## 3. 完整性检查 ✅ 必须

### 目的
确保数据源信息足够详细，达到最低质量标准。

### 验证命令

```bash
# 从项目根目录运行
python scripts/check_completeness.py sources/path/to/file.json
```

### 评分标准

完整性检查会对三类字段进行评分：

#### 1. 必需字段（Required Fields）
- Schema 中标记为 `required` 的字段
- **必须 100% 完成**

#### 2. 推荐字段（Recommended Fields）
- 对数据源理解很重要但非必需的字段
- 例如：`description`, `data_content`, `coverage.temporal`, `quality.*`
- **目标：≥80%**

#### 3. 可选字段（Optional Fields）
- 增强信息但不影响基本使用
- 例如：`usage.popular_datasets`, `metadata.standards`, `contact.email`
- 尽量填充，但不是强制要求

### 最低要求

```
✅ 必需字段: 100%
✅ 推荐字段: ≥80%
✅ 总体完成度: ≥70%
```

### 如果不达标

1. 查看输出报告，识别缺失字段
2. 回到网站补充缺失信息
3. 重新运行完整性检查
4. 重复直到达标

### 示例输出

```
📊 完整性检查报告

必需字段: 12/12 (100%) ✅
推荐字段: 15/18 (83%) ✅
可选字段: 8/20 (40%)
总体完成度: 35/50 (70%) ✅

缺失的推荐字段:
- coverage.temporal.start_year
- quality.citation_count
- metadata.standards

总体评价: 达到最低标准 ✅
```

---

## 验证检查点

⚠️ **只有三项验证全部完成后，才能进入下一步（生成索引/更新文档）**

使用以下检查清单确认：

- [ ] Schema 验证通过（无错误输出）
- [ ] URL 可访问性验证通过或手动确认（至少 primary_url）
- [ ] 完整性检查达标（≥70%，必需字段 100%，推荐字段 ≥80%）

---

## 常见问题

### Q1: Schema 验证失败但我确认字段正确？
**A**: 检查字段拼写、类型、嵌套层级是否完全匹配 schema。使用 JSON 格式化工具检查语法。

### Q2: URL 验证全部失败？
**A**: 可能是网络问题或网站防爬虫。手动在浏览器中确认 URL 有效，然后继续。

### Q3: 完整性只有 60%，如何提升？
**A**: 优先补充"推荐字段"。如果确实无法获取某些信息，确保必需字段和核心推荐字段（如 description、data_content）完整。

### Q4: 可以跳过某项验证吗？
**A**: **不可以！** 三项验证都是必须的。如果验证失败，必须修复或手动确认后才能继续。
