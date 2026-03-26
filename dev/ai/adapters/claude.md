# Adapter Claude

- Seguir `AGENTS.md` y `dev/workflow.md`.
- Cargar antes `dev/policies/governance_manifest.md` como manifiesto corto de
  routing y carga mínima.
- Usar la capa estática mínima siempre presente y recuperar gobernanza bajo demanda.
- Usar `SymDex` solo para código vivo; no para gobernanza textual.
- Aplicar reglas de ingeniería desde `dev/policies/ai_engineering_governance.md`.
- Cargar `doc/architecture/ai_engineering_dossier.md` solo cuando la tarea
  requiera profundidad adicional de arquitectura o trade-offs.
- Declarar y respetar modo operativo (`M0`..`M4`) al inicio de cada sesión.
- Si Claude abre una iniciativa `M4` o usa `Plan mode` para prepararla, no
  dejar la planificación solo en chat: tras la transición a `M4`, persistirla
  en `dev/records/initiatives/<initiative_id>/handoff.md` antes de `F1`.
- Si Claude es `motor_activo`, no ejecutar implementación en `M4` sin `plan.md` en estado `CONGELADO`.
- Si Claude es `motor_auditor`, emitir auditorías con decisión `PASS` o `FAIL`.
- Si Claude es `motor_auditor`, usar `hallazgos` solo para problemas materiales y `observaciones` para ruido no bloqueante.
- Para gobernanza dinámica, usar `governance_search` con filtros por `phase`,
  `document_type` y `motor` antes de cargar documentos completos.
- Para código vivo, usar `symdex_search_code` y luego `symdex_read_code`.
- Mantener `SymDex` como vía principal para búsqueda de código vivo y evitar
  búsquedas textuales amplias salvo fallback operativo.
- Routing obligatorio:
  - gobernanza -> `governance_search` y luego lectura canónica
  - código -> `symdex_search_code` y luego `symdex_read_code`
- No usar `Glob`, `Globpattern`, `Grep`, `find`, `rg` o lecturas directas como
  vía principal si `governance_search` o `symdex_search_code` están expuestos.
- Herramientas internas solo como fallback si el MCP falla, no está disponible o
  para lectura final puntual del archivo ya localizado.
- En respuestas técnicas, declarar herramienta usada y fuente canónica usada.
- Al inicio de sesión o tras recarga, comprobar si están disponibles
  `governance_search`, `symdex_search_code` y `symdex_read_code`; si no lo
  están, declarar limitación operativa.
- Registrar bloqueos de proceso con evidencia concreta (ruta + estado faltante).
- Usar solo terminología activa: `motor_activo` y `motor_auditor`.
- Registrar bitácora tras cada respuesta final con:
  - `scripts/ops/bitacora_append.py`
  - `--ia claude`
  - `--pregunta <texto_usuario>`
  - `--respuesta <respuesta_final>`
