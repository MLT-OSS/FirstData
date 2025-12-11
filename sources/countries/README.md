# 各国官方数据源 | Official Data Sources by Country

## 概览 | Overview

本目录包含各国官方政府机构发布的权威数据源。

This directory contains official data sources from government agencies of various countries.

## 目录结构 | Directory Structure

```
sources/countries/
├── north-america/        # 北美洲 | North America
│   ├── canada/          # 加拿大 | Canada
│   ├── usa/             # 美国 | United States (planned)
│   └── mexico/          # 墨西哥 | Mexico (planned)
├── europe/              # 欧洲 | Europe (planned)
├── asia/                # 亚洲 | Asia (planned)
├── oceania/             # 大洋洲 | Oceania (planned)
├── south-america/       # 南美洲 | South America (planned)
└── africa/              # 非洲 | Africa (planned)
```

## 已收录地区 | Included Regions

### 🌎 北美洲 | North America
- **国家数量**: 2
- **数据源总数**: 2
- [查看详情](north-america)

#### 🇨🇦 加拿大 | Canada
- **数据源数量**: 1
- **主要机构**: Statistics Canada
- [查看详情](north-america/canada/)

#### 🇺🇸 美国 | United States
- **数据源数量**: 1
- **主要机构**: United States Census Bureau
- [查看详情](north-america/usa/)

## 分类标准 | Classification Criteria

各国官方数据源按以下规则分类：

Official country data sources are classified according to the following rules:

- **路径格式** | Path Format: `sources/countries/{continent}/{country}/{id}.json`
- **大洲代码** | Continent Code: 使用英文小写大洲名称（如 `north-america`, `europe`, `asia`）
- **国家代码** | Country Code: 使用英文小写国家名称（如 `canada`, `usa`, `uk`）
- **文件命名** | File Naming: 直接使用数据源ID作为文件名，无需领域子目录

## 统计信息 | Statistics

- **已收录国家** | Countries Included: 2
- **总数据源** | Total Sources: 2
- **计划收录** | Planned: 200+

## 贡献 | Contributing

如需添加新国家的数据源，请参考[贡献指南](../../docs/CONTRIBUTING.md)。

To add data sources for new countries, please refer to the [Contributing Guide](../../docs/CONTRIBUTING.md).

---

**最后更新 | Last Updated**: 2025-12-10
