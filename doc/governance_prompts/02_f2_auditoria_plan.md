# F2 — Auditoría De `plan.md`
> [!IMPORTANT]
> Bootstrap obligatorio de gobernanza antes de usar este prompt:
> leer `AGENTS.md`, cargar la Skill canonica si existe, usar `governance_search`
> para gobernanza con `phase`/`document_type` cuando aplique, usar `symdex_code`
> para codigo vivo y `codebase-memory-mcp` para wiring/impacto/legacy cuando
> toque codigo, y declarar cualquier degradacion antes de recurrir a lectura
> bruta.

Atajo manual para la fase canónica `F2`.

La fuente de verdad operativa para esta capability es
`dev/skills/f2_plan_audit/SKILL.md`.

Usa la iniciativa activa.

Actúa siguiendo:

- `AGENTS.md`
- `dev/workflow.md`
- `dev/skills/f2_plan_audit/SKILL.md`
- `dev/prompts/plan_audit.md`
- `dev/policies/audit_finding_contract_policy.md`

Objetivo:

- auditar `plan.md`
- dejar el resultado en `plan_audit.md`
- emitir solo `PASS` o `FAIL`

Reglas adicionales obligatorias:

- no uses la categoría `observaciones`
- toda debilidad, riesgo o ambigüedad material debe ir a `Hallazgos`
- si emites `FAIL`, cada hallazgo debe incluir contrato completo de
  remediación: `Tipo`, `Artefacto afectado`, `Seccion exacta`,
  `Archivos permitidos`, `Archivos prohibidos`, `Cambio minimo requerido`,
  `Criterio de cierre`, `Rerun scope`, `Reapertura requerida`, `Evidencia`
- si emites `PASS`, justifica explícitamente por qué no existe ningún hallazgo
  material ni pendiente

Antes de seguir:

1. confirma qué iniciativa estás auditando
2. audita `plan.md`
3. escribe `plan_audit.md` en la carpeta correcta
