# Governance Baseline Manifest (Hard)

Propósito:
- declarar qué forma parte del baseline canónico exportable y qué queda fuera
  como overlay local o runtime operativo.

## 1) Entra en el baseline exportable

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/`
- `dev/policies/`
- `dev/prompts/`
- `dev/templates/initiative/`
- `dev/templates/orchestrator/`
- `dev/templates/governance/`
- `dev/ai/`
- scripts canónicos de `dev`, `ops` y `migration`
- documentación reusable de gobernanza
- scaffolding vacío de `dev/records/` para iniciativas, bitácora y reviews

## 2) No entra en el baseline exportable

- `dev/records/` como histórico real
- iniciativas concretas
- bitácoras reales
- `.orchestrator_local/`
- caches, logs, sesiones o outputs generados
- configuraciones locales efímeras del operador

## 3) Overlay local mínima del repo consumidor

La overlay mínima del repo consumidor incluye:

- `dev/repo_governance_profile.md`

Puede incluir además adaptadores locales de producto, siempre que no
sustituyan el canon.

## 4) Regla de instalación y actualización

- el baseline se instala desde `GobernanzaIA`
- la actualización de consumidores debe tocar solo archivos del baseline
  exportable
- el runtime operativo y la overlay local no se tratan como baseline

## 5) Criterio de aceptabilidad

El baseline está bien definido cuando:

- el bootstrap puede copiarlo sin ambigüedad
- el consumidor sabe qué puede personalizar localmente
- no se exportan records reales ni runtime efímero
