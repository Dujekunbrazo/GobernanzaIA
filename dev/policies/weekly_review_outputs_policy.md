# Policy: Weekly Review Outputs

## Objetivo

Definir salidas semanales comparables, versionables y aptas para automatizacion.

## Artefactos canónicos

- `weekly_review.md`
- `weekly_review_delta.md`
- `weekly_review_audit.md` cuando se use auditoria lateral
- `candidate_initiatives.md`
- actualizacion de `initiative_backlog.md`
- actualizacion de `architecture_findings_register.md`

## Reglas

- `weekly_review.md` es el informe principal
- `weekly_review_delta.md` captura tendencia y cambios respecto a la ultima
  revision valida
- `weekly_review_audit.md` solo aplica cuando exista auditoria lateral
- los artefactos semanales no sustituyen el registro persistente de hallazgos
- ningun artefacto semanal puede sustituir `plan.md`
- `candidate_initiatives.md` no puede contener plan por commits ni write set
  operativo detallado

## Criterio de aceptabilidad

Los outputs semanales son correctos cuando:

- pueden compararse semana a semana
- diferencian baseline inicial de delta semanal
- no dependen de memoria conversacional
- dejan clara la separacion entre hallazgo, candidata y plan de iniciativa
