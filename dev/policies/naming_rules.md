# Naming Rules (Hard)

Estas reglas fijan la nomenclatura obligatoria para artefactos de proceso.

## 1) Iniciativas

Carpeta:
- `dev/records/initiatives/<initiative_id>/`

Patrón de `<initiative_id>`:
- `YYYY-MM-DD_tema_corto`
- regex: `^\d{4}-\d{2}-\d{2}_[a-z0-9_]+$`

Archivos estándar permitidos por iniciativa:
- `ask.md`
- `ask_audit.md`
- `plan.md`
- `plan_audit.md`
- `execution.md`
- `post_audit.md`
- `closeout.md`
- `handoff.md` (opcional)

## 2) Bitácora diaria por IA

Carpeta:
- `dev/records/bitacora/`

Patrón de archivo:
- `YYYY-MM-DD_<ia>.md`
- `<ia>` permitido: `codex`, `claude`, `gemini`, `roo`
- regex: `^\d{4}-\d{2}-\d{2}_(codex|claude|gemini|roo)\.md$`

## 3) Templates de iniciativa

Carpeta:
- `dev/templates/initiative/`

Archivos requeridos:
- `ask.md`
- `ask_audit.md`
- `plan.md`
- `plan_audit.md`
- `execution.md`
- `post_audit.md`
- `closeout.md`

## 4) Adaptadores IA

Carpeta:
- `dev/ai/adapters/`

Archivos esperados:
- `codex.md`
- `claude.md`
- `gemini.md`
- `roo.md`

## 5) Validación obligatoria

Script oficial:
- `scripts/dev/check_naming_compliance.py`

Si hay errores de nomenclatura:
- no se puede cerrar iniciativa
- estado mínimo: `BLOQUEADO` hasta corregir
