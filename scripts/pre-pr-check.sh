#!/usr/bin/env bash
# scripts/pre-pr-check.sh
#
# Local secrecy linter. Mirrors .github/workflows/secrecy-check.yml so banned
# terms are caught locally *before* they end up on GitHub / Discord webhooks.
#
# Scope (anywhere reviewers or webhooks will echo the text back):
#   * PR body / title / branch name before `gh pr create` or `gh pr edit`
#   * PR review body (`gh pr review --body`)
#   * PR / issue comments that reference a fix (don't quote the banned word!)
#   * Commit messages, release notes, wiki entries
#
# Webhooks (Discord etc.) cache the *original* payload even after GitHub edits,
# so "edit afterwards" is not a real fix. Always lint before sending.
#
# Usage:
#   scripts/pre-pr-check.sh --body-file /tmp/body.md [--title "..."] [--branch "feat/..."]
#   scripts/pre-pr-check.sh --body "inline body text"
#   scripts/pre-pr-check.sh --text "any arbitrary text blob"   # review body, comment, commit msg
#   scripts/pre-pr-check.sh --stdin < body.md
#   scripts/pre-pr-check.sh --scan-sources           # same scan CI does for firstdata/sources
#   scripts/pre-pr-check.sh --tags-lint              # scan firstdata/sources tags for ASCII
#                                                   # uppercase or duplicate (case-insensitive)
#                                                   # violations — complements CI / style guide
#
# Exit code: 0 = clean, 1 = confidential term or tags violation found, 2 = usage error.
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
TEXT=""
SCAN_SOURCES=0
READ_STDIN=0
TAGS_LINT=0

usage() {
  sed -n '2,28p' "$0"
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --body)         BODY="$2"; shift 2 ;;
    --body-file)    BODY_FILE="$2"; shift 2 ;;
    --title)        TITLE="$2"; shift 2 ;;
    --branch)       BRANCH="$2"; shift 2 ;;
    --text)         TEXT="$2"; shift 2 ;;
    --review-body)  TEXT="$2"; shift 2 ;;   # alias of --text (reviewer-side)
    --stdin)        READ_STDIN=1; shift ;;
    --scan-sources) SCAN_SOURCES=1; shift ;;
    --tags-lint)    TAGS_LINT=1; shift ;;
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
check_field "text blob"      "$TEXT"

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

if [[ "$TAGS_LINT" -eq 1 ]]; then
  repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  src_dir="$repo_root/firstdata/sources"
  if [[ ! -d "$src_dir" ]]; then
    echo "::error::--tags-lint: sources dir not found at $src_dir" >&2
    exit 1
  fi
  python3 - "$src_dir" <<'PY'
import json, pathlib, re, sys
src = pathlib.Path(sys.argv[1])
ascii_re = re.compile(r'^[\x20-\x7E]+$')
violations_upper = []   # (file, tag)
violations_dup   = []   # (file, tag_lower, originals)
parse_errors = []
for f in sorted(src.rglob('*.json')):
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        parse_errors.append((str(f), str(e)))
        continue
    tags = d.get('tags') or []
    if not isinstance(tags, list):
        continue
    # ASCII uppercase check
    for t in tags:
        if isinstance(t, str) and ascii_re.match(t) and re.search(r'[A-Z]', t):
            violations_upper.append((str(f), t))
    # Duplicate (case-insensitive) check
    by_lower = {}
    for t in tags:
        if not isinstance(t, str): continue
        k = t.lower()
        by_lower.setdefault(k, []).append(t)
    for k, originals in by_lower.items():
        if len(originals) > 1:
            violations_dup.append((str(f), k, originals))

exit_code = 0
if parse_errors:
    print('🔴 JSON parse errors:', file=sys.stderr)
    for f, e in parse_errors:
        print(f'  {f}: {e}', file=sys.stderr)
    exit_code = 1
if violations_upper:
    print(f'🔴 tags-lint: {len(violations_upper)} ASCII-uppercase tag(s) found:', file=sys.stderr)
    for f, t in violations_upper:
        print(f'  {f}: {t!r}', file=sys.stderr)
    exit_code = 1
if violations_dup:
    print(f'🔴 tags-lint: {len(violations_dup)} duplicate tag group(s) (case-insensitive):', file=sys.stderr)
    for f, k, originals in violations_dup:
        print(f'  {f}: {originals} → {k!r}', file=sys.stderr)
    exit_code = 1
if exit_code == 0:
    print('✅ tags-lint: all tags compliant (ASCII lowercase + no case-insensitive duplicates).')
sys.exit(exit_code)
PY
fi

echo "✅ Pre-PR secrecy check passed."
