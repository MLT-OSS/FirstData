# 行业领域 | Sector Data Sources

## 概览 | Overview

本目录包含特定行业和专业领域的数据源。

This directory contains data sources from specific industries and professional domains.

**路径**: `sources/sectors/`

## 目录结构 | Directory Structure

```
sectors/
├── energy/                  # 能源 | Energy
├── innovation_patents/      # 科技创新-专利 | Innovation & Patents
├── education/               # 教育评估 | Education Assessment
├── agriculture_food/        # 农业与食品 | Agriculture & Food
├── finance_markets/         # 金融市场 | Financial Markets
├── computer_science_ai/     # 计算机科学与AI/ML | Computer Science & AI/ML
├── nlp/                     # 自然语言处理 | Natural Language Processing
├── biology/                 # 生物与生命科学 | Biology & Life Sciences
├── chemistry_materials/     # 化学与材料 | Chemistry & Materials
├── geoscience_geography/    # 地球科学与地理 | Geoscience & Geography
├── social_media/            # 社交媒体与网络数据 | Social Media & Network Data
├── sports/                  # 体育运动 | Sports
├── transportation/          # 交通运输 | Transportation
├── museums_culture/         # 博物馆与文化遗产 | Museums & Cultural Heritage
├── timeseries/              # 时间序列数据 | Time Series Data
├── cybersecurity/           # 网络安全 | Cybersecurity
└── other/                   # 其他专业领域 | Other Professional Domains
```

## 已收录数据源 | Included Sources

### 计算机科学与AI/ML | Computer Science & AI/ML

1. **ImageNet** (`imagenet`) ⭐💎
   - 权威性：5.0
   - 数据格式：JPEG, tar, zip
   - 访问类型：学术注册
   - [查看详情](computer_science_ai/imagenet.json)

2. **CIFAR-10 and CIFAR-100** (`cifar`) ⭐💎
   - 权威性：5.0
   - 数据格式：Binary, Python pickle
   - 访问类型：开放
   - [查看详情](computer_science_ai/cifar.json)

3. **Common Crawl** (`common-crawl`) ⭐
   - 权威性：4.0
   - 数据格式：WARC, WET, WAT
   - 访问类型：开放
   - [查看详情](computer_science_ai/common-crawl.json)

### 自然语言处理 | Natural Language Processing

1. **BooksCorpus** (`bookscorpus`) ⭐
   - 权威性：3.0
   - 数据格式：Text
   - 访问类型：学术注册
   - [查看详情](nlp/bookscorpus.json)

2. **CoNLL Shared Tasks Data** (`conll-shared-tasks`) ⭐💎
   - 权威性：5.0
   - 数据格式：CoNLL format, Text
   - 访问类型：开放
   - [查看详情](nlp/conll-shared-tasks.json)

### 生物与生命科学 | Biology & Life Sciences

1. **The Cancer Genome Atlas** (`tcga`) ⭐💎
   - 权威性：5.0
   - 数据格式：BAM, VCF, TSV
   - 访问类型：受控访问
   - [查看详情](biology/tcga.json)

### 化学与材料 | Chemistry & Materials

1. **Cambridge Structural Database (CSD)** (`cambridge-structural-database`) ⭐💎
   - 权威性：5.0
   - 数据格式：CIF, MOL
   - 访问类型：订阅
   - [查看详情](chemistry_materials/cambridge-structural-database.json)

### 能源 | Energy

1. **Statistical Review of World Energy** (`bp-statistical-review`) ⭐💎
   - 权威性：5.0
   - 数据格式：Excel, CSV, PDF
   - 访问类型：开放
   - [查看详情](energy/bp-statistical-review.json)

### 金融市场 | Financial Markets

1. **CRSP - Center for Research in Security Prices** (`crsp`) ⭐💎
   - 权威性：5.0
   - 数据格式：SAS, CSV
   - 访问类型：订阅
   - [查看详情](finance_markets/crsp.json)

2. **Bloomberg Terminal (Public Data)** (`bloomberg-terminal`) ⭐💎
   - 权威性：5.0
   - 数据格式：Proprietary
   - 访问类型：订阅
   - [查看详情](finance_markets/bloomberg-terminal.json)

3. **Cryptocurrency Market Data (CoinMarketCap & CoinGecko)** (`cryptocurrency-data`) ⭐
   - 权威性：4.0
   - 数据格式：JSON, CSV
   - 访问类型：免费+付费API
   - [查看详情](finance_markets/cryptocurrency-data.json)

4. **Alpha Vantage API** (`alpha-vantage`) ⭐
   - 权威性：4.0
   - 数据格式：JSON, CSV
   - 访问类型：免费+付费API
   - [查看详情](finance_markets/alpha-vantage.json)

### 科技创新与专利 | Innovation & Patents

1. **Derwent Innovation Index** (`derwent-innovation-index`) ⭐💎
   - 权威性：5.0
   - 数据格式：Proprietary
   - 访问类型：订阅
   - [查看详情](innovation_patents/derwent-innovation-index.json)

### 教育评估 | Education Assessment

1. **Academic Ranking of World Universities** (`arwu`) ⭐💎
   - 权威性：5.0
   - 数据格式：Excel, HTML
   - 访问类型：开放
   - [查看详情](education/arwu.json)

### 农业与食品 | Agriculture & Food

1. **Agricultural Market Information System (AMIS)** (`amis`) ⭐💎
   - 权威性：5.0
   - 数据格式：Excel, CSV
   - 访问类型：开放
   - [查看详情](agriculture_food/amis.json)

### 博物馆与文化遗产 | Museums & Cultural Heritage

1. **British Museum Collection** (`british-museum-collection`) ⭐💎
   - 权威性：5.0
   - 数据格式：JSON, IIIF
   - 访问类型：开放
   - [查看详情](museums_culture/british-museum-collection.json)

### 体育运动 | Sports

1. **ATP/WTA Tennis Data** (`tennis-atp-wta-data`) ⭐
   - 权威性：4.0
   - 数据格式：CSV
   - 访问类型：开放
   - [查看详情](sports/tennis-atp-wta-data.json)

## 统计信息 | Statistics

- **已收录**: 17
- **计划收录**: 150+
- **覆盖领域**: 17 个专业领域

## 分类标准 | Classification Criteria

行业领域数据源按专业领域分类：

Sector data sources are classified by professional domain:

- **路径格式** | Path Format: `sources/sectors/{industry}/{id}.json`
- **行业划分** | Industry Division: 按照专业领域和行业特征划分
- **文件命名** | File Naming: 使用数据源 ID

## 贡献 | Contributing

如需添加或更新行业领域数据源，请参考[贡献指南](../../docs/CONTRIBUTING.md)。

To add or update sector data sources, please refer to the [Contributing Guide](../../docs/CONTRIBUTING.md).

---

**最后更新 | Last Updated**: 2025-12-09
