# Adapter Roo Code

- `.roo/rules/*` actúa como capa de ejecución, no como fuente normativa primaria.
- Toda regla de Roo debe apuntar a `AGENTS.md` y `dev/workflow.md`.
- Declarar y respetar modo operativo (`M0`..`M4`) al inicio de cada sesión.
- Si Roo y `AGENTS.md` difieren, se debe corregir Roo en el mismo cambio.
- Registrar bitácora tras cada respuesta final con:
  - `scripts/ops/bitacora_append.py`
  - `--ia roo`
  - `--pregunta <texto_usuario>`
  - `--respuesta <respuesta_final>`
