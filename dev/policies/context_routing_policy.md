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
- callers o usos locales acotados

Capa primaria:

- `symdex_code`

Fallback:

- búsqueda textual controlada y lectura puntual del archivo

Regla adicional:

- `semantic_search` solo puede actuar como búsqueda conceptual primaria si el
  backend semántico de `SymDex` está validado localmente
- si no lo está, `symdex_code` queda limitado a lookup puntual y el análisis
  conceptual local debe declararse como degradado

### Memoria estructural persistente

Preguntas típicas:

- wiring global
- blast radius
- impact analysis
- dead code
- legacy
- call paths
- arquitectura estructural

Capa primaria:

- `codebase-memory-mcp`

Fallback:

- `symdex_code` más lectura canónica del repo

Referencia:

- `dev/policies/structural_memory_policy.md`
- `dev/policies/symdex_semantic_policy.md`

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
