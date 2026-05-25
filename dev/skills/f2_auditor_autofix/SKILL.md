# SKILL

- `name`: `f2_auditor_autofix`
- `purpose`: corregir fallos mecanicos de expediente elegibles tras `F2`/`F4 FAIL` y dejar el expediente listo para reauditoria inmediata
- `when_to_use`:
  - existe `plan_audit.md` o `post_audit.md` en `FAIL`
  - todos los hallazgos elegibles son mecanicos y locales al expediente o a
    reconciliaciones ya decididas entre `plan.md`, DoD, write set, sidecars,
    `execution.md`, `plan_audit.md` o `post_audit.md`
  - el write set permitido queda acotado a artefactos de iniciativa y, si
    aplica, al archivo de gobernanza/tooling ya implicado por el DoD
- `when_not_to_use`:
  - no usar para fallos de producto
  - no usar para reinterpretar alcance
  - no usar si el hallazgo exige cambiar policies, prompts canonicos o codigo
    de runtime
  - no usar si cambia objetivo, alcance sustantivo, producto, arquitectura,
    restricciones, criterios PASS/FAIL o decision material
- `motor`: `codex_preferred`
- `agent_id`: `m4.audit.codex.safe_autofix`
- `agent_profile`: `codex_auditor_autofix`
- `phase`: `F2`
- `preconditions`:
  - existe `plan_audit.md` valido
  - los hallazgos cumplen `SAFE_AUDITOR_AUTOFIX`
- `inputs`:
  - `dev/records/initiatives/<initiative_id>/plan_audit.md`
  - artefactos de iniciativa permitidos por el audit
- `read_set`:
  - `AGENTS.md`
  - `dev/workflow.md`
  - `dev/prompts/audit_autofix.md`
  - `dev/policies/audit_finding_contract_policy.md`
  - `dev/policies/m4_artifact_shape_contract_policy.md`
  - artefactos markdown permitidos del expediente
- `write_set`:
  - artefactos de iniciativa listados en `Archivos permitidos:`
  - archivo de gobernanza/tooling listado en `Archivos permitidos:` solo si el
    DoD o write set congelado ya lo implicaba
- `hard_rules`:
  - aplicar solo el cambio minimo requerido
  - respetar literalmente `Archivos permitidos`, `Rerun scope` y `Reapertura requerida`
  - corregir en el acto los fallos mecanicos elegibles; no devolver a Claude
    por ceremonia
  - no tocar prompts canonicos, policies ni codigo de producto
  - no reescribir el artefacto de auditoria
  - cerrar la respuesta de chat con `HANDOFF_SIGUIENTE_AGENTE` para reauditoria
    de la misma fase
- `required_references`:
  - `dev/prompts/audit_autofix.md`
  - `dev/policies/audit_finding_contract_policy.md`
  - `dev/policies/m4_artifact_shape_contract_policy.md`
- `optional_references`:
  - `dev/prompts/plan_audit.md`
- `exit_checklist`:
  - solo se modificaron artefactos permitidos
  - el expediente mantiene shape canonico
  - el cambio es mecanico y trazable
  - el expediente queda listo para reauditoria inmediata
- `fallback_and_escalation`:
  - si cualquier hallazgo deja de ser elegible, parar y reabrir la fase minima
    necesaria
  - si el autofix no cierra el hallazgo, volver al flujo normal de `FAIL`
