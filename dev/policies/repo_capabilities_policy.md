# Repo Capabilities Policy (Hard)

Proposito:
- definir como declara un repo consumidor sus capacidades reales sin reescribir
  el canon

## 1) Perfil canonico por repo

Cada repo consumidor debe declarar un unico perfil local de capacidades.

Ese perfil:

- describe tooling realmente disponible
- describe señales runtime realmente observables
- no redefine reglas normativas
- no sustituye `AGENTS.md` ni `dev/workflow.md`

## 2) Responsabilidades del perfil

El perfil declara, como minimo:

- capacidades de retrieval de gobernanza
- capacidades de lectura de codigo vivo
- estado real de busqueda semantica de `SymDex`
- capacidades de memoria estructural
- superficies disponibles para validacion real
- señales runtime observables
- restricciones locales relevantes para `F8`

## 3) Ubicacion

El baseline distribuye una plantilla canonica.

El repo consumidor mantiene su instancia local en:

- `dev/repo_governance_profile.md`

La plantilla fuente vive en:

- `dev/templates/governance/repo_governance_profile.md`

## 4) Regla de verdad

- el perfil describe disponibilidad real, no deseos ni roadmap
- si una capacidad no esta instalada o validada, debe declararse como ausente
- el motor debe degradar segun el perfil, no asumir capacidades
- el routing de cada consulta se rige por
  `dev/policies/context_routing_policy.md`

Estados aceptables de declaracion:

- `DISPONIBLE`
  - capacidad instalada, accesible y funcional en uso real
- `DEGRADADO`
  - capacidad expuesta pero con limites materiales observados
- `NO_DISPONIBLE`
  - capacidad ausente, no expuesta o no funcional

## 5) Capacidades minimas a declarar

- `governance_search`
- `symdex_code`
- `symdex_semantic_search`
- `symdex_embedding_backend`
- `symdex_lookup_mode`
- `symdex_search_text_path_pattern`
- `codebase-memory-mcp`
- `codebase_memory_project_resolution`
- `codebase_memory_query_graph`
- validacion real observable
- `trace on`
- terminal o logs legibles
- el detalle de uso de la capacidad estructural se rige por
  `dev/policies/structural_memory_policy.md`

## 6) Prohibiciones

- prohibido declarar una capacidad como disponible si no esta operativa
- prohibido declarar `symdex_semantic_search: DISPONIBLE` si solo existe la
  tool expuesta pero no embeddings validos
- prohibido declarar `search_text(path_pattern=...)` como `DISPONIBLE` si el
  wrapper local o el CLI real muestran fallos reproducibles
- prohibido declarar `codebase-memory-mcp: DISPONIBLE` como si eso implicara
  automaticamente proyecto efectivo, esquema valido y `query_graph` estable
- prohibido usar el perfil para introducir workflow alternativo
- prohibido duplicar el perfil en varias rutas locales
- prohibido esconder diferencias materiales entre repos bajo metadata informal

## 7) Criterio de aceptabilidad

Un perfil de repo es aceptable cuando:

- esta en la ruta canonica
- refleja el estado real del entorno
- permite al motor decidir routing y fallback
- distingue entre capacidad expuesta y capacidad realmente usable
- no redefine el canon ni crea rutas paralelas
