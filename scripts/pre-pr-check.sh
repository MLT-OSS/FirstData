#!/usr/bin/env bash
# scripts/pre-pr-check.sh
#
# Local secrecy linter for PR body / title / branch name before `gh pr create`
# or `gh pr edit --body-file`. Mirrors .github/workflows/secrecy-check.yml so
# failures surface locally instead of being caught by CI after the PR opens.
#
# Usage:
#   scripts/pre-pr-check.sh --body-file /tmp/body.md [--title "..."] [--branch "feat/..."]
#   scripts/pre-pr-check.sh --body "inline body text"
#   scripts/pre-pr-check.sh --stdin < body.md
#   scripts/pre-pr-check.sh --scan-sources           # same scan CI does for firstdata/sources
#
# Exit code: 0 = clean, 1 = confidential term found.
#
# Keep the BANNED_TERMS list in sync with .github/workflows/secrecy-check.yml.
set -euo pipefail

BANNED_TERMS=(
  "langfuse"
  "insight pipeline"
  "gitlab"
  "code.mlamp.cn"
  "codex.mlamp.cn"
  "glab"
  "im.deepminer"
  "im-test.xming"
)

BODY=""
BODY_FILE=""
TITLE=""
BRANCH=""
SCAN_SOURCES=0
READ_STDIN=0

usage() {
  sed -n '2,18p' "$0"
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --body)         BODY="$2"; shift 2 ;;
    --body-file)    BODY_FILE="$2"; shift 2 ;;
    --title)        TITLE="$2"; shift 2 ;;
    --branch)       BRANCH="$2"; shift 2 ;;
    --stdin)        READ_STDIN=1; shift ;;
    --scan-sources) SCAN_SOURCES=1; shift ;;
    -h|--help)      usage ;;
    *)              echo "Unknown arg: $1" >&2; usage ;;
  esac
done

if [[ -n "$BODY_FILE" ]]; then
  if [[ ! -f "$BODY_FILE" ]]; then
    echo "::error::body file not found: $BODY_FILE" >&2
    exit 2
  fi
  BODY="$(cat "$BODY_FILE")"
fi

if [[ "$READ_STDIN" -eq 1 ]]; then
  BODY="$(cat)"
fi

if [[ -z "$BRANCH" ]] && command -v git >/dev/null 2>&1; then
  BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
fi

found=0

check_field() {
  local label="$1"
  local text="$2"
  [[ -z "$text" ]] && return 0
  local lower_text
  lower_text=$(printf '%s' "$text" | tr '[:upper:]' '[:lower:]')
  for term in "${BANNED_TERMS[@]}"; do
    local lower_term
    lower_term=$(printf '%s' "$term" | tr '[:upper:]' '[:lower:]')
    if [[ "$lower_text" == *"$lower_term"* ]]; then
      echo "🔴 BLOCKED: '$term' found in $label" >&2
      found=1
    fi
  done
}

check_field "branch name"    "$BRANCH"
check_field "PR title"       "$TITLE"
check_field "PR description" "$BODY"

if [[ "$SCAN_SOURCES" -eq 1 ]]; then
  repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  src_dir="$repo_root/firstdata/sources"
  if [[ -d "$src_dir" ]]; then
    for term in "${BANNED_TERMS[@]}"; do
      matches=$(grep -ril "$term" "$src_dir" 2>/dev/null || true)
      if [[ -n "$matches" ]]; then
        echo "🔴 '$term' found in source files:" >&2
        printf '  %s\n' $matches >&2
        found=1
      fi
    done
  fi
fi

if [[ "$found" -eq 1 ]]; then
  echo "::error::PR metadata or sources contain confidential term(s). Rewrite before opening / updating the PR." >&2
  exit 1
fi

echo "✅ Pre-PR secrecy check passed."
