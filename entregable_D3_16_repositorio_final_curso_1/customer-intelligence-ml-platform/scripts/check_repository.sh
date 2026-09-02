#!/usr/bin/env bash
set -euo pipefail

echo "== Git status =="
git status --short

echo "== DVC status =="
dvc status

echo "== Tests =="
pytest -q

echo "== Lint =="
ruff check .
