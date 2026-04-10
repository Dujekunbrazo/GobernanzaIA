# Prompt — Post Audit / Debug

Actúa como motor auditor después de la implementación.

## Referencias obligatorias

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/implementation_gate.md`

## Entrada mínima

- `dev/records/initiatives/<initiative_id>/plan.md` en `CONGELADO`
- `dev/records/initiatives/<initiative_id>/execution.md`
- evidencia de validación (comandos, logs, pruebas)

Si falta evidencia mínima:
- devolver `FAIL` por trazabilidad incompleta

## Objetivo

Verificar que lo implementado coincide con el plan congelado y no introduce
regresiones.

## Qué auditar

1. Trazabilidad (ejecutado vs plan)
2. Calidad técnica (bugs y deuda introducida)
3. Validación (pruebas y comandos realmente ejecutables)
4. Seguridad de cierre (riesgos remanentes claros)
5. Clasificación correcta de todos los puntos auditados como `hallazgos`

## Formato de salida obligatorio

Guardar en:
- `dev/records/initiatives/<initiative_id>/post_audit.md`

Estructura:
- Initiative ID
- Fecha
- Auditor
- Veredicto: `PASS` | `FAIL`
- Hallazgos materiales por severidad (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`)
- Evidencia concreta por hallazgo
- Recomendación de fix atómico por hallazgo (sin implementarlo)
- Justificación del veredicto
- Condición para avanzar

## Reglas de decisión

- `PASS`: sin hallazgos abiertos ni pendientes.
- `FAIL`: existe al menos un bloqueante pendiente.

## Restricciones

- No reescribir la implementación.
- No mezclar fixes y mejoras en el mismo hallazgo.
- No cerrar tarea con `FAIL`.
- No usar la categoría `observaciones`.
