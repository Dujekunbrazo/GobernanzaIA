# Prompts De Gobernanza

Estos prompts están pensados para copiar y pegar tal cual.

No hace falta repetirle toda la gobernanza cada vez. Si Claude está bien
anclado al repo, la debe leer desde `CLAUDE.md`, `AGENTS.md`,
`dev/workflow.md` y `dev/ai/adapters/claude.md`.

La idea es simple:

- tú hablas normal
- el prompt solo marca el momento del proceso
- la gobernanza traduce eso a artefactos, fases y restricciones
- no tienes que sustituir placeholders manualmente

## Orden de uso

1. `00_abrir_m4_y_handoff.md`
2. `01_m4_f1_ask.md`
3. `02_f2_validacion_ask.md`
4. `03_f3_auditoria_ask.md`
5. `04_f4_plan.md`
6. `05_f5_auditoria_plan.md`
7. `06_f6_ejecucion.md`
8. `07_f7_post_auditoria.md`
9. `08_f8_validacion_real_guiada.md`
10. `09_f9_cierre.md`
11. `10_f10_lecciones.md`

## Regla rápida

- al abrir `M4`, antes de `F1`: `handoff.md`
- `F1`: `ask.md`
- `F4`: `plan.md`
- `F6`: `execution.md`
- `F7`: `post_audit.md`
- `F8`: `real_validation.md` cuando aplica
- `F9`: `closeout.md`
- `F10`: `lessons_learned.md`

## Regla operativa

- al abrir una iniciativa `M4`, Claude debe crear él mismo un `initiative_id`
  canónico
- si la iniciativa ya existe, Claude debe detectar la iniciativa activa por
  contexto y por los artefactos del repo
- si hay ambigüedad material entre varias iniciativas, debe bloquear y pedir
  una sola aclaración
