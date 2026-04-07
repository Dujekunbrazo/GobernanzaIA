# REPO GOVERNANCE PROFILE

## Identidad

- Repo: <nombre_repo>
- Propósito: <dominio_del_repo>
- Superficie principal: <producto_cli_backend_ui_etc>

## Capacidades de gobernanza

- governance_search: DISPONIBLE | NO_DISPONIBLE
- Corpus de gobernanza local válido: SI | NO

## Capacidades de código vivo

- symdex_code: DISPONIBLE | NO_DISPONIBLE
- symdex_semantic_search: DISPONIBLE | NO_DISPONIBLE
- symdex_default_backend: none | local | voyage
- symdex_embedding_backend: none | local | voyage
- Estado de validación semántica: VALIDADO | PENDIENTE | NO_APLICA
- symdex_observed_quality: BAJA | MEDIA | ALTA
- symdex_observed_best_backend: none | local | voyage | NO_EVALUADO
- Rutas indexables principales:
  - <ruta_1>
  - <ruta_2>

## Capacidades de memoria estructural

- codebase-memory-mcp: DISPONIBLE | NO_DISPONIBLE
- Estado de validación local: VALIDADO | PENDIENTE | NO_APLICA
- codebase_memory_known_limits:
  - <limite_1>
- Cobertura esperada:
  - wiring global: SI | NO
  - blast radius: SI | NO
  - dead code / legacy: SI | NO
  - arquitectura estructural: SI | NO

## Validación real

- F8 observable: SI | NO
- Superficies reales de validación:
  - <superficie_1>
  - <superficie_2>
- trace on o equivalente: SI | NO
- terminal/logs observables: SI | NO

## Restricciones locales

- Restricciones de entorno:
  - <restriccion_1>
- Riesgos operativos conocidos:
  - <riesgo_1>

## Fallbacks

- Si falta governance_search:
  - <fallback>
- Si falta symdex_code:
  - <fallback>
- Si symdex_code existe pero falta backend semántico validado:
  - usar lookup puntual (`search_symbols`, `search_text`, `get_symbol`,
    `get_file_outline`) sin simular búsqueda conceptual
- Si falta codebase-memory-mcp:
  - <fallback>
- Si falta validación real:
  - <fallback o BLOQUEADO>

## Notas

- Este perfil describe capacidades reales del repo.
- Los campos observacionales no redefinen el canon; solo capturan calidad y
  límites reales del repo.
- `symdex_default_backend` expresa el backend recomendado por el baseline.
- `symdex_embedding_backend` expresa el backend realmente validado en el repo.
- No redefine el workflow canónico ni la gobernanza normativa.
