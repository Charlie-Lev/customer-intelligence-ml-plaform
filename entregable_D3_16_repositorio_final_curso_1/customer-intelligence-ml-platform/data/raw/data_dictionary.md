# Diccionario de datos — Customer Churn

Dataset sintético de **NovaTel Perú S.A.C.** para predecir la cancelación de clientes.

| Variable | Tipo esperado | Descripción | Rol |
|---|---|---|---|
| `customer_id` | string | Identificador único con formato `NT-000001`. | Identificador; excluir del modelo. |
| `gender` | categórica | Género declarado: Femenino o Masculino. | Predictora. |
| `age` | numérica | Edad del cliente, entre 18 y 82 años. | Predictora; contiene faltantes. |
| `region` | categórica | Lima, Norte, Centro, Sur u Oriente. | Predictora; contiene faltantes. |
| `customer_segment` | categórica | Masivo, Joven digital, Familia o Premium. | Predictora. |
| `contract_type` | categórica | Contrato Mensual, Anual o Bianual. | Predictora relevante. |
| `tenure_months` | numérica | Antigüedad del cliente en meses. | Predictora relevante. |
| `monthly_fee` | numérica | Tarifa mensual en soles (S/). | Predictora; contiene outliers. |
| `total_spent` | numérica | Gasto acumulado estimado en soles (S/). | Predictora; contiene faltantes. |
| `internet_service` | categórica | Fibra, DSL o Sin internet. | Predictora; contiene faltantes. |
| `tv_service` | categórica binaria | Indica si tiene televisión: Sí/No. | Predictora. |
| `streaming_service` | categórica binaria | Indica si tiene streaming: Sí/No. | Predictora. |
| `support_calls` | numérica discreta | Llamadas recientes a soporte. | Predictora relevante; contiene outliers. |
| `complaints` | numérica discreta | Reclamos registrados recientemente. | Predictora relevante. |
| `payment_method` | categórica | Tarjeta, Débito automático, Transferencia o Efectivo. | Predictora. |
| `last_payment_delay` | numérica discreta | Días de atraso del último pago. | Predictora relevante; contiene outliers. |
| `digital_usage_score` | numérica | Puntaje de uso digital entre 0 y 100. | Predictora; contiene faltantes. |
| `marketing_score` | numérica | Afinidad estimada con campañas, entre 0 y 100. | Predictora; contiene faltantes. |
| `preferred_contact_hour` | numérica discreta | Hora preferida de contacto, de 8 a 20. | Variable deliberadamente débil. |
| `internal_campaign_code` | categórica | Código interno de campaña. | Variable irrelevante para selección de atributos. |
| `churn` | binaria | 1 = cliente canceló; 0 = cliente permanece. | Variable objetivo. |

## Calidad incorporada deliberadamente

- Cerca de 1,000 registros en la versión base.
- Aproximadamente 20–25% de clientes con `churn = 1`.
- Valores faltantes en variables seleccionadas.
- Outliers en tarifa, llamadas de soporte y atraso de pago.
- Variables débiles o irrelevantes para ejercicios de selección.
- Relaciones de negocio no determinísticas: más reclamos, atraso y contratos mensuales elevan el riesgo; mayor antigüedad y uso digital lo reducen.

## Consideraciones académicas

El dataset es sintético y no contiene información personal real. Los patrones se diseñaron para practicar exploración, limpieza, pipelines, evaluación, versionado, monitoreo de drift y reentrenamiento.
