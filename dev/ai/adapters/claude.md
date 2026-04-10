# Adapter Claude

- `AGENTS.md` es el contrato compartido con Codex.
- Este adapter no debe redefinir workflow, policies ni routing canonico.
- Claude es el motor activo del repo.
- Al inicio de sesion o tras recarga, comprobar:
  - `governance_search`
  - `semantic_search` via `symdex_code`
  - `get_symbol` via `symdex_code`
  - `codebase-memory-mcp` (`list_projects`, `get_architecture`, `search_graph`, `trace_path`, `query_graph`)
- Si alguna capacidad falta o falla, declararlo antes de continuar.

## Routing canonico por responsabilidad

- gobernanza -> `governance_search` y luego lectura canónica puntual
- codigo vivo -> `symdex_code`
- wiring, arquitectura estructural, impacto, blast radius y legacy ->
  `codebase-memory-mcp`

## Uso canonico por fase

- `M0`:
  - Claude no sustituye el aterrizaje tecnico con Codex
  - Claude recibe despues un `input de planificacion` ya compactado
- `plan.md`:
  - usar `Claude Opus`, `medium`
- implementacion:
  - usar `Claude Sonnet`, `medium`
- validacion real, cierre y lecciones:
  - usar `Claude Sonnet`, `low` por defecto
- weekly factual:
  - usar `Claude Sonnet`
- weekly estrategico:
  - usar `Claude Opus`

## Reglas de codigo vivo

- usar `semantic_search` solo si la capacidad semantica esta validada
- si no lo esta, degradar a `search_symbols` y `get_symbol`
- usar `search_text` solo como apoyo textual, no como sustituto del lookup
  puntual
- despues usar `get_symbol`, `get_file_outline` o `get_symbols`

## Reglas de analisis estructural

- verificar primero el proyecto efectivo con `list_projects`
- usar `search_graph` para discovery y `trace_path` para relaciones reales
- reservar `query_graph` para ultima milla y solo con query acotada
- volver a `symdex_code` para leer fino el codigo exacto localizado

## Prohibiciones

- prohibido usar `Glob`, `Grep`, `find`, `rg`, `Read` o `Bash` como via
  principal cuando exista el MCP correcto
- prohibido usar `Opus` para exploracion factual o lectura bruta por rutina
- prohibido producir planes de iniciativa desde el weekly
- herramientas internas solo como fallback si el MCP falla o no esta
  disponible, o para lectura final puntual del archivo ya localizado

## En respuestas tecnicas

- declarar herramienta usada
- declarar responsabilidad cubierta
- declarar fuente canonica localizada
- declarar proyecto estructural usado, si aplica
- declarar estado de `semantic_search`: `DISPONIBLE`, `DEGRADADO` o `NO_DISPONIBLE`
- declarar fallback, si lo hubo
- declarar limitacion metodologica observada, si la hubo
