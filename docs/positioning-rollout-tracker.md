# Positioning Rollout Tracker

> Living companion to `docs/adr/ADR-001-positioning-context-layer.md`.
> Edits merge into `main` only via reviewed PRs; no direct pushes.

## Scope Lock v3 (authoritative)

- **Locked**: 2026-05-07 02:23 GMT+8 (UTC 2026-05-06 18:23)
- **Re-confirmed**: 2026-05-07 03:24 GMT+8 (after v4/v8/v9/v10 override attempts withdrawn)
- **Base commit**: `bad47726fc50a3c7c69aaab1fae64286cb44350b`
- **Authoritative regex**: held by @明察 in PR-2's `scripts/check-positioning-consistency.sh`
- **Totals**: 23 hits / 22 CHANGE + 1 KEEP / 8 files (scope authority, v3 lock, @明察 SOP-7 msg `1501655057933013012`)
- **Base commit**: `bad47726fc50a3c7c69aaab1fae64286cb44350b`
- **Scope regex (v3 authority, 明鉴 super-wider)**: `知识库|ナレッジベース|知識ベース|オープンデータソースリポジトリ|データソースリポジトリ`
- **Tool (independent CI gate)**: `scripts/check-positioning-consistency.sh` v7 wide → 25 hits / 23 CHANGE / 2 KEEP (whitelist: en:592, ja:592). Number diff = regex coverage delta, legitimate.
- **Adjudication**: scope → @明察 v3 authority; tool → archived as CI gate, not scope

## Per-file breakdown (v3)

| File | Line | Content (excerpt) | Action |
|---|---|---|---|
| `README.md` | 7 | 全球最全面、最权威、最结构化的开源数据源知识库 | CHANGE |
| `README.md` | 9 | 全球最全面的权威数据源知识库 | CHANGE |
| `README.md` | 11 | Structured Open Data Source Repository | CHANGE |
| `README.md` | 32 | 权威数据源知识库 | CHANGE |
| `README.md` | 68 | Primary Sources knowledge | CHANGE |
| `README.md` | 148 | 结构化数据源知识库 | CHANGE |
| `README.md` | 150 | Structured 数据源知识库 | CHANGE |
| `README.en.md` | 7 | (subtitle) Open Data Source Repository — Agent First | CHANGE |
| `README.en.md` | 30 | authoritative knowledge base | CHANGE |
| `README.en.md` | 66 | primary-sources knowledge base | CHANGE |
| `README.en.md` | 146 | structured knowledge base | CHANGE |
| `README.ja.md` | 7 | オープンデータソースリポジトリ — Agent First | CHANGE |
| `README.ja.md` | 30 | 権威的ナレッジベース | CHANGE |
| `README.ja.md` | 66 | 一次情報ナレッジベース | CHANGE |
| `README.ja.md` | 146 | 構造化ナレッジベース | CHANGE |
| `README.ja.md` | 148 | 構造化データソースナレッジベース | CHANGE |
| `README.ja.md` | 592 | 公式にデータソースリポジトリに収録されます | **KEEP** (business-process wording, not category self-title) |
| `pyproject.toml` | 4 | description: "Open Data Source Repository ..." | CHANGE |
| `AGENTS.md` | 7 | 数据源知识库 | CHANGE |
| `CLAUDE.md` | 7 | 数据源知识库 | CHANGE |
| `skills/firstdata/SKILL.md` | 20 | 全球权威数据源知识库 | CHANGE |
| `skills/firstdata/SKILL.md` | 179 | 数据源知识库 | CHANGE |
| `firstdata/sources/china/README.md` | 186 | 中国数据源知识库 | CHANGE |

## Supersedes chain (for audit)

| Version | Status | Numbers | Source | Retired at |
|---|---|---|---|---|
| v3 | **AUTHORITATIVE** | 23 / 22 / 1 | @明察 SOP-7 adjudication | — |
| v4 | withdrawn | 24 / 24 / 0 | @墨子 symmetry-flip over en:592+ja:592 | 2026-05-07 03:05 |
| v7 | withdrawn | 22 / 22 / 1 (same as v3, different lock-time) | prior naming attempt | 2026-05-07 02:40 |
| v8 | withdrawn | 26 / 26 / 0 | @明察 v1.3 regex upgrade proposal | 2026-05-07 03:15 |
| v9 | withdrawn | 25 / 23 / 2 | @明鉴 local v7 wide exec override | 2026-05-07 03:24 |
| v10 | withdrawn | 26 / 23 / 3 | @墨子 compromise proposal (KEEP L592×2 + L593) | 2026-05-07 03:26 |

> All withdrawals are documented with message IDs in `memory/reflections/2026-05-07-enumeration-discipline.md`.

## PR Map

| PR | Branch | Scope | Status |
|---|---|---|---|
| PR-A | `feat/positioning-adr-001` | `docs/adr/ADR-001-*`, `docs/adr/README.md`, this tracker | Draft |
| PR-1 | same branch, later commit | 22 copy edits (CHANGE) across 8 files | Pending PR-A merge |
| PR-2 | `feat/positioning-tooling` | `scripts/check-positioning-consistency.sh`, `.pre-commit-config.yaml` | Pending |
| PR-3 | `feat/positioning-ci` | `.github/workflows/positioning-check.yml` | Pending PR-2 merge |

## Merge gate (applies to every PR above)

1. `scripts/check-positioning-consistency.sh` returns `CHANGE == 0` on HEAD (PR-1/PR-3 only; PR-A has no content diff, PR-2 adds the script)
2. Byte-level diff matches the per-file breakdown above (for PR-1)
3. Two reviewer approvals from @明察 + @明鉴
4. **NEVER `gh pr merge --admin`** — Order-44 applies

## Tolerance window

- **Proposal**: 3–7 days (data-backed by ClawHub `installsAllTime=0`)
- **Decider**: @ningzimu
- **Start**: time of PR-1 merge
- **Exit**: external facing surfaces (README, ClawHub description, `pyproject.toml`, SKILL.md) all read as "External Facts Context Layer" language

## Defensive artefacts

- `scripts/check-positioning-consistency.sh` (authoritative, PR-2)
- Three-language self-title cross-reference table (enforced by `KEEP_WHITELIST` empty after v3 close)
- Anti-pattern #29 BB (Cross-language-self-title-blindspot) and #30 CC (Memory-Ground-Truth-Drift) both sunk into `docs/conventions.md`
