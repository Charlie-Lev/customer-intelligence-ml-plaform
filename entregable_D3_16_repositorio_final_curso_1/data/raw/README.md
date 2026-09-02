# Datos del proyecto

Esta carpeta contiene los datos de entrada del caso **Customer Churn Prediction** de NovaTel Perú S.A.C.

## Archivos

- `customer_churn.csv`: dataset base de entrenamiento con 1,000 clientes.
- `generate_dataset.py`: generador reproducible del dataset.
- `data_dictionary.md`: definición de variables y reglas de calidad.

## Regenerar el dataset

Desde la raíz del repositorio:

```bash
python data/raw/generate_dataset.py
```

Cambiar el número de registros:

```bash
python data/raw/generate_dataset.py --rows 5000
```

Generar datos futuros con drift:

```bash
python data/raw/generate_dataset.py \
  --rows 1000 \
  --seed 2026 \
  --scenario drift \
  --output data/monitoring/customer_churn_new_data.csv
```

## Reproducibilidad

La ejecución predeterminada utiliza la semilla `42`. Con los mismos parámetros se obtiene el mismo dataset.

## Uso responsable

Los datos son completamente sintéticos. No representan clientes reales ni deben usarse para tomar decisiones comerciales reales.
