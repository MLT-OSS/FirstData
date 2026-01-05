# 数据源收录指南

本指南提供数据源收录的详细步骤和最佳实践。

## 📋 目录

- [收录流程概览](#收录流程概览)
- [步骤1：信息调研](#步骤1信息调研)
- [步骤2：元数据收集](#步骤2元数据收集)
- [步骤3：创建JSON文件](#步骤3创建json文件)
- [步骤4：验证与测试](#步骤4验证与测试)
- [步骤5：文档更新](#步骤5文档更新)
- [常见问题](#常见问题)
- [最佳实践](#最佳实践)

---

## 收录流程概览

```
1. 信息调研 (30分钟)
   ↓
2. 元数据收集 (45分钟)
   ↓
3. 创建JSON文件 (15分钟)
   ↓
4. 验证与测试 (15分钟)
   ↓
5. 文档更新 (15分钟)
   ↓
6. 提交PR
```

**预估总时间**: 2-2.5小时/数据源

---

## 步骤1：信息调研

### 1.1 确认数据源资格

在开始收录前，确认数据源符合以下条件：

✅ **必须满足**：
- 官方或权威机构发布
- 数据可公开访问（开放或注册后访问）
- 网站/API可正常访问
- 有明确的数据更新机制

❌ **不符合条件**：
- 个人博客或非官方整理
- 完全付费且无试用
- 长期未更新（超过3年）
- 网站已失效

### 1.2 初步调研

访问数据源官网，了解：

1. **数据源基本信息**
   - 发布机构是谁？
   - 数据覆盖哪些领域？
   - 数据更新频率？

2. **访问方式**
   - 是否需要注册？
   - 有没有API？
   - 支持哪些数据格式？

3. **使用条款**
   - 许可证类型？
   - 有无使用限制？
   - 商业使用是否允许？

### 1.3 记录关键URL

收集以下URL（如果存在）：

- 官方首页
- 数据门户/下载页面
- API文档
- 使用指南
- 许可证说明
- 联系方式

---

## 步骤2：元数据收集

### 2.1 必需字段（100%完成）

参考 [datasource.schema.json](../schemas/datasource.schema.json)，以下字段必须填写：

#### 基本信息
```json
{
  "id": "唯一标识符（kebab-case）",
  "name": "数据源中文名称",
  "name_en": "数据源英文名称",
  "description": "详细描述（200字以上）",
  "url": "官方URL",
  "organization": "发布机构",
  "organization_en": "发布机构英文名"
}
```

**示例**：
```json
{
  "id": "china-pbc",
  "name": "中国人民银行",
  "name_en": "People's Bank of China",
  "description": "中国的中央银行，负责制定和执行货币政策...",
  "url": "http://www.pbc.gov.cn/",
  "organization": "中国人民银行",
  "organization_en": "People's Bank of China"
}
```

#### 分类信息
```json
{
  "category": "主类别",
  "subcategory": "子类别",
  "tags": ["标签1", "标签2", "标签3"]
}
```

**类别参考**：
- 国际组织: `international`
- 中国: `china`
- 美国: `usa`
- 学术研究: `academic`

**子类别示例**：
- 金融财政: `finance`
- 经济统计: `economy`
- 健康医疗: `health`

#### 访问信息
```json
{
  "access_type": "open | registration | restricted",
  "license": "许可证类型",
  "cost": "free | freemium | paid"
}
```

#### 技术信息
```json
{
  "data_formats": ["JSON", "CSV", "XML", "Excel"],
  "api_available": true,
  "api_type": "REST | GraphQL | SOAP | Other",
  "update_frequency": "daily | weekly | monthly | quarterly | annually | irregular"
}
```

#### 时间范围
```json
{
  "time_coverage_start": "YYYY-MM-DD",
  "time_coverage_end": "YYYY-MM-DD | ongoing"
}
```

#### 质量评分

使用 6 个维度评估数据源质量（1-5 分，整数）：

```json
{
  "quality": {
    "authority_level": 5,              // 来源权威性 (1-5)
    "methodology_transparency": 4,     // 方法论透明度 (1-5)
    "update_timeliness": 5,           // 更新及时性 (1-5)
    "data_completeness": 5,           // 数据完整性 (1-5)
    "documentation_quality": 4,       // 文档质量 (1-5)
    "citation_count": 5               // 引用频次 (1-5)
  }
}
```

**评分参考**：
- **authority_level（权威性）**：国际组织/中央政府 = 5，部委级 = 4-5，地方政府 = 3-4
- **methodology_transparency（方法论透明度）**：方法论完全公开 = 5，部分公开 = 3-4
- **update_timeliness（更新及时性）**：实时/每日 = 5，每月 = 4，每年 = 3
- **data_completeness（数据完整性）**：覆盖所有指标 = 5，主要指标 = 4，部分指标 = 3
- **documentation_quality（文档质量）**：完整文档+示例 = 5，基本文档 = 3-4
- **citation_count（引用频次）**：被广泛引用 = 5，经常被引用 = 4，定期被引用 = 3，偶尔被引用 = 2，很少被引用 = 1

#### 状态与元数据
```json
{
  "status": "active | archived | deprecated",
  "verified": true,
  "last_verified": "YYYY-MM-DD",
  "metadata_created": "YYYY-MM-DD",
  "metadata_updated": "YYYY-MM-DD"
}
```

### 2.2 推荐字段（建议80%以上完成）

```json
{
  "country": "国家/地区",
  "language": ["zh", "en"],
  "geographic_coverage": "global | national | regional | local",
  "api_documentation": "API文档URL",
  "data_dictionary": "数据字典URL",
  "contact_email": "联系邮箱",
  "related_sources": ["相关数据源ID"],
  "citation": "引用格式",
  "doi": "DOI（如果有）"
}
```

### 2.3 可选字段

根据数据源特点选择性填写：

```json
{
  "keywords": ["关键词数组"],
  "subjects": ["主题分类"],
  "api_rate_limit": "API限流说明",
  "api_authentication": "API认证方式",
  "bulk_download": true,
  "historical_data": true,
  "real_time": false,
  "mobile_app": false,
  "notes": "备注说明",
  "changelog": "变更记录"
}
```

---

## 步骤3：创建JSON文件

### 3.1 确定文件路径

根据数据源类别确定存放位置：

**中国数据源**：
```
sources/china/{领域}/{子领域}/{id}.json
```
示例：
- `sources/china/finance/banking/pbc.json`
- `sources/china/economy/statistics/nbs.json`

**国际组织**：
```
sources/international/{id}.json
```
示例：
- `sources/international/world-bank.json`
- `sources/international/unesco.json`

**其他国家**：
```
sources/{country}/{领域}/{id}.json
```
示例：
- `sources/usa/census/census-bureau.json`

### 3.2 使用模板创建

复制示例模板：

```bash
# 最小示例
cp schemas/examples/minimal-datasource.json sources/china/finance/banking/new-source.json

# 完整示例
cp schemas/examples/complete-datasource.json sources/china/finance/banking/new-source.json
```

### 3.3 填写元数据

使用文本编辑器打开JSON文件，按照步骤2收集的信息填写。

**注意事项**：
- 保持JSON格式正确（注意逗号、引号）
- 日期使用 ISO 8601 格式：`YYYY-MM-DD`
- 布尔值使用 `true`/`false`（小写，无引号）
- 数组使用方括号 `[]`
- URL确保可访问

### 3.4 格式化JSON

使用工具格式化（可选但推荐）：

```bash
# 使用Python格式化
python -m json.tool sources/china/finance/banking/new-source.json > temp.json
mv temp.json sources/china/finance/banking/new-source.json
```

---

## 步骤4：验证与测试

### 4.1 Schema验证

验证JSON文件符合Schema：

```bash
python scripts/validate.py sources/china/finance/banking/new-source.json
```

**期望输出**：
```
✅ sources/china/finance/banking/new-source.json - 验证通过
```

**如果验证失败**：
- 仔细阅读错误信息
- 检查缺失或错误的字段
- 确认数据类型正确
- 修复后重新验证

### 4.2 URL验证

验证所有URL可访问：

```bash
python scripts/verify_urls.py sources/china/finance/banking/new-source.json
```

**期望输出**：
```
检查 URL: http://www.pbc.gov.cn/
✅ 状态码: 200 - OK

检查 URL: http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html
✅ 状态码: 200 - OK

所有URL验证通过！
```

**如果URL验证失败**：
- 检查URL是否正确
- 确认网站是否可访问
- 某些网站可能需要User-Agent或Cookies
- 如果是暂时性问题，稍后重试

### 4.3 完整性检查

检查字段完整性：

```bash
python scripts/check_completeness.py sources/china/finance/banking/new-source.json
```

**期望输出**：
```
必需字段: 100% (20/20)
推荐字段: 85% (17/20)
可选字段: 40% (8/20)

总体完成度: 78%
评级: 优秀 ⭐⭐⭐⭐⭐
```

**最低要求**：
- 必需字段：100%
- 推荐字段：≥80%
- 总体完成度：≥70%

### 4.4 生成索引测试

测试索引生成：

```bash
python scripts/build_index.py --test sources/china/finance/banking/new-source.json
```

确认新数据源能正确添加到索引中。

---

## 步骤5：文档更新

### 5.1 更新一级目录 README

在对应的一级目录 README 中添加新数据源。

**注意**: 仅在一级目录（china, international, countries, academic, sectors）下维护 README 文件，子目录不需要 README。

例如，添加到 `sources/china/README.md`：

```markdown
### 金融财政 | Finance

#### 银行监管

1. **中国人民银行** (`china-pbc`) ⭐💎
   - 权威性：5.0
   - 数据格式：JSON, Excel, PDF
   - 访问类型：开放
   - [查看详情](finance/banking/pbc.json)

2. **新增数据源** (`new-source-id`) ⭐⭐⭐⭐
   - 权威性：4.0
   - 数据格式：CSV, Excel
   - 访问类型：注册
   - [查看详情](finance/banking/new-source.json)
```

### 5.2 更新任务清单

在任务清单中更新状态。

例如，在 `tasks/china/finance.md` 中：

```markdown
### ✅ 1.X 新增数据源 (`new-source-id`)
- **状态**: ✅ 已完成
- **完成日期**: 2025-12-01
- **文件**: `sources/china/finance/banking/new-source.json`
- **贡献者**: @your-username
- **权威性**: 4
- **URL**: https://example.com/
```

### 5.3 更新进度统计

更新相关文件中的进度统计：

- `tasks/china/README.md`
- `tasks/README.md`
- `ROADMAP.md`

---

## 常见问题

### Q1: 找不到某个必需字段的信息怎么办？

**A**:
1. 仔细查看官网的"关于我们"、"使用说明"等页面
2. 查看API文档或数据字典
3. 联系数据源提供方
4. 如果确实无法获取，在Issue中说明情况

### Q2: 数据源有多个URL，应该用哪个？

**A**:
- `url` 字段：使用官方主页URL
- 其他URL可以放在：
  - `api_documentation`：API文档
  - `data_dictionary`：数据字典
  - `related_urls`：其他相关链接

### Q3: 如何判断数据源的权威性评分？

**A**: 参考以下标准：

| 评分 | 标准 |
|------|------|
| 5.0 💎 | 国际组织、国家级中央政府、央行 |
| 4.5 ⭐ | 部委级政府机构、知名研究机构 |
| 4.0 | 省级政府、大型国企 |
| 3.5 | 地市级政府、行业协会 |
| 3.0 | 区县级、第三方统计 |

### Q4: 数据格式太多，都要列出来吗？

**A**:
- 列出主要的常用格式
- 优先级：JSON > CSV > Excel > XML > PDF
- 如果格式超过5种，选择最重要的5种

### Q5: API需要认证，如何填写？

**A**:
```json
{
  "api_available": true,
  "api_type": "REST",
  "api_authentication": "API Key",
  "api_documentation": "https://...",
  "access_type": "registration",
  "notes": "需要注册获取API Key，每日限额1000次请求"
}
```

### Q6: 数据源包含多个子数据集，如何处理？

**A**:
- 如果子数据集独立且重要，可以分别收录
- 如果是同一机构的系列数据，作为一个数据源，在描述中说明包含的子集
- 使用 `related_sources` 字段关联相关数据源

### Q7: 验证脚本报错怎么办？

**A**:
1. 仔细阅读错误信息
2. 检查JSON语法（使用JSONLint等工具）
3. 确认字段名拼写正确
4. 检查数据类型（字符串用引号，布尔值不用引号）
5. 查看示例文件参考正确格式

---

## 最佳实践

### ✅ DO - 推荐做法

1. **描述要详细**
   - 至少200字
   - 说明数据源的特点和价值
   - 提及主要数据集和指标
   - 包含使用场景

2. **URL要准确**
   - 使用官方URL，不要用短链接
   - 确保URL稳定，避免包含会话参数
   - 优先使用HTTPS

3. **标签要具体**
   - 3-10个标签
   - 包含领域、数据类型、应用场景
   - 使用规范化的标签（参考已有数据源）

4. **评分要客观**
   - 基于事实，不要主观臆断
   - 参考同类数据源
   - 必要时说明评分理由

5. **元数据要完整**
   - 必需字段100%完成
   - 推荐字段尽量完整
   - 能找到的信息都要填写

### ❌ DON'T - 避免做法

1. **不要复制粘贴**
   - 不要直接复制官网描述
   - 用自己的话概括总结
   - 避免重复信息

2. **不要猜测信息**
   - 不确定的信息不要填写
   - 不要臆造评分
   - 存疑的标记为待确认

3. **不要忽略验证**
   - 不要跳过Schema验证
   - 不要忽略URL验证错误
   - 不要提交未测试的代码

4. **不要使用缩写**
   - name字段用全称
   - 描述中首次出现缩写要注明全称
   - 避免地方性俚语

5. **不要包含敏感信息**
   - 不要包含API密钥
   - 不要包含个人账号信息
   - 不要包含付费账号凭证

---

## 工具和资源

### 推荐工具

- **JSON编辑器**：VS Code + JSON插件
- **JSON验证**：[JSONLint](https://jsonlint.com/)
- **URL检查**：[DownForEveryoneOrJustMe](https://downforeveryoneorjustme.com/)
- **网站快照**：[Web Archive](https://web.archive.org/)

### 参考资源

- [JSON Schema官方文档](https://json-schema.org/)
- [ISO 8601日期格式](https://www.iso.org/iso-8601-date-and-time-format.html)
- [开放数据许可证指南](https://opendefinition.org/licenses/)
- [数据引用格式](https://www.force11.org/datacitation)

### 示例文件

- 最小示例：[schemas/examples/minimal-datasource.json](../schemas/examples/minimal-datasource.json)
- 完整示例：[schemas/examples/complete-datasource.json](../schemas/examples/complete-datasource.json)
- 优秀案例：[sources/china/finance/banking/pbc.json](../sources/china/finance/banking/pbc.json)

---

## 下一步

完成数据源收录后：

1. ✅ 提交Pull Request
2. ⏳ 等待代码审查
3. 🔄 根据反馈修改
4. ✅ PR合并
5. 🎉 恭喜，您已成功贡献！

---

[← 返回贡献指南](CONTRIBUTING.md) | [查看质量标准](quality-criteria.md) | [返回任务清单](../tasks/README.md)
