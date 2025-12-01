---
name: 认领数据源收录任务
about: 认领一个数据源的收录任务
title: '[认领] 数据源ID - 数据源名称'
labels: 'task-claim, help wanted'
assignees: ''
---

## 📋 任务信息

**数据源ID**: `your-datasource-id`
**数据源名称**: Your DataSource Name
**所属领域**: 选择领域（如：国际组织/中国-金融财政/美国等）
**任务清单**: [链接到具体任务清单](../tasks/...)
**目标文件路径**: `sources/.../your-datasource-id.json`

---

## ✅ 认领人信息

**认领人**: @your-github-username
**预计完成时间**: YYYY-MM-DD
**联系方式**（可选）:

---

## 📝 工作计划

简要说明你的工作计划：

- [ ] 访问数据源官方网站，确认可访问性
- [ ] 收集元数据信息（机构、描述、覆盖范围等）
- [ ] 评估数据源质量（权威性、透明度、完整性等）
- [ ] 按照模板创建JSON文件
- [ ] 本地运行验证脚本 `python scripts/validate.py sources/path/to/file.json`
- [ ] 提交Pull Request

---

## 🔗 相关资源

请在开始前阅读以下文档：

- [数据收集指南](../../docs/data-collection-guide.md)
- [元数据标准](../../docs/metadata-standard.md)
- [权威性评估标准](../../docs/quality-criteria.md)
- [JSON Schema示例](../../schemas/examples/)

---

## ❓ 问题和疑虑

如果你在收录过程中遇到任何问题，请在下方评论区提问。

---

## 📌 注意事项

- ✅ 确保数据源符合[收录标准](../../PRD.md#41-收录范围)
- ✅ 所有必填字段必须完整填写
- ✅ URL必须可访问（建议运行 `scripts/check-urls.py`）
- ✅ 权威性评分需要基于客观标准
- ✅ 提交前必须通过本地验证（`scripts/validate.py`）

---

**认领后请将任务清单中的状态更新为 🚧（进行中）**
