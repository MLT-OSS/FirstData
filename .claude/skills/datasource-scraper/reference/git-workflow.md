# Git 工作流程

完成数据源验证和文档更新后，将更改提交到 Git 仓库并推送到远程。

## 提交前检查清单

**⚠️ 以下所有检查项必须全部完成，否则不允许提交到 Git！**

### ✅ 文件验证（必须全部通过）

- [ ] **Schema 验证通过** - 运行 `validate.py` 无错误
- [ ] **完整性 ≥70%** - 运行 `check_completeness.py` 达标
  - 必需字段: 100%
  - 推荐字段: ≥80%
  - 总体: ≥70%
- [ ] **URL 可访问** - 运行 `verify_urls.py` 或人工确认
  - `primary_url` 必须验证（自动或手动确认）
  - 其他 URL 建议验证

### ✅ 文档更新（必须全部完成）

- [ ] **更新领域 README** - 添加数据源条目到对应 README
- [ ] **任务文件标记完成** - 将 📋 改为 ✅
- [ ] **更新进度统计** - 同步更新以下 5 个文件：
  - [ ] `README.md` (badge + 总体统计表)
  - [ ] `tasks/README.md` (总进度 + 分类表)
  - [ ] `ROADMAP.md` (总进度 + 里程碑)
  - [ ] `sources/{category}/README.md` (已收录数量)
  - [ ] `tasks/china/README.md` (仅中国数据源)

### ✅ 质量检查（必须符合标准）

- [ ] **必需字段完整** - 所有 required 字段有值
- [ ] **双语内容完整** - 中国/国际数据源提供中英双语
- [ ] **评分有据** - 质量评分基于实际观察
- [ ] **分类正确** - 文件保存在正确的目录路径

### ⭕ 索引生成（可选）

- [ ] 测试索引生成 - `generate_indexes.py --test`
- [ ] 新数据源出现在索引中

### ✅ 最终确认（必须检查）

- [ ] **文件保存在正确目录** - 符合分类规则
- [ ] **命名规范** - 使用 datasource ID 作为文件名
- [ ] **无 TODO 占位符** - 没有待填充的占位符

---

## Git 提交流程

### 自动推送模式（默认）

当所有验证通过后，自动提交并推送到远程仓库。

#### 执行步骤

```bash
# 1. 添加所有更改
git add .

# 2. 创建提交（根据操作类型选择消息）
# 新增数据源
git commit -m "feat: 添加{数据源名称}数据源 ({datasource-id})"

# 更新数据源
git commit -m "update: 更新{数据源名称}数据源 ({datasource-id})"

# 批量操作
git commit -m "feat: 批量添加{领域}数据源 ({count}个)"

# 3. 推送到远程仓库
git push origin feat/auto-push-git
```

### 提交消息格式

遵循约定式提交（Conventional Commits）规范：

#### 新增数据源
```
feat: 添加{name} ({id})

- 添加 {organization.name} 数据源
- 覆盖范围：{coverage.geographic.scope}
- 时间跨度：{coverage.temporal.start_year}-{coverage.temporal.end_year}
- 质量评分：{quality.average_score}/5.0
```

**示例**：
```
feat: 添加世界银行开放数据 (worldbank-open-data)

- 添加 World Bank 数据源
- 覆盖范围：全球
- 时间跨度：1960-2024
- 质量评分：4.9/5.0
```

#### 更新数据源
```
update: 更新{name} ({id})

- 更新 API 文档 URL
- 补充数据内容描述
- 更新时间跨度至 {end_year}
```

**示例**：
```
update: 更新中国人民银行 (china-pbc)

- 更新 API 文档 URL
- 补充贷款市场报价利率数据
- 更新时间跨度至 2024
```

#### 批量操作
```
feat: 批量添加{领域}数据源 ({count}个)

- {datasource-1}: {organization-1}
- {datasource-2}: {organization-2}
- {datasource-3}: {organization-3}
```

**示例**：
```
feat: 批量添加金融监管数据源 (3个)

- china-pbc: 中国人民银行
- china-nfra: 国家金融监督管理总局
- china-csrc: 中国证监会
```

---

## 触发条件

自动推送在以下情况触发：

1. **新数据源创建成功**
   - Schema 验证通过
   - URL 可访问性验证通过
   - 完整性检查达标
   - 所有文档更新完成

2. **数据源更新完成**
   - 更新验证通过
   - 备份文件已创建
   - 文档同步更新

3. **索引文件生成**
   - 新数据源出现在索引中
   - 统计数据更新

---

## 注意事项

### 推送前确认

- ✅ 所有验证通过（3 项验证 + 提交检查清单）
- ✅ 提交消息描述清晰
- ✅ 推送到正确的分支（默认：`feat/auto-push-git`）

### 分支管理

**默认分支**：`feat/auto-push-git`

如需更改分支，在提交前先切换：
```bash
git checkout -b your-branch-name
git push origin your-branch-name
```

### 冲突处理

如果推送失败（远程有更新），先拉取合并：
```bash
git pull --rebase origin feat/auto-push-git
git push origin feat/auto-push-git
```

---

## 常见问题

### Q1: 提交后发现错误怎么办？
**A**: 使用 `git commit --amend` 修改最后一次提交，或创建新的修复提交。

### Q2: 可以手动提交而不使用自动推送吗？
**A**: 可以。在完成所有验证后，手动执行 git add、commit、push 命令。

### Q3: 如何查看当前分支？
**A**: 运行 `git branch` 或 `git status`。

### Q4: 推送失败显示 "rejected" 怎么办？
**A**: 远程仓库有新提交。先运行 `git pull --rebase` 合并更新，再推送。

### Q5: 提交消息写错了可以修改吗？
**A**: 如果还没推送，使用 `git commit --amend` 修改。如果已推送，不建议修改（会导致历史不一致）。
