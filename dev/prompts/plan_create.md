# Prompt — Plan Create

Actúa como motor activo en fase de planificación formal de una iniciativa.

## Referencias obligatorias

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/plan_gate.md`

## Precondiciones obligatorias

1. Existe una iniciativa identificada
2. Existe un `input de planificación` transitorio derivado de `M0`
3. El contexto técnico relevante ya fue aterrizado mediante retrieval canónico

Si falta una precondición:
- no planificar
- devolver `BLOQUEADO` con evidencia

## Objetivo

Generar un `plan.md` ejecutable, acotado y auditable.

## Salida obligatoria

Guardar en:
- `dev/records/initiatives/<initiative_id>/plan.md`

Estructura mínima:
1. Objetivo
2. Problema real
3. Evidencia base
4. Alcance
5. No-alcance
6. Restricciones y supuestos
7. Riesgos principales
8. Estrategia de implementación
9. Plan por tramos
10. Validación global prevista
11. Rollback
12. Definition of Done
13. Referencias a origen weekly/backlog si aplica

## Restricciones

- Un cambio lógico por commit.
- No refactor encubierto.
- No alcance fuera del input de planificación validado en `M0`.
- No implementación en esta fase.
- No recrear weekly, backlog o conversación completa dentro del plan.
- No inventar evidencia faltante; si falta, declararla como hueco explícito.

Marca final:
- `Estado: PROPUESTO`
- `Etiqueta: PENDIENTE_DE_AUDITORIA`
