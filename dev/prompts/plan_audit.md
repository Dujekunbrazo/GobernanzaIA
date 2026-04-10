# Prompt — Plan Audit

Actúa como motor auditor del plan técnico.

## Referencias obligatorias

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/plan_gate.md`

## Entrada mínima

- `dev/records/initiatives/<initiative_id>/plan.md` en `PROPUESTO`

Si falta algo:
- devolver `FAIL` por precondición incompleta

## Objetivo

Validar que el plan es ejecutable, coherente y seguro antes del congelado.

## Qué auditar

1. Coherencia problema-evidencia-alcance-plan
2. Calidad de ejecución (atomicidad, orden, validaciones, rollback)
3. Riesgo técnico (regresiones y complejidad)
4. Gobernanza (sin alcance extra, sin rutas inventadas, sin duplicidad)
5. Clasificación correcta de todos los puntos auditados como `hallazgos`

## Formato de salida obligatorio

Guardar en:
- `dev/records/initiatives/<initiative_id>/plan_audit.md`

Estructura:
- Initiative ID
- Fecha
- Auditor
- Veredicto: `PASS` | `FAIL`
- Hallazgos materiales numerados por severidad (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`)
- Evidencia por hallazgo
- Recomendación por hallazgo
- Justificación del veredicto
- Condición para avanzar

## Reglas de decisión

- `PASS`: sin hallazgos abiertos ni pendientes.
- `FAIL`: existe al menos un bloqueante pendiente.

## Restricciones

- No reescribir el plan durante auditoría.
- No implementar fixes.
- No introducir alcance nuevo.
- No usar la categoría `observaciones`.
