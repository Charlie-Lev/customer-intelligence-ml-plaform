# Laboratorio — Git y DVC

## Escenario

El equipo de Data Science de NovaTel necesita modificar el pipeline sin afectar
la rama principal y versionar una actualización del dataset.

## Parte A — Git

1. Cree la rama:

```bash
git switch -c feature/churn-experiment
```

2. Modifique un parámetro del modelo en `params.yaml`.
3. Revise el cambio:

```bash
git diff
```

4. Ejecute pruebas:

```bash
pytest -q
```

5. Registre el cambio:

```bash
git add params.yaml
git commit -m "model: update churn training parameter"
```

6. Publique la rama y abra un Pull Request.

## Parte B — DVC

1. Inicialice DVC.
2. Versione `data/raw/customer_churn.csv`.
3. Configure un remote local.
4. Ejecute `dvc push`.
5. Ejecute `dvc repro`.
6. Consulte métricas con `dvc metrics show`.

## Parte C — Nueva versión del dataset

1. Genere 1,200 registros con otra semilla.
2. Actualice el archivo `.dvc`.
3. Reejecute el pipeline.
4. Compare métricas.
5. Registre el cambio con Git.

## Evidencias

Entregue:

- captura o salida de `git log --oneline`;
- URL del Pull Request;
- salida de `dvc status`;
- salida de `dvc dag`;
- comparación de métricas;
- explicación de la diferencia entre Git y DVC.
