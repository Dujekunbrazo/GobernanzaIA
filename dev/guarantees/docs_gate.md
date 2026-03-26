# Docs Gate (Plantilla)

Propósito: validar documentación antes del cierre final (`F8`) y de las
lecciones finales (`F9`).

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Modo:
- motor_activo:
- motor_auditor:
- Fecha:

## Checklist documental (`F8`)

- [ ] README actualizado de forma incremental (si aplica)
- [ ] No se reescribió README completo
- [ ] No se inventaron rutas/comandos/features
- [ ] Rutas documentadas existen en el repo
- [ ] Comandos documentados son ejecutables
- [ ] Riesgos y limitaciones quedaron explícitos
- [ ] Cumple `dev/policies/documentation_rules.md`

## Checklist de gobernanza (`F8`)

- [ ] `closeout.md` existe
- [ ] Fases F1-F9 trazadas en `closeout.md`
- [ ] Gates Ask/Plan/Implementation en verde
- [ ] Si la initiative tocó una capability transversal, existe `capability_closure.md`
- [ ] Si existe `capability_closure.md`, `scripts/dev/check_capability_closure.py` fue ejecutado sin errores
- [ ] Si hubo excepción formal, existe `exception_record.md` y cumple `dev/policies/exception_rules.md`
- [ ] Si hubo excepción formal, `scripts/dev/check_exception_record.py` fue ejecutado sin errores
- [ ] Decisiones relevantes registradas en `dev/logs/decisions.md`
- [ ] Scripts tocados cumplen `dev/policies/scripts_rules.md` (si aplica)
- [ ] Evidencia de bitácora IA disponible en `dev/records/bitacora/` (si hubo trabajo conversacional)
- [ ] En cierre `F8/F9`, la bitácora final quedó incluida en el mismo bloque de commit/push de cierre (sin commit residual)
- [ ] Naming compliance ejecutado (`scripts/dev/check_naming_compliance.py`) sin errores
- [ ] State0 compliance ejecutado (`scripts/dev/check_state0.py`) sin errores
- [ ] `closeout.md` declara si quedó o no convivencia legacy/canónico y si hubo excepciones abiertas
- [ ] `closeout.md` usa flags binarios para `legacy_retired`, `parallel_paths_remaining`, `wiring_complete`, `exception_open` y `capability_closure_verified`

## Checklist de lecciones (`F9`)

- [ ] `lessons_learned.md` existe
- [ ] Lecciones técnicas y de proceso documentadas
- [ ] Propuestas de cambio a gobernanza registradas
- [ ] Cada propuesta tiene decisión (`ADOPTAR`, `NO_ADOPTAR`, `REVISAR_MAS_ADELANTE`)

## Condición de cierre

- [ ] Iniciativa puede declararse cerrada

## Regla de bloqueo

Si este gate no está en verde:
- no se puede declarar cierre formal.
