# Prompt — Plan Create (F4)

Actúa como `motor_activo` en fase de planificación.

## Referencias obligatorias

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/plan_gate.md`

## Precondiciones obligatorias

1. Existe `dev/records/initiatives/<initiative_id>/ask.md`
2. `ask.md` está en estado `CONGELADO`
3. Existe `ask_audit.md` con resultado `PASS`
4. Si existe `handoff.md`, debe leerse antes de proponer `plan.md`

Si falta una precondición:
- no planificar
- devolver `BLOQUEADO` con evidencia

## Objetivo

Generar un `plan.md` ejecutable, acotado y auditable.

Si existe `handoff.md`, el plan debe:

- conservar el valor de la planificación previa
- mantener trazabilidad con el handoff
- explicar cualquier delta material respecto al handoff

## Salida obligatoria

Guardar en:
- `dev/records/initiatives/<initiative_id>/plan.md`

Estructura mínima:
1. Objetivo
2. Alcance
3. No-alcance
4. Impacto técnico
5. Riesgos (Top 3)
6. Plan por commits (intención, archivos, cambios, validación)
7. Rollback
8. Definition of Done
9. Referencia al Ask congelado

## Restricciones

- Un cambio lógico por commit.
- No refactor encubierto.
- No alcance fuera de Ask.
- No implementación en esta fase.
- No sobrescribir `handoff.md`; ese archivo queda reservado a apertura de `M4`
  pre-`F1`.

Marca final:
- `Estado: PROPUESTO`
- `Etiqueta: PENDIENTE DE AUDITORIA DEL MOTOR_AUDITOR`
