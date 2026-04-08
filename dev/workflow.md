# Dev Workflow - Motor Directo

Este documento define la referencia operativa corta para trabajar en este repo
sin logica ejecutiva externa.

## Fuente de verdad

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/*.md`
- `dev/ai/adapters/*.md`
- `dev/policies/*.md`

Si una capa difiere, se corrige en el mismo cambio.

## Como debe cargarse

- `AGENTS.md` es la capa estatica siempre presente.
- `dev/workflow.md` se carga bajo demanda como referencia compacta.
- Las policies y guarantees se localizan primero con `governance_search`.

## Modos

- `M0 CONVERSACION`
- `M1 ANALISIS`
- `M2 DEBUG`
- `M3 IMPLEMENTACION_MENOR`
- `M4 INICIATIVA_COMPLETA`

Reglas:

- `M0`, `M1` y `M2` no autorizan cambios de codigo
- `M3` exige alcance acotado y trazable
- `M4` exige el pipeline `F1-F10`

## M3 - Secuencia minima

Artefactos minimos:

- `ask.md`
- `execution.md`
- `closeout.md`
- `lessons_learned.md`

Secuencia:

1. definir alcance, no alcance, evidencia y criterio de aceptacion
2. implementar el cambio acotado
3. registrar validacion en `execution.md`
4. verificar `dev/guarantees/m3_delivery_gate.md`
5. cerrar en `closeout.md` y `lessons_learned.md`

## M4 - Referencia compacta

Artefactos sustantivos habituales:

- `ask.md`
- `ask_audit.md`
- `plan.md`
- `plan_audit.md`
- `execution.md`
- `post_audit.md`
- `real_validation.md` cuando aplique
- `closeout.md`
- `lessons_learned.md`

Pipeline:

1. `F1` Ask propuesto
2. `F2` Validacion de ask por usuario
3. `F3` Auditoria y congelado de ask
4. `F4` Plan propuesto
5. `F5` Auditoria y congelado de plan
6. `F6` Implementacion
7. `F7` Post-auditoria / debug
8. `F8` Validacion real guiada
9. `F9` Docs + cierre
10. `F10` Lecciones finales

## Reglas de auditoria formal

Aplica a `F3`, `F5` y `F7`.

Reglas:

- solo el `motor_auditor` emite auditoria formal
- la decision formal solo puede ser `PASS` o `FAIL`
- no se permite `PASS` con hallazgos pendientes
- si el resultado es `FAIL`, no se avanza

## F8 - Validacion real guiada

`F8` aplica cuando cambia comportamiento observable del producto.

Reglas:

- no es una auditoria formal nueva
- debe registrar expected, observed y evidencia viva
- debe usar:
  - chat del producto
  - `trace on`
  - terminal o logs
  - resultados visibles en runtime real
- si aparece un fallo material, corresponde reabrir `F6`
- si se reabre `F6`, deben repetirse `F7` y `F8`

## Routing de contexto

- gobernanza -> `governance_search`
- codigo vivo -> `symdex_code`
- estructura e impacto -> `codebase-memory-mcp`
- validacion observable -> evidencia runtime real

## Carga minima recomendada

- `AGENTS.md`
- `dev/workflow.md`
- un gate relevante
- una policy de soporte relevante
- `dev/repo_governance_profile.md` solo si hace falta declarar degradacion

No cargar mas contexto del necesario si un retrieval dirigido resuelve la
tarea con trazabilidad suficiente.
