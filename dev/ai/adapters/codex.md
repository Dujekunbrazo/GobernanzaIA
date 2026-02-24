# Adapter Codex

- Seguir `AGENTS.md` como contrato principal.
- Declarar y respetar modo operativo (`M0`..`M4`) al inicio de cada sesión.
- Ejecutar auditorías internas en F2.5, F5 y F8 cuando el modo sea `M4`.
- En auditorías, priorizar hallazgos de riesgo/regresión sobre estilo.
- No promover congelado si el resultado de auditoría es `FAIL`.
- Registrar bitácora tras cada respuesta final con:
  - `scripts/ops/bitacora_append.py`
  - `--ia codex`
  - `--pregunta <texto_usuario>`
  - `--respuesta <respuesta_final>`
