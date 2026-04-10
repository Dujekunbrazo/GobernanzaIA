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

Reglas adicionales:

- dentro de `lookup puntual`, el orden preferente es:
  - `search_symbols`
  - `get_symbol`
  - `get_file_outline` o `get_symbols`
  - `search_text` solo como apoyo textual
- `search_text(path_pattern=...)` no se considera happy path por defecto mientras
  el wrapper local o el CLI real no lo soporten de forma estable en el repo

## 2) Estados de backend

Backends admitidos:

- `none`
- `local`
- `voyage`

Los estados que la gobernanza debe distinguir son:

1. `default backend`
   - backend que el baseline instala o recomienda por defecto
2. `validated backend`
   - backend realmente validado en el repo y la sesión actual
3. `observed best backend`
   - backend que ha mostrado mejor calidad empírica observada en un repo
     concreto

Reglas canónicas:

- el backend por defecto del baseline puede seguir siendo `local`
- `voyage` es opcional, no obligatorio y nunca puede asumirse por defecto
- `voyage` puede figurar como `observed best backend` en un repo concreto si
  la evidencia comparativa lo demuestra
- el `observed best backend` no sustituye automáticamente al `default backend`
  del canon
- el routing operativo debe atender siempre al `validated backend` del repo
  actual, no al backend por defecto abstracto

## 3) Regla de verdad

- que la tool `semantic_search` esté expuesta no demuestra por sí sola que la
  capacidad semántica esté operativa
- la capacidad semántica solo cuenta como `DISPONIBLE` si existe backend
  configurado y validación funcional real
- si no hay embeddings válidos, `symdex_code` debe declararse como disponible
  solo para lookup puntual
- si `semantic_search` está expuesto pero devuelve fallback, warning o ausencia
  de embeddings, el estado correcto es `DEGRADADO`, no `DISPONIBLE`
- si `search_text(path_pattern=...)` falla en el wrapper o en el CLI real, ese
  patrón de uso debe declararse como `DEGRADADO`

## 4) Routing operativo

- preguntas de símbolo, archivo o bloque exacto:
  - `symdex_code` lookup puntual
- preguntas conceptuales locales sobre código vivo:
  - `semantic_search` solo si la capacidad semántica está validada
- si no hay backend semántico validado:
  - degradar a `search_symbols` + `get_symbol`
  - usar `search_text` solo como apoyo textual cuando aporte señal real
  - no simular búsqueda por concepto
- si `search_text(path_pattern=...)` falla:
  - degradar a lookup puntual y lectura exacta del archivo ya localizado
  - no insistir con patrones amplios como si fueran el camino canónico

## 5) Validación mínima

Una instalación semántica de `SymDex` es aceptable cuando:

- el perfil del repo distingue `default backend`, `validated backend` y,
  cuando exista evidencia, `observed best backend`
- el perfil del repo declara backend activo
- existe indexado local funcional
- una búsqueda `semantic_search` devuelve respuesta operativa o deja trazado
  claro de ausencia de embeddings
- el autochequeo humano distingue:
  - tool expuesta
  - backend semántico real
  - capacidad realmente usable de `search_text(path_pattern=...)` si se pretende
    tratarla como operativa

## 6) Prohibiciones

- prohibido declarar `symdex_semantic_search: DISPONIBLE` si la búsqueda
  semántica no está realmente operativa
- prohibido comparar `SymDex` contra `codebase-memory-mcp` usando
  `semantic_search` sin embeddings
- prohibido asumir `voyage` como backend canónico o gratuito
- prohibido promover un `observed best backend` a verdad canónica sin decisión
  explícita sobre el baseline
- prohibido tratar `search_text(path_pattern=...)` como estable por defecto si
  el comportamiento observado del wrapper o del CLI real no lo confirma

## 7) Referencias

- `dev/policies/context_stack_policy.md`
- `dev/policies/context_routing_policy.md`
- `dev/policies/repo_capabilities_policy.md`
