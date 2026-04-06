# Repo Capabilities Policy (Hard)

Propósito:
- definir cómo declara un repo consumidor sus capacidades reales sin reescribir
  el canon.

## 1) Perfil canónico por repo

Cada repo consumidor debe declarar un único perfil local de capacidades.

Ese perfil:

- describe tooling realmente disponible
- describe señales runtime realmente observables
- no redefine reglas normativas
- no sustituye `AGENTS.md` ni `dev/workflow.md`

## 2) Responsabilidades del perfil

El perfil declara, como mínimo:

- capacidades de retrieval de gobernanza
- capacidades de lectura de código vivo
- capacidades de memoria estructural
- superficies disponibles para validación real
- señales runtime observables
- restricciones locales relevantes para `F8`

## 3) Ubicación

El baseline distribuye una plantilla canónica.

El repo consumidor mantiene su instancia local en:

- `dev/repo_governance_profile.md`

La plantilla fuente vive en:

- `dev/templates/governance/repo_governance_profile.md`

## 4) Regla de verdad

- el perfil describe disponibilidad real, no deseos ni roadmap
- si una capacidad no está instalada o validada, debe declararse como ausente
- el orquestador debe degradar según el perfil, no asumir capacidades
- el routing de cada consulta se rige por
  `dev/policies/context_routing_policy.md`

## 5) Capacidades mínimas a declarar

- `governance_search`
- `symdex_code`
- `codebase-memory-mcp`
- validación real observable
- `trace on`
- terminal o logs legibles

## 6) Prohibiciones

- prohibido declarar una capacidad como disponible si no está operativa
- prohibido usar el perfil para introducir workflow alternativo
- prohibido duplicar el perfil en varias rutas locales
- prohibido esconder diferencias materiales entre repos bajo metadata informal

## 7) Criterio de aceptabilidad

Un perfil de repo es aceptable cuando:

- está en la ruta canónica
- refleja el estado real del entorno
- permite al orquestador decidir routing y fallback
- no redefine el canon ni crea rutas paralelas
