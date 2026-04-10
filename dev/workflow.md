# Dev Workflow - Claude + Codex

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
- `M0` puede terminar en un `input de planificacion` transitorio para
  `Claude`.
- Ese input no es artefacto formal de iniciativa y no se persiste en
  `dev/records/initiatives/`.

## Modos

- `M0 CONVERSACION`
- `M1 ANALISIS`
- `M2 DEBUG`
- `M3 IMPLEMENTACION_MENOR`
- `M4 INICIATIVA_COMPLETA`

Reglas:

- `M0`, `M1` y `M2` no autorizan cambios de codigo
- `M3` exige alcance acotado y trazable
- `M4` usa `plan.md` como artefacto primario de planificacion

## Carriles de trabajo

### Carril iniciativa

Usado para cambios concretos que van a ejecucion.

Artefactos sustantivos habituales:

- `plan.md`
- `plan_audit.md`
- `execution.md`
- `post_audit.md`
- `real_validation.md` cuando aplique
- `closeout.md`
- `lessons_learned.md`

Secuencia:

1. trabajar la idea en `M0` con lectura de codigo y aterrizaje tecnico
2. convertir la conversacion en `input de planificacion` para `Claude`
3. generar `plan.md`
4. auditar y congelar el plan
5. implementar
6. post-auditar
7. ejecutar validacion real cuando aplique
8. cerrar y extraer lecciones

Reglas:

- el primer artefacto formal es `plan.md`
- `plan.md` es el unico artefacto de planificacion de iniciativa
- `execution.md` solo registra delta de ejecucion y evidencia
- `post_audit.md` solo registra hallazgos, veredicto y remediacion
- `closeout.md` y `lessons_learned.md` no deben recrear el plan
- `closeout.md` debe declarar explicitamente si el cierre deja backlog vivo o
  si `SIN_CAMBIOS`

### Carril weekly review

Usado para revision estrategica recurrente del repo.

Salidas esperadas:

- `weekly_briefing.md`
- `weekly_review.md`
- `weekly_review_delta.md` cuando exista weekly anterior
- `candidate_initiatives.md`
- actualizacion de findings y backlog

Secuencia:

1. briefing factual
2. review estrategica
3. actualizacion de findings y backlog
4. promocion opcional de candidatos a iniciativa

Reglas:

- el weekly no genera `plan.md`
- el weekly no propone commits de implementacion
- el weekly descubre, prioriza y propone candidatos
- el trabajo real de iniciativa se abre despues en `M0`
- el primer weekly de un repo o de una gobernanza recien implantada se ejecuta
  como `BASELINE`, sin delta previo y con profundidad alta

## Reglas de auditoria formal

Aplica a la auditoria de plan y a la post-auditoria.

Reglas:

- solo `Codex` emite auditoria formal
- la decision formal solo puede ser `PASS` o `FAIL`
- no se permite `PASS` con hallazgos pendientes
- si el resultado es `FAIL`, no se avanza

## Validacion real guiada

La validacion real aplica cuando cambia comportamiento observable del producto.

Reglas:

- no es una auditoria formal nueva
- debe registrar expected, observed y evidencia viva
- debe usar:
  - chat del producto
  - `trace on`
  - terminal o logs
  - resultados visibles en runtime real
- si aparece un fallo material, corresponde reabrir implementacion y repetir
  post-auditoria y validacion real

## Routing de contexto

- gobernanza -> `governance_search`
- codigo vivo -> `symdex_code`
- estructura e impacto -> `codebase-memory-mcp`
- validacion observable -> evidencia runtime real

## Memoria operativa viva

- `dev/records/reviews/architecture_findings_register.md`:
  hallazgos persistentes del weekly
- `dev/records/reviews/initiative_backlog.md`:
  ideas y candidatos surgidos en conversacion, weekly o closeout
- `dev/records/reviews/initiative_architecture_backlog.md`:
  remanentes y follow-ups nacidos en `closeout.md` y `lessons_learned.md`

Reglas:

- no mezclar backlog de ideas con hallazgos persistentes
- no dejar deuda residual solo enterrada en artefactos de iniciativa
- promocionar un candidato del backlog a iniciativa requiere volver a `M0`

## Carga minima recomendada

- `AGENTS.md`
- `dev/workflow.md`
- un gate relevante
- una policy de soporte relevante
- `dev/repo_governance_profile.md` solo si hace falta declarar degradacion

No cargar mas contexto del necesario si un retrieval dirigido resuelve la
tarea con trazabilidad suficiente.
