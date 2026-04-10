# Structural Analysis Execution Policy (Hard)

Propósito:
- regular cómo se ejecuta un análisis estructural serio con
  `codebase-memory-mcp`
- evitar análisis superficiales basados solo en hubs, recuentos o intuición
- obligar a declarar límites metodológicos del grafo cuando existan

## 1) Preconditions

Antes de analizar, debe verificarse:

- `list_projects` ejecutado en la sesion actual
- proyecto correcto identificado en la capa estructural
- indexado persistido y estado listo para consulta
- modo de indexación conocido (`fast`, `moderate` o `full`)
- esquema real conocido si va a usarse `query_graph`

Si alguna de estas precondiciones falla:

- no se analiza
- el estado correcto es `BLOQUEADO`

## 2) Minimum protocol

Un análisis estructural serio debe dejar trazado, como mínimo:

- el proyecto o índice usado
- el modo de indexación usado
- la subtool estructural primaria elegida para arrancar
- al menos `1` traza crítica real
- al menos `1` hub o punto de acoplamiento relevante
- al menos `1` limitación metodológica observada

No es aceptable cerrar un análisis con:

- solo hubs
- solo recuentos de nodos o edges
- solo intuiciones sobre arquitectura
- Cypher pesado sin reducción previa del espacio de búsqueda

Protocolo operativo mínimo:

- `search_graph` para discovery estructural inicial
- `trace_path` para callers, callees, data flow y blast radius real
- `query_graph` solo para última milla cuando las dos herramientas anteriores
  no basten
- si se usa `query_graph`, la query debe llevar:
  - `LIMIT`
  - labels explícitos
  - propiedades verificadas antes con `get_graph_schema` o evidencia previa del
    grafo

## 3) Expected outputs

Cuando aplique, el análisis debe responder con evidencia:

- quién llama a quién
- qué impacta cambiar un símbolo relevante
- qué hubs existen
- qué límites del grafo impiden responder mejor

Cuando haga falta semántica fina del código:

- `codebase-memory-mcp` no sustituye a `symdex_code`
- el análisis debe declarar cuándo necesita lectura exacta de código como capa
  secundaria

## 4) Known graph limits to declare

Cuando aparezcan, deben declararse explícitamente:

- routes HTTP huérfanas o desconectadas del grafo
- edges `TESTS` a nivel clase pero no de método
- `RAISES` subindexado
- ruido excesivo de nodos `Section`
- imposibilidad de reconstruir secuencia exacta de ejecución desde el grafo

## 5) Prohibitions

- prohibido presentar el grafo como si devolviera código fuente
- prohibido presentar una limitación del grafo como si fuera ausencia real de
  wiring
- prohibido cerrar un análisis estructural sin declarar sus límites
- prohibido usar `cross_service` como si fuera apto cuando el boundary
  Python -> HTTP dinámico no esté realmente conectado
- prohibido arrancar por `query_graph` cuando `search_graph` o `trace_path`
  responden la misma pregunta con menor peso
- prohibido lanzar Cypher global sobre `Function`, `Method` o `Class` sin scope
  previo, `LIMIT` y justificación metodológica

## 6) Acceptability criteria

El análisis estructural se considera aceptable cuando:

- parte de un proyecto/indexado verificado
- declara el modo de indexación
- declara la subtool con la que arrancó y por qué
- incluye una traza crítica real
- incluye un hub real
- incluye una limitación metodológica real
- no finge que el grafo resuelve preguntas que no puede responder

## 7) References

- `dev/policies/context_routing_policy.md`
- `dev/policies/structural_memory_policy.md`
- `dev/policies/context_stack_policy.md`
