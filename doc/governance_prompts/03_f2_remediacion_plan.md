# Remediación De `plan.md` Tras `F2 FAIL`
> [!IMPORTANT]
> Bootstrap obligatorio de gobernanza antes de usar este prompt:
> leer `AGENTS.md`, cargar la Skill canonica si existe, usar `governance_search`
> para gobernanza con `phase`/`document_type` cuando aplique, usar `symdex_code`
> para codigo vivo y `codebase-memory-mcp` para wiring/impacto/legacy cuando
> toque codigo, y declarar cualquier degradacion antes de recurrir a lectura
> bruta.

La fuente de verdad operativa para esta capability es
`dev/skills/f2_auditor_autofix/SKILL.md`.

Usa la iniciativa activa de esta conversación y el `plan_audit.md` más
reciente.

Lee:

- `plan.md`
- `plan_audit.md`
- `dev/policies/audit_finding_contract_policy.md`

Objetivo:

- corregir `plan.md` para cerrar todos los hallazgos materiales abiertos de
  `F2`
- dejar el plan listo para nueva auditoría

Reglas:

- no introduzcas alcance nuevo
- no rebajes la exigencia del audit
- no toques código
- mantén `plan.md` en estado apto para reauditoría
- si el audit pide shape o metadata canónica, corrige exactamente eso y no otra
  cosa
- si falta una precondición o hay contradicción material, el estado correcto es
  `BLOQUEADO`

Antes de seguir, confirma qué iniciativa estás corrigiendo y luego actualiza
`plan.md`.
