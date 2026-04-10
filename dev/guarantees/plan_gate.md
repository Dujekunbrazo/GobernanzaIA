# Plan Gate (Plantilla)

Propósito: validar plan antes de permitir implementación.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Modo:
- Fecha:
- Motor activo: `Claude`
- Motor auditor: `Codex`

## Prerequisitos

- [ ] Existe `plan.md`
- [ ] `plan.md` está en estado `PROPUESTO` o `CONGELADO`

## Checklist de planificación

- [ ] `plan.md` define objetivo claro
- [ ] `plan.md` define alcance y no-alcance claros
- [ ] `plan.md` incorpora evidencia verificable del repo
- [ ] `plan.md` explicita restricciones, supuestos y riesgos
- [ ] `plan.md` lista tramos o commits atómicos con validación por tramo
- [ ] `plan.md` incluye estrategia de rollback
- [ ] `plan.md` incluye Definition of Done
- [ ] Si el plan toca una capability transversal, identifica owner arquitectónico y abstracción canónica
- [ ] Si aplica, el plan define `descriptor`/`policy`/`registry`/punto de extensión y wiring común
- [ ] El plan identifica superficies incluidas y cobertura horizontal requerida
- [ ] El plan no propone coverage vertical aislada por `tool`/`path`/`channel`
- [ ] El plan no mantiene paths paralelos ni fallback legacy para la misma capability
- [ ] El plan no deja integraciones huérfanas previstas
- [ ] La validación del plan incluye pruebas estructurales de wiring end-to-end, no-branching y no-convivencia cuando aplique

## Checklist de auditoría y congelado

- [ ] Existe `plan_audit.md`
- [ ] `plan_audit.md` tiene resultado `PASS`
- [ ] `plan.md` quedó en `CONGELADO`
- [ ] No hay hallazgos abiertos

## Condición para implementación

- [ ] Plan apto para implementación (`plan.md` en `CONGELADO`)

## Regla de bloqueo

Si este gate no está en verde:
- el motor activo no puede iniciar implementación.
- un plan que nazca con branching local, wiring parcial, coverage vertical o
  caminos paralelos para una capability transversal no puede declararse apto
  para implementación.
