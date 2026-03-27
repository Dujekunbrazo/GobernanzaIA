# Adapter Roo Code

- `.roo/rules/*` actúa como capa de ejecución, no como fuente normativa primaria.
- Toda regla de Roo debe apuntar a `AGENTS.md` y `dev/workflow.md`.
- Cargar antes `dev/policies/governance_manifest.md` como manifiesto corto de
  routing y carga mínima.
- Los modos nativos de Roo no redefinen `M0-M4` ni `F1-F10`.
- Los modos nativos `Ask/Architect/Code/Debug/Orchestrator` son solo una piel
  de producto; el proceso real sigue siendo `M0-M4` y `F1-F10`.
- Roo puede actuar como `motor_activo` o `motor_auditor` solo si el usuario lo designa explícitamente.
- Usar la capa estática mínima siempre presente y recuperar gobernanza bajo demanda.
- Usar `SymDex` solo para código vivo; no para gobernanza textual.
- Para gobernanza dinámica, usar `governance_search` con filtros por `phase`,
  `document_type` y `motor`.
- Para código vivo, usar `semantic_search` y `get_symbol` (via symdex_code).
- Mantener `SymDex` como vía principal para búsqueda de código vivo y evitar
  búsquedas textuales amplias salvo fallback operativo.
- Routing obligatorio:
  - consulta de gobernanza -> `governance_search` y luego lectura canónica
  - consulta de código -> `semantic_search` y luego `get_symbol` (via symdex_code)
- No sustituir ese routing por tools internas salvo bloqueo declarado con
  evidencia.
- En cada respuesta técnica, declarar herramienta usada y fuente canónica usada.
- No usar `dev/records/initiatives/` como fuente principal de proceso si existe
  fuente canónica en `dev/`.
- Al inicio de sesión o tras recarga, comprobar si están disponibles
  `governance_search`, `semantic_search` y `get_symbol` (via symdex_code); si no lo
  están, declarar limitación operativa.
- Si una auditoría formal (`F3`, `F5` o `F7`) va a ejecutarse en Roo, preguntar
  explícitamente al usuario si desea cambiar de API/modelo antes de iniciar la
  auditoría.
- Si Roo no puede ver el modelo/API actual, declararlo como `no visible` y pedir
  igualmente confirmación.
- Sin confirmación explícita del usuario sobre mantener o cambiar la API/modelo
  para la auditoría, estado = `BLOQUEADO`.
- Aplicar reglas de ingeniería desde `dev/policies/ai_engineering_governance.md`.
- Cargar `doc/architecture/ai_engineering_dossier.md` solo cuando la tarea
  requiera profundidad adicional de arquitectura o trade-offs.
- Declarar y respetar modo operativo (`M0`..`M4`) al inicio de cada sesión.
- Si Roo es `motor_activo` o `motor_auditor`, respetar el rol designado en la iniciativa.
- Si Roo y `AGENTS.md` difieren, se debe corregir Roo en el mismo cambio.
- Usar solo terminología activa: `motor_activo` y `motor_auditor`.
- Registrar bitácora tras cada respuesta final con:
  - `scripts/ops/bitacora_append.py`
  - `--ia roo`
  - `--pregunta <texto_usuario>`
  - `--respuesta <respuesta_final>`
