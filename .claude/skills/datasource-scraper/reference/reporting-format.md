# 输出报告格式

根据操作类型（创建或更新）使用不同的报告格式向用户展示结果。

## 创建操作报告

当创建新数据源时，使用此格式向用户汇报。

### 报告模板

```
✅ 已创建 sources/{path}/{filename}.json

📁 数据源 ID: {datasource-id}
🏢 组织: {organization.name} ({organization.type})
⭐ 平均质量评分: {quality.average_score}/5.0
🔗 主要 URL: {access.primary_url}
🌍 覆盖范围: {coverage.geographic.scope}, {coverage.geographic.countries 或 regions}
📅 时间跨度: {coverage.temporal.start_year}-{coverage.temporal.end_year}
📊 数据格式: {data_characteristics.formats}
🔓 访问类型: {access.access_level}

✅ Schema 验证: 通过
✅ URL 可访问性: 通过
✅ 完整性检查: {completeness_percentage}% (达标)

主要数据内容：
- {data_content[0].category.zh} - {data_content[0].description.zh}
- {data_content[1].category.zh} - {data_content[1].description.zh}
- {data_content[2].category.zh} - {data_content[2].description.zh}
```

### 完整示例

```
✅ 已创建 sources/international/economics/worldbank.json

📁 数据源 ID: worldbank-open-data
🏢 组织: World Bank (国际组织)
⭐ 平均质量评分: 4.9/5.0
🔗 主要 URL: https://data.worldbank.org
🌍 覆盖范围: 全球, 217个国家和地区
📅 时间跨度: 1960-2024
📊 数据格式: CSV, JSON, Excel, XML
🔓 访问类型: 开放访问

✅ Schema 验证: 通过
✅ URL 可访问性: 通过
✅ 完整性检查: 88% (达标)

主要数据内容：
- 宏观经济指标 - GDP、通胀率、失业率等核心经济指标
- 社会发展指标 - 教育、健康、贫困等社会发展数据
- 环境与气候 - 能源消耗、碳排放、自然资源数据
- 基础设施 - 交通、通信、能源等基础设施统计
- 金融与贸易 - 国际贸易、外汇储备、债务数据
```

---

## 更新操作报告

当更新现有数据源时，使用此格式展示变更详情。

### 报告模板

```
✅ 已更新 sources/{path}/{filename}.json

📊 变更摘要：

【更新字段】({count}个):
  * {field_name}: {old_value} → {new_value}
  * {field_name}: 已添加
  * catalog_metadata.last_updated: {old_date} → {new_date}

【保留字段】:
  * quality.* (所有质量评分)
  * catalog_metadata.contributor
  * catalog_metadata.created_date
  * {其他保留的字段}

【数组合并】:
  * tags: 新增 {new_tags}
  * usage.use_cases: 新增 {new_use_cases}
  * data_content: 合并 {merged_count} 个类别

【备份位置】: {filename}.backup

✅ Schema 验证: 通过
✅ URL 可访问性: 通过
✅ 完整性检查: {completeness_percentage}% (达标)
```

### 完整示例

```
✅ 已更新 sources/china/finance/banking/pbc.json

📊 变更摘要：

【更新字段】(5个):
  * access.api.documentation: http://www.pbc.gov.cn/api/old → https://www.pbc.gov.cn/openapi/docs
  * coverage.temporal.end_year: 2023 → 2024
  * data_content[2]: 已添加 "贷款市场报价利率"
  * access.api.authentication: null → "api_key"
  * catalog_metadata.last_updated: 2024-10-15 → 2024-12-10

【保留字段】:
  * quality.authority_level: 5.0
  * quality.methodology_transparency: 4.8
  * quality.update_timeliness: 4.9
  * quality.data_completeness: 4.7
  * quality.documentation_quality: 4.6
  * quality.citation_count: 5.0
  * catalog_metadata.contributor: "mlamp"
  * catalog_metadata.created_date: "2024-09-20"

【数组合并】:
  * tags: 新增 ["LPR", "贷款利率"]
  * usage.use_cases: 新增 "金融机构贷款定价参考"
  * data_content: 合并 1 个新类别（总共 8 个）

【备份位置】: pbc.json.backup

✅ Schema 验证: 通过
✅ URL 可访问性: 通过
✅ 完整性检查: 92% (达标)
```

---

## 批量操作报告

当一次处理多个数据源时，使用汇总报告。

### 报告模板

```
✅ 批量操作完成

📊 统计信息：
- 成功: {success_count}
- 失败: {failure_count}
- 总计: {total_count}

✅ 成功列表：
1. {datasource-id-1} - {name-1}
   - 路径: sources/{path-1}/{file-1}.json
   - 质量: {score-1}/5.0

2. {datasource-id-2} - {name-2}
   - 路径: sources/{path-2}/{file-2}.json
   - 质量: {score-2}/5.0

❌ 失败列表：
1. {datasource-id-x} - {name-x}
   - 原因: {error_message}
```

---

## 验证失败报告

当验证未通过时，使用此格式提示用户。

### Schema 验证失败

```
❌ Schema 验证失败

错误详情：
1. 字段 'id' 缺失（必需字段）
2. 字段 'coverage.geographic.scope' 值 "nationwide" 不在允许范围内
   允许值: global, regional, national, local
3. 字段 'quality.authority_level' 类型错误
   期望: number, 实际: string

请修复上述错误后重新验证。
```

### URL 验证失败

```
⚠️ URL 可访问性验证失败

验证结果：
- ❌ access.primary_url: https://example.com (403 Forbidden)
- ✅ organization.website: https://www.example.org (200 OK)
- ⚠️ access.api.documentation: https://api.example.com/docs (Timeout)

建议：
1. 手动在浏览器中确认 URL 是否有效
2. 查找权威引用（GitHub、维基百科、学术论文）
3. 确认至少 primary_url 可访问

如已确认 URL 有效，可以继续下一步。
```

### 完整性检查失败

```
❌ 完整性检查未达标

评分结果：
- 必需字段: 12/12 (100%) ✅
- 推荐字段: 10/18 (56%) ❌ (要求 ≥80%)
- 可选字段: 5/20 (25%)
- 总体完成度: 27/50 (54%) ❌ (要求 ≥70%)

缺失的推荐字段：
- description.zh (中文描述)
- description.en (英文描述)
- data_content (数据内容分类)
- coverage.temporal.start_year (开始年份)
- coverage.temporal.end_year (结束年份)
- quality.methodology_transparency (方法论透明度)
- quality.update_timeliness (更新及时性)
- quality.documentation_quality (文档质量)

建议：
1. 优先补充 description 和 data_content（核心推荐字段）
2. 回到网站获取缺失的时间跨度信息
3. 根据实际观察补充质量评分
4. 重新运行完整性检查
```

---

## 报告原则

### 清晰性
- 使用 emoji 图标增强可读性
- 分层展示信息（概要 → 详情）
- 突出关键信息（ID、质量、验证状态）

### 完整性
- 包含所有重要元数据
- 展示验证结果
- 提供文件路径

### 可操作性
- 失败时提供明确的错误信息
- 给出具体的修复建议
- 指导下一步操作
