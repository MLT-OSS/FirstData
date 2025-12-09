# Schema 字段详细说明

## 基础信息

### id
唯一标识符，格式：小写、连字符分隔
- 示例: "china-nbs", "worldbank-data"

### name
组织名称（多语言）
- `en`: 英文名称
- `zh`: 中文名称（如适用）
- `native`: 本地语言名称

### organization
- `name`: 组织名称
- `type`: international_organization | national_government | research_institution | industry_association | commercial
- `country`: ISO 3166-1 alpha-2 国家代码（国际组织为 null）
- `website`: 组织官网

### description
详细描述（中英双语）

## 访问信息 (access)

### primary_url
数据主访问地址

### api
- `available`: boolean
- `documentation`: API 文档 URL
- `version`: API 版本
- `authentication`: boolean

### download
- `available`: boolean
- `formats`: ["Excel", "CSV", "JSON", ...]

### access_level
open | registration | academic | commercial | restricted

## 覆盖范围 (coverage)

### geographic
- `scope`: global | regional | national | subnational
- `countries`: 数量或国家代码数组
- `regions`: 覆盖的区域

### temporal
- `start_year`: 起始年份
- `end_year`: 结束年份（持续更新则为当前年份）
- `update_frequency`: real-time | daily | weekly | monthly | quarterly | annual | irregular | one-time

### domains
主题领域数组，如: ["economics", "health", "demographics"]

### indicators
指标/变量的大致数量

## 数据内容 (data_content)

格式："类别名 - 详细说明"

示例：
```json
{
  "en": [
    "National Accounts - GDP, GNI, national income and expenditure accounts",
    "Population Statistics - Census data, demographic indicators, birth/death rates"
  ],
  "zh": [
    "国民经济核算 - GDP、GNI、国民收入和支出账户",
    "人口统计 - 普查数据、人口指标、出生/死亡率"
  ]
}
```

## 数据特征 (data_characteristics)

### types
statistical | time-series | cross-sectional | panel | geospatial | text | image | api

### granularity
数据粒度级别，如: ["national", "provincial", "monthly"]

### formats
可用数据格式，如: ["CSV", "Excel", "JSON"]

### languages
ISO 639-1 代码，如: ["zh", "en"]

## 质量评分 (quality) ⭐ 重要

⚠️ **6 维度评分系统** - 所有评分必须是整数 1-5

### authority_level
来源权威性 (1-5 整数)
- 5: 国际组织、国家央行、最高统计机关
- 4: 部委级政府机构、顶级研究机构
- 3: 省级政府、知名大学、行业协会
- 2: 地市级政府、专业研究机构
- 1: 区县级、第三方商业机构

### methodology_transparency
方法论透明度 (1-5 整数)
- 5: 完整公开方法论 + 数据收集流程 + 质量控制 + 可复现
- 4: 公开方法论 + 数据收集流程
- 3: 基本方法论说明
- 2: 简单提及方法
- 1: 无方法论说明

### update_timeliness
更新及时性 (1-5 整数)
- 5: 实时/每日 (`real-time`, `daily`)
- 4: 每周/每月 (`weekly`, `monthly`)
- 3: 每季度/每年 (`quarterly`, `annual`)
- 2: 不定期但在更新 (`irregular`)
- 1: 一次性或已停止 (`one-time`)

### data_completeness
数据完整性 (1-5 整数)
- 5: 全球/全国范围 + 50年以上 + 该领域最全面
- 4: 全球/全国范围 + 20年以上 + 覆盖主要主题
- 3: 区域/省级范围 + 10年以上 + 覆盖核心主题
- 2: 部分地区 + 5年以上 + 部分主题
- 1: 单一地区 + 少于5年 + 单一主题

### documentation_quality
文档质量 (1-5 整数)
- 5: 完整文档 + 示例代码 + 用户指南 + 方法论 + 数据字典
- 4: 完整文档 + 用户指南 + 数据字典
- 3: 基本文档 + 数据字典
- 2: 仅有基本说明文档
- 1: 无文档或文档不清晰

### citation_count
引用频次 (1-5 整数)
- 5: 被广泛引用，学术界和实务界的标准数据源
- 4: 经常被引用，领域内知名度高
- 3: 定期被引用，有一定影响力
- 2: 偶尔被引用，知名度一般
- 1: 很少被引用或无引用记录

**评估依据**：
- 学术论文引用次数（Google Scholar, Web of Science）
- 政策文件和报告引用
- 行业报告和分析引用
- 媒体报道引用

### 示例

```json
{
  "quality": {
    "authority_level": 5,
    "methodology_transparency": 4,
    "update_timeliness": 5,
    "data_completeness": 5,
    "documentation_quality": 4,
    "citation_count": 5
  }
}
```

## 许可协议 (licensing)

- `license`: 许可证名称
- `commercial_use`: boolean
- `attribution_required`: boolean
- `restrictions`: 使用限制数组

## 元数据标准 (metadata)

- `standards_followed`: ["SDMX", "ISO 3166", ...]
- `data_dictionary`: boolean
- `methodology_docs`: boolean
- `user_guide`: boolean

## 使用信息 (usage)

- `use_cases`: 常见用例数组
- `example_studies`: 示例研究
- `code_examples`: 代码示例 URL

## 其他字段

### related_sources
相关数据源的 ID 数组

### contact
联系信息对象

### catalog_metadata
- `added_date`: YYYY-MM-DD
- `last_updated`: YYYY-MM-DD
- `verified_date`: YYYY-MM-DD
- `contributor`: 贡献者名称
- `status`: active | inactive | deprecated | under_review

### tags
标签数组，用于搜索和分类
