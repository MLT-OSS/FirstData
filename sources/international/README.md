# 国际数据源 | International Data Sources

## 概览 | Overview

本目录包含国际组织和跨国机构发布的全球性数据源。

This directory contains global data sources from international organizations and multinational agencies.

**路径**: `sources/international/`

## 目录结构 | Directory Structure

```
international/
├── economics/        # 经济 | Economics
├── trade/            # 贸易 | Trade
├── energy/           # 能源 | Energy
├── agriculture/      # 农业 | Agriculture
├── health/           # 健康 | Health
├── environment/      # 环境 | Environment
└── development/      # 发展 | Development
```

## 已收录数据源 | Included Sources

### 经济 | Economics

1. **World Bank** (`intl-worldbank`) ⭐💎
   - 权威性：5.0
   - 数据格式：JSON, XML, CSV, Excel
   - 访问类型：开放
   - [查看详情](economics/worldbank.json)

2. **IMF - International Monetary Fund** (`intl-imf`) ⭐💎
   - 权威性：5.0
   - 数据格式：SDMX, JSON, CSV, Excel
   - 访问类型：开放
   - [查看详情](economics/imf.json)

3. **OECD** (`intl-oecd`) ⭐💎
   - 权威性：5.0
   - 数据格式：SDMX, JSON, CSV
   - 访问类型：开放
   - [查看详情](economics/oecd.json)

4. **BIS Statistics - Bank for International Settlements** (`bis-statistics`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, SDMX, JSON
   - 访问类型：开放
   - [查看详情](economics/bis.json)

### 贸易 | Trade

1. **WTO - World Trade Organization** (`intl-wto`) ⭐💎
   - 权威性：5.0
   - 数据格式：Excel, CSV
   - 访问类型：开放
   - [查看详情](trade/wto.json)

### 能源 | Energy

1. **IEA Energy Data** (`iea-energy-data`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, SDMX, JSON, XML
   - 访问类型：注册
   - [查看详情](energy/iea.json)

### 知识产权 | Intellectual Property

1. **WIPO IP Statistics** (`wipo-ip-statistics`) ⭐💎
   - 权威性：5.0
   - 数据格式：Excel, PDF, CSV
   - 访问类型：开放
   - [查看详情](wipo.json)

### 农业 | Agriculture

1. **FAOSTAT - Food and Agriculture Data** (`faostat`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, JSON, XML
   - 访问类型：开放
   - [查看详情](agriculture/faostat.json)

## 统计信息 | Statistics

- **已收录**: 8
- **计划收录**: 20+
- **覆盖领域**: 经济、贸易、能源、农业、知识产权、健康、环境、发展

## 分类标准 | Classification Criteria

国际数据源按主题领域分类：

International data sources are classified by thematic domain:

- **路径格式** | Path Format: `sources/international/{domain}/{id}.json`
- **领域划分** | Domain Division: economics, trade, health, environment, development
- **文件命名** | File Naming: 使用数据源 ID（如 `worldbank.json`, `imf.json`）

## 贡献 | Contributing

如需添加或更新国际数据源，请参考[贡献指南](../../docs/CONTRIBUTING.md)。

To add or update international data sources, please refer to the [Contributing Guide](../../docs/CONTRIBUTING.md).

---

**最后更新 | Last Updated**: 2025-12-10
