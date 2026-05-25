# F3 — Implementación
> [!IMPORTANT]
> Bootstrap obligatorio de gobernanza antes de usar este prompt:
> leer `AGENTS.md`, cargar la Skill canonica si existe, usar `governance_search`
> para gobernanza con `phase`/`document_type` cuando aplique, usar `symdex_code`
> para codigo vivo y `codebase-memory-mcp` para wiring/impacto/legacy cuando
> toque codigo, y declarar cualquier degradacion antes de recurrir a lectura
> bruta.

Quiero ejecutar esta iniciativa según la gobernanza del repo.

Usa la iniciativa activa y actúa siguiendo:

- `AGENTS.md`
- `dev/workflow.md`
- `dev/prompts/implementation_execute.md`
- `dev/guarantees/implementation_gate.md`

Antes de seguir:

1. Confirma qué iniciativa vas a implementar.
2. Verifica que existe `plan.md` en estado `CONGELADO`.
3. Verifica que existe `plan_audit.md` con resultado `PASS`.

Si alguna precondición falla:

- no implementes
- devuelve `BLOQUEADO` con evidencia

Reglas adicionales obligatorias:

- implementa tramo a tramo o commit a commit, sin salirte del `plan.md`
- actualiza `execution.md` en la carpeta correcta
- en cada tramo registra intención, archivos tocados, validación y resultado
- por defecto usa tests dirigidos al `write set`
- no ejecutes la suite completa en cada tramo salvo que el plan lo exija, el
  cambio sea sistémico o estemos cerrando `F6`
- si ejecutas la suite completa, justifica explícitamente por qué
- si detectas desviación material, riesgo nuevo o bloqueo, para y repórtalo
  antes de seguir
- no cierres la iniciativa desde esta fase

Objetivo de la fase:

- ejecutar `plan.md` congelado con trazabilidad real en `execution.md`
- minimizar coste de validación sin perder señal
- dejar la iniciativa lista para `F4`, no para cierre
# Compatibilidad legacy

La fuente de verdad operativa para `F3` es
`dev/skills/f3_implementation_execute/SKILL.md`. Este prompt queda como atajo
manual de solo lectura.
