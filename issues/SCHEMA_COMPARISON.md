# DataSource Hub Schema 标准对比

## 📋 文档概述

本文档对比了 DataSource Hub 项目中两种不同的数据源元数据标准：
- **旧标准**：`docs/data-collection-guide.md` 中描述的扁平化结构
- **新标准**：`schemas/datasource-schema.json` 定义的嵌套化结构

**创建日期**: 2025-12-05

---

## 📂 已有数据源列表及标准符合情况

### ✅ 完全符合新标准的数据源 (12个)

| 文件路径 | 数据源名称 | 符合状态 |
|---------|-----------|---------|
| `sources/academic/economics/nber.json` | NBER Data Library | ✅ 完全符合 |
| `sources/china/national/nbs.json` | 国家统计局 | ✅ 完全符合 |
| `sources/china/finance/banking/pbc.json` | 中国人民银行 | ✅ 完全符合 |
| `sources/china/finance/banking/nfra.json` | 国家金融监管总局 | ✅ 完全符合 |
| `sources/china/finance/securities/csrc.json` | 中国证监会 | ✅ 完全符合 |
| `sources/china/economy/macro/ndrc.json` | 国家发改委 | ✅ 完全符合 |
| `sources/china/economy/trade/customs.json` | 海关总署 | ✅ 完全符合 |
| `sources/china/economy/trade/mofcom.json` | 商务部 | ✅ 完全符合 |
| `sources/international/economics/worldbank.json` | 世界银行 | ✅ 完全符合 |
| `sources/international/economics/imf.json` | 国际货币基金组织 | ✅ 完全符合 |
| `sources/international/economics/oecd.json` | 经合组织 | ✅ 完全符合 |
| `sources/international/economics/wto.json` | 世界贸易组织 | ✅ 完全符合 |

### ⚠️ 部分不符合的数据源 (已解决)

| 文件路径 | 问题描述 | 处理状态 |
|---------|---------|---------|
| ~~`sources/china/finance/monetary-policy/pbc-monetary-policy-report.json`~~ | `data_characteristics.types` 包含非法值 `'analytical'` | ✅ 已删除 (2025-12-05) |

---

## 🔄 两种标准的详细对比

### 1. 整体结构对比

#### 旧标准 (docs/data-collection-guide.md)
```json
{
  "扁平化结构": "大部分字段在顶层",
  "单语言": "中英文字段分离(name, name_en)",
  "简单评分": "3个维度的质量评分",
  "分类方式": "使用category和subcategory字段"
}
```

#### 新标准 (schemas/datasource-schema.json)
```json
{
  "嵌套化结构": "按功能分组为多个对象",
  "多语言支持": "统一的多语言对象结构",
  "全面评估": "5个维度的质量评分",
  "分类方式": "通过目录结构和tags实现"
}
```

---

### 2. 字段级别详细对比

#### 2.1 基本信息字段

| 字段名 | 旧标准 | 新标准 | 变化说明 |
|--------|--------|--------|----------|
| **id** | ✅ `string` | ✅ `string` | 保持不变 |
| **name** | ❌ `string` (单语言) | ✅ `object {en, zh, native}` | **重大变化**: 改为多语言对象 |
| **name_en** | ✅ `string` | ❌ 已废弃 | 合并到 `name.en` |
| **description** | ❌ `string` (单语言) | ✅ `object {en, zh}` | **重大变化**: 改为多语言对象 |
| **organization** | ❌ `string` | ✅ `object {name, type, country, website}` | **重大变化**: 改为结构化对象 |
| **organization_en** | ✅ `string` | ❌ 已废弃 | 不再需要 |

**示例对比**:

<table>
<tr>
<th>旧标准</th>
<th>新标准</th>
</tr>
<tr>
<td>

```json
{
  "name": "中国人民银行",
  "name_en": "People's Bank of China",
  "organization": "中国人民银行",
  "organization_en": "People's Bank of China"
}
```

</td>
<td>

```json
{
  "name": {
    "en": "People's Bank of China",
    "zh": "中国人民银行",
    "native": "中国人民银行"
  },
  "organization": {
    "name": "People's Bank of China",
    "type": "national_government",
    "country": "CN",
    "website": "http://www.pbc.gov.cn"
  }
}
```

</td>
</tr>
</table>

#### 2.2 分类和标签

| 字段名 | 旧标准 | 新标准 | 变化说明 |
|--------|--------|--------|----------|
| **category** | ✅ `string` ("china", "usa", "international") | ❌ 已废弃 | 改用目录结构 |
| **subcategory** | ✅ `string` ("finance", "economy") | ❌ 已废弃 | 改用目录结构 |
| **tags** | ✅ `array of strings` | ✅ `array of strings` | 保持不变，但更加重要 |

**分类方式变化**:
- 旧标准: `"category": "china", "subcategory": "finance"`
- 新标准: 文件路径 `sources/china/finance/banking/pbc.json` + `tags`

#### 2.3 访问信息字段

| 字段名 | 旧标准 | 新标准 | 变化说明 |
|--------|--------|--------|----------|
| **url** | ✅ `string` (顶层) | ❌ 已废弃 | 移至 `access.primary_url` |
| **access_type** | ✅ `string` (顶层) | ❌ 已废弃 | 移至 `access.access_level` |
| **access** | ❌ 不存在 | ✅ `object` (完整对象) | **新增**: 包含所有访问相关信息 |

**新标准的 access 对象结构**:
```json
{
  "access": {
    "primary_url": "string",           // 主要访问URL
    "api": {                           // API信息
      "available": "boolean",
      "documentation": "string | null",
      "version": "string | null",
      "authentication": "boolean | null"
    },
    "download": {                      // 下载选项
      "available": "boolean",
      "formats": ["array"]
    },
    "access_level": "enum",            // 访问级别
    "registration_required": "boolean"
  }
}
```

#### 2.4 数据覆盖范围

| 字段名 | 旧标准 | 新标准 | 变化说明 |
|--------|--------|--------|----------|
| **time_coverage_start** | ✅ `string (date)` | ❌ 已废弃 | 移至 `coverage.temporal.start_year` |
| **time_coverage_end** | ✅ `string (date/ongoing)` | ❌ 已废弃 | 移至 `coverage.temporal.end_year` |
| **coverage** | ❌ 不存在 | ✅ `object` (完整对象) | **新增**: 地理+时间+领域覆盖 |

**新标准的 coverage 对象结构**:
```json
{
  "coverage": {
    "geographic": {                    // 地理覆盖
      "scope": "enum",                 // global/regional/national/subnational
      "countries": "integer | array",  // 国家数量或列表
      "regions": ["array"]             // 覆盖区域
    },
    "temporal": {                      // 时间覆盖
      "start_year": "integer",
      "end_year": "integer",
      "update_frequency": "enum"       // real-time/daily/weekly/monthly...
    },
    "domains": ["array"],              // 领域列表 (必需)
    "indicators": "integer"            // 指标数量 (可选)
  }
}
```

#### 2.5 数据特征

| 字段名 | 旧标准 | 新标准 | 变化说明 |
|--------|--------|--------|----------|
| **data_formats** | ✅ `array` (顶层) | ❌ 已废弃 | 移至 `data_characteristics.formats` |
| **api_available** | ✅ `boolean` (顶层) | ❌ 已废弃 | 移至 `access.api.available` |
| **api_type** | ✅ `string` (顶层) | ❌ 已废弃 | 移至 `access.api` (隐含) |
| **update_frequency** | ✅ `string` (顶层) | ❌ 已废弃 | 移至 `coverage.temporal.update_frequency` |
| **data_characteristics** | ❌ 不存在 | ✅ `object` (完整对象) | **新增**: 数据类型、粒度、格式、语言 |

**新标准的 data_characteristics 对象**:
```json
{
  "data_characteristics": {
    "types": ["array"],                // 数据类型 (必需)
    "granularity": ["array"],          // 数据粒度 (必需)
    "formats": ["array"],              // 数据格式 (必需)
    "languages": ["array"]             // 语言代码 (可选)
  }
}
```

**types 枚举值变化**:
- 旧标准: 无明确限制
- 新标准: `["statistical", "time-series", "cross-sectional", "panel", "geospatial", "text", "image", "api"]`

#### 2.6 质量评分

| 字段名 | 旧标准 | 新标准 | 变化说明 |
|--------|--------|--------|----------|
| **authority** | ✅ `number (1-5)` | ❌ 已废弃 | 改为 `quality.authority_level` |
| **data_quality** | ✅ `number (1-5)` | ❌ 已废弃 | 拆分为多个维度 |
| **coverage** (评分) | ✅ `number (1-5)` | ❌ 已废弃 | 改为 `quality.data_completeness` |
| **quality** | ❌ 不存在 | ✅ `object` (5维度) | **新增**: 全面的质量评估体系 |

**评分体系对比**:

<table>
<tr>
<th>旧标准 (3维度)</th>
<th>新标准 (5维度)</th>
</tr>
<tr>
<td>

```json
{
  "authority": 5.0,
  "data_quality": 4.5,
  "coverage": 4.0
}
```

</td>
<td>

```json
{
  "quality": {
    "authority_level": 5,
    "methodology_transparency": 4,
    "update_timeliness": 4,
    "data_completeness": 4,
    "documentation_quality": 3,
    "citation_count": "very_high"
  }
}
```

</td>
</tr>
</table>

**新增的质量维度**:
- `methodology_transparency`: 方法论透明度
- `update_timeliness`: 更新及时性
- `documentation_quality`: 文档质量
- `citation_count`: 引用情况

#### 2.7 许可和使用

| 字段名 | 旧标准 | 新标准 | 变化说明 |
|--------|--------|--------|----------|
| **license** | ✅ `string` (顶层) | ❌ 已废弃 | 移至 `licensing.license` |
| **cost** | ✅ `string` (free/paid) | ❌ 已废弃 | 用 `access_level` 替代 |
| **licensing** | ❌ 不存在 | ✅ `object` (完整对象) | **新增**: 详细的许可信息 |

**新标准的 licensing 对象**:
```json
{
  "licensing": {
    "license": "string",               // 许可证名称 (必需)
    "commercial_use": "boolean",       // 是否允许商业使用
    "attribution_required": "boolean", // 是否需要署名
    "restrictions": ["array"]          // 使用限制列表
  }
}
```

#### 2.8 新增的可选字段

以下字段在旧标准中**完全不存在**，在新标准中**新增**：

| 字段名 | 类型 | 说明 | 必需性 |
|--------|------|------|--------|
| **data_content** | `object {en: array, zh: array}` | 主要数据内容列表 | 可选 |
| **metadata** | `object` | 元数据标准和文档信息 | 可选 |
| **usage** | `object` | 使用案例和代码示例 | 可选 |
| **related_sources** | `array of strings` | 相关数据源ID列表 | 可选 |
| **contact** | `object {email, support_url}` | 联系方式 | 可选 |
| **catalog_metadata** | `object` | 目录元数据（添加日期、状态等） | 部分必需 |

**data_content 示例** (新增):
```json
{
  "data_content": {
    "en": [
      "GDP and economic growth indicators",
      "Poverty and income distribution data",
      "International debt statistics"
    ],
    "zh": [
      "GDP和经济增长指标",
      "贫困和收入分配数据",
      "国际债务统计"
    ]
  }
}
```

**metadata 示例** (新增):
```json
{
  "metadata": {
    "standards_followed": ["SDMX", "ISO 3166", "HS Classification"],
    "data_dictionary": true,
    "methodology_docs": true,
    "user_guide": true
  }
}
```

**catalog_metadata 示例** (新增):
```json
{
  "catalog_metadata": {
    "added_date": "2025-01-25",
    "last_updated": "2025-01-25",
    "verified_date": "2025-01-25",
    "contributor": "DataSource Hub Team",
    "status": "active"
  }
}
```

---

### 3. 必需字段对比

#### 旧标准的必需字段 (来自文档描述)
```
✅ id
✅ name
✅ name_en
✅ description
✅ url
✅ organization
✅ organization_en
✅ category
✅ subcategory
✅ tags
✅ access_type
✅ license
✅ cost
✅ data_formats
✅ api_available
✅ api_type (如果api_available=true)
✅ update_frequency
✅ time_coverage_start
✅ time_coverage_end
✅ authority
✅ data_quality
✅ coverage
✅ status
✅ verified
✅ last_verified
✅ metadata_created
✅ metadata_updated
```

#### 新标准的必需字段 (schema定义)
```
✅ id
✅ name (object with "en" required)
✅ organization (object with "name" and "type" required)
✅ description (object with "en" required)
✅ access (object)
✅ coverage (object)
✅ data_characteristics (object)
✅ quality (object with 5 dimensions)
✅ licensing (object with "license" required)
```

**必需字段数量对比**:
- 旧标准: ~25个顶层必需字段
- 新标准: 8个顶层必需对象，内部包含必需子字段

---

## 📊 完整示例对比

### 示例：中国人民银行数据源

<table>
<tr>
<th width="50%">旧标准格式</th>
<th width="50%">新标准格式（实际使用）</th>
</tr>
<tr>
<td valign="top">

```json
{
  "id": "china-pbc",
  "name": "中国人民银行",
  "name_en": "People's Bank of China",
  "description": "中国的中央银行，负责制定和执行货币政策...",
  "url": "http://www.pbc.gov.cn/",
  "organization": "中国人民银行",
  "organization_en": "People's Bank of China",
  "category": "china",
  "subcategory": "finance",
  "tags": ["央行", "货币政策", "金融"],
  "access_type": "open",
  "license": "开放政府数据",
  "cost": "free",
  "data_formats": ["JSON", "Excel", "PDF"],
  "api_available": false,
  "api_type": null,
  "update_frequency": "monthly",
  "time_coverage_start": "1990-01-01",
  "time_coverage_end": "ongoing",
  "authority": 5.0,
  "data_quality": 4.5,
  "coverage": 4.8,
  "status": "active",
  "verified": true,
  "last_verified": "2025-01-25",
  "metadata_created": "2025-01-25",
  "metadata_updated": "2025-01-25"
}
```

</td>
<td valign="top">

```json
{
  "id": "china-pbc",
  "name": {
    "en": "People's Bank of China",
    "zh": "中国人民银行",
    "native": "中国人民银行"
  },
  "organization": {
    "name": "People's Bank of China",
    "type": "national_government",
    "country": "CN",
    "website": "http://www.pbc.gov.cn"
  },
  "description": {
    "en": "The central bank of China...",
    "zh": "中国的中央银行，负责制定和执行货币政策..."
  },
  "access": {
    "primary_url": "http://www.pbc.gov.cn/",
    "api": {
      "available": false,
      "documentation": null,
      "version": null,
      "authentication": null
    },
    "download": {
      "available": true,
      "formats": ["JSON", "Excel", "PDF"]
    },
    "access_level": "open",
    "registration_required": false
  },
  "coverage": {
    "geographic": {
      "scope": "national",
      "countries": 1,
      "regions": ["China"]
    },
    "temporal": {
      "start_year": 1990,
      "end_year": 2025,
      "update_frequency": "monthly"
    },
    "domains": ["finance", "monetary-policy", "banking"]
  },
  "data_content": {
    "en": [
      "Monetary policy and interest rates",
      "Foreign exchange reserves",
      "Money supply statistics"
    ],
    "zh": [
      "货币政策和利率数据",
      "外汇储备数据",
      "货币供应量统计"
    ]
  },
  "data_characteristics": {
    "types": ["statistical", "time-series"],
    "granularity": ["national", "monthly"],
    "formats": ["JSON", "Excel", "PDF"],
    "languages": ["zh", "en"]
  },
  "quality": {
    "authority_level": 5,
    "methodology_transparency": 5,
    "update_timeliness": 5,
    "data_completeness": 4,
    "documentation_quality": 4,
    "citation_count": "very_high"
  },
  "licensing": {
    "license": "Open Government Data",
    "commercial_use": true,
    "attribution_required": true,
    "restrictions": []
  },
  "metadata": {
    "standards_followed": ["National standards"],
    "data_dictionary": true,
    "methodology_docs": true,
    "user_guide": false
  },
  "contact": {
    "email": "webmaster@pbc.gov.cn"
  },
  "catalog_metadata": {
    "added_date": "2025-01-25",
    "last_updated": "2025-01-25",
    "verified_date": "2025-01-25",
    "contributor": "DataSource Hub Team",
    "status": "active"
  },
  "tags": [
    "china",
    "central-bank",
    "monetary-policy",
    "finance"
  ]
}
```

</td>
</tr>
</table>

---
