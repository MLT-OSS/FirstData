# FirstData 🌐

English | **[中文](README.md)** | **[日本語](README.ja.md)**

---

**The World's Most Comprehensive, Authoritative, and Structured Open Data Source Repository**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Sources](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/MLT-OSS/FirstData/refs/heads/main/assets/badges/sources-count.json)](firstdata/indexes/statistics.json)
[![Progress](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/MLT-OSS/FirstData/refs/heads/main/assets/badges/progress.json)](firstdata/indexes/statistics.json)
[![Authority](https://img.shields.io/badge/Authority-Government%20%26%20International%20First-brightgreen.svg)](#)
[![MCP Server](https://img.shields.io/badge/MCP-AI%20Smart%20Search-purple.svg)](https://firstdata.deepminer.com.cn/)

---

## 🎯 Why FirstData?

### The Fact Defense Line in the AI Era: From "Information Overload" to "Truth Scarcity"

In today's era where Generative AI is reshaping the internet, **"information" has become unprecedentedly abundant, while "truth" is becoming scarce**.

When noise, patchwork content, and hallucinations become the default background, **trusted primary sources are no longer just reference materials, but the foundation of the entire intelligence system**.

### Our Mission: Building the Trusted Foundation for the AI Era

This project aims to build a **global, authoritative, and structured Primary Sources knowledge base**.

We systematically discover and aggregate high-trust sources across domains—covering scientific research, government disclosures, laws and regulations, corporate filings and financial reports, standards and authoritative industry materials—**transforming scattered, non-standard, difficult-to-reuse original content into traceable, verifiable, and citable "Core Facts"**, while preserving complete evidence chains and version history, ensuring that every conclusion can be traced "back to the source".

### This is a "Fact Defense Line" for the Large Model Era

✅ **Provide anti-hallucination, anti-poisoning trusted foundation for models**

- Plans to cover 1000+ authoritative data sources (all from government agencies, international organizations, academic institutions, and authoritative industry associations worldwide)
- 100% URL validation to ensure link availability

✅ **Provide computable, reviewable evidence chain closure for Deep Research**

- Structured metadata system with complete access paths
- Support programmatic access for automated evidence tracing

✅ **Upgrade AI from "vaguely summarizing secondary information" to "rigorous reasoning and citation based on primary evidence"**

- MCP intelligent Agent understands complex queries and accurately recommends authoritative data sources
- Provides complete paths to original data (URL, API, download methods)
- Includes use cases and citation examples to ensure proper usage

> **In the GenAI era, Clean Data > Big Model.**
>
> **Let every deep thought be built on verifiable facts.**

---

## 🚀 Core Advantages

| Feature | Our Unique Strengths | Value in the AI Era |
| ------- | -------------------- | ------------------- |
| 🇨🇳 **Deep Coverage of Chinese Data Sources** | **Global Exclusive**: Plans to include 500+ Chinese government data sources across core sectors | Fills the China gap in global data source directories, providing trusted Chinese data for cross-border research |
| 📊 **Structured Metadata System** | Complete metadata standards (access URLs, API interfaces, authority levels, update frequency, data content, etc.), not just links | Machine-readable, programmable access, supports automated evidence chain construction |
| ⭐ **Authority Level Classification** | Six authority levels: government, international organizations, research institutions, market, commercial, and others | Scientifically assess data source credibility, provide quality filtering basis for AI |
| 🤖 **AI Smart Search** | LLM-driven data source query Agent that understands complex multi-dimensional queries | Get authoritative data sources through natural language, no manual filtering needed |
| 🔌 **MCP Protocol Integration** | Provides standard MCP Server, integrable with Claude Desktop, Cline, and other AI applications | Enable any AI application to access the authoritative data source knowledge base |
| 🌍 **Bilingual Support** | All metadata provided in both Chinese and English | Connect global data ecosystems, break language barriers |
| 🔍 **100% Verification** | Every URL tested, every data source with complete documentation, every authority level with justification | Ensure data sources are genuinely available, avoid broken links and hallucinated citations |

---

## 📊 Data Source Overview

### Current Statistics

| Category | Count | Coverage |
| -------- | ----- | -------- |
| 🌍 **International Organizations** | 33 / 100+ | World Bank, IMF, OECD, WHO, FAO... |
| 🇨🇳 **Chinese Government** | 19 / 500+ | PBC, National Bureau of Statistics, Customs, CSRC... |
| 🌎 **Country Officials** | 25 / 200+ | USA, Canada, Japan, UK, Australia... |
| 🎓 **Academic Institutions** | 26 / 100+ | NBER, Penn World Table, PubMed... |
| 🏭 **Industry Sectors** | 32 / 100+ | Energy, Finance, Health, Climate... |
| **Total** | **135 / 1000+** | **13% Complete** |

### Completed Sources

#### 🌍 International Organizations (33)

📄 **Details**: [sources/international/README.md](sources/international/README.md)

#### 🇨🇳 Chinese Data Sources (19)

📄 **Details**: [sources/china/README.md](sources/china/README.md)

#### 🌎 Country Officials (25)

📄 **Details**: [sources/countries/README.md](sources/countries/README.md)

#### 🎓 Academic Research (26)

📄 **Details**: [sources/academic/README.md](sources/academic/README.md)

#### 🏭 Industry Sectors (32)

📄 **Details**: [sources/sectors/README.md](sources/sectors/README.md)

### Quality Assurance: Ensuring Every Data Source is a Trusted Foundation

- ✅ **100% URL Verification** - Every link is tested and available
- ✅ **Authority First** - Primarily includes government and international organization data sources
- ✅ **Metadata Validation** - All JSON files pass schema validation
- ✅ **Bilingual Documentation** - All data sources provide Chinese and English descriptions
- ✅ **Complete Evidence Chain** - Provides complete path from query to raw data

## 📐 Metadata Structure

Each data source contains **structured metadata** that supports machine-readable and automated evidence chain construction:

### Core Information

- **Unique ID**: Lowercase, hyphen-separated identifier
- **Name**: English, Chinese, and local language names
- **Organization**: Name, type, country, official website
- **Description**: Detailed bilingual description

### Access and Discovery

- **Primary URL**: Main data portal
- **API Information**: Availability, documentation, authentication requirements
- **Download Options**: Bulk download, supported formats (CSV, Excel, JSON, etc.)
- **Access Level**: Open, registration required, academic, commercial, restricted

### Coverage Details

- **Geographic Scope**: Global, regional, national, subnational
- **Countries/Regions**: Specific coverage areas
- **Time Range**: Start year, end year, update frequency
- **Sectors**: Economics, health, climate, energy, etc.
- **Data Content**: Specific data categories and content descriptions

### Authority Identification - Credibility Assurance for the AI Era

**authority_level field**: Authority level classification

- `government` - Government agencies
- `international` - International organizations
- `research` - Research institutions
- `market` - Market institutions
- `commercial` - Commercial institutions
- `other` - Others

**Complete Schema**: See [schemas/datasource-schema.json](schemas/datasource-schema.json)

## 🎯 FirstData MCP

**Connecting Natural Language with Primary Authoritative Data - The "Last Mile"**

---

We've built a structured knowledge base of authoritative data sources, each with complete metadata, access paths, and authority identifiers. But for most users, the real challenge is: How to quickly find the most suitable one among massive data sources? Once you find the data source website, how to accurately locate the target data on complex official platforms? How to seamlessly integrate all this into your daily AI workflow?

**FirstData MCP** is built for this purpose—transforming a static data source knowledge base into a dynamic intelligent navigation system, making authoritative data accessible to everyone.

---

### 📖 Why FirstData MCP?

In the LLM era, we're used to asking for answers directly, but often face two core pain points:

❌ **Pain Point 1: Untraceable Data Sources (Hallucination Risk)**

- AI-generated numbers may be outdated, incorrect, or completely fabricated
- Lack of original evidence chain, unable to trace and verify
- Secondary citations lose original context through layers of retelling

❌ **Pain Point 2: High Barrier to Professional Databases (Difficult Retrieval)**

- Government and international organization websites have complex navigation and obscure terminology
- Don't know which data source is most authoritative and what its coverage is
- Even after finding the official website, don't know how to locate target data

### 💡 Our Solution

**This MCP service builds a complete closure from "vague intent" to "precise data path":**

It doesn't directly generate potentially outdated numbers, but acts as an **"authoritative data guide"**, directing users to trusted primary sources such as national statistical bureaus, World Bank, industry white papers, etc., and provides **retrieval manuals with specific click-by-click steps**.

> **Let data return to authority, let retrieval no longer get lost.**

---

### ✨ Core Features

#### 1️⃣ Authoritative Source Locator

**Solving the "Where to find?" problem**

Based on users' natural language questions (e.g., "China's new energy vehicle exports in 2023"), intelligently recommend the most authoritative primary data source websites.

**Feature Highlights:**

- 🧠 **Understand Complex Queries**: Automatically identify multi-dimensional needs like geography + time + sector + authority
- 🎯 **Smart Recommendations**: Top 3-5 most relevant data sources with detailed matching reasons
- 📊 **Authority Guarantee**: All recommendations tagged with authority levels (government/international/research/market, etc.)
- 🔗 **Ready-to-Use Information**: Directly provide access URLs, API documentation, data formats
- ✅ **Complete Evidence Chain**: Every step from query to raw data is traceable
- 🌍 **Global Coverage**: Data sources cover major sectors globally, balancing breadth and depth

**Filter out marketing accounts and secondary citations, directly reach official websites, official reports, or professional databases.**

**Usage Examples:**

<details>
<summary><b>Example 1: Researcher - Developing Country Economic Data 📚</b></summary>

**Scenario**:

> "I want to research GDP information of developing countries for economic growth studies"

**Problems with Traditional Methods**:

- ❌ Google search filled with secondary reports, blog articles, outdated links
- ❌ Uncertain about data source authority and methodology
- ❌ Spend hours navigating institutional websites, still might find wrong data

**Using FirstData MCP:**

1. 🔍 **Natural Language Question**: "Developing country GDP"
2. 🎯 **Agent Auto-Filters**: World Bank, IMF, regional development banks
3. 📊 **Compare Authority Levels**: International organizations, government agencies, etc.

**Results:**

```
📋 Recommended Data Sources:

1. World Bank World Development Indicators
   - API: Supported (complete documentation)
   - Coverage: 217 countries and regions
   - Time Range: 1960-present
   - Authority Level: international (International Organization)
   - Evidence Chain: World Bank Official → Primary Data → Traceable

2. IMF World Economic Outlook
   - API: Supported
   - Coverage: 194 global economies
   - Update Frequency: Quarterly
   - Authority Level: international (International Organization)
```

**Value**:

- ✅ From "uncertain search" to "evidence-based research"
- ✅ Save hours of filtering time
- ✅ Avoid research conclusion bias from using wrong data sources

</details>

<details>
<summary><b>Example 2: Data Analyst - China Monetary Policy Data 💰</b></summary>

**Scenario**:

> "I need M1, M2 money supply and interest rate data for China in the past 10 years"

**Problems with Traditional Methods**:

- ❌ AI assistants may give outdated links or secondary websites
- ❌ Unclear about data update frequency and historical coverage
- ❌ Lack API access information, unable to automate retrieval

**MCP Workflow:**

1. 🔍 **Identify Keywords**: China + monetary policy + M1/M2 + 10-year time range
2. 🎯 **Filter Conditions**: Country=CN + Sector=Finance + Time coverage≥10 years
3. 📊 **Recommend Top Data Sources** (with evidence chain)

**Results:**

```
📋 Recommended Data Sources:

1. People's Bank of China (PBC)
   - Data Portal: http://www.pbc.gov.cn/diaochatongjisi/
   - API Documentation: Official interface available
   - Update Frequency: Monthly
   - Historical Coverage: 1990-present
   - Authority Level: government (Government Agency)
   - Evidence Chain: China Central Bank Official → Primary Data → Traceable

   📈 Available Data:
   - M0, M1, M2 Money Supply (Monthly)
   - Deposit and Loan Benchmark Rates
   - Interbank Lending Rates
```

**Value**:

- ✅ **Anti-Hallucination**: Ensure data from official authoritative agencies
- ✅ **Computable**: Provide API access, support automated data retrieval
- ✅ **Reviewable**: Complete metadata, anyone can verify data sources

</details>

<details>
<summary><b>Example 3: Policymaker - Global Climate Data 🌍</b></summary>

**Scenario**:

> "I need authoritative climate data to support policy decisions, need global data with API access"

**Risks**:

- ❌ Using unreliable data sources may lead to policy mistakes
- ❌ Lack methodology transparency, unable to assess data quality
- ❌ Secondary citations lack original evidence chain

**MCP Workflow:**

1. 🔍 **Multi-Dimensional Filtering**: Geographic scope=global + Sector=climate + Has API + High authority
2. 🎯 **Recommend Qualified Data Sources**
3. 📊 **Sort by Authority Level** (prioritize government and international organizations)
4. 📋 **Provide Complete Evidence Chain**

**Results:**

```
📋 Recommended Data Sources:

1. NASA Earthdata
   - Coverage: Global
   - API: Supported (complete documentation)
   - Data Types: Satellite observations, climate models
   - Authority Level: government (Government Agency)
   - Update Frequency: Real-time/Daily
   - Evidence Chain: NASA Official → Satellite Data → Verifiable

2. NOAA Climate Data Online
   - Coverage: Global
   - API: Supported
   - Update Frequency: Real-time/Daily
   - Authority Level: government (Government Agency)
   - Evidence Chain: US Government → Meteorological Monitoring → Traceable
```

**Value**:

- ✅ **Evidence Chain Closure**: From query → recommendation → raw data → completely traceable
- ✅ **Methodology Transparency**: Clear data collection methods and quality standards
- ✅ **Reproducible Research**: Other researchers can verify conclusions based on same data sources
- ✅ **Reduce Policy Risks**: From "uncertain decision basis" to "verifiable authoritative evidence"

</details>

---

#### 2️⃣ Site Pathfinder

**Solving the "How to find?" problem**

For professional websites with complex structures and obscure terminology, provides step-by-step operation manuals with complete navigation guidance from homepage to target data.

**Feature Highlights:**

- 📖 **Step-by-Step Operation Guide**: Clearly specify operation objects, key interface elements, filter condition settings for each step
- 🎯 **Multi-Path Assurance**: Provide main path + alternative solutions + API access, each path verified
- 🔍 **Precise Positioning**: Specific to button locations, filter settings, download steps, not general descriptions
- 💡 **Lower Barriers**: Non-professionals can quickly locate, from "hours of exploration" to "3-5 minutes precise retrieval"
- 🔄 **Regular Updates**: Manual verification of website changes, timely update of operation paths
- 🤖 **Smart Matching**: Recommend most relevant operation instructions based on user query intent

**Provide detailed website navigation guidance for commonly used authoritative data sources, precisely locate data positions.**

---

### 🚀 Complete Usage Example: Smart Search + Operation Manual One-Stop Solution

**Scenario: Finding IPO Prospectus of Newly Listed Tech Companies for Investment Research**

**User Question:**

> "I want to research a recently listed domestic AI tech company, need to find their IPO prospectus to analyze business model and financial status"

**✅ Complete FirstData MCP Workflow:**

#### 📋 Step 1: Smart Search for Trusted Data Sources

```
Recommended Data Sources:

1. Hong Kong Exchanges and Clearing Limited (HKEX)
   - Description: HKEX operates HKEXnews, providing official platform for
                 listed company prospectuses, annual reports, IPO information,
                 and regulatory filings
   - Access URL: https://www.hkexnews.hk
   - Authority Level: market (Market Institution)
   - Document Types: Prospectuses, annual reports, announcements
   - Evidence Chain: Official Disclosure Documents → Directly Citable

2. China Securities Regulatory Commission (CSRC)
   - Access URL: http://www.csrc.gov.cn
   - Overseas Listing Filing Information Query
   - Authority Level: government (Government Agency)
```

**Value Points:**

- ✅ **Avoid Hallucination**: Recommended official disclosure platforms, not news websites
- ✅ **Authority Guarantee**: Clearly tag authority level of data sources
- ✅ **Provide Key Clues**: Pre-provide financial summary information to help understand data background

#### 📖 Step 2: Get Website Operation Manual

MCP has built-in **operation manual database**, covering website navigation and download steps for commonly used authoritative data sources.

**Search HKEXnews Website Operation Instructions:**

```
source: https://www.hkexnews.hk
operation: How to find IPO prospectuses of newly listed companies?
```

**Manual Search Results:**

```
Website Operation Manual:

Main Path (Recommended):
1. Visit Hong Kong Stock Exchange HKEXnews homepage (https://www.hkexnews.hk)
2. Click "NEW LISTINGS" option in main navigation bar
3. Enter New Listing Information page
4. Select corresponding market segment (Main Board or GEM)
5. Find target company name or stock code in newly listed company list
6. Click corresponding prospectus download link (Prospectus)
7. Download PDF file

Alternative Path:
1. Visit Hong Kong Stock Exchange HKEXnews homepage
2. Use search function to input company name or stock code
3. Filter document type as "Prospectus" in search results
4. Select latest dated prospectus
5. Click download link to get PDF file
```

**Value Points:**

- ✅ **Ready-to-Use Guidance**: Provides step-by-step operation instructions, no manual exploration of website structure needed
- ✅ **Multi-Path Assurance**: Provides alternative solutions, ensures successful document retrieval
- ✅ **Lower Barriers**: Non-professionals can quickly locate official documents

#### 📊 Step 3: Analysis Based on Official Data

**Research Analysis Framework After Obtaining Prospectus:**

Based on official data disclosed in the prospectus, systematic analysis can be conducted:

**1. Business Model Analysis**

- **Core Business**: Understand company's main business and revenue sources from "Business Overview" section
- **Market Positioning**: Analyze target market, customer base, and competitive advantages
- **Profit Model**: Identify revenue structure, pricing strategy, and monetization paths

**2. Financial Status Analysis**

- **Revenue Trends**: Review historical financial data, analyze revenue growth rate and sustainability
- **Profitability**: Assess key indicators like gross margin, net margin
- **Cash Flow**: Study operating cash flow, financing purposes, and capital reserves

**3. Risk Factor Assessment**

- **Business Risks**: Main risks listed in "Risk Factors" section of prospectus
- **Financial Risks**: Debt level, liquidity, solvency
- **Industry Risks**: Market competition, technological changes, regulatory policy changes

**4. Investment Value Judgment**

- **Growth Potential**: Assess growth space based on business planning and market prospects
- **Valuation Reasonableness**: Compare P/E ratio, P/S ratio and other indicators with industry peers
- **Use of Proceeds**: Whether IPO fund usage plan aligns with strategic goals

**✅ Complete Evidence Chain Closure:**

```
User Raises Research Need
  ↓
MCP Smart Search Recommends Authoritative Data Source (HKEX)
  ↓
Get Website Operation Manual (Step-by-Step Navigation Guidance)
  ↓
Download Official Prospectus (Primary Authoritative Document)
  ↓
Conduct Systematic Analysis Based on Official Disclosure Data
  ↓
All Conclusions Traceable to Original Documents for Verification
```

**Core Value:**

- ✅ **Anti-Hallucination**: Recommended official HKEX disclosure platform, not news websites or AI-generated content
- ✅ **Verifiable**: Complete evidence chain, anyone can obtain same raw data following the path
- ✅ **Ready-to-Use Guidance**: Provides step-by-step operation instructions, from "don't know where to find" to "3-5 minutes precise retrieval"
- ✅ **Multi-Path Assurance**: Main path + alternative solutions + search function, ensures successful document download

---

## 🚀 Quick Start

### Integrate FirstData MCP

**Configure FirstData MCP to your AI application for intelligent search of authoritative data sources and operation manual navigation**

Supports multiple platforms: Claude Desktop, Cline (VS Code), Zed, Cursor, and all AI applications compatible with MCP protocol.

---

#### Configuration Guide: Choose Based on Your Platform

> **📝 Important Note**
>
> **Apply for API Key (Required)**: Before configuring the MCP server, please visit [FirstData API Application](https://firstdata.deepminer.com.cn/) to apply for a free API key. Replace all `<YOUR_FIRSTDATA_API_KEY>` in the configuration examples below with your actual API key.

---

<details>
<summary><b>Claude Desktop</b></summary>

**Manual JSON Configuration**

1. **Find Configuration File**:

   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`
2. **Add Configuration**:

   ```json
   {
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```
3. **Restart Claude Desktop** to apply configuration

</details>

<details>
<summary><b>Cline (VS Code Extension)</b></summary>

1. **Open Cline MCP Settings**:

   - Open Cline in VS Code
   - Click settings icon → **Advanced MCP settings**
   - Or directly edit `cline_mcp_settings.json`
2. **Add Configuration**:

   ```json
   {
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```

   > **Tip**: The `autoApprove` field allows commonly used read-only tools to execute automatically without confirmation each time.
   >
3. **After saving configuration**, Cline will automatically load the MCP server

Reference: [Cline MCP Configuration Docs](https://docs.cline.bot/mcp/configuring-mcp-servers)

</details>

<details>
<summary><b>Zed Editor</b></summary>

1. **Create Configuration File**:

   - Create `.zed/settings.json` in project root directory
   - Or use global configuration: `~/.config/zed/settings.json`
2. **Add Configuration**:

   ```json
   {
     "context_servers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         },
         "enabled": true
       }
     }
   }
   ```

   > **Note**: Zed uses `context_servers` instead of `mcpServers`
   >
3. **Reload Zed** or restart project to apply configuration

</details>

<details>
<summary><b>Cursor Editor</b></summary>

1. **Open Cursor Settings**:

   - `Cmd/Ctrl + Shift + P` → Search "MCP Settings"
   - Or go to `Cursor Settings` → `MCP` → `New MCP Server`
2. **Add Configuration**:

   ```json
   {
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```
3. **Restart Cursor** to load MCP server

</details>

<details>
<summary><b>Copilot / VS Code</b></summary>

**Recommended Method: HTTP Server**

1. Reference [VS Code MCP Configuration Guide](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server)
2. Add configuration to VS Code MCP settings:

   ```json
   {
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```

**Using VS Code CLI:**

```bash
code --add-mcp '{"name":"firstdata","type":"streamable-http","url":"https://firstdata.deepminer.com.cn/mcp","headers":{"Authorization":"Bearer <YOUR_FIRSTDATA_API_KEY>"}}'
```

</details>

<details>
<summary><b>Copilot CLI</b></summary>

Use HTTP server method to connect:

```json
   {
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
```

</details>

<details>
<summary><b>Windsurf</b></summary>

1. **Open Windsurf MCP Configuration**:

   - Reference [Windsurf MCP Configuration Guide](https://docs.windsurf.com/windsurf/cascade/mcp#mcp-config-json)
2. **Add Configuration**:

   ```json
   {
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```

</details>

<details>
<summary><b>JetBrains AI Assistant & Junie</b></summary>

1. **Open JetBrains IDE Settings**:

   - Go to `Settings | Tools | AI Assistant | Model Context Protocol (MCP)`
   - Or `Settings | Tools | Junie | MCP Settings`
2. **Click `Add` and add the following configuration**:

   ```json
   {
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```

</details>

<details>
<summary><b>Warp Terminal</b></summary>

1. **Open Warp Settings**:

   - Go to `Settings | AI | Manage MCP Servers`
2. **Click `+ Add` to add MCP server**:

   ```json
   {
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```

Reference: [Warp MCP Configuration Docs](https://docs.warp.dev/knowledge-and-collaboration/mcp#adding-an-mcp-server)

</details>

<details>
<summary><b>Gemini CLI</b></summary>

Reference [Gemini CLI MCP Configuration Guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md), use the following configuration:

```json
    {
      "mcpServers": {
        "firstdata": {
          "type": "streamable-http",
          "url": "https://firstdata.deepminer.com.cn/mcp",
          "headers": {
            "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
          }
        }
      }
    }
```

</details>

<details>
<summary><b>Gemini Code Assist</b></summary>

Reference [Gemini Code Assist MCP Configuration Guide](https://cloud.google.com/gemini/docs/codeassist/use-agentic-chat-pair-programmer#configure-mcp-servers), use the following configuration:

```json
{
  "mcpServers": {
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Factory CLI (Droid)</b></summary>

Reference [Factory CLI MCP Configuration Docs](https://docs.factory.ai/cli/configuration/mcp), use the following configuration:

```json
{
  "mcpServers": {
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Qoder & Qoder CLI</b></summary>

1. Open **Qoder Settings**
2. Go to `MCP Server` → `+ Add`
3. Add the following configuration:
   ```json
   {
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```

Reference: [Qoder MCP Configuration Docs](https://docs.qoder.com/user-guide/chat/model-context-protocol)

</details>

<details>
<summary><b>Kiro</b></summary>

**Method 1: Via Kiro Settings**

1. Open **Kiro Settings**
2. Go to `Configure MCP` → `Open Workspace or User MCP Config`

**Method 2: Via Activity Bar**

1. Select `Kiro` from IDE **Activity Bar**
2. Go to `MCP Servers` → `Click Open MCP Config`

**Configuration Content:**

```json
{
  "mcpServers": {
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
      }
    }
  }
}
```

</details>

<details>
<summary><b>OpenCode</b></summary>

1. **Create or edit configuration file**:

   - Path: `~/.config/opencode/opencode.json`
   - Create it if the file doesn't exist
2. **Add the following configuration**:

   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "mcpServers": {
       "firstdata": {
         "type": "streamable-http",
         "url": "https://firstdata.deepminer.com.cn/mcp",
         "headers": {
           "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
         }
       }
     }
   }
   ```

Reference: [OpenCode MCP Configuration Docs](https://opencode.ai/docs/mcp-servers)

</details>

<details>
<summary><b>Visual Studio</b></summary>

Reference Visual Studio MCP configuration documentation, use the following configuration:

```json
{
  "mcpServers": {
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Codex</b></summary>

Reference [Codex MCP Configuration Guide](https://github.com/openai/codex/blob/main/docs/advanced.md#model-context-protocol-mcp), use the following configuration:

```json
{
  "mcpServers": {
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_FIRSTDATA_API_KEY>"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Amp</b></summary>

Reference [Amp MCP Configuration Docs](https://ampcode.com/manual#mcp), use the following configuration:

```json
{
  "mcpServers": {
    "firstdata": {
      "type": "http",
      "url": "http://localhost:8001/mcp",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

</details>

---

#### Usage Instructions

**After configuration**, you can ask questions in natural language on MCP-supported AI platforms:

**Example Questions**:

- "Help me find the M2 money supply data source from the People's Bank of China"
- "I need global climate data with API access, recommend authoritative sources"
- "Find listed company disclosure information on Hong Kong Stock Exchange"
- "Where can I find GDP data for developing countries?"

The search Agent will find and recommend the most authoritative data sources for you.

## 🤝 How to Contribute

### Recommend New Data Sources

Found an authoritative and trusted data source? Welcome to recommend it to us!

**Recommendation Process:**

1. [Submit an Issue](Link) explaining data source information and recommendation reasons
2. We'll evaluate its authority, data quality, and credibility
3. Once evaluated, it will be officially included in the data source repository

**Inclusion Criteria:**

- ✅ Official government data sources (national, provincial, local levels)
- ✅ Official international organization data
- ✅ Top academic institutions and research repositories
- ✅ Regularly updated authoritative industry data

## 💬 Community and Support

Join our community to connect with data researchers, developers, and contributors!

### WeChat Group

<div align="center">
  <img src="docs/images/wechat-qrcode.png" alt="WeChat Group QR Code" width="300"/>
  <p><i>Scan to join WeChat group</i></p>
</div>

> 💡 **Benefits of Joining**:
> - Discuss data source recommendations and usage experiences
> - Get technical support and best practices
> - Participate in project development and contributions
> - Learn about latest data source updates and feature releases

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

<p align="center">
  <strong>Building the Trusted Foundation for AI Era | Every Deep Thought Based on Verifiable Facts</strong>
</p>

<p align="center">
  <sub>Made with ❤️ by the FirstData Community</sub>
</p>

<p align="center">
  <a href="#-why-firstdata">Why</a> •
  <a href="#-core-advantages">Core Advantages</a> •
  <a href="#-data-source-overview">Data Sources</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-how-to-contribute">Contribute</a>
</p>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MLT-OSS/FirstData&type=date&legend=top-left)](https://www.star-history.com/#MLT-OSS/FirstData&type=date&legend=top-left)
