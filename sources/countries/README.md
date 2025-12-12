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

### 🌏 亚洲 | Asia

1. **Bank of Japan Statistics** (`boj-statistics`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, PDF
   - 访问类型：开放
   - [查看详情](asia/boj-statistics.json)

2. **Directorate General of Commercial Intelligence and Statistics** (`india-dgcis`) ⭐💎
   - 权威性：5.0
   - 数据格式：text, Excel, PDF
   - 访问类型：开放
   - [查看详情](asia/india-dgcis.json)

3. **Bank of Korea** (`korea-bok`) ⭐💎
   - 权威性：5.0
   - 数据格式：Excel, CSV, PDF
   - 访问类型：开放
   - [查看详情](asia/korea-bok.json)

### 🌍 欧洲 | Europe

1. **Bank of England Statistical Interactive Database** (`uk-boe`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, XML, PDF
   - 访问类型：开放
   - [查看详情](europe/bank-of-england.json)

### 🌎 北美洲 | North America
- **国家数量**: 2
- **数据源总数**: 16
- [查看详情](north-america)

#### 🇨🇦 加拿大 | Canada
- **数据源数量**: 1
- **主要机构**: Statistics Canada
- [查看详情](north-america/canada/)

#### 🇺🇸 美国 | United States
- **数据源数量**: 3
- **主要机构**: United States Census Bureau, NOAA, USGS

**已收录数据源**:

1. **US Census Bureau** (`census-bureau`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, JSON, Excel, XML
   - 访问类型：开放
   - [查看详情](north-america/usa/census-bureau.json)

2. **NOAA Climate Data Online (CDO)** (`noaa-cdo`) ⭐
   - 权威性：4.8
   - 数据格式：CSV, JSON, XML, NetCDF, PDF
   - 访问类型：注册
   - [查看详情](north-america/usa/noaa-cdo.json)

3. **USGS EarthExplorer** (`usgs-earthexplorer`) ⭐💎
   - 权威性：5.0
   - 数据格式：GeoTIFF, HDF, NetCDF, JPEG2000, LAS, LAZ, Shapefile, KML
   - 访问类型：需注册
   - [查看详情](north-america/usa/usgs-earthexplorer.json)

4. **Agriculture and Agri-Food Canada** (`aafc`) ⭐💎
   - 权威性：5.0
   - 数据格式：GeoTIF, FGDB, GDB, CSV, Shapefile, JSON, REST API
   - 访问类型：开放
   - [查看详情](north-america/aafc.json)

5. **Bank of Mexico Economic Information System** (`mx-banxico`) ⭐💎
   - 权威性：5.0
   - 数据格式：JSON, XML, JSONP, Excel, CSV
   - 访问类型：开放
   - [查看详情](north-america/banxico.json)

6. **Bank of Canada** (`canada-boc`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, JSON, XML, Excel, RSS
   - 访问类型：开放
   - [查看详情](north-america/canada/canada-boc.json)

7. **Statistics Canada** (`canada-statcan`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, JSON, XML, Excel, SDMX, HTML, PDF
   - 访问类型：开放
   - [查看详情](north-america/canada/statcan.json)

8. **Canadian Institute for Health Information** (`canada-cihi`) ⭐💎
   - 权威性：5.0
   - 数据格式：Excel, CSV, PDF, HTML, JSON
   - 访问类型：开放
   - [查看详情](north-america/canada-cihi.json)

9. **Canada Energy Regulator** (`canada-cer`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, JSON, XML, Excel, Interactive Dashboards
   - 访问类型：开放
   - [查看详情](north-america/canada-energy-regulator.json)

10. **U.S. Energy Information Administration** (`usa-eia`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, JSON, XML, PDF, API
   - 访问类型：开放
   - [查看详情](north-america/eia.json)

11. **National Council for the Evaluation of Social Development Policy** (`mexico-coneval`) ⭐💎
   - 权威性：5.0
   - 数据格式：Excel, CSV, PDF
   - 访问类型：开放
   - [查看详情](north-america/mexico/coneval.json)

12. **Data.gov.uk** (`uk-data-gov`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, JSON, XML, Excel, PDF, RDF, Shapefile, GeoJSON
   - 访问类型：开放
   - [查看详情](north-america/uk-data-gov.json)

13. **Bureau of Economic Analysis** (`us-bea`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, JSON, XML, PDF
   - 访问类型：开放
   - [查看详情](north-america/us-bea.json)

14. **Bureau of Labor Statistics** (`us-bls`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, JSON, XML, PDF, TXT, API
   - 访问类型：开放
   - [查看详情](north-america/us-bls.json)

15. **Centers for Disease Control and Prevention** (`us-cdc`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, XML, Text, PDF, Interactive Query
   - 访问类型：开放
   - [查看详情](north-america/us-cdc.json)

16. **Data.gov** (`us-data-gov`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, JSON, XML, Excel, PDF, Shapefile, KML, RDF
   - 访问类型：开放
   - [查看详情](north-america/us-data-gov.json)

### 🌏 大洋洲 | Oceania

1. **Australian Bureau of Statistics** (`australia-abs`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, JSON, XML, API
   - 访问类型：开放
   - [查看详情](oceania/abs.json)

2. **Australian Institute of Health and Welfare** (`aus-aihw`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, Excel, JSON, PDF, Interactive dashboards
   - 访问类型：开放
   - [查看详情](oceania/aihw.json)

3. **Bureau of Meteorology** (`bureau-of-meteorology`) ⭐💎
   - 权威性：5.0
   - 数据格式：CSV, JSON, XML, NetCDF, GeoTIFF, GRIB2, HTML, PDF
   - 访问类型：需注册
   - [查看详情](oceania/bureau-of-meteorology.json)

### 🌎 南美洲 | South America

1. **Central Bank of Brazil** (`brazil-bcb`) ⭐💎
   - 权威性：5.0
   - 数据格式：JSON, CSV, XML, WSDL, OData, HTML, PDF
   - 访问类型：开放
   - [查看详情](south-america/brazil-bcb.json)

## 分类标准 | Classification Criteria

各国官方数据源按以下规则分类：

Official country data sources are classified according to the following rules:

- **路径格式** | Path Format: `sources/countries/{continent}/{country}/{id}.json`
- **大洲代码** | Continent Code: 使用英文小写大洲名称（如 `north-america`, `europe`, `asia`）
- **国家代码** | Country Code: 使用英文小写国家名称（如 `canada`, `usa`, `uk`）
- **文件命名** | File Naming: 直接使用数据源ID作为文件名，无需领域子目录

## 统计信息 | Statistics

- **已收录国家** | Countries Included: 11
- **总数据源** | Total Sources: 24
- **计划收录** | Planned: 200+

## 贡献 | Contributing

如需添加新国家的数据源，请参考[贡献指南](../../docs/CONTRIBUTING.md)。

To add data sources for new countries, please refer to the [Contributing Guide](../../docs/CONTRIBUTING.md).

---

**最后更新 | Last Updated**: 2025-12-11
