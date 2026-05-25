# F6/F7 — Cierre Con motor auditor + Lecciones
> [!IMPORTANT]
> Bootstrap obligatorio de gobernanza antes de usar este prompt:
> leer `AGENTS.md`, cargar la Skill canonica si existe, usar `governance_search`
> para gobernanza con `phase`/`document_type` cuando aplique, usar `symdex_code`
> para codigo vivo y `codebase-memory-mcp` para wiring/impacto/legacy cuando
> toque codigo, y declarar cualquier degradacion antes de recurrir a lectura
> bruta.

Atajo de compatibilidad para el tramo final posterior a
`READY_FOR_CODEX_CLOSEOUT`. Este estado significa cierre completo con motor auditor, no
handoff manual por subpasos.

Usa la iniciativa activa de esta conversación.

Precondición:

- `real_validation.md` declara `APTA_PARA_F6` o `NO_APLICA`, o la iniciativa
  llegó a cierre porque `F5` no aplica según el canon vigente

Haz el cierre según la gobernanza del repo:

- genera o actualiza `closeout.md`
- después genera o actualiza `lessons_learned.md`
- crea el commit final de cierre
- empuja la rama de iniciativa
- integra en `main/master` y empuja troncal salvo bloqueo real o instruccion de
  PR/merge manual
- refresca MCP post-merge en `main/master`
- borra rama local y remota
- deja `closeout.md` actualizado con evidencia final o bloqueo concreto

Actúa siguiendo:

- `AGENTS.md`
- `dev/workflow.md`
- `dev/templates/initiative/closeout.md`
- `dev/templates/initiative/lessons_learned.md`

Restricciones:

- no recrees el plan
- no reabras `F3/F4` salvo que aparezca una inconsistencia material nueva
- si el cierre deja backlog vivo, decláralo explícitamente
- no dejes push, merge, refresh o borrado de rama como pendiente rutinario

Antes de seguir, confirma qué iniciativa vas a cerrar solo si no puede inferirse
de los artefactos y del handoff.
# Compatibilidad legacy

La fuente de verdad operativa para `F6` es
`dev/skills/f6_closeout/SKILL.md`. La fuente de verdad operativa para `F7` es
`dev/skills/f7_lessons/SKILL.md`. Este prompt queda como atajo manual de solo
lectura.
