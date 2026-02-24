# Adapter Claude

- Seguir `AGENTS.md` y `dev/workflow.md`.
- Declarar y respetar modo operativo (`M0`..`M4`) al inicio de cada sesión.
- No ejecutar implementación en `M4` sin artefacto `plan.md` en estado `CONGELADO`.
- Registrar bloqueos de proceso con evidencia concreta (ruta + estado faltante).
- Registrar bitácora tras cada respuesta final con:
  - `scripts/ops/bitacora_append.py`
  - `--ia claude`
  - `--pregunta <texto_usuario>`
  - `--respuesta <respuesta_final>`
