# Adapter Gemini

- Consumir primero `AGENTS.md`.
- Declarar y respetar modo operativo (`M0`..`M4`) al inicio de cada sesión.
- Mantener salida estructurada por fases del workflow solo en modo `M4`.
- Si falta una precondición del modo activo, bloquear avance y reportarla con evidencia.
- Registrar bitácora tras cada respuesta final con:
  - `scripts/ops/bitacora_append.py`
  - `--ia gemini`
  - `--pregunta <texto_usuario>`
  - `--respuesta <respuesta_final>`
