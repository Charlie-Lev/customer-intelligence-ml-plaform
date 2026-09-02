#!/usr/bin/env bash
set -euo pipefail

git init
dvc init

mkdir -p /tmp/dvc-storage
dvc remote add -d course-storage /tmp/dvc-storage

echo "Git and DVC initialized."
echo "Next:"
echo "  dvc add data/raw/customer_churn.csv"
echo "  git add ."
echo "  git commit -m 'chore: initialize Git and DVC'"
