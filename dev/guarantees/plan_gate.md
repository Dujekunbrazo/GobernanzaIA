# Plan Gate (Plantilla)

Propósito: validar plan antes de permitir implementación.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Fecha:
- Responsable:

## Prerequisitos

- [ ] `ask.md` existe y está en `CONGELADO`
- [ ] `ask_audit.md` existe con resultado válido

## Checklist F4-F5

- [ ] Existe `plan.md`
- [ ] `plan.md` está en estado `PROPUESTO`
- [ ] Define alcance y no-alcance claros
- [ ] Lista commits atómicos con validación por commit
- [ ] Incluye estrategia de rollback
- [ ] Incluye Definition of Done
- [ ] Existe `plan_audit.md`
- [ ] `plan_audit.md` tiene resultado `PASS` o `PASS_WITH_OBSERVATIONS`

## Condición para F6

- [ ] Plan puede congelarse (`plan.md` en `CONGELADO`)

## Regla de bloqueo

Si este gate no está en verde:
- Code no puede iniciar F7.
