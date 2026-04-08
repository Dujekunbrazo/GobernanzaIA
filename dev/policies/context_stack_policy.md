# Context Stack Policy (Hard)

Proposito:
- definir la arquitectura canonica de contexto de la gobernanza
- evitar solapes, rutas paralelas y dependencia de memoria conversacional

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

## 2) Regla de responsabilidad

- cada pregunta debe rutearse a la capa minima que la responda de forma
  canonica
- ninguna capa sustituye responsabilidades de otra
- `symdex_code` y `codebase-memory-mcp` son complementarias; ninguna sustituye
  a la otra
- la memoria del chat no es una capa valida de contexto

## 3) Routing obligatorio

- reglas, fases, gates, templates y prompts:
  - `governance_search` y lectura canonica puntual
- simbolos, archivos y detalle de implementacion en codigo vivo:
  - `symdex_code`
  - `semantic_search` solo cuenta como busqueda conceptual real si el backend
    semantico esta validado
- wiring global, impact analysis, blast radius, legacy y dead code:
  - `codebase-memory-mcp` cuando este disponible
- validacion observable de producto:
  - evidencia runtime real

## 4) Fallbacks permitidos

- si `governance_search` falla, puede leerse el documento canonico por ruta
- si `symdex_code` no esta expuesto, puede usarse busqueda textual controlada
  solo como fallback
- si `symdex_code` esta expuesto pero sin backend semantico validado, la
  degradacion correcta es lookup puntual
- si `codebase-memory-mcp` no esta disponible, el analisis estructural degrada
  temporalmente a `symdex_code` mas lectura canonica del repo
- si falta evidencia runtime real, el estado correcto es `BLOQUEADO`

## 5) Prohibiciones

- prohibido usar memoria conversacional como mecanismo principal de continuidad
- prohibido resolver wiring estructural solo con intuicion o grep cuando la
  capa estructural canonica este disponible
- prohibido dejar dos capas respondiendo la misma responsabilidad como vias
  primarias simultaneas

## 6) Criterio de cierre canonico

La arquitectura de contexto se considera cerrada cuando:

- cada capa tiene responsabilidad explicita
- cada consulta tiene routing principal y fallback
- la validacion real usa evidencia observable
- la memoria estructural entra como sustitucion de la via estructural previa y
  no como camino paralelo adicional
- el coste operativo se controla con retrieval dirigido y no con expansion
  indiscriminada de contexto
