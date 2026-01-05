# 完整工作流程示例

本文档提供端到端的工作流程示例，展示从用户输入到最终完成的完整步骤。

---

## 示例 1：标准流程 - 使用 Web Search + WebFetch

### 场景
用户提供一个国际组织数据源的名字，需要抓取信息并创建数据源文件。

### 用户输入
```
世界卫生组织数据
```

### 完整流程

#### 步骤 1：获取网站内容
**参考**: [data-acquisition.md](data-acquisition.md)

**操作**：
1. 识别输入类型：名字输入
2. 使用 WebSearch 搜索：`"World Health Organization data"`
3. 找到官方数据门户：`https://www.who.int/data`
4. 使用 AskUserQuestion 确认 URL
5. 使用 WebFetch 访问页面，提取信息：
   - 组织名称：World Health Organization
   - 描述：全球健康数据和统计
   - API：有，文档链接
   - 数据类别：疾病监测、健康指标、疫苗覆盖率等

#### 步骤 2：信息提取
**参考**: [information-extraction.md](information-extraction.md)

**操作**：
1. 填充基础信息：
   - `id`: `who-data`
   - `name.en`: `WHO Global Health Observatory`
   - `name.zh`: `世界卫生组织全球健康观测站`
   - `organization.type`: `international_organization`

2. 填充访问信息：
   - `primary_url`: `https://www.who.int/data/gho`
   - `api.available`: `true`
   - `access_level`: `open`

3. 填充覆盖范围：
   - `geographic.scope`: `global`
   - `temporal.start_year`: `2000`
   - `temporal.update_frequency`: `monthly`

4. 填充数据内容（中英双语）

#### 步骤 3：质量评估
**参考**: [quality-criteria.md](quality-criteria.md)

**操作**：
1. 评估 6 个维度：
   - `authority_level`: 5（国际组织，健康领域最高权威）
   - `methodology_transparency`: 5（完整公开方法论）
   - `update_timeliness`: 4（每月更新）
   - `data_completeness`: 5（全球覆盖，20+ 年历史）
   - `documentation_quality`: 5（完整文档、API 示例、用户指南）
   - `citation_count`: 5（广泛引用）

#### 步骤 4-5：生成 JSON & Upsert 操作
**参考**: [upsert-workflow.md](upsert-workflow.md)

**操作**：
1. 生成完整的 JSON 数据
2. 检测现有数据源：未找到
3. 使用 `@datasource-classifier` 确定路径：
   - 推荐：`sources/international/health/who.json`
4. 创建新文件

#### 步骤 6：验证
**参考**: [validation-guide.md](validation-guide.md)

**操作**：
1. Schema 验证：✅ 通过
2. URL 可访问性验证：✅ 通过
3. 完整性检查：92% ✅ 达标

#### 步骤 7：生成索引
```bash
python scripts/generate_indexes.py --test sources/international/health/who.json
```

#### 步骤 8：更新文档
**参考**: [documentation-update.md](documentation-update.md)

**操作**：
1. 更新 `sources/international/README.md`
2. 更新 `tasks/international.md`（📋 → ✅）
3. 更新进度统计（5 个文件）

#### 步骤 9-10：Git 提交
**参考**: [git-workflow.md](git-workflow.md)

**操作**：
1. 完成提交前检查清单
2. 执行 git 提交：
   ```bash
   git add .
   git commit -m "feat: 添加世界卫生组织全球健康观测站数据源 (who-data)"
   git push origin feat/auto-push-git
   ```

#### 输出报告
**参考**: [reporting-format.md](reporting-format.md)

```
✅ 已创建 sources/international/health/who.json

📁 数据源 ID: who-data
🏢 组织: World Health Organization (international_organization)
⭐ 平均质量评分: 4.8/5.0
🔗 主要 URL: https://www.who.int/data/gho
🌍 覆盖范围: 全球, 194 个国家
📅 时间跨度: 2000-2024
📊 数据格式: CSV, JSON, Excel
🔓 访问类型: 开放访问

✅ Schema 验证: 通过
✅ URL 可访问性: 通过
✅ 完整性检查: 92% (达标)

主要数据内容：
- 疾病监测数据 - 传染病、慢性病发病率和死亡率
- 健康系统指标 - 医疗资源、卫生支出、服务覆盖率
- 人口健康指标 - 预期寿命、婴儿死亡率、孕产妇健康
- 疫苗接种数据 - 疫苗覆盖率、免疫计划监测
```

---

## 示例 2：复杂流程 - 使用 Playwright

### 场景
用户提供一个使用 JavaScript 动态加载的数据源网站，需要使用浏览器工具提取信息。

### 用户输入
```
https://data.example.com
```

### 完整流程

#### 步骤 1：获取网站内容
**参考**: [data-acquisition.md](data-acquisition.md)

**操作**：

**第一层尝试 - Web Search + WebFetch**：
1. 使用 WebFetch 访问：`https://data.example.com`
2. 返回内容：几乎空白（< 500 字符）
3. 检测到：`<div id="root"></div>`（React SPA）
4. **判断**：需要降级到 Playwright

**第二层 - Playwright 浏览器自动化**：
1. 告知用户：
   ```
   ⚠️ 检测到访问困难，需要使用浏览器工具

   【遇到的问题】: 该页面使用 React 框架，内容完全由 JavaScript 动态加载。
   WebFetch 只能获取到页面骨架，无法看到实际的数据目录和 API 文档。

   【解决方案】: 使用 Playwright 浏览器工具，等待 JavaScript 执行完成后提取内容

   【需要您的协助】: 通常不需要您的操作，我会自动等待页面加载完成

   【继续操作】: 现在开始使用浏览器工具...
   ```

2. 执行 Playwright 流程：
   - `browser_navigate({ url: "https://data.example.com" })`
   - `browser_wait_for({ time: 3 })` - 等待 React 渲染
   - `browser_snapshot()` - 获取渲染后的内容
   - `browser_evaluate({ function: "..." })` - 提取数据
   - `browser_take_screenshot({ filename: "final-state.png" })`
   - `browser_close()`

3. 反馈给用户：
   ```
   ✅ Playwright 提取完成

   📊 已获取以下信息：
   - ✅ 组织名称: Example Data Initiative
   - ✅ 描述: Open data platform for research...
   - ✅ API 文档: https://data.example.com/api-docs
   - ✅ 数据类别: 15 个
   - ✅ 更新频率: monthly
   - ✅ 许可协议: CC BY 4.0

   接下来将使用这些信息填充 JSON schema...
   ```

#### 步骤 2-10：后续步骤
与示例 1 相同，参考对应的 reference 文档。

---

## 示例 3：更新现有数据源

### 场景
用户想更新已存在的数据源（如中国人民银行），补充新增的 API 文档链接。

### 用户输入
```
更新中国人民银行数据源
```

### 关键步骤（Upsert 流程）
**参考**: [upsert-workflow.md](upsert-workflow.md)

**操作**：

#### 步骤 1-4：正常执行获取和信息提取
生成新的 JSON 数据（包含新的 API 文档链接）

#### 步骤 5：Upsert 操作（检测到已存在）
1. 检测现有数据源：✅ 找到 `sources/china/finance/banking/pbc.json`
2. **创建备份**：`pbc.json.backup`
3. **智能合并**：
   - 更新 `access.api.documentation`（新 URL）
   - 更新 `coverage.temporal.end_year`（2024）
   - **保留** `quality.*`（所有质量评分）
   - 合并 `tags`（去重）
   - 更新 `catalog_metadata.last_updated`
4. **验证**：合并结果通过 schema 验证
5. **保存更新**

#### 输出报告
**参考**: [reporting-format.md](reporting-format.md)

```
✅ 已更新 sources/china/finance/banking/pbc.json

📊 变更摘要：

【更新字段】(3个):
  * access.api.documentation: http://www.pbc.gov.cn/api/old → https://www.pbc.gov.cn/openapi/docs
  * coverage.temporal.end_year: 2023 → 2024
  * catalog_metadata.last_updated: 2024-10-15 → 2024-12-10

【保留字段】:
  * quality.authority_level: 5.0
  * quality.methodology_transparency: 4.8
  * quality.update_timeliness: 4.9
  * quality.data_completeness: 4.7
  * quality.documentation_quality: 4.6
  * quality.citation_count: 5.0
  * catalog_metadata.contributor: "mlamp"
  * catalog_metadata.added_date: "2024-09-20"

【数组合并】:
  * tags: 新增 ["LPR", "贷款利率"]
  * data_content: 保持原有 8 个类别

【备份位置】: pbc.json.backup

✅ Schema 验证: 通过
✅ URL 可访问性: 通过
✅ 完整性检查: 94% (达标)
```

---

## 流程对照表

| 步骤 | 对应文档 | 主要操作 |
|-----|---------|---------|
| 1. 获取网站内容 | [data-acquisition.md](data-acquisition.md) | Web Search + WebFetch 或 Playwright |
| 2. 信息提取 | [information-extraction.md](information-extraction.md) | 填充 JSON 字段 |
| 3. 质量评估 | [quality-criteria.md](quality-criteria.md) | 6 维度评分 |
| 4. 生成 JSON | [information-extraction.md](information-extraction.md) | 生成完整 JSON |
| 5. Upsert 操作 | [upsert-workflow.md](upsert-workflow.md) | 检测 → 创建/更新 |
| 6. 验证 | [validation-guide.md](validation-guide.md) | 三项验证 |
| 7. 生成索引 | - | generate_indexes.py |
| 8. 更新文档 | [documentation-update.md](documentation-update.md) | README + 任务清单 + 进度统计 |
| 9-10. Git 提交 | [git-workflow.md](git-workflow.md) | 检查清单 + 提交推送 |

---

## 常见变体

### 变体 1：需要登录的数据源
**操作**：在步骤 1 使用 Playwright，检测登录页面，提示用户手动登录，等待登录完成后继续。
**详见**：[data-acquisition.md - 场景 2](data-acquisition.md#场景-2-需要登录的数据门户)

### 变体 2：交互式菜单的数据源
**操作**：在步骤 1 使用 Playwright，点击展开菜单，提取隐藏内容。
**详见**：[data-acquisition.md - 场景 3](data-acquisition.md#场景-3-交互式数据目录)

### 变体 3：批量添加多个数据源
**操作**：对每个数据源重复完整流程，最后生成批量操作报告。
**详见**：[reporting-format.md - 批量操作报告](reporting-format.md#批量操作报告)

---

## 快速参考

### 当遇到困难时
- **WebFetch 返回空白** → 参考 [data-acquisition.md](data-acquisition.md) 使用 Playwright
- **字段不知道如何填** → 参考 [information-extraction.md](information-extraction.md)
- **质量评分不确定** → 参考 [quality-criteria.md](quality-criteria.md)
- **验证失败** → 参考 [validation-guide.md](validation-guide.md)
- **不知道保存到哪个目录** → 参考 [upsert-workflow.md](upsert-workflow.md)
- **文档更新不完整** → 参考 [documentation-update.md](documentation-update.md)
- **Git 提交前检查** → 参考 [git-workflow.md](git-workflow.md)
