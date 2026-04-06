# Consumer Rollout Policy (Hard)

Propósito:
- definir cómo expandir el baseline canónico a Kiminion y a futuros repos sin
  tocar código de producto ni destruir overlay local.

## 1) Instalación en repo nuevo

- usar `scripts/migration/bootstrap_governance.py`
- instalar baseline canónico y scaffolding vacío
- completar después la overlay local mínima en:
  - `dev/repo_governance_profile.md`

## 2) Actualización de repo existente

- reimportar desde `GobernanzaIA`
- revisar el diff antes de validar
- preservar la overlay local del consumidor
- no usar borrados abiertos ni limpieza manual agresiva

## 3) Overlay local protegida

La overlay local mínima del consumidor incluye:

- `dev/repo_governance_profile.md`

Esa overlay:

- no debe sobrescribirse por defecto en reimportaciones
- no forma parte del histórico canónico del baseline
- debe seguir reflejando la realidad del repo consumidor

## 4) Regla de seguridad

- cualquier actualización del baseline debe tocar solo archivos exportables del
  manifiesto canónico
- si una operación afecta rutas ambiguas o no exportables, debe pararse

## 5) Criterio de aceptabilidad

La expansión a consumidores es aceptable cuando:

- un repo nuevo puede instalarse limpio
- un repo existente puede actualizarse sin tocar producto
- la overlay local se preserva
- el diff final queda revisable y reversible
