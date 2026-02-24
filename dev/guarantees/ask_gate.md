# Ask Gate (Plantilla)

Propósito: validar Ask antes de permitir planificación.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Fecha:
- Responsable:

## Checklist F1-F2

- [ ] Existe `ask.md` para la iniciativa
- [ ] `ask.md` tiene estado `PROPUESTO` o `VALIDADO`
- [ ] Incluye objetivo, alcance preliminar y restricciones
- [ ] Incluye evidencia verificable del repo
- [ ] Incluye supuestos explícitos
- [ ] Incluye preguntas bloqueantes/no bloqueantes
- [ ] Incluye opciones y trade-offs
- [ ] El usuario validó Ask (F2)

## Checklist F2.5 (Auditoría Codex de Ask)

- [ ] Existe `ask_audit.md`
- [ ] El resultado de auditoría es `PASS` o `PASS_WITH_OBSERVATIONS`
- [ ] Si hubo observaciones, quedaron registradas
- [ ] No hay bloqueantes abiertos

## Condición para F3

- [ ] Ask puede congelarse (`ask.md` en `CONGELADO`)

## Regla de bloqueo

Si este gate no está en verde:
- Architect no puede iniciar F4.
