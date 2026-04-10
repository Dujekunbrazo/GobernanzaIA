# Context Routing Policy (Hard)

Proposito:
- definir que capa canonica responde cada tipo de consulta
- fijar la degradacion aceptable cuando una capa no esta disponible
- canonizar el routing eficiente por carril, tooling y modelo

## 1) Regla general

- cada consulta debe resolverse por una unica capa primaria
- el fallback solo se usa si la capa primaria no esta disponible o no puede
  responder con evidencia suficiente
- queda prohibido combinar dos capas primarias como si fueran equivalentes
- el coste operativo se optimiza eligiendo la capa con mayor senal y menor
  expansion de contexto

## 2) Routing por tipo de consulta

### Tabla canonica de preguntas

| Tipo de pregunta | Capa primaria | Capa secundaria |
| --- | --- | --- |
| `¿que hace este simbolo?` | `symdex_code` | ninguna |
| `¿donde esta este simbolo?` | `symdex_code` | `codebase-memory-mcp` |
| `¿quien llama a X?` | `codebase-memory-mcp` | ninguna |
| `¿que impacta cambiar X?` | `codebase-memory-mcp` | ninguna |
| `¿como esta organizado este archivo?` | `symdex_code` | ninguna |
| `¿cuales son los hubs?` | `codebase-memory-mcp` | ninguna |
| `¿que tests cubren esto?` | `codebase-memory-mcp` | ninguna |
| `¿hay duplicacion?` | `codebase-memory-mcp` | ninguna |
| `¿que endpoint HTTP usa esto?` | lectura canonica de `manifests` o `openapi.yaml` | `symdex_code` o `codebase-memory-mcp` como apoyo |
| `busco algo que haga X` | `symdex_code semantic_search` si backend semantico validado | `codebase-memory-mcp` |

### Gobernanza normativa

Preguntas tipicas:

- reglas
- workflow
- gates
- templates
- prompts
- adapters
- backlogs y registros canonicos

Capa primaria:

- `governance_search`

Fallback:

- lectura canonica directa del documento exacto ya localizado

Escalera operativa:

- `governance_search` con query breve y concreta
- aplicar `document_type`, `phase` o `motor` cuando reduzca el espacio
- leer solo el documento canonico exacto ya localizado
- no cargar corpus amplio de gobernanza salvo ambiguedad material

### Codigo vivo local

Preguntas tipicas:

- simbolo
- archivo
- bloque concreto
- implementacion local
- busqueda conceptual local cuando exista backend semantico validado

Capa primaria:

- `symdex_code`

Fallback:

- busqueda textual controlada y lectura puntual del archivo

Reglas adicionales:

- `semantic_search` solo puede actuar como busqueda conceptual primaria si el
  backend semantico de `SymDex` esta validado localmente
- si no lo esta, `symdex_code` queda limitado a lookup puntual
- `symdex_code` es primario para:
  - localizar simbolos
  - leer codigo exacto
  - obtener outline de archivo
  - responder que hace un simbolo
- `search_symbols` es la via primaria cuando existe nombre aproximado de
  simbolo
- `get_symbol` es la via primaria cuando ya existe simbolo o archivo candidato
- `get_file_outline` y `get_symbols` son la via primaria para anatomia de
  archivo
- `search_text` es una via textual auxiliar y no debe ser el primer recurso si
  existe lookup puntual suficiente
- `search_text` con `path_pattern` no debe tratarse como happy path por defecto;
  solo procede con patrones estrechos y cuando el wrapper local lo soporte de
  forma estable

### Memoria estructural persistente

Preguntas tipicas:

- wiring global
- blast radius
- impact analysis
- dead code
- legacy
- call paths
- arquitectura estructural
- tests conectados
- duplicacion estructural

Capa primaria:

- `codebase-memory-mcp`

Fallback:

- `symdex_code` mas lectura canonica del repo

Reglas adicionales:

- `codebase-memory-mcp` es primario para:
  - call paths
  - hubs
  - impacto de cambio
  - analisis global de relaciones
  - legacy estructural
  - cobertura estructural de tests
  - duplicacion por similitud
- `codebase-memory-mcp` no sustituye:
  - lectura exacta del codigo
  - docstrings y detalle fino de simbolo
  - lectura canonica de `manifests` y `openapi.yaml` cuando el grafo no
    conecta rutas HTTP
- antes de un analisis estructural serio debe verificarse el proyecto efectivo
  con `list_projects`
- si va a usarse `query_graph`, antes debe verificarse el esquema real con
  `get_graph_schema`
- el orden primario aceptable es:
  - `search_graph` para discovery estructural inicial
  - `trace_path` para callers, callees, data flow e impacto real
  - `query_graph` solo para ultima milla, con `LIMIT`, labels explicitos y
    propiedades verificadas en el esquema
- `search_graph` en modo BM25 no constituye por si solo evidencia estructural
  suficiente para concluir wiring, dead code o legacy
- queda prohibido arrancar un analisis estructural general con `query_graph`
  global o con Cypher no acotado

### Evidencia runtime real

Preguntas tipicas:

- comportamiento observable
- trazas reales
- logs reales
- efectos visibles en producto
- validacion real

Capa primaria:

- evidencia runtime real

Fallback:

- ninguno cosmetico
- si no hay evidencia observable suficiente, el estado correcto es `BLOQUEADO`

## 3) Routing por carril

### Carril iniciativa

- `M0`:
  - gobernanza -> `governance_search`
  - codigo vivo -> `symdex_code`
  - wiring/impacto -> `codebase-memory-mcp`
  - salida esperada: conversacion aterrizada + `input de planificacion`
- `plan.md`:
  - se produce desde retrieval dirigido y contexto estructurado
  - queda prohibido construirlo a base de lectura masiva o chat sin anclaje
- auditoria de plan:
  - prioridad a `plan.md`, codigo vivo y memoria estructural
- implementacion:
  - prioridad a codigo vivo y memoria estructural
- post-auditoria:
  - prioridad a `plan.md`, `execution.md`, diffs reales, codigo vivo y memoria
    estructural
- validacion real:
  - prioridad a evidencia runtime real

### Carril weekly review

- briefing factual:
  - usa `governance_search`, `symdex_code` y `codebase-memory-mcp`
  - no propone solucion estrategica ni plan operativo
- review estrategica:
  - consume el briefing factual
  - no relee codigo bruto salvo ausencia material de evidencia
- actualizacion de findings y backlog:
  - usa weekly review, registros persistentes y delta previo cuando exista
- baseline weekly:
  - mismo routing, pero con alcance repo completo y profundidad alta

## 4) Routing por modelo

- `Claude Sonnet`
  - briefing factual del weekly
  - implementacion
  - validacion real
  - cierre y lecciones
- `Claude Opus`
  - `plan.md`
  - review estrategica del weekly
- `Codex`
  - auditoria formal
  - aterrizaje tecnico en `M0`

Reglas:

- `Opus` no se usa para leer codigo bruto por rutina
- `Sonnet` no sustituye la sintesis estrategica cuando el trabajo requiere
  planificacion compleja
- `Codex` no sustituye a `Claude` como motor activo de produccion

## 5) Prohibiciones

- prohibido usar el chat como fuente primaria de continuidad
- prohibido resolver wiring estructural con busqueda textual como via principal
  cuando exista `codebase-memory-mcp`
- prohibido usar `symdex_code` para sustituir evidencia runtime
- prohibido tratar `semantic_search` como si siempre fuera semantica validada
- prohibido usar `search_text(path_pattern=...)` como primer recurso por
  defecto
- prohibido usar `query_graph` como primer paso de discovery estructural
- prohibido usar `Glob`, `Grep`, `find`, `rg`, `Read` o `Bash` como via
  principal si existe el MCP correcto
- prohibido usar `Opus` para tareas factuales que puede resolver `Sonnet`
- prohibido convertir el weekly en via paralela de planificacion de iniciativa

## 6) Criterio de aceptabilidad

El routing es aceptable cuando:

- cada consulta tiene capa primaria y fallback
- no existen solapes primarios
- la degradacion queda trazada y no inventa evidencia
- el routing evita contexto bruto innecesario cuando existe retrieval dirigido
- el modelo usado es proporcional al tipo de trabajo
