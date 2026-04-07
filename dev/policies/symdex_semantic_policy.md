# SymDex Semantic Policy (Hard)

Propósito:
- regular cuándo `symdex_code` dispone de capacidad semántica real y cómo debe
  declararse, validarse y rutearse.

## 1) Niveles de capacidad

`symdex_code` tiene dos niveles distintos:

1. `lookup puntual`
   - `search_symbols`
   - `search_text`
   - `get_symbol`
   - `get_symbols`
   - `get_file_outline`
2. `búsqueda semántica real`
   - `semantic_search`
   - requiere embeddings operativos y validados

Queda prohibido tratar ambos niveles como equivalentes.

## 2) Backend canónico

Backends admitidos:

- `none`
- `local`
- `voyage`

Regla canónica:

- el backend por defecto del baseline es `local`
- `voyage` es opcional, no obligatorio y nunca puede asumirse por defecto

## 3) Regla de verdad

- que la tool `semantic_search` esté expuesta no demuestra por sí sola que la
  capacidad semántica esté operativa
- la capacidad semántica solo cuenta como `DISPONIBLE` si existe backend
  configurado y validación funcional real
- si no hay embeddings válidos, `symdex_code` debe declararse como disponible
  solo para lookup puntual

## 4) Routing operativo

- preguntas de símbolo, archivo o bloque exacto:
  - `symdex_code` lookup puntual
- preguntas conceptuales locales sobre código vivo:
  - `semantic_search` solo si la capacidad semántica está validada
- si no hay backend semántico validado:
  - degradar a `search_symbols` + `search_text` + `get_symbol`
  - no simular búsqueda por concepto

## 5) Validación mínima

Una instalación semántica de `SymDex` es aceptable cuando:

- el perfil del repo declara backend activo
- existe indexado local funcional
- una búsqueda `semantic_search` devuelve respuesta operativa o deja trazado
  claro de ausencia de embeddings
- el autochequeo humano distingue:
  - tool expuesta
  - backend semántico real

## 6) Prohibiciones

- prohibido declarar `symdex_semantic_search: DISPONIBLE` si la búsqueda
  semántica no está realmente operativa
- prohibido comparar `SymDex` contra `codebase-memory-mcp` usando
  `semantic_search` sin embeddings
- prohibido asumir `voyage` como backend canónico o gratuito

## 7) Referencias

- `dev/policies/context_stack_policy.md`
- `dev/policies/context_routing_policy.md`
- `dev/policies/repo_capabilities_policy.md`
