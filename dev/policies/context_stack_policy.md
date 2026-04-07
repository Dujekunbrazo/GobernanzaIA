# Context Stack Policy (Hard)

Propósito:
- definir la arquitectura canónica de contexto de la gobernanza.
- evitar solapes, rutas paralelas y dependencia de memoria conversacional.

## 1) Capas canónicas

La gobernanza opera sobre cinco capas distintas:

1. `gobernanza normativa`
   - fuente: `AGENTS.md`, `dev/workflow.md`, `dev/guarantees/`,
     `dev/policies/`, `dev/templates/initiative/`, `dev/ai/adapters/`
   - resuelve reglas, gates, precedencia y contratos formales
2. `gobernanza ejecutiva del orquestador`
   - fuente: runtime del orquestador, `phase_ticket`, `resume_packet`,
     receipts, checkpoints y metadata de sesión
   - resuelve fase vigente, límites operativos, continuidad, intentos,
     excepciones y siguiente paso permitido
3. `código vivo local`
   - fuente: `symdex_code`
   - resuelve lectura fina de símbolos, archivos, bloques y wiring local
   - `symdex_code` responde ante todo: "¿qué dice el código?"
   - su búsqueda semántica requiere backend de embeddings validado
4. `memoria estructural persistente`
   - fuente prevista: `codebase-memory-mcp`
   - resuelve call paths, blast radius, legacy, dead code, arquitectura
     estructural y contraste entre wiring esperado y wiring real
   - `codebase-memory-mcp` responde ante todo: "¿qué se conecta con qué?"
5. `evidencia runtime real`
   - fuente: chat del producto, `trace on`, terminal, logs y resultados
     visibles en ejecución real
   - resuelve validación observable y cierre real de comportamiento

## 2) Regla de responsabilidad

- cada pregunta debe rutearse a la capa mínima que la responda de forma
  canónica
- ninguna capa sustituye responsabilidades de otra
- `symdex_code` y `codebase-memory-mcp` son complementarias; ninguna sustituye
  a la otra
- el orquestador coordina capas; no reemplaza artefactos sustantivos de motor
- la memoria del chat no es una capa válida de contexto

## 3) Routing obligatorio

- reglas, fases, gates, templates y prompts:
  - `governance_search` y lectura canónica puntual
- estado de fase, reentrada, checkpoints, excepciones y límites vigentes:
  - runtime del orquestador
- símbolos, archivos y detalle de implementación en código vivo:
  - `symdex_code`
  - `semantic_search` solo cuenta como búsqueda conceptual real si el backend
    semántico está validado
- wiring global, impact analysis, blast radius, legacy y dead code:
  - `codebase-memory-mcp` cuando esté disponible
- validación observable de producto:
  - evidencia runtime real

## 4) Fallbacks permitidos

- si `governance_search` falla, puede leerse el documento canónico por ruta
- si `symdex_code` no está expuesto, puede usarse búsqueda textual controlada
  solo como fallback
- si `symdex_code` está expuesto pero sin backend semántico validado, la
  degradación correcta es lookup puntual; no búsqueda conceptual simulada
- si `codebase-memory-mcp` no está disponible, el análisis estructural degrada
  temporalmente a `symdex_code` más lectura canónica del repo
- si falta evidencia runtime real, el estado correcto es `BLOQUEADO`; no se
  inventa validación

## 5) Prohibiciones

- prohibido usar memoria conversacional como mecanismo principal de continuidad
- prohibido resolver wiring estructural solo con intuición o grep cuando la
  capa estructural canónica esté disponible
- prohibido mezclar runtime operativo del orquestador con artefactos
  sustantivos de la iniciativa
- prohibido dejar dos capas respondiendo la misma responsabilidad como vías
  primarias simultáneas
- referencia operativa:
  - `dev/policies/structural_memory_policy.md`
  - `dev/policies/symdex_semantic_policy.md`

## 6) Criterio de cierre canónico

La arquitectura de contexto se considera cerrada cuando:

- cada capa tiene responsabilidad explícita
- cada consulta tiene routing principal y fallback
- la continuidad operativa no depende del chat
- la validación real usa evidencia observable
- la memoria estructural entra como sustitución de la vía estructural previa y
  no como camino paralelo adicional
- el coste operativo se controla con retrieval dirigido y no con expansión
  indiscriminada de contexto
