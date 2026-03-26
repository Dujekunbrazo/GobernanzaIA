# Ask Gate (Plantilla)

Propósito: validar Ask antes de permitir planificación.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Modo:
- motor_activo:
- motor_auditor:
- Fecha:

## Checklist F1-F2

- [ ] Existe `ask.md` para la iniciativa
- [ ] `ask.md` tiene estado `PROPUESTO` o `VALIDADO`
- [ ] `ask.md` incluye cabecera mínima (`Modo`, `motor_activo`, rama, `baseline_mit`)
- [ ] Incluye objetivo, alcance preliminar y restricciones
- [ ] Incluye evidencia verificable del repo
- [ ] Incluye supuestos explícitos
- [ ] Incluye preguntas bloqueantes/no bloqueantes
- [ ] Incluye opciones y trade-offs
- [ ] El usuario validó Ask (`F2`)

## Checklist F3 (Auditoría + congelado de Ask)

- [ ] Existe `ask_audit.md`
- [ ] El resultado de auditoría es `PASS`
- [ ] `ask.md` quedó en estado `CONGELADO`
- [ ] No hay hallazgos abiertos

## Condición para F4

- [ ] Ask apto para planificación (`ask.md` en `CONGELADO`)

## Regla de bloqueo

Si este gate no está en verde:
- el `motor_activo` no puede iniciar `F4`.
