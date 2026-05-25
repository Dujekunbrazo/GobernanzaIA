# SKILL

- `name`: `f5_real_validation`
- `purpose`: conducir con motor auditor y el usuario la validacion real observable y registrar `real_validation.md`
- `when_to_use`:
  - `post_audit.md` tiene `PASS`
  - la iniciativa cambia comportamiento observable o superficie operativa
  - toca decidir `APTA_PARA_F6`, `REABRIR_F3` o `NO_APLICA`
- `when_not_to_use`:
  - no usar antes de `F4 PASS`
  - no usar para implementar fixes
  - no inventar evidencia si no hay runtime/log/salida observable
- `motor`: `codex_preferred`
- `agent_id`: `m4.f5.codex.real_validation_guide`
- `agent_profile`: `codex_real_validation_guide`
- `phase`: `F5`
- `preconditions`:
  - `post_audit.md` con `PASS`
  - criterios observables definidos
  - usuario disponible si la validacion requiere interaccion
- `inputs`:
  - `plan.md`
  - `execution.md`
  - `post_audit.md`
  - runtime, terminal, logs o salida observable
- `read_set`:
  - `AGENTS.md`
  - `dev/workflow.md`
  - `dev/templates/initiative/real_validation.md`
- `write_set`:
  - `dev/records/initiatives/<initiative_id>/real_validation.md`
- `hard_rules`:
  - ejecutar barrido real antes de decidir fixes
  - si hay fallo material, decision `REABRIR_F3`
  - `F6` solo empieza con `APTA_PARA_F6` o `NO_APLICA` justificado
  - la decision final debe escribirse como linea literal exacta:
    `- Decisión final: APTA_PARA_F6` (o `REABRIR_F3` o `NO_APLICA`);
    solo esos tres valores son aceptados por el parser canonico
  - cerrar la respuesta de chat con `HANDOFF_SIGUIENTE_AGENTE` para `F3` si
    hay `REABRIR_F3`, o para `F6` si hay `APTA_PARA_F6`/`NO_APLICA`
- `required_references`:
  - `dev/prompts/real_validation.md`
  - `dev/templates/initiative/real_validation.md`
- `optional_references`:
  - logs o traces de la superficie validada
- `exit_checklist`:
  - matriz de casos completada
  - evidencia real registrada
  - linea literal `- Decisión final: APTA_PARA_F6 | REABRIR_F3 | NO_APLICA`
    presente en `real_validation.md` con exactamente uno de los tres valores
  - fallos materiales abren `F3`
- `fallback_and_escalation`:
  - si falta evidencia real, estado `BLOQUEADO`
  - si se reabre `F3`, repetir `F4` y `F5`
