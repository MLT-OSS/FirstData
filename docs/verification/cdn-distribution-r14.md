# R14 Step 1 v2 [DEPRECATED - HEAD-only baseline] · FirstData CDN/WAF 指纹分布

> ⚠️ **2026-05-07 02:06 标注 DEPRECATED**：本文档 + csv 为 **v0 pilot baseline**，不作为 Step 2 分层决策的数据源。
>
> **废弃原因**：HEAD-only 探测 → 49.9% unknown 家族，因为大量站点对 HEAD 请求返回 403/405 或精简 header。需 Step 1 v2 脚本（HEAD→GET fallback + 6 类失败单列 + CF body 探测 + 国产 WAF 指纹）重跑。
>
> **本文档保留**用于：1）方法论复盘；2）v2 改进空间估算（见“status-based 分桶”章节）。
> **v2 跑完后本文档被新文档替换**。

- 扫描源数（working tree）: **705**
- tracked HEAD 源数: **698**（口径 = `git ls-tree -r HEAD firstdata/sources/**/*.json`）
- commit: `f6434e1`
- 探测: `curl -sI -L` + Chrome 120 UA + follow redirects(5) + 15s timeout
- 脚本: `scripts/r14_cdn_fingerprint.py`

> ⚠️ 本步骤只做**指纹分布**，不做**三层能力结论**。  
> 分布数字 = 「我们观察到的 CDN/WAF 公开 header 特征」，不等价「L2/L3 能否通过」。
> 真实通过率需三层实测（Step 5）给出。

## [RETRACTED] v1 三条越界结论（2026-05-07 01:31 明鉴指令）

v1 交付（2026-05-07 01:04）在「观察」段下了三条越界结论，**全部撤回**：

- ~~观察 2：「government × cloudflare 仅 3.1%，主体结构决定 L2 GET+UA 已可覆盖绝大部分政府源」~~ **[RETRACTED]**
- ~~观察 3：「unknown + origin = 82.2%，是 easy tier」~~ **[RETRACTED]**
- ~~总结：「政府源 L2 GET+UA 足够」~~ **[RETRACTED]**

**撤回原因**：三条都把 **CDN 指纹分布（已测）** 直接外推成 **L2 通过能力（未测）**。  
3.1% 是 Cloudflare 识别率，不是 L2 通过率；剩下 96.9% 政府源里 223 个 unknown 含多少国产 WAF / 政府自建网关本步骤无法判断；easy tier 需要三层实测验证。  
反模式命名：**「分布推断 ↔ 能力结论边界失守」** — 已归档 `memory/qa-studies/README.md §10`。

**截稿前自我检查问句**（以后执行）：
> 「这句话描述的是**已测到的分布**，还是**未测的能力**？后者删掉。」

## 源数口径对齐：R10 `653f849` 603 → R14 `f6434e1` 698，差值 +95

- 口径一致（均为 `git ls-tree -r <hash> --name-only | grep 'firstdata/sources/.*\.json$' | wc -l`）
- 两 commit 间 main 分支 `firstdata/sources/**` 路径下共 113 次 commit（自然 PR 合并增长）
- 差值来源 = 自然 PR 增长，**非口径变化**
- working tree 显示 705 = tracked 698 + 7 个未 commit 的 PM batch JSON（数字铁律第五次违反记录详见 `memory/2026-05-07.md`）

## 总分布（CDN/WAF 类别）

| CDN/WAF | 数量 | 占比 |
|---------|-----:|-----:|
| `cloudflare` | 53 | 7.5% |
| `cloudfront` | 22 | 3.1% |
| `akamai` | 5 | 0.7% |
| `azure` | 9 | 1.3% |
| `alicdn` | 20 | 2.8% |
| `aliyun-waf` | 2 | 0.3% |
| `tencent-cdn` | 1 | 0.1% |
| `imperva` | 5 | 0.7% |
| `unknown_origin_like` | 215 | 30.5% |
| `unknown_custom_gw` | 112 | 15.9% |
| `unknown_error` | 32 | 4.5% |
| `unknown` | 138 | 19.6% |
| `dns_fail` | 1 | 0.1% |
| `tls_fail` | 27 | 3.8% |
| `connect_fail` | 3 | 0.4% |
| `read_timeout` | 50 | 7.1% |
| `other_error` | 10 | 1.4% |

## unknown 二次归因（Server header 拆）

| sub-class | 数量 | 说明 |
|-----------|-----:|------|
| `unknown_origin_like` | 215 | Server: nginx/apache/iis/openresty/... 但无 CDN/WAF marker |
| `unknown_custom_gw`   | 112 | Server 值非标/伪装/自定义网关 |
| `unknown_error`       | 32 | 非 2xx/3xx 返回，header 不可信 |
| `unknown`             | 138 | 无任何线索（空 header / 无 server）|

**总 unknown 家族**: 497

> 注: unknown_* 家族中是否含 CDN/WAF 仍未知（国产 WAF / 政府自建网关特征库不全）。 L2/L3 能力需三层实测验证。

## unknown 家族 status-based 分桶（基于 csv 现有字段，v2 脚本改进方向）

本表把 unknown* 家族 497 条按 HTTP status + Server 是否缺失二次拆解，用于估算 Step 1 v2 脚本 `HEAD→GET fallback` 的**预期改进空间**。
**本表只是 v0 pilot 数据的再分析，不改 CDN 分类结论，不进 Step 2 决策**——v2 脚本重跑后以 v2 结果为准。

| 桶 | 数量 | 占 unknown* | 说明 | v2 脚本改进方向 |
|---|---:|---:|---|---|
| `status=200 + Server 有值` | 279 | 56.1% | 规则未覆盖的 origin/网关 | 扩 CDN_RULES + Server 枚举表 |
| `status=200 + Server 缺失/空` | 138 | 27.8% | 空 header origin（无任何线索）| 拉 body 前 2KB 做 CF challenge 探测 + 国产 WAF body 指纹 |
| `status=403/405` | 50 | 10.1% | HEAD 拒绝 | **GET fallback** 取 last-response header 重新归类 |
| `status=404` | 10 | 2.0% | URL 可能已失效或 HEAD 被拒 | GET fallback + 可能需要 URL 修正 |
| `status=412` | 8 | 1.6% | nmpa-style 地域/证书预检 | 专项调研（mTLS / Origin header 要求）|
| `status=202` | 3 | 0.6% | 异步接受 | 保持 unknown |
| `status=5xx` | 5 | 1.0% | 服务端错误 | 移入 `truly_blocked.csv` |
| `status=302` | 1 | 0.2% | 重定向残留（curl -L 未能跟随）| 提高 `--max-redirs` 或检查跨域 |
| `status=4xx 其他` | 3 | 0.6% | 401/400 | 保持 unknown |
| **合计** | **497** | **100%** | | |

**预期 v2 改进（仅估算，v2 跑完验证）**：
- GET fallback → 预计吸收 50+10 = 60 条（12.1% of unknown*）进入已识别 CDN
- 拉 body 前 2KB CF challenge 探测 → 预计从 138 空 header 里识别出一部分 `cf_challenge_legacy` / `cf_managed`
- 扩 CDN_RULES + Server 枚举 → 预计从 279 `规则未覆盖` 里识别出一部分国产 WAF / 政府自建网关

**v2 验收标准**：`truly_unknown < 10%`（v0 `truly_unknown` 估算上限 = 138 空 header + 279 规则未覆盖中未能归因部分；lower bound 需 v2 实测）。

> 注：本桶 per cdn-subclass 细分参考 `r14-cdn-raw.csv` 原始行；`unknown`(138) 全部是 status=200 + Server 缺失；`unknown_origin_like`(215) 193/215 是 status=200 + Server 有值。

## 失败类型（单列，不进 unknown）

| failure | 数量 |
|---------|-----:|
| `dns_fail` | 1 |
| `tls_fail` | 27 |
| `connect_fail` | 3 |
| `read_timeout` | 50 |
| `other_error` | 10 |

## 矩阵: authority_level × cdn_class（数量）

| authority_level \ cdn | `cloudflare` | `cloudfront` | `akamai` | `azure` | `alicdn` | `aliyun-waf` | `tencent-cdn` | `imperva` | `unknown_origin_like` | `unknown_custom_gw` | `unknown_error` | `unknown` | `dns_fail` | `tls_fail` | `connect_fail` | `read_timeout` | `other_error` | **合计** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| government | 11 | 8 | 3 | 6 | 2 | 2 | 1 | 3 | 92 | 56 | 24 | 84 | 1 | 23 | 0 | 34 | 7 | **357** |
| research | 9 | 2 | 0 | 2 | 8 | 0 | 0 | 0 | 52 | 18 | 3 | 28 | 0 | 0 | 0 | 7 | 0 | **129** |
| international | 29 | 5 | 1 | 1 | 0 | 0 | 0 | 1 | 14 | 9 | 3 | 12 | 0 | 2 | 0 | 0 | 0 | **77** |
| other | 1 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 32 | 8 | 2 | 4 | 0 | 1 | 0 | 7 | 2 | **64** |
| market | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 18 | 10 | 0 | 5 | 0 | 0 | 3 | 1 | 0 | **43** |
| commercial | 1 | 6 | 1 | 0 | 1 | 0 | 0 | 0 | 7 | 11 | 0 | 5 | 0 | 1 | 0 | 1 | 1 | **35** |

## 状态码分布（连通性参考，非分层依据）

- `200`: 488
- `timeout/error`: 86
- `403`: 82
- `404`: 14
- `412`: 8
- `405`: 6
- `302`: 4
- `503`: 3
- `202`: 3
- `502`: 2
- `301`: 2
- `420`: 1
- `567`: 1
- `501`: 1
- `521`: 1
- `500`: 1
- `400`: 1
- `401`: 1

## 口径说明

- 源口径: `git ls-tree -r f6434e1 --name-only | grep firstdata/sources/**/*.json | wc -l` = **698**
- 工作树口径: `find firstdata/sources -name '*.json' | wc -l` = **705** （可能含 untracked；本 PR 基于 working tree 扫描）
- `unknown_origin_like` 命中的源 **可能** 有反代 CDN 但 header 去 CDN 化（常见于 Cloudflare Full Strict、政府自建 WAF）
- 同一域名可能叠加 CDN→origin 链路，本表记最外层响应
- 本 v2 数据**替代** v1（HEAD-only，无 server/header_keys 字段）

## Methodology limitations

- **HEAD vs GET 差异未验证**：某些源 HEAD 返回精简头、GET 返回完整头。本轮用 HEAD（带 UA）。后续 Step 5 用 GET 时分类可能变动。
- **国产 WAF 指纹覆盖不全**：已加安恒/深信服/知道创宇/网宿/阿里云/Tencent CDN，但启明星辰/启博/绿盟等未专门特征化——可能误归 `unknown_custom_gw`。
- **TLS 层未测**：本脚本只看应用层 header，未测 JA3/JA4。CF 的 TLS 指纹层拒绝会表现为 403 或 timeout。

---
Generated by `scripts/r14_cdn_fingerprint.py` @ commit `f6434e1`
