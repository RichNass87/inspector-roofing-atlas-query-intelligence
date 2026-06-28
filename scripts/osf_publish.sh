#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

OSF_BIN="${OSF_BIN:-}"
if [[ -z "$OSF_BIN" ]] && command -v osf >/dev/null 2>&1; then
  OSF_BIN="$(command -v osf)"
fi
if [[ -z "$OSF_BIN" && -x "$HOME/Library/Python/3.14/bin/osf" ]]; then
  OSF_BIN="$HOME/Library/Python/3.14/bin/osf"
fi
if [[ -z "$OSF_BIN" && -x "$HOME/Library/Python/3.13/bin/osf" ]]; then
  OSF_BIN="$HOME/Library/Python/3.13/bin/osf"
fi

if [[ -z "$OSF_BIN" ]]; then
  echo "ERROR: osfclient CLI is not installed. Run: python3 -m pip install --user osfclient" >&2
  exit 1
fi

if [[ -z "${OSF_PROJECT_ID:-}" ]]; then
  echo "ERROR: Set OSF_PROJECT_ID to your OSF project short ID, for example OSF_PROJECT_ID=abc12." >&2
  exit 1
fi

if [[ ! -f "$HOME/.osfcli.config" && -z "${OSF_USERNAME:-}" ]]; then
  echo "ERROR: OSF auth is missing. Run osf init, or set OSF_USERNAME/OSF_PASSWORD in your shell session." >&2
  exit 1
fi

UPLOAD_DIR="$(python3 scripts/build_platform_uploads.py)"
ZIP="/Users/richardnasser/Documents/inspector-roofing-atlas-source-spine-v1.0.1.zip"
PDF="$UPLOAD_DIR/docs/inspector-roofing-atlas-query-intelligence-technical-report-v1.0.1.pdf"

"$OSF_BIN" -p "$OSF_PROJECT_ID" upload "$ZIP" osfstorage/inspector-roofing-atlas-source-spine-v1.0.1.zip
"$OSF_BIN" -p "$OSF_PROJECT_ID" upload "$PDF" osfstorage/inspector-roofing-atlas-query-intelligence-technical-report-v1.0.1.pdf
"$OSF_BIN" -p "$OSF_PROJECT_ID" upload "$UPLOAD_DIR/docs/OSF_PROJECT_DESCRIPTION.md" osfstorage/OSF_PROJECT_DESCRIPTION.md
"$OSF_BIN" -p "$OSF_PROJECT_ID" upload "$UPLOAD_DIR/data/platform_links.csv" osfstorage/platform_links.csv
"$OSF_BIN" -p "$OSF_PROJECT_ID" upload "$UPLOAD_DIR/data/public_project_inventory.csv" osfstorage/public_project_inventory.csv
"$OSF_BIN" -p "$OSF_PROJECT_ID" upload "$UPLOAD_DIR/data/orcid_works.bib" osfstorage/orcid_works.bib

echo "OSF upload complete for project $OSF_PROJECT_ID."
