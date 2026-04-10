# Prompt — Implementation Execute

Actúa como motor activo en implementación.

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

Ejecutar el `plan.md` congelado, tramo a tramo o commit a commit, sin alcance
extra.

## Restricciones

- 1 cambio lógico por commit.
- Prohibido refactor encubierto.
- Prohibido introducir cambios fuera de `plan.md`.
- Prohibido reexplicar el plan en `execution.md`.
- No cerrar la iniciativa desde esta fase.
- Por defecto, validar cada tramo con tests dirigidos al `write set`.
- No ejecutar la suite completa por rutina en cada tramo.
- La suite completa solo aplica si el `plan.md` la exige, si el cambio es
  sistémico o si se está cerrando `F6`.
- Si aparece desviación material respecto al plan, parar y devolver
  `BLOQUEADO` con evidencia antes de seguir al siguiente tramo.

## Salida obligatoria

Actualizar:
- `dev/records/initiatives/<initiative_id>/execution.md`

Con:
1. Lista de tramos o commits ejecutados
2. Por tramo o commit: intención, archivos, validación y resultado
3. Riesgos detectados
4. Bloqueos o desviaciones (si aplica)
5. Indicación explícita de si la validación fue dirigida o suite completa, y
   por qué
