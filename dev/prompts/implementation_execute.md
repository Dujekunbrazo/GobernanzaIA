# Prompt — Implementation Execute (F6)

Actúa como `motor_activo` en implementación.

## Referencias obligatorias

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/implementation_gate.md`

## Precondiciones obligatorias

1. Existe `plan.md`
2. `plan.md` está en estado `CONGELADO`
3. Existe `plan_audit.md` con resultado `PASS`

Si alguna precondición falla:
- no implementar
- devolver `BLOQUEADO` con evidencia (ruta + estado faltante)

## Objetivo

Ejecutar el plan congelado, commit a commit, sin alcance extra.

## Restricciones

- 1 cambio lógico por commit.
- Prohibido refactor encubierto.
- Prohibido introducir cambios fuera de `plan.md`.
- No cerrar la iniciativa desde esta fase.

## Salida obligatoria

Actualizar:
- `dev/records/initiatives/<initiative_id>/execution.md`

Con:
1. Lista de commits ejecutados
2. Por commit: intención, archivos, validación y resultado
3. Riesgos detectados
4. Bloqueos o desviaciones (si aplica)
