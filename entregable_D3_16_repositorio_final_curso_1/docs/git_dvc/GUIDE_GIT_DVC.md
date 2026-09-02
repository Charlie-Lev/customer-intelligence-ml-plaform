# Guía práctica de Git, GitHub y DVC

## Objetivo

Versionar conjuntamente:

- código y configuración con Git;
- datasets y artefactos con DVC;
- experimentos reproducibles mediante `dvc.yaml`;
- colaboración mediante ramas y Pull Requests.

## Entorno web recomendado

Se recomienda GitHub Codespaces porque permite crear ramas, realizar commits,
hacer push y abrir Pull Requests desde el navegador.

## 1. Crear el repositorio

1. Crear un repositorio vacío en GitHub.
2. Subir el contenido del entregable D3.14.
3. Abrir **Code → Codespaces → Create codespace**.

## 2. Configurar identidad Git

```bash
git config user.name "Nombre del estudiante"
git config user.email "correo@example.com"
```

## 3. Verificar el repositorio

```bash
git status
git branch
git log --oneline --decorate --graph --all
```

## 4. Flujo branch → commit → push → PR

```bash
git switch -c feature/data-validation
```

Realizar cambios y revisar:

```bash
git status
git diff
```

Agregar y confirmar:

```bash
git add src/data tests
git commit -m "feat(data): add customer dataset validation"
```

Publicar la rama:

```bash
git push -u origin feature/data-validation
```

Crear el Pull Request desde GitHub y solicitar revisión.

## 5. Convención de commits

```text
feat: nueva funcionalidad
fix: corrección
test: pruebas
docs: documentación
refactor: reorganización sin cambio funcional
chore: configuración o mantenimiento
data: actualización de dataset o referencia DVC
model: actualización de modelo o métricas
```

Ejemplos:

```bash
git commit -m "feat(features): add reusable preprocessing pipeline"
git commit -m "test(training): validate model artifact creation"
git commit -m "data(raw): track churn dataset with DVC"
```

## 6. Inicializar DVC

DVC debe inicializarse dentro de un repositorio Git:

```bash
dvc init
git add .dvc .dvcignore
git commit -m "chore(dvc): initialize data version control"
```

## 7. Versionar el dataset

```bash
dvc add data/raw/customer_churn.csv
```

Esto genera:

```text
data/raw/customer_churn.csv.dvc
```

El CSV queda excluido de Git y el archivo `.dvc` sí se versiona:

```bash
git add data/raw/customer_churn.csv.dvc data/raw/.gitignore
git commit -m "data(raw): track customer churn dataset with DVC"
```

## 8. Configurar un remote gratuito para laboratorio

Para una práctica sin servicios de pago puede utilizarse una carpeta local:

```bash
mkdir -p /tmp/dvc-storage
dvc remote add -d course-storage /tmp/dvc-storage
git add .dvc/config
git commit -m "chore(dvc): configure course remote"
```

Subir los datos:

```bash
dvc push
```

Recuperarlos:

```bash
dvc pull
```

> La carpeta local sirve para practicar el flujo. Para trabajo compartido se
> puede configurar posteriormente un almacenamiento remoto compatible.

## 9. Ejecutar el pipeline reproducible

```bash
dvc repro
```

Consultar métricas:

```bash
dvc metrics show
```

Visualizar el DAG:

```bash
dvc dag
```

## 10. Modificar datos y generar una nueva versión

Regenerar el dataset:

```bash
python data/raw/generate_dataset.py --rows 1200 --seed 2026
dvc add data/raw/customer_churn.csv
git add data/raw/customer_churn.csv.dvc
git commit -m "data(raw): update churn dataset to 1200 records"
dvc push
```

Reejecutar:

```bash
dvc repro
dvc metrics diff
```

## 11. Recuperar una versión anterior

```bash
git log --oneline
git checkout <commit> -- data/raw/customer_churn.csv.dvc
dvc checkout
```

Para volver a la rama actual:

```bash
git restore data/raw/customer_churn.csv.dvc
dvc checkout
```

## 12. Checklist del estudiante

- [ ] Trabajé en una rama.
- [ ] Revisé `git diff`.
- [ ] Usé un mensaje de commit descriptivo.
- [ ] Publiqué la rama.
- [ ] Abrí un Pull Request.
- [ ] Inicialicé DVC.
- [ ] Versioné el dataset con `dvc add`.
- [ ] Configuré un remote.
- [ ] Ejecuté `dvc push`.
- [ ] Ejecuté `dvc repro`.
- [ ] Consulté métricas.
- [ ] Probé recuperar una versión anterior.
