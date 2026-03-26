# Arquitectura de Contexto y Recuperación

## Propósito

Definir la separación operativa entre:

- gobernanza de proceso
- navegación de código vivo del producto

## Principio central

La gobernanza responde a `como procedemos`.
El índice de código responde a `sobre que trabajamos`.

No deben mezclarse en el mismo sistema de contexto.

## Capa estática

Siempre presente:

- reglas duras
- resumen del workflow
- precedencia técnica
- instrucciones de recuperación

Objetivo de tamaño:
- `~3K-5K` tokens

## Gobernanza recuperable

Corpus canónico:

- `dev/policies/`
- `dev/guarantees/`
- `dev/prompts/`
- `dev/templates/initiative/`
- `dev/ai/adapters/`
- `dev/workflow.md`
- `doc/architecture/`

Exclusiones duras:

- `dev/records/`
- `dev/records/legacy/`
- `.roo/`
- bitácoras
- histórico
- artefactos generados

Recuperación recomendada:

1. filtrar por `fase`
2. filtrar por `tipo de documento`
3. filtrar por `motor` si aplica
4. aplicar ranking semántico dentro del subconjunto
5. si hay ambigüedad, cargar el documento canónico completo

Implementación operativa local:

- servidor MCP: `scripts/ops/context_mcp/governance_retrieval_server.mjs`
- herramienta MCP: `governance_search`
- índice persistente: `state/context_retrieval/governance_index.json`
- caché de embeddings: `state/context_retrieval/governance_embedding_cache.json`
- embeddings: `OpenAI` si `OPENAI_API_KEY` está disponible; fallback a
  `Google Gemini Embeddings` si solo existe `GOOGLE_API_KEY` o
  `GEMINI_API_KEY`

## SymDex

`SymDex` se reserva solo para código vivo del producto.

Incluir:

- `core/`
- `integrations/MCP-Microsoft-Office/src/`
- `scripts/`
- `tests/`
- `manifests/`

Excluir:

- `node_modules`
- `.venv`
- `__pycache__`
- `.git`
- caches
- logs
- `state`
- `sessions`
- `content`
- gobernanza textual

Implementación operativa local:

- servidor MCP: `scripts/ops/context_mcp/symdex_code_server.mjs`
- herramientas MCP:
  - `symdex_search_code`
  - `symdex_read_code`
- índice persistente: `state/context_retrieval/symdex_code_index.json`

## Routing de consultas

- si la consulta pide workflow, gates, prompts, templates, adapters o
  arquitectura, consultar `governance_search`
- si la consulta pide runtime, símbolos, tests o navegación de código,
  consultar `symdex_search_code`
- si hay ambigüedad, cargar el documento/fichero canónico correspondiente

## Motores

La arquitectura es neutral por motor.

- el usuario designa `motor_activo`
- el usuario designa `motor_auditor` en `F2`
- `Codex`, `Claude`, `Gemini` y `Roo` pueden actuar bajo el mismo contrato

`Roo` no define un workflow paralelo.
Sus modos nativos son capa de producto, no fuente de verdad.
