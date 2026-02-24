# AI Governance Layer

Esta carpeta contiene adaptadores por motor para aplicar una sola política.

Para cualquier trabajo asistido por IA en este repo:
- Directriz maestra: `AGENTS.md`
- Workflow operativo: `dev/workflow.md`
- Gates de proceso: `dev/guarantees/`
- Adaptadores por motor (Codex/Claude/Gemini/Roo): `dev/ai/adapters/`
- Bitácora diaria por IA: `dev/records/bitacora/` (script: `scripts/ops/bitacora_append.py`)

Regla dura:
- No mezclar carpetas del proyecto Python con gobernanza IA.
- Declarar modo operativo (`M0`..`M4`) al inicio; usar F1-F9 completo solo en `M4`.
