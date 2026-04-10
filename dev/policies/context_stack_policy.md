# Context Stack Policy (Hard)

Proposito:
- definir la arquitectura canonica de contexto de la gobernanza
- evitar solapes, rutas paralelas y dependencia de memoria conversacional
- dejar claro donde entra el `input de planificacion` sin convertirlo en capa
  canonica

## 1) Capas canonicas

La gobernanza opera sobre cuatro capas distintas:

1. `gobernanza normativa`
   - fuente: `AGENTS.md`, `dev/workflow.md`, `dev/guarantees/`,
     `dev/policies/`, `dev/templates/initiative/`, `dev/ai/adapters/`
   - resuelve reglas, gates, precedencia y contratos formales
2. `codigo vivo local`
   - fuente: `symdex_code`
   - resuelve lectura fina de simbolos, archivos, bloques y wiring local
   - `symdex_code` responde ante todo: "¿que dice el codigo?"
3. `memoria estructural persistente`
   - fuente: `codebase-memory-mcp` cuando este disponible
   - resuelve call paths, blast radius, legacy, dead code, arquitectura
     estructural y contraste entre wiring esperado y wiring real
   - `codebase-memory-mcp` responde ante todo: "¿que se conecta con que?"
4. `evidencia runtime real`
   - fuente: chat del producto, `trace on`, terminal, logs y resultados
     visibles en ejecucion real
   - resuelve validacion observable y cierre real de comportamiento

## 2) Artefacto transitorio permitido

- el `input de planificacion` es un artefacto transitorio de trabajo
- nace al cerrar `M0`
- resume una conversacion tecnica ya anclada al stack canonico
- sirve para alimentar a `Claude` en la generacion de `plan.md`
- no forma parte del expediente formal de iniciativa
- no crea una quinta capa de contexto

## 3) Regla de responsabilidad

- cada pregunta debe rutearse a la capa minima que la responda de forma
  canonica
- ninguna capa sustituye responsabilidades de otra
- `symdex_code` y `codebase-memory-mcp` son complementarias; ninguna sustituye
  a la otra
- la memoria del chat no es una capa valida de contexto
- el `input de planificacion` no sustituye ninguna capa; solo compacta salida
  de trabajo ya aterrizada

## 4) Routing obligatorio

- reglas, fases, gates, templates y prompts:
  - `governance_search` y lectura canonica puntual
  - aplicar query breve y filtros antes de ampliar lectura
- simbolos, archivos y detalle de implementacion en codigo vivo:
  - `symdex_code`
  - `semantic_search` solo cuenta como busqueda conceptual real si el backend
    semantico esta validado
  - el orden preferente es:
    - `search_symbols` -> `get_symbol`
    - `get_file_outline` -> `get_symbols`
    - `semantic_search` solo si procede
- wiring global, impact analysis, blast radius, legacy y dead code:
  - `codebase-memory-mcp` cuando este disponible
  - el orden preferente es:
    - `list_projects`
    - `get_graph_schema` si va a usarse Cypher
    - `search_graph`
    - `trace_path`
    - `query_graph` solo al final y acotado
- validacion observable de producto:
  - evidencia runtime real

## 5) Aplicacion operativa

### En `M0`

- se consulta el stack canonico para entender problema, alcance y riesgos
- se aterriza la idea con apoyo de `Codex`
- solo al final puede emitirse un `input de planificacion`

### En `plan.md`

- `Claude` trabaja sobre el `input de planificacion`
- si el input no basta, debe volver al stack canonico y no inventar

### En weekly review

- la capa factual trabaja sobre el stack canonico
- la capa estrategica consume briefing factual y hallazgos previos
- el weekly no sustituye `M0` ni `plan.md`

## 6) Fallbacks permitidos

- si `governance_search` falla, puede leerse el documento canonico por ruta
- si `symdex_code` no esta expuesto, puede usarse busqueda textual controlada
  solo como fallback
- si `symdex_code` esta expuesto pero sin backend semantico validado, la
  degradacion correcta es lookup puntual
- si `search_text(path_pattern=...)` falla o es inestable, la degradacion
  correcta es lookup puntual mas lectura exacta del archivo ya localizado
- si `codebase-memory-mcp` no esta disponible, el analisis estructural degrada
  temporalmente a `symdex_code` mas lectura canonica del repo
- si `codebase-memory-mcp` esta disponible pero no existe proyecto efectivo,
  esquema util o query acotada, el estado correcto no es improvisar Cypher sino
  degradar o declarar limitacion metodologica
- si falta evidencia runtime real, el estado correcto es `BLOQUEADO`

## 7) Prohibiciones

- prohibido usar memoria conversacional como mecanismo principal de continuidad
- prohibido resolver wiring estructural solo con intuicion o grep cuando la
  capa estructural canonica este disponible
- prohibido dejar dos capas respondiendo la misma responsabilidad como vias
  primarias simultaneas
- prohibido persistir el `input de planificacion` como si fuera artefacto
  formal de iniciativa
- prohibido arrancar por `query_graph` cuando `search_graph` o `trace_path`
  responden la misma pregunta con menos peso

## 8) Criterio de cierre canonico

La arquitectura de contexto se considera cerrada cuando:

- cada capa tiene responsabilidad explicita
- cada consulta tiene routing principal y fallback
- la validacion real usa evidencia observable
- la memoria estructural entra como sustitucion de la via estructural previa y
  no como camino paralelo adicional
- el coste operativo se controla con retrieval dirigido y no con expansion
  indiscriminada de contexto
- el `input de planificacion` se usa como puente y no como nuevo artefacto
  canonico
