# Implementation Gate (Plantilla)

Propósito: validar ejecución real antes del cierre documental.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Modo:
- motor_activo:
- motor_auditor:
- Fecha:

## Prerequisitos

- [ ] `plan.md` existe y está en `CONGELADO`
- [ ] `plan_audit.md` existe con resultado `PASS`

## Checklist F6 (Implementación)

- [ ] Existe `execution.md`
- [ ] `execution.md` lista commits ejecutados
- [ ] Cada commit corresponde a un cambio lógico
- [ ] No hay cambios fuera del plan congelado
- [ ] Se registraron comandos de validación y resultados
- [ ] Si la implementación toca una capability transversal, usa la abstracción canónica y el owner arquitectónico definidos en el plan
- [ ] La capability modificada quedó conectada en el wiring canónico definido en el plan
- [ ] No introduce branching por `tool`/`path`/`channel`/`filter` para resolver la capability
- [ ] No deja coverage vertical aislada, wiring parcial ni integraciones huérfanas para la misma capability
- [ ] No mantiene paths paralelos ni fallback legacy conviviendo con el camino canónico
- [ ] `planner`, `generator`, `router` y `execute` consumen el mecanismo común; no absorbieron lógica específica por herramienta fuera del owner arquitectónico
- [ ] Existe evidencia end-to-end de activación real y evidencia estructural de no-branching y no-convivencia cuando aplique

## Checklist F7 (Post-auditoría / Debug)

- [ ] Existe `post_audit.md`
- [ ] Resultado `PASS`
- [ ] No hay hallazgos abiertos
- [ ] Riesgos remanentes documentados
- [ ] La post-auditoría verificó ausencia de branching oportunista, wiring parcial, paths paralelos y fallback legacy en las capabilities transversales tocadas

## Condición para F8

- [ ] Implementación apta para cierre documental

## Regla de bloqueo

Si este gate no está en verde:
- no se puede avanzar a `F8`.
- una implementación que resuelva la capability con `ifs`, bypass, hacks path-specific, wiring incompleto o caminos paralelos no es apta para `F8` aunque el caso puntual funcione.
