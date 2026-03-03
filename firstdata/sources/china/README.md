# 中国数据源 | China Data Sources

> 📊 **最新统计**: 查看 [indexes/statistics.json](../../indexes/statistics.json) 获取实时数据源统计信息。

---

## 📚 已收录数据源

### 📍 国家级综合统计

#### 国家统计局 - National Bureau of Statistics
- **文件**: [nbs.json](national/nbs.json)
- **权威等级**: government
- **涵盖**: GDP、人口、工业、投资、消费等全面统计
- **更新频率**: 月度

### 💰 金融财政

#### 银行系统

##### 中国人民银行 - People's Bank of China
- **文件**: [pbc.json](finance/banking/pbc.json)
- **权威等级**: government
- **涵盖**: 货币供应、利率、汇率、外汇储备、信贷数据
- **更新频率**: 月度

##### 国家金融监督管理总局 - National Financial Regulatory Administration
- **文件**: [nfra.json](finance/banking/nfra.json)
- **权威等级**: government
- **涵盖**: 银行业、保险业监管数据、金融机构统计
- **更新频率**: 季度

#### 证券市场

##### 证监会 - China Securities Regulatory Commission
- **文件**: [csrc.json](finance/securities/csrc.json)
- **权威等级**: government
- **涵盖**: 股票市场、IPO、上市公司、债券、基金数据
- **更新频率**: 月度

##### 香港交易所 - Hong Kong Exchanges and Clearing
- **文件**: [hkex.json](finance/securities/hkex.json)
- **权威等级**: commercial
- **涵盖**: 证券交易数据、衍生品数据、上市公司信息、市场指数
- **更新频率**: 实时

### 📈 经济贸易

#### 对外贸易

##### 海关总署 - General Administration of Customs
- **文件**: [customs.json](economy/trade/customs.json)
- **权威等级**: government
- **涵盖**: 进出口数据、贸易差额、HS商品分类
- **更新频率**: 月度

##### 商务部 - Ministry of Commerce
- **文件**: [mofcom.json](economy/trade/mofcom.json)
- **权威等级**: government
- **涵盖**: FDI、ODI、零售、电商、服务贸易
- **更新频率**: 月度

#### 宏观经济

##### 国家发改委 - National Development and Reform Commission
- **文件**: [ndrc.json](economy/macro/ndrc.json) ⭐💎
- **权威等级**: government
- **涵盖**: 固定资产投资、价格监测、产业政策
- **更新频率**: 月度

##### 国家发展改革委东数西算工程 - NDRC East-to-West Computing Resources Project
- **文件**: [china-ndrc-computing.json](economy/macro/china-ndrc-computing.json) ⭐💎
- **权威等级**: government
- **访问类型**: 需注册
- **涵盖**: 8大国家算力枢纽节点、10个国家数据中心集群、算力基础设施统计、工程进展报告、政策文件、算力资源调度、绿色算力指标、网络性能数据
- **特色**: 覆盖京津冀、长三角、粤港澳大湾区、成渝等8个枢纽节点，统筹推进通用算力、智能算力、超级算力协同建设，构建全国一体化算力网络体系
- **更新频率**: 不定期

### 🎓 教育科研

#### 高等教育

##### 中华人民共和国教育部高等教育统计 - Ministry of Education of China - Higher Education Statistics
- **文件**: [china-moe-higher-education.json](education/higher_education/china-moe-higher-education.json) ⭐💎
- **权威等级**: government
- **访问类型**: 需注册
- **涵盖**: 高等教育招生与在校生数据、毕业生统计、高校机构数据、师资队伍统计、基础设施数据、教育质量指标、民办/公办院校对比、高等职业教育统计
- **特色**: 年度全国高等教育事业发展统计公报，提供本科、硕士、博士等各层次教育的详细分类数据（2005年至今）
- **更新频率**: 年度

### ⛰️ 自然资源

#### 矿产资源

##### 工业和信息化部稀土办公室 - MIIT Rare Earth Office - Rare Earth Industry Regulation and Production Quotas
- **文件**: [china-miit-rare-earth.json](resources/mineral/china-miit-rare-earth.json) ⭐💎
- **权威等级**: government
- **访问类型**: 需注册
- **涵盖**: 稀土行业规范条件、生产总量控制指标、出口配额管理、稀土产业政策、稀土开采指标、冶炼分离指标、行业准入名单
- **特色**: 管理全国稀土行业准入与生产配额，涵盖开采、冶炼分离等全产业链监管数据
- **更新频率**: 不定期

##### 自然资源部矿产资源数据 - Ministry of Natural Resources - Mineral Resources Data
- **文件**: [china-mnr-minerals.json](resources/mineral/china-mnr-minerals.json) ⭐💎
- **权威等级**: government
- **访问类型**: 需注册
- **涵盖**: 矿产资源储量统计、矿业权登记数据、矿产资源开发利用数据、矿产品产量统计、矿产资源规划、地质勘查数据、重要矿产资源保障程度
- **特色**: 覆盖能源矿产、金属矿产、非金属矿产等全类别矿产资源的权威统计数据
- **更新频率**: 年度

### 💻 科技创新

#### 数字经济

##### 国家数据局 - National Data Administration of China
- **文件**: [china-national-data-bureau.json](technology/digital_economy/china-national-data-bureau.json) ⭐💎
- **权威等级**: government
- **访问类型**: 需注册
- **涵盖**: 数据资源管理、数据要素市场建设、数据基础设施统计、数据安全与合规、数据产业发展指标、数字化转型案例、数据交易市场数据
- **特色**: 国家数据管理机构，负责协调推进数据基础制度建设、统筹数据资源整合共享和开发利用
- **更新频率**: 不定期

#### 知识产权

##### 国家知识产权局专利统计 - China National Intellectual Property Administration - Patent Statistics
- **文件**: [china-cnipa-patents.json](technology/intellectual_property/china-cnipa-patents.json) ⭐💎
- **权威等级**: government
- **访问类型**: 需注册
- **涵盖**: 专利申请量和授权量、发明专利统计、实用新型专利、外观设计专利、PCT国际专利申请、专利维持情况、专利转让与许可、专利质量指标、分省市专利统计、分行业专利统计、国内外申请人对比、高价值专利统计
- **特色**: 月度更新，提供从1985年至今的历史数据，涵盖国内外专利申请全貌，支持按地区、行业、技术领域多维度分析
- **更新频率**: 月度

#### 科技资源

##### 重大科研基础设施和大型科研仪器国家网络管理平台 - National Platform for Research Infrastructure and Large-scale Scientific Instruments
- **文件**: [china-most-infrastructure.json](technology/sci_resources/china-most-infrastructure.json) ⭐💎
- **权威等级**: government
- **访问类型**: 需注册
- **涵盖**: 国家重大科研基础设施目录、大型科研仪器共享平台、仪器设备开放共享数据、设施运行状况监测、服务绩效评估
- **特色**: 实时更新的国家级科研设施和仪器共享服务平台，促进科研资源开放共享
- **更新频率**: 每日

##### 国家重点研发计划 - National Key R&D Program of China - Industrial Software and 16 Key Special Projects
- **文件**: [china-most-rnd.json](technology/sci_resources/china-most-rnd.json) ⭐💎
- **权威等级**: government
- **访问类型**: 需注册
- **涵盖**: 工业软件专项项目立项、16个重点专项资助数据、项目进展与成果、科研经费投入统计、项目参与单位信息、技术攻关方向、成果转化数据
- **特色**: 聚焦工业软件及16个国家战略重点领域（新一代信息技术、高端装备、新材料等），支撑关键核心技术攻关
- **更新频率**: 年度

#### 标准化

##### 国家标准化管理委员会 - Standardization Administration of China (SAC)
- **文件**: [china-sac-standards.json](technology/standards/china-sac-standards.json) ⭐💎
- **权威等级**: government
- **访问类型**: 需注册
- **涵盖**: 国家标准目录与全文、标准制修订计划、行业标准信息、地方标准备案、团体标准统计、企业标准自我声明、标准实施效果评估、国际标准采标情况、标准化技术委员会信息、重点领域标准化路线图
- **特色**: 国家标准化工作主管部门，管理全国标准化工作，覆盖所有行业和领域的标准信息
- **更新频率**: 不定期

#### 通信产业

##### 中华人民共和国工业和信息化部 - Ministry of Industry and Information Technology of the People's Republic of China
- **文件**: [china-miit.json](technology/telecommunications/china-miit.json) ⭐💎
- **权威等级**: government
- **访问类型**: 需注册
- **涵盖**: 电信业务统计、互联网行业数据、工业生产数据、软件产业统计、无线电管理、信息通信行业发展指标、5G建设进展、新能源汽车产销数据、工业企业效益
- **特色**: 工业和信息化领域主管部门，提供工业经济运行、信息通信业发展、软件和信息技术服务业等多维度权威统计数据
- **更新频率**: 月度

### 🔬 研究机构

##### 中国信息通信研究院 - China Academy of Information and Communications Technology
- **文件**: [china-caict.json](research/china-caict.json) ⭐
- **权威等级**: research
- **访问类型**: 需注册
- **涵盖**: 云计算白皮书、算力发展指数、ICT产业研究报告、数字经济蓝皮书、先进计算报告、技术白皮书（5G、物联网、区块链、大数据等）、行业标准与基准
- **特色**: 工业和信息化部直属科研机构，国家ICT领域高端专业智库，发布权威行业研究报告和技术白皮书
- **更新频率**: 不定期

---

## 🏆 项目亮点

### 全球领先的深度覆盖
FirstData 提供**全球最全面**的中国官方数据源知识库：

- **覆盖深度**: 国家级 + 省级 + 行业
- **元数据详细度**: 40+字段专业级
- **权威等级**: 6维度评分系统

### 核心价值
1. **权威性**：全部来自政府官方机构和权威协会
2. **系统性**：覆盖17个领域、34个省级行政区
3. **专业性**：详细的元数据和质量评估
4. **实用性**：API访问方式、数据内容详细说明

### 数据源特点

#### 高权威性 High Authority
- 🏛️ 来源: 国家统计局、人民银行、海关总署等官方机构
- ✅ 认证: 政府官网、权威组织发布

#### 全面覆盖 Comprehensive Coverage
- 📊 覆盖领域: 20个核心领域
- 🌏 地理范围: 全国、省级、地市级
- 📅 时间跨度: 1949年至今

#### 开放获取 Open Access
- 🆓 大部分为开放数据，无需付费
- 📥 支持Excel、PDF、HTML等多种格式下载
- 🌐 提供中英文双语界面

---

## 目录结构 Directory Structure

**✅ 完整的目录结构已创建**，包含所有子目录，覆盖20个领域：

```
sources/china/
├── national/                   # 国家级综合统计
│   └── nbs.json
├── finance/                    # 金融财政
│   ├── banking/                # 银行系统
│   │   ├── pbc.json
│   │   └── nfra.json
│   ├── securities/             # 证券市场
│   │   ├── csrc.json
│   │   └── hkex.json
│   ├── bonds/                  # 债券市场
│   ├── insurance/              # 保险行业
│   ├── funds/                  # 基金行业
│   ├── fiscal/                 # 财政税收
│   ├── forex/                  # 外汇管理
│   └── monetary-policy/        # 货币政策
├── economy/                    # 经济贸易
│   ├── macro/                  # 宏观经济
│   │   └── ndrc.json
│   ├── trade/                  # 对外贸易
│   │   ├── customs.json
│   │   └── mofcom.json
│   ├── industry/               # 工业制造
│   ├── market/                 # 市场监管
│   ├── soe/                    # 国有企业
│   └── consumption/            # 消费市场
├── transport/                  # 交通运输
│   ├── comprehensive/          # 综合运输
│   ├── railway/                # 铁路运输
│   ├── highway/                # 公路运输
│   ├── aviation/               # 民航运输
│   └── waterway/               # 水路运输
├── culture/                    # 文化旅游
│   ├── tourism/                # 旅游产业
│   ├── cultural_industry/      # 文化产业
│   ├── heritage/               # 文化遗产
│   ├── media/                  # 媒体广播
│   └── publishing/             # 新闻出版
├── technology/                 # 科技创新
│   ├── intellectual_property/  # 知识产权
│   ├── digital_economy/        # 数字经济
│   ├── telecommunications/     # 通信产业
│   ├── high_tech/              # 高新技术
│   └── sci_resources/          # 科技资源
├── education/                  # 教育科研
│   ├── basic_education/        # 基础教育
│   ├── higher_education/       # 高等教育
│   ├── vocational/             # 职业教育
│   ├── research/               # 科学研究
│   ├── funding/                # 科研资助
│   └── institutions/           # 科研机构
├── justice/                    # 公安司法
│   ├── public_security/        # 公安部门
│   ├── judiciary/              # 司法系统
│   ├── procuratorate/          # 检察系统
│   └── legal_services/         # 法律服务
├── labor/                      # 人力社保
│   ├── employment/             # 就业统计
│   ├── social_security/        # 社会保障
│   ├── wages/                  # 工资收入
│   ├── labor_relations/        # 劳动关系
│   └── talent/                 # 人才发展
├── housing/                    # 住房建设
│   ├── real_estate/            # 房地产市场
│   ├── construction/           # 建筑业
│   ├── urban_planning/         # 城市规划
│   └── public_housing/         # 保障性住房
├── meteorology/                # 气象地震
│   ├── weather/                # 天气气象
│   ├── climate/                # 气候监测
│   ├── earthquake/             # 地震监测
│   └── disaster/               # 灾害预警
├── civil-affairs/              # 民政社会
│   ├── social_services/        # 社会服务
│   ├── charity/                # 慈善公益
│   ├── funeral/                # 殡葬管理
│   └── community/              # 社区治理
├── agriculture/                # 农业农村
│   ├── crop/                   # 种植业
│   ├── livestock/              # 畜牧业
│   ├── forestry/               # 林业
│   ├── fishery/                # 渔业
│   └── rural/                  # 农村发展
├── resources/                  # 自然资源
│   ├── land/                   # 土地资源
│   ├── mineral/                # 矿产资源
│   ├── ocean/                  # 海洋资源
│   └── surveying/              # 测绘地理
├── health/                     # 卫生健康
│   ├── healthcare/             # 医疗卫生
│   ├── disease_control/        # 疾病防控
│   ├── pharma/                 # 医药监管
│   └── tcm/                    # 中医药
├── audit/                      # 审计税务
│   ├── audit/                  # 审计监督
│   ├── taxation/               # 税务征管
│   ├── customs/                # 海关监管
│   └── accounting/             # 会计管理
├── environment/                # 生态环境
│   ├── pollution_control/      # 污染防治
│   ├── ecology/                # 生态保护
│   └── climate/                # 气候变化
├── provincial/                 # 省级数据源
│   ├── municipalities/         # 直辖市
│   │   ├── beijing/
│   │   ├── shanghai/
│   │   ├── tianjin/
│   │   └── chongqing/
│   ├── provinces/              # 省份
│   ├── autonomous_regions/     # 自治区
│   │   ├── inner_mongolia/
│   │   ├── guangxi/
│   │   ├── tibet/
│   │   ├── ningxia/
│   │   └── xinjiang/
│   ├── special_admin_regions/  # 特别行政区
│   │   ├── hong_kong/
│   │   └── macau/
│   └── major_cities/           # 重点城市
├── research/                   # 研究机构
│   # 中国社会科学院、国务院发展研究中心、北京大学经济研究中心
│   # 清华大学经济管理学院、中国人民大学经济研究所、中国科学院
├── industry/                   # 行业协会
│   # 中国工业协会、汽车工业协会、钢铁工业协会
│   # 石油化工协会、纺织工业协会、电子信息产业协会、医药行业协会
├── special/                    # 特色数据
│   # 人口普查、经济普查、农业普查、投入产出表
│   # 分省GDP、县域统计、行业分类标准、扶贫脱贫数据
└── README.md
```

## 领域分类说明 Domain Classification

### 国家级部委数据源（345个）
包含17个领域的政府部委数据源：
- 💰 金融财政 (36个) - 银行、证券、债券、保险、基金、财政、外汇
- 🚂 交通运输 (27个) - 综合、铁路、公路、航空、水路
- 🎭 文化旅游 (26个) - 旅游、文化产业、文化遗产、媒体、出版
- 📈 经济贸易 (24个) - 宏观经济、对外贸易、工业、市场监管、国企
- 💻 科技创新 (24个) - 知识产权、数字经济、通信、高新技术、科技资源
- 🎓 教育科研 (24个) - 基础教育、高等教育、职业教育、科研、资助、机构
- ⚖️ 公安司法 (21个) - 公安、司法、检察、法律服务
- 👷 人力社保 (20个) - 就业、社保、工资、劳动关系、人才
- 🏠 住房建设 (20个) - 房地产、建筑、城市规划、保障房
- 🌦️ 气象地震 (19个) - 天气、气候、地震、灾害
- 🤝 民政社会 (19个) - 社会服务、慈善、殡葬、社区
- 🌾 农业农村 (18个) - 种植、畜牧、林业、渔业、农村发展
- ⛰️ 自然资源 (18个) - 土地、矿产、海洋、测绘
- 🏥 卫生健康 (18个) - 医疗、疾控、医药、中医药
- 📊 审计税务 (17个) - 审计、税务、海关、会计
- 🌳 生态环境 (13个) - 污染防治、生态保护、气候变化
- 📍 国家级综合 (1个) - 国家统计局

### 省级数据源（49个）
- 📍 直辖市 (4个)
- 📍 省 (23个)
- 📍 自治区 (5个)
- 📍 特别行政区 (2个)
- 📍 重点城市 (15个)

### 研究机构和特色数据（21个）
- 🔬 研究机构 (6个) - 社科院、发展研究中心、高校研究机构、中科院
- 🏢 行业协会 (7个) - 工业、汽车、钢铁、石化、纺织、电子信息、医药
- ⭐ 特色数据 (8个) - 普查数据、投入产出表、分省GDP、县域统计等

## 📚 领域说明 Domain Details

### 💰 金融财政（36个）
- **银行系统**（7个）：人民银行、国家金融监督管理总局、存款保险、银行业协会等
- **证券市场**（8个）：证监会、上交所、深交所、北交所、新三板、中国结算、证券业协会
- **债券市场**（3个）：中国债券信息网、上海清算所、国债发行
- **保险行业**（2个）：保险统计、保险业协会
- **基金行业**（3个）：基金业协会、公募基金、私募基金
- **财政税收**（6个）：财政部、财政收支、地方政府债务、预算报告、国库统计
- **外汇管理**（7个）：外汇管理局、外汇储备、国际收支、跨境人民币、外汇市场、外债、国际投资头寸

### 📈 经济贸易（24个）
- **宏观经济**（5个）：发改委、价格监测、GDP、CPI/PPI、PMI
- **对外贸易**（7个）：商务部、FDI、ODI、海关总署、海关统计、进出口、分国别贸易
- **工业制造**（5个）：工信部、工业增加值、制造业、中小企业、规上企业
- **市场监管**（4个）：市场监管总局、企业注册、消费者权益、质量监督
- **国有企业**（3个）：国资委、中央企业、地方国企

### 💻 科技创新（24个）
- **知识产权**（7个）：知识产权局、专利统计、发明专利、实用新型、外观设计、商标、著作权
- **数字经济**（6个）：网信办、互联网统计、数字经济、电商数据、大数据产业、云计算
- **通信产业**（6个）：工信部通信数据、电信业务统计、移动用户、宽带接入、5G建设、物联网
- **高新技术**（5个）：高新技术产业、人工智能、机器人产业、半导体产业、新材料

### 🚂 交通运输（27个）
- **综合运输**（5个）：交通运输部、交通运输统计、客运统计、货运统计、物流统计
- **铁路运输**（6个）：国家铁路局、铁路统计、铁路客运、铁路货运、高铁数据、铁路建设
- **公路运输**（5个）：公路统计、公路路网、高速公路、道路运输、道路安全
- **民航运输**（6个）：民航局、民航统计、机场数据、航空公司、航班运行、航空安全
- **水路运输**（5个）：海事局、水路统计、港口数据、内河航运、海上安全

### 🎭 文化旅游（26个）
- **旅游产业**（9个）：文化和旅游部、旅游统计、国内旅游、入境旅游、出境旅游、旅游收入、景区数据、星级饭店、旅行社
- **文化产业**（7个）：文化产业统计、文化企业、文化消费、博物馆、演出市场、艺术品市场、文化场馆
- **文化遗产**（4个）：文化遗产保护、世界遗产、非物质文化遗产、文物古迹
- **广播影视**（6个）：国家广电总局、广播电视统计、电影产业、电视产业、流媒体、网络视听节目

### 🎓 教育科研（24个）
- **基础教育**（7个）：教育部、教育统计、学前教育、小学、初中、高中
- **高等教育**（6个）：高校基本数据、招生数据、毕业生数据、学科目录、学位授予
- **职业教育**（3个）：职业院校、技能培训、学徒制
- **科学研究**（5个）：科技部、研发经费、研发人员、科技论文、科技成果
- **科研资助**（3个）：国家自然科学基金委、国家社科基金、重点研发计划


## 📖 使用说明 Usage Guide

每个JSON文件遵循FirstData标准元数据Schema，包含以下关键信息：

- **基本信息**: ID、名称（中英文）、描述
- **访问信息**: website、data_url、api_url（如有）
- **权威等级**: government/international/research/market等
- **覆盖范围**: 地理范围、领域、更新频率
- **数据内容**: 可用数据类型和内容描述
- **搜索标签**: 中英文关键词、同义词
