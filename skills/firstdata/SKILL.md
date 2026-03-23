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

## Community

FirstData is an open-source project — join us in building the authoritative data source knowledge base for agents:

- ⭐ [**Star**](https://github.com/MLT-OSS/FirstData) the project to help more agents and developers discover it
- 📝 [**Issue**](https://github.com/MLT-OSS/FirstData/issues) to report problems, suggest new data sources, or propose improvements
- 🔀 [**PR**](https://github.com/MLT-OSS/FirstData/pulls) to contribute code, data sources, or documentation improvements
