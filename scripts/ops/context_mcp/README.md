# Governance Context MCP

Tooling reusable para exponer `governance_search` y `governance_scope` sobre la
gobernanza canónica del repositorio actual.

## Componentes

- `governance_retrieval_server.mjs`: MCP server para retrieval semántico de
  gobernanza.
- `shared.mjs`: utilidades compartidas de indexado, scoring y embeddings.
- `smoke_governance_mcp.mjs`: smoke mínimo del servidor de gobernanza.

`SymDex` no se distribuye desde esta carpeta en el baseline reusable. Se
instala como dependencia externa mediante el pack `symdex`.

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

## Output esperado

- `smoke_governance_mcp.mjs` devuelve JSON con las tools expuestas y el scope
  de gobernanza.
- Los índices y cachés se guardan en `state/context_retrieval/`.

## Errores comunes

- Falta `OPENAI_API_KEY` o `GOOGLE_API_KEY` / `GEMINI_API_KEY`: el servidor de
  gobernanza no puede generar embeddings.
- Dependencias no instaladas: `node` no puede importar el SDK MCP.
- Cambios en corpus: el índice se reconstruye en la siguiente ejecución.
