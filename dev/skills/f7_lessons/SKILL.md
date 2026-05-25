# SKILL

- `name`: `f7_lessons`
- `purpose`: extraer lecciones finales y registrar follow-ups vivos tras el cierre operativo
- `when_to_use`:
  - `F6` esta completado o en cierre operativo trazado
  - toca escribir `lessons_learned.md`
- `when_not_to_use`:
  - no usar para reabrir implementacion
  - no usar para esconder deuda material
  - no usar antes de conocer resultado de `F6`
- `motor`: `codex_preferred`
- `agent_id`: `m4.f7.codex.lessons_curator`
- `agent_profile`: `codex_lessons_curator`
- `phase`: `F7`
- `preconditions`:
  - `closeout.md` existe
  - estado de backlog/finding decidido
- `inputs`:
  - `plan.md`
  - `execution.md`
  - `post_audit.md`
  - `real_validation.md`
  - `closeout.md`
- `read_set`:
  - `AGENTS.md`
  - `dev/workflow.md`
  - `dev/templates/initiative/lessons_learned.md`
  - memoria operativa viva si aplica
- `write_set`:
  - `dev/records/initiatives/<initiative_id>/lessons_learned.md`
  - backlogs o findings solo si `closeout.md` lo exige
- `hard_rules`:
  - no duplicar el plan
  - no dejar remanentes enterrados solo en lessons
  - propuestas deben tener decision
  - si `F6` forma parte de un cierre completo autorizado, no detenerse tras
    crear `lessons_learned.md`: continuar con commit final, push, merge,
    refrescos post-merge y borrado de ramas segun
    `dev/policies/git_workflow_rules.md`
  - cerrar la respuesta de chat con `HANDOFF_SIGUIENTE_AGENTE` con
    `Siguiente fase: N/A` solo cuando el cierre operativo ya este completo o
    bloqueado con causa concreta
- `required_references`:
  - `dev/templates/initiative/lessons_learned.md`
- `optional_references`:
  - `dev/records/reviews/initiative_backlog.md`
  - `dev/records/reviews/initiative_architecture_backlog.md`
  - `dev/records/reviews/architecture_findings_register.md`
- `exit_checklist`:
  - lecciones tecnicas y de proceso registradas
  - propuestas con decision
  - remanentes vivos enviados a backlog/finding si aplica
  - estado Git final completo o bloqueo concreto reflejado en `closeout.md`
- `fallback_and_escalation`:
  - si aparece deuda material no cerrada, reabrir fase correspondiente
