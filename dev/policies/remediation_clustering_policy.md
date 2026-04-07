# Policy: Remediation Clustering

## Objetivo

Agrupar hallazgos materiales en iniciativas candidatas gobernables.

## Reglas de agrupacion

Priorizar agrupacion por:

- concept dominante
- synchronization compartida
- write set dominante
- causa raiz comun
- misma superficie observable o mismo owner arquitectonico

## Reglas de no agrupacion

- no mezclar hallazgos de riesgo y timing incompatibles
- no meter varias capabilities no relacionadas en la misma candidata
- no abrir una iniciativa por ruido menor o cosmetico

## Criterio de aceptabilidad

El clustering es correcto cuando:

- cada candidata tiene una justificacion clara
- el write set dominante es reconocible
- la iniciativa resultante es ejecutable y auditable
