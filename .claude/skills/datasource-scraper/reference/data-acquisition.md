# 数据获取策略指南

**对应主 SKILL.md 步骤 1：获取网站内容**

本文档详细说明如何从数据源网站获取信息，包括两层降级策略的使用方法。

---

## 输入识别

根据用户输入类型选择处理方式：

### URL 输入
- 特征：以 `http://` 或 `https://` 开头
- 处理：直接使用该 URL 进行数据获取

### 名字输入
- 特征：不以 `http://` 或 `https://` 开头
- 示例：`GenBank - 基因序列数据库`、`人民银行数据`、`World Bank`
- 处理流程：
  1. 使用 WebSearch 搜索官方网站
  2. 从搜索结果中识别最可能的官方 URL
  3. 使用 AskUserQuestion 向用户确认 URL 是否正确
  4. 确认后进入数据获取流程

---

## 两层降级策略

根据网站复杂度和可访问性，选择合适的工具。

```
第一层: Web Search + WebFetch（静态内容，优先使用）
  ↓ 如遇 JS 渲染/需要登录/交互内容
第二层: Playwright（浏览器自动化，最后手段）
```

---

## 第一层：Web Search + WebFetch（主要策略）

### Web Search 搜索

使用多角度搜索获取概览信息：

**搜索查询示例**：
- `"{组织名称} data"`
- `"{组织名称} API documentation"`
- `"{组织名称} methodology"`
- `"{组织名称} about"`
- `"{组织名称} datasets"`

**提取目标**：
- 组织名称和类型
- 主要 URL
- API 文档链接
- 数据门户地址
- 组织概述信息

### WebFetch 详细验证

直接访问用户提供的 URL 或搜索中发现的关键页面。

**提取目标信息**：
- **组织信息**：名称、类型、描述、官网
- **关键 URL**：主页、数据门户、API 文档、下载页面
- **数据覆盖范围**：地理范围、时间跨度、主题领域
- **更新频率**：实时、每日、每月、每年等
- **许可协议**：开放程度、商业使用限制
- **API 可用性**：是否提供 API、认证方式、文档链接
- **数据格式**：CSV、JSON、Excel、PDF 等

### 适用场景
- ✅ 静态 HTML 页面
- ✅ 服务端渲染的页面
- ✅ 信息在页面源代码中可见
- ✅ 无需登录即可访问关键信息
- ✅ 无需交互即可看到完整内容

### 不适用场景
- ❌ JavaScript 动态渲染页面（WebFetch 返回空白或骨架）
- ❌ 需要登录才能查看
- ❌ 内容隐藏在交互元素中（下拉菜单、Tab、折叠面板）
- ❌ 页面返回 403 Forbidden（反爬机制）

---

## 第二层：Playwright 浏览器自动化（最后手段）

### 触发条件

当第一层策略无法获取足够信息时，满足以下**任一条件**即可触发：

#### 1. JavaScript 渲染页面
- WebFetch 返回的 HTML 内容 < 500 字符
- HTML 中包含大量 `<script>` 标签但内容区域为空或仅有骨架
- 检测到 React/Vue/Angular 等 SPA 框架特征（如 `<div id="root">`, `<div id="app">`）
- 页面提示 "Please enable JavaScript"

#### 2. 需要登录或认证
- 页面包含登录提示关键词：`login`, `sign in`, `authentication required`, `please log in`
- 返回 401 Unauthorized 或 403 Forbidden 状态码
- 内容显示 "请登录查看"、"Members only"、"Restricted access"

#### 3. 交互式内容
- 搜索结果提示需要点击、展开才能看到完整内容
- 数据类别列表在下拉菜单、折叠面板或 Tab 中
- 需要选择地区/年份等参数才显示数据范围
- 内容在鼠标悬停或点击后才显示

#### 4. 用户明确要求
- 用户在请求中提到 "使用浏览器"、"需要登录"、"手动访问"

---

### 使用前的用户沟通（⚠️ 必须遵守）

调用 Playwright 前，**必须**向用户清楚说明情况。

#### 标准沟通模板

```
⚠️ 检测到访问困难，需要使用浏览器工具

【遇到的问题】: [具体描述问题]

常见问题示例：
- 该页面使用 JavaScript 动态加载内容，WebFetch 只能获取到空白页面
- 该数据源需要登录才能查看 API 文档和完整数据目录
- 数据类别列表隐藏在交互式菜单中，需要点击展开
- 页面返回 403 错误，可能有反爬机制

【解决方案】: 使用 Playwright 浏览器工具打开页面

【需要您的协助】: [列出可能需要的用户操作]
常见协助场景：
- ✋ 如果遇到登录页面，需要您手动完成登录
- ✋ 如果出现验证码/人机验证，需要您手动完成
- ✋ 如果需要选择特定选项，我会截图请您确认
- ⏱️ 预计需要 1-3 分钟

【继续操作】: 现在开始使用浏览器工具访问该页面...
```

---

### Playwright 详细工作流程

#### 步骤 1: 打开页面并初步诊断

```javascript
// 1. 导航到目标页面
await browser_navigate({ url: targetUrl })

// 2. 获取页面快照
const snapshot = await browser_snapshot()

// 3. 截图展示当前状态
await browser_take_screenshot({
  filename: 'initial-page.png',
  type: 'png'
})
```

向用户反馈：
```
🌐 已打开页面: [URL]
📸 页面截图已保存
📋 正在分析页面结构...
```

---

#### 步骤 2: 检测并处理登录需求

检测登录表单：
```javascript
const needsLogin = (
  snapshot.includes('textbox') &&
  (snapshot.includes('password') ||
   snapshot.includes('login') ||
   snapshot.includes('sign in'))
)
```

如果检测到登录：

```
📸 检测到登录页面

请按以下步骤操作：
1. 查看上方截图，确认页面状态
2. 在您的浏览器中访问该页面并完成登录
3. 登录完成后，我会自动检测并继续提取信息

⏳ 正在等待登录完成...（每 5 秒检查一次页面状态）
```

登录检测循环：
```javascript
let loginAttempts = 0
const maxAttempts = 36  // 3 分钟

while (needsLogin && loginAttempts < maxAttempts) {
  await browser_wait_for({ time: 5 })
  const newSnapshot = await browser_snapshot()
  needsLogin = (/* 再次检测登录表单 */)
  loginAttempts++

  // 每 30 秒提醒一次
  if (loginAttempts % 6 === 0) {
    console.log(`⏳ 仍在等待登录... (已等待 ${loginAttempts * 5} 秒)`)
  }
}
```

---

#### 步骤 3: 处理交互式内容

##### 3.1 展开折叠内容

```javascript
// 查找 "Show more" / "展开" 按钮
const snapshot = await browser_snapshot()

await browser_click({
  element: "Show more button",
  ref: "e42"  // 从 snapshot 中获取
})

await browser_wait_for({ time: 2 })

// 截图验证
await browser_take_screenshot({ filename: 'expanded-content.png' })
```

##### 3.2 切换 Tab 标签

```javascript
const tabs = ['API Documentation', 'Data Catalog', 'Download']

for (const tabName of tabs) {
  console.log(`🔄 切换到 ${tabName} 标签...`)

  await browser_click({
    element: `${tabName} tab`,
    ref: "eXX"  // 从 snapshot 获取
  })

  await browser_wait_for({ time: 1 })

  // 提取该 tab 的信息
  const data = await browser_evaluate({
    function: `() => { /* 提取逻辑 */ }`
  })
}
```

##### 3.3 下拉菜单选择

```javascript
await browser_select_option({
  element: "Region selector",
  ref: "e25",
  values: ["All regions"]
})

await browser_wait_for({ time: 1 })
```

---

#### 步骤 4: 提取结构化数据

使用 `browser_evaluate` 执行 JavaScript 提取信息：

```javascript
const extractedData = await browser_evaluate({
  function: `() => {
    // 辅助函数：安全获取文本
    const getText = (selector) => {
      const el = document.querySelector(selector)
      return el?.textContent?.trim() || null
    }

    // 辅助函数：获取链接
    const getLink = (pattern) => {
      const links = Array.from(document.querySelectorAll('a'))
      const link = links.find(a => pattern.test(a.textContent))
      return link?.href || null
    }

    return {
      // 组织信息
      organizationName: getText('.org-name, .organization, h1'),
      description: getText('.description, .about, .intro'),

      // API 信息
      apiDocUrl: getLink(/api|developer|technical/i),
      apiAuthentication: document.body.textContent.includes('API key') ? 'api_key' :
                         document.body.textContent.includes('OAuth') ? 'oauth' : null,

      // 数据类别
      categories: Array.from(document.querySelectorAll('.category, .data-type, .dataset'))
        .map(el => ({
          name: el.querySelector('.name, .title, h3')?.textContent?.trim(),
          description: el.querySelector('.desc, .description, p')?.textContent?.trim()
        }))
        .filter(cat => cat.name),

      // 更新频率
      updateFrequency: (
        document.body.textContent.match(/(daily|weekly|monthly|quarterly|annually|real-?time)/i)?.[0] ||
        getText('.update-frequency, .frequency')
      ),

      // 地理覆盖
      geographicCoverage: (
        document.body.textContent.includes('global') ? 'global' :
        document.body.textContent.includes('regional') ? 'regional' : null
      ),

      // 许可信息
      license: getText('.license, .terms, [class*="license"]'),

      // 数据格式
      formats: Array.from(document.querySelectorAll('[class*="format"], .file-type'))
        .map(el => el.textContent.trim().toLowerCase())
        .filter(f => ['csv', 'json', 'xml', 'excel', 'pdf'].some(fmt => f.includes(fmt))),

      // 其他关键链接
      downloadUrl: getLink(/download|export|获取数据/i),
      methodologyUrl: getLink(/methodology|方法论|technical notes/i),
      contactUrl: getLink(/contact|support|联系/i),

      // 时间跨度
      temporalCoverage: (() => {
        const text = document.body.textContent
        const yearRange = text.match(/(19|20)\\d{2}\\s*[-–—到至]\\s*(19|20)\\d{2}/)
        if (yearRange) {
          const years = yearRange[0].match(/(19|20)\\d{2}/g)
          return { start: years[0], end: years[1] }
        }
        return null
      })()
    }
  }`
})
```

向用户反馈：
```
✅ 已提取组织信息: [名称]
✅ 已找到 API 文档: [URL]
✅ 已提取数据类别: 共 15 个
✅ 更新频率: 每月
✅ 许可协议: CC BY 4.0
📊 正在整理提取的数据...
```

---

#### 步骤 5: 多页面信息聚合

如果需要访问多个页面：

```javascript
const pages = [
  { name: 'API Documentation', url: apiUrl },
  { name: 'Data Catalog', url: catalogUrl },
  { name: 'Methodology', url: methodUrl }
]

const allData = {}

for (const page of pages) {
  console.log(`📄 正在访问: ${page.name}`)

  await browser_navigate({ url: page.url })
  await browser_wait_for({ time: 2 })

  const pageData = await browser_evaluate({
    function: `() => { /* 针对该页面的提取逻辑 */ }`
  })

  allData[page.name] = pageData
  console.log(`✅ ${page.name} 信息提取完成`)
}

// 合并所有页面的数据
const mergedData = {
  ...allData['API Documentation'],
  categories: allData['Data Catalog'].categories,
  methodology: allData['Methodology'].description
}
```

---

#### 步骤 6: 错误处理与重试

```javascript
// 检测验证码
const snapshot = await browser_snapshot()
if (snapshot.includes('captcha') || snapshot.includes('reCAPTCHA')) {
  await browser_take_screenshot({ filename: 'captcha.png' })

  console.log(`
    🤖 检测到验证码

    📸 已截图当前页面

    请在浏览器中手动完成验证码验证。
    完成后我会自动继续。

    ⏳ 正在等待...
  `)

  // 等待验证码完成
  let captchaSolved = false
  while (!captchaSolved) {
    await browser_wait_for({ time: 5 })
    const newSnapshot = await browser_snapshot()
    captchaSolved = !newSnapshot.includes('captcha')
  }

  console.log('✅ 验证码已完成')
}
```

---

#### 步骤 7: 完成并清理

```javascript
// 最终截图
await browser_take_screenshot({
  filename: 'final-state.png',
  fullPage: true
})

// 关闭浏览器
await browser_close()

// 总结报告
console.log(`
✅ Playwright 提取完成

📊 已获取以下信息：
- ✅ 组织名称: ${data.organizationName}
- ✅ 描述: ${data.description}
- ✅ API 文档: ${data.apiDocUrl || '未找到'}
- ✅ 数据类别: ${data.categories.length} 个
- ✅ 更新频率: ${data.updateFrequency || '未知'}
- ✅ 许可协议: ${data.license || '未明确'}
- ✅ 地理覆盖: ${data.geographicCoverage || '未指定'}

📸 已保存截图供参考

接下来将使用这些信息填充 JSON schema...
`)
```

---

## 使用场景示例

### 场景 1: React SPA 页面

```
触发原因: WebFetch 返回几乎空白的 HTML（<div id="root"></div>）

Playwright 流程:
  1. browser_navigate
  2. browser_wait_for({ time: 3 }) - 等待 React 渲染
  3. browser_snapshot - 获取渲染后的内容
  4. browser_evaluate - 提取数据
  5. browser_close
```

### 场景 2: 需要登录的数据门户

```
触发原因: WebFetch 返回 "Please login to continue"

Playwright 流程:
  1. browser_navigate
  2. browser_take_screenshot - 显示登录页面
  3. 提示用户登录
  4. 循环检测登录状态
  5. 检测到登录成功
  6. 提取内容
  7. browser_close
```

### 场景 3: 交互式数据目录

```
触发原因: 数据类别列表隐藏在下拉菜单中

Playwright 流程:
  1. browser_navigate
  2. browser_snapshot - 找到菜单按钮
  3. browser_click - 点击展开
  4. browser_wait_for - 等待动画完成
  5. browser_evaluate - 提取展开后的列表
  6. browser_take_screenshot - 截图验证
  7. browser_close
```

---

## 最佳实践

### 1. 谨慎使用
- ✅ 仅在前两层方法确实无效时才使用 Playwright
- ✅ 能用 WebFetch 解决的不用 Playwright
- ❌ 不要默认就用 Playwright（速度慢、资源占用高）

### 2. 充分沟通
- ✅ 每个关键步骤都向用户说明
- ✅ 使用截图帮助用户理解当前状态
- ✅ 明确告知需要用户做什么
- ✅ 预估所需时间

### 3. 合理等待
- ✅ 页面加载后等待 2-3 秒确保 JS 执行完成
- ✅ 点击操作后等待 1-2 秒等待响应
- ✅ 登录等待设置合理超时（3 分钟）
- ❌ 不要无限期等待

### 4. 错误处理
- ✅ 捕获并向用户说明所有错误
- ✅ 提供可能的原因和解决建议
- ✅ 询问用户是否重试或提供替代方案
- ❌ 不要默默失败

### 5. 资源管理
- ✅ 完成后务必调用 `browser_close()`
- ✅ 避免打开多个页面（除非必要）
- ✅ 使用 Tab 管理而不是多窗口
- ❌ 不要让浏览器一直开着

### 6. 截图策略
- ✅ 关键步骤截图（登录页、最终状态）
- ✅ 出错时截图帮助诊断
- ✅ 使用有意义的文件名
- ❌ 不要每一步都截图（浪费存储）

### 7. 数据提取
- ✅ 使用健壮的选择器（多种备选）
- ✅ 所有提取都使用可选链 `?.` 避免错误
- ✅ 过滤掉 null/undefined 值
- ✅ 提取失败的字段标记为 null

---

## 工具函数参考

### 常用 Playwright 工具

| 工具 | 用途 |
|------|------|
| `browser_navigate` | 导航到 URL |
| `browser_snapshot` | 获取页面结构 |
| `browser_take_screenshot` | 截图 |
| `browser_click` | 点击元素 |
| `browser_evaluate` | 执行 JS 提取数据 |
| `browser_wait_for` | 等待时间/元素 |
| `browser_type` | 输入文本 |
| `browser_select_option` | 选择下拉选项 |
| `browser_close` | 关闭浏览器 |
| `browser_console_messages` | 查看控制台日志 |
| `browser_network_requests` | 查看网络请求 |

### JavaScript 提取辅助函数

```javascript
// 安全获取文本
const getText = (selector) => document.querySelector(selector)?.textContent?.trim() || null

// 获取所有文本
const getAllText = (selector) =>
  Array.from(document.querySelectorAll(selector)).map(el => el.textContent.trim())

// 查找包含特定文本的链接
const findLink = (pattern) =>
  Array.from(document.querySelectorAll('a')).find(a => pattern.test(a.textContent))?.href

// 提取表格数据
const extractTable = (tableSelector) =>
  Array.from(document.querySelectorAll(`${tableSelector} tr`)).map(row =>
    Array.from(row.querySelectorAll('td, th')).map(cell => cell.textContent.trim())
  )

// 检查文本是否包含关键词
const containsKeyword = (...keywords) =>
  keywords.some(kw => document.body.textContent.toLowerCase().includes(kw.toLowerCase()))

// 提取日期范围
const extractDateRange = () => {
  const text = document.body.textContent
  const match = text.match(/(19|20)\d{2}\s*[-–—到至]\s*(19|20)\d{2}/)
  if (match) {
    const years = match[0].match(/(19|20)\d{2}/g)
    return { start: years[0], end: years[1] }
  }
  return null
}
```

---

## 注意事项

1. **隐私与安全**: 不要在浏览器操作中记录用户的登录凭据
2. **性能考虑**: Playwright 比 WebFetch 慢 10-20 倍，谨慎使用
3. **网站条款**: 确保自动化操作符合目标网站的服务条款
4. **超时管理**: 所有等待操作都应设置合理超时
5. **错误恢复**: 准备好降级方案（如让用户手动提供信息）
