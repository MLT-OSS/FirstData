#!/usr/bin/env python3
"""R14 Step 1 · FirstData 全量 CDN/WAF 指纹扫描（v2）

对每个源的 data_url (fallback website) 发 `curl -I`（Chrome 120 UA, follow redirects）,
解析 CDN/WAF 指纹，按 authority_level × cdn_class 出分布矩阵。

v2 增强（2026-05-07, R14 Step 1 明鉴补测指令）:
  1. 记录 `server` header 原值
  2. 记录 `raw_header_snippet`（去值归类的 header key 序列，80B）
  3. 国产 WAF 指纹（安恒 / 深信服 / 知道创宇 / 网宿 / 阿里云 WAF / Tencent T-Sec）
  4. unknown 二次归因：基于 Server header 值拆
       - unknown_origin_like （nginx/apache/iis/openresty but no CDN marker）
       - unknown_custom_gw   （server 值非标 / spoofed / 空）
       - unknown_error       （非 2xx 状态码, header 不可信）
  5. 失败类型单列: dns_fail / tls_fail / connect_timeout / read_timeout

注意: 本脚本仅做**指纹分布**不做**能力结论**。"unknown" 源 L2/L3 能否覆盖须由三层实测决定。

输出:
  - docs/verification/cdn-distribution-r14.md
  - docs/verification/r14-cdn-raw.csv
"""
from __future__ import annotations
import json
import glob
import subprocess
import re
import csv
import sys
import os
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

TIMEOUT = 15

# CDN/WAF 分类规则（按优先级顺序匹配）
# 格式: (cdn_label, [匹配片段列表, 任一命中即归类])
CDN_RULES = [
    ("cloudflare",       ["cf-ray:", "cf-mitigated:", "cf-chl-bypass:", "server: cloudflare"]),
    ("cloudfront",       ["x-amz-cf-id:", "x-amz-cf-pop:"]),
    ("akamai",           ["x-akamai-", "server: akamaighost", "server: akamainetstorage"]),
    ("fastly",           ["x-fastly-", "server: fastly"]),
    ("azure",            ["x-azure-ref:", "x-msedge-ref:"]),
    ("alicdn",           ["x-alicdn", "server: tengine"]),
    ("aliyun-waf",       ["x-yd-waf-info:", "x-waf-", "ali-swift"]),
    ("tencent-cdn",      ["x-nws-log-uuid:", "server: tencent-cos"]),
    ("baidu-bfe",        ["server: bfe"]),
    ("imperva",          ["x-cdn: incapsula", "x-iinfo:"]),
    ("sucuri",           ["x-sucuri-"]),
    ("cn-waf-anheng",    ["x-safedog:", "x-safedog-flags:"]),
    ("cn-waf-sangfor",   ["x-sinfor", "x-ac-waf"]),
    ("cn-waf-yunsuo",    ["x-yunsuo", "x-kns-"]),
    ("cn-waf-wangsu",    ["x-yundun", "server: wangsu"]),
]

# Server 值到 origin_like 的映射
ORIGIN_LIKE_RE = re.compile(
    r"^(nginx|apache|microsoft-iis|openresty|lighttpd|caddy|gunicorn|jetty|tomcat|kestrel|werkzeug|gse)",
    re.IGNORECASE,
)


def parse_last_response(raw_lower: str) -> str:
    """跟随 -L 跳转时 curl -I 会打印多段 header，取最后一段（真正响应的站点）。"""
    blocks = [b for b in re.split(r"(?=^http/[0-9.]+\s)", raw_lower, flags=re.MULTILINE) if b.strip()]
    return blocks[-1] if blocks else raw_lower


def extract_server(headers_lower: str) -> str:
    m = re.search(r"^server:\s*([^\r\n]+)", headers_lower, re.MULTILINE)
    return m.group(1).strip() if m else ""


def extract_header_keys(headers_lower: str, limit: int = 120) -> str:
    """抽取 header key 序列（不含值），供后续人工模式识别。"""
    keys = []
    for line in headers_lower.splitlines():
        if ":" in line and not line.startswith("http/"):
            k = line.split(":", 1)[0].strip()
            if k and k not in keys:
                keys.append(k)
    s = ",".join(keys)
    return s[:limit]


def classify_cdn(headers_lower: str, server: str, status: int) -> str:
    """一级分类: 显式 CDN/WAF → origin_like → custom_gw → unknown_error / unknown."""
    for label, patterns in CDN_RULES:
        for p in patterns:
            if p in headers_lower:
                return label

    # server 值 fallback
    if server:
        if ORIGIN_LIKE_RE.match(server):
            return "unknown_origin_like"
        # 非空但非标准 server 值 = 自定义网关/伪装
        return "unknown_custom_gw"

    # 非 2xx/3xx 且无 server header → header 不可信
    if status and (status >= 400 or status == 0):
        return "unknown_error"

    return "unknown"


def classify_error(stderr: str, curl_exit: int) -> str:
    """curl 失败细分: dns_fail / tls_fail / connect_timeout / read_timeout / other."""
    s = (stderr or "").lower()
    # curl exit codes: 6=DNS, 7=connect, 28=timeout, 35/51/60=TLS
    if curl_exit == 6 or "could not resolve" in s:
        return "dns_fail"
    if curl_exit in (35, 51, 60) or "ssl" in s or "tls" in s or "certificate" in s:
        return "tls_fail"
    if curl_exit == 7 or "connection refused" in s or "failed to connect" in s:
        return "connect_fail"
    if curl_exit == 28 or "timed out" in s or "timeout" in s:
        return "read_timeout"
    return "other_error"


def probe(source_id: str, authority: str, url: str) -> dict:
    host = urlparse(url).hostname or ""
    try:
        r = subprocess.run(
            [
                "curl", "-sI", "-L",
                "--max-redirs", "5",
                "--max-time", str(TIMEOUT),
                "-A", UA,
                "-o", "/dev/null",
                "-D", "-",
                url,
            ],
            capture_output=True, text=True, timeout=TIMEOUT + 5,
        )
        raw = (r.stdout or "").lower()
        last = parse_last_response(raw)
        status_m = re.match(r"http/[0-9.]+\s+(\d{3})", last)
        status = int(status_m.group(1)) if status_m else 0
        server = extract_server(last)
        header_keys = extract_header_keys(last)

        if r.returncode != 0 or status == 0:
            err_class = classify_error(r.stderr, r.returncode)
            return {
                "id": source_id, "authority": authority, "url": url, "host": host,
                "status": status, "cdn": err_class, "server": server,
                "header_keys": header_keys, "err": (r.stderr or "")[:120],
            }

        cdn = classify_cdn(last, server, status)
        return {
            "id": source_id, "authority": authority, "url": url, "host": host,
            "status": status, "cdn": cdn, "server": server,
            "header_keys": header_keys, "err": "",
        }
    except subprocess.TimeoutExpired:
        return {"id": source_id, "authority": authority, "url": url, "host": host,
                "status": 0, "cdn": "read_timeout", "server": "",
                "header_keys": "", "err": "subprocess_timeout"}
    except Exception as e:
        return {"id": source_id, "authority": authority, "url": url, "host": host,
                "status": 0, "cdn": "other_error", "server": "",
                "header_keys": "", "err": str(e)[:120]}


def load_sources():
    out = []
    for f in sorted(glob.glob("firstdata/sources/**/*.json", recursive=True)):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        url = d.get("data_url") or d.get("website")
        if not url or not url.startswith(("http://", "https://")):
            continue
        out.append((d.get("id", "?"), d.get("authority_level", "unknown"), url))
    return out


# CDN 分类顺序（表格列顺序）——稳定优先级
CDN_DISPLAY_ORDER = [
    "cloudflare", "cloudfront", "akamai", "fastly", "azure",
    "alicdn", "aliyun-waf", "tencent-cdn", "baidu-bfe", "imperva", "sucuri",
    "cn-waf-anheng", "cn-waf-sangfor", "cn-waf-yunsuo", "cn-waf-wangsu",
    "unknown_origin_like", "unknown_custom_gw", "unknown_error", "unknown",
    "dns_fail", "tls_fail", "connect_fail", "read_timeout", "other_error",
]


def main():
    # —— 口径锚定（在每次输出前记录，不信任脚本外部状态） ——
    commit = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True,
    ).stdout.strip()
    # working tree vs committed 源数校验
    tracked_count = int(subprocess.run(
        ["bash", "-c",
         "git ls-tree -r HEAD --name-only | grep -E '^firstdata/sources/.*\\.json$' | wc -l"],
        capture_output=True, text=True,
    ).stdout.strip() or "0")

    sources = load_sources()
    wt_count = len(sources)
    print(f"[info] HEAD={commit} tracked_sources={tracked_count} working_tree_sources={wt_count}",
          file=sys.stderr)
    print(f"[info] scanning {wt_count} sources with concurrency=30", file=sys.stderr)

    results = []
    with ThreadPoolExecutor(max_workers=30) as ex:
        futs = {ex.submit(probe, sid, auth, url): sid for sid, auth, url in sources}
        done = 0
        for f in as_completed(futs):
            results.append(f.result())
            done += 1
            if done % 50 == 0:
                print(f"[progress] {done}/{wt_count}", file=sys.stderr)

    os.makedirs("docs/verification", exist_ok=True)

    # —— raw csv（首行 metadata 注释，第二行开始是数据）——
    csv_path = "docs/verification/r14-cdn-raw.csv"
    with open(csv_path, "w", newline="") as f:
        f.write(f"# R14 Step 1 v2 raw probe data | commit={commit} | "
                f"tracked_sources={tracked_count} | working_tree={wt_count} | "
                f"probe=curl -sI -L -A Chrome/120 --max-time {TIMEOUT}s\n")
        w = csv.DictWriter(f, fieldnames=[
            "id", "authority", "url", "host", "status", "cdn", "server", "header_keys", "err",
        ])
        w.writeheader()
        w.writerows(sorted(results, key=lambda r: r["id"]))

    # —— 聚合 ——
    matrix = defaultdict(Counter)
    cdn_total = Counter()
    auth_total = Counter()
    for r in results:
        matrix[r["authority"]][r["cdn"]] += 1
        cdn_total[r["cdn"]] += 1
        auth_total[r["authority"]] += 1

    # 显示顺序: 先按 CDN_DISPLAY_ORDER 列已出现的, 再补未列出的按数量倒序
    cdn_order = [c for c in CDN_DISPLAY_ORDER if c in cdn_total]
    extra = [c for c in cdn_total if c not in cdn_order]
    cdn_order += sorted(extra, key=lambda k: -cdn_total[k])
    auth_order = sorted(auth_total, key=lambda k: -auth_total[k])

    total = sum(cdn_total.values())

    # —— unknown 二次归因表 ——
    unknown_labels = [
        "unknown_origin_like", "unknown_custom_gw", "unknown_error", "unknown",
    ]
    unknown_breakdown = [(c, cdn_total.get(c, 0)) for c in unknown_labels]

    # —— 状态码分布 ——
    status_ct = Counter(r["status"] for r in results)

    lines = [
        "# R14 Step 1 v2 · FirstData CDN/WAF 指纹分布",
        "",
        f"- 扫描源数（working tree）: **{wt_count}**",
        f"- tracked HEAD 源数: **{tracked_count}**（口径 = `git ls-tree -r HEAD firstdata/sources/**/*.json`）",
        f"- commit: `{commit}`",
        f"- 探测: `curl -sI -L` + Chrome 120 UA + follow redirects(5) + {TIMEOUT}s timeout",
        f"- 脚本: `scripts/r14_cdn_fingerprint.py`",
        "",
        "> ⚠️ 本步骤只做**指纹分布**，不做**三层能力结论**。  ",
        "> 分布数字 = 「我们观察到的 CDN/WAF 公开 header 特征」，不等价「L2/L3 能否通过」。",
        "> 真实通过率需三层实测（Step 5）给出。",
        "",
        "## 总分布（CDN/WAF 类别）",
        "",
        "| CDN/WAF | 数量 | 占比 |",
        "|---------|-----:|-----:|",
    ]
    for c in cdn_order:
        n = cdn_total[c]
        lines.append(f"| `{c}` | {n} | {n/total*100:.1f}% |")

    lines += [
        "",
        "## unknown 二次归因（Server header 拆）",
        "",
        "| sub-class | 数量 | 说明 |",
        "|-----------|-----:|------|",
        f"| `unknown_origin_like` | {cdn_total.get('unknown_origin_like', 0)} | Server: nginx/apache/iis/openresty/... 但无 CDN/WAF marker |",
        f"| `unknown_custom_gw`   | {cdn_total.get('unknown_custom_gw', 0)} | Server 值非标/伪装/自定义网关 |",
        f"| `unknown_error`       | {cdn_total.get('unknown_error', 0)} | 非 2xx/3xx 返回，header 不可信 |",
        f"| `unknown`             | {cdn_total.get('unknown', 0)} | 无任何线索（空 header / 无 server）|",
        "",
        "**总 unknown 家族**: {}".format(sum(cdn_total.get(c, 0) for c in unknown_labels)),
        "",
        "> 注: unknown_* 家族中是否含 CDN/WAF 仍未知（国产 WAF / 政府自建网关特征库不全）。"
        " L2/L3 能力需三层实测验证。",
        "",
        "## 失败类型（单列，不进 unknown）",
        "",
        "| failure | 数量 |",
        "|---------|-----:|",
    ]
    for fc in ("dns_fail", "tls_fail", "connect_fail", "read_timeout", "other_error"):
        lines.append(f"| `{fc}` | {cdn_total.get(fc, 0)} |")

    lines += [
        "",
        "## 矩阵: authority_level × cdn_class（数量）",
        "",
        "| authority_level \\ cdn | " + " | ".join(f"`{c}`" for c in cdn_order) + " | **合计** |",
        "|---" * (len(cdn_order) + 2) + "|",
    ]
    for a in auth_order:
        row = [a] + [str(matrix[a].get(c, 0)) for c in cdn_order] + [f"**{auth_total[a]}**"]
        lines.append("| " + " | ".join(row) + " |")

    lines += [
        "",
        "## 状态码分布（连通性参考，非分层依据）",
        "",
    ]
    for s in sorted(status_ct, key=lambda k: -status_ct[k]):
        label = "timeout/error" if s == 0 else str(s)
        lines.append(f"- `{label}`: {status_ct[s]}")

    lines += [
        "",
        "## 口径说明",
        "",
        f"- 源口径: `git ls-tree -r {commit} --name-only | grep firstdata/sources/**/*.json | wc -l` = **{tracked_count}**",
        f"- 工作树口径: `find firstdata/sources -name '*.json' | wc -l` = **{wt_count}** "
        "（可能含 untracked；本 PR 基于 working tree 扫描）",
        "- `unknown_origin_like` 命中的源 **可能** 有反代 CDN 但 header 去 CDN 化（常见于 Cloudflare Full Strict、政府自建 WAF）",
        "- 同一域名可能叠加 CDN→origin 链路，本表记最外层响应",
        "- 本 v2 数据**替代** v1（HEAD-only，无 server/header_keys 字段）",
        "",
        "## Methodology limitations",
        "",
        "- **HEAD vs GET 差异未验证**：某些源 HEAD 返回精简头、GET 返回完整头。本轮用 HEAD（带 UA）。"
        "后续 Step 5 用 GET 时分类可能变动。",
        "- **国产 WAF 指纹覆盖不全**：已加安恒/深信服/知道创宇/网宿/阿里云/Tencent CDN，"
        "但启明星辰/启博/绿盟等未专门特征化——可能误归 `unknown_custom_gw`。",
        "- **TLS 层未测**：本脚本只看应用层 header，未测 JA3/JA4。CF 的 TLS 指纹层拒绝会表现为 403 或 timeout。",
        "",
        "---",
        f"Generated by `scripts/r14_cdn_fingerprint.py` @ commit `{commit}`",
    ]

    md_path = "docs/verification/cdn-distribution-r14.md"
    with open(md_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[done] wrote {md_path} + {csv_path}", file=sys.stderr)
    print(f"[summary] {dict(cdn_total)}", file=sys.stderr)


if __name__ == "__main__":
    main()
