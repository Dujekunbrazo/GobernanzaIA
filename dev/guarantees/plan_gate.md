# Plan Gate (Plantilla)

Propósito: validar plan antes de permitir implementación.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Modo:
- motor_activo:
- motor_auditor:
- Fecha:

## Prerequisitos

- [ ] `ask.md` existe y está en `CONGELADO`
- [ ] `ask_audit.md` existe con resultado `PASS`

## Checklist F4-F5

- [ ] Existe `plan.md`
- [ ] `plan.md` está en estado `PROPUESTO` o `CONGELADO`
- [ ] Define alcance y no-alcance claros
- [ ] Lista commits atómicos con validación por commit
- [ ] Incluye estrategia de rollback
- [ ] Incluye Definition of Done
- [ ] Si el plan toca una capability transversal, identifica owner arquitectónico y abstracción canónica
- [ ] Si aplica, el plan define `descriptor`/`policy`/`registry`/punto de extensión y wiring común
- [ ] El plan identifica superficies incluidas y cobertura horizontal requerida
- [ ] El plan no propone coverage vertical aislada por `tool`/`path`/`channel`
- [ ] El plan no mantiene paths paralelos ni fallback legacy para la misma capability
- [ ] El plan no deja integraciones huérfanas previstas
- [ ] El plan no descarga lógica específica por herramienta en `planner`/`generator`/`router`/`execute` cuando corresponde un mecanismo común
- [ ] La validación del plan incluye pruebas estructurales de wiring end-to-end, no-branching y no-convivencia cuando aplique
- [ ] Existe `plan_audit.md`
- [ ] `plan_audit.md` tiene resultado `PASS`
- [ ] `plan.md` quedó en `CONGELADO`

## Condición para F6

- [ ] Plan apto para implementación (`plan.md` en `CONGELADO`)

## Regla de bloqueo

Si este gate no está en verde:
- el `motor_activo` no puede iniciar `F6`.
- un plan que nazca con branching local, wiring parcial, coverage vertical o caminos paralelos para una capability transversal no puede declararse apto para `F6`.
