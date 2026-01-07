---
description: 自动推送并使用 glab 创建 Merge Request
allowed-tools: Bash(git push:*), Bash(git branch:*), Bash(git log:*), Bash(git diff:*), Bash(git status:*), Bash(git rev-parse:*), Bash(git config:*), Bash(git remote:*), Bash(git merge-base:*), Bash(which:*), Bash(glab:*), Bash(python3:*), Read, AskUserQuestion
argument-hint: [target_branch]
model: sonnet
category: git
---
## 功能说明

自动化 Merge Request 创建流程，包括：

1. 推送当前分支到远程仓库
2. 智能分析远程主要分支（main/master/develop/alpha/beta 等）
3. 根据当前分支名称推荐最可能的目标分支
4. 让用户选择目标分支（或使用提供的参数）
5. **正确计算** commit 增量（使用 merge-base 找共同祖先）
6. 分析提交历史并生成 MR 的 title 和 description
7. **展示 MR 预览并请求用户确认**
8. **优先使用 glab CLI** 直接创建 MR（降级到 Web 链接）

## 参数说明

- `[target_branch]` - 可选参数，指定目标分支名称
  - 如果提供：直接使用该分支作为目标分支（会校验分支是否存在）
  - 如果不提供：通过 AskUserQuestion 让用户选择目标分支

## 执行步骤

### 第一步: 推送当前分支到远程

1. 获取当前分支名称：`git rev-parse --abbrev-ref HEAD`
2. 推送到远程同名分支：`git push origin <current_branch>`
3. 捕获推送输出，提取 Merge Request 创建链接（如果有）

### 第二步: 处理目标分支参数

**如果用户提供了 `target_branch` 参数**：

1. 获取所有远程分支：`git branch -r`
2. 校验提供的分支是否存在于远程：
   ```bash
   git branch -r | grep -q "origin/$target_branch"
   ```
3. 如果分支存在：直接使用该分支，跳过第三步和第四步
4. 如果分支不存在：提示错误并列出可用的主要分支
   ```
   ❌ 错误：远程分支 '$target_branch' 不存在

   可用的主要分支：
   - develop
   - main
   - staging

   请使用正确的分支名称重新运行命令。
   ```

**如果用户未提供参数**：
继续执行第三步和第四步

### 第三步: 分析远程分支（仅当未提供参数时）

1. 获取所有远程分支：`git branch -r`
2. 过滤出主要分支：
   - `main`, `master` - 主分支
   - `develop`, `dev` - 开发分支
   - `alpha`, `beta` - 预发布分支
   - `staging`, `production` - 环境分支
3. 按优先级排序（develop > main > master > staging > alpha > beta > production）

### 第四步: 推荐目标分支（仅当未提供参数时）

根据当前分支名称前缀智能推荐：

| 分支前缀                           | 推荐目标分支 | 理由                       |
| ---------------------------------- | ------------ | -------------------------- |
| `feat/`, `feature/`            | develop      | 新功能通常先合并到开发分支 |
| `fix/`, `bugfix/`, `hotfix/` | develop      | Bug 修复优先到开发分支     |
| `refactor/`                      | develop      | 重构代码通常到开发分支     |
| `test/`                          | develop      | 测试相关到开发分支         |
| `docs/`                          | develop      | 文档更新到开发分支         |
| `release/`                       | main/master  | 发布分支合并到主分支       |
| `hotfix/` (紧急)                 | main/master  | 紧急修复可能直接到主分支   |
| 其他                               | develop      | 默认推荐开发分支           |

**推荐逻辑**：

1. 如果当前分支是 `release/*` 或 `hotfix/*`（且有 main/master 分支），优先推荐 main/master
2. 否则优先推荐 develop（如果存在）
3. 如果没有 develop，推荐 main 或 master
4. 将推荐的分支放在选项列表首位，并标注 "(推荐)"

### 第五步: 用户选择目标分支（仅当未提供参数时）

使用 `AskUserQuestion` 工具：

- **问题**: "你想要将 `<current_branch>` 合并到哪个分支?"
- **header**: "目标分支"
- **multiSelect**: false
- **options**: 列出所有主要分支，推荐的分支在第一位并加 "(推荐)" 标识

### 第六步: 分析提交历史并生成 MR 内容

**CRITICAL**: 必须使用 `git merge-base` 找到正确的共同祖先，避免计算错误的 commit 数量。

1. **找到共同祖先**：

   ```bash
   # 获取两个分支的共同祖先 commit
   BASE_COMMIT=$(git merge-base origin/<target_branch> origin/<current_branch>)
   ```
2. **获取提交范围**（从共同祖先到当前分支）：

   ```bash
   # 正确的方式：从共同祖先开始计算
   git log $BASE_COMMIT..origin/<current_branch> --oneline

   # ❌ 错误方式（会包含已合并的 commit）：
   # git log origin/<target_branch>..origin/<current_branch> --oneline
   ```
3. **分析改动统计**：

   ```bash
   git diff origin/<target_branch>...origin/<current_branch> --shortstat
   ```
4. **生成 Title**：

   - 如果只有 1 个提交：直接使用该提交的 message
   - 如果有多个提交：
     - 分析所有提交的 type（feat/fix/refactor 等）
     - 如果 type 一致，使用 `<type>(<scope>): <综合描述>`
     - 如果 type 混合，使用通用格式：`<主要type>: <分支功能描述>`
   - 最多 80 字符
5. **生成 Description**（Markdown 格式）：

   ```markdown
   ## 概述
   [分支的整体功能描述，基于分支名称和提交历史]

   ## 主要改进

   ### [模块/功能分类 1]
   - 改进点 1
   - 改进点 2

   ### [模块/功能分类 2]
   - 改进点 1
   - 改进点 2

   ## 技术细节
   [可选：如果有显著的技术实现亮点，简洁描述关键技术点]
   ```

### 第七步: 展示 MR 预览并请求用户确认

在创建 MR 前，必须向用户展示完整的预览信息并等待确认。

**展示内容格式**：

```
📋 Merge Request 预览

源分支: feat/tool-system-arch
目标分支: develop
提交数量: 1 commit
文件改动: 7 files changed, 1349 insertions(+), 1191 deletions(-)

─────────────────────────────────────
Title:
refactor(tools): 优化 AgentLoader 配置解析和测试稳定性

─────────────────────────────────────
Description:
## 概述
...（完整的 description 内容）...

─────────────────────────────────────
```

**用户确认**：

使用 `AskUserQuestion` 工具：

- **问题**: "是否创建此 Merge Request?"
- **header**: "确认创建"
- **multiSelect**: false
- **options**:
  1. "创建 MR" (description: "使用上述信息创建 Merge Request")
  2. "取消" (description: "放弃创建，不做任何操作")

如果用户选择"取消"，则终止流程并提示：

```
ℹ️  已取消创建 Merge Request
```

### 第八步: 创建 Merge Request

根据系统环境和 Git 平台，选择最佳创建方式：

#### 方式 1: 使用 glab CLI（推荐，GitLab 专用）

**检测 glab**：

```bash
which glab
```

如果 glab 已安装且远程是 GitLab，**优先使用** glab 创建 MR：

```bash
glab mr create \
  --source-branch <current_branch> \
  --target-branch <target_branch> \
  --title "<title>" \
  --description "<description>" \
  --yes
```

**优势**：

- ✅ 自动创建 MR，无需手动操作
- ✅ 自动填充 title 和 description
- ✅ 返回 MR 链接
- ✅ 支持更多参数（assignee, label, milestone 等）

**成功输出格式**：

glab 会返回 MR 链接（第一行），必须提取并清晰展示给用户：

```
✅ Merge Request 创建成功！

🔗 MR 链接: https://code.mlamp.cn/mlt-oss/opencc/-/merge_requests/48

合并信息：
- 源分支: feat/tool-system-arch
- 目标分支: develop
- 提交数量: 1 commit
- 文件改动: 7 files changed, 1349 insertions(+), 1191 deletions(-)

💡 提示：
- 点击链接查看 MR 详情
- 建议检查 CI/CD pipeline 状态
- 确保所有检查通过后再请求 review
```

**提取 MR 链接的方法**：

glab 的输出格式：

```
https://code.mlamp.cn/mlt-oss/opencc/-/merge_requests/48

Creating merge request for feat/tool-system-arch into develop in mlt-oss/opencc
```

链接在第一行，可以这样提取：

```bash
# 执行 glab 并捕获输出
output=$(glab mr create ... 2>&1)

# 提取第一行（MR 链接）
mr_url=$(echo "$output" | head -n1)

# 展示给用户
echo "✅ Merge Request 创建成功！"
echo ""
echo "🔗 MR 链接: $mr_url"
```

#### 方式 2: 生成 Web 链接（降级方案）

如果 glab 未安装或不适用，根据 Git 远程仓库类型生成不同格式的链接：

**GitLab 格式**（如 code.mlamp.cn）：

```
<gitlab_url>/-/merge_requests/new?merge_request[source_branch]=<current_branch>&merge_request[target_branch]=<target_branch>&merge_request[title]=<url_encoded_title>
```

**检测方法**：

- 检查 `git remote get-url origin`
- 如果包含 `gitlab` 或已知 GitLab 域名（如 `code.mlamp.cn`）

**GitHub 格式**：

```
<github_url>/compare/<target_branch>...<current_branch>?expand=1&title=<url_encoded_title>
```

**检测方法**：

- 如果远程 URL 包含 `github.com`

**其他平台**：

- 提供基础的推送信息和手动创建 MR 的提示

**URL 编码规则**：

- Title 需要进行 URL 编码（空格 → `%20`，中文 → UTF-8 编码，冒号 → `%3A`）
- 使用 Python：`python3 -c "import urllib.parse; print(urllib.parse.quote('<title>'))")`

**Web 链接方式的输出**：

```
✅ 代码已成功推送到远程仓库！

**Merge Request 创建链接：**
<完整的 MR 创建链接>

💡 提示：
- 链接已包含 title，点击后可直接创建 MR
- Description 需要手动复制粘贴到 MR 描述框中
```

## 特殊场景处理

### 场景 1: 当前分支已推送到远程

- 检查远程分支是否存在：`git branch -r | grep origin/<current_branch>`
- 如果存在，使用 `git push origin <current_branch>` 更新
- 如果不存在，使用 `git push -u origin <current_branch>` 创建并跟踪

### 场景 2: 没有远程主要分支

- 如果远程只有当前分支，提示用户：

```

  ⚠️  未检测到远程主要分支（main/develop 等）
  无法创建 Merge Request，请先设置主分支或手动指定目标分支。

```

### 场景 3: 推送失败

- 捕获错误信息并展示给用户
- 常见原因：
  - 没有推送权限
  - 分支保护规则
  - 网络问题
- 提供解决建议

### 场景 4: 无提交差异

- 检查是否有新的提交：`git log <target_branch>..<current_branch>`
- 如果没有差异，提示：

```

  ℹ️  当前分支与目标分支没有差异，无需创建 Merge Request

```

## 使用示例

### 示例 1: 使用 glab（推荐方式）

```bash
# 在功能分支上
git checkout feat/user-authentication

# 执行命令，指定目标分支
/merge-request develop

# 流程：
# 1. 推送代码到远程
# 2. 分析提交历史（使用 merge-base 正确计算）
# 3. 生成 Title 和 Description
# 4. 展示预览：
#    📋 Merge Request 预览
#    源分支: feat/user-authentication
#    目标分支: develop
#    提交数量: 1 commit
#    ...
# 5. 询问用户确认："是否创建此 Merge Request?"
# 6. 用户选择 "创建 MR"
# 7. 使用 glab 自动创建

# 输出：
# ✅ Merge Request 创建成功！
#
# 🔗 MR 链接: https://code.mlamp.cn/mlt-oss/opencc/-/merge_requests/48
#
# 合并信息：
# - 源分支: feat/user-authentication
# - 目标分支: develop
# - 提交数量: 1 commit
# - 文件改动: 5 files changed, 320 insertions(+), 10 deletions(-)
#
# 💡 提示：
# - 点击链接查看 MR 详情
# - 建议检查 CI/CD pipeline 状态
```

### 示例 2: 不带参数（交互式选择目标分支）

```bash
# 执行命令，不提供参数
/merge-request

# 流程：
# 1. 系统分析并推荐目标分支：
#    - develop (推荐)
#    - main
#    - staging
# 2. 用户选择目标分支
# 3. 其余流程同示例 1
```

### 示例 3: 用户取消创建

```bash
/merge-request develop

# 流程：
# 1-4. 正常执行，展示预览
# 5. 询问确认时，用户选择 "取消"

# 输出：
# ℹ️  已取消创建 Merge Request
```

### 示例 4: 降级到 Web 链接（glab 未安装）

```bash
# 如果系统没有安装 glab
/merge-request develop

# 流程：
# 1-6. 正常执行并确认
# 7. 检测到 glab 未安装
# 8. 生成 Web 链接

# 输出：
# ✅ 代码已成功推送到远程仓库！
#
# **Merge Request 创建链接：**
# https://code.mlamp.cn/mlt-oss/opencc/-/merge_requests/new?...
#
# 💡 提示：
# - 链接已包含 title，点击后可直接创建 MR
# - Description 需要手动复制粘贴到 MR 描述框中
```

## 最佳实践

1. **在推送前确保本地测试通过**

   - 运行测试：`npm test` 或 `pytest`
   - 确保代码格式化：`npm run lint`
2. **Commit message 规范**

   - 使用 `/commit` 命令生成规范的 commit message
   - 规范的 commit message 有助于生成更好的 MR title
3. **及时同步目标分支**

   - 在创建 MR 前，先 rebase 或 merge 目标分支
   - 减少合并冲突
4. **Review Description**

   - 自动生成的 description 可能需要微调
   - 添加 screenshots、breaking changes 等额外信息

## 技术实现细节

### URL 编码实现

使用 Python 进行 URL 编码：

```python
import urllib.parse

title = "feat(auth): 添加用户身份验证功能"
encoded_title = urllib.parse.quote(title)
# 结果: feat%28auth%29%3A+%E6%B7%BB%E5%8A%A0%E7%94%A8%E6%88%B7%E8%BA%AB%E4%BB%BD%E9%AA%8C%E8%AF%81%E5%8A%9F%E8%83%BD
```

或使用 Bash：

```bash
# macOS/Linux
echo "feat(auth): 添加用户身份验证功能" | jq -sRr @uri

# 或使用 python 单行命令
python3 -c "import urllib.parse; print(urllib.parse.quote('feat(auth): 添加用户身份验证功能'))"
```

### Git 远程 URL 解析

```bash
# 获取远程 URL
git remote get-url origin
# 输出示例:
# - git@code.mlamp.cn:mlt-oss/opencc.git
# - https://code.mlamp.cn/mlt-oss/opencc.git
# - git@github.com:user/repo.git

# 解析为 Web URL
# GitLab: https://code.mlamp.cn/mlt-oss/opencc
# GitHub: https://github.com/user/repo
```

### 提交历史分析示例（使用 merge-base）

```bash
# ❌ 错误方式：直接比较分支
git log origin/develop..origin/feat/tool-system-arch --oneline
# 可能输出：
# 8698b45 refactor(tools): 优化 AgentLoader 配置解析和测试稳定性
# c3333d2 refactor(tools): 重构 MCP loader 实现并发控制和重试机制
# 问题：c3333d2 已经在 develop 分支中，不应该计入

# ✅ 正确方式：使用 merge-base
BASE=$(git merge-base origin/develop origin/feat/tool-system-arch)
git log $BASE..origin/feat/tool-system-arch --oneline
# 正确输出（只有实际的增量）：
# 8698b45 refactor(tools): 优化 AgentLoader 配置解析和测试稳定性

# 验证 merge-base
echo "共同祖先: $BASE"
git log -1 --oneline $BASE
# c3333d2 refactor(tools): 重构 MCP loader 实现并发控制和重试机制
```

### glab CLI 使用示例

```bash
# 检测 glab
which glab
# /opt/homebrew/bin/glab

# 创建 MR（带 heredoc 避免转义问题）
glab mr create \
  --source-branch feat/tool-system-arch \
  --target-branch develop \
  --title "refactor(tools): 优化工具系统架构和并发控制" \
  --description "$(cat <<'EOF'
## 概述
本 MR 对工具系统进行优化...
EOF
)" \
  --yes

# glab 原始输出：
# https://code.mlamp.cn/mlt-oss/opencc/-/merge_requests/48
#
# Creating merge request for feat/tool-system-arch into develop in mlt-oss/opencc

# 应该向用户展示的输出：
# ✅ Merge Request 创建成功！
#
# 🔗 MR 链接: https://code.mlamp.cn/mlt-oss/opencc/-/merge_requests/48
#
# 合并信息：
# - 源分支: feat/tool-system-arch
# - 目标分支: develop
# - 提交数量: 1 commit
# - 文件改动: 7 files changed, 1349 insertions(+), 1191 deletions(-)
```

## 注意事项

1. **权限要求**

   - 需要对远程仓库有推送权限
   - 需要有创建 Merge Request 的权限
2. **分支命名建议**

   - 使用规范的分支前缀（feat/, fix/, refactor/ 等）
   - 有助于系统智能推荐目标分支
3. **CI/CD 集成**

   - 创建 MR 后，检查 CI/CD pipeline 状态
   - 确保所有检查通过后再请求 review
