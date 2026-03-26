# Prompt — M4 Opening Handoff

Actúa como `motor_activo` al abrir una iniciativa `M4`.

## Referencias obligatorias

- `AGENTS.md`
- `dev/workflow.md`
- `dev/ai/adapters/claude.md` si Claude es el motor usado

## Objetivo

Persistir el análisis y la planificación previa dentro de `M4`, antes de `F1`,
para que no se pierdan al pasar de conversación a iniciativa formal.

## Salida obligatoria

Guardar en:

- `dev/records/initiatives/<initiative_id>/handoff.md`

## Estructura mínima

1. Objetivo y problema
2. Evidencia técnica
3. Alcance propuesto
4. No-alcance propuesto
5. Supuestos
6. Preguntas abiertas
7. Opciones y trade-offs
8. Recomendación
9. Borrador de plan por commits
10. Criterios de derivación a `ask.md`
11. Criterios de derivación a `plan.md`

## Restricciones

- No llamar a este artefacto `plan.md`.
- No asumir que esto sustituye `F1` o `F4`.
- No crear este artefacto en `M0`; solo tras la transición a `M4`.
- No dejar la planificación final solo en chat.
- No implementar código.
