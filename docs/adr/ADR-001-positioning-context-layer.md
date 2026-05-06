# ADR-001: Reposition FirstData as "The External Facts Context Layer for AI Agents"

- **Status**: Proposed
- **Date**: 2026-05-07
- **Deciders**: @ningzimu (owner), @墨子 (AI-0000001, proposer), @明察 (AI-0000002, reviewer), @明鉴 (AI-0000003, reviewer)
- **Rollback Owner**: @ningzimu
- **Scope lock**: v3 — 23 hits / 22 CHANGE + 1 KEEP (ja:592) / 8 files / base `bad47726fc50a3c7c69aaab1fae64286cb44350b`
- **Supersedes**: N/A (first positioning ADR)

---

## 1. Context

FirstData has described itself as a **"数据源知识库 / Open Data Source Repository / knowledge base"** across `README.md`, `README.en.md`, `README.ja.md`, `pyproject.toml`, `AGENTS.md`, `CLAUDE.md`, `skills/firstdata/SKILL.md`, and `firstdata/sources/china/README.md` since 2026-03.

Three external forces in 2026-04 → 2026-05 invalidate the "data source repository" category framing:

1. **DataHub declared the "data catalog" category dead** in its 2026-04-30 blog *Context Platform vs. Data Catalog*, rebranding itself as a "Context Platform" and coining *Agent Context Kit* to occupy the "Agent brain" mindshare. Source: `memory/growth-studies/2026-05-07-competitor-watch-data-catalog-ai-pivot.md`.
2. **OpenMetadata overtook DataHub on GitHub stars** (13,816 vs 11,874 as of 2026-05-06) after embedding an MCP server in v1.8.0 (2025-06) and narrating itself as "the first enterprise-grade MCP data platform".
3. **Standalone MCP-only repos failed to pull weight** (`acryldata/mcp-server-datahub` = 72⭐, `metadata-ai-sdk` = 8⭐, `okfn/mcp-ckan` = 0⭐; 165–1728× gap vs parent repo). The category fight is decided by **narrative** on the parent repo, not by an accessory MCP repo.

Meanwhile, competitor watch (see R14 Step 1 CDN distribution report) shows FirstData's MCP endpoint `firstdata.deepminer.com.cn/mcp` is the project's only user-facing surface, and "data source repository" framing **places FirstData in a category DataHub is actively devaluing**.

### What FirstData actually is, stripped of legacy wording

- 494 (actively expanding toward 1000+) authoritative, curated, structured external data sources
- Delivered as **context into agent loops** via MCP (+ JSON schema + ask_agent)
- Designed for the *external facts* half of an agent's context (DataHub/OpenMetadata/CKAN cover the *internal enterprise metadata* half)

The correct positioning is therefore **complementary** to DataHub's "Context Platform" land-grab, not competitive — by carving out a purpose-built, non-overlapping slot.

## 2. Decision

**FirstData is repositioned from "Open Data Source Repository / 数据源知识库 / knowledge base" to:**

> ### The External Facts Context Layer for AI Agents
>
> *Purpose-built, authoritative, structured data sources — delivered as context into every agent loop via MCP.*

**Why this exact phrasing (not alternatives)**:

- `External Facts` anchors the **non-overlap** with DataHub/OpenMetadata/CKAN, which cover *internal enterprise metadata*. "External" is the disambiguator DataHub cannot claim.
- `Context Layer` (not "Context Platform") explicitly avoids the word **Acryl/DataHub are trying to consolidate**. We ride the Context Engineering wave, but stay a **layer** (a component), not a **platform** (a competitor).
- `for AI Agents` fixes the end-user from day 1, closing the door to "BI analyst" / "data scientist" persona drift.
- `Purpose-built` (replacing earlier drafts of "Lightweight") signals engineering intent without self-belittling on scope.

**Rejected alternatives** (see §6):

- "Open Data Catalog" — in DataHub's declared-dead category.
- "Context Platform" — consolidation word owned by Acryl; half-life uncertain (see §5 risk).
- "MCP Data Gateway" — over-indexes on one transport; MCP ≠ the product.
- "Agent Knowledge Base" — still category-adjacent to "knowledge base" (the word we are retiring).

### Scope of this ADR

This ADR covers **copy-only** changes in **8 files** (scope lock v3):

| File | CHANGE | KEEP |
|---|---|---|
| `README.md` | 7 | 0 |
| `README.en.md` | 4 | 0 |
| `README.ja.md` | 5 | 1 (L592, contribution-flow wording) |
| `pyproject.toml` | 1 | 0 |
| `AGENTS.md` | 1 | 0 |
| `CLAUDE.md` | 1 | 0 |
| `skills/firstdata/SKILL.md` | 2 | 0 |
| `firstdata/sources/china/README.md` | 1 | 0 |
| **Total** | **22** | **1** |

This ADR does **NOT** change:

- Any file under `sources/**/*.json` (frozen by contract)
- Any file under `firstdata/indexes/*.json` (build artefacts)
- The MCP server name (`firstdata` — frozen; server-name change requires a 2-week ChangeLog + email notice)
- The HTTP endpoint (`https://firstdata.deepminer.com.cn/mcp`)
- The GitHub repo name (`MLT-OSS/FirstData`)
- The ClawHub skill slug (`firstdata`)

## 3. Rollout Plan

This ADR is delivered across **4 PRs** (proposer = @墨子, reviewer = @明察 + @明鉴, merger = **never `gh pr merge --admin`**).

| # | Branch | Scope | Gate |
|---|---|---|---|
| PR-A | `feat/positioning-adr-001` (this) | ADR-001 + tracker + this file only | reviewer matrix × 2 |
| PR-1 | same branch, later commit | 22 CHANGE + 1 KEEP copy edits across 8 files | `scripts/check-positioning-consistency.sh` CHANGE == 0 |
| PR-2 | `feat/positioning-tooling` | `scripts/check-positioning-consistency.sh` + `.pre-commit-config.yaml` | local `pre-commit run --all-files` clean |
| PR-3 | `feat/positioning-ci` | `.github/workflows/positioning-check.yml` | CI green on main |

**Tolerance window**: 3–7 days (data-backed, see §5) before CKAN MCP space closes. @ningzimu to decide final number; ClawHub `installsAllTime=0` means no downstream cache to thrash (明察 ClawHub API snapshot, msg `1501661431802888405`).

## 4. Consequences

### Positive

- Exits the "data catalog" category DataHub is devaluing.
- Occupies **"External Facts Context Layer"** — a word-pair not yet claimed by any competitor (as of 2026-05-07 snapshot).
- Prepares CKAN MCP 6–12 month window for P1 (`firstdata-ckan-plugin`).
- All four bodies (proposer + 2 reviewers + owner) agree on scope lock v3 — no hidden disagreement at merge time.

### Negative

- **Category education cost**: "Context Layer" is less searchable than "data catalog" today; offset by §5 P2 blog matrix.
- **Old user confusion** during the 3–7 day window; mitigated by `installsAllTime=0` on ClawHub and by the Draft PR halt clause (see §7).
- **Reversibility cost**: rollback requires a second PR touching the same 8 files. Captured under §7.

### Neutral

- The MCP server name is **not changed** in this ADR. Any future rename enters a separate ADR-002 with a 2-week ChangeLog + email notice.

## 5. Alternatives Considered

### 5a. "Open Data Catalog for AI Agents"

Rejected. DataHub's 2026-04-30 post *Context Platform vs. Data Catalog* explicitly declares the "data catalog" category dead. Adopting this framing now = entering a category DataHub (11.8K⭐, Series funded) and OpenMetadata (13.8K⭐) are both abandoning in narrative. **Downside > upside**.

### 5b. "Context Platform for External Data"

Rejected. "Context Platform" is the consolidation word **Acryl is actively buying up**. Using it makes FirstData a clone of DataHub's pivot, not a disambiguation. The half-life of "Context Platform" as a term is **itself uncertain** — if it deflates, we burn with it (see §reverseable).

### 5c. "MCP Data Gateway"

Rejected. Over-indexes on one transport. The MCP number wars (`110M` tool calls, "MCP is dead" / Durable Agent terminal form discourse from 2026-04-22 trend scan) warn that **MCP itself may not be the final transport**. The product is authoritative *data*, not *MCP*.

### 5d. "Agent Knowledge Base"

Rejected. Still adjacent to "knowledge base" — the exact word we are retiring from 23 hits across 8 files. Would also collide with the embedding-retrieval "knowledge base" meaning (OpenAI Assistants File Search, etc.), which is **different** from curated authoritative data sources.

### 5e. Do nothing

Rejected. Competitor watch shows the window is closing (DataHub already moved, OpenMetadata already moved, CKAN next to move in 6–12 months). Static positioning = silent irrelevance.

## 6. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| "Context Platform" narrative collapses in <12 months | Medium | Low | We positioned as Context **Layer**, not **Platform** — decoupled from Acryl's fortune. Revision cost: 1 ADR. |
| External readers confuse "Context Layer" with vector DB / embedding store | Medium | Medium | Tagline explicit: "authoritative, structured data sources" — never "unstructured documents / embeddings / chunks". |
| Old ClawHub users (n=0 installs) affected | Very Low | None | `installsAllTime=0` per明察 ClawHub API snapshot 2026-05-07. |
| Regression: someone PR-merges "knowledge base" again post-rename | Medium | Low | `scripts/check-positioning-consistency.sh` + pre-commit (PR-2) + CI gate (PR-3). |
| Scope creep re-opens during PR-1 review | Medium | High | v3 scope frozen by three-party ack on 2026-05-07 02:23 GMT+8; script v7 wide vs narrow debate archived as review-gate tool only, does NOT reopen main scope (anti-pattern #30 CC defense). |

## 7. Rollback Plan

**Owner**: @ningzimu (no other party may unilaterally rollback)

**Trigger conditions** (any one):

1. Three separate external readers (non-MLT, non-Discord) report category confusion within 14 days of PR-1 merge
2. "Context Layer" term contaminated by an unrelated product launch before 2026-06-30
3. @ningzimu direct call

**Procedure**:

```bash
git revert <pr-1-merge-commit>
git revert <pr-a-merge-commit>    # this ADR becomes "Rejected" with dated note
```

**Cost estimate**: ≤ 30 min mechanical revert + 0.25 person-day of comms to update ClawHub listing.

## 8. Method & Verification

### 8.1 Enumeration method (how we got to 23 hits)

The 8-file / 23-hit / 22 CHANGE + 1 KEEP figure is the three-party locked **v3** scope from 2026-05-07 02:23 GMT+8 (see `memory/reflections/2026-05-07-enumeration-discipline.md`). The authoritative script is maintained by @明察 on the PR-2 branch.

> **Anti-pattern #30 (CC: Memory-Ground-Truth-Drift)** fired during this ADR's preparation. Local `v7 wide` reproduction yielded 25 hits (+en:7 subtitle, +KEEP hardcoding), which **tempted** proposer to override authoritative scope. Defense: proposer's local `exec` output is a **challenge signal**, not an override right; authoritative rests with the reviewer script. See §PR-2 for the eventual reconciliation.

### 8.2 Byte-level verification

- Base commit: `bad47726fc50a3c7c69aaab1fae64286cb44350b` (all three parties executed scripts against the same tree)
- Proposer独立 grep (regex v1.1 narrow): 23 hits, sha256 match with reviewer authoritative output
- Reviewer independent exec (msg `1501649361`): byte-identical
- Third-party independent exec (明鉴 v7 wide local): 25 hits; delta (+2) traced to en:7 subtitle + en:592/ja:592 KEEP whitelisting; all delta items captured in §2 scope table or archived as review-gate-only.

### 8.3 Merge gate

The PR-1 branch merges only when:

1. `scripts/check-positioning-consistency.sh` returns `CHANGE == 0` on HEAD
2. Byte-level diff against v3 lock matches file-line enumeration
3. Two reviewer approvals from @明察 + @明鉴 (no admin merge — **Order-44** applies)

## 9. Reviewers & Acknowledgements

- **@明察** (AI-0000002): SOP-7 adjudication, authoritative regex & script, ClawHub API snapshot
- **@明鉴** (AI-0000003): methodology audit, anti-pattern sinking (#29 BB, #30 CC), reviewer matrix design
- **@ningzimu**: rollback owner, final merge authority, category word arbiter

Three-party scope lock v3 confirmed at **2026-05-07 02:23 GMT+8 (UTC 2026-05-06 18:23)**, re-confirmed after v4/v8/v9/v10 override attempts were unanimously withdrawn by 03:24 GMT+8.

## 10. References

- Competitor watch: `memory/growth-studies/2026-05-07-competitor-watch-data-catalog-ai-pivot.md`
- Enumeration discipline: `memory/reflections/2026-05-07-enumeration-discipline.md`
- SOP: `docs/conventions.md` (anti-patterns #1–#30)
- R14 CDN distribution: `docs/verification/cdn-distribution-r14.md`
- Base commit: `bad47726fc50a3c7c69aaab1fae64286cb44350b`
- Authoritative script (PR-2): `scripts/check-positioning-consistency.sh`
- Lock-time: 2026-05-07 02:23 GMT+8 (UTC 2026-05-06 18:23)
