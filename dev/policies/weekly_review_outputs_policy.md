# Policy: Weekly Review Outputs

## Objetivo

Definir salidas semanales comparables, versionables y aptas para automatizacion.

## Artefactos canónicos

- `weekly_review.md`
- `weekly_review_delta.md`
- `weekly_review_audit.md` cuando se use auditoria lateral

## Reglas

- `weekly_review.md` es el informe principal
- `weekly_review_delta.md` captura tendencia y cambios respecto a la ultima
  revision valida
- `weekly_review_audit.md` solo aplica cuando exista auditoria lateral
- los artefactos semanales no sustituyen el registro persistente de hallazgos

## Criterio de aceptabilidad

Los outputs semanales son correctos cuando:

- pueden compararse semana a semana
- diferencian baseline inicial de delta semanal
- no dependen de memoria conversacional
