---
allowed-tools: Bash, AskUserQuestion
description: 根据 git add 的内容生成符合规范的 commit message
argument-hint:
category: git
---

**重要提示**: 生成 commit message 时，不要添加以下内容：
- `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
- `Co-Authored-By: Claude <noreply@anthropic.com>`

## 功能说明

自动分析已暂存的 git 改动,根据内置规范生成 commit message,并在用户确认后执行提交。

## 执行步骤

1. 运行 `git status` 检查是否有已暂存的改动
2. 运行 `git diff --staged` 获取暂存区的具体改动内容
3. 分析改动内容,判断改动类型、影响范围和是否存在破坏性变更
4. 严格按照以下规范生成 commit message (**必须只使用一个 type**)
5. **展示生成的 commit message 给用户确认**
6. 使用 AskUserQuestion 工具询问用户是否确认提交
7. 如果用户确认,执行 `git commit -m "生成的commit message"`
8. 如果用户拒绝,询问是否需要重新生成或手动修改

## Git Commit 规范

你将作为 git commit message 生成器。接收 git diff 后,只输出 commit message,不输出任何解释、问题或额外评论。

### 一、Commit 类型（type）

**type 为必填项**，用于明确标识提交的变更类型。

#### 1. 主要类型（优先使用）

- **feat**：新增功能
- **fix**：修复缺陷

#### 2. 辅助类型

- **docs**：文档变更（仅修改文档内容）
- **style**：代码格式调整（不影响代码逻辑,如空格、缩进、分号等）
- **refactor**：代码重构（既不新增功能也不修复缺陷）
- **perf**：性能优化
- **test**：测试相关（新增或修正测试用例）
- **build**：构建系统或外部依赖变更（如 webpack、npm）
- **ci**：CI/CD 配置文件或脚本变更
- **revert**：代码回滚（执行 git revert 时使用）

**使用原则**：

- 每次提交只使用一个类型
- 当一次提交同时包含主要类型和辅助类型时，优先使用主要类型
- 例如：同时包含新功能和文档更新时，使用 `feat`

### 二、影响范围（scope）

**scope 为必填项**，用于描述变更影响的模块。

**格式**：`模块名`

**示例**：

- `common` - 公共模块
- `activity` - 活动模块
- `auth` - 认证模块
- `utils` - 工具类
- `proxy` - 代理服务
- `visualizer` - 可视化工具

**确定 scope 的方法**：

- 根据文件路径确定模块名称
- 如果改动涉及多个模块，选择主要影响的模块
- 如果是全局性改动，使用 `global` 或 `all`

### 三、简短描述（subject）

**格式要求**：

- 使用祈使语气，例如："添加"而非"添加了"
- 不大写首字母
- 不加句号
- 最多 50 字符
- 必须使用中文
- 准确描述改动的核心内容
- 不要包含vibe coding方法论的信息，如更新openspec的文档

**示例**：

- ✅ `优化服务器端口配置逻辑`
- ✅ `修复用户登录超时问题`
- ❌ `优化了服务器端口配置逻辑。` (有句号、过去式)
- ❌ `Fix server port config` (使用英文)

### 四、详细描述（body）

**填写要求**：

- 使用 "-" 开头的要点列表
- 每行最多 72 字符
- 必须使用中文
- 详细说明变更前的情况和修改动机
- 小型修改可选填
- **重大需求、功能更新等必须添加 body 说明**

**示例**：

```text
- 将端口变量重命名为大写(PORT),遵循常量命名规范
- 添加环境变量端口支持以实现灵活部署
- 修复端口冲突时的错误提示信息
```

### 五、破坏性变更（breaking changes）

必须明确标注是否存在破坏性变更。

如存在破坏性变更，在 body 末尾添加空行后，使用以下格式：

```text
BREAKING CHANGE: <详细说明破坏性变更的内容和影响>
```

**需要标注的场景**：

- 版本升级（导致不兼容的）
- 接口参数变更或删除
- API 废弃或迁移
- 配置文件格式变更
- 其他可能影响现有功能的重大调整

**示例**：

```text
BREAKING CHANGE: 删除了旧版 API v1 端点,所有客户端需迁移到 v2
```

### 六、输出格式

**严格禁止**:

❌ **禁止在一次 commit 中使用多个 type 块**
❌ **禁止输出多个 `<type>(<scope>): <subject>` 行**

**标准格式**：

```text
<type>(<scope>): <subject>

<body>
```

**包含破坏性变更时**：

```text
<type>(<scope>): <subject>

<body>

BREAKING CHANGE: <breaking change description>
```

### 七、完整示例

#### 示例 1：新功能

```text
feat(proxy): 添加流式响应解析功能

- 实现 StreamParser 类用于解析 SSE 格式的流式响应
- 支持提取流式响应中的工具调用信息
- 添加错误处理和日志记录
```

#### 示例 2：Bug 修复

```text
fix(auth): 修复 token 过期后无法刷新的问题

- 在 token 过期前 5 分钟自动触发刷新
- 添加刷新失败的重试机制(最多 3 次)
- 修复并发请求时的竞态条件
```

#### 示例 3：破坏性变更

```text
feat(config): 重构配置文件格式

- 将配置文件从 JSON 迁移到 YAML 格式
- 支持环境变量插值
- 添加配置验证和默认值

BREAKING CHANGE: 配置文件格式从 config.json 改为 config.yaml,需要手动迁移现有配置
```

#### 示例 4：代码重构

```text
refactor(server): 优化请求处理中间件结构

- 将中间件拆分为独立的模块
- 使用责任链模式简化错误处理
- 提高代码可测试性
```

## 用户交互流程

### 步骤 1: 展示生成的 commit message

在生成 commit message 后,使用清晰的格式展示给用户:

```text
📝 生成的 Commit Message:
---
<生成的完整commit message>
---
```

### 步骤 2: 询问用户确认

使用 AskUserQuestion 工具和用户进行交互

## 特殊场景处理

### 场景 1: 无暂存改动

如果运行 `git status` 发现没有已暂存的改动, 提示用户是否使用 `git add` 添加文件到暂存区。

### 场景 2: 混合类型改动

如果改动同时包含多种类型(如新功能 + Bug 修复),按以下优先级选择:

1. 优先选择主要类型 (feat/fix)
2. 如果同时包含 feat 和 fix,选择改动行数更多的类型
3. **使用【标签】在 body 中分组说明不同类型的改动**

**错误示例** (违反单一类型原则):

```text
feat(ui): 添加新功能

fix(auth): 修复登录问题
```

**正确示例**:

```text
feat(ui): 添加新功能并修复登录问题

【新功能】
- 添加用户头像上传功能

【Bug 修复】
- 修复登录超时问题
```

## 注意事项

1. **严格遵守单一类型原则**: 每次提交只能有一个 type
2. **scope 必填**: 必须明确指定影响范围
3. **中英文使用**: type 和 scope 使用英文小写,其他内容使用中文
4. **准确性**: commit message 必须准确反映实际改动内容
5. **简洁性**: subject 要简洁明了,body 要有条理
6. **破坏性变更**: 必须明确标注,不能遗漏
