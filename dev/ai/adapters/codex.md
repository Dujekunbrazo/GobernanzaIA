# Adapter Codex

- `AGENTS.md` es el contrato compartido con Claude.
- Este adapter no debe redefinir workflow, policies ni routing canonico.
- Al inicio de sesion o tras recarga, comprobar:
  - `governance_search`
  - `semantic_search` via `symdex_code`
  - `get_symbol` via `symdex_code`
  - `codebase-memory-mcp` (`get_architecture`, `search_graph`, `query_graph`)
- Si alguna capacidad falta o falla, declararlo antes de continuar.
- Routing canonico por responsabilidad:
  - gobernanza -> `governance_search` y luego lectura canonica puntual
  - codigo vivo -> `symdex_code`
  - wiring, arquitectura estructural, impacto, blast radius y legacy ->
    `codebase-memory-mcp`
- En codigo vivo:
  - usar `semantic_search` solo si la capacidad semantica esta validada
  - si no lo esta, degradar a `search_symbols` o `search_text`
  - despues usar `get_symbol`, `get_file_outline` o `get_symbols`
- En analisis estructural:
  - usar `codebase-memory-mcp` para localizar relaciones y alcance
  - volver a `symdex_code` para leer fino el codigo exacto localizado
- Prohibido usar `Glob`, `Grep`, `find`, `rg`, `Read` o `Bash` como via
  principal cuando exista el MCP correcto.
- Herramientas internas solo como fallback si el MCP falla o no esta
  disponible, o para lectura final puntual del archivo ya localizado.
- En respuestas tecnicas, declarar:
  - herramienta usada
  - responsabilidad cubierta
  - fuente canonica localizada
  - fallback, si lo hubo
