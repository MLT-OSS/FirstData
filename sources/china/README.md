# China Data Sources - 中国数据源

## 概览 Overview

本目录包含中国官方数据源的元数据。根据PRD规划，中国数据源专区将深度覆盖16个领域，预计收录400+个高质量数据源。

This directory contains metadata for official Chinese data sources. According to the PRD, the China data sources section will provide in-depth coverage of 16 domains, with an estimated 400+ high-quality data sources.

## 当前样例 Current Samples

本次创建了6个高优先级数据源样例：

### 1. 国家级综合统计 National Statistics
- **[nbs.json](national/nbs.json)** - 国家统计局 (National Bureau of Statistics)
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 涵盖: GDP、人口、工业、投资、消费等全面统计
  - 更新频率: 月度

### 2. 金融财政 Finance
#### 银行系统 Banking
- **[pbc.json](finance/banking/pbc.json)** - 中国人民银行 (People's Bank of China)
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 涵盖: 货币供应、利率、汇率、外汇储备、信贷数据
  - 更新频率: 月度

#### 证券市场 Securities
- **[csrc.json](finance/securities/csrc.json)** - 证监会 (China Securities Regulatory Commission)
  - 权威性: ⭐⭐⭐⭐⭐ (4.8/5.0)
  - 涵盖: 股票市场、IPO、上市公司、债券、基金数据
  - 更新频率: 月度

### 3. 经济贸易 Economy & Trade
#### 对外贸易 Foreign Trade
- **[customs.json](economy/trade/customs.json)** - 海关总署 (General Administration of Customs)
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 涵盖: 进出口数据、贸易差额、HS商品分类
  - 更新频率: 月度

- **[mofcom.json](economy/trade/mofcom.json)** - 商务部 (Ministry of Commerce)
  - 权威性: ⭐⭐⭐⭐⭐ (4.8/5.0)
  - 涵盖: FDI、ODI、零售、电商、服务贸易
  - 更新频率: 月度

#### 宏观经济 Macroeconomics
- **[ndrc.json](economy/macro/ndrc.json)** - 国家发改委 (National Development and Reform Commission)
  - 权威性: ⭐⭐⭐⭐⭐ (4.6/5.0)
  - 涵盖: 固定资产投资、价格监测、产业政策
  - 更新频率: 月度

## 数据源特点 Data Source Features

### 高权威性 High Authority
- ✅ 所有数据源均为中国政府官方机构
- ✅ 平均权威性评分: 4.9/5.0
- ✅ 被学术界和业界广泛引用

### 全面覆盖 Comprehensive Coverage
- 📊 覆盖领域: 统计、金融、经济、贸易
- 🌏 地理范围: 全国、省级、地市级
- 📅 时间跨度: 1949年至今（国家统计局）

### 开放获取 Open Access
- 🆓 全部为开放数据，无需付费
- 📥 支持Excel、PDF、HTML等多种格式下载
- 🌐 提供中英文双语界面

## 目录结构 Directory Structure

```
sources/china/
├── national/           # 国家级综合统计
│   └── nbs.json
├── finance/            # 金融财政
│   ├── banking/        # 银行系统
│   │   └── pbc.json
│   └── securities/     # 证券市场
│       └── csrc.json
├── economy/            # 经济贸易
│   ├── macro/          # 宏观经济
│   │   └── ndrc.json
│   └── trade/          # 对外贸易
│       ├── customs.json
│       └── mofcom.json
└── README.md
```

## 下一步规划 Next Steps

根据PRD第6.4节，后续将添加以下领域的数据源：

### 即将添加 Coming Soon
1. **农业农村** Agriculture (18个数据源)
2. **自然资源** Natural Resources (22个数据源)
3. **生态环境** Environment (16个数据源)
4. **卫生健康** Health (21个数据源)
5. **教育科研** Education & Research (27个数据源)
6. **人力社保** Labor & Social Security (24个数据源)
7. **住房建设** Housing & Construction (24个数据源)
8. **交通运输** Transportation (32个数据源)
9. **文化旅游** Culture & Tourism (31个数据源)
10. **科技创新** Technology & Innovation (29个数据源)
11. **气象地震** Meteorology & Seismology (23个数据源)
12. **民政社会** Civil Affairs (23个数据源)
13. **公安司法** Public Security & Justice (25个数据源)
14. **审计税务** Audit & Taxation (21个数据源)
15. **省级数据** Provincial Data (60个数据源)
16. **研究机构** Research Institutions (6个数据源)
17. **行业协会** Industry Associations (7个数据源)
18. **特色数据** Special Data (8个数据源)

**总计目标**: 488个中国数据源

## 使用说明 Usage Guide

每个JSON文件遵循DataSource Hub标准元数据Schema，包含以下关键信息：

- **基本信息**: ID、名称（中英文）、维护机构
- **访问信息**: URL、API、下载方式、访问级别
- **覆盖范围**: 地理、时间、领域、指标数量
- **数据特征**: 类型、粒度、格式、语言
- **质量评估**: 权威性、透明度、及时性、完整性、文档质量（5维度评分）
- **许可协议**: License、使用限制
- **使用信息**: 应用场景、示例研究

## 贡献指南 Contributing

欢迎为中国数据源专区贡献新的数据源或更新现有信息！请参考：
- [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) - 贡献指南
- [data-collection-guide.md](../../docs/data-collection-guide.md) - 数据收集指南
- [quality-criteria.md](../../docs/quality-criteria.md) - 质量评估标准

## 联系方式 Contact

- 项目仓库: [待定]
- Issue提交: [待定]
- 讨论区: [待定]

---

**最后更新 Last Updated**: 2025-01-25
**状态 Status**: 样例阶段 (Sample Phase)
**完成度 Completion**: 6/488 (1.2%)
