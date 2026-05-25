# F4 — Post-Auditoría
> [!IMPORTANT]
> Bootstrap obligatorio de gobernanza antes de usar este prompt:
> leer `AGENTS.md`, cargar la Skill canonica si existe, usar `governance_search`
> para gobernanza con `phase`/`document_type` cuando aplique, usar `symdex_code`
> para codigo vivo y `codebase-memory-mcp` para wiring/impacto/legacy cuando
> toque codigo, y declarar cualquier degradacion antes de recurrir a lectura
> bruta.

Quiero hacer la post-auditoría de esta iniciativa.

Usa la iniciativa activa.

Audita la implementación contra el `plan.md`, el `execution.md` y la evidencia
de validación disponible.

Deja el resultado en `post_audit.md` dentro de la misma carpeta y confirma qué iniciativa estás auditando.

Reglas adicionales obligatorias:
- no uses la categoría `observaciones`
- toda debilidad, riesgo o ambigüedad material debe ir a `Hallazgos`
- si emites `FAIL`, cada hallazgo debe incluir contrato completo de
  remediación: `Tipo`, `Artefacto afectado`, `Seccion exacta`,
  `Archivos permitidos`, `Archivos prohibidos`, `Cambio minimo requerido`,
  `Criterio de cierre`, `Rerun scope`, `Reapertura requerida`, `Evidencia`
- si emites `PASS`, justifica explícitamente por qué no existe ningún
  hallazgo material ni pendiente
- si el plan define invariantes congeladas, audítalas primero
# Compatibilidad legacy

La fuente de verdad operativa para `F4` es
`dev/skills/f4_post_audit/SKILL.md`. Este prompt queda como atajo manual de solo
lectura.
