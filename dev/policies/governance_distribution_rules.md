# Governance Distribution Rules (Hard)

Estas reglas definen como se distribuye y sincroniza la gobernanza reusable
entre el repositorio canónico de baseline y los repositorios consumidores.

## 1) Repositorio canónico

- `GobernanzaIA` es la fuente canónica del baseline reusable.
- Los repositorios de producto consumen ese baseline.
- `dev/records/` nunca se exporta como histórico entre repositorios.
- el inventario canónico del baseline vive en:
  - `dev/policies/governance_baseline_manifest.md`
- la expansión segura a consumidores se rige por:
  - `dev/policies/consumer_rollout_policy.md`

## 2) Separación de responsabilidades

- Cambios reusables de gobernanza deben nacer en `GobernanzaIA` o promoverse a
  `GobernanzaIA` antes de consolidarse como baseline.
- Cambios de runtime o de dominio de un producto se quedan en el repo
  consumidor.
- Adaptadores de producto (`.roo/`, `.claude/`, `CLAUDE.md`) son opcionales y
  no sustituyen la fuente normativa canónica.

## 3) Mecanismo de sincronización

- El baseline se instala o reimporta usando
  `scripts/migration/bootstrap_governance.py` ejecutado desde el repo fuente
  hacia el repo destino.
- Toda instalación o reimportación debe dejar metadata de baseline en
  `dev/governance_baseline.json`.
- La instalación baseline debe dejar también la plantilla canónica de perfil en
  `dev/templates/governance/repo_governance_profile.md`.
- El repo consumidor no debe actualizar manualmente a mano los archivos del
  baseline si el mismo cambio puede entrar por bootstrap desde la fuente
  canónica.

## 3.1) Baseline y overlay local

- el baseline reusable vive en `GobernanzaIA`
- el repo consumidor recibe ese baseline y mantiene una overlay local mínima
- la overlay local incluye, como mínimo:
  - `dev/repo_governance_profile.md`
- el perfil local no redefine el canon; declara capacidades reales del repo
- el runtime local del orquestador queda fuera del baseline exportable
- la overlay local debe preservarse en actualizaciones del baseline

## 4) Capabilities operativas opcionales

- `symdex` se instala como dependencia externa desde su fuente oficial; no se
  exporta como snapshot desde el repo consumidor.
- `governance_search` se distribuye como tooling local reusable del baseline.
- `codebase-memory-mcp` se integrará como capacidad estructural canónica; su
  disponibilidad real debe declararse en `dev/repo_governance_profile.md`.
- El wiring MCP de `Roo` debe resolverse mediante merge canónico de
  `.roo/mcp.json`; queda prohibido sobrescribir servidores hermanos por pack.

## 5) Flujo recomendado

1. Trabajar la mejora reusable en `GobernanzaIA`.
2. Validar y versionar el baseline en `GobernanzaIA`.
3. Reimportar en el repo consumidor con `bootstrap_governance.py --force`.
4. Revisar el diff del consumidor y validar sus gates locales.

## 6) Excepciones

- Si una mejora reusable nace primero en un repo consumidor por urgencia real,
  debe registrarse en la iniciativa y promocionarse después a `GobernanzaIA`.
- No se puede cerrar esa capability como baseline consolidado mientras siga
  existiendo solo en el consumidor.
