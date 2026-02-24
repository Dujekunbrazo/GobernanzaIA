# Docs Gate (Plantilla)

Propósito: validar documentación antes del cierre final.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Fecha:
- Responsable:

## Checklist documental

- [ ] README actualizado de forma incremental
- [ ] No se reescribió README completo
- [ ] No se inventaron rutas/comandos/features
- [ ] Rutas documentadas existen en el repo
- [ ] Comandos documentados son ejecutables
- [ ] Riesgos y limitaciones quedaron explícitos
- [ ] Cumple `dev/policies/documentation_rules.md`

## Checklist de gobernanza

- [ ] `closeout.md` existe
- [ ] Fases F1-F9 trazadas en `closeout.md`
- [ ] Gates Ask/Plan/Implementation en verde
- [ ] Decisiones relevantes registradas en `dev/logs/decisions.md`
- [ ] Scripts tocados cumplen `dev/policies/scripts_rules.md` (si aplica)
- [ ] Evidencia de bitácora IA disponible en `dev/records/bitacora/` (si hubo trabajo conversacional)
- [ ] Naming compliance ejecutado (`scripts/dev/check_naming_compliance.py`) sin errores
- [ ] State0 compliance ejecutado (`scripts/dev/check_state0.py`) sin errores

## Condición de cierre

- [ ] Iniciativa puede declararse cerrada

## Regla de bloqueo

Si este gate no está en verde:
- no se puede declarar cierre formal.
