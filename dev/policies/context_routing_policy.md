# Context Routing Policy (Hard)

Proposito:
- definir que capa canonica responde cada tipo de consulta
- fijar la degradacion aceptable cuando una capa no esta disponible

## 1) Regla general

- cada consulta debe resolverse por una unica capa primaria
- el fallback solo se usa si la capa primaria no esta disponible o no puede
  responder con evidencia suficiente
- queda prohibido combinar dos capas primarias como si fueran equivalentes

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

Capa primaria:

- `governance_search`

Fallback:

- lectura canonica directa del documento exacto ya localizado

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

### Evidencia runtime real

Preguntas tipicas:

- comportamiento observable
- trazas reales
- logs reales
- efectos visibles en producto
- validacion `F8`

Capa primaria:

- evidencia runtime real

Fallback:

- ninguno cosmetico
- si no hay evidencia observable suficiente, el estado correcto es `BLOQUEADO`

## 3) Routing por fase

- `F1-F5`:
  - prioridad a gobernanza normativa y codigo vivo
- `F6`:
  - prioridad a codigo vivo y memoria estructural
- `F7`:
  - prioridad a plan congelado, diffs reales, codigo vivo y memoria estructural
- `F8`:
  - prioridad a evidencia runtime real y, cuando aporte contraste, memoria
    estructural

## 4) Prohibiciones

- prohibido usar el chat como fuente primaria de continuidad
- prohibido resolver wiring estructural con busqueda textual como via principal
  cuando exista `codebase-memory-mcp`
- prohibido usar `symdex_code` para sustituir evidencia runtime
- prohibido usar `Glob`, `Grep`, `find`, `rg`, `Read` o `Bash` como via
  principal si existe el MCP correcto

## 5) Criterio de aceptabilidad

El routing es aceptable cuando:

- cada consulta tiene capa primaria y fallback
- no existen solapes primarios
- la degradacion queda trazada y no inventa evidencia
- el routing evita contexto bruto innecesario cuando existe retrieval dirigido
