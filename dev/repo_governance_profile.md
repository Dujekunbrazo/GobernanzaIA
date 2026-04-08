# REPO GOVERNANCE PROFILE

## Identidad

- Repo: GobernanzaIA
- Proposito: baseline canonico de gobernanza multi-IA reusable por repos consumidores
- Superficie principal: artefactos de gobernanza, policies, templates, prompts y scripts de migracion

## Capacidades de gobernanza

- governance_search: DISPONIBLE
- Corpus de gobernanza local valido: SI

## Capacidades de codigo vivo

- symdex_code: NO_APLICA
- symdex_semantic_search: NO_APLICA
- Motivo: este repo no contiene codigo de producto; solo gobernanza y scripts auxiliares

## Capacidades de memoria estructural

- codebase-memory-mcp: NO_APLICA
- Motivo: no hay codigo de producto que indexar estructuralmente

## Validacion real

- F8 observable: NO_APLICA
- Motivo: no hay comportamiento observable de producto; las iniciativas de este repo son de gobernanza pura

## Restricciones locales

- Este repo no tiene runtime de producto
- Los scripts en `scripts/` son herramientas auxiliares de gobernanza, no producto
- Las mejoras de gobernanza se validan por consistencia documental, no por runtime

## Fallbacks

- Si falta governance_search:
  - usar lectura canonica del baseline y busqueda textual puntual solo como fallback
- Si falta symdex_code:
  - NO_APLICA para este repo
- Si falta codebase-memory-mcp:
  - NO_APLICA para este repo
- Si falta validacion real:
  - NO_APLICA para este repo

## Notas

- Este perfil describe las capacidades reales de GobernanzaIA como repo canonico de baseline.
- GobernanzaIA no tiene codigo de producto; su superficie es exclusivamente gobernanza.
- No redefine el workflow canonico ni la gobernanza normativa.
