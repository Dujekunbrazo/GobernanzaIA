# Governance Context MCP

Tooling reusable para exponer `governance_search`, `governance_scope` y el
adaptador canónico `symdex_code` sobre el repositorio actual.

## Componentes

- `governance_retrieval_server.mjs`: MCP server para retrieval semántico de
  gobernanza.
- `symdex_code_server.mjs`: adaptador MCP ligero para `SymDex` con tools
  canónicas (`semantic_search`, `get_symbol`, etc.).
- `shared.mjs`: utilidades compartidas de indexado, scoring y embeddings.
- `smoke_governance_mcp.mjs`: smoke mínimo del servidor de gobernanza.

## Uso

Instalar dependencias:

```bash
npm ci
```

Smoke mínimo:

```bash
node smoke_governance_mcp.mjs
```

Servidor de gobernanza:

```bash
node governance_retrieval_server.mjs
```

Servidor de SymDex:

```bash
node symdex_code_server.mjs
```

## Output esperado

- `smoke_governance_mcp.mjs` devuelve JSON con las tools expuestas y el scope
  de gobernanza.
- Los índices y cachés se guardan en `state/context_retrieval/`.

## Errores comunes

- Falta `OPENAI_API_KEY` o `GOOGLE_API_KEY` / `GEMINI_API_KEY`: el servidor de
  gobernanza no puede generar embeddings.
- Dependencias no instaladas: `node` no puede importar el SDK MCP.
- Cambios en corpus: el índice se reconstruye en la siguiente ejecución.
