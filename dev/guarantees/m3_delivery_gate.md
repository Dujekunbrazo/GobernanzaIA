# M3 Delivery Gate (Plantilla)

Propósito: validar que un cambio `M3` sigue siendo acotado, trazable y
estructuralmente completo antes del cierre.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Modo:
- motor_activo:
- motor_auditor:
- Fecha:

## Prerequisitos

- [ ] Existe `ask.md`
- [ ] `ask.md` define alcance y no-alcance acotados
- [ ] Existe `execution.md`

## Checklist de implementación `M3`

- [ ] El cambio sigue siendo acotado y trazable
- [ ] No hay refactor encubierto ni expansión material de alcance
- [ ] `execution.md` registra comandos de validación y resultados
- [ ] Si el cambio toca una capability transversal, identifica owner
      arquitectónico y abstracción canónica
- [ ] Si existe `capability_closure.md`, `scripts/dev/check_capability_closure.py` fue ejecutado sin errores
- [ ] Si aplica, la capability quedó conectada en su wiring canónico
- [ ] No existe branching por `tool`/`path`/`channel`/`filter` para resolver
      la capability
- [ ] No existe coverage vertical aislada, wiring parcial ni integraciones
      huérfanas
- [ ] No conviven camino legacy y camino canónico para la misma capability
- [ ] Si hubo excepción formal, existe `exception_record.md` y cumple
      `dev/policies/exception_rules.md`
- [ ] Si hubo excepción formal, `scripts/dev/check_exception_record.py` fue
      ejecutado sin errores
- [ ] Existe evidencia estructural de wiring real, no-convivencia y
      no-branching cuando aplique

## Checklist de cierre `M3`

- [ ] Existe `closeout.md`
- [ ] Existe `lessons_learned.md`
- [ ] `closeout.md` usa flags binarios de cierre estructural
- [ ] Naming compliance ejecutado (`scripts/dev/check_naming_compliance.py`)
      sin errores
- [ ] State0 compliance ejecutado (`scripts/dev/check_state0.py`) sin errores

## Regla de bloqueo

Si este gate no está en verde:
- no se puede cerrar la iniciativa `M3`.
- si aparece necesidad de wiring adicional, múltiples commits lógicos o
  auditoría formal de plan, corresponde transición a `M4`.
