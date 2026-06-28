#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

KAGGLE_BIN="${KAGGLE_BIN:-}"
if [[ -z "$KAGGLE_BIN" ]] && command -v kaggle >/dev/null 2>&1; then
  KAGGLE_BIN="$(command -v kaggle)"
fi
if [[ -z "$KAGGLE_BIN" && -x "$HOME/Library/Python/3.14/bin/kaggle" ]]; then
  KAGGLE_BIN="$HOME/Library/Python/3.14/bin/kaggle"
fi
if [[ -z "$KAGGLE_BIN" && -x "$HOME/Library/Python/3.13/bin/kaggle" ]]; then
  KAGGLE_BIN="$HOME/Library/Python/3.13/bin/kaggle"
fi

if [[ -z "$KAGGLE_BIN" ]]; then
  echo "ERROR: kaggle CLI is not installed. Run: python3 -m pip install --user kaggle" >&2
  exit 1
fi

if [[ ! -f "$HOME/.kaggle/kaggle.json" ]]; then
  echo "ERROR: Missing ~/.kaggle/kaggle.json. Create a Kaggle API token from Account settings." >&2
  exit 1
fi

chmod 600 "$HOME/.kaggle/kaggle.json"

MODE="${KAGGLE_MODE:-auto}"
MESSAGE="${KAGGLE_MESSAGE:-v1.0.1 public-safe source-spine update}"

case "$MODE" in
  create)
    "$KAGGLE_BIN" datasets create -p . --dir-mode zip
    ;;
  version)
    "$KAGGLE_BIN" datasets version -p . -m "$MESSAGE" --dir-mode zip
    ;;
  auto)
    if "$KAGGLE_BIN" datasets version -p . -m "$MESSAGE" --dir-mode zip; then
      exit 0
    fi
    "$KAGGLE_BIN" datasets create -p . --dir-mode zip
    ;;
  *)
    echo "ERROR: KAGGLE_MODE must be auto, create, or version." >&2
    exit 1
    ;;
esac
