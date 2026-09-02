# Repositorio final — Curso 1

## Del desarrollo de modelos a Machine Learning Engineering

Este repositorio integra los entregables D2 y D3.2–D3.15 sin reducir sus
notebooks enriquecidos ni sus módulos reutilizables.

## Notebooks

```text
01_data_understanding.ipynb
02_model_development.ipynb
03_model_evaluation.ipynb
04_pipeline_validation.ipynb
05_batch_prediction.ipynb
99_end_to_end_demo.ipynb
```

Total: **281 celdas**.

## Capacidades

- Generación y validación de datos.
- Exploración y entendimiento del dataset.
- Preprocesamiento reusable.
- Entrenamiento y comparación de modelos.
- Evaluación avanzada y selección de umbral.
- Persistencia y carga del pipeline.
- Inferencia batch.
- Validación end-to-end.
- Pruebas automatizadas.
- CLI.
- GitHub Codespaces.
- Git y Pull Requests.
- DVC para datos y pipelines.
- GitHub Actions.

## Instalación

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Pruebas

```bash
pytest -v
```

## Entrenamiento

```bash
python main.py train --data data/raw/customer_churn.csv
```

## Pipeline DVC

```bash
dvc init
dvc repro
dvc metrics show
```

## Próximo curso

Este repositorio será extendido con FastAPI, Docker, AWS y Prometheus sin
reemplazar el pipeline central.
