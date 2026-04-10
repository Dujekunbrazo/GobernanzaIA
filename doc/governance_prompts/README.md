# Prompts De Gobernanza

Estos prompts están pensados para copiar y pegar tal cual.

No hace falta repetirle toda la gobernanza cada vez. Si Claude está bien
anclado al repo, la debe leer desde `CLAUDE.md`, `AGENTS.md`,
`dev/workflow.md` y `dev/ai/adapters/claude.md`.

La idea es simple:

- tú hablas normal
- Codex te ayuda a aterrizar la idea en `M0`
- cuando ya está madura, conviertes la conversación en `input de planificación`
- Claude produce `plan.md`
- Codex audita el plan
- Claude ejecuta, valida y cierra
- no tienes que sustituir placeholders manualmente

## Flujo de iniciativa

1. Habla con Codex en `M0`
2. Usa `97 idea codex.md` para pedir a Codex el `input de planificación`
3. Pega ese bloque en Claude con `98 idea codex to claude plan.md`
4. Audita el `plan.md` con `99 prompt plan a codex.md`
5. Si el plan falla, usa `15_f4_remediacion_plan.md`
6. Ejecuta con Claude sobre `plan.md` usando `06_f6_implementacion.md`
7. Audita implementación con `07_f7_post_auditoria.md`
8. Cierra con `09_f9_f10_cierre_y_lecciones.md`

## Flujo weekly review

1. Usa `20_weekly_mit_review.md`
2. El weekly produce hallazgos, candidatos y backlog
3. Si eliges un candidato, vuelve al flujo de iniciativa

## Prompts activos

- `97 idea codex.md`
- `98 idea codex to claude plan.md`
- `99 prompt plan a codex.md`
- `04_f4_plan.md`
- `05_f5_auditoria_plan.md`
- `06_f6_implementacion.md`
- `07_f7_post_auditoria.md`
- `09_f9_f10_cierre_y_lecciones.md`
- `15_f4_remediacion_plan.md`
- `20_weekly_mit_review.md`

## Qué ya no existe

- artefactos intermedios de apertura previos
- prompts de apertura basados en el flujo anterior

## Regla rápida

- conversación `M0` -> `input de planificación` -> `plan.md`
- `plan.md` es el primer artefacto formal de iniciativa
- weekly review no genera `plan.md`
- el backlog no sustituye el plan
- cierre: `closeout.md` + `lessons_learned.md`

## Regla operativa

- al abrir una iniciativa formal, Claude debe crear él mismo un `initiative_id`
  canónico
- si la iniciativa ya existe, Claude debe detectar la iniciativa activa por
  contexto y por los artefactos del repo
- si hay ambigüedad material entre varias iniciativas, debe bloquear y pedir
  una sola aclaración
