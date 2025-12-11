# DataSource Hub

**全球最全面、最权威、最结构化的开源数据源知识库**

**The World's Most Comprehensive, Authoritative, and Structured Open Data Source Repository**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Sources](https://img.shields.io/badge/Data%20Sources-28%2F950+-blue.svg)](tasks/README.md)
[![Progress](https://img.shields.io/badge/Progress-3%25-yellow.svg)](ROADMAP.md)
[![Quality Rating](https://img.shields.io/badge/Avg%20Quality-5.0%2F5.0-brightgreen.svg)](#)

---

## 📖 项目简介 | Project Overview

DataSource Hub 是一个开源的权威数据源知识库，旨在帮助研究人员、数据分析师、政策制定者和开发者快速发现和访问全球高质量的官方数据源。

DataSource Hub is an open-source authoritative data source knowledge base designed to help researchers, data analysts, policymakers, and developers quickly discover and access high-quality official data sources worldwide.

### 🎯 核心特色 | Key Features

#### 🏆 **深度覆盖中国数据源**
- **全球唯一**的中国官方数据源深度覆盖
- 规划收录 **488个** 中国国家级、省级、行业数据源
- 涵盖16个核心领域，从经济金融到社会民生

#### 📊 **结构化元数据体系**
- 基于 **JSON Schema** 的严格标准
- **40+字段** 的详细元数据信息
- 包括访问方式、覆盖范围、数据内容、质量评估等

#### ⭐ **6维度质量评级**
- 来源权威性 (Source Authority)
- 方法论透明度 (Methodology Transparency)
- 更新及时性 (Timeliness)
- 数据完整性 (Completeness)
- 文档质量 (Documentation Quality)
- 引用频次 (Citation Count)

#### 🌐 **中英双语支持**
- 所有元数据提供中英文双语
- 便于国内外用户使用

---

## 📂 项目结构 | Project Structure

```
datasource/
├── README.md                          # 项目主文档
├── PRD.md                             # 产品需求文档
├── ROADMAP.md                         # 项目路线图和里程碑 ⭐
├── PROJECT_STATUS.md                  # 项目当前状态
├── tasks/                             # 任务管理系统 ⭐
│   ├── README.md                      # 任务系统总览
│   ├── international.md               # 国际组织数据源 (100+)
│   ├── countries.md                   # 各国官方数据源 (200+)
│   ├── academic.md                    # 学术研究数据源 (50+)
│   ├── sectors.md                     # 行业领域数据源 (150+)
│   └── china/                         # 中国数据源任务 (488)
│       ├── README.md                  # 中国数据源总览
│       ├── finance.md                 # 金融财政领域 (35个)
│       └── [16个领域文件]             # 其他领域任务清单
├── sources/                           # 数据源元数据（核心资产）
│   ├── china/                         # 中国数据源 (6个已完成)
│   │   ├── README.md
│   │   ├── national/nbs.json         # 国家统计局 ⭐⭐⭐⭐⭐
│   │   ├── finance/
│   │   │   ├── banking/pbc.json      # 中国人民银行 ⭐⭐⭐⭐⭐
│   │   │   └── securities/csrc.json  # 证监会 ⭐⭐⭐⭐⭐
│   │   └── economy/
│   │       ├── macro/ndrc.json       # 发改委 ⭐⭐⭐⭐⭐
│   │       └── trade/
│   │           ├── customs.json      # 海关总署 ⭐⭐⭐⭐⭐
│   │           └── mofcom.json       # 商务部 ⭐⭐⭐⭐⭐
│   └── international/                 # 国际组织 (4个已完成)
│       └── economics/
│           ├── worldbank.json        # 世界银行 ⭐⭐⭐⭐⭐
│           ├── imf.json              # 国际货币基金组织 ⭐⭐⭐⭐⭐
│           ├── oecd.json             # 经合组织 ⭐⭐⭐⭐⭐
│           └── wto.json              # 世界贸易组织 ⭐⭐⭐⭐⭐
├── schemas/                           # JSON Schema 定义
│   └── datasource-schema.json        # 40+字段标准 ✅
├── scripts/                           # 工具脚本
│   ├── validate.py                   # 元数据验证 ✅
│   └── generate_indexes.py           # 索引生成 ✅
├── docs/                              # 完善的文档体系 ⭐
│   ├── CONTRIBUTING.md               # 贡献指南 ✅
│   ├── data-collection-guide.md      # 数据收录指南 ✅
│   └── quality-criteria.md           # 质量评估标准 ✅
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── claim-task.md             # 任务认领模板 ✅
└── indexes/                           # 自动生成的索引
    └── (运行脚本自动生成)
```

---

## 📊 当前进展 | Current Progress

### 总体统计 | Overall Statistics

| 指标 | 当前/目标 | 进度 |
|------|-----------|------|
| **总数据源** | 28 / 950+ | 3% |
| **国际组织** | 14 / 100+ | 14% |
| **各国官方** | 2 / 200+ | 1% |
| **中国数据源** | 7 / 488 | 1% |
| **学术研究** | 4 / 50+ | 8% |
| **行业领域** | 1 / 150+ | 1% |
| **平均权威性** | ⭐⭐⭐⭐⭐ (5.0/5.0) | - |
| **URL可访问性** | 100% | ✅ |

📋 **详细任务规划**: [tasks/README.md](tasks/README.md)
🗺️ **项目路线图**: [ROADMAP.md](ROADMAP.md)

### 已完成数据源 | Completed Sources

#### 🌍 国际组织 (14个)
- ✅ 世界银行 (World Bank) - 权威性 5.0 💎
- ✅ 国际货币基金组织 (IMF) - 权威性 5.0 💎
- ✅ 经合组织 (OECD) - 权威性 5.0 💎
- ✅ 世界贸易组织 (WTO) - 权威性 5.0 💎
- ✅ 国际能源署 (IEA) - 权威性 5.0 💎
- ✅ 世界知识产权组织 (WIPO) - 权威性 5.0 💎
- ✅ 亚洲开发银行 (ADB) - 权威性 5.0 💎
- ✅ 非洲开发银行 (AfDB) - 权威性 4.5 💎
- ✅ 美洲开发银行 (IDB) - 权威性 4.5 💎
- ✅ 国际清算银行 (BIS) - 权威性 5.0 💎
- ✅ 联合国粮农组织 (FAOSTAT) - 权威性 5.0 💎
- ✅ OECD国际学生评估项目 (PISA) - 权威性 5.0 💎
- ✅ NASA地球数据 (NASA Earthdata) - 权威性 5.0 💎

📄 **详细信息**: [sources/international/README.md](sources/international/README.md)

#### 🇨🇳 中国数据源 (7个)
- ✅ 国家统计局 (NBS) - 权威性 5.0 💎
- ✅ 中国人民银行 (PBC) - 权威性 5.0 💎
- ✅ 国家金融监督管理总局 (NFRA) - 权威性 5.0 💎
- ✅ 证监会 (CSRC) - 权威性 4.8 ⭐
- ✅ 海关总署 (Customs) - 权威性 5.0 💎
- ✅ 商务部 (MOFCOM) - 权威性 4.8 ⭐
- ✅ 发改委 (NDRC) - 权威性 4.6 ⭐
  
📄 **详细信息**: [sources/china/README.md](sources/china/README.md)

#### 🌎 各国官方 (2个)
- ✅ 加拿大统计局 (Statistics Canada) - 权威性 5.0 💎
- ✅ 美国人口普查局 (US Census Bureau) - 权威性 5.0 💎

📄 **详细信息**: [sources/countries/README.md](sources/countries/README.md)

#### 🎓 学术研究 (4个)
- ✅ 国家经济研究局 (NBER) - 权威性 5.0 💎
- ✅ 宾州世界表 (Penn World Table) - 权威性 5.0 💎
- ✅ 格罗宁根增长与发展中心数据库 (GGDC) - 权威性 5.0 💎
- ✅ 世界不平等数据库 (World Inequality Database) - 权威性 5.0 💎

📄 **详细信息**: [sources/academic/README.md](sources/academic/README.md)

#### 🏭 行业领域 (2个)
- ✅ ImageNet - 权威性 4.7 ⭐
- ✅ WIPO IP Statistics - 权威性 5.0 💎

📄 **详细信息**: [sources/sectors/README.md](sources/sectors/README.md)

---

## 🚀 快速开始 | Quick Start

### 浏览数据源 | Browse Data Sources

```bash
# 克隆仓库
git clone [repository-url]
cd datasource

# 查看中国数据源
cd sources/china
python view_samples.py
```

### 读取元数据 | Read Metadata

```python
import json

# 读取国家统计局数据源元数据
with open('sources/china/national/nbs.json', 'r', encoding='utf-8') as f:
    nbs = json.load(f)

print(f"Name: {nbs['name']['en']}")
print(f"URL: {nbs['access']['primary_url']}")
print(f"Quality: {sum(nbs['quality'].values())/6:.1f}/5.0")
print(f"Indicators: {nbs['coverage']['indicators']}")
```

### 按领域筛选 | Filter by Domain

```python
import json
from pathlib import Path

# 查找所有经济领域数据源
for json_file in Path('sources').rglob('*.json'):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'economics' in data['coverage']['domains']:
        print(f"✅ {data['name']['en']}")
```

---

## 🎓 元数据标准 | Metadata Schema

每个数据源包含以下标准化元数据：

### 必填字段 | Required Fields

```json
{
  "id": "unique-identifier",
  "name": {"en": "English Name", "zh": "中文名称"},
  "organization": {
    "name": "Organization Name",
    "type": "international_organization | national_government | research_institution",
    "country": "ISO 3166-1 code"
  },
  "description": {"en": "Description", "zh": "描述"},
  "access": {
    "primary_url": "https://...",
    "api": {...},
    "access_level": "open | registration | academic | commercial"
  },
  "coverage": {
    "geographic": {...},
    "temporal": {...},
    "domains": ["economics", "health", ...]
  },
  "data_content": {
    "en": ["Category 1 - Description", ...],
    "zh": ["分类1 - 说明", ...]
  },
  "quality": {
    "authority_level": 5,
    "methodology_transparency": 5,
    "update_timeliness": 4,
    "data_completeness": 5,
    "documentation_quality": 4,
    "citation_count": 5
  }
}
```

完整 Schema 请查看：[PRD.md - Section 3.1](PRD.md)

---

## 📈 项目规划 | Roadmap

详细路线图请查看：[ROADMAP.md](ROADMAP.md)

### M0: 项目初始化 ✅ (已完成)
- [x] 建立元数据标准 (40+字段 JSON Schema)
- [x] 创建中国核心数据源样例 (6个)
- [x] 创建国际核心数据源样例 (4个)
- [x] 完善的文档体系（贡献指南、收录指南、质量标准）
- [x] 任务管理系统（950+ 数据源规划）
- [x] 验证和索引生成脚本

### M1: 高优先级数据源 🚧 (进行中)
- [ ] 国际组织核心数据源 (15个目标，4个完成)
- [ ] 中国部委级数据源 (30个目标)
- [ ] 主要国家官方统计机构 (10个目标)

### M2: 规模扩展 📋 (计划中)
- [ ] 中国省级数据源 (60个)
- [ ] 学术研究数据源 (50个)
- [ ] 行业领域数据源 (150个)
- [ ] 达到 **300+** 数据源

### M3: 社区与工具 🔮 (未来)
- [ ] CI/CD 自动化验证
- [ ] Web 可视化界面
- [ ] API 服务
- [ ] 社区贡献流程优化

---

## 🤝 贡献指南 | Contributing

欢迎贡献新的数据源或改进现有信息！

### 📋 认领任务 | Claim a Task

1. 查看 [任务清单](tasks/README.md) 选择待完成的数据源
2. 使用 [认领模板](.github/ISSUE_TEMPLATE/claim-task.md) 创建 Issue
3. 等待维护者确认（24小时内）
4. 按照 [收录指南](docs/data-collection-guide.md) 完成收录
5. 提交 Pull Request

### 📚 完整文档 | Full Documentation

- **[贡献指南](docs/CONTRIBUTING.md)** - 完整的贡献流程和规范
- **[数据收录指南](docs/data-collection-guide.md)** - 详细的5步收录流程
- **[质量评估标准](docs/quality-criteria.md)** - 质量标准和评分体系
- **[任务系统](tasks/README.md)** - 950+ 数据源任务规划

### 数据源收录标准 | Inclusion Criteria

✅ **优先收录**：
- 政府官方机构数据（国家级、省级）
- 国际组织官方数据
- 顶级学术机构和研究数据仓库
- 定期更新的权威行业数据

❌ **不收录**：
- 完全商业付费数据（无免费层级）
- 个人或小型非官方组织数据
- 长期未更新的数据源（>3年）
- 无官方文档或无法验证的数据

---

## 📄 许可协议 | License

本项目采用 [MIT License](LICENSE) 开源。

数据源本身的许可协议请查看各数据源的 `licensing` 字段。

---

## 📞 联系方式 | Contact

- **项目主页**: https://code.mlamp.cn/0003432/datasource-hub
- **Issue 提交**: https://code.mlamp.cn/0003432/datasource-hub/issues
- **任务认领**: [创建 Issue](.github/ISSUE_TEMPLATE/claim-task.md)

---

## 🙏 致谢 | Acknowledgments

本项目灵感来源于：
- [OpenMetadata](https://github.com/open-metadata/OpenMetadata) - 数据目录平台
- SDMX 国际统计数据交换标准

感谢所有数据源的维护机构为开放数据做出的贡献！

---

## 📊 项目状态 | Project Status

| 指标 | 状态 |
|------|------|
| **当前里程碑** | M0 完成 ✅ / M1 进行中 🚧 |
| **总体进度** | 10 / 950+ (1%) |
| **完成度** | 国际组织 4%、中国 1% |
| **最近更新** | 2025-12-01 |
| **质量评分** | ⭐⭐⭐⭐⭐ (4.9/5.0) |

📊 **详细状态**: [PROJECT_STATUS.md](PROJECT_STATUS.md)
🗺️ **完整路线图**: [ROADMAP.md](ROADMAP.md)

---

<p align="center">
  <strong>打造全球最权威的数据源知识库</strong><br>
  <strong>Building the World's Most Authoritative Data Source Knowledge Base</strong>
</p>

<p align="center">
  Made with ❤️ by DataSource Hub Team
</p>
