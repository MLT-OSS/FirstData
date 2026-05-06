#!/usr/bin/env python3
"""R14 Step 1: FirstData 全量 CDN/WAF 指纹扫描

对每个源的 data_url (fallback website) 发 `curl -I` (realistic UA)，
解析 CDN/WAF 指纹，按 authority_level × cdn_class 出分布矩阵。

输出: docs/verification/cdn-distribution-r14.md + r14-cdn-raw.csv
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

def classify_cdn(headers_lower: str) -> str:
    """基于响应头分类 CDN/WAF. Returns a single label."""
    if "cf-ray:" in headers_lower or "server: cloudflare" in headers_lower:
        return "cloudflare"
    if "x-amz-cf-id:" in headers_lower or "x-amz-cf-pop:" in headers_lower:
        return "cloudfront"
    if "x-akamai-" in headers_lower or "akamai" in headers_lower:
        return "akamai"
    if "x-fastly-" in headers_lower or "fastly" in headers_lower.split("server:",1)[-1][:80]:
        return "fastly"
    if "x-served-by:" in headers_lower and "cache-" in headers_lower:
        return "fastly"
    if "x-azure-ref:" in headers_lower or "x-msedge-ref:" in headers_lower:
        return "azure"
    if "x-alicdn" in headers_lower or "server: tengine" in headers_lower:
        return "alicdn"
    if "x-cdn: incapsula" in headers_lower or "x-iinfo:" in headers_lower:
        return "imperva"
    if "x-sucuri-" in headers_lower:
        return "sucuri"
    # server header hints (Chinese CDN)
    m = re.search(r"^server:\s*([^\r\n]+)", headers_lower, re.MULTILINE)
    if m:
        srv = m.group(1).strip()
        if "cloudflare" in srv: return "cloudflare"
        if "tengine" in srv: return "alicdn"
        if "bfe" in srv: return "baidu-bfe"
        if "apache" in srv or "nginx" in srv or "microsoft-iis" in srv or "openresty" in srv:
            return "origin"
    return "unknown"

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
        # use the *last* response (after redirects): naive split on HTTP/
        blocks = [b for b in re.split(r"(?=^http/[0-9.]+\s)", raw, flags=re.MULTILINE) if b.strip()]
        last = blocks[-1] if blocks else raw
        status_m = re.match(r"http/[0-9.]+\s+(\d{3})", last)
        status = int(status_m.group(1)) if status_m else 0
        cdn = classify_cdn(last)
        return {
            "id": source_id, "authority": authority, "url": url, "host": host,
            "status": status, "cdn": cdn, "err": "",
        }
    except subprocess.TimeoutExpired:
        return {"id": source_id, "authority": authority, "url": url, "host": host,
                "status": 0, "cdn": "timeout", "err": "timeout"}
    except Exception as e:
        return {"id": source_id, "authority": authority, "url": url, "host": host,
                "status": 0, "cdn": "error", "err": str(e)[:120]}

def load_sources():
    out = []
    for f in glob.glob("firstdata/sources/**/*.json", recursive=True):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        url = d.get("data_url") or d.get("website")
        if not url or not url.startswith(("http://", "https://")):
            continue
        out.append((d.get("id","?"), d.get("authority_level","unknown"), url))
    return out

def main():
    sources = load_sources()
    print(f"[info] scanning {len(sources)} sources with concurrency=30", file=sys.stderr)
    results = []
    with ThreadPoolExecutor(max_workers=30) as ex:
        futs = {ex.submit(probe, sid, auth, url): sid for sid, auth, url in sources}
        done = 0
        for f in as_completed(futs):
            results.append(f.result())
            done += 1
            if done % 50 == 0:
                print(f"[progress] {done}/{len(sources)}", file=sys.stderr)

    os.makedirs("docs/verification", exist_ok=True)
    # raw csv
    with open("docs/verification/r14-cdn-raw.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id","authority","url","host","status","cdn","err"])
        w.writeheader(); w.writerows(results)

    # aggregate matrix
    matrix = defaultdict(Counter)
    cdn_total = Counter()
    auth_total = Counter()
    for r in results:
        matrix[r["authority"]][r["cdn"]] += 1
        cdn_total[r["cdn"]] += 1
        auth_total[r["authority"]] += 1

    commit = subprocess.run(["git","rev-parse","--short","HEAD"],
                             capture_output=True, text=True).stdout.strip()

    cdn_order = sorted(cdn_total, key=lambda k: -cdn_total[k])
    auth_order = sorted(auth_total, key=lambda k: -auth_total[k])

    total = sum(cdn_total.values())
    lines = [
        f"# R14 Step 1 · FirstData CDN/WAF 指纹分布",
        "",
        f"- 扫描源数: **{total}**",
        f"- commit: `{commit}`",
        f"- 探测方式: `curl -I` + Chrome 120 UA + follow redirects + 15s timeout",
        f"- 脚本: `scripts/r14_cdn_fingerprint.py`",
        "",
        "## 总分布 (CDN/WAF 类别)",
        "",
        "| CDN/WAF | 数量 | 占比 |",
        "|---------|-----:|-----:|",
    ]
    for c in cdn_order:
        n = cdn_total[c]
        lines.append(f"| {c} | {n} | {n/total*100:.1f}% |")
    lines += [
        "",
        "## 矩阵: authority_level × cdn_class (数量)",
        "",
        "| authority_level \\ cdn | " + " | ".join(cdn_order) + " | **合计** |",
        "|---" * (len(cdn_order)+2) + "|",
    ]
    for a in auth_order:
        row = [a] + [str(matrix[a].get(c,0)) for c in cdn_order] + [f"**{auth_total[a]}**"]
        lines.append("| " + " | ".join(row) + " |")

    lines += [
        "",
        "## 状态码分布 (连通性参考, 非本步决策依据)",
        "",
    ]
    status_ct = Counter(r["status"] for r in results)
    for s in sorted(status_ct, key=lambda k: -status_ct[k]):
        label = "timeout/error" if s == 0 else str(s)
        lines.append(f"- {label}: {status_ct[s]}")

    lines += [
        "",
        "## 口径说明",
        "",
        "- `origin`: 识别到 apache/nginx/iis/openresty 但无 CDN 标志, 视为直连源站",
        "- `unknown`: 无可识别特征 (私有 CDN / 无 server 头 / 定制网关)",
        "- `timeout`/`error`: 本轮未能建立连接, 不代表源失效 (可能是临时网络/CDN-level 拒绝)",
        "- 分类仅基于响应头; 同一域名可能叠加 Cloudflare→origin 链路, 本表记最外层",
        "",
        "---",
        f"Generated by `scripts/r14_cdn_fingerprint.py` @ commit {commit}",
    ]

    with open("docs/verification/cdn-distribution-r14.md", "w") as f:
        f.write("\n".join(lines) + "\n")

    print("[done] wrote docs/verification/cdn-distribution-r14.md + r14-cdn-raw.csv", file=sys.stderr)
    print("\n".join(lines))

if __name__ == "__main__":
    main()
