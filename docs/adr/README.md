# Architecture Decision Records (ADR)

This directory captures architectural / strategic decisions for FirstData. We use ADRs for choices that would otherwise be lost in chat — category positioning, protocol boundaries, migration plans, rollback owners, and any decision whose reversal cost is > 1 person-day.

## Conventions

- **File name**: `ADR-<NNN>-<kebab-case-title>.md`
- **Status values**: `Proposed` → `Accepted` → (`Deprecated` | `Superseded by ADR-<NNN>` | `Rejected`)
- **Status transitions are commit-visible**: change the `Status:` field in a dated follow-up commit; never rewrite history.
- **Scope**: one ADR per decision. Do not bundle unrelated decisions for convenience.
- **Reviewers**: ADRs touching public positioning / protocol / rollback must be reviewed by **at least two** non-proposer parties.

## Index

| ID | Status | Title | Date |
|---|---|---|---|
| [ADR-001](./ADR-001-positioning-context-layer.md) | Proposed | Reposition FirstData as "The External Facts Context Layer for AI Agents" | 2026-05-07 |

## Workflow

1. Proposer copies the template (or an existing ADR) into a branch `feat/adr-<NNN>-<slug>`.
2. Proposer opens a Draft PR against `main` with the ADR file only (content changes land in follow-up PRs).
3. Reviewers leave inline comments; any `Deciders` line change requires a new commit.
4. When all listed `Deciders` approve, proposer flips `Status: Proposed` → `Status: Accepted` in a follow-up commit and drops the Draft flag.
5. Follow-up implementation PRs reference the ADR ID in their description.

## Rollback

Every ADR that can be reverted must have a `Rollback Plan` section that names a **single** rollback owner. No party other than the rollback owner may initiate revert.
