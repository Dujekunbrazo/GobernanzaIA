# Naming Rules (Hard)

Estas reglas fijan la nomenclatura obligatoria para artefactos de proceso.

## 1) Iniciativas

Carpeta:
- `dev/records/initiatives/<initiative_id>/`

Patrón de `<initiative_id>`:
- `YYYY-MM-DD_tema_corto`
- regex: `^\d{4}-\d{2}-\d{2}_[a-z0-9_]+$`

Cabecera mínima esperada en artefactos principales:
- `Initiative ID`
- `Modo`
- `Estado`
- `Fecha`
- `motor_activo`
- `motor_auditor` (obligatorio en `M4`)
- `Rama`
- `baseline_mit`

Set mínimo por modo:
- `M3`: `ask.md`, `execution.md`, `closeout.md`, `lessons_learned.md`
- `M4`: `ask.md`, `ask_audit.md`, `plan.md`, `plan_audit.md`, `execution.md`,
  `post_audit.md`, `closeout.md`, `lessons_learned.md`

Archivos opcionales permitidos:
- `handoff.md` (`PRE-F1`, artefacto primogénito para conservar planificación previa)
- `baseline_freeze.md`
- `capability_closure.md`
- `exception_record.md`
- `real_validation.md`

## 2) Bitácora diaria por IA

Carpeta:
- `dev/records/bitacora/`

Patrón de archivo:
- `YYYY-MM-DD_<ia>.md`
- `<ia>` permitido: `codex`, `claude`
- regex: `^\d{4}-\d{2}-\d{2}_(codex|claude)\.md$`

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
- `lessons_learned.md`

Archivos opcionales recomendados:
- `capability_closure.md`
- `exception_record.md`
- `real_validation.md`

## 4) Adaptadores IA

Carpeta:
- `dev/ai/adapters/`

Archivos esperados:
- `codex.md`
- `claude.md`

## 5) Validación obligatoria

Script oficial:
- `scripts/dev/check_naming_compliance.py`

Si hay errores de nomenclatura:
- no se puede cerrar iniciativa
- estado mínimo: `BLOQUEADO` hasta corregir
