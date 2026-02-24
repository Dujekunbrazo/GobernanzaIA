# Implementation Gate (Plantilla)

Propósito: validar ejecución real antes de cierre.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Fecha:
- Responsable:

## Prerequisitos

- [ ] `plan.md` existe y está en `CONGELADO`
- [ ] `plan_audit.md` existe con resultado válido

## Checklist F7

- [ ] Existe `execution.md`
- [ ] `execution.md` lista commits ejecutados
- [ ] Cada commit corresponde a un cambio lógico
- [ ] No hay cambios fuera del plan congelado
- [ ] Se registraron comandos de validación y resultados

## Checklist F8 (Post-auditoría Codex)

- [ ] Existe `post_audit.md`
- [ ] Resultado `PASS` o `PASS_WITH_OBSERVATIONS`
- [ ] Hallazgos `HIGH/CRITICAL` resueltos o aceptados explícitamente
- [ ] Riesgos remanentes documentados

## Condición para F9

- [ ] Implementación apta para cierre documental y orquestación final

## Regla de bloqueo

Si este gate no está en verde:
- No se puede cerrar la iniciativa.
