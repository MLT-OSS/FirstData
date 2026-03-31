---
name: firstdata
description: Find official portals, APIs, and download paths for authoritative primary data sources (governments, international organizations, research institutions, etc.). Use when users need to know "where to find this data from an official source", "which source is more authoritative", or "how to cite primary data". Covers 1000+ global data sources with authority comparison and site navigation guidance.
version: 0.0.2
metadata:
  openclaw:
    homepage: https://github.com/MLT-OSS/FirstData
    primaryEnv: FIRSTDATA_API_KEY
    emoji: "📊"
    requires:
      env:
        - FIRSTDATA_API_KEY
      bins:
        - curl
---
# FirstData

## What FirstData Is

FirstData is a structured knowledge base of authoritative primary data sources, covering 1000+ sources to help agents locate official origins rather than generating unverified answers.

It does not replace raw data — it acts as an "authoritative data navigator", taking vague user needs as input, recommending the most appropriate primary sources, and providing clear access paths, API information, and download methods so both users and agents can trace back to original evidence.

**Coverage**:

- International organizations: World Bank, IMF, OECD, WHO, FAO, etc.
- Chinese government agencies: PBC, National Bureau of Statistics, General Administration of Customs, CSRC, etc.
- National official agencies: US, Canada, Japan, UK, Australia, etc.
- Academic & research databases: NBER, Penn World Table, PubMed, etc.
- Corporate disclosure & market platforms: stock exchange disclosure systems, listed company filings, etc.
- Industry-specific databases: energy, finance, health, climate, legal & regulatory, etc.

**When to use**: When users need to find official data sources, compare source authority, obtain official URLs/APIs/download paths, or build evidence-chain workflows. FirstData is a source locator, not an answer generator — after receiving results, guide users back to original sources for verification rather than treating them as final answers.

## Capabilities

**1. Source Locator** — Returns the top 3–5 most relevant sources with authority level, matching rationale, access URL, API documentation, and download methods.

**2. Site Pathfinder** — Provides step-by-step navigation from homepage to target data for complex official websites, including alternative paths and API access methods.

**3. Evidence-Ready Workflows** — Can be embedded into workflows requiring evidence chains: deep research, policy analysis, investment research, compliance auditing, fact-checking, etc.

Each data source includes structured metadata: authority level (`government` / `international` / `research` / `market` / `commercial` / `other`), access URL, API information, download formats, geographic scope, update frequency, access level, etc.

## Typical Queries

Typical query scenarios when agents call FirstData via MCP:

| User Need                                                                 | Query Direction                              | Expected Output                                               |
| ------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------- |
| "Which official source should I cite for China's 2023 NEV export volume?" | China Customs, National Bureau of Statistics | Official source + authority level + data page URL             |
| "Where to download IPO prospectus for a Hong Kong-listed company?"        | HKEXnews                                     | Official platform + step-by-step navigation                   |
| "World Bank vs IMF GDP data — which is better for academic citation?"    | World Bank WDI, IMF WEO                      | Source comparison + authority differences + API docs          |
| "Need global climate data with API access"                                | NASA Earthdata, NOAA CDO                     | Data source + API docs + access methods                       |
| "Where is the official data for China's M2 money supply?"                 | People's Bank of China                       | Official data portal + update frequency + historical coverage |

Full project background and feature documentation: [README](https://raw.githubusercontent.com/MLT-OSS/FirstData/refs/heads/main/README.md)

## Quick Start

This skill connects to the FirstData MCP server (`firstdata.deepminer.com.cn`), the project's official hosted API endpoint. An API key (`FIRSTDATA_API_KEY`) is required for authentication.

**If you already have `FIRSTDATA_API_KEY` set**, configure the MCP connection:

```bash
npx mcporter config add firstdata https://firstdata.deepminer.com.cn/mcp --header 'Authorization=Bearer ${FIRSTDATA_API_KEY}'
```

Or add manually to your MCP config:

```json
{
  "mcpServers": {
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <FIRSTDATA_API_KEY>"
      }
    }
  }
}
```

**If you don't have an API key**, see [firstdata-register.md](references/firstdata-register.md) for the registration process (two API calls to the FirstData server to obtain a JWT token).

Once connected, browse the tool list provided by the firstdata MCP and select the appropriate tool based on your needs.

## MCP Tools Reference

The FirstData MCP server provides 5 tools. Below is a reference with usage guidelines, limitations, and examples.

### Common Limitations (all tools)

- **Authentication required**: All tools require a valid API key (JWT token) via `Authorization: Bearer <token>` header.
- **Daily call quota**: API usage is subject to a per-token daily call quota. Quota varies by API key tier (trial accounts: 30 calls/day). There is currently no client-facing API to query remaining quota at runtime — callers should implement their own usage tracking if quota management is needed.
- **Network dependency**: All tools make HTTP calls to the FirstData server (`firstdata.deepminer.com.cn`). Network latency and server availability affect response times.

### Tool: `search_source`

**Purpose**: Unified data source search tool supporting keyword search, structured filtering, pagination, and multiple output modes.

**Limitations**:
- Maximum **200** results per query (`limit` parameter range: 1–200, default: 20).
- ⚠️ **Each keyword is matched as an independent substring — pass each search term as a separate array element.** For example, use `["中国", "GDP"]` (173 results) instead of `["中国 GDP"]` (0 results). This is by design to preserve multi-word terms like `"New Zealand"` or `"World Bank"`.
- Keyword matching is **substring-based**, not semantic search. Keywords are matched against source metadata fields (name, description, tags, content).
- The `domain` parameter uses **substring matching**, not exact enum matching (e.g., `"finance"` matches `"public-finance"`, `"finance"`, `"financial-markets"`).
- No boolean operators (AND/OR/NOT). Multiple keywords in the array are combined with AND logic.
- Response time: typically **~1 second**.

### Tool: `get_source`

**Purpose**: Retrieve full details for specific data sources by their IDs.

**Limitations**:
- Invalid `source_id` values do NOT cause an error response (`isError: false`). Instead, the result array includes `{"id": "xxx", "error": "Not found"}` for each invalid ID alongside valid results. Callers must check individual items for `error` fields rather than relying solely on `isError`.
- No schema-level limit on the number of `source_ids` per request, but performance with large batches (50+) is unverified. As a practical guideline (not a hard limit), consider batching in groups of ~20.
- The `fields` parameter filters returned fields; when omitted, all fields are returned.

### Tool: `ask_agent`

**Purpose**: LLM-powered intelligent search agent for complex, cross-domain, or ambiguous queries that require multi-step reasoning.

**Limitations**:
- Query length: 2–1,000 characters.
- Maximum results: 1–20 (default: 5).
- **Non-idempotent**: Same query may return different results across calls (LLM reasoning varies).
- **Response time: typically 2–8 seconds** (involves LLM inference). May take longer (10–30+ seconds) when the agent triggers `web_search` for external information.
- Internally uses LangChain ReAct agent with `jq` for local data queries plus optional `web_search`. The web search step is not user-controllable.
- **Use `search_source` instead** for simple keyword matching or structured filtering — it is faster, deterministic, and cheaper.

### Tool: `get_access_guide`

**Purpose**: Generate detailed access instructions for a specific data source using RAG (Retrieval-Augmented Generation).

**Limitations**:
- **Not all data sources have instruction libraries.** If a source has no pre-built instructions, results will be empty or irrelevant.
- Invalid `source_id` returns `{"error": "数据源 xxx 不存在"}`.
- `top_k` range: 1–5 (default: 3).
- **Response time is highly variable: 3–20 seconds**, depending on RAG retrieval complexity and server load.
- Retrieval quality depends heavily on the specificity of the `operation` parameter. Vague descriptions yield lower-quality matches. Use specific action verbs and entity names (e.g., "查询2024年M2货币供应量数据" rather than "查数据").

### Tool: `report_feedback`

**Purpose**: Submit user feedback to the development team when FirstData has a confirmed issue.

**Limitations**:
- `feedback_message` length: 10–2,000 characters.
- **Non-idempotent**: Duplicate calls create duplicate feedback entries. Do not retry on success.
- Only use when a genuine issue is confirmed (missing source, incorrect data, broken functionality). Do not use as a general comment channel.

**Examples**:

```
# Example 1: Broken link
feedback_message="链接失效：数据源 china-pbc 的 data_url (https://www.pbc.gov.cn/diaochatongjisi/116219/index.html) 返回 404，无法访问数据页面。检索关键词：中国货币供应量"

# Example 2: Outdated or inaccurate content
feedback_message="数据内容过时：数据源 worldbank-open-data 的 update_frequency 标注为 quarterly，但实际数据页面显示最近更新日期为 2024-06-30，已超过 6 个月未更新。建议核实并修正更新频率或标注数据滞后情况"
```

## Description Quality Guidelines

When adding or modifying MCP tool descriptions, follow these principles (based on [MCP tool description quality research](https://arxiv.org/abs/2602.14878)):

**Core principle: "Write it right before writing it all"** — Functionality accuracy (+11.6% impact) matters ~8× more than Conciseness (+1.5%).

**6-dimension checklist** (check all before submitting):

- [ ] **Purpose**: Is the tool's function clearly stated in the first sentence?
- [ ] **Guidelines**: Are usage scenarios and when-to-use / when-not-to-use rules included?
- [ ] **Examples**: Are typical input/output examples provided?
- [ ] **Limitations**: Are constraints, edge cases, and known limitations documented?
- [ ] **Parameters**: Are all parameters described with types, ranges, and defaults?
- [ ] **Return Format**: Is the response structure documented?

## Community

FirstData is an open-source project — join us in building the authoritative data source knowledge base for agents:

- ⭐ [**Star**](https://github.com/MLT-OSS/FirstData) the project to help more agents and developers discover it
- 📝 [**Issue**](https://github.com/MLT-OSS/FirstData/issues) to report problems, suggest new data sources, or propose improvements
- 🔀 [**PR**](https://github.com/MLT-OSS/FirstData/pulls) to contribute code, data sources, or documentation improvements
