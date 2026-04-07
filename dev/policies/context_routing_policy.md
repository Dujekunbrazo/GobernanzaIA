# Context Routing Policy (Hard)

Propósito:
- definir qué capa canónica responde cada tipo de consulta y cuál es su
  degradación aceptable.

## 1) Regla general

- cada consulta debe resolverse por una única capa primaria
- el fallback solo se usa si la capa primaria no está disponible o no puede
  responder con evidencia suficiente
- queda prohibido combinar dos capas primarias como si fueran equivalentes

## 2) Routing por tipo de consulta

### Tabla canónica de preguntas

| Tipo de pregunta | Capa primaria | Capa secundaria |
| --- | --- | --- |
| `¿qué hace este símbolo?` | `symdex_code` | ninguna |
| `¿dónde está este símbolo?` | `symdex_code` | `codebase-memory-mcp` |
| `¿quién llama a X?` | `codebase-memory-mcp` | ninguna |
| `¿qué impacta cambiar X?` | `codebase-memory-mcp` | ninguna |
| `¿cómo está organizado este archivo?` | `symdex_code` | ninguna |
| `¿cuáles son los hubs?` | `codebase-memory-mcp` | ninguna |
| `¿qué tests cubren esto?` | `codebase-memory-mcp` | ninguna |
| `¿hay duplicación?` | `codebase-memory-mcp` | ninguna |
| `¿qué endpoint HTTP usa esto?` | lectura canónica de `manifests` / `openapi.yaml` | `symdex_code` o `codebase-memory-mcp` solo como apoyo |
| `busco algo que haga X` | `symdex_code semantic_search` si backend semántico validado | `codebase-memory-mcp` |

Notas:

- si `symdex_code` no tiene backend semántico validado, `busco algo que haga X`
  degrada a lookup puntual más declaración explícita de degradación
- si `codebase-memory-mcp` no conecta rutas HTTP reales, la pregunta sobre
  endpoints debe resolverse por lectura canónica del repo
- queda prohibido responder una misma pregunta con dos capas primarias
  simultáneas

### Gobernanza normativa

Preguntas típicas:

- reglas
- workflow
- gates
- templates
- prompts
- adapters

Capa primaria:

- `governance_search`

Fallback:

- lectura canónica directa del documento exacto

### Estado operativo de iniciativa

Preguntas típicas:

- fase vigente
- siguiente paso permitido
- reentrada
- intentos consumidos
- excepciones vivas
- último checkpoint aceptado

Capa primaria:

- runtime del orquestador

Fallback:

- ninguno informal
- si el runtime no puede reconstruirse con seguridad, el estado correcto es
  `BLOQUEADO`

### Código vivo local

Preguntas típicas:

- símbolo
- archivo
- bloque concreto
- implementación local
- búsqueda conceptual local cuando exista backend semántico validado

Capa primaria:

- `symdex_code`

Fallback:

- búsqueda textual controlada y lectura puntual del archivo

Regla adicional:

- `semantic_search` solo puede actuar como búsqueda conceptual primaria si el
  backend semántico de `SymDex` está validado localmente
- si no lo está, `symdex_code` queda limitado a lookup puntual y el análisis
  conceptual local debe declararse como degradado
- `symdex_code` es primario para:
  - localizar símbolos
  - leer código exacto
  - obtener outline de archivo
  - responder qué hace un símbolo
- `symdex_code` no es primario para:
  - hubs
  - blast radius
  - call paths multiarchivo
  - acoplamiento global
  - cobertura de tests
  - endpoints HTTP del sistema

### Memoria estructural persistente

Preguntas típicas:

- wiring global
- blast radius
- impact analysis
- dead code
- legacy
- call paths
- arquitectura estructural
- tests conectados
- duplicación estructural

Capa primaria:

- `codebase-memory-mcp`

Fallback:

- `symdex_code` más lectura canónica del repo

Regla adicional:

- `codebase-memory-mcp` es primario para:
  - call paths
  - hubs
  - impacto de cambio
  - análisis global de relaciones
  - legacy estructural
  - cobertura estructural de tests
  - duplicación por similitud
- `codebase-memory-mcp` no sustituye:
  - lectura exacta del código
  - docstrings y detalle fino de símbolo
  - lectura canónica de `manifests` y `openapi.yaml` cuando el grafo no
    conecta rutas HTTP

Referencia:

- `dev/policies/structural_memory_policy.md`
- `dev/policies/symdex_semantic_policy.md`
- `dev/policies/structural_analysis_execution_policy.md`

### Evidencia runtime real

Preguntas típicas:

- comportamiento observable
- trazas reales
- logs reales
- efectos visibles en producto
- validación `F8`

Capa primaria:

- evidencia runtime real

Fallback:

- ninguno cosmético
- si no hay evidencia observable suficiente, el estado correcto es `BLOQUEADO`

## 3) Routing por fase

- `F1-F5`:
  - prioridad a gobernanza normativa, runtime del orquestador y código vivo
- `F6`:
  - prioridad a runtime del orquestador, código vivo y, cuando exista,
    memoria estructural
- `F7`:
  - prioridad a plan congelado, código vivo, diffs reales y memoria
    estructural
- `F8`:
  - prioridad a runtime del orquestador y evidencia runtime real

## 4) Prohibiciones

- prohibido usar el chat como fuente primaria de continuidad
- prohibido resolver wiring estructural con búsqueda textual como vía principal
  cuando exista `codebase-memory-mcp`
- prohibido usar `symdex_code` para sustituir evidencia runtime
- prohibido usar runtime del orquestador para sustituir reglas normativas

## 5) Criterio de aceptabilidad

El routing es aceptable cuando:

- cada consulta tiene capa primaria y fallback
- cada fase sabe qué capa priorizar
- no existen solapes primarios
- la degradación queda trazada y no inventa evidencia
- el routing evita contexto bruto innecesario cuando existe retrieval dirigido
