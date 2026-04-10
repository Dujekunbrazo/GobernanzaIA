# Governance Distribution Rules (Hard)

Estas reglas definen como se distribuye y sincroniza la gobernanza reusable
entre el repositorio canonico de baseline y los repositorios consumidores.

## 1) Repositorio canonico

- `GobernanzaIA` es la fuente canonica del baseline reusable
- los repositorios de producto consumen ese baseline
- `dev/records/` nunca se exporta como historico entre repositorios
- el inventario canonico del baseline vive en:
  - `dev/policies/governance_baseline_manifest.md`
- la expansion segura a consumidores se rige por:
  - `dev/policies/consumer_rollout_policy.md`

## 2) Separacion de responsabilidades

- cambios reusables de gobernanza deben nacer en `GobernanzaIA` o promoverse a
  `GobernanzaIA` antes de consolidarse como baseline
- cambios de runtime o de dominio de un producto se quedan en el repo
  consumidor
- adaptadores de producto (`.claude/`, `CLAUDE.md` y equivalentes) son
  opcionales y no sustituyen la fuente normativa canonica
- el baseline exporta el workflow activo; queda prohibido convivir con un
  workflow viejo y otro nuevo en paralelo

## 3) Mecanismo de sincronizacion

- el baseline se instala o reimporta usando
  `scripts/migration/bootstrap_governance.py` ejecutado desde el repo fuente
  hacia el repo destino
- toda instalacion o reimportacion debe dejar metadata de baseline en
  `dev/governance_baseline.json`
- la instalacion baseline debe dejar tambien la plantilla canonica de perfil en
  `dev/templates/governance/repo_governance_profile.md`

## 4) Baseline y overlay local

- el baseline reusable vive en `GobernanzaIA`
- el repo consumidor recibe ese baseline y mantiene una overlay local minima
- la overlay local incluye, como minimo:
  - `dev/repo_governance_profile.md`
- el perfil local no redefine el canon; declara capacidades reales del repo
- la overlay local debe preservarse en actualizaciones del baseline
- la memoria operativa viva del consumidor se mantiene local y no se sobrescribe
  por reimportacion:
  - `dev/records/reviews/initiative_backlog.md`
  - `dev/records/reviews/architecture_findings_register.md`
  - `dev/records/reviews/initiative_architecture_backlog.md`

## 5) Capabilities operativas opcionales

- `symdex` se instala como dependencia externa desde su fuente oficial; no se
  exporta como snapshot desde el repo consumidor
- `governance_search` se distribuye como tooling local reusable del baseline
- `codebase-memory-mcp` es la capacidad estructural canonica cuando este
  disponible; su estado real debe declararse en
  `dev/repo_governance_profile.md`
- el wiring MCP de superficies nativas debe resolverse mediante merge canonico;
  queda prohibido sobrescribir servidores hermanos por pack

## 6) Distribucion de responsabilidades documentales

- el baseline reusable debe exportar un workflow `plan-first`
- el baseline reusable no debe exportar artefactos intermedios del workflow
  anterior como parte del canon activo
- el primer artefacto formal de iniciativa del consumidor es `plan.md`
- el `input de planificacion` es transitorio y no forma parte del baseline
- el weekly del baseline descubre y prioriza; no genera planes de iniciativa
- el backlog del consumidor conserva ideas y candidatos vivos entre weeklies e
  iniciativas

## 7) Flujo recomendado

1. trabajar la mejora reusable en `GobernanzaIA`
2. validar y versionar el baseline en `GobernanzaIA`
3. reimportar en el repo consumidor con `bootstrap_governance.py --force`
4. revisar el diff del consumidor y validar sus gates locales
5. confirmar que no queda ningun workflow paralelo activo tras la reimportacion
