# AI Governance Layer

Esta carpeta contiene los adaptadores canónicos del sistema.

Para cualquier trabajo asistido por IA en este repo:
- Directriz maestra: `AGENTS.md`
- Workflow operativo: `dev/workflow.md`
- Gates de proceso: `dev/guarantees/`
- Policy de ingeniería (lectura base): `dev/policies/ai_engineering_governance.md`
- Dossier largo de ingeniería (lectura condicional): `doc/architecture/ai_engineering_dossier.md`
- Adaptadores activos: `dev/ai/adapters/claude.md` y
  `dev/ai/adapters/codex.md`

Regla dura:
- No mezclar carpetas del proyecto Python con gobernanza IA.
- Declarar modo operativo (`M0`..`M4`) al inicio.
- `Claude` es el motor activo del repo.
- `Codex` es el motor auditor del repo.
- Mantener carga condicional: usar el dosier largo solo cuando el tipo de tarea
  lo requiera.
