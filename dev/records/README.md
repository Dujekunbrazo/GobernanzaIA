# Records de Iniciativas

Esta carpeta almacena evidencia operativa por iniciativa.

## Estructura

`dev/records/initiatives/<initiative_id>/`

`dev/records/bitacora/`

`<initiative_id>` recomendado:
`YYYY-MM-DD_tema_corto`

## Artefactos estándar

- `ask.md`
- `ask_audit.md`
- `plan.md`
- `plan_audit.md`
- `execution.md`
- `post_audit.md`
- `closeout.md`

## Política

- `dev/guarantees/*.md` contiene plantillas de gate (política).
- `dev/records/initiatives/*` contiene evidencia de ejecución (historial).
- `dev/records/bitacora/*` contiene conversación diaria por IA.
- `dev/records/legacy/*` conserva snapshots históricos previos a la normalización.
- Nomenclatura se valida con `scripts/dev/check_naming_compliance.py`.
- Estado base de organización se valida con `scripts/dev/check_state0.py`.
