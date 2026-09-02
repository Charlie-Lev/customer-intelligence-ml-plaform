# DVC Commands Cheatsheet

```bash
dvc init
dvc add data/raw/customer_churn.csv
dvc remote add -d course-storage /tmp/dvc-storage
dvc push
dvc pull
dvc checkout
dvc status
dvc repro
dvc dag
dvc metrics show
dvc metrics diff
dvc cache dir
```

# Git Commands Cheatsheet

```bash
git status
git switch -c feature/name
git diff
git add <files>
git commit -m "type(scope): message"
git push -u origin feature/name
git log --oneline --graph --decorate --all
git fetch
git pull --rebase
```
