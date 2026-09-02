# Customer Intelligence ML Platform

Repositorio consolidado del curso **Del desarrollo de modelos a MLE**.

## Contenido

- Dataset sintético de churn.
- Seis notebooks enriquecidos.
- Módulos reutilizables en `src/`.
- Entrenamiento, evaluación y predicción.
- Pruebas automatizadas.
- CLI.
- GitHub Actions.
- Configuración DVC.
- Carpetas de artefactos y reportes.

## Notebooks

```text
01_data_understanding.ipynb
02_model_development.ipynb
03_model_evaluation.ipynb
04_pipeline_validation.ipynb
05_batch_prediction.ipynb
99_end_to_end_demo.ipynb
```

Los notebooks conservan el contenido enriquecido de los entregables
D3.3, D3.8, D3.9, D3.10, D3.11 y D3.12.

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

## Predicción

```bash
python main.py predict   --data data/raw/customer_churn.csv   --model artifacts/models/churn_pipeline.joblib
```
