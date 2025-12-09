# DataSource Hub - 产品需求文档 (PRD)

**文档版本**: 1.0
**创建日期**: 2025-01-22
**项目类型**: 开源知识库项目
**项目状态**: 规划阶段

---

## 1. 项目概述

### 1.1 项目背景

在数据驱动决策的时代，研究人员、数据分析师、政策制定者和开发者经常面临以下挑战：

- **数据源分散**：权威数据散落在各个国际组织、政府机构、学术机构的网站上
- **发现困难**：缺乏统一的数据源导航和发现机制
- **质量参差**：难以评估数据源的权威性和可靠性
- **信息不完整**：缺少系统化的元数据信息（访问方式、覆盖范围、更新频率等）
- **标准不一**：不同数据源的描述格式和质量标准各异

### 1.2 项目愿景

打造**全球最全面、最权威、最结构化的开源数据源知识库**，成为数据工作者获取权威数据的第一站。

### 1.3 项目目标

#### 核心目标
1. **全面性**：收录200+个全球各领域、各地区的权威数据源
2. **权威性**：优先收录官方机构、国际组织、顶级学术机构的数据源
3. **结构化**：建立标准化的数据源元数据体系
4. **易用性**：提供多维度分类、索引和检索机制
5. **开放性**：完全开源，鼓励社区贡献和协作

#### 次要目标
- 建立数据源质量评估标准
- 提供数据源使用案例和代码示例
- 定期维护和更新数据源信息
- 形成数据源领域的最佳实践

### 1.4 目标用户群体

**主要用户**：
- **数据科学家/分析师**：需要高质量数据进行分析和建模
- **学术研究人员**：需要权威数据支持研究工作
- **政策制定者**：需要官方统计数据支持决策
- **软件开发者**：需要API数据源进行应用开发
- **记者/媒体从业者**：需要可靠数据源进行报道

**次要用户**：
- 学生和教育工作者
- 商业分析师
- 非政府组织工作人员
- 数据爱好者

### 1.5 核心价值主张

| 用户痛点 | DataSource Hub 解决方案 | 价值 |
|---------|----------------------|------|
| 不知道去哪里找权威数据 | 汇总全球权威数据源 | 节省搜索时间 |
| 不确定数据源是否可靠 | 提供权威性评级 | 降低数据风险 |
| 不了解数据覆盖范围 | 详细元数据信息 | 提高决策效率 |
| 不清楚如何访问数据 | 访问方式和API文档链接 | 降低使用门槛 |
| 数据源信息分散 | 统一的结构化知识库 | 一站式服务 |

---

## 2. 功能需求

### 2.1 核心功能

#### F1. 数据源元数据管理
**需求描述**：为每个数据源建立完整的元数据信息

**必需字段**：
- 基本信息（ID、名称、描述、维护机构）
- 访问信息（URL、API、下载方式、访问级别）
- 覆盖范围（地理、时间、领域、指标数量）
- **主要数据内容（可获得的核心数据类别和指标说明）**
- 数据特征（类型、粒度、格式、语言）
- 质量评估（权威性、透明度、及时性、完整性、文档质量）
- 许可协议（License、使用限制）
- 元数据标准（遵循的国际标准）
- 使用信息（应用场景、示例代码）
- 关联数据源（相关/互补的其他数据源）
- 联系方式（支持邮箱、帮助文档）
- 目录元数据（添加日期、更新日期、贡献者、状态）
- 标签（便于检索）

**可选字段**：
- 示例研究论文
- 可视化示例
- 常见问题
- 变更日志

#### F2. 多维度分类体系
**需求描述**：建立科学的分类taxonomy，支持多维度浏览

**分类维度**：
1. **按领域分类**
   - 一级分类：经济金融、健康医疗、环境气候、社会发展、科技创新、教育文化、农业食品、能源资源、交通物流、公共安全
   - 二级分类：每个一级分类下细分3-8个子类别

2. **按地区分类**
   - 全球性数据源
   - 区域性（七大洲）
   - 国家级（重点：G20国家）
   - 省市级（可选）

3. **按机构类型分类**
   - 国际组织（联合国系统、区域组织）
   - 国家政府（统计局、央行、部委）
   - 学术机构（大学、研究中心）
   - 行业协会
   - 商业机构

4. **按数据类型分类**
   - 统计数据（结构化表格）
   - 时间序列数据
   - 空间地理数据
   - 文本语料
   - 图像/视频
   - API服务

5. **按访问方式分类**
   - 完全开放
   - 需注册免费
   - 学术许可
   - 商业付费
   - 申请审批

6. **按更新频率分类**
   - 实时
   - 日/周
   - 月/季
   - 年度
   - 一次性

#### F3. 权威性评级系统
**需求描述**：建立客观的5星评级体系

**评估维度**（每项1-5星）：

1. **来源权威性** (Source Authority)
   - 5星：联合国机构、G7国家官方统计机构
   - 4星：其他国家官方机构、OECD、顶级学术机构
   - 3星：知名研究机构、行业权威协会
   - 2星：地方政府、专业咨询公司
   - 1星：企业数据、众包数据

2. **方法论透明度** (Methodology Transparency)
   - 5星：完整方法论文档、数据可复现、开源
   - 4星：详细方法说明、数据字典完整
   - 3星：基本方法描述、有样本说明
   - 2星：简要说明、缺少细节
   - 1星：无方法论文档

3. **更新及时性** (Timeliness)
   - 5星：实时或日更新
   - 4星：周更新或月更新
   - 3星：季度更新
   - 2星：年度更新
   - 1星：不定期更新或已停止更新

4. **数据完整性** (Completeness)
   - 5星：覆盖全面、缺失值<5%、长时间序列
   - 4星：覆盖较全、缺失值5-10%
   - 3星：覆盖中等、缺失值10-20%
   - 2星：覆盖有限、缺失值20-50%
   - 1星：覆盖稀疏、缺失值>50%

5. **文档质量** (Documentation Quality)
   - 5星：完整数据字典、用户指南、API文档、教程
   - 4星：数据字典、基本指南、FAQ
   - 3星：基本说明文档
   - 2星：简要说明
   - 1星：无文档或仅有标题

**综合评分**：6个维度的算术平均值（保留1位小数）

**展示方式**：
- 总分：★★★★☆ (4.2/5.0)
- 各维度得分明细

#### F4. 索引和检索机制
**需求描述**：提供多种方式快速找到需要的数据源

**索引文件**：
1. `all-sources.json` - 所有数据源的完整列表
2. `by-domain.json` - 按领域分组索引
3. `by-region.json` - 按地区分组索引
4. `by-authority.json` - 按权威性评级分组
5. `by-type.json` - 按数据类型分组
6. `by-access.json` - 按访问方式分组
7. `statistics.json` - 统计信息（总数、分布、更新日志）

**检索支持**：
- 全文搜索（通过标签、名称、描述）
- 多条件筛选（领域+地区+访问方式）
- 排序（按权威性、更新时间、字母顺序）

#### F5. 数据验证和质量控制
**需求描述**：确保数据源元数据的准确性和一致性

**验证规则**：
1. **格式验证**
   - 符合JSON Schema标准
   - 必填字段完整
   - 字段类型正确

2. **内容验证**
   - URL格式有效
   - 评分范围（1-5）
   - 日期格式正确（YYYY-MM-DD）
   - 语言代码符合ISO 639-1标准
   - 国家代码符合ISO 3166-1标准

3. **逻辑验证**
   - 时间范围合理（start_year ≤ end_year ≤ 当前年份）
   - 分类ID存在于taxonomy中
   - 相关数据源ID有效

4. **链接验证**
   - 定期检查URL可访问性
   - 标记失效链接
   - 建议更新或移除

**自动化工具**：
- `validate.py` - 元数据验证脚本
- `check-urls.py` - 链接健康检查
- GitHub Actions - CI/CD自动验证

---

## 3. 数据架构

### 3.1 数据源元数据标准 (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://datasourcehub.org/schemas/datasource-v1.json",
  "title": "DataSource Metadata Schema",
  "description": "Standard schema for describing authoritative data sources",
  "type": "object",
  "required": [
    "id",
    "name",
    "organization",
    "description",
    "access",
    "coverage",
    "data_characteristics",
    "quality",
    "licensing"
  ],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier (lowercase, hyphen-separated)",
      "pattern": "^[a-z0-9-]+$"
    },
    "name": {
      "type": "object",
      "required": ["en"],
      "properties": {
        "en": {"type": "string"},
        "zh": {"type": "string"},
        "native": {"type": "string"}
      }
    },
    "organization": {
      "type": "object",
      "required": ["name", "type"],
      "properties": {
        "name": {"type": "string"},
        "type": {
          "type": "string",
          "enum": [
            "international_organization",
            "national_government",
            "research_institution",
            "industry_association",
            "commercial"
          ]
        },
        "country": {"type": ["string", "null"]},
        "website": {"type": "string", "format": "uri"}
      }
    },
    "description": {
      "type": "object",
      "required": ["en"],
      "properties": {
        "en": {"type": "string"},
        "zh": {"type": "string"}
      }
    },
    "access": {
      "type": "object",
      "required": ["primary_url", "access_level"],
      "properties": {
        "primary_url": {"type": "string", "format": "uri"},
        "api": {
          "type": "object",
          "properties": {
            "available": {"type": "boolean"},
            "documentation": {"type": "string", "format": "uri"},
            "version": {"type": "string"},
            "authentication": {"type": "boolean"}
          }
        },
        "download": {
          "type": "object",
          "properties": {
            "available": {"type": "boolean"},
            "formats": {
              "type": "array",
              "items": {"type": "string"}
            }
          }
        },
        "access_level": {
          "type": "string",
          "enum": ["open", "registration", "academic", "commercial", "restricted"]
        },
        "registration_required": {"type": "boolean"}
      }
    },
    "coverage": {
      "type": "object",
      "required": ["geographic", "temporal", "domains"],
      "properties": {
        "geographic": {
          "type": "object",
          "properties": {
            "scope": {
              "type": "string",
              "enum": ["global", "regional", "national", "subnational"]
            },
            "countries": {"type": ["integer", "array"]},
            "regions": {"type": "array", "items": {"type": "string"}}
          }
        },
        "temporal": {
          "type": "object",
          "properties": {
            "start_year": {"type": "integer", "minimum": 1800},
            "end_year": {"type": "integer"},
            "update_frequency": {
              "type": "string",
              "enum": ["real-time", "daily", "weekly", "monthly", "quarterly", "annual", "irregular", "one-time"]
            }
          }
        },
        "domains": {
          "type": "array",
          "items": {"type": "string"},
          "minItems": 1
        },
        "indicators": {"type": "integer", "minimum": 0}
      }
    },
    "data_content": {
      "type": "object",
      "description": "Description of main data categories and indicators available from this source",
      "properties": {
        "en": {
          "type": "array",
          "description": "List of main data categories in English",
          "items": {"type": "string"}
        },
        "zh": {
          "type": "array",
          "description": "List of main data categories in Chinese",
          "items": {"type": "string"}
        }
      }
    },
    "data_characteristics": {
      "type": "object",
      "required": ["types", "granularity", "formats"],
      "properties": {
        "types": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["statistical", "time-series", "cross-sectional", "panel", "geospatial", "text", "image", "api"]
          }
        },
        "granularity": {
          "type": "array",
          "items": {"type": "string"}
        },
        "formats": {
          "type": "array",
          "items": {"type": "string"}
        },
        "languages": {
          "type": "array",
          "items": {"type": "string", "pattern": "^[a-z]{2}$"}
        }
      }
    },
    "quality": {
      "type": "object",
      "required": [
        "authority_level",
        "methodology_transparency",
        "update_timeliness",
        "data_completeness",
        "documentation_quality"
      ],
      "properties": {
        "authority_level": {"type": "integer", "minimum": 1, "maximum": 5},
        "methodology_transparency": {"type": "integer", "minimum": 1, "maximum": 5},
        "update_timeliness": {"type": "integer", "minimum": 1, "maximum": 5},
        "data_completeness": {"type": "integer", "minimum": 1, "maximum": 5},
        "documentation_quality": {"type": "integer", "minimum": 1, "maximum": 5},
        "citation_count": {
          "type": "string",
          "enum": ["very_high", "high", "medium", "low", "unknown"]
        }
      }
    },
    "licensing": {
      "type": "object",
      "required": ["license"],
      "properties": {
        "license": {"type": "string"},
        "commercial_use": {"type": "boolean"},
        "attribution_required": {"type": "boolean"},
        "restrictions": {"type": "array", "items": {"type": "string"}}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "standards_followed": {"type": "array", "items": {"type": "string"}},
        "data_dictionary": {"type": "boolean"},
        "methodology_docs": {"type": "boolean"},
        "user_guide": {"type": "boolean"}
      }
    },
    "usage": {
      "type": "object",
      "properties": {
        "use_cases": {"type": "array", "items": {"type": "string"}},
        "example_studies": {"type": "array", "items": {"type": "string"}},
        "code_examples": {"type": "array", "items": {"type": "string"}}
      }
    },
    "related_sources": {
      "type": "array",
      "items": {"type": "string"}
    },
    "contact": {
      "type": "object",
      "properties": {
        "email": {"type": "string", "format": "email"},
        "support_url": {"type": "string", "format": "uri"}
      }
    },
    "catalog_metadata": {
      "type": "object",
      "required": ["added_date", "last_updated", "status"],
      "properties": {
        "added_date": {"type": "string", "format": "date"},
        "last_updated": {"type": "string", "format": "date"},
        "verified_date": {"type": "string", "format": "date"},
        "contributor": {"type": "string"},
        "status": {
          "type": "string",
          "enum": ["active", "inactive", "deprecated", "under_review"]
        }
      }
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 1
    }
  }
}
```

### 3.2 目录结构设计

```
datasource/
├── sources/                      # 数据源元数据（核心资产）
│   ├── international/           # 国际组织
│   │   ├── economics/          # 经济金融类
│   │   │   ├── worldbank.json              # 世界银行开放数据
│   │   │   ├── imf.json                    # 国际货币基金组织
│   │   │   ├── oecd.json                   # 经合组织统计
│   │   │   ├── wto.json                    # 世界贸易组织
│   │   │   ├── bis.json                    # 国际清算银行
│   │   │   ├── adb.json                    # 亚洲开发银行
│   │   │   ├── afdb.json                   # 非洲开发银行
│   │   │   ├── iadb.json                   # 美洲开发银行
│   │   │   ├── ebrd.json                   # 欧洲复兴开发银行
│   │   │   ├── unctad.json                 # 联合国贸发会议
│   │   │   ├── un-comtrade.json            # 联合国商品贸易数据库
│   │   │   └── paris-club.json             # 巴黎俱乐部
│   │   ├── health/             # 健康医疗类
│   │   │   ├── who.json                    # 世界卫生组织
│   │   │   ├── unicef.json                 # 联合国儿童基金会
│   │   │   ├── gbd.json                    # 全球疾病负担研究
│   │   │   ├── unaids.json                 # 联合国艾滋病规划署
│   │   │   ├── gavi.json                   # 全球疫苗免疫联盟
│   │   │   ├── global-fund.json            # 全球基金
│   │   │   ├── paho.json                   # 泛美卫生组织
│   │   │   ├── ecdc.json                   # 欧洲疾控中心
│   │   │   └── wpro.json                   # WHO西太平洋区域办公室
│   │   ├── environment/        # 环境气候类
│   │   │   ├── unep.json                   # 联合国环境署
│   │   │   ├── ipcc.json                   # 政府间气候变化专门委员会
│   │   │   ├── wmo.json                    # 世界气象组织
│   │   │   ├── unfccc.json                 # 联合国气候变化框架公约
│   │   │   ├── iucn.json                   # 世界自然保护联盟
│   │   │   ├── unep-wcmc.json              # 世界保护监测中心
│   │   │   ├── cbd.json                    # 生物多样性公约
│   │   │   ├── cites.json                  # 濒危野生动植物种国际贸易公约
│   │   │   ├── ramsar.json                 # 湿地公约
│   │   │   ├── undrr.json                  # 联合国减少灾害风险办公室
│   │   │   └── imo.json                    # 国际海事组织（海洋数据）
│   │   ├── social/             # 社会发展类
│   │   │   ├── undp.json                   # 联合国开发计划署
│   │   │   ├── ilo.json                    # 国际劳工组织
│   │   │   ├── unesco.json                 # 联合国教科文组织
│   │   │   ├── unhcr.json                  # 联合国难民署
│   │   │   ├── iom.json                    # 国际移民组织
│   │   │   ├── un-women.json               # 联合国妇女署
│   │   │   ├── unhabitat.json              # 联合国人居署
│   │   │   ├── unodc.json                  # 联合国毒品和犯罪问题办公室
│   │   │   ├── ohchr.json                  # 联合国人权高专办
│   │   │   └── unicef-mics.json            # UNICEF多指标类集调查
│   │   ├── agriculture/        # 农业与食品
│   │   │   ├── fao.json                    # 联合国粮农组织
│   │   │   ├── ifad.json                   # 国际农业发展基金
│   │   │   ├── wfp.json                    # 世界粮食计划署
│   │   │   ├── cgiar.json                  # 国际农业研究磋商组织
│   │   │   ├── ifpri.json                  # 国际食物政策研究所
│   │   │   └── worldfish.json              # 世界渔业中心
│   │   ├── energy/             # 能源资源
│   │   │   ├── iea.json                    # 国际能源署
│   │   │   ├── irena.json                  # 国际可再生能源署
│   │   │   ├── iaea.json                   # 国际原子能机构
│   │   │   ├── opec.json                   # 石油输出国组织
│   │   │   └── ief.json                    # 国际能源论坛
│   │   ├── statistics/         # 统计与人口
│   │   │   ├── unsd.json                   # 联合国统计司
│   │   │   ├── unpopulation.json           # 联合国人口司
│   │   │   ├── unsd-sdg.json               # 联合国SDG数据库
│   │   │   ├── unescap.json                # 联合国亚太经社会
│   │   │   ├── uneca.json                  # 联合国非洲经委会
│   │   │   ├── unece.json                  # 联合国欧洲经委会
│   │   │   ├── eclac.json                  # 联合国拉美加勒比经委会
│   │   │   └── unescwa.json                # 联合国西亚经社会
│   │   ├── transport/          # 交通运输
│   │   │   ├── icao.json                   # 国际民航组织
│   │   │   ├── imo-stats.json              # 国际海事组织
│   │   │   ├── iru.json                    # 国际道路运输联盟
│   │   │   └── uic.json                    # 国际铁路联盟
│   │   ├── technology/         # 科技与创新
│   │   │   ├── wipo.json                   # 世界知识产权组织
│   │   │   ├── itu.json                    # 国际电信联盟
│   │   │   ├── unesco-uis-rd.json          # UNESCO科研统计
│   │   │   └── cern-opendata.json          # 欧洲核子研究中心
│   │   ├── finance/            # 金融市场
│   │   │   ├── bis-stats.json              # 国际清算银行统计
│   │   │   ├── world-federation-exchanges.json  # 世界交易所联合会
│   │   │   ├── iosco.json                  # 国际证监会组织
│   │   │   └── fsb.json                    # 金融稳定委员会
│   │   ├── standards/          # 标准与计量
│   │   │   ├── iso.json                    # 国际标准化组织
│   │   │   ├── bipm.json                   # 国际计量局
│   │   │   └── codex.json                  # 国际食品法典委员会
│   │   ├── regional/           # 区域性组织
│   │   │   ├── eu/                         # 欧盟
│   │   │   │   ├── eurostat.json
│   │   │   │   ├── ecb.json
│   │   │   │   ├── eea.json                # 欧洲环境署
│   │   │   │   ├── efsa.json               # 欧洲食品安全局
│   │   │   │   └── ema.json                # 欧洲药品管理局
│   │   │   ├── asean/                      # 东盟
│   │   │   │   ├── asean-stats.json
│   │   │   │   └── asean-biodiversity.json
│   │   │   ├── au/                         # 非盟
│   │   │   │   └── au-statistics.json
│   │   │   ├── mercosur/                   # 南方共同市场
│   │   │   │   └── mercosur-stats.json
│   │   │   ├── gcc/                        # 海湾合作委员会
│   │   │   │   └── gcc-stat.json
│   │   │   ├── apec/                       # 亚太经合组织
│   │   │   │   └── apec-stats.json
│   │   │   └── oecd-regional/              # OECD区域数据
│   │   │       └── oecd-territorial.json
│   │   └── specialized/        # 专门机构
│   │       ├── transparency/               # 透明度与治理
│   │       │   ├── transparency-international.json  # 国际透明组织
│   │       │   ├── world-justice-project.json      # 世界正义工程
│   │       │   └── freedom-house.json              # 自由之家
│   │       ├── humanitarian/               # 人道主义
│   │       │   ├── unocha.json             # 联合国人道协调厅
│   │       │   ├── icrc.json               # 国际红十字委员会
│   │       │   └── fts.json                # 金融追踪服务
│   │       ├── security/                   # 安全与和平
│   │       │   ├── sipri.json              # 斯德哥尔摩国际和平研究所
│   │       │   ├── unidir.json             # 联合国裁军研究所
│   │       │   └── iiss.json               # 国际战略研究所
│   │       └── maritime/                   # 海洋事务
│   │           ├── imo-gisis.json          # 国际海事组织信息系统
│   │           └── ioc-unesco.json         # UNESCO政府间海洋学委员会
│   │
│   ├── countries/              # 各国官方数据源
│   │   ├── north_america/     # 北美洲
│   │   │   ├── usa/           # 美国
│   │   │   │   ├── census.json                 # 人口普查局
│   │   │   │   ├── bls.json                    # 劳工统计局
│   │   │   │   ├── bea.json                    # 经济分析局
│   │   │   │   ├── fred.json                   # 联邦储备经济数据
│   │   │   │   ├── datagov.json                # 政府开放数据
│   │   │   │   ├── cdc.json                    # 疾病控制中心
│   │   │   │   ├── eia.json                    # 能源信息署
│   │   │   │   ├── usda-nass.json              # 农业统计局
│   │   │   │   ├── noaa.json                   # 国家海洋大气局
│   │   │   │   ├── nasa.json                   # 航空航天局数据
│   │   │   │   ├── nces.json                   # 教育统计中心
│   │   │   │   ├── usgs.json                   # 地质调查局
│   │   │   │   ├── epa.json                    # 环保署
│   │   │   │   ├── sec.json                    # 证券交易委员会
│   │   │   │   └── uspto.json                  # 专利商标局
│   │   │   ├── canada/        # 加拿大
│   │   │   │   ├── statcan.json                # 加拿大统计局
│   │   │   │   ├── boc.json                    # 加拿大银行
│   │   │   │   ├── open-canada.json            # 加拿大开放数据
│   │   │   │   ├── cihi.json                   # 加拿大健康信息研究所
│   │   │   │   ├── nrcan.json                  # 自然资源部
│   │   │   │   └── ic.json                     # 创新科技部
│   │   │   └── mexico/        # 墨西哥
│   │   │       ├── inegi.json                  # 国家统计地理信息局
│   │   │       ├── banxico.json                # 墨西哥银行
│   │   │       └── datos-gob-mx.json           # 政府开放数据
│   │   │
│   │   ├── europe/            # 欧洲
│   │   │   ├── eu/            # 欧盟（已在regional部分）
│   │   │   │   ├── eurostat.json
│   │   │   │   └── ecb.json
│   │   │   ├── uk/            # 英国
│   │   │   │   ├── ons.json                    # 国家统计局
│   │   │   │   ├── datagov-uk.json             # 政府开放数据
│   │   │   │   ├── boe.json                    # 英格兰银行
│   │   │   │   ├── fca.json                    # 金融行为监管局
│   │   │   │   ├── nhs-digital.json            # NHS数字化服务
│   │   │   │   └── ukri.json                   # 英国研究创新署
│   │   │   ├── germany/       # 德国
│   │   │   │   ├── destatis.json               # 联邦统计局
│   │   │   │   ├── bundesbank.json             # 德国央行
│   │   │   │   ├── govdata.json                # 政府数据门户
│   │   │   │   ├── dwd.json                    # 气象局
│   │   │   │   └── rki.json                    # 罗伯特科赫研究所
│   │   │   ├── france/        # 法国
│   │   │   │   ├── insee.json                  # 国家统计局
│   │   │   │   ├── banque-france.json          # 法国银行
│   │   │   │   ├── datagouv-fr.json            # 政府开放数据
│   │   │   │   ├── sante-publique.json         # 公共卫生局
│   │   │   │   └── meteo-france.json           # 法国气象局
│   │   │   ├── italy/         # 意大利
│   │   │   │   ├── istat.json                  # 国家统计局
│   │   │   │   ├── banca-italia.json           # 意大利银行
│   │   │   │   └── dati-gov-it.json            # 政府开放数据
│   │   │   ├── spain/         # 西班牙
│   │   │   │   ├── ine.json                    # 国家统计局
│   │   │   │   ├── bde.json                    # 西班牙银行
│   │   │   │   └── datos-gob-es.json           # 政府开放数据
│   │   │   ├── netherlands/   # 荷兰
│   │   │   │   ├── cbs.json                    # 中央统计局
│   │   │   │   ├── dnb.json                    # 荷兰银行
│   │   │   │   └── dataoverheid.json           # 政府开放数据
│   │   │   ├── sweden/        # 瑞典
│   │   │   │   ├── scb.json                    # 统计局
│   │   │   │   ├── riksbank.json               # 瑞典央行
│   │   │   │   └── oppnadata.json              # 开放数据门户
│   │   │   ├── switzerland/   # 瑞士
│   │   │   │   ├── bfs.json                    # 联邦统计局
│   │   │   │   ├── snb.json                    # 瑞士国家银行
│   │   │   │   └── opendata-swiss.json         # 开放数据
│   │   │   ├── norway/        # 挪威
│   │   │   │   ├── ssb.json                    # 统计局
│   │   │   │   └── norges-bank.json            # 挪威银行
│   │   │   ├── denmark/       # 丹麦
│   │   │   │   ├── dst.json                    # 统计局
│   │   │   │   └── nationalbanken.json         # 丹麦国家银行
│   │   │   ├── finland/       # 芬兰
│   │   │   │   ├── stat-fi.json                # 统计局
│   │   │   │   └── bof.json                    # 芬兰银行
│   │   │   ├── poland/        # 波兰
│   │   │   │   ├── gus.json                    # 中央统计局
│   │   │   │   └── nbp.json                    # 波兰国家银行
│   │   │   ├── russia/        # 俄罗斯
│   │   │   │   ├── rosstat.json                # 联邦统计局
│   │   │   │   └── cbr.json                    # 俄罗斯央行
│   │   │   └── turkey/        # 土耳其
│   │   │       ├── turkstat.json               # 统计局
│   │   │       └── tcmb.json                   # 土耳其央行
│   │   │
│   │   ├── asia/              # 亚洲
│   │   │   ├── east_asia/     # 东亚
│   │   │   │   ├── china/     # 中国
│   │   │   │   │   ├── nbs.json                # 国家统计局
│   │   │   │   │   ├── pbc.json                # 人民银行
│   │   │   │   │   ├── customs.json            # 海关总署
│   │   │   │   │   ├── mofcom.json             # 商务部
│   │   │   │   │   ├── mof.json                # 财政部
│   │   │   │   │   ├── ndrc.json               # 发改委
│   │   │   │   │   ├── miit.json               # 工信部
│   │   │   │   │   ├── nhc.json                # 卫健委
│   │   │   │   │   ├── mee.json                # 生态环境部
│   │   │   │   │   ├── moa.json                # 农业农村部
│   │   │   │   │   ├── cnipa.json              # 知识产权局
│   │   │   │   │   ├── cma.json                # 气象局
│   │   │   │   │   └── csrc.json               # 证监会
│   │   │   │   ├── japan/     # 日本
│   │   │   │   │   ├── stat.json               # 统计局
│   │   │   │   │   ├── boj.json                # 日本银行
│   │   │   │   │   ├── e-stat.json             # 政府统计门户
│   │   │   │   │   ├── mof.json                # 财务省
│   │   │   │   │   ├── meti.json               # 经济产业省
│   │   │   │   │   ├── mhlw.json               # 厚生劳动省
│   │   │   │   │   ├── mext.json               # 文部科学省
│   │   │   │   │   └── jma.json                # 气象厅
│   │   │   │   └── south_korea/ # 韩国
│   │   │   │       ├── kostat.json             # 统计厅
│   │   │   │       ├── bok.json                # 韩国银行
│   │   │   │       ├── data-go-kr.json         # 政府公共数据
│   │   │   │       ├── kipo.json               # 知识产权局
│   │   │   │       └── kdca.json               # 疾病管理厅
│   │   │   ├── southeast_asia/ # 东南亚
│   │   │   │   ├── singapore/ # 新加坡
│   │   │   │   │   ├── singstat.json           # 统计局
│   │   │   │   │   ├── mas.json                # 金融管理局
│   │   │   │   │   └── datagov-sg.json         # 政府开放数据
│   │   │   │   ├── malaysia/  # 马来西亚
│   │   │   │   │   ├── dosm.json               # 统计局
│   │   │   │   │   └── bnm.json                # 马来西亚国家银行
│   │   │   │   ├── thailand/  # 泰国
│   │   │   │   │   ├── nso.json                # 国家统计局
│   │   │   │   │   └── bot.json                # 泰国银行
│   │   │   │   ├── indonesia/ # 印度尼西亚
│   │   │   │   │   ├── bps.json                # 中央统计局
│   │   │   │   │   └── bi.json                 # 印尼银行
│   │   │   │   ├── philippines/ # 菲律宾
│   │   │   │   │   ├── psa.json                # 统计署
│   │   │   │   │   └── bsp.json                # 菲律宾央行
│   │   │   │   └── vietnam/   # 越南
│   │   │   │       ├── gso.json                # 统计总局
│   │   │   │       └── sbv.json                # 越南国家银行
│   │   │   ├── south_asia/    # 南亚
│   │   │   │   ├── india/     # 印度
│   │   │   │   │   ├── mospi.json              # 统计部
│   │   │   │   │   ├── rbi.json                # 印度储备银行
│   │   │   │   │   ├── datagov-in.json         # 政府开放数据
│   │   │   │   │   ├── niti-aayog.json         # 国家转型委员会
│   │   │   │   │   └── dgci.json               # 商业情报总局
│   │   │   │   ├── pakistan/  # 巴基斯坦
│   │   │   │   │   ├── pbs.json                # 统计局
│   │   │   │   │   └── sbp.json                # 巴基斯坦国家银行
│   │   │   │   └── bangladesh/ # 孟加拉国
│   │   │   │       ├── bbs.json                # 统计局
│   │   │   │       └── bb.json                 # 孟加拉国银行
│   │   │   └── middle_east/   # 中东
│   │   │       ├── israel/    # 以色列
│   │   │   │       ├── cbs-israel.json         # 中央统计局
│   │   │   │       └── boi.json                # 以色列银行
│   │   │       ├── saudi_arabia/ # 沙特阿拉伯
│   │   │   │       ├── gastat.json             # 统计总局
│   │   │   │       └── sama.json               # 沙特央行
│   │   │       └── uae/       # 阿联酋
│   │   │           ├── fcsa.json               # 联邦统计局
│   │   │           └── cbuae.json              # 阿联酋央行
│   │   │
│   │   ├── oceania/           # 大洋洲
│   │   │   ├── australia/     # 澳大利亚
│   │   │   │   ├── abs.json                    # 统计局
│   │   │   │   ├── rba.json                    # 澳大利亚储备银行
│   │   │   │   ├── datagov-au.json             # 政府开放数据
│   │   │   │   ├── aihw.json                   # 健康福利研究所
│   │   │   │   ├── bom.json                    # 气象局
│   │   │   │   └── geoscience-au.json          # 地球科学局
│   │   │   └── new_zealand/   # 新西兰
│   │   │       ├── stats-nz.json               # 统计局
│   │   │       ├── rbnz.json                   # 新西兰储备银行
│   │   │       └── data-govt-nz.json           # 政府数据门户
│   │   │
│   │   ├── south_america/     # 南美洲
│   │   │   ├── brazil/        # 巴西
│   │   │   │   ├── ibge.json                   # 地理统计局
│   │   │   │   ├── bcb.json                    # 巴西央行
│   │   │   │   └── dados-gov-br.json           # 政府开放数据
│   │   │   ├── argentina/     # 阿根廷
│   │   │   │   ├── indec.json                  # 统计普查局
│   │   │   │   └── bcra.json                   # 阿根廷央行
│   │   │   ├── chile/         # 智利
│   │   │   │   ├── ine-chile.json              # 国家统计局
│   │   │   │   └── bcentral-chile.json         # 智利央行
│   │   │   └── colombia/      # 哥伦比亚
│   │   │       ├── dane.json                   # 国家统计局
│   │   │       └── banrep.json                 # 哥伦比亚央行
│   │   │
│   │   └── africa/            # 非洲
│   │       ├── south_africa/  # 南非
│   │       │   ├── statssa.json                # 统计局
│   │       │   └── resbank.json                # 南非储备银行
│   │       ├── nigeria/       # 尼日利亚
│   │       │   ├── nbs-nigeria.json            # 国家统计局
│   │       │   └── cbn.json                    # 尼日利亚央行
│   │       ├── egypt/         # 埃及
│   │       │   ├── capmas.json                 # 统计局
│   │       │   └── cbe.json                    # 埃及央行
│   │       └── kenya/         # 肯尼亚
│   │           ├── knbs.json                   # 国家统计局
│   │           └── centralbank-kenya.json      # 肯尼亚央行
│   │
│   ├── china/                 # 中国数据源专区（深度覆盖）
│   │   ├── national/          # 国家级综合统计
│   │   │   ├── nbs.json                        # 国家统计局
│   │   │   ├── nbs-data.json                   # 国家数据网
│   │   │   ├── stats-annual.json               # 中国统计年鉴
│   │   │   ├── stats-abstract.json             # 统计摘要
│   │   │   ├── monthly-stats.json              # 月度统计数据
│   │   │   └── regional-stats.json             # 区域统计数据
│   │   ├── finance/           # 金融财政
│   │   │   ├── banking/                        # 银行系统
│   │   │   │   ├── pbc.json                    # 中国人民银行
│   │   │   │   ├── pbc-stats.json              # 人民银行统计数据
│   │   │   │   ├── cbirc.json                  # 银保监会
│   │   │   │   ├── deposit-insurance.json      # 存款保险基金
│   │   │   │   └── banking-industry.json       # 银行业协会
│   │   │   ├── securities/                     # 证券市场
│   │   │   │   ├── csrc.json                   # 证监会
│   │   │   │   ├── sse.json                    # 上海证券交易所
│   │   │   │   ├── szse.json                   # 深圳证券交易所
│   │   │   │   ├── bse.json                    # 北京证券交易所
│   │   │   │   ├── neeq.json                   # 全国股转系统(新三板)
│   │   │   │   ├── csdc.json                   # 中国结算
│   │   │   │   └── sac.json                    # 证券业协会
│   │   │   ├── bonds/                          # 债券市场
│   │   │   │   ├── chinabond.json              # 中国债券信息网
│   │   │   │   ├── shclearhouse.json           # 上海清算所
│   │   │   │   └── treasury-bonds.json         # 国债发行数据
│   │   │   ├── insurance/                      # 保险行业
│   │   │   │   ├── insurance-stats.json        # 保险业统计
│   │   │   │   └── iia.json                    # 保险业协会
│   │   │   ├── funds/                          # 基金行业
│   │   │   │   ├── amac.json                   # 基金业协会
│   │   │   │   ├── mutual-funds.json           # 公募基金数据
│   │   │   │   └── pe-funds.json               # 私募基金数据
│   │   │   ├── fiscal/                         # 财政税收
│   │   │   │   ├── mof.json                    # 财政部
│   │   │   │   ├── fiscal-revenue.json         # 财政收入数据
│   │   │   │   ├── fiscal-expenditure.json     # 财政支出数据
│   │   │   │   ├── local-gov-debt.json         # 地方政府债务
│   │   │   │   └── budget-reports.json         # 预算报告
│   │   │   └── forex/                          # 外汇管理
│   │   │       ├── safe.json                   # 国家外汇管理局
│   │   │       ├── forex-reserves.json         # 外汇储备数据
│   │   │       ├── bop.json                    # 国际收支平衡表
│   │   │       └── cross-border-rmb.json       # 跨境人民币业务
│   │   ├── economy/           # 经济贸易
│   │   │   ├── macro/                          # 宏观经济
│   │   │   │   ├── ndrc.json                   # 国家发展改革委
│   │   │   │   ├── ndrc-price.json             # 价格监测数据
│   │   │   │   ├── gdp-data.json               # GDP核算数据
│   │   │   │   ├── cpi-ppi.json                # CPI/PPI数据
│   │   │   │   └── pmi.json                    # 采购经理人指数
│   │   │   ├── trade/                          # 对外贸易
│   │   │   │   ├── mofcom.json                 # 商务部
│   │   │   │   ├── mofcom-fdi.json             # 外商投资数据
│   │   │   │   ├── mofcom-odi.json             # 对外投资数据
│   │   │   │   ├── customs.json                # 海关总署
│   │   │   │   ├── customs-stats.json          # 海关统计数据
│   │   │   │   ├── import-export.json          # 进出口商品数据
│   │   │   │   └── trade-countries.json        # 分国别贸易数据
│   │   │   ├── industry/                       # 工业制造
│   │   │   │   ├── miit.json                   # 工业和信息化部
│   │   │   │   ├── industrial-output.json      # 工业增加值
│   │   │   │   ├── manufacturing.json          # 制造业数据
│   │   │   │   ├── sme-data.json               # 中小企业数据
│   │   │   │   └── enterprise-stats.json       # 规上企业统计
│   │   │   ├── market/                         # 市场监管
│   │   │   │   ├── samr.json                   # 市场监管总局
│   │   │   │   ├── business-registration.json  # 企业注册数据
│   │   │   │   ├── consumer-protection.json    # 消费者权益
│   │   │   │   └── quality-supervision.json    # 质量监督数据
│   │   │   ├── soe/                            # 国有企业
│   │   │   │   ├── sasac.json                  # 国资委
│   │   │   │   ├── central-soe.json            # 中央企业数据
│   │   │   │   └── local-soe.json              # 地方国企数据
│   │   │   └── consumption/                    # 消费市场
│   │   │       ├── retail-sales.json           # 社会消费品零售
│   │   │       ├── ecommerce.json              # 电子商务数据
│   │   │       └── logistics-index.json        # 物流景气指数
│   │   ├── agriculture/       # 农业农村
│   │   │   ├── crop/                           # 种植业
│   │   │   │   ├── moa.json                    # 农业农村部
│   │   │   │   ├── moa-stats.json              # 农业统计数据
│   │   │   │   ├── grain-production.json       # 粮食产量数据
│   │   │   │   ├── vegetable-stats.json        # 蔬菜统计
│   │   │   │   ├── cotton-data.json            # 棉花数据
│   │   │   │   └── agricultural-prices.json    # 农产品价格
│   │   │   ├── livestock/                      # 畜牧业
│   │   │   │   ├── livestock-stats.json        # 畜牧业统计
│   │   │   │   ├── pork-data.json              # 生猪数据
│   │   │   │   ├── dairy-stats.json            # 乳制品统计
│   │   │   │   └── poultry-data.json           # 家禽数据
│   │   │   ├── forestry/                       # 林业
│   │   │   │   ├── forestry.json               # 国家林草局
│   │   │   │   ├── forest-resources.json       # 森林资源数据
│   │   │   │   └── ecological-protection.json  # 生态保护数据
│   │   │   ├── fishery/                        # 渔业
│   │   │   │   ├── fishery.json                # 渔业渔政局
│   │   │   │   ├── aquatic-production.json     # 水产品产量
│   │   │   │   └── fishing-stats.json          # 捕捞统计
│   │   │   └── rural/                          # 农村发展
│   │   │       ├── rural-economy.json          # 农村经济数据
│   │   │       ├── farmer-income.json          # 农民收入
│   │   │       └── poverty-alleviation.json    # 脱贫攻坚数据
│   │   ├── resources/         # 自然资源
│   │   │   ├── land/                           # 土地资源
│   │   │   │   ├── mnr.json                    # 自然资源部
│   │   │   │   ├── land-use.json               # 土地利用数据
│   │   │   │   ├── land-transaction.json       # 土地出让数据
│   │   │   │   └── cadastral-survey.json       # 地籍调查
│   │   │   ├── mineral/                        # 矿产资源
│   │   │   │   ├── mineral-resources.json      # 矿产资源统计
│   │   │   │   ├── mining-production.json      # 矿业生产数据
│   │   │   │   └── rare-earth.json             # 稀土数据
│   │   │   ├── energy/                         # 能源资源
│   │   │   │   ├── nea.json                    # 国家能源局
│   │   │   │   ├── energy-production.json      # 能源生产数据
│   │   │   │   ├── energy-consumption.json     # 能源消费数据
│   │   │   │   ├── electricity-stats.json      # 电力统计
│   │   │   │   ├── coal-stats.json             # 煤炭统计
│   │   │   │   ├── oil-gas.json                # 石油天然气
│   │   │   │   └── renewable-energy.json       # 可再生能源
│   │   │   ├── water/                          # 水资源
│   │   │   │   ├── mwr.json                    # 水利部
│   │   │   │   ├── water-resources.json        # 水资源公报
│   │   │   │   ├── water-conservancy.json      # 水利建设数据
│   │   │   │   └── flood-drought.json          # 洪旱灾害统计
│   │   │   └── safety/                         # 安全生产
│   │   │       ├── mem.json                    # 应急管理部
│   │   │       ├── production-safety.json      # 安全生产统计
│   │   │       ├── coal-mine-safety.json       # 煤矿安全数据
│   │   │       └── disaster-stats.json         # 灾害统计数据
│   │   ├── environment/       # 生态环境
│   │   │   ├── pollution/                      # 污染防治
│   │   │   │   ├── mee.json                    # 生态环境部
│   │   │   │   ├── air-quality.json            # 全国空气质量
│   │   │   │   ├── water-quality.json          # 水环境质量
│   │   │   │   ├── soil-pollution.json         # 土壤污染数据
│   │   │   │   └── noise-pollution.json        # 噪声污染数据
│   │   │   ├── climate/                        # 气候变化
│   │   │   │   ├── carbon-emission.json        # 碳排放数据
│   │   │   │   ├── ghg-inventory.json          # 温室气体清单
│   │   │   │   ├── carbon-trading.json         # 碳交易数据
│   │   │   │   └── climate-action.json         # 气候行动数据
│   │   │   ├── ecology/                        # 生态保护
│   │   │   │   ├── biodiversity.json           # 生物多样性数据
│   │   │   │   ├── nature-reserves.json        # 自然保护区
│   │   │   │   ├── wetlands.json               # 湿地数据
│   │   │   │   └── desertification.json        # 荒漠化治理
│   │   │   └── monitoring/                     # 环境监测
│   │   │       ├── env-monitoring.json         # 环境监测数据
│   │   │       ├── pollution-sources.json      # 污染源普查
│   │   │       └── env-impact.json             # 环评数据
│   │   ├── health/            # 卫生健康
│   │   │   ├── public_health/                  # 公共卫生
│   │   │   │   ├── nhc.json                    # 国家卫生健康委
│   │   │   │   ├── health-stats.json           # 卫生统计年鉴
│   │   │   │   ├── disease-surveillance.json   # 疾病监测数据
│   │   │   │   ├── mortality-data.json         # 死因监测数据
│   │   │   │   └── maternal-child.json         # 妇幼健康数据
│   │   │   ├── disease_control/                # 疾病防控
│   │   │   │   ├── cdc.json                    # 中国疾控中心
│   │   │   │   ├── infectious-disease.json     # 传染病数据
│   │   │   │   ├── chronic-disease.json        # 慢性病数据
│   │   │   │   ├── vaccination.json            # 疫苗接种数据
│   │   │   │   └── covid-data.json             # 新冠疫情数据
│   │   │   ├── medical_services/               # 医疗服务
│   │   │   │   ├── hospital-stats.json         # 医疗机构统计
│   │   │   │   ├── medical-personnel.json      # 医护人员数据
│   │   │   │   ├── outpatient-data.json        # 门诊数据
│   │   │   │   └── inpatient-data.json         # 住院数据
│   │   │   ├── pharma/                         # 医药监管
│   │   │   │   ├── nmpa.json                   # 国家药监局
│   │   │   │   ├── drug-approval.json          # 药品审批数据
│   │   │   │   ├── medical-devices.json        # 医疗器械数据
│   │   │   │   └── adverse-reactions.json      # 药品不良反应
│   │   │   └── tcm/                            # 中医药
│   │   │       ├── tcm.json                    # 国家中医药局
│   │   │       ├── tcm-hospitals.json          # 中医医疗机构
│   │   │       └── tcm-resources.json          # 中药资源数据
│   │   ├── education/         # 教育科研
│   │   │   ├── basic_education/                # 基础教育
│   │   │   │   ├── moe.json                    # 教育部
│   │   │   │   ├── education-stats.json        # 教育统计数据
│   │   │   │   ├── preschool.json              # 学前教育数据
│   │   │   │   ├── primary-school.json         # 小学教育数据
│   │   │   │   ├── middle-school.json          # 初中教育数据
│   │   │   │   └── high-school.json            # 高中教育数据
│   │   │   ├── higher_education/               # 高等教育
│   │   │   │   ├── universities.json           # 高校基本数据
│   │   │   │   ├── enrollment.json             # 招生数据
│   │   │   │   ├── graduates.json              # 毕业生数据
│   │   │   │   ├── discipline-catalog.json     # 学科目录
│   │   │   │   └── degree-conferral.json       # 学位授予数据
│   │   │   ├── vocational/                     # 职业教育
│   │   │   │   ├── vocational-colleges.json    # 职业院校数据
│   │   │   │   ├── skills-training.json        # 技能培训数据
│   │   │   │   └── apprenticeship.json         # 学徒制数据
│   │   │   ├── research/                       # 科学研究
│   │   │   │   ├── most.json                   # 科学技术部
│   │   │   │   ├── rd-expenditure.json         # 研发经费数据
│   │   │   │   ├── rd-personnel.json           # 研发人员数据
│   │   │   │   ├── scientific-papers.json      # 科技论文数据
│   │   │   │   └── tech-achievements.json      # 科技成果数据
│   │   │   ├── funding/                        # 科研资助
│   │   │   │   ├── nsfc.json                   # 国家自然科学基金委
│   │   │   │   ├── nsfc-projects.json          # 基金项目数据
│   │   │   │   ├── nssfc.json                  # 国家社科基金
│   │   │   │   └── social-science-projects.json # 社科项目数据
│   │   │   └── institutions/                   # 科研机构
│   │   │       ├── cas.json                    # 中国科学院数据
│   │   │       ├── cae.json                    # 中国工程院
│   │   │       └── research-institutes.json    # 科研院所数据
│   │   ├── labor/             # 人力社保
│   │   │   ├── employment/                     # 就业统计
│   │   │   │   ├── mohrss.json                 # 人力资源社会保障部
│   │   │   │   ├── employment-total.json       # 总体就业数据
│   │   │   │   ├── urban-employment.json       # 城镇就业
│   │   │   │   ├── rural-employment.json       # 农村劳动力转移
│   │   │   │   ├── unemployment-rate.json      # 失业率统计
│   │   │   │   └── job-market.json             # 人力市场供需
│   │   │   ├── wages/                          # 工资薪酬
│   │   │   │   ├── salary-stats.json           # 工资统计
│   │   │   │   ├── minimum-wage.json           # 最低工资标准
│   │   │   │   ├── average-wage.json           # 平均工资
│   │   │   │   ├── industry-wage.json          # 分行业工资
│   │   │   │   └── regional-wage.json          # 分地区工资
│   │   │   ├── social_security/                # 社会保障
│   │   │   │   ├── social-insurance.json       # 社会保险统计
│   │   │   │   ├── pension-fund.json           # 养老保险基金
│   │   │   │   ├── medical-insurance.json      # 医疗保险
│   │   │   │   ├── unemployment-insurance.json # 失业保险
│   │   │   │   └── work-injury-insurance.json  # 工伤保险
│   │   │   ├── talent/                         # 人才培养
│   │   │   │   ├── vocational-training.json    # 职业培训
│   │   │   │   ├── skill-certification.json    # 职业技能鉴定
│   │   │   │   ├── talent-statistics.json      # 人才统计
│   │   │   │   └── professional-titles.json    # 职称评定数据
│   │   │   └── labor_relations/                # 劳动关系
│   │   │       ├── labor-contracts.json        # 劳动合同
│   │   │       ├── labor-disputes.json         # 劳动争议
│   │   │       ├── collective-bargaining.json  # 集体协商
│   │   │       └── labor-inspection.json       # 劳动监察
│   │   ├── housing/           # 住房建设
│   │   │   ├── real_estate/                    # 房地产
│   │   │   │   ├── mohurd.json                 # 住房城乡建设部
│   │   │   │   ├── realestate-stats.json       # 房地产统计
│   │   │   │   ├── property-prices.json        # 房价数据
│   │   │   │   ├── property-sales.json         # 商品房销售
│   │   │   │   ├── land-supply.json            # 土地供应
│   │   │   │   └── property-investment.json    # 房地产开发投资
│   │   │   ├── construction/                   # 建筑业
│   │   │   │   ├── construction-stats.json     # 建筑业统计
│   │   │   │   ├── construction-output.json    # 建筑业产值
│   │   │   │   ├── construction-enterprises.json # 建筑企业数据
│   │   │   │   ├── engineering-quality.json    # 工程质量
│   │   │   │   └── construction-safety.json    # 施工安全
│   │   │   ├── urban_planning/                 # 城乡规划
│   │   │   │   ├── urban-planning.json         # 城市规划数据
│   │   │   │   ├── urban-construction.json     # 城市建设
│   │   │   │   ├── infrastructure.json         # 基础设施
│   │   │   │   ├── municipal-utilities.json    # 市政公用
│   │   │   │   └── village-planning.json       # 乡村规划
│   │   │   ├── affordable_housing/             # 保障房
│   │   │   │   ├── public-rental-housing.json  # 公租房
│   │   │   │   ├── affordable-housing.json     # 经济适用房
│   │   │   │   ├── shantytown-renovation.json  # 棚户区改造
│   │   │   │   └── housing-provident-fund.json # 住房公积金
│   │   │   └── architectural_standards/        # 建筑标准
│   │   │       ├── building-standards.json     # 建筑标准规范
│   │   │       ├── green-building.json         # 绿色建筑
│   │   │       ├── energy-efficiency.json      # 建筑节能
│   │   │       └── building-materials.json     # 建筑材料
│   │   ├── transport/         # 交通运输
│   │   │   ├──综合/                            # 综合运输
│   │   │   │   ├── mot.json                    # 交通运输部
│   │   │   │   ├── transport-stats.json        # 交通运输统计
│   │   │   │   ├── passenger-transport.json    # 客运统计
│   │   │   │   ├── freight-transport.json      # 货运统计
│   │   │   │   └── logistics-stats.json        # 物流统计
│   │   │   ├── railway/                        # 铁路运输
│   │   │   │   ├── nra.json                    # 国家铁路局
│   │   │   │   ├── railway-stats.json          # 铁路统计
│   │   │   │   ├── railway-passenger.json      # 铁路客运
│   │   │   │   ├── railway-freight.json        # 铁路货运
│   │   │   │   ├── high-speed-rail.json        # 高铁数据
│   │   │   │   └── railway-construction.json   # 铁路建设
│   │   │   ├── highway/                        # 公路运输
│   │   │   │   ├── highway-stats.json          # 公路统计
│   │   │   │   ├── highway-network.json        # 公路路网
│   │   │   │   ├── expressway.json             # 高速公路
│   │   │   │   ├── road-transport.json         # 道路运输
│   │   │   │   └── road-safety.json            # 道路安全
│   │   │   ├── aviation/                       # 民航运输
│   │   │   │   ├── caac.json                   # 中国民航局
│   │   │   │   ├── aviation-stats.json         # 民航统计
│   │   │   │   ├── airports.json               # 机场数据
│   │   │   │   ├── airlines.json               # 航空公司
│   │   │   │   ├── flight-operations.json      # 航班运行
│   │   │   │   └── aviation-safety.json        # 航空安全
│   │   │   ├── waterway/                       # 水路运输
│   │   │   │   ├── msa.json                    # 海事局
│   │   │   │   ├── waterway-stats.json         # 水路统计
│   │   │   │   ├── ports.json                  # 港口数据
│   │   │   │   ├── inland-waterway.json        # 内河航运
│   │   │   │   └── maritime-safety.json        # 海上安全
│   │   │   └── urban_transit/                  # 城市交通
│   │   │       ├── metro.json                  # 城市轨道交通
│   │   │       ├── public-transport.json       # 公共交通
│   │   │       ├── taxi.json                   # 出租车
│   │   │       ├── traffic-congestion.json     # 交通拥堵
│   │   │       └── parking.json                # 停车设施
│   │   ├── culture/           # 文化旅游
│   │   │   ├── tourism/                        # 旅游产业
│   │   │   │   ├── mct.json                    # 文化和旅游部
│   │   │   │   ├── tourism-stats.json          # 旅游统计数据
│   │   │   │   ├── domestic-tourism.json       # 国内旅游
│   │   │   │   ├── inbound-tourism.json        # 入境旅游
│   │   │   │   ├── outbound-tourism.json       # 出境旅游
│   │   │   │   ├── tourism-revenue.json        # 旅游收入
│   │   │   │   └── scenic-areas.json           # 景区数据
│   │   │   ├── cultural_industry/              # 文化产业
│   │   │   │   ├── cultural-industry-stats.json # 文化产业统计
│   │   │   │   ├── cultural-enterprises.json   # 文化企业
│   │   │   │   ├── cultural-consumption.json   # 文化消费
│   │   │   │   ├── museums.json                # 博物馆数据
│   │   │   │   └── performing-arts.json        # 演出市场
│   │   │   ├── heritage/                       # 文化遗产
│   │   │   │   ├── cultural-heritage.json      # 文化遗产保护
│   │   │   │   ├── world-heritage.json         # 世界遗产
│   │   │   │   ├── intangible-heritage.json    # 非物质文化遗产
│   │   │   │   └── historical-sites.json       # 文物古迹
│   │   │   ├── media/                          # 广播影视
│   │   │   │   ├── nrta.json                   # 国家广播电视总局
│   │   │   │   ├── broadcasting-stats.json     # 广播电视统计
│   │   │   │   ├── film-industry.json          # 电影产业
│   │   │   │   ├── tv-industry.json            # 电视产业
│   │   │   │   └── streaming-media.json        # 网络视听
│   │   │   └── publishing/                     # 新闻出版
│   │   │       ├── npa.json                    # 国家新闻出版署
│   │   │       ├── publishing-stats.json       # 出版统计
│   │   │       ├── book-publishing.json        # 图书出版
│   │   │       ├── periodicals.json            # 期刊出版
│   │   │       └── digital-publishing.json     # 数字出版
│   │   ├── technology/        # 科技创新
│   │   │   ├── intellectual_property/          # 知识产权
│   │   │   │   ├── cnipa.json                  # 国家知识产权局
│   │   │   │   ├── patent-stats.json           # 专利统计数据
│   │   │   │   ├── invention-patents.json      # 发明专利
│   │   │   │   ├── utility-models.json         # 实用新型
│   │   │   │   ├── design-patents.json         # 外观设计
│   │   │   │   ├── trademarks.json             # 商标数据
│   │   │   │   └── copyright.json              # 著作权
│   │   │   ├── digital_economy/                # 数字经济
│   │   │   │   ├── cac.json                    # 国家网信办
│   │   │   │   ├── internet-stats.json         # 互联网统计
│   │   │   │   ├── digital-economy-stats.json  # 数字经济统计
│   │   │   │   ├── ecommerce-data.json         # 电子商务数据
│   │   │   │   ├── big-data-industry.json      # 大数据产业
│   │   │   │   └── cloud-computing.json        # 云计算产业
│   │   │   ├── telecommunications/             # 通信产业
│   │   │   │   ├── miit-telecom.json           # 工信部通信数据
│   │   │   │   ├── telecom-stats.json          # 电信业务统计
│   │   │   │   ├── mobile-users.json           # 移动用户
│   │   │   │   ├── broadband.json              # 宽带接入
│   │   │   │   ├── 5g-deployment.json          # 5G建设
│   │   │   │   └── iot.json                    # 物联网
│   │   │   ├── high_tech/                      # 高新技术
│   │   │   │   ├── high-tech-industry.json     # 高新技术产业
│   │   │   │   ├── artificial-intelligence.json # 人工智能
│   │   │   │   ├── robotics.json               # 机器人产业
│   │   │   │   ├── semiconductor.json          # 半导体产业
│   │   │   │   └── new-materials.json          # 新材料
│   │   │   └── science_resources/              # 科技资源
│   │   │       ├── istic.json                  # 科技信息研究所
│   │   │       ├── cstnet.json                 # 中国科技网
│   │   │       ├── science-databases.json      # 科技数据库
│   │   │       ├── tech-platforms.json         # 科技平台
│   │   │       └── innovation-centers.json     # 创新中心
│   │   ├── meteorology/       # 气象地震
│   │   │   ├── weather/                        # 气象观测
│   │   │   │   ├── cma.json                    # 中国气象局
│   │   │   │   ├── weather-data.json           # 气象数据
│   │   │   │   ├── daily-weather.json          # 日常天气
│   │   │   │   ├── precipitation.json          # 降水数据
│   │   │   │   ├── temperature.json            # 气温数据
│   │   │   │   └── extreme-weather.json        # 极端天气
│   │   │   ├── climate/                        # 气候变化
│   │   │   │   ├── climate-data.json           # 气候数据
│   │   │   │   ├── climate-change.json         # 气候变化监测
│   │   │   │   ├── seasonal-forecast.json      # 季节预报
│   │   │   │   └── climate-models.json         # 气候模型
│   │   │   ├── meteorological_services/        # 气象服务
│   │   │   │   ├── weather-forecast.json       # 天气预报
│   │   │   │   ├── meteorological-disasters.json # 气象灾害
│   │   │   │   ├── agricultural-meteorology.json # 农业气象
│   │   │   │   └── aviation-meteorology.json   # 航空气象
│   │   │   ├── seismology/                     # 地震监测
│   │   │   │   ├── cea.json                    # 中国地震局
│   │   │   │   ├── earthquake-data.json        # 地震数据
│   │   │   │   ├── earthquake-catalog.json     # 地震目录
│   │   │   │   ├── seismic-networks.json       # 地震台网
│   │   │   │   └── earthquake-early-warning.json # 地震预警
│   │   │   └── geophysics/                     # 地球物理
│   │   │       ├── geomagnetic-data.json       # 地磁数据
│   │   │       ├── ionosphere.json             # 电离层
│   │   │       ├── space-weather.json          # 空间天气
│   │   │       └── crustal-movement.json       # 地壳形变
│   │   ├── civil_affairs/     # 民政社会
│   │   │   ├── social_administration/          # 社会事务
│   │   │   │   ├── mca.json                    # 民政部
│   │   │   │   ├── marriage-stats.json         # 婚姻登记统计
│   │   │   │   ├── divorce-stats.json          # 离婚统计
│   │   │   │   ├── adoption.json               # 收养登记
│   │   │   │   └── funeral-services.json       # 殡葬服务
│   │   │   ├── social_organizations/           # 社会组织
│   │   │   │   ├── ngo-data.json               # 社会组织数据
│   │   │   │   ├── social-groups.json          # 社会团体
│   │   │   │   ├── foundations.json            # 基金会
│   │   │   │   ├── private-non-enterprise.json # 民办非企业
│   │   │   │   └── charity-organizations.json  # 慈善组织
│   │   │   ├── social_welfare/                 # 社会福利
│   │   │   │   ├── welfare-stats.json          # 社会福利统计
│   │   │   │   ├── elderly-care.json           # 养老服务
│   │   │   │   ├── disability-welfare.json     # 残疾人福利
│   │   │   │   ├── child-welfare.json          # 儿童福利
│   │   │   │   └── welfare-institutions.json   # 福利机构
│   │   │   ├── social_assistance/              # 社会救助
│   │   │   │   ├── dibao.json                  # 低保数据
│   │   │   │   ├── temporary-assistance.json   # 临时救助
│   │   │   │   ├── disaster-relief.json        # 救灾救济
│   │   │   │   └── vagrant-assistance.json     # 流浪救助
│   │   │   └── community_services/             # 基层治理
│   │   │       ├── community-stats.json        # 社区统计
│   │   │       ├── village-committees.json     # 村民委员会
│   │   │       ├── residents-committees.json   # 居民委员会
│   │   │       └── community-services.json     # 社区服务
│   │   ├── justice/           # 公安司法
│   │   │   ├── public_security/                # 公安治安
│   │   │   │   ├── mps.json                    # 公安部
│   │   │   │   ├── crime-stats.json            # 犯罪统计
│   │   │   │   ├── traffic-accidents.json      # 交通事故
│   │   │   │   ├── fire-incidents.json         # 火灾数据
│   │   │   │   ├── household-registration.json # 户籍管理
│   │   │   │   └── public-order.json           # 治安管理
│   │   │   ├── judicial_administration/        # 司法行政
│   │   │   │   ├── moj.json                    # 司法部
│   │   │   │   ├── lawyers.json                # 律师数据
│   │   │   │   ├── notary.json                 # 公证数据
│   │   │   │   ├── legal-aid.json              # 法律援助
│   │   │   │   └── prisons.json                # 监狱管理
│   │   │   ├── courts/                         # 法院系统
│   │   │   │   ├── court.json                  # 最高人民法院
│   │   │   │   ├── court-cases.json            # 案件统计
│   │   │   │   ├── court-judgments.json        # 裁判文书
│   │   │   │   ├── execution-cases.json        # 执行案件
│   │   │   │   └── judicial-transparency.json  # 司法公开
│   │   │   ├── procuratorate/                  # 检察系统
│   │   │   │   ├── procuratorate.json          # 最高人民检察院
│   │   │   │   ├── prosecution-cases.json      # 公诉案件
│   │   │   │   ├── supervision-cases.json      # 监督案件
│   │   │   │   ├── anti-corruption.json        # 反贪腐数据
│   │   │   │   └── public-interest.json        # 公益诉讼
│   │   │   └── arbitration/                    # 仲裁调解
│   │   │       ├── arbitration-stats.json      # 仲裁统计
│   │   │       ├── commercial-arbitration.json # 商事仲裁
│   │   │       ├── labor-arbitration.json      # 劳动仲裁
│   │   │       └── mediation.json              # 人民调解
│   │   ├── audit/             # 审计税务
│   │   │   ├── government_audit/               # 政府审计
│   │   │   │   ├── audit.json                  # 审计署
│   │   │   │   ├── audit-reports.json          # 审计报告
│   │   │   │   ├── budget-audit.json           # 预算执行审计
│   │   │   │   ├── economic-audit.json         # 经济责任审计
│   │   │   │   ├── project-audit.json          # 项目审计
│   │   │   │   └── financial-audit.json        # 财政审计
│   │   │   ├── taxation/                       # 税收征管
│   │   │   │   ├── sta.json                    # 国家税务总局
│   │   │   │   ├── tax-stats.json              # 税收统计
│   │   │   │   ├── tax-revenue.json            # 税收收入
│   │   │   │   ├── vat-data.json               # 增值税数据
│   │   │   │   ├── corporate-tax.json          # 企业所得税
│   │   │   │   ├── individual-tax.json         # 个人所得税
│   │   │   │   └── customs-duties.json         # 关税数据
│   │   │   ├── tax_enforcement/                # 税收稽查
│   │   │   │   ├── tax-inspection.json         # 税务稽查
│   │   │   │   ├── tax-violations.json         # 税收违法
│   │   │   │   ├── tax-collection.json         # 欠税追缴
│   │   │   │   └── tax-relief.json             # 税收减免
│   │   │   └── accounting_standards/           # 会计准则
│   │   │       ├── accounting-standards.json   # 会计准则
│   │   │       ├── accounting-firms.json       # 会计师事务所
│   │   │       ├── certified-accountants.json  # 注册会计师
│   │   │       └── accounting-supervision.json # 会计监督
│   │   ├── provincial/        # 省级数据源（34个省级行政区全覆盖）
│   │   │   ├── municipalities/                 # 直辖市（4个）
│   │   │   │   ├── beijing/                    # 北京市
│   │   │   │   │   ├── bj-stats.json           # 北京统计局
│   │   │   │   │   ├── bj-data.json            # 北京政府数据
│   │   │   │   │   └── bj-econ.json            # 北京经济信息网
│   │   │   │   ├── shanghai/                   # 上海市
│   │   │   │   │   ├── sh-stats.json           # 上海统计局
│   │   │   │   │   ├── sh-data.json            # 上海政府数据
│   │   │   │   │   └── sh-pudong.json          # 浦东新区数据
│   │   │   │   ├── tianjin/                    # 天津市
│   │   │   │   │   ├── tj-stats.json           # 天津统计局
│   │   │   │   │   └── tj-data.json            # 天津政府数据
│   │   │   │   └── chongqing/                  # 重庆市
│   │   │   │       ├── cq-stats.json           # 重庆统计局
│   │   │   │       └── cq-data.json            # 重庆政府数据
│   │   │   ├── provinces/                      # 省份（23个）
│   │   │   │   ├── hebei/                      # 河北省
│   │   │   │   │   ├── hebei-stats.json        # 河北统计局
│   │   │   │   │   └── hebei-data.json         # 河北政府数据
│   │   │   │   ├── shanxi/                     # 山西省
│   │   │   │   │   ├── shanxi-stats.json       # 山西统计局
│   │   │   │   │   └── shanxi-data.json        # 山西政府数据
│   │   │   │   ├── liaoning/                   # 辽宁省
│   │   │   │   │   ├── ln-stats.json           # 辽宁统计局
│   │   │   │   │   └── ln-data.json            # 辽宁政府数据
│   │   │   │   ├── jilin/                      # 吉林省
│   │   │   │   │   ├── jl-stats.json           # 吉林统计局
│   │   │   │   │   └── jl-data.json            # 吉林政府数据
│   │   │   │   ├── heilongjiang/               # 黑龙江省
│   │   │   │   │   ├── hlj-stats.json          # 黑龙江统计局
│   │   │   │   │   └── hlj-data.json           # 黑龙江政府数据
│   │   │   │   ├── jiangsu/                    # 江苏省
│   │   │   │   │   ├── js-stats.json           # 江苏统计局
│   │   │   │   │   ├── js-data.json            # 江苏政府数据
│   │   │   │   │   └── js-suzhou.json          # 苏州市数据
│   │   │   │   ├── zhejiang/                   # 浙江省
│   │   │   │   │   ├── zj-stats.json           # 浙江统计局
│   │   │   │   │   ├── zj-data.json            # 浙江政府数据
│   │   │   │   │   └── zj-hangzhou.json        # 杭州市数据
│   │   │   │   ├── anhui/                      # 安徽省
│   │   │   │   │   ├── ah-stats.json           # 安徽统计局
│   │   │   │   │   └── ah-data.json            # 安徽政府数据
│   │   │   │   ├── fujian/                     # 福建省
│   │   │   │   │   ├── fj-stats.json           # 福建统计局
│   │   │   │   │   ├── fj-data.json            # 福建政府数据
│   │   │   │   │   └── fj-xiamen.json          # 厦门市数据
│   │   │   │   ├── jiangxi/                    # 江西省
│   │   │   │   │   ├── jx-stats.json           # 江西统计局
│   │   │   │   │   └── jx-data.json            # 江西政府数据
│   │   │   │   ├── shandong/                   # 山东省
│   │   │   │   │   ├── sd-stats.json           # 山东统计局
│   │   │   │   │   ├── sd-data.json            # 山东政府数据
│   │   │   │   │   └── sd-qingdao.json         # 青岛市数据
│   │   │   │   ├── henan/                      # 河南省
│   │   │   │   │   ├── henan-stats.json        # 河南统计局
│   │   │   │   │   └── henan-data.json         # 河南政府数据
│   │   │   │   ├── hubei/                      # 湖北省
│   │   │   │   │   ├── hb-stats.json           # 湖北统计局
│   │   │   │   │   ├── hb-data.json            # 湖北政府数据
│   │   │   │   │   └── hb-wuhan.json           # 武汉市数据
│   │   │   │   ├── hunan/                      # 湖南省
│   │   │   │   │   ├── hun-stats.json          # 湖南统计局
│   │   │   │   │   └── hun-data.json           # 湖南政府数据
│   │   │   │   ├── guangdong/                  # 广东省
│   │   │   │   │   ├── gd-stats.json           # 广东统计局
│   │   │   │   │   ├── gd-data.json            # 广东政府数据
│   │   │   │   │   ├── gd-guangzhou.json       # 广州市数据
│   │   │   │   │   ├── gd-shenzhen.json        # 深圳市数据
│   │   │   │   │   └── gd-zhuhai.json          # 珠海市数据
│   │   │   │   ├── hainan/                     # 海南省
│   │   │   │   │   ├── hainan-stats.json       # 海南统计局
│   │   │   │   │   └── hainan-data.json        # 海南政府数据
│   │   │   │   ├── sichuan/                    # 四川省
│   │   │   │   │   ├── sc-stats.json           # 四川统计局
│   │   │   │   │   ├── sc-data.json            # 四川政府数据
│   │   │   │   │   └── sc-chengdu.json         # 成都市数据
│   │   │   │   ├── guizhou/                    # 贵州省
│   │   │   │   │   ├── gz-stats.json           # 贵州统计局
│   │   │   │   │   └── gz-data.json            # 贵州政府数据
│   │   │   │   ├── yunnan/                     # 云南省
│   │   │   │   │   ├── yn-stats.json           # 云南统计局
│   │   │   │   │   └── yn-data.json            # 云南政府数据
│   │   │   │   ├── shaanxi/                    # 陕西省
│   │   │   │   │   ├── shaanxi-stats.json      # 陕西统计局
│   │   │   │   │   ├── shaanxi-data.json       # 陕西政府数据
│   │   │   │   │   └── shaanxi-xian.json       # 西安市数据
│   │   │   │   ├── gansu/                      # 甘肃省
│   │   │   │   │   ├── gansu-stats.json        # 甘肃统计局
│   │   │   │   │   └── gansu-data.json         # 甘肃政府数据
│   │   │   │   ├── qinghai/                    # 青海省
│   │   │   │   │   ├── qinghai-stats.json      # 青海统计局
│   │   │   │   │   └── qinghai-data.json       # 青海政府数据
│   │   │   │   └── taiwan/                     # 台湾省
│   │   │   │       ├── taiwan-stats.json       # 台湾统计部门
│   │   │   │       └── taiwan-data.json        # 台湾开放数据
│   │   │   ├── autonomous_regions/             # 自治区（5个）
│   │   │   │   ├── inner_mongolia/             # 内蒙古自治区
│   │   │   │   │   ├── nmg-stats.json          # 内蒙古统计局
│   │   │   │   │   └── nmg-data.json           # 内蒙古政府数据
│   │   │   │   ├── guangxi/                    # 广西壮族自治区
│   │   │   │   │   ├── gx-stats.json           # 广西统计局
│   │   │   │   │   └── gx-data.json            # 广西政府数据
│   │   │   │   ├── tibet/                      # 西藏自治区
│   │   │   │   │   ├── tibet-stats.json        # 西藏统计局
│   │   │   │   │   └── tibet-data.json         # 西藏政府数据
│   │   │   │   ├── ningxia/                    # 宁夏回族自治区
│   │   │   │   │   ├── ningxia-stats.json      # 宁夏统计局
│   │   │   │   │   └── ningxia-data.json       # 宁夏政府数据
│   │   │   │   └── xinjiang/                   # 新疆维吾尔自治区
│   │   │   │       ├── xinjiang-stats.json     # 新疆统计局
│   │   │   │       └── xinjiang-data.json      # 新疆政府数据
│   │   │   ├── special_admin_regions/          # 特别行政区（2个）
│   │   │   │   ├── hong_kong/                  # 香港特别行政区
│   │   │   │   │   ├── hk-census.json          # 香港统计处
│   │   │   │   │   ├── hk-data.json            # 香港政府数据
│   │   │   │   │   ├── hk-hkma.json            # 香港金管局
│   │   │   │   │   └── hk-hkex.json            # 香港交易所
│   │   │   │   └── macau/                      # 澳门特别行政区
│   │   │   │       ├── macau-stats.json        # 澳门统计局
│   │   │   │       ├── macau-data.json         # 澳门政府数据
│   │   │   │       └── macau-amcm.json         # 澳门金管局
│   │   │   └── major_cities/                   # 重点城市数据（计划单列市等）
│   │   │       ├── shenzhen.json               # 深圳市（已在广东省）
│   │   │       ├── dalian.json                 # 大连市
│   │   │       ├── ningbo.json                 # 宁波市
│   │   │       ├── xiamen.json                 # 厦门市（已在福建省）
│   │   │       ├── qingdao.json                # 青岛市（已在山东省）
│   │   │       ├── chengdu.json                # 成都市（已在四川省）
│   │   │       ├── wuhan.json                  # 武汉市（已在湖北省）
│   │   │       ├── xian.json                   # 西安市（已在陕西省）
│   │   │       ├── hangzhou.json               # 杭州市（已在浙江省）
│   │   │       ├── nanjing.json                # 南京市
│   │   │       └── suzhou.json                 # 苏州市（已在江苏省）
│   │   ├── research/          # 研究机构
│   │   │   ├── cass.json                       # 中国社会科学院
│   │   │   ├── drc.json                        # 国务院发展研究中心
│   │   │   ├── cass-ie.json                    # 社科院经济所
│   │   │   ├── pkucer.json                     # 北大经济研究中心
│   │   │   ├── thucer.json                     # 清华经管学院
│   │   │   └── ruc-ier.json                    # 人大经济研究所
│   │   ├── industry/          # 行业协会
│   │   │   ├── cia.json                        # 中国工业协会
│   │   │   ├── auto-industry.json              # 汽车工业协会
│   │   │   ├── steel-industry.json             # 钢铁工业协会
│   │   │   ├── petroleum.json                  # 石油化工协会
│   │   │   ├── textile.json                    # 纺织工业协会
│   │   │   ├── electronics.json                # 电子信息产业协会
│   │   │   └── pharma.json                     # 医药行业协会
│   │   └── special_data/      # 特色数据
│   │       ├── population-census.json          # 人口普查数据
│   │       ├── economic-census.json            # 经济普查数据
│   │       ├── agricultural-census.json        # 农业普查数据
│   │       ├── input-output-tables.json        # 投入产出表
│   │       ├── provincial-gdp.json             # 分省GDP数据
│   │       ├── county-stats.json               # 县域统计数据
│   │       ├── industry-classification.json    # 行业分类标准
│   │       └── poverty-data.json               # 扶贫脱贫数据
│   │
│   ├── academic/               # 学术研究数据源
│   │   ├── repositories/      # 综合性数据仓库
│   │   │   ├── icpsr.json
│   │   │   ├── harvard-dataverse.json
│   │   │   ├── figshare.json
│   │   │   └── zenodo.json
│   │   ├── economics/         # 经济学
│   │   │   ├── nber.json
│   │   │   ├── penn-world-table.json
│   │   │   └── groningen.json
│   │   ├── health/            # 健康医学
│   │   │   ├── pubmed.json
│   │   │   ├── clinicaltrials.json
│   │   │   └── dhs.json
│   │   ├── environment/       # 环境科学
│   │   │   ├── nasa-earthdata.json
│   │   │   ├── noaa.json
│   │   │   └── copernicus.json
│   │   └── social/            # 社会科学
│   │       ├── pew-research.json
│   │       ├── world-values-survey.json
│   │       └── gss.json
│   │
│   └── sectors/                # 行业/专业领域
│       ├── energy/            # 能源
│       │   ├── iea.json
│       │   ├── eia.json
│       │   ├── bp.json
│       │   └── irena.json
│       ├── technology/        # 科技创新
│       │   ├── wipo.json      # 专利
│       │   ├── uspto.json
│       │   ├── epo.json
│       │   └── global-innovation-index.json
│       ├── education/         # 教育
│       │   ├── pisa.json
│       │   ├── timss.json
│       │   └── pirls.json
│       ├── agriculture/       # 农业
│       │   ├── fao.json
│       │   └── usda.json
│       └── finance/           # 金融市场
│           ├── bis.json
│           └── worldfed.json
│
├── schemas/                    # 元数据标准定义
│   ├── datasource-schema.json # JSON Schema定义
│   ├── taxonomy-schema.json   # 分类体系Schema
│   ├── field-definitions.md   # 字段详细说明
│   └── examples/              # 示例文件
│       ├── complete-example.json
│       └── minimal-example.json
│
├── taxonomies/                 # 分类体系
│   ├── domains.json           # 领域分类
│   ├── regions.json           # 地区分类
│   ├── data-types.json        # 数据类型分类
│   ├── access-levels.json     # 访问级别分类
│   └── organization-types.json # 机构类型分类
│
├── indexes/                    # 索引和目录
│   ├── all-sources.json       # 所有数据源索引
│   ├── by-domain.json         # 按领域索引
│   ├── by-region.json         # 按地区索引
│   ├── by-authority.json      # 按权威性分级索引
│   ├── by-type.json           # 按数据类型索引
│   ├── by-access.json         # 按访问方式索引
│   └── statistics.json        # 统计信息
│
├── docs/                       # 文档
│   ├── README.md              # 项目说明
│   ├── CONTRIBUTING.md        # 贡献指南
│   ├── data-collection-guide.md   # 数据收集指南
│   ├── quality-criteria.md    # 质量评估标准
│   ├── metadata-standard.md   # 元数据标准详细说明
│   ├── authority-rating.md    # 权威性评级方法
│   ├── taxonomy-guide.md      # 分类体系指南
│   └── api-reference.md       # （未来）API文档
│
├── scripts/                    # 工具脚本
│   ├── validate.py            # 验证数据源元数据
│   ├── generate-index.py      # 生成索引文件
│   ├── check-urls.py          # 检查链接有效性
│   ├── export-csv.py          # 导出为CSV
│   ├── export-excel.py        # 导出为Excel
│   ├── stats.py               # 生成统计报告
│   ├── utils/                 # 工具函数
│   │   ├── schema_validator.py
│   │   ├── url_checker.py
│   │   └── file_manager.py
│   └── requirements.txt       # Python依赖
│
├── tests/                      # 测试文件
│   ├── test_validation.py
│   ├── test_schema.py
│   └── fixtures/              # 测试数据
│
├── .github/
│   ├── workflows/
│   │   ├── validate.yml       # PR自动验证
│   │   ├── check-links.yml    # 定期链接检查
│   │   └── generate-index.yml # 自动生成索引
│   ├── ISSUE_TEMPLATE/
│   │   ├── new-source.md      # 新增数据源模板
│   │   ├── update-source.md   # 更新数据源模板
│   │   └── report-issue.md    # 问题报告模板
│   └── pull_request_template.md
│
├── .gitignore
├── LICENSE                     # MIT License
├── README.md                   # 项目主文档
└── PRD.md                      # 本文档
```

### 3.3 分类Taxonomy设计

#### domains.json（领域分类）

```json
{
  "economics": {
    "name": {
      "en": "Economics & Finance",
      "zh": "经济与金融"
    },
    "description": "Macroeconomic data, financial statistics, trade, and development",
    "subcategories": {
      "macroeconomics": "Macroeconomic Indicators",
      "finance": "Financial Markets & Banking",
      "trade": "International Trade",
      "development": "Economic Development",
      "labor": "Labor & Employment"
    }
  },
  "health": {
    "name": {
      "en": "Health & Medicine",
      "zh": "健康与医疗"
    },
    "description": "Public health, epidemiology, healthcare systems",
    "subcategories": {
      "public_health": "Public Health",
      "epidemiology": "Disease & Epidemiology",
      "healthcare_systems": "Healthcare Systems",
      "nutrition": "Nutrition",
      "mental_health": "Mental Health"
    }
  },
  "environment": {
    "name": {
      "en": "Environment & Climate",
      "zh": "环境与气候"
    },
    "description": "Climate data, biodiversity, pollution, natural resources",
    "subcategories": {
      "climate": "Climate Change",
      "biodiversity": "Biodiversity",
      "pollution": "Pollution & Air Quality",
      "energy": "Energy",
      "water": "Water Resources",
      "natural_disasters": "Natural Disasters"
    }
  },
  "social": {
    "name": {
      "en": "Social Development",
      "zh": "社会发展"
    },
    "description": "Population, education, inequality, migration",
    "subcategories": {
      "population": "Population & Demographics",
      "education": "Education",
      "inequality": "Inequality & Poverty",
      "migration": "Migration",
      "culture": "Culture & Society",
      "gender": "Gender"
    }
  },
  "technology": {
    "name": {
      "en": "Technology & Innovation",
      "zh": "科技与创新"
    },
    "description": "Patents, R&D, digital technology, innovation",
    "subcategories": {
      "patents": "Patents & IP",
      "rnd": "R&D Statistics",
      "digital": "Digital Technology",
      "innovation": "Innovation Indicators",
      "internet": "Internet & Telecommunications"
    }
  },
  "agriculture": {
    "name": {
      "en": "Agriculture & Food",
      "zh": "农业与食品"
    },
    "description": "Agricultural production, food security, rural development",
    "subcategories": {
      "production": "Agricultural Production",
      "food_security": "Food Security",
      "rural_development": "Rural Development",
      "fisheries": "Fisheries & Aquaculture"
    }
  },
  "education_culture": {
    "name": {
      "en": "Education & Culture",
      "zh": "教育与文化"
    },
    "description": "Educational statistics, cultural indicators",
    "subcategories": {
      "primary_secondary": "Primary & Secondary Education",
      "higher_education": "Higher Education",
      "skills": "Skills & Competencies",
      "cultural_heritage": "Cultural Heritage"
    }
  },
  "energy": {
    "name": {
      "en": "Energy & Resources",
      "zh": "能源与资源"
    },
    "description": "Energy production, consumption, renewable energy",
    "subcategories": {
      "fossil_fuels": "Fossil Fuels",
      "renewables": "Renewable Energy",
      "nuclear": "Nuclear Energy",
      "energy_efficiency": "Energy Efficiency"
    }
  },
  "transport": {
    "name": {
      "en": "Transport & Logistics",
      "zh": "交通与物流"
    },
    "description": "Transportation data, logistics, infrastructure",
    "subcategories": {
      "road": "Road Transport",
      "aviation": "Aviation",
      "maritime": "Maritime",
      "rail": "Rail"
    }
  },
  "governance": {
    "name": {
      "en": "Governance & Public Policy",
      "zh": "治理与公共政策"
    },
    "description": "Government statistics, public policy, institutions",
    "subcategories": {
      "government_finance": "Government Finance",
      "institutions": "Institutions & Governance",
      "justice": "Justice & Safety",
      "corruption": "Corruption & Transparency"
    }
  }
}
```

#### regions.json（地区分类）

```json
{
  "global": {
    "name": {
      "en": "Global",
      "zh": "全球"
    },
    "description": "Worldwide coverage"
  },
  "africa": {
    "name": {
      "en": "Africa",
      "zh": "非洲"
    },
    "subregions": ["northern_africa", "sub_saharan_africa"]
  },
  "asia": {
    "name": {
      "en": "Asia",
      "zh": "亚洲"
    },
    "subregions": ["east_asia", "south_asia", "southeast_asia", "central_asia", "west_asia"]
  },
  "europe": {
    "name": {
      "en": "Europe",
      "zh": "欧洲"
    },
    "subregions": ["western_europe", "eastern_europe", "northern_europe", "southern_europe"]
  },
  "north_america": {
    "name": {
      "en": "North America",
      "zh": "北美洲"
    },
    "subregions": ["usa", "canada", "mexico", "caribbean"]
  },
  "south_america": {
    "name": {
      "en": "South America",
      "zh": "南美洲"
    }
  },
  "oceania": {
    "name": {
      "en": "Oceania",
      "zh": "大洋洲"
    },
    "subregions": ["australia_new_zealand", "pacific_islands"]
  },
  "countries": {
    "usa": "United States",
    "china": "China",
    "japan": "Japan",
    "germany": "Germany",
    "uk": "United Kingdom",
    "france": "France",
    "india": "India",
    "canada": "Canada",
    "australia": "Australia",
    "brazil": "Brazil"
  }
}
```

---

## 4. 数据源收录标准

### 4.1 收录范围

#### 优先收录（Priority 1）
- **国际组织官方数据**：联合国及其专门机构、世界银行、IMF、OECD、WTO等
- **G20国家官方统计机构**：国家统计局、中央银行、政府部委数据
- **顶级学术机构数据**：世界知名大学和研究中心维护的权威数据库

#### 第二优先（Priority 2）
- **其他国家官方统计**：非G20国家的官方统计机构
- **区域性国际组织**：欧盟、非盟、东盟等区域组织数据
- **行业权威协会**：具有国际影响力的行业协会统计数据
- **知名研究机构**：皮尤研究中心、布鲁金斯学会等

#### 第三优先（Priority 3）
- **专业咨询公司**：麦肯锡、高德纳等权威咨询机构公开数据
- **大型企业开放数据**：Google、Meta等科技公司的公开数据集
- **高质量众包数据**：有严格质控的开源数据项目

### 4.2 收录标准

数据源必须满足以下**全部必要条件**：

#### 必要条件（Must Have）
1. ✅ **权威性**：来自官方机构、国际组织或知名学术/研究机构
2. ✅ **可访问性**：数据可通过公开URL访问（开放或需注册但免费）
3. ✅ **文档性**：有基本的数据说明或元数据
4. ✅ **合法性**：数据使用有明确的许可协议
5. ✅ **活跃性**：数据源仍在维护中（非已停止更新的历史项目）

#### 加分条件（Nice to Have）
- ⭐ API可用
- ⭐ 多种格式支持（CSV、JSON、Excel等）
- ⭐ 完整的方法论文档
- ⭐ 长时间序列数据
- ⭐ 高更新频率
- ⭐ 多语言支持
- ⭐ 被学术界广泛引用

### 4.3 排除标准

以下类型的数据源**不予收录**：

❌ **低质量数据源**
- 无法验证来源的数据
- 众包但缺乏质量控制的数据
- 个人博客或非机构维护的数据

❌ **不可访问数据源**
- 完全付费且价格昂贵的商业数据（如Bloomberg终端）
- 需要复杂申请流程的受限数据（除非特别重要）
- 链接已失效且无替代的历史数据源

❌ **违法或有争议的数据源**
- 违反版权或知识产权的数据
- 涉及个人隐私未经授权的数据
- 政治立场极度偏颇的数据源

❌ **过时或停止维护的数据源**
- 已超过5年未更新且无历史价值的数据
- 机构已解散且数据无法访问

### 4.4 质量评估检查清单

在收录新数据源前，使用以下清单评估：

```
数据源评估清单
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

基本信息
□ 数据源名称明确
□ 维护机构可信
□ 官方网站可访问
□ 数据源仍在活跃更新

权威性评估
□ 来源机构权威性评分 (1-5): ___
□ 方法论透明度评分 (1-5): ___
□ 是否有同行评审或第三方验证

可用性评估
□ 数据可免费访问或有合理的访问方式
□ 支持的数据格式: ___________
□ 是否提供API
□ 文档完整性评分 (1-5): ___

覆盖范围
□ 地理覆盖范围: ___________
□ 时间跨度: _____ 至 _____
□ 涵盖领域: ___________
□ 数据粒度: ___________

更新维护
□ 更新频率: ___________
□ 最近更新日期: ___________
□ 数据完整性评分 (1-5): ___

许可协议
□ 许可类型: ___________
□ 是否允许商业使用
□ 是否要求署名

最终评估
□ 总体评分 (1-5): ___
□ 是否收录: □ 是  □ 否  □ 待定
□ 优先级: □ P1  □ P2  □ P3
```

---

## 5. 技术实现规范

### 5.1 技术栈选择

| 组件 | 技术选择 | 理由 |
|------|---------|------|
| 数据格式 | JSON | 人类可读、机器友好、版本控制友好、广泛支持 |
| Schema验证 | JSON Schema (Draft-07) | 标准化、工具链成熟 |
| 脚本语言 | Python 3.8+ | 易于维护、库丰富、社区活跃 |
| 版本控制 | Git + GitHub | 开源标准、协作友好 |
| CI/CD | GitHub Actions | 免费、集成度高 |
| 文档格式 | Markdown | 通用、易编辑 |
| 开源协议 | MIT License | 最宽松、商业友好 |

### 5.2 数据格式规范

#### 文件命名规范
- **小写字母**：所有文件名使用小写
- **连字符分隔**：使用 `-` 连接单词，如 `world-bank.json`
- **语义化**：文件名应反映数据源名称
- **唯一性**：ID必须在全局唯一

#### JSON格式规范
- **缩进**：使用2个空格
- **编码**：UTF-8
- **排序**：按字母顺序排列顶层键（除特殊情况）
- **换行**：Unix风格（LF）

#### 日期格式
- 统一使用 ISO 8601 格式：`YYYY-MM-DD`
- 示例：`2025-01-22`

#### 语言代码
- 使用 ISO 639-1 两字母代码
- 示例：`en`, `zh`, `es`, `fr`

#### 国家代码
- 使用 ISO 3166-1 alpha-2 代码
- 示例：`US`, `CN`, `JP`, `GB`

### 5.3 验证工具要求

#### validate.py 功能需求
```python
功能列表：
1. JSON格式验证
   - 文件是否为有效JSON
   - 字符编码检查（UTF-8）

2. Schema合规性验证
   - 必填字段完整性
   - 字段类型正确性
   - 枚举值有效性

3. 内容合理性验证
   - URL格式正确性
   - 评分范围（1-5）
   - 日期格式和逻辑（start_year ≤ end_year）
   - 语言代码符合ISO 639-1
   - 国家代码符合ISO 3166-1

4. 引用完整性验证
   - related_sources引用的ID存在
   - domains/regions引用的分类存在于taxonomy

5. 重复性检查
   - ID唯一性
   - 文件名与ID一致性

6. 生成验证报告
   - 通过/失败统计
   - 详细错误信息
   - 警告信息（如可选字段缺失）
```

#### check-urls.py 功能需求
```python
功能列表：
1. URL可访问性检查
   - primary_url
   - api.documentation
   - organization.website
   - contact.support_url

2. HTTP状态码检查
   - 200: 正常
   - 301/302: 重定向（需更新）
   - 404: 失效（需移除或修复）
   - 500+: 服务器错误（暂时性）

3. 超时处理
   - 设置合理超时（10秒）
   - 记录超时URL

4. 生成健康报告
   - 总URL数量
   - 正常/异常/超时统计
   - 失效URL清单
   - 建议修复操作

5. 定期调度
   - 每周运行（GitHub Actions）
   - 生成Issue提醒维护者
```

#### generate-index.py 功能需求
```python
功能列表：
1. 扫描所有数据源文件
   - 递归遍历sources/目录
   - 读取所有.json文件

2. 生成all-sources.json
   - 包含所有数据源的简化信息
   - 字段：id, name, organization, domains, regions, quality综合评分

3. 生成分类索引
   - by-domain.json: 按领域分组
   - by-region.json: 按地区分组
   - by-authority.json: 按评分分级（5星、4星等）
   - by-type.json: 按数据类型分组
   - by-access.json: 按访问方式分组

4. 生成统计信息
   - 总数据源数量
   - 各领域分布
   - 各地区分布
   - 评分分布
   - 最近更新日志

5. 自动更新
   - 在PR合并后自动运行
   - 提交更新的索引文件
```

### 5.4 自动化脚本功能

#### export-csv.py
- 导出为CSV格式
- 支持自定义字段选择
- 便于Excel分析

#### export-excel.py
- 导出为多sheet Excel文件
  - Sheet 1: All Sources（所有数据源）
  - Sheet 2: By Domain（按领域）
  - Sheet 3: By Region（按地区）
  - Sheet 4: Statistics（统计信息）
- 包含格式化（表头加粗、冻结首行等）

#### stats.py
- 生成统计报告
- 可视化分析（如果需要）
- 输出Markdown格式报告

---

## 6. 数据源收录规划

### 6.1 规模概览

| 类别 | 计划 | 当前完成 | 进度 | 详细任务清单 |
|------|------|---------|------|-------------|
| 🌍 国际组织 | 100+ | 15 | 15% | [tasks/international.md](tasks/international.md) |
| 🌎 各国官方 | 200+ | 32 | 16% | [tasks/countries.md](tasks/countries.md) |
| 🇨🇳 中国数据源 | 488 | 6 | 1% | [tasks/china/](tasks/china/) |
| 🎓 学术研究 | 50+ | 4 | 8% | [tasks/academic.md](tasks/academic.md) |
| 🏭 行业领域 | 150+ | 0 | 0% | [tasks/sectors.md](tasks/sectors.md) |
| **总计** | **950+** | **57** | **6%** | [所有任务](tasks/README.md) |

**实时进度追踪**: [项目路线图](ROADMAP.md) | [任务管理系统](tasks/README.md)

---

### 6.2 核心差异化优势

DataSource Hub的核心特色：
1. **深度收录**: 聚焦权威官方数据源，提供专业级元数据
2. **中国数据源**: 全球领先的中国官方数据源深度覆盖（488个规划）
3. **专业元数据**: 40+字段、6维度质量评分、API访问详情
4. **目标用户**: 数据专业人士（分析师、研究员、开发者）

### 6.3 收录优先级

#### 第一阶段（P1）：核心数据源（100个）
- 国际组织核心15个（✅ 已完成）
- 美国核心10个（进行中 10/15）
- 中国国家级13个（进行中 6/13）
- G20国家核心50个（进行中）
- 学术研究核心15个（进行中 4/15）

#### 第二阶段（P2）：中国深度覆盖（488个）
详见 [tasks/china/README.md](tasks/china/README.md)

**16个国家级部委领域**：
- 💰 金融财政（35个）- [详情](tasks/china/finance.md)
- 📈 经济贸易（30个）
- 🚂 交通运输（32个）
- 💻 科技创新（29个）
- 🎓 教育科研（27个）
- ⚖️ 公安司法（25个）
- 👷 人力社保（24个）
- 🏠 住房建设（24个）
- 🌦️ 气象地震（23个）
- 🤝 民政社会（23个）
- ⛰️ 自然资源（22个）
- 🏥 卫生健康（21个）
- 📊 审计税务（21个）
- 🌾 农业农村（18个）
- 🌳 生态环境（16个）
- 📍 国家级综合（6个）

**省级和特色数据**：
- 省级数据源（60个）
- 研究机构（6个）
- 行业协会（7个）
- 特色数据（8个）

#### 第三阶段（P3）：国际扩展（300+个）
- 国际组织完整100个
- 各国官方200+个
- 学术研究50+个
- 行业领域100+个

详见各领域任务清单：[tasks/README.md](tasks/README.md)

### 6.4 重点领域说明

#### 中国数据源的战略意义

🏆 **全球领先的深度覆盖**：
- DataSource Hub: **488个中国数据源**（系统化规划）
- 全球最全面的中国官方数据源知识库

**核心价值**：
- 覆盖16个国家级部委领域
- 涵盖34个省级行政区
- 包含研究机构和行业协会
- 全部来自官方权威机构

**应用场景**：
- 中国经济分析与研究
- 政策制定参考
- 学术研究数据支持
- 商业决策数据来源

详细规划见：[tasks/china/README.md](tasks/china/README.md)

---

## 7. 项目里程碑与实施计划

### 7.1 阶段划分

#### 第一阶段：基础架构搭建（Week 1-2）

**目标**：建立项目基础设施

**任务清单**：
1. ✅ 创建项目目录结构
2. ✅ 编写JSON Schema定义
3. ✅ 编写分类taxonomy（domains.json, regions.json等）
4. ✅ 编写核心文档
   - README.md（项目介绍）
   - CONTRIBUTING.md（贡献指南）
   - data-collection-guide.md（数据收集指南）
   - metadata-standard.md（元数据标准）
   - quality-criteria.md（质量评估标准）
5. ✅ 设置Git仓库和.gitignore
6. ✅ 选择开源协议（MIT License）

**可交付成果**：
- 完整的目录结构
- Schema定义文件
- Taxonomy分类体系
- 核心文档

#### 第二阶段：核心数据收录（Week 3-6）

**目标**：收录50个核心权威数据源

**任务清单**：
1. ✅ 收录15个国际组织数据源
   - 经济：World Bank, IMF, OECD, WTO
   - 健康：WHO, UNICEF, GBD
   - 环境：UNEP, IPCC, WMO
   - 社会：UNDP, ILO, UNESCO
   - 统计：UNdata, UN Population

2. ✅ 收录20个主要国家数据源
   - 美国（5个）
   - 中国（4个）
   - 欧盟（2个）
   - 英国（2个）
   - 日本（2个）
   - 其他G20国家（5个）

3. ✅ 收录15个学术数据源
   - 综合仓库（4个）
   - 经济学（3个）
   - 健康医学（3个）
   - 环境科学（3个）
   - 社会科学（2个）

4. ✅ 质量审核
   - 验证所有URL可访问
   - 确保元数据完整
   - 权威性评分准确

**可交付成果**：
- 50个高质量数据源JSON文件
- 初步的索引文件

#### 第三阶段：工具开发（Week 7-8）

**目标**：开发自动化工具和验证系统

**任务清单**：
1. ✅ 开发validate.py
   - JSON格式验证
   - Schema合规性验证
   - 内容合理性验证
   - 引用完整性验证

2. ✅ 开发generate-index.py
   - 生成all-sources.json
   - 生成分类索引
   - 生成统计信息

3. ✅ 开发check-urls.py
   - URL可访问性检查
   - 生成健康报告

4. ✅ 开发导出工具
   - export-csv.py
   - export-excel.py

5. ✅ 设置GitHub Actions
   - 自动验证PR
   - 定期链接检查
   - 自动生成索引

6. ✅ 编写测试用例

**可交付成果**：
- 完整的工具脚本集
- CI/CD自动化流程
- 测试覆盖

#### 第四阶段：扩展和完善（Week 9-12）

**目标**：扩展到100+数据源，完善社区机制

**任务清单**：
1. ✅ 扩展数据源至100+
   - 补充更多国家数据源
   - 增加行业专业数据源
   - 收录区域性数据源

2. ✅ 完善文档
   - 添加使用案例
   - 编写最佳实践
   - 翻译为多语言（中英文）

3. ✅ 建立社区贡献机制
   - Issue模板
   - PR模板
   - 贡献者指南

4. ✅ 优化索引和检索
   - 改进分类体系
   - 添加标签系统

5. ✅ 宣传和推广
   - 撰写博客文章
   - 社交媒体推广
   - 提交到awesome列表

**可交付成果**：
- 100+数据源
- 完善的社区机制
- 多语言文档

#### 第五阶段：持续维护（Ongoing）

**目标**：保持数据源的活跃和准确性

**任务清单**：
1. ✅ 定期更新数据源信息
2. ✅ 处理社区Issue和PR
3. ✅ 定期链接检查和修复
4. ✅ 添加新发现的权威数据源
5. ✅ 改进工具和流程
6. ✅ 收集用户反馈

**可交付成果**：
- 季度更新报告
- 社区活跃度

### 7.2 时间线（预估）

```
Week 1-2:  基础架构搭建
Week 3-4:  国际组织数据源收录
Week 5:    主要国家数据源收录
Week 6:    学术数据源收录
Week 7-8:  工具开发和自动化
Week 9-10: 扩展至100+数据源
Week 11:   文档完善和社区机制
Week 12:   测试、优化、发布

Total: 约3个月完成第一版
```

### 7.3 关键里程碑

| 里程碑 | 描述 | 预期时间 |
|--------|------|---------|
| M1: 项目初始化 | 目录结构、Schema、文档完成 | Week 2 |
| M2: 核心数据源 | 50个数据源收录完成 | Week 6 |
| M3: 工具链完成 | 验证、索引、检查工具就绪 | Week 8 |
| M4: 第一版发布 | 100+数据源，完整文档 | Week 12 |
| M5: 社区版本 | 200+数据源，活跃社区 | Month 6 |

---

## 8. 社区协作机制

### 8.1 贡献流程

#### 新增数据源流程

```
1. Fork项目
   ↓
2. 创建新分支（add-datasource-xxx）
   ↓
3. 按照模板创建JSON文件
   ↓
4. 本地运行validate.py验证
   ↓
5. 提交Pull Request
   ↓
6. 自动验证（GitHub Actions）
   ↓
7. 维护者Review
   ↓
8. 合并到主分支
   ↓
9. 自动生成索引文件
```

#### 更新数据源流程

```
1. 发现数据源信息过时
   ↓
2. 提交Issue或直接PR
   ↓
3. 更新相应JSON文件
   ↓
4. 验证和Review
   ↓
5. 合并更新
```

### 8.2 质量审核机制

#### 自动审核（GitHub Actions）
- JSON格式验证
- Schema合规性检查
- URL可访问性测试
- 必填字段完整性

#### 人工审核（维护者）
- 数据源权威性评估
- 元数据准确性检查
- 分类合理性判断
- 评分公正性审核

#### 审核标准
- **Accept（接受）**：符合所有标准，可直接合并
- **Request Changes（请求修改）**：有明显问题，需修改后重审
- **Comment（评论）**：提供建议，无强制要求

### 8.3 维护者职责

#### 领域维护者
- 负责特定领域（如经济、健康）的数据源审核
- 评估领域内数据源的权威性
- 建议新的高质量数据源

#### 地区维护者
- 负责特定地区（如亚洲、欧洲）的数据源
- 熟悉本地区官方统计机构
- 提供多语言支持

#### 核心维护者
- 总体项目管理
- 重大决策（如Schema变更）
- 协调各领域维护者
- 处理复杂Issue

### 8.4 贡献者激励

- **Contributors页面**：展示所有贡献者
- **积分系统**（可选）：根据贡献量授予徽章
- **致谢文档**：在README中致谢重要贡献者
- **年度报告**：总结社区贡献

---

## 9. 成功指标

### 9.1 量化指标

#### 第一年目标

| 指标 | 目标值 | 衡量方式 |
|------|--------|---------|
| 数据源总数 | 200+ | 文件数量统计 |
| 覆盖领域 | 10个主要领域 | domains覆盖度 |
| 覆盖国家/地区 | 50+ | 地区覆盖度 |
| 高权威性数据源（4星+） | 80% | 评分分布 |
| GitHub Stars | 500+ | GitHub统计 |
| 贡献者数量 | 20+ | GitHub Contributors |
| 月活跃访问量 | 1000+ | GitHub Insights |
| 外部引用/引用 | 10+ | 学术论文、博客引用 |

#### 长期目标（3年）

| 指标 | 目标值 |
|------|--------|
| 数据源总数 | 500+ |
| 覆盖国家/地区 | 100+ |
| GitHub Stars | 5000+ |
| 贡献者数量 | 100+ |
| 成为行业标准 | 被主要研究机构采用 |

### 9.2 质量指标

| 指标 | 目标值 | 衡量方式 |
|------|--------|---------|
| 元数据完整性 | 95%+ | 必填字段填充率 |
| URL有效性 | 98%+ | 链接健康检查 |
| 平均权威性评分 | 4.5+ | 所有数据源平均分 |
| 更新及时性 | 每季度更新 | 最后更新日期统计 |
| Schema合规率 | 100% | 验证通过率 |

### 9.3 影响力指标

- **学术引用**：被研究论文引用作为数据源参考
- **媒体报道**：被数据科学、研究领域的媒体报道
- **行业采用**：被企业、政府、NGO使用
- **教育使用**：被大学课程或培训项目采用
- **工具集成**：被数据分析工具或平台集成

---

## 10. 风险和限制

### 10.1 潜在挑战

#### 1. 数据源变更风险
**问题**：
- 官方网站URL变更
- 数据源停止维护
- API版本更新

**应对策略**：
- 定期自动化链接检查
- 记录历史URL和变更日志
- 提供数据源状态标记（active/deprecated）
- 社区监控和快速响应

#### 2. 质量控制挑战
**问题**：
- 主观评分偏差
- 数据源质量下降
- 社区贡献质量参差

**应对策略**：
- 明确评分标准和示例
- 多维度评分减少偏差
- 维护者交叉审核
- 定期质量审计

#### 3. 维护工作量
**问题**：
- 数据源信息需持续更新
- PR审核需要专业知识
- 工具和文档需要维护

**应对策略**：
- 建立维护者团队
- 自动化工具减少人工
- 社区协作分担工作
- 清晰的文档降低门槛

#### 4. 版权和许可问题
**问题**：
- 数据源许可协议复杂
- 元数据描述可能侵权
- 商业数据收录边界

**应对策略**：
- 仅收录公开可访问数据源
- 描述使用原创文字
- 明确标注许可信息
- 咨询法律意见（如需）

#### 5. 规模扩展挑战
**问题**：
- JSON文件数量增多后管理复杂
- 索引生成时间变长
- 搜索效率降低

**应对策略**：
- 优化目录结构
- 引入数据库（如需）
- 实施缓存机制
- 考虑未来API服务

### 10.2 项目限制

#### 范围限制
- **不提供数据本身**：仅提供数据源元数据和访问信息
- **不做数据托管**：不存储或镜像原始数据
- **不做数据清洗**：不对原始数据进行处理

#### 技术限制
- **静态数据**：当前阶段为静态JSON文件，无动态查询
- **人工维护**：依赖人工收录和更新，非自动发现
- **无实时性**：元数据更新有延迟

#### 覆盖限制
- **语言限制**：初期主要为中英文，其他语言有限
- **地域偏向**：可能偏向主要国家，小国数据源较少
- **领域覆盖**：初期聚焦核心领域，细分领域逐步补充

---

## 11. 未来愿景

### 11.1 短期愿景（1年内）

1. **成为权威参考**
   - 被学术界、数据科学社区认可
   - 成为数据工作者的首选数据源导航

2. **建立社区**
   - 活跃的贡献者社区
   - 跨领域的维护者团队

3. **工具生态**
   - Python/R包封装数据源访问
   - 命令行工具快速查询

### 11.2 中期愿景（2-3年）

1. **API服务**
   - 提供RESTful API查询数据源
   - 支持高级搜索和筛选

2. **Web界面**
   - 开发用户友好的Web界面
   - 可视化展示数据源分布

3. **智能推荐**
   - 基于用户需求推荐数据源
   - 数据源关联关系挖掘

4. **数据质量监控**
   - 自动化数据源健康监控
   - 质量报告和告警

### 11.3 长期愿景（3年+）

1. **数据生态枢纽**
   - 成为连接数据提供者和使用者的桥梁
   - 推动数据开放和标准化

2. **知识图谱**
   - 构建数据源知识图谱
   - 语义化检索和发现

3. **全球协作**
   - 多语言支持（10+语言）
   - 全球维护者网络

4. **行业影响力**
   - 推动数据源元数据标准化
   - 与国际组织合作

---

## 12. 附录

### 12.1 参考资料

#### 元数据标准
- Dublin Core Metadata Initiative: https://www.dublincore.org/
- DataCite Metadata Schema: https://schema.datacite.org/
- W3C DCAT: https://www.w3.org/TR/vocab-dcat/
- SDMX: https://sdmx.org/

#### 数据质量
- ISO 25012 Data Quality Model
- FAIR Principles (Findable, Accessible, Interoperable, Reusable)

#### 开源项目参考
- Data Portals: https://dataportals.org/
- OpenMetadata: https://github.com/open-metadata/OpenMetadata

### 12.2 术语表

| 术语 | 定义 |
|------|------|
| 数据源 (Data Source) | 提供可访问数据的官方或权威机构平台 |
| 元数据 (Metadata) | 描述数据源的结构化信息 |
| Taxonomy | 分类体系，用于组织和分类数据源 |
| Schema | 数据结构定义，规定数据源元数据的格式 |
| Authority Level | 权威性级别，评估数据源可信度的指标 |
| Open Data | 开放数据，可自由访问和使用的数据 |
| API | 应用程序编程接口，程序化访问数据的方式 |
| SDMX | 统计数据和元数据交换标准 |

### 12.3 联系方式

- **项目仓库**: [待定] https://github.com/[username]/datasource-hub
- **项目网站**: [待定]
- **联系邮箱**: [待定]
- **讨论社区**: [待定] GitHub Discussions

---

## 文档变更历史

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|---------|------|
| 1.0 | 2025-01-22 | 初始版本 | DataSource Hub Team |

---

**END OF DOCUMENT**
