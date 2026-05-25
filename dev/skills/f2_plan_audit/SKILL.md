# SKILL

- `name`: `f2_plan_audit`
- `purpose`: auditar formalmente `plan.md` y emitir `PASS` o `FAIL` con contrato completo de hallazgos
- `when_to_use`:
  - existe `plan.md` en estado `PROPUESTO`
  - toca ejecutar `F2`
- `when_not_to_use`:
  - no usar para remediar `plan.md`
  - no usar para implementar
  - no usar si falta `plan.md` o falta precondicion minima
- `motor`: `codex_preferred`
- `agent_id`: `m4.f2.codex.plan_auditor`
- `agent_profile`: `codex_plan_auditor`
- `phase`: `F2`
- `preconditions`:
  - existe `dev/records/initiatives/<initiative_id>/plan.md`
  - el artefacto tiene metadata y headings minimos para ser auditado
- `inputs`:
  - `dev/records/initiatives/<initiative_id>/plan.md`
- `read_set`:
  - `AGENTS.md`
  - `dev/workflow.md`
  - `dev/prompts/plan_audit.md`
  - `dev/policies/audit_finding_contract_policy.md`
  - `dev/guarantees/plan_gate.md`
- `write_set`:
  - `dev/records/initiatives/<initiative_id>/plan_audit.md`
- `hard_rules`:
  - actuar como auditor de plan: evaluar congelabilidad, alcance,
    decisiones, riesgos y validacion prevista; no auditar implementacion
    inexistente
  - emitir solo `PASS` o `FAIL`
  - prohibido usar categoria `observaciones`
  - si hay `FAIL`, cada hallazgo debe incluir contrato completo
  - no reescribir `plan.md` durante auditoria
  - no introducir alcance nuevo
  - detectar TTL declarations en `plan.md`: si cualquier Decision
    D-XX, `## Riesgos remanentes` o nota del expediente cita patrones
    como "se retira en B?.?", "diferido a Y", "TTL = B?.?.?",
    "deferred to X", el plan DEBE incluir tambien (a) un campo
    `followup_target` en la decision con `architecture_findings_register.md`
    o `initiative_architecture_backlog.md` como destino, (b) criterio
    binario de cierre del TTL verificable por grep/test, y (c) owner
    explicito (`initiative_id` siguiente o `"sin owner declarado"`).
    Sin estos 3 campos, emitir FAIL con hallazgo
    `TTL_DECLARATION_SIN_FOLLOWUP` (regla anti-deuda historica
    historica documentada en
    `feedback_ttl_declarado_se_olvida`)
  - cerrar la respuesta de chat con `HANDOFF_SIGUIENTE_AGENTE` para `F1`
    si hay `FAIL`, o para `F3` si hay `PASS`
- `required_references`:
  - `dev/prompts/plan_audit.md`
  - `dev/policies/audit_finding_contract_policy.md`
  - `dev/guarantees/plan_gate.md`
- `optional_references`:
  - `doc/governance_prompts/02_f2_auditoria_plan.md`
  - `doc/governance_prompts/03_f2_remediacion_plan.md`
- `exit_checklist`:
  - existe `plan_audit.md`
  - veredicto `PASS` o `FAIL`
  - si `FAIL`, todos los hallazgos estan tipados y cerrables
  - existe `## Justificación del veredicto`
  - existe `## Escalado de remediacion`
- `fallback_and_escalation`:
  - si falta precondicion material, emitir `FAIL` con evidencia
  - si no se puede tipar ni cerrar un hallazgo, el estado correcto es `FAIL`
