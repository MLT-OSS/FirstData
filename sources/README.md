# 数据源集合 | Data Sources

## 概览 | Overview

本目录包含 DataSource Hub 收录的所有数据源元数据。

This directory contains metadata for all data sources included in DataSource Hub.

## 目录结构 | Directory Structure

### 📂 中国数据源 | China
**路径**: `sources/china/`

中国政府机构和官方组织发布的权威数据源。

Official data sources from Chinese government agencies and organizations.

[查看详情 | View Details →](china/README.md)

### 🌍 国际组织 | International
**路径**: `sources/international/`

国际组织和跨国机构发布的全球性数据源。

Global data sources from international organizations and multinational agencies.

[查看详情 | View Details →](international/README.md)

### 🌎 各国官方 | Countries
**路径**: `sources/countries/`

各国官方政府机构发布的权威数据源。

Official data sources from government agencies of various countries.

[查看详情 | View Details →](countries/README.md)

### 🎓 学术研究 | Academic
**路径**: `sources/academic/`

学术机构和研究组织维护的学术研究数据源。

Academic research data sources maintained by educational and research institutions.

[查看详情 | View Details →](academic/README.md)

### 🏭 行业领域 | Sectors
**路径**: `sources/sectors/`

特定行业和专业领域的数据源。

Data sources from specific industries and professional domains.

[查看详情 | View Details →](sectors/README.md)

## 数据源统计 | Statistics

| 类别 Category | 数量 Count | 状态 Status |
|--------------|-----------|------------|
| 中国 China | 10 | ✅ Active |
| 国际 International | 4 | ✅ Active |
| 各国 Countries | 1 | ✅ Active |
| 学术 Academic | 1 | ✅ Active |
| 行业 Sectors | 0 | 🔄 Planned |
| **总计 Total** | **16** | - |

## 分类规则 | Classification Rules

### 路径格式 | Path Format

- **中国数据源**: `sources/china/{domain}/{subdomain}/{id}.json`
- **国际组织**: `sources/international/{domain}/{id}.json`
- **各国官方**: `sources/countries/{continent}/{country}/{id}.json`
- **学术研究**: `sources/academic/{domain}/{id}.json`
- **行业领域**: `sources/sectors/{industry}/{id}.json`

### 命名规范 | Naming Convention

- 文件名使用数据源 ID
- ID 格式：`{国家/组织}-{简称}` (如 `china-pbc`, `canada-statcan`)
- 使用小写字母和连字符

## 贡献 | Contributing

如需添加或更新数据源，请参考[贡献指南](../docs/CONTRIBUTING.md)。

To add or update data sources, please refer to the [Contributing Guide](../docs/CONTRIBUTING.md).

---

**最后更新 | Last Updated**: 2025-12-09
