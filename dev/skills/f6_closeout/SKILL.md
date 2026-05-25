# SKILL

- `name`: `f6_closeout`
- `purpose`: cerrar la iniciativa con `closeout.md`, README incremental si aplica y cierre Git completo trazado
- `when_to_use`:
  - `F5` declara `APTA_PARA_F6` o `NO_APLICA`
  - toca cierre documental y operativo
- `when_not_to_use`:
  - no usar con `post_audit.md` en `FAIL`
  - no usar si `real_validation.md` requerido falta
  - no usar para extraer lecciones `F7`
- `motor`: `codex_preferred`
- `agent_id`: `m4.f6.codex.closeout_auditor`
- `agent_profile`: `codex_closeout_auditor`
- `phase`: `F6`
- `preconditions`:
  - `plan.md` congelado
  - `post_audit.md` con `PASS`
  - `real_validation.md` apto o `NO_APLICA`
- `inputs`:
  - artefactos de iniciativa
  - estado Git
  - diffs finales
- `read_set`:
  - `AGENTS.md`
  - `dev/workflow.md`
  - `dev/templates/initiative/closeout.md`
  - `README.md`
- `write_set`:
  - `dev/records/initiatives/<initiative_id>/closeout.md`
  - `README.md` si cambia superficie operativa, DX o flujo de uso
- `hard_rules`:
  - no reescribir el plan
  - README incremental obligatorio si aplica
  - working tree, commits, rama, push y merge deben quedar trazados
  - no presumir merge ni borrado de ramas: ejecutarlos o documentar bloqueo
    concreto
  - tras `F5` apta, el cierre estandar no se detiene en un handoff manual:
    debe continuar con `F7`, commit final, push, merge a `main/master`, push de
    troncal, borrado de ramas y refrescos post-merge salvo instruccion explicita
    de PR/merge manual o bloqueo tecnico
  - refrescar `SymDex` y `codebase-memory-mcp` solo si el merge a `main/master`
    ya ocurrio; si la iniciativa sigue en rama, registrar
    `PENDIENTE_HASTA_MERGE`
  - refrescar `governance_search` si el cierre integro cambios en el corpus de
    gobernanza
  - no reindexar una rama feature para hacer visibles sus simbolos en MCP
  - cerrar la respuesta de chat con `HANDOFF_SIGUIENTE_AGENTE` para `F7` solo si
    el entorno obliga a separar turnos; si motor auditor sigue activo, ejecutar `F7` en
    el mismo tramo
- `required_references`:
  - `dev/templates/initiative/closeout.md`
  - `dev/prompts/readme_update.md`
- `optional_references`:
  - `doc/governance_prompts/06_f6_f7_cierre_y_lecciones.md`
- `exit_checklist`:
  - `closeout.md` completo
  - README actualizado o `NO_APLICA` justificado
  - estado Git final trazado
  - backlogs/finding impacts declarados
  - TTL declarations registradas: si `plan.md` declara TTL en
    Decisiones D-XX, o `closeout.md` `## Riesgos remanentes` cita TTL,
    o cualquier nota del expediente menciona patrones tipo "se retira
    en X" / "diferido a Y" / "TTL = B?.?.?", el campo
    `ttl_declarations_registered: yes` exige entrada correspondiente
    en `architecture_findings_register.md` o
    `initiative_architecture_backlog.md` con criterio binario de
    cierre + owner asignado. Si `TTL_declarations_count > 0` con
    `ttl_declarations_registered: no`, NO declarar F6 completo;
    reabrir y registrar antes de avanzar a F7 (regla anti-deuda
    historica documentada en
    `feedback_ttl_declarado_se_olvida`)
  - cierre operativo completo o bloqueo concreto trazado
- `fallback_and_escalation`:
  - si working tree, commits, protecciones remotas o cambios ajenos no permiten
    cierre, dejar `CIERRE_GIT_BLOQUEADO_*` con siguiente paso minimo
  - si falta validacion, volver a `F5`
