# 目录结构规则

根据数据源类型保存到相应目录。

## 中国数据源 (sources/china/)

```
china/
├── national/          # 国家级机构
│   └── nbs.json      # 国家统计局
├── finance/
│   ├── banking/      # 银行业
│   │   └── pbc.json # 中国人民银行
│   ├── securities/   # 证券业
│   │   └── csrc.json
│   └── insurance/    # 保险业
├── economy/
│   ├── macro/        # 宏观经济
│   │   └── ndrc.json
│   └── trade/        # 贸易
│       ├── customs.json
│       └── mofcom.json
├── social/           # 社会领域
├── education/        # 教育
├── health/           # 卫生健康
└── provincial/       # 省级数据
```

## 国际数据源 (sources/international/)

```
international/
├── economics/        # 经济
│   ├── worldbank.json
│   ├── imf.json
│   └── oecd.json
├── trade/           # 贸易
│   └── wto.json
├── health/          # 健康
├── environment/     # 环境
└── development/     # 发展
```

## 各国数据源 (sources/countries/)

```
countries/
├── us/              # 美国
├── uk/              # 英国
├── jp/              # 日本
├── de/              # 德国
└── ...
```

## 学术数据源 (sources/academic/)

基于 tasks/academic.md 的分类：

```
academic/
├── repositories/       # 综合性数据仓库
│   ├── icpsr.json
│   ├── harvard-dataverse.json
│   ├── figshare.json
│   └── zenodo.json
├── economics/          # 经济学
│   └── nber.json
├── health/             # 健康医学
│   ├── pubmed.json
│   └── genbank.json
├── environment/        # 环境科学
├── social/             # 社会科学
├── physics_chemistry/  # 物理化学
└── biology/            # 生命科学
```

## 行业数据源 (sources/sectors/)

基于 tasks/sectors.md 的分类（150+个数据源规划）：

```
sectors/
├── energy/                  # 能源 (10个)
│   └── iea.json
├── innovation_patents/      # 科技创新-专利 (12个)
│   └── wipo.json
├── education/               # 教育评估 (8个)
│   └── oecd-pisa.json
├── agriculture_food/        # 农业与食品 (8个)
│   └── faostat.json
├── finance_markets/         # 金融市场 (12个)
│   └── bis.json
├── computer_science_ai/     # 计算机科学与AI/ML (20个)
│   ├── imagenet.json
│   └── kaggle.json
├── nlp/                     # 自然语言处理 (12个)
│   └── wordnet.json
├── biology/                 # 生物与生命科学 (10个)
├── chemistry_materials/     # 化学与材料 (6个)
├── geoscience_geography/    # 地球科学与地理 (15个)
│   └── openstreetmap.json
├── social_media/            # 社交媒体与网络数据 (10个)
├── sports/                  # 体育运动 (8个)
├── transportation/          # 交通运输 (8个)
├── museums_culture/         # 博物馆与文化遗产 (6个)
├── timeseries/              # 时间序列数据
├── cybersecurity/           # 网络安全
└── other/                   # 其他专业领域
```

## 选择规则

1. **中国数据源**: 按领域和层级分类
   - 国家级机构 → `china/national/`
   - 特定领域 → `china/{domain}/{subdomain}/`

2. **国际数据源**: 按主题领域分类
   - `international/{domain}/`

3. **各国数据源**: 按国家分类
   - `countries/{country-code}/`

4. **学术数据源**: 按学科领域分类
   - `academic/{domain}/`

5. **行业数据源**: 按行业领域分类
   - `sectors/{domain}/`

6. **文件命名**: 使用数据源名称的简称小写形式
   - 示例: `nbs.json`, `pbc.json`, `worldbank.json`
