# Records de Iniciativas

Esta carpeta almacena evidencia operativa por iniciativa.

## Estructura

`dev/records/initiatives/<initiative_id>/`

`dev/records/bitacora/`

`<initiative_id>` recomendado:
`YYYY-MM-DD_tema_corto`

## Artefactos estándar

- `M3`: `ask.md`, `execution.md`, `closeout.md`, `lessons_learned.md`
- `M4`: `ask.md`, `ask_audit.md`, `plan.md`, `plan_audit.md`, `execution.md`, `post_audit.md`, `closeout.md`, `lessons_learned.md`

Opcionales:
- `handoff.md` (`PRE-F1`, artefacto primogénito de apertura de `M4`)
- `baseline_freeze.md`

## Regla de apertura de iniciativa

- En `M0` no se crean artefactos.
- Tras la transición a `M4`, si la conversación o `Plan mode` ya generaron
  planificación útil, la salida durable debe guardarse en
  `dev/records/initiatives/<initiative_id>/handoff.md`.
- `handoff.md` se crea dentro de `M4`, antes de `F1`.
- `ask.md` y `plan.md` se derivan desde ese artefacto cuando exista.

## Política

- `dev/guarantees/*.md` contiene plantillas de gate (política).
- `dev/records/initiatives/*` contiene evidencia de ejecución (historial).
- `dev/records/bitacora/*` contiene conversación diaria por IA.
- `dev/records/legacy/*` conserva snapshots históricos previos a la normalización.
- Nomenclatura se valida con `scripts/dev/check_naming_compliance.py`.
- Estado base de organización se valida con `scripts/dev/check_state0.py`.
