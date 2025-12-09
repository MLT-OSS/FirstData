# 贡献指南

欢迎为 DataSource 项目做出贡献！本指南将帮助您了解如何参与项目开发。

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [认领任务流程](#认领任务流程)
- [数据源收录流程](#数据源收录流程)
- [代码贡献流程](#代码贡献流程)
- [质量标准](#质量标准)
- [提交规范](#提交规范)

---

## 行为准则

我们致力于为所有贡献者提供一个友好、安全和包容的环境。参与本项目即表示您同意：

- 尊重不同观点和经验
- 接受建设性的批评
- 关注对社区最有利的事情
- 对其他社区成员保持同理心

---

## 如何贡献

您可以通过以下方式为项目做出贡献：

### 1. 收录新数据源

这是最直接的贡献方式。查看 [任务清单](../tasks/README.md) 选择待完成的数据源。

### 2. 改进现有数据源

- 更新过时的URL
- 补充缺失的元数据字段
- 改进数据源描述
- 添加使用示例

### 3. 完善文档

- 改进现有文档的清晰度
- 添加示例和教程
- 翻译文档
- 修复拼写和语法错误

### 4. 代码改进

- 修复bug
- 添加新功能
- 改进性能
- 增强测试覆盖率

### 5. 报告问题

- 报告bug
- 提出功能建议
- 报告数据源失效
- 提出改进意见

---

## 认领任务流程

### 步骤 1：选择任务

1. 浏览 [任务清单](../tasks/README.md)
2. 选择一个标记为 📋 **待开始** 的任务
3. 优先选择标记为 ⭐ **P1** 的高优先级任务

### 步骤 2：创建认领Issue

使用 [认领任务模板](../.github/ISSUE_TEMPLATE/claim-task.md) 创建Issue：

```markdown
标题：[认领] datasource-id - 数据源名称
标签：task-claim, help wanted
```

### 步骤 3：等待确认

- 维护者会在24小时内确认
- 确认后，任务状态更新为 🚧 **进行中**

### 步骤 4：完成任务

- 按照 [数据收录指南](data-collection-guide.md) 完成收录
- 确保符合 [质量标准](quality-criteria.md)

### 步骤 5：提交PR

- 创建Pull Request
- 关联认领的Issue
- 等待代码审查

---

## 数据源收录流程

### 1. 数据收集

#### 必需字段（40+字段）

参考 [schemas/datasource.schema.json](../schemas/datasource.schema.json)：

**基本信息**：
- `id`: 唯一标识符（使用kebab-case）
- `name`: 数据源名称
- `name_en`: 英文名称
- `description`: 详细描述
- `url`: 官方URL
- `organization`: 发布机构

**分类信息**：
- `category`: 主类别
- `subcategory`: 子类别
- `tags`: 标签数组

**技术信息**：
- `api_available`: 是否有API
- `api_type`: API类型（REST/GraphQL等）
- `data_formats`: 数据格式数组
- `update_frequency`: 更新频率

**访问信息**：
- `access_type`: 访问类型（open/registration/restricted）
- `license`: 许可证类型
- `cost`: 费用信息

**质量指标**（6 维度）：
- `authority_level`: 来源权威性（1-5）
- `methodology_transparency`: 方法论透明度（1-5）
- `update_timeliness`: 更新及时性（1-5）
- `data_completeness`: 数据完整性（1-5）
- `documentation_quality`: 文档质量（1-5）
- `citation_count`: 引用频次（1-5）

完整字段列表请参考Schema文件。

### 2. 创建JSON文件

在对应目录创建JSON文件，例如：

```
sources/china/finance/banking/pbc.json
```

使用Schema验证：

```bash
python scripts/validate.py sources/china/finance/banking/pbc.json
```

### 3. URL验证

确保所有URL可访问：

```bash
python scripts/verify_urls.py sources/china/finance/banking/pbc.json
```

### 4. 生成索引

运行索引生成脚本：

```bash
python scripts/build_index.py
```

### 5. 更新README

更新对应的一级目录 README 文件，例如 `sources/china/README.md`。

**注意**: 仅在一级目录（china, international, countries, academic, sectors）下维护 README 文件，子目录不需要 README。

---

## 代码贡献流程

### 1. Fork 项目

点击GitHub页面右上角的 "Fork" 按钮。

### 2. 克隆到本地

```bash
git clone https://github.com/YOUR_USERNAME/datasource.git
cd datasource
```

### 3. 创建分支

```bash
git checkout -b feature/datasource-id
# 或
git checkout -b fix/issue-description
```

分支命名规范：
- `feature/` - 新功能
- `fix/` - Bug修复
- `docs/` - 文档改进
- `refactor/` - 代码重构

### 4. 进行修改

- 遵循项目代码风格
- 添加必要的注释
- 更新相关文档
- 添加/更新测试

### 5. 提交更改

```bash
git add .
git commit -m "类型: 简短描述"
```

提交信息格式见 [提交规范](#提交规范)。

### 6. 推送到Fork

```bash
git push origin feature/datasource-id
```

### 7. 创建Pull Request

1. 在GitHub上打开您的Fork
2. 点击 "Compare & pull request"
3. 填写PR描述：
   - 说明更改的内容
   - 关联相关Issue（使用 `Closes #123`）
   - 列出测试步骤
4. 提交PR

### 8. 代码审查

- 维护者会审查您的代码
- 根据反馈进行修改
- 保持沟通和响应

### 9. 合并

- PR通过审查后会被合并
- 感谢您的贡献！

---

## 质量标准

所有贡献都应符合以下质量标准：

### 数据源收录质量

1. **完整性**
   - 必需字段100%完整
   - 推荐字段至少80%完整
   - 描述清晰详细（200字以上）

2. **准确性**
   - URL 100%可访问
   - 信息来源可验证
   - 元数据准确无误

3. **规范性**
   - 严格遵循JSON Schema
   - 通过所有验证测试
   - 文件命名符合规范

详见 [质量评估标准](quality-criteria.md)。

### 代码质量

1. **可读性**
   - 清晰的变量和函数命名
   - 适当的注释
   - 符合PEP 8（Python）或相应语言规范

2. **测试**
   - 新功能必须有测试
   - 测试覆盖率不低于80%
   - 所有测试必须通过

3. **文档**
   - 公共函数有文档字符串
   - 复杂逻辑有解释注释
   - 更新相关文档

---

## 提交规范

### 提交信息格式

```
类型: 简短描述（不超过50字符）

详细描述（可选，72字符换行）

关联Issue: #123
```

### 提交类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### 示例

```
feat: 添加中国人民银行数据源

- 完成40+字段元数据收集
- URL验证通过
- 添加使用示例

Closes #42
```

```
fix: 修复UNESCO数据源URL失效问题

UNESCO官网域名变更，更新所有相关链接。

Closes #128
```

```
docs: 更新数据收录指南

- 添加Schema验证步骤
- 补充URL验证说明
- 增加常见问题解答
```

---

## 常见问题

### Q: 我是新手，应该从哪里开始？

A: 推荐从以下任务开始：
- 标记为 `good-first-issue` 的Issue
- 更新现有数据源的过时信息
- 改进文档和修复拼写错误

### Q: 如何选择数据源收录的优先级？

A: 参考 [ROADMAP.md](../ROADMAP.md) 中的优先级标记：
- ⭐ P1：高优先级
- P2：中优先级
- P3：低优先级

建议优先完成P1任务。

### Q: Schema中的字段太多，都必须填写吗？

A: 分为三类：
- **必需字段**：必须填写
- **推荐字段**：强烈建议填写
- **可选字段**：根据数据源情况填写

详见 [数据收录指南](data-collection-guide.md)。

### Q: 提交PR后多久会得到反馈？

A: 我们努力在48小时内进行初步审查。

### Q: 发现数据源失效怎么办？

A: 创建Issue报告，标签使用 `bug`, `url-broken`。

---

## 获得帮助

如有疑问，可以通过以下方式获得帮助：

- 查看 [文档](../docs/)
- 搜索已有的 [Issues](https://github.com/yourusername/datasource/issues)
- 创建新的Issue提问
- 参考 [FAQ](../docs/FAQ.md)

---

## 致谢

感谢所有为本项目做出贡献的人！

您的贡献将帮助研究者和开发者更容易地找到和使用高质量的数据源。

---

[← 返回首页](../README.md) | [查看任务清单](../tasks/README.md)
