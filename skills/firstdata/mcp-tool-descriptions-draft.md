# MCP Tool Descriptions — Server-Side Draft

> **Purpose**: This file contains the exact text to be added to each tool's description in the MCP server Python code.
> After PR review approval, copy these Limitations sections into the server-side tool description strings.
> These texts must remain **identical** to the corresponding sections in `SKILL.md`.

---

## search_source — Add to description

```
**Limitations:**
- Maximum 200 results per query (limit range: 1–200, default: 20)
- Keywords are NOT auto-tokenized by spaces. Each keyword is matched as an exact substring. ["中国 GDP"] returns 0 results — use ["中国", "GDP"] instead
- Keyword matching is substring-based, not semantic search
- domain parameter uses substring matching, not exact enum matching
- No boolean operators (AND/OR/NOT). Multiple keywords use AND logic
- Subject to daily API call quota per token
```

## get_source — Add to description

```
**Limitations:**
- Invalid source_id does NOT set isError=true. Returns {"id": "xxx", "error": "Not found"} in the result array. Callers must check individual items for error fields
- No schema-level limit on source_ids count, but recommended ≤20 per request for reliable performance
- Subject to daily API call quota per token
```

## ask_agent — Add to description

```
**Limitations:**
- Query length: 2–1,000 characters
- Maximum results: 1–20 (default: 5)
- Non-idempotent: same query may return different results (LLM reasoning varies)
- Response time: typically 2–8 seconds; may reach 10–30+ seconds when web_search is triggered
- Subject to daily API call quota per token
```

## get_access_guide — Add to description

```
**Limitations:**
- Not all data sources have instruction libraries. Sources without pre-built instructions return empty or irrelevant results
- Invalid source_id returns {"error": "数据源 xxx 不存在"}
- top_k range: 1–5 (default: 3)
- Response time is highly variable: 3–20 seconds depending on RAG retrieval complexity and server load
- Retrieval quality depends on specificity of the operation parameter. Use specific action verbs and entity names
- Subject to daily API call quota per token
```

## report_feedback — Add to description + Example

```
**Limitations:**
- feedback_message length: 10–2,000 characters
- Non-idempotent: duplicate calls create duplicate feedback entries. Do not retry on success
- Subject to daily API call quota per token

**示例:**
- 链接失效反馈: feedback_message="链接失效：数据源 china-pbc 的 data_url 返回 404，无法访问。检索关键词：中国货币供应量"
- 数据过时反馈: feedback_message="数据内容过时：数据源 worldbank-open-data 的 update_frequency 标注为 quarterly，但实际已超过 6 个月未更新"
```

---

## Verification Evidence

Each limitation is backed by one of these sources:

| Limitation | Source |
|---|---|
| search_source limit: 1–200 | inputSchema `maximum: 200, minimum: 1` |
| Keywords not auto-tokenized | Tested: `["中国 GDP"]` → 0 results; `["中国", "GDP"]` → 173 results |
| Substring matching | Tested: `["中国GDP"]` → 1 result (exact substring); `["GDP"]` → 100 results |
| domain substring matching | inputSchema description: "领域关键词，子串匹配" |
| get_source silent error | Tested: invalid ID returns `{"id":"xxx","error":"Not found"}` with `isError: false` |
| get_source mixed valid/invalid | Tested: valid IDs return data, invalid return error objects, no request interruption |
| ask_agent query length | inputSchema `minLength: 2, maxLength: 1000` |
| ask_agent max_results | inputSchema `minimum: 1, maximum: 20, default: 5` |
| ask_agent non-idempotent | annotations `idempotentHint: false` |
| ask_agent response time | Tested 3 runs: 7.4s, 2.9s, 1.8s |
| get_access_guide invalid source | Tested: returns `{"error": "数据源 xxx 不存在"}` |
| get_access_guide top_k | inputSchema `minimum: 1, maximum: 5, default: 3` |
| get_access_guide response time | Tested 3 runs: 3.0s, 17.6s, 19.1s |
| report_feedback message length | inputSchema `minLength: 10, maxLength: 2000` |
| Daily call quota exists | TokenVerifyResponse schema: `quota_allowed`, `remaining_daily` fields |
| Trial quota: 30/day | Tested via `/api/trial/session-info`: `total_calls: 30` |
