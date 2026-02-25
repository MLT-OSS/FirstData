# 数据源集合 | Data Sources

## 概览 | Overview

本目录包含 FirstData 收录的所有数据源元数据。

This directory contains metadata for all data sources included in FirstData.

> 📊 **最新统计**: 查看 [indexes/statistics.json](../indexes/statistics.json) 获取实时数据源统计信息。

## 目录结构 | Directory Structure

### 📂 中国数据源 | China
**路径**: `sources/china/`

中国政府机构和官方组织发布的权威数据源，涵盖20个领域：
- 国家级综合统计
- 国家级部委数据源：金融、经济、交通、文化、科技、教育等17个领域
- 省级数据源：34个省级行政区 + 15个重点城市
- 研究机构和特色数据

[查看详情 | View Details →](china/README.md)

### 🌍 国际组织 | International
**路径**: `sources/international/`

国际组织和跨国机构发布的全球性数据源，涵盖14个领域：
- 经济、贸易、能源、农业、教育、健康
- 环境、发展、金融、知识产权、地球科学
- 劳工与社会、交通运输、标准与计量

[查看详情 | View Details →](international/README.md)

### 🌎 各国官方 | Countries
**路径**: `sources/countries/`

各国官方政府机构发布的权威数据源，涵盖6大洲42个国家：
- 北美洲：美国、加拿大、墨西哥
- 欧洲：15个国家
- 亚洲：14个国家（除中国）
- 大洋洲：澳大利亚、新西兰
- 南美洲：4个国家
- 非洲：4个国家

[查看详情 | View Details →](countries/README.md)

### 🎓 学术研究 | Academic
**路径**: `sources/academic/`

学术机构和研究组织维护的学术研究数据源，涵盖9个学科领域：
- 经济学、健康医学、环境科学
- 社会科学、物理学、化学
- 生命科学、材料学
- 地球科学与地理信息

[查看详情 | View Details →](academic/README.md)

### 🏭 行业领域 | Sectors
**路径**: `sources/sectors/`

特定行业和专业领域的数据源，按照国际标准产业分类（ISIC Rev.4）组织：
- A-S共19个产业门类
- 从农业到服务业的完整覆盖
- 包括制造业、能源、金融、信息通信、教育、健康等

[查看详情 | View Details →](sectors/README.md)

## 分类规则 | Classification Rules

### 路径格式 | Path Format

- **中国数据源**: `sources/china/{domain}/{subdomain}/{id}.json`
- **国际组织**: `sources/international/{domain}/{id}.json`
- **各国官方**: `sources/countries/{continent}/{id}.json`
- **学术研究**: `sources/academic/{domain}/{id}.json`
- **行业领域**: `sources/sectors/{isic-category}/{id}.json`

### 命名规范 | Naming Convention

- 文件名使用数据源 ID
- ID 格式：`{国家/组织}-{简称}` (如 `china-pbc`, `canada-statcan`)
- 使用小写字母和连字符
- 目录名使用连字符分隔（如 `north-america`, `civil-affairs`）

## 数据源特点 | Data Source Features

### 高权威性 | High Authority
- ✅ 所有数据源均来自官方机构、知名研究组织或权威行业机构
- ✅ 数据经过严格的质量控制和验证
- ✅ 被学术界、政策制定者和业界广泛引用

### 开放获取 | Open Access
- 🆓 大部分数据源提供开放访问或注册后免费使用
- 📥 支持多种访问方式：API、批量下载、在线查询
- 🌐 遵循FAIR数据原则（可查找、可访问、可互操作、可重用）

### 全面覆盖 | Comprehensive Coverage
- 📊 地理覆盖：全球、区域、国家、省级、城市级
- 📅 时间跨度：从历史数据到实时更新
- 🔬 领域覆盖：经济、金融、健康、环境、教育、科技等
