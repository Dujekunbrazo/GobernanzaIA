# Governance Baseline Manifest (Hard)

Proposito:
- declarar que forma parte del baseline canonico exportable y que queda fuera
  como overlay local o runtime operativo

## 1) Entra en el baseline exportable

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/`
- `dev/policies/`
- `dev/prompts/`
- `dev/templates/initiative/`
- `dev/templates/governance/`
- `dev/ai/`
- scripts canonicos de `dev`, `ops` y `migration`
- documentacion reusable de gobernanza
- scaffolding vacio de `dev/records/` para iniciativas, bitacora y reviews

## 2) No entra en el baseline exportable

- `dev/records/` como historico real
- iniciativas concretas
- bitacoras reales
- caches, logs, sesiones o outputs generados
- configuraciones locales efimeras del operador
- artefactos de una capa ejecutiva externa al repo consumidor

## 3) Overlay local minima del repo consumidor

La overlay minima del repo consumidor incluye:

- `dev/repo_governance_profile.md`

Puede incluir ademas adaptadores locales de producto, siempre que no
sustituyan el canon.

## 4) Regla de instalacion y actualizacion

- el baseline se instala desde `GobernanzaIA`
- la actualizacion de consumidores debe tocar solo archivos del baseline
  exportable
- la overlay local no se trata como baseline

## 5) Criterio de aceptabilidad

El baseline esta bien definido cuando:

- el bootstrap puede copiarlo sin ambiguedad
- el consumidor sabe que puede personalizar localmente
- no se exportan records reales ni runtime efimero
