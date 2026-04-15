#!/bin/bash
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BASE="$HOME/.openclaw"

sync_agent() {
  local ws="$1"; shift
  local dest="$BASE/$ws/.agents/skills"
  mkdir -p "$dest"
  for cat in "$@"; do
    [ -d "$REPO_DIR/skills/$cat" ] && for skill in "$REPO_DIR/skills/$cat"/*/; do
      [ -d "$skill" ] && cp -r "$skill" "$dest/"
    done
  done
  echo "✓ $ws"
}

sync_agent workspace-forge  dev design meta
sync_agent workspace-pixel  design meta
sync_agent workspace-judge  dev design meta
sync_agent workspace-core   infra dev meta
sync_agent workspace-dex    sales business meta
sync_agent workspace-mara   business sales meta
sync_agent workspace-iris   itp business meta
sync_agent workspace-scribe itp business sales meta
sync_agent workspace-echo   itp meta
echo "Done."
