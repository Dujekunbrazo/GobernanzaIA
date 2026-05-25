# F1 — Crear `plan.md`
> [!IMPORTANT]
> Bootstrap obligatorio de gobernanza antes de usar este prompt:
> leer `AGENTS.md`, cargar la Skill canonica si existe, usar `governance_search`
> para gobernanza con `phase`/`document_type` cuando aplique, usar `symdex_code`
> para codigo vivo y `codebase-memory-mcp` para wiring/impacto/legacy cuando
> toque codigo, y declarar cualquier degradacion antes de recurrir a lectura
> bruta.

Atajo manual para la fase canónica `F1`.

La fuente de verdad operativa para esta capability es
`dev/skills/f1_plan_creation/SKILL.md`.

Usa la iniciativa activa y el `input de planificación` transitorio preparado en
esta conversación.

Actúa siguiendo:

- `AGENTS.md`
- `dev/workflow.md`
- `dev/skills/f1_plan_creation/SKILL.md`
- `dev/prompts/plan_create.md`
- `dev/policies/m4_artifact_shape_contract_policy.md`

Objetivo:

- generar o actualizar `plan.md` en la carpeta correcta
- respetar exactamente la plantilla y headings canónicos de
  `dev/templates/initiative/plan.md`
- dejar el artefacto listo para `F2`

Reglas mínimas:

- no implementar
- no introducir alcance nuevo
- no omitir headings ni metadata obligatoria
- si falta una precondición, devolver `BLOQUEADO` con evidencia

Antes de seguir:

1. confirma qué iniciativa estás usando
2. confirma que existe `input de planificación` transitorio suficiente
3. genera o actualiza `plan.md`
