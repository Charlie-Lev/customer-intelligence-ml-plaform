# Solución del instructor — Git y DVC

## Resultado esperado

```bash
git switch -c feature/churn-experiment
```

Modificar `params.yaml`, por ejemplo:

```yaml
model:
  max_iter: 1200
```

Validar:

```bash
pytest -q
git add params.yaml
git commit -m "model: increase logistic regression iterations"
git push -u origin feature/churn-experiment
```

## DVC

```bash
dvc init
git add .dvc .dvcignore
git commit -m "chore(dvc): initialize DVC"

dvc add data/raw/customer_churn.csv
git add data/raw/customer_churn.csv.dvc data/raw/.gitignore
git commit -m "data(raw): track churn dataset with DVC"

mkdir -p /tmp/dvc-storage
dvc remote add -d course-storage /tmp/dvc-storage
git add .dvc/config
git commit -m "chore(dvc): configure local course storage"

dvc push
dvc repro
dvc metrics show
dvc dag
```

## Actualización del dataset

```bash
python data/raw/generate_dataset.py \
  --rows 1200 \
  --seed 2026 \
  --output data/raw/customer_churn.csv

dvc add data/raw/customer_churn.csv
dvc repro
dvc metrics diff

git add data/raw/customer_churn.csv.dvc \
  reports/metrics/training_metrics.json

git commit -m "data(raw): update dataset and training metrics"
dvc push
```

## Respuestas esperadas

**Git** registra código, configuración y archivos livianos de control.

**DVC** registra referencias y metadatos para datasets, modelos y otros
artefactos que no conviene almacenar directamente en Git.

El archivo `.dvc` debe versionarse en Git; el contenido pesado se almacena en
el cache de DVC y en el remote configurado.
