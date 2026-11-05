#!/usr/bin/env bash
# Regenerate the templates, build both pages, then screenshot every scene for QA and the landing-page thumbnails.
set -euo pipefail
cd "$(dirname "$0")/.."
SKILL="$HOME/.claude/skills/architecture-animated/scripts"
python3 -I scripts/make_templates.py
for p in network pipelines; do
  python3 -I "$SKILL/build.py" "docs/${p}_template.html" "docs/${p}.html"
done
if [[ "${1:-}" == "--shots" ]]; then
  for p in network pipelines; do
    python3 -I "$SKILL/shoot.py" "docs/${p}.html" "/tmp/${p}_shots" --thumb "docs/thumb-${p}.png"
  done
fi
