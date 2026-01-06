# 中国金融财政领域 - 任务清单

**领域**: 金融财政
**总数**: 36个数据源
**已完成**: 4个
**进度**: 11%

---

## 📊 子领域进度概览

| 子领域 | 计划 | 完成 | 进度 |
|--------|------|------|------|
| 银行系统 | 7 | 2 | 29% |
| 证券市场 | 8 | 2 | 25% |
| 债券市场 | 3 | 0 | 0% |
| 保险行业 | 2 | 0 | 0% |
| 基金行业 | 3 | 0 | 0% |
| 财政税收 | 6 | 0 | 0% |
| 外汇管理 | 7 | 0 | 0% |
| **总计** | **36** | **4** | **11%** | - |

---

## 1. 银行系统（7个数据源）

### ✅ 1.1 中国人民银行 (`china-pbc`)
- **状态**: ✅ 已完成
- **完成日期**: 2025-01-20
- **文件**: `sources/china/finance/banking/pbc.json`
- **贡献者**: 系统初始化
- **权威性**: 5.0 💎
- **URL**: http://www.pbc.gov.cn/
- **说明**: 中国人民银行官方网站，发布货币政策、金融统计等数据

### 📋 1.2 人民银行统计数据 (`pbc-stats`)
- **状态**: 📋 已完成
- **完成日期**: 2025-01-20
- **文件**: `sources/china/finance/banking/pbc-stats.json`
- **贡献者**: 系统初始化
- **权威性**: 5.0 💎
- **URL**: http://www.pbc.gov.cn/diaochatongjisi/
- **说明**: 人民银行调查统计司发布的金融统计数据

### 📋 1.3 人民银行货币政策执行报告 (`pbc-monetary`)
- **状态**: 📋 待开始

- **URL**: http://www.pbc.gov.cn/zhengcehuobisi/125207/125227/125957/index.html
- **目标文件**: `sources/china/finance/banking/pbc-monetary.json`
- **预估工作量**: 1.5小时
- **说明**: 季度货币政策执行报告，包含宏观经济和金融形势分析
- **认领**: [点击认领Issue](#)

### 📋 1.4 银保监会 (`cbirc`)
- **状态**: 📋 待开始

- **URL**: http://www.cbirc.gov.cn/
- **目标文件**: `sources/china/finance/banking/cbirc.json`
- **预估工作量**: 2小时
- **说明**: 中国银行保险监督管理委员会，发布银行业和保险业监管统计数据
- **认领**: [点击认领Issue](#)

### 📋 1.5 存款保险基金 (`deposit-insurance`)
- **状态**: 📋 待开始

- **URL**: http://www.dic.pbc.gov.cn/
- **目标文件**: `sources/china/finance/banking/deposit-insurance.json`
- **预估工作量**: 1小时
- **说明**: 存款保险基金管理有限责任公司，发布存款保险制度相关数据
- **认领**: [点击认领Issue](#)

### 📋 1.6 银行业协会 (`banking-industry`)
- **状态**: 📋 待开始

- **URL**: https://www.china-cba.net/
- **目标文件**: `sources/china/finance/banking/banking-industry.json`
- **预估工作量**: 1.5小时
- **说明**: 中国银行业协会，发布银行业发展报告和统计数据
- **认领**: [点击认领Issue](#)

### ❓ 1.7 商业银行统计汇总 (`commercial-banks`)
- **状态**: ❓ 待确认
- **说明**: 需要讨论是否单独收录各大商业银行（工农中建交）的数据，还是仅收录银保监会的汇总数据
- **讨论**: [创建讨论Issue](#)

---

## 2. 证券市场（8个数据源）

### ✅ 2.1 证监会 (`csrc`)
- **状态**: ✅ 已完成
- **完成日期**: 2025-01-22
- **文件**: `sources/china/finance/securities/csrc.json`
- **权威性**: 5.0 💎
- **URL**: http://www.csrc.gov.cn/
- **说明**: 中国证券监督管理委员会，发布证券市场监管和统计数据

### 📋 2.2 上海证券交易所 (`sse`)
- **状态**: 📋 已完成
- **完成日期**: 2025-01-21
- **文件**: `sources/china/finance/securities/sse.json`
- **权威性**: 5.0 💎
- **URL**: http://www.sse.com.cn/
- **说明**: 上海证券交易所，发布A股市场交易数据、上市公司信息

### 📋 2.3 深圳证券交易所 (`szse`)
- **状态**: 📋 已完成
- **完成日期**: 2025-01-21
- **文件**: `sources/china/finance/securities/szse.json`
- **权威性**: 5.0 💎
- **URL**: http://www.szse.cn/
- **说明**: 深圳证券交易所，发布A股市场交易数据、上市公司信息

### 📋 2.4 北京证券交易所 (`bse`)
- **状态**: 📋 待开始

- **URL**: https://www.bse.cn/
- **目标文件**: `sources/china/finance/securities/bse.json`
- **预估工作量**: 1.5小时
- **说明**: 北京证券交易所（2021年成立），服务创新型中小企业
- **认领**: [点击认领Issue](#)

### 📋 2.5 全国股转系统（新三板）(`neeq`)
- **状态**: 📋 待开始

- **URL**: http://www.neeq.com.cn/
- **目标文件**: `sources/china/finance/securities/neeq.json`
- **预估工作量**: 1.5小时
- **说明**: 全国中小企业股份转让系统，发布新三板市场数据
- **认领**: [点击认领Issue](#)

### 📋 2.6 中国结算 (`csdc`)
- **状态**: 📋 待开始

- **URL**: http://www.chinaclear.cn/
- **目标文件**: `sources/china/finance/securities/csdc.json`
- **预估工作量**: 1.5小时
- **说明**: 中国证券登记结算有限责任公司，发布证券登记结算统计数据
- **认领**: [点击认领Issue](#)

### 📋 2.7 证券业协会 (`sac`)
- **状态**: 📋 待开始

- **URL**: http://www.sac.net.cn/
- **目标文件**: `sources/china/finance/securities/sac.json`
- **预估工作量**: 1小时
- **说明**: 中国证券业协会，发布证券行业统计数据
- **认领**: [点击认领Issue](#)

### ✅ 2.8 香港交易所 (`hkex`)
- **状态**: ✅ 已完成
- **完成日期**: 2025-12-24
- **文件**: `sources/china/finance/securities/hkex.json`
- **贡献者**: DataSource Hub Team
- **权威性**: 4.7 💎
- **URL**: https://www.hkex.com.hk/
- **说明**: 香港交易及结算所有限公司，提供证券、衍生品市场数据及上市公司信息

---

## 3. 债券市场（3个数据源）

### 📋 3.1 中国债券信息网 (`chinabond`)
- **状态**: 📋 待开始

- **URL**: https://www.chinabond.com.cn/
- **目标文件**: `sources/china/finance/bonds/chinabond.json`
- **预估工作量**: 2小时
- **说明**: 中央国债登记结算公司，发布债券市场数据、收益率曲线等
- **认领**: [点击认领Issue](#)

### 📋 3.2 上海清算所 (`shclearhouse`)
- **状态**: 📋 待开始

- **URL**: https://www.shclearing.com/
- **目标文件**: `sources/china/finance/bonds/shclearhouse.json`
- **预估工作量**: 1.5小时
- **说明**: 银行间市场清算所股份有限公司，发布债券交易清算数据
- **认领**: [点击认领Issue](#)

### 📋 3.3 国债发行数据 (`treasury-bonds`)
- **状态**: 📋 待开始

- **URL**: http://www.mof.gov.cn/guozaixin/
- **目标文件**: `sources/china/finance/bonds/treasury-bonds.json`
- **预估工作量**: 1小时
- **说明**: 财政部国债信息，发布国债发行、兑付数据
- **认领**: [点击认领Issue](#)

---

## 4. 保险行业（2个数据源）

### 📋 4.1 保险业统计 (`insurance-stats`)
- **状态**: 📋 待开始

- **URL**: http://www.cbirc.gov.cn/ (银保监会下属)
- **目标文件**: `sources/china/finance/insurance/insurance-stats.json`
- **预估工作量**: 1.5小时
- **说明**: 银保监会发布的保险业统计数据
- **认领**: [点击认领Issue](#)

### 📋 4.2 保险业协会 (`iia`)
- **状态**: 📋 待开始

- **URL**: http://www.iachina.cn/
- **目标文件**: `sources/china/finance/insurance/iia.json`
- **预估工作量**: 1小时
- **说明**: 中国保险行业协会，发布保险行业报告
- **认领**: [点击认领Issue](#)

---

## 5. 基金行业（3个数据源）

### 📋 5.1 基金业协会 (`amac`)
- **状态**: 📋 待开始

- **URL**: http://www.amac.org.cn/
- **目标文件**: `sources/china/finance/funds/amac.json`
- **预估工作量**: 2小时
- **说明**: 中国证券投资基金业协会，发布公募和私募基金统计数据
- **认领**: [点击认领Issue](#)

### 📋 5.2 公募基金数据 (`mutual-funds`)
- **状态**: 📋 待开始

- **URL**: http://www.amac.org.cn/researchstatistics/dataservice/
- **目标文件**: `sources/china/finance/funds/mutual-funds.json`
- **预估工作量**: 1.5小时
- **说明**: 公募基金规模、业绩、持仓等数据
- **认领**: [点击认领Issue](#)

### 📋 5.3 私募基金数据 (`pe-funds`)
- **状态**: 📋 待开始

- **URL**: http://www.amac.org.cn/researchstatistics/dataservice/
- **目标文件**: `sources/china/finance/funds/pe-funds.json`
- **预估工作量**: 1.5小时
- **说明**: 私募基金登记备案统计数据
- **认领**: [点击认领Issue](#)

---

## 6. 财政税收（6个数据源）

### 📋 6.1 财政部 (`mof`)
- **状态**: 📋 已完成
- **完成日期**: 2025-01-21
- **文件**: `sources/china/finance/fiscal/mof.json`
- **权威性**: 5.0 💎
- **URL**: http://www.mof.gov.cn/
- **说明**: 中华人民共和国财政部，发布全国财政收支数据

### 📋 6.2 财政收入数据 (`fiscal-revenue`)
- **状态**: 📋 待开始

- **URL**: http://www.mof.gov.cn/zhengwuxinxi/caizhengshuju/
- **目标文件**: `sources/china/finance/fiscal/fiscal-revenue.json`
- **预估工作量**: 1小时
- **说明**: 月度、年度全国财政收入数据
- **认领**: [点击认领Issue](#)

### 📋 6.3 财政支出数据 (`fiscal-expenditure`)
- **状态**: 📋 待开始

- **URL**: http://www.mof.gov.cn/zhengwuxinxi/caizhengshuju/
- **目标文件**: `sources/china/finance/fiscal/fiscal-expenditure.json`
- **预估工作量**: 1小时
- **说明**: 月度、年度全国财政支出数据
- **认领**: [点击认领Issue](#)

### 📋 6.4 地方政府债务 (`local-gov-debt`)
- **状态**: 📋 待开始

- **URL**: http://www.mof.gov.cn/
- **目标文件**: `sources/china/finance/fiscal/local-gov-debt.json`
- **预估工作量**: 1.5小时
- **说明**: 地方政府债务余额、发行情况等数据
- **认领**: [点击认领Issue](#)

### 📋 6.5 预算报告 (`budget-reports`)
- **状态**: 📋 待开始

- **URL**: http://yss.mof.gov.cn/
- **目标文件**: `sources/china/finance/fiscal/budget-reports.json`
- **预估工作量**: 1小时
- **说明**: 年度预算报告、预算执行情况报告
- **认领**: [点击认领Issue](#)

### 📋 6.6 税收数据 (`tax-revenue`)
- **状态**: 📋 待开始

- **说明**: 注：税收数据可能与审计税务领域的`国家税务总局`重叠，需确认是否单独收录
- **讨论**: [创建讨论Issue](#)

---

## 7. 外汇管理（7个数据源）

### 📋 7.1 国家外汇管理局 (`safe`)
- **状态**: 📋 待开始

- **URL**: http://www.safe.gov.cn/
- **目标文件**: `sources/china/finance/forex/safe.json`
- **预估工作量**: 2小时
- **说明**: 国家外汇管理局，发布外汇储备、国际收支等数据
- **认领**: [点击认领Issue](#)

### 📋 7.2 外汇储备数据 (`forex-reserves`)
- **状态**: 📋 待开始

- **URL**: http://www.safe.gov.cn/safe/whxw/index.html
- **目标文件**: `sources/china/finance/forex/forex-reserves.json`
- **预估工作量**: 1小时
- **说明**: 月度外汇储备规模数据
- **认领**: [点击认领Issue](#)

### 📋 7.3 国际收支平衡表 (`bop`)
- **状态**: 📋 待开始

- **URL**: http://www.safe.gov.cn/safe/gjsy/index.html
- **目标文件**: `sources/china/finance/forex/bop.json`
- **预估工作量**: 1.5小时
- **说明**: 季度、年度国际收支平衡表数据
- **认领**: [点击认领Issue](#)

### 📋 7.4 跨境人民币业务 (`cross-border-rmb`)
- **状态**: 📋 待开始

- **URL**: http://www.safe.gov.cn/
- **目标文件**: `sources/china/finance/forex/cross-border-rmb.json`
- **预估工作量**: 1小时
- **说明**: 跨境人民币收付统计数据
- **认领**: [点击认领Issue](#)

### 📋 7.5 外债数据 (`external-debt`)
- **状态**: 📋 待开始

- **URL**: http://www.safe.gov.cn/safe/wz/index.html
- **目标文件**: `sources/china/finance/forex/external-debt.json`
- **预估工作量**: 1小时
- **说明**: 季度全口径外债数据
- **认领**: [点击认领Issue](#)

### 📋 7.6 银行结售汇 (`bank-forex`)
- **状态**: 📋 待开始

- **URL**: http://www.safe.gov.cn/safe/whxw/index.html
- **目标文件**: `sources/china/finance/forex/bank-forex.json`
- **预估工作量**: 1小时
- **说明**: 月度银行结售汇统计数据
- **认领**: [点击认领Issue](#)

### 📋 7.7 外汇市场交易 (`forex-market`)
- **状态**: 📋 待开始

- **URL**: http://www.chinamoney.com.cn/
- **目标文件**: `sources/china/finance/forex/forex-market.json`
- **预估工作量**: 1.5小时
- **说明**: 外汇交易中心发布的人民币汇率、交易量等数据
- **认领**: [点击认领Issue](#)

---

## 📚 相关资源

### 领域指南
- [金融数据收集指南](../../docs/guides/finance.md)（待创建）
- [权威性评估标准](../../docs/quality-criteria.md)
- [中国金融监管机构列表](../../docs/references/china-financial-regulators.md)（待创建）

### 参考资料
- [中国人民银行统计体系](http://www.pbc.gov.cn/diaochatongjisi/)
- [证监会信息披露](http://www.csrc.gov.cn/csrc/c100028/common_list.shtml)
- [财政部统计数据](http://www.mof.gov.cn/zhengwuxinxi/caizhengshuju/)

---

## 📝 认领说明

1. **选择任务**：在上方找到状态为 📋 的任务
2. **创建Issue**：在GitHub创建认领Issue
   - 标题：`[认领] 数据源ID - 数据源名称`
   - 使用模板：[claim-task.md](../../../.github/ISSUE_TEMPLATE/claim-task.md)
3. **开始工作**：Fork项目，创建分支
4. **参考指南**：查看 [数据收集指南](../../docs/data-collection-guide.md)
5. **提交PR**：完成后提交Pull Request

---

## 🎯 本周目标（Week 2）

- [ ] 完成银行系统剩余5个（目标：7/7 完成）
- [ ] 完成证券市场剩余4个（目标：7/7 完成）
- [ ] 启动债券市场3个

**期待你的加入！** 🚀

---

[← 返回中国数据源总览](README.md) | [返回任务系统首页](../README.md)
