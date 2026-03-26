# Bitacora Rules (Hard)

Estas reglas definen la bitácora automática de trabajo con IAs para desarrollo.

## 1) Alcance

Aplica a interacciones de trabajo con:
- Codex
- Claude
- Gemini
- Roo

No aplica al runtime de un producto consumidor.

## 2) Ruta canónica

`dev/records/bitacora/`

Archivo por IA y día:
- `YYYY-MM-DD_codex.md`
- `YYYY-MM-DD_claude.md`
- `YYYY-MM-DD_gemini.md`
- `YYYY-MM-DD_roo.md`

## 3) Creación automática

- Si no existe archivo del día para esa IA, se crea al primer turno.
- Cada turno agrega bloque con:
  - hora
  - pregunta del usuario
  - respuesta de la IA
  - metadata opcional (`initiative_id`, fase)

## 4) Script oficial

Script canónico:
- `scripts/ops/bitacora_append.py`

Wrapper compatibilidad:
- `scripts/bitacora_append.py`

Validador canónico:
- `scripts/dev/check_bitacora_compliance.py`

## 5) Campos mínimos por turno

- `Usuario`
- `<IA>`
- timestamp

## 6) Seguridad

- Redactar patrones de secretos sensibles.
- No incluir contenido explícitamente marcado como no registrable si el operador lo indica.

## 7) Enforcements

- Cada adapter de IA debe registrar turno tras cada respuesta final.
- Toda instalación del baseline debe incluir el script de append y el
  validador de cumplimiento.
- Cierre de iniciativa requiere evidencia de bitácora del periodo trabajado.
- Esa evidencia debe poder validarse con
  `scripts/dev/check_bitacora_compliance.py`.
- En cierre `F8/F9`, el append de bitácora del cierre debe ejecutarse antes del
  commit formal final para evitar commits/push extra por trazabilidad tardía.

## 8) Regla de bloqueo

Si falla el append:
- marcar advertencia de trazabilidad
- reintentar una vez
- si persiste, registrar incidente en `closeout.md` y reflejar aprendizaje en
  `lessons_learned.md`

En cierre `F8/F9`:
- si el append falla, no cerrar la iniciativa como completa hasta resolver
  trazabilidad o documentar excepción explícita en `closeout.md`.

## 9) Modos de integración

- CLI directa:
  `python scripts/ops/bitacora_append.py --ia codex --pregunta "..." --respuesta "..."`
- Por archivos:
  `--pregunta-file` y `--respuesta-file`
- Por `stdin` JSON:
  `--stdin-json` con claves `ia`, `pregunta`, `respuesta`,
  `initiative_id`, `phase`

Objetivo:
- permitir integración homogénea desde distintas superficies/editoriales sin
  duplicar scripts por IA.


