# Docs Gate (Plantilla)

Propósito: validar documentación antes del cierre final y de las lecciones
finales.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Modo:
- Fecha:
- Motor activo: `Claude`
- Motor auditor: `Codex`

## Checklist documental

- [ ] README actualizado de forma incremental (si aplica)
- [ ] No se reescribió README completo
- [ ] No se inventaron rutas/comandos/features
- [ ] Rutas documentadas existen en el repo
- [ ] Comandos documentados son ejecutables
- [ ] Riesgos y limitaciones quedaron explícitos
- [ ] Cumple `dev/policies/documentation_rules.md`

## Checklist de gobernanza

- [ ] `closeout.md` existe
- [ ] Fases de iniciativa trazadas en `closeout.md`
- [ ] Gates de plan e implementación en verde
- [ ] Si la iniciativa tocó comportamiento observable del producto, existe `real_validation.md`
- [ ] Si existe `real_validation.md`, su decisión final es `APTA_PARA_F6` o `NO_APLICA`
- [ ] Si la iniciativa tocó una capability transversal, existe `capability_closure.md`
- [ ] Si existe `capability_closure.md`, `scripts/dev/check_capability_closure.py` fue ejecutado sin errores
- [ ] Si hubo excepción formal, existe `exception_record.md` y cumple `dev/policies/exception_rules.md`
- [ ] Si hubo excepción formal, `scripts/dev/check_exception_record.py` fue ejecutado sin errores
- [ ] Decisiones relevantes registradas en `dev/logs/decisions.md`
- [ ] Scripts tocados cumplen `dev/policies/scripts_rules.md` (si aplica)
- [ ] Naming compliance ejecutado (`scripts/dev/check_naming_compliance.py`) sin errores
- [ ] State0 compliance ejecutado (`scripts/dev/check_state0.py`) sin errores
- [ ] `closeout.md` declara si quedó o no convivencia legacy/canónico y si hubo excepciones abiertas

## Checklist de lecciones

- [ ] `lessons_learned.md` existe
- [ ] Lecciones técnicas y de proceso documentadas
- [ ] Propuestas de cambio a gobernanza registradas
- [ ] Cada propuesta tiene decisión (`ADOPTAR`, `NO_ADOPTAR`, `REVISAR_MAS_ADELANTE`)

## Condición de cierre

- [ ] Iniciativa puede declararse cerrada

## Regla de bloqueo

Si este gate no está en verde:
- no se puede declarar cierre formal.
