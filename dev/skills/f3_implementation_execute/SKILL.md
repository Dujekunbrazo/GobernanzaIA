# SKILL

- `name`: `f3_implementation_execute`
- `purpose`: ejecutar `plan.md` congelado en `F3`, tramo a tramo, registrando evidencia real en `execution.md`
- `when_to_use`:
  - existe iniciativa `M4`
  - `plan.md` esta `CONGELADO`
  - `plan_audit.md` tiene `PASS`
- `when_not_to_use`:
  - no usar para crear o auditar planes
  - no usar si el plan no esta congelado
  - no usar para cerrar `F5-F7`
- `motor`: `claude_preferred`
- `agent_id`: `m4.f3.claude.implementation_executor`
- `agent_profile`: `claude_implementation_executor`
- `phase`: `F3`
- `preconditions`:
  - `plan.md` congelado
  - `plan_audit.md` con `PASS`
  - write set permitido claro
- `inputs`:
  - `dev/records/initiatives/<initiative_id>/plan.md`
  - `dev/records/initiatives/<initiative_id>/plan_audit.md`
- `read_set`:
  - `AGENTS.md`
  - `dev/workflow.md`
  - `dev/guarantees/implementation_gate.md`
  - `dev/templates/initiative/execution.md`
- `write_set`:
  - archivos permitidos por `plan.md`
  - `dev/records/initiatives/<initiative_id>/execution.md`
- `hard_rules`:
  - cargar `AGENTS.md` antes de actuar y usar `governance_search` para
    localizar gobernanza aplicable de `F3`
  - usar `symdex_code` para codigo vivo y `codebase-memory-mcp` para wiring,
    impacto, legacy y blast radius cuando el tramo toque codigo
  - declarar cualquier degradacion de tooling canonico antes de usar lectura
    bruta como via principal
  - implementar solo el plan congelado
  - actuar como ejecutor: no replanificar ni ampliar alcance; si el plan no
    basta, devolver `BLOQUEADO` con evidencia
  - un cambio logico por commit
  - no cerrar la iniciativa desde `F3`
  - parar si aparece desviacion material
  - cerrar la respuesta de chat con `HANDOFF_SIGUIENTE_AGENTE` para `F4`
    cuando el usuario vaya a copiarla a Codex
- `required_references`:
  - `dev/prompts/implementation_execute.md`
  - `dev/guarantees/implementation_gate.md`
  - `dev/templates/initiative/execution.md`
- `optional_references`:
  - `doc/governance_prompts/04_f3_implementacion.md`
- `exit_checklist`:
  - cambios dentro del write set
  - `execution.md` actualizado
  - validacion dirigida ejecutada o bloqueo trazado
  - riesgos y desvios registrados
- `fallback_and_escalation`:
  - si falta precondicion, devolver `BLOQUEADO`
  - si el alcance cambia, reabrir `F1`
