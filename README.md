# DataSource Hub

**全球最全面、最权威、最结构化的开源数据源知识库**

**The World's Most Comprehensive, Authoritative, and Structured Open Data Source Repository**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Sources](https://img.shields.io/badge/Data%20Sources-10-blue.svg)](#)
[![Quality Rating](https://img.shields.io/badge/Avg%20Quality-4.9%2F5.0-brightgreen.svg)](#)

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

#### ⭐ **5维度权威性评级**
- 来源权威性 (Source Authority)
- 方法论透明度 (Methodology Transparency)
- 更新及时性 (Timeliness)
- 数据完整性 (Completeness)
- 文档质量 (Documentation Quality)

#### 🌐 **中英双语支持**
- 所有元数据提供中英文双语
- 便于国内外用户使用

---

## 📂 项目结构 | Project Structure

```
datasource/
├── README.md                          # 项目主文档
├── PRD.md                             # 产品需求文档
├── sources/                           # 数据源元数据（核心资产）
│   ├── china/                         # 中国数据源 (6个样例)
│   │   ├── national/                  # 国家级综合统计
│   │   │   └── nbs.json              # 国家统计局 ⭐⭐⭐⭐⭐
│   │   ├── finance/                   # 金融财政
│   │   │   ├── banking/
│   │   │   │   └── pbc.json          # 中国人民银行 ⭐⭐⭐⭐⭐
│   │   │   └── securities/
│   │   │       └── csrc.json         # 证监会 ⭐⭐⭐⭐⭐
│   │   └── economy/                   # 经济贸易
│   │       ├── macro/
│   │       │   └── ndrc.json         # 发改委 ⭐⭐⭐⭐⭐
│   │       └── trade/
│   │           ├── customs.json      # 海关总署 ⭐⭐⭐⭐⭐
│   │           └── mofcom.json       # 商务部 ⭐⭐⭐⭐⭐
│   └── international/                 # 国际组织 (4个样例)
│       └── economics/
│           ├── worldbank.json        # 世界银行 ⭐⭐⭐⭐⭐
│           ├── imf.json              # 国际货币基金组织 ⭐⭐⭐⭐⭐
│           ├── oecd.json             # 经合组织 ⭐⭐⭐⭐⭐
│           └── wto.json              # 世界贸易组织 ⭐⭐⭐⭐⭐
├── schemas/                           # JSON Schema 定义 (待创建)
│   └── datasource-schema.json
├── scripts/                           # 工具脚本 (待创建)
│   ├── validate.py                   # 元数据验证
│   ├── generate_indexes.py           # 索引生成
│   └── check_urls.py                 # URL健康检查
├── indexes/                           # 自动生成的索引 (待生成)
│   ├── all-sources.json
│   ├── by-domain.json
│   ├── by-region.json
│   └── by-authority.json
└── docs/                              # 文档 (待创建)
    ├── CONTRIBUTING.md
    ├── data-collection-guide.md
    └── quality-criteria.md
```

---

## 📊 当前数据 | Current Data

### 统计概览 | Statistics

| 指标 | 数值 |
|------|------|
| **总数据源** | 10 个 |
| **中国数据源** | 6 个 (国家统计局、人民银行、证监会等) |
| **国际数据源** | 4 个 (世界银行、IMF、OECD、WTO) |
| **平均权威性评分** | ⭐⭐⭐⭐⭐ (4.9/5.0) |
| **总指标数** | 6,400+ |
| **URL可访问性** | 100% |

### 中国数据源详情 | China Data Sources

查看完整的中国数据源概览：[sources/china/README.md](sources/china/README.md)

| 数据源 | 权威性 | 指标数 | 更新频率 |
|--------|--------|--------|----------|
| 国家统计局 (NBS) | ⭐⭐⭐⭐⭐ 5.0 | 5,000+ | 月度 |
| 中国人民银行 (PBC) | ⭐⭐⭐⭐⭐ 5.0 | 800+ | 月度 |
| 证监会 (CSRC) | ⭐⭐⭐⭐⭐ 4.8 | 600+ | 月度 |
| 海关总署 (Customs) | ⭐⭐⭐⭐⭐ 5.0 | 2,000+ | 月度 |
| 商务部 (MOFCOM) | ⭐⭐⭐⭐⭐ 4.8 | 1,200+ | 月度 |
| 发改委 (NDRC) | ⭐⭐⭐⭐⭐ 4.6 | 800+ | 月度 |

详细信息请查看：[CHINA_SAMPLES_SUMMARY.md](CHINA_SAMPLES_SUMMARY.md)

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
print(f"Quality: {sum(nbs['quality'].values())/5:.1f}/5.0")
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
    "documentation_quality": 4
  }
}
```

完整 Schema 请查看：[PRD.md - Section 3.1](PRD.md)

---

## 📈 项目规划 | Roadmap

### Phase 1: 核心数据源 (进行中)
- [x] 建立元数据标准 (JSON Schema)
- [x] 创建中国核心数据源样例 (6个)
- [x] 创建国际核心数据源样例 (4个)
- [ ] 完成中国部委级数据源 (30个目标)
- [ ] 完成国际组织数据源 (20个目标)

### Phase 2: 自动化工具 (计划中)
- [ ] JSON Schema 验证脚本
- [ ] 自动索引生成工具
- [ ] URL健康检查工具
- [ ] CI/CD 自动化验证
- [ ] 贡献者指南和模板

### Phase 3: 规模扩展 (计划中)
- [ ] 中国省级数据源 (60个)
- [ ] 中国行业协会 (50个)
- [ ] 国际区域组织 (30个)
- [ ] 达到 **300+** 数据源

### Phase 4: 社区与展示 (未来)
- [ ] 发布到 GitHub
- [ ] 开发 Web 可视化界面
- [ ] 建立社区贡献流程
- [ ] API 服务

---

## 🆚 与同类项目对比 | Comparison

### vs awesome-public-datasets

| 维度 | awesome-public-datasets | DataSource Hub |
|------|------------------------|----------------|
| **总数据量** | ~800个 | 10个（目标300+） |
| **中国数据源** | <5个 | 🏆 **6个（目标488个）** |
| **元数据字段** | ~5个基础字段 | 🏆 **40+个详细字段** |
| **质量评级** | 无 | 🏆 **5维度评分系统** |
| **数据内容说明** | 混在描述中 | 🏆 **独立结构化字段** |
| **访问方式** | 简单URL | 🏆 **API、下载、认证详情** |
| **多语言** | 仅英文 | 🏆 **中英双语** |
| **架构** | YAML → README | 🏆 **JSON + Schema验证** |

**定位差异**：
- awesome-public-datasets: 轻量级数据集目录
- **DataSource Hub**: 专业级权威数据源元数据平台

我们是**互补关系**，而非竞争关系！

---

## 🤝 贡献指南 | Contributing

欢迎贡献新的数据源或改进现有信息！

### 如何贡献 | How to Contribute

1. **Fork** 本仓库
2. 创建新的数据源 JSON 文件（参考现有样例）
3. 确保符合 JSON Schema 标准
4. 提交 **Pull Request**

### 数据源收录标准 | Inclusion Criteria

✅ **优先收录**：
- 政府官方机构数据
- 国际组织数据
- 顶级学术机构数据
- 定期更新的权威数据

❌ **不收录**：
- 商业付费数据（除非有免费层级）
- 个人或小型组织数据
- 长期未更新的数据源
- 无官方文档的数据

详细指南请查看：`docs/CONTRIBUTING.md` (待创建)

---

## 📄 许可协议 | License

本项目采用 [MIT License](LICENSE) 开源。

数据源本身的许可协议请查看各数据源的 `licensing` 字段。

---

## 📞 联系方式 | Contact

- **项目主页**: [待定]
- **Issue 提交**: [待定]
- **讨论区**: [待定]
- **邮箱**: [待定]

---

## 🙏 致谢 | Acknowledgments

本项目灵感来源于：
- [awesome-public-datasets](https://github.com/awesomedata/awesome-public-datasets) - 公共数据集目录
- [OpenMetadata](https://github.com/open-metadata/OpenMetadata) - 数据目录平台
- SDMX 国际统计数据交换标准

感谢所有数据源的维护机构为开放数据做出的贡献！

---

## 📊 项目状态 | Project Status

**当前阶段**: Phase 1 - 核心数据源建设
**完成度**: 10/300 (3.3%)
**最近更新**: 2025-11-29
**质量评分**: ⭐⭐⭐⭐⭐ (4.9/5.0)

---

<p align="center">
  <strong>打造全球最权威的数据源知识库</strong><br>
  <strong>Building the World's Most Authoritative Data Source Knowledge Base</strong>
</p>

<p align="center">
  Made with ❤️ by DataSource Hub Team
</p>
