# Prompt — Ask Discovery

Actúa como `motor_activo` en fase Ask siguiendo estrictamente:

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/ask_gate.md`

Tu tarea es preparar el dossier Ask para una iniciativa técnica.

## Entradas obligatorias

1. `handoff.md` si existe
2. Seed plan inicial (usuario + asistente) si no existe `handoff.md`
3. Contexto técnico disponible (archivos/logs)

Si falta una entrada obligatoria:
- detenerse
- declarar `BLOQUEADO`

## Regla de precedencia

- Si existe `dev/records/initiatives/<initiative_id>/handoff.md`, ese archivo
  es la fuente primaria de apertura de `M4` pre-`F1`.
- El chat o seed plan se usa solo como apoyo para aclarar huecos verificables.

## Salida obligatoria (documento Ask)

Genera un documento listo para guardar en:

`dev/records/initiatives/<initiative_id>/ask.md`

Con estas secciones:

1. Objetivo y contexto
2. Evidencia técnica
3. Supuestos
4. Preguntas bloqueantes / no bloqueantes
5. Opciones y trade-offs
6. Recomendación Ask
7. Criterios de aceptación para el `motor_activo`

## Restricciones

- No implementar código.
- No generar plan final de commits.
- No mezclar solución final con fase Ask.
- Si existe `handoff.md`, preservar evidencia, supuestos, preguntas y
  trade-offs relevantes.
- Si algo útil del `handoff.md` no entra en Ask, dejarlo trazado como insumo
  pendiente para `F4`.
- Si el Ask queda `VALIDADO`, debe pasar por auditoría `F3`.
