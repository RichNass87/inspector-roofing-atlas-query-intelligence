#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v kaggle >/dev/null 2>&1; then
  echo "ERROR: kaggle CLI is not installed. Run: python3 -m pip install --user kaggle" >&2
  exit 1
fi

if [[ ! -f "$HOME/.kaggle/kaggle.json" ]]; then
  echo "ERROR: Missing ~/.kaggle/kaggle.json. Create a Kaggle API token from Account settings." >&2
  exit 1
fi

kaggle datasets create -p . --dir-mode zip
