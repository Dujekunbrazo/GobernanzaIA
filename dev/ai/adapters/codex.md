# Adapter Codex

- Seguir `AGENTS.md` como contrato principal.
- Cargar antes `dev/policies/governance_manifest.md` como manifiesto corto de
  routing y carga mínima.
- Usar la capa estática mínima siempre presente y recuperar gobernanza bajo demanda.
- Usar `SymDex` solo para código vivo; no para gobernanza textual.
- Aplicar reglas de ingeniería desde `dev/policies/ai_engineering_governance.md`.
- Cargar `doc/architecture/ai_engineering_dossier.md` solo cuando la tarea
  requiera profundidad adicional de arquitectura o trade-offs.
- Declarar y respetar modo operativo (`M0`..`M4`) al inicio de cada sesión.
- Si Codex es `motor_activo`, ejecutar fases de propuesta/plan/implementación según `dev/workflow.md`.
- Si Codex es `motor_auditor`, auditar en `F3`, `F5` y `F7`.
- Para gobernanza dinámica, usar `governance_search` con filtros por `phase`,
  `document_type` y `motor` antes de cargar documentos completos.
- Para código vivo, usar `semantic_search` y luego `get_symbol` (via symdex_code).
- Mantener `SymDex` como vía principal para búsqueda de código vivo y evitar
  búsquedas textuales amplias salvo fallback operativo.
- En auditorías, registrar como `hallazgos` solo problemas materiales.
- En auditorías, mover el ruido editorial o cosmético a `observaciones`.
- No promover congelado/cierre si el resultado de auditoría es `FAIL`.
- Usar solo terminología activa: `motor_activo` y `motor_auditor`.
- En cierres Git (`F9/F10`) con historial de `Permission denied` en `.git`,
  pedir permisos efectivos al inicio del bloque de cierre y evitar reintentos
  en bucle de `git add/commit/push`.
- Registrar bitácora tras cada respuesta final con:
  - `scripts/ops/bitacora_append.py`
  - `--ia codex`
  - `--pregunta <texto_usuario>`
  - `--respuesta <respuesta_final>`
