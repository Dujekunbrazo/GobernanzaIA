# Scoped Validation Policy

## Proposito

Formalizar que la validacion por iniciativa debe ser proporcional al write set
y al blast radius reales, evitando ejecutar la suite completa por rutina.

## Regla central

Por defecto, cada iniciativa debe ejecutar validacion dirigida y proporcional
al scope real del cambio.

La suite completa no es la validacion estandar por defecto.

## Validacion minima esperada

Toda iniciativa debe priorizar:

- tests directamente afectados por el write set
- tests rozados por dependencias relevantes
- checks rapidos de integracion del camino tocado

## Cuando si procede suite completa

La suite completa solo se justifica cuando:

- el cambio es transversal
- el blast radius no puede acotarse con confianza
- existe riesgo sistemico real
- el framework, wiring base o contratos comunes han cambiado
- se ejecuta el control periodico del carril weekly

## Obligaciones del plan y la ejecucion

- `plan.md` debe declarar una estrategia de validacion proporcional cuando
  aplique
- `execution.md` debe registrar la validacion realmente ejecutada
- `post_audit.md` debe evaluar si la validacion fue suficiente para el scope
  real del cambio

## Prohibiciones

- prohibido exigir suite completa por rutina sin justificar blast radius
- prohibido documentar como ejecutados tests que no se corrieron
- prohibido cerrar una iniciativa con validacion inventada
