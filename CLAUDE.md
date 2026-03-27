# Claude Adapter Entry

Antes de ejecutar cualquier tarea en este repo, Claude debe leer en este orden:

1. `AGENTS.md`
2. `dev/workflow.md`
3. `dev/ai/adapters/claude.md`

Si hay contradicción, prevalece `AGENTS.md`.

## Reglas duras de routing MCP

- Si `governance_search` está disponible:
  - cualquier consulta de gobernanza debe empezar por `governance_search`
  - después puede hacerse lectura canónica puntual del archivo localizado
- Si `semantic_search` y `get_symbol` (via symdex_code) están disponibles:
  - cualquier consulta de código debe empezar por `semantic_search`
    (o `search_symbols`/`search_text`)
  - después debe usarse `get_symbol` (o `get_file_outline`/`get_symbols`)
    sobre el bloque relevante
- `Glob`, `Globpattern`, `Grep`, `find`, `rg`, `Read` o `Bash` no cuentan como
  vía principal para gobernanza o código si el MCP correspondiente está
  disponible
- Herramientas internas solo pueden usarse:
  - como fallback si el MCP falla o no está expuesto
  - o para lectura final puntual del archivo ya localizado

## Declaración obligatoria

En respuestas técnicas, Claude debe declarar explícitamente:

- herramienta usada
- fuente canónica usada
- si hubo fallback por ausencia o fallo del MCP

## Autocheck de sesión

Al inicio de sesión o tras recarga, Claude debe comprobar si están disponibles:

- `governance_search`
- `semantic_search` (via symdex_code)
- `get_symbol` (via symdex_code)

Si no están disponibles, debe declararlo antes de continuar.
