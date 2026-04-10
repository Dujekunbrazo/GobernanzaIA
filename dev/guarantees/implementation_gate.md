# Implementation Gate (Plantilla)

Propósito: validar ejecución real antes del cierre documental.

## Datos de la iniciativa

- Initiative ID:
- Ruta: `dev/records/initiatives/<initiative_id>/`
- Modo:
- Fecha:
- Motor activo: `Claude`
- Motor auditor: `Codex`

## Prerequisitos

- [ ] `plan.md` existe y está en `CONGELADO`
- [ ] `plan_audit.md` existe con resultado `PASS`

## Checklist de implementación

- [ ] Existe `execution.md`
- [ ] `execution.md` lista commits o tramos ejecutados
- [ ] Cada commit o tramo corresponde a un cambio lógico
- [ ] No hay cambios fuera del plan congelado
- [ ] Se registraron comandos de validación y resultados
- [ ] Si la implementación toca una capability transversal, usa la abstracción canónica y el owner arquitectónico definidos en el plan
- [ ] La capability modificada quedó conectada en el wiring canónico definido en el plan
- [ ] No introduce branching por `tool`/`path`/`channel`/`filter` para resolver la capability
- [ ] No deja coverage vertical aislada, wiring parcial ni integraciones huérfanas para la misma capability
- [ ] No mantiene paths paralelos ni fallback legacy conviviendo con el camino canónico
- [ ] Existe evidencia end-to-end de activación real y evidencia estructural de no-branching y no-convivencia cuando aplique

## Checklist de post-auditoría

- [ ] Existe `post_audit.md`
- [ ] Resultado `PASS`
- [ ] No hay hallazgos abiertos
- [ ] Riesgos remanentes documentados
- [ ] La post-auditoría verificó ausencia de branching oportunista, wiring parcial, paths paralelos y fallback legacy en las capabilities transversales tocadas

## Checklist de validación real

- [ ] Si la iniciativa toca comportamiento observable del producto, existe `real_validation.md`
- [ ] Si la iniciativa no toca comportamiento observable, la validación real quedó trazada como `NO_APLICA`
- [ ] `real_validation.md` registra script o matriz completa de pruebas reales
- [ ] Cada caso registra esperado, observado, resultado y evidencia
- [ ] El barrido real se completó antes de decidir fixes generales
- [ ] `real_validation.md` declara `Decisión final: APTA_PARA_F6`, `REABRIR_F3` o `NO_APLICA`
- [ ] Si la decisión fue `REABRIR_F3`, no se avanzó a cierre

## Condición para cierre documental

- [ ] Implementación apta para cierre documental

## Regla de bloqueo

Si este gate no está en verde:
- no se puede avanzar a cierre.
- una implementación que resuelva la capability con `ifs`, bypass, hacks
  path-specific, wiring incompleto o caminos paralelos no es apta para cierre
  aunque el caso puntual funcione.
