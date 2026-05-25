# SKILL

- `name`: `f1_plan_creation`
- `purpose`: crear o actualizar `plan.md` en `F1` con shape canonico, alcance acotado y salida apta para auditoria formal
- `when_to_use`:
  - existe iniciativa activa en `M4`
  - existe `input de planificacion` transitorio suficiente
  - toca crear o remediar `plan.md`
- `when_not_to_use`:
  - no usar para implementar
  - no usar para auditar
  - no usar si falta precondicion material; en ese caso devolver `BLOQUEADO`
- `motor`: `claude_preferred`
- `agent_id`: `m4.f1.claude.plan_architect`
- `agent_profile`: `claude_plan_architect`
- `phase`: `F1`
- `preconditions`:
  - existe carpeta de iniciativa
  - existe `input de planificacion` transitorio
  - el contexto tecnico ya fue aterrizado en `M0`
  - si el `input de planificacion` propone canon nuevo (nueva `BX.Y`,
    nuevo `access_pattern`, nuevo arquetipo trigger/receptor, nueva
    capability seed o renombrado de un tipo, capability o `BX.Y` ya
    canonizado), debe constar en el input o en `plan.md` la salida
    literal de `python scripts/dev/memory_precheck.py <termino_candidato>`
    con `Verdict: ALLOW` o `Verdict: BLOCK` y, si `BLOCK`, justificacion
    de que la propuesta es reconciliacion con canon previo (no canon
    nuevo). Esta es la operacionalizacion de `AGENTS.md` §5 Regla 32 a
    nivel de `F1`
- `inputs`:
  - `input de planificacion` transitorio
  - `dev/records/initiatives/<initiative_id>/plan.md` si ya existe
- `read_set`:
  - `AGENTS.md`
  - `dev/workflow.md`
  - `dev/guarantees/plan_gate.md`
  - `dev/policies/m4_artifact_shape_contract_policy.md`
  - `dev/templates/initiative/plan.md`
- `write_set`:
  - `dev/records/initiatives/<initiative_id>/plan.md`
- `hard_rules`:
  - cargar `AGENTS.md` antes de actuar y usar `governance_search` para
    localizar gobernanza aplicable de `F1`
  - si el plan toca codigo, usar `symdex_code` para codigo vivo y
    `codebase-memory-mcp` para wiring, impacto, legacy y blast radius antes de
    degradar a lectura bruta
  - si el plan propone canon nuevo (ver `preconditions`), ejecutar o
    citar literalmente la salida de `scripts/dev/memory_precheck.py` en
    el propio `plan.md` y rechazar avanzar mientras haya `Verdict: BLOCK`
    sin reconciliacion explicita (AGENTS.md §5 Regla 32)
  - declarar cualquier degradacion de tooling canonico antes de continuar
  - no implementar
  - no introducir alcance nuevo fuera del input validado
  - cerrar la respuesta de chat con `HANDOFF_SIGUIENTE_AGENTE` para `F2`
    cuando el usuario vaya a copiarla a Codex
  - usar headings y metadata canonicos
  - no omitir secciones obligatorias
  - si una seccion aplica poco, rellenarla explicitamente
- `required_references`:
  - `dev/prompts/plan_create.md`
  - `dev/guarantees/plan_gate.md`
  - `dev/templates/initiative/plan.md`
  - `dev/policies/m4_artifact_shape_contract_policy.md`
- `optional_references`:
  - `dev/policies/audit_finding_contract_policy.md`
  - `doc/governance_prompts/01_f1_plan.md`
- `exit_checklist`:
  - metadata obligatoria completa
  - headings canonicos presentes
  - `## Dudas abiertas` cerrado o bloqueado con evidencia
  - no hay headings inventados
  - el write set y el alcance estan reconciliados
  - si el plan propone canon nuevo, la salida de `memory_precheck.py`
    queda citada literal en `plan.md` con su verdict (Regla 32)
  - el plan queda apto para `F2`
- `fallback_and_escalation`:
  - si falta input o precondicion material, devolver `BLOQUEADO`
  - si hay contradiccion estructural no resoluble dentro de `plan.md`, parar y escalar a `M0`
