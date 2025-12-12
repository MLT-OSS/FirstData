# 学术研究 | Academic Research

## 概览 | Overview

本目录包含学术研究机构和数据仓库的元数据。学术研究数据源专区涵盖经济学、健康医学、环境科学、社会科学、物理化学、生命科学等多个领域，预计收录50+个高质量学术数据源。

This directory contains metadata for academic research institutions and data repositories. The academic research data sources section covers economics, health, environmental science, social science, physical chemistry, life sciences, and other fields, with an estimated 50+ high-quality academic data sources.

## 目录结构 Directory Structure

```
academic/
├── repositories/      # 综合性数据仓库 General Data Repositories
├── economics/         # 经济学 Economics
├── health/            # 健康医学 Health & Medicine
├── environment/       # 环境科学 Environmental Science
├── social/            # 社会科学 Social Science
├── physics_chemistry/ # 物理化学 Physics & Chemistry
└── biology/           # 生命科学 Life Sciences & Biology
```

## 当前收录 Current Collection

### 经济学 Economics

#### BIS Statistics
- **[bis-statistics.json](economics/bis-statistics.json)** - 国际清算银行统计数据
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 国际金融数据、银行统计、金融市场数据
  - 涵盖: 全球，1948-2025年，5,000+指标
  - 更新频率: 季度
  - 特色: 国际银行统计、国际债务证券、全球流动性指标、OTC衍生品、外汇汇率、支付系统

#### The Conference Board Economic Data
- **[conference-board.json](economics/conference-board.json)** - 世界大型企业联合会经济数据
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 经济指标、景气指数、生产率数据
  - 涵盖: 全球主要经济体，1948-2025年
  - 更新频率: 月度
  - 特色: 领先经济指数(LEI)、消费者信心指数、CEO信心指数、劳动生产率数据

#### NBER - National Bureau of Economic Research
- **[nber.json](economics/nber.json)** - 国家经济研究局
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 研究论文、公共数据集、经济指标
  - 涵盖: 34,000+ 工作论文，商业周期数据，劳动经济学，生产率指标
  - 更新频率: 每周
  - 特色: 43位诺贝尔经济学奖获得者，1,800+附属经济学家

#### Penn World Table
- **[penn-world-table.json](economics/penn-world-table.json)** - 宾州世界表
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 跨国比较数据、经济增长、生产率
  - 涵盖: 185个国家，1950-2023年，50+经济指标
  - 更新频率: 年度
  - 特色: GDP、PPP、资本存量、全要素生产率、人力资本

#### GGDC Databases
- **[ggdc-databases.json](economics/ggdc-databases.json)** - 格罗宁根增长与发展中心数据库
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 生产率、全球价值链、历史发展、结构变化
  - 涵盖: 200+国家，1870-2023年，200+指标
  - 更新频率: 年度
  - 特色: Penn World Table、EU KLEMS、WIOD、Maddison Project等多个数据库

#### World Inequality Database
- **[world-inequality-database.json](economics/world-inequality-database.json)** - 世界不平等数据库
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 收入分配、财富不平等、社会不平等
  - 涵盖: 70+国家，1900-2024年，100+不平等指标
  - 更新频率: 年度
  - 特色: 顶层收入份额、财富集中度、性别不平等、World Inequality Report数据来源

### 健康医学 Health & Medicine

#### PubMed
- **[pubmed.json](health/pubmed.json)** - PubMed生物医学文献数据库
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 文献引用、摘要、全文链接、API
  - 涵盖: 全球范围，3900万+引用文献，1946-2025年
  - 更新频率: 每日
  - 特色: MEDLINE索引、MeSH主题词、PMC全文、E-utilities API、免费访问

#### ClinicalTrials.gov
- **[clinicaltrials-gov.json](health/clinicaltrials-gov.json)** - 临床试验注册数据库
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 临床试验注册、研究设计、结果数据、API
  - 涵盖: 全球220个国家，40万+临床试验，2000-2025年
  - 更新频率: 每日
  - 特色: NCT编号、患者招募、试验方案、API v2.0、免费访问

#### Demographic and Health Surveys (DHS)
- **[dhs.json](health/dhs.json)** - 人口与健康调查项目
  - 权威性: ⭐⭐⭐⭐⭐ (4.8/5.0)
  - 类型: 人口统计、健康调查、横截面数据、API
  - 涵盖: 90个发展中国家，400+调查，1984-2025年
  - 更新频率: 不定期（每国约5年一次）
  - 特色: USAID资助、家庭调查、母婴健康、艾滋病、营养数据、需注册访问

#### Global Health Data Exchange (GHDx)
- **[ghdx.json](health/ghdx.json)** - 全球健康数据交换平台
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 全球疾病负担、健康指标、时间序列、API
  - 涵盖: 204个国家，1950-2025年，1万+健康指标
  - 更新频率: 不定期（GBD研究更新）
  - 特色: IHME维护、GBD数据、死亡率、疾病负担、健康融资、风险因素

#### The Cancer Genome Atlas (TCGA)
- **[tcga.json](health/tcga.json)** - 癌症基因组图谱
  - 权威性: ⭐⭐⭐⭐⭐ (4.6/5.0)
  - 类型: 基因组数据、癌症研究、横截面、API
  - 涵盖: 美国，2万+样本，33种癌症类型，2006-2018年
  - 更新频率: 一次性（项目已完成）
  - 特色: NCI/NHGRI、全基因组测序、RNA-seq、甲基化、蛋白质组、GDC平台

#### UK Biobank
- **[uk-biobank.json](health/uk-biobank.json)** - 英国生物样本库
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 队列研究、多模态数据、纵向、API
  - 涵盖: 英国，50万参与者，1万+指标，2006-2025年
  - 更新频率: 不定期（持续随访）
  - 特色: 全基因组测序、影像数据、生物标志物、医疗记录、需申请访问

### 环境科学 Environmental Science

#### Copernicus Open Access Hub
- **[copernicus-open-access-hub.json](environment/copernicus-open-access-hub.json)** - 哥白尼开放访问中心
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 地球观测数据、卫星遥感、环境监测
  - 涵盖: 全球，2014-2025年
  - 更新频率: 每日
  - 特色: Sentinel卫星数据、大气监测、海洋监测、陆地监测、气候变化、紧急管理

### 生命科学 Life Sciences & Biology

#### 1000 Genomes Project
- **[1000-genomes.json](biology/1000-genomes.json)** - 千人基因组计划
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 人类基因组变异、群体遗传学数据
  - 涵盖: 全球26个群体，2,504个个体，2008-2015年
  - 更新频率: 一次性（项目已完成）
  - 特色: 全基因组测序、变异数据、群体基因组学、单核苷酸多态性(SNP)、结构变异

#### GenBank
- **[genbank.json](biology/genbank.json)** - 基因库
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 基因序列、DNA数据库、API
  - 涵盖: 全球所有生物，1982-2025年
  - 更新频率: 每日
  - 特色: NCBI维护、INSDC成员、E-utilities API、所有公开DNA序列、免费访问

### 物理与化学 Physics & Chemistry

#### CERN Open Data Portal
- **[cern-open-data.json](physics_chemistry/cern-open-data.json)** - CERN 开放数据门户
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 粒子物理实验数据、高能物理数据
  - 涵盖: CERN实验，2010-2025年
  - 更新频率: 不定期
  - 特色: LHC实验数据、CMS实验、ALICE实验、ATLAS实验、教育资源、模拟数据

#### Crystallography Open Database
- **[crystallography-open-database.json](physics_chemistry/crystallography-open-database.json)** - 晶体学开放数据库
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 晶体结构数据、化学信息学
  - 涵盖: 全球，500,000+晶体结构，1915-2025年
  - 更新频率: 每日
  - 特色: 开放访问、CIF格式、无机/有机/金属有机晶体、结构参数、空间群信息

### 社会科学 Social Science

#### Afrobarometer
- **[afrobarometer.json](social/afrobarometer.json)** - 非洲晴雨表
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 公众态度调查、民主治理、社会经济数据
  - 涵盖: 39个非洲国家，1999-2025年
  - 更新频率: 不定期（约2-3年一轮）
  - 特色: 民主态度、治理质量、经济状况、社会价值观、选举行为、公民参与

#### Asian Barometer Survey
- **[asian-barometer.json](social/asian-barometer.json)** - 亚洲民主动态调查
  - 权威性: ⭐⭐⭐⭐⭐ (5.0/5.0)
  - 类型: 公众态度调查、民主治理、政治文化
  - 涵盖: 20个亚洲国家和地区，2001-2025年
  - 更新频率: 不定期（约3-4年一轮）
  - 特色: 民主化进程、政治价值观、政治参与、公民社会、治理评估、社会信任

## 数据源特点 Data Source Features

- **顶级学术权威**: 收录世界顶尖研究机构和大学的数据源
- **高质量研究数据**: 经过学术同行评审或严格质量控制
- **开放获取**: 大部分数据源提供开放访问或注册后免费使用
- **多学科覆盖**: 涵盖自然科学、社会科学、健康医学等多个领域
- **可复现性支持**: 提供代码、方法论文档，支持研究复现

## 收录标准 Inclusion Criteria

1. **学术权威性**: 由知名研究机构、大学或学术组织维护
2. **数据质量**: 数据经过严格的质量控制和验证
3. **可访问性**: 提供公开访问或注册后免费使用
4. **文档完整**: 提供详细的数据说明和方法论文档
5. **引用价值**: 在学术界具有广泛引用和认可

## 使用说明 Usage Notes

学术数据源主要面向：
- 学术研究人员和博士生
- 政策分析师和智库研究员
- 数据科学家和统计学家
- 教育工作者和学生

大部分数据源要求：
- 引用数据来源
- 遵守使用许可协议
- 不用于商业用途（部分数据源）

## 相关任务 Related Tasks

详细的收录计划和进度追踪请参见：
- [学术研究数据源任务清单](../../tasks/academic.md)

---

**总进度 Overall Progress**: 19/50+ 已完成 (38%)
**最近更新 Last Updated**: 2025-12-11
