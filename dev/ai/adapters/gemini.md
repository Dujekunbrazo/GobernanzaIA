# Adapter Gemini

- Consumir primero `AGENTS.md`.
- Cargar antes `dev/policies/governance_manifest.md` como manifiesto corto de
  routing y carga mínima.
- Usar la capa estática mínima siempre presente y recuperar gobernanza bajo demanda.
- Usar `SymDex` solo para código vivo; no para gobernanza textual.
- Para gobernanza dinámica, usar `governance_search` con filtros por `phase`,
  `document_type` y `motor`.
- Para código vivo, usar `symdex_search_code` y `symdex_read_code`.
- Mantener `SymDex` como vía principal para búsqueda de código vivo y evitar
  búsquedas textuales amplias salvo fallback operativo.
- Aplicar reglas de ingeniería desde `dev/policies/ai_engineering_governance.md`.
- Cargar `doc/architecture/ai_engineering_dossier.md` solo cuando la tarea
  requiera profundidad adicional de arquitectura o trade-offs.
- Declarar y respetar modo operativo (`M0`..`M4`) al inicio de cada sesión.
- Mantener salida estructurada por fases del workflow en modo `M4`.
- Si Gemini es `motor_auditor`, no dejar hallazgos abiertos al devolver `PASS`.
- Si Gemini es `motor_auditor`, registrar como `observaciones` todo lo que no tenga impacto material.
- Si falta una precondición del modo activo, bloquear avance y reportarla con evidencia.
- Usar solo terminología activa: `motor_activo` y `motor_auditor`.
- Registrar bitácora tras cada respuesta final con:
  - `scripts/ops/bitacora_append.py`
  - `--ia gemini`
  - `--pregunta <texto_usuario>`
  - `--respuesta <respuesta_final>`
