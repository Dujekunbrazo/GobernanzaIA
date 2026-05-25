# Dev Workflow - canon multi-IA

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
- `dev/skills/` es la capa operativa preferente para capacidades migradas.
- Las policies y guarantees se localizan primero con `governance_search`.
- si la consulta de gobernanza esta acotada a una fase, `governance_search`
  debe usar `phase`
- si ademas la duda esta acotada a una familia documental, anadir
  `document_type`
- `M0` puede terminar en un `input de planificacion` transitorio para
  `motor activo`.
- Ese input no es artefacto formal de iniciativa y no se persiste en
  `dev/records/initiatives/`.

## Continuidad durable de motor auditor

Esta regla aplica solo a `motor auditor`.

No aplica a `motor activo` mientras no exista instruccion explicita posterior del
usuario. No crea fase, carril, iniciativa, workflow paralelo ni excepcion al
contrato compartido de `AGENTS.md`.

Objetivo:

- reducir el impacto de fallos de compactacion, contexto largo o recarga de
  sesion en trabajos de `motor auditor`;
- mantener un handoff operativo minimo en archivo durable;
- evitar depender de la memoria conversacional como fuente canonica.

Ruta canonica:

- `dev/records/bitacora/YYYY-MM-DD_codex.md`

Triggers observables:

- fallo explicito de compactacion o recuperacion de contexto;
- transicion de modo o fase;
- bloqueo material;
- decision material de arquitectura, alcance, validacion o Git;
- cierre de turno con cambios o analisis sustantivo;
- trabajo largo: mas de 10 acciones de herramientas o mas de 15-20 minutos
  desde la ultima entrada relevante, lo que ocurra antes.

Contenido minimo recomendado:

- modo/fase;
- objetivo actual;
- decisiones tomadas;
- archivos relevantes;
- evidencia o comandos ya ejecutados;
- bloqueos;
- siguiente paso minimo seguro.

Reglas:

- la bitacora no sustituye `AGENTS.md`, `plan.md`, auditorias formales ni
  artefactos `F1-F7`;
- no guardar transcripciones completas salvo peticion explicita;
- no registrar secretos ni datos marcados por el usuario como no registrables;
- si se usa agente notario, su autoridad se limita a observar, auditar o
  escribir handoff; no decide producto, alcance, arquitectura ni cierre;
- si la continuidad durable entra en conflicto con un artefacto formal, gana
  el artefacto formal segun la precedencia de `AGENTS.md`.

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
2. convertir la conversacion en `input de planificacion` para `motor activo`
3. generar `plan.md`
4. auditar y congelar el plan
5. implementar
6. post-auditar
7. ejecutar validacion real con motor auditor cuando aplique
8. cerrar y extraer lecciones con motor auditor

Reglas:

- el primer artefacto formal es `plan.md`
- `plan.md` es el unico artefacto de planificacion de iniciativa
- `execution.md` solo registra delta de ejecucion y evidencia
- `post_audit.md` solo registra hallazgos, veredicto y remediacion
- `closeout.md` y `lessons_learned.md` no deben recrear el plan
- `F5`, `F6` y `F7` se ejecutan con motor auditor tras `F4 PASS` usando
  `dev/skills/f5_real_validation/`, `dev/skills/f6_closeout/` y
  `dev/skills/f7_lessons/`
- `READY_FOR_CODEX_CLOSEOUT` no es un estado de espera manual: motor auditor debe
  ejecutar `F6`, `F7` y el cierre Git completo en una misma secuencia siempre
  que no exista bloqueo tecnico o instruccion explicita de PR/merge manual
- `F6` debe cerrar tambien la capa operativa de Git:
  commits finales, working tree limpio y estado de rama/remoto trazado
- el cierre Git completo estandar incluye:
  - generar/actualizar `closeout.md`, README si aplica y `lessons_learned.md`
  - actualizar bitacora antes del commit final si aplica
  - crear commit final de cierre
  - hacer push de la rama de iniciativa
  - integrar en `main/master` mediante la estrategia aprobada o merge directo
    si no hay instruccion de PR manual
  - hacer push de `main/master`
  - borrar rama local y remota de iniciativa
  - refrescar `governance_search` si cambio el corpus de gobernanza
  - refrescar `SymDex` y `codebase-memory-mcp` en `main/master` si hubo cambio
    de codigo o wiring estructural
- si la iniciativa ya fue mergeada a `main/master`, `F6` debe dejar resuelto
  tambien el refresco repo-local de indices MCP sobre `main/master`:
  - `scripts/dev/refresh_symdex_index.ps1`
  - `scripts/dev/refresh_codebase_memory_index.ps1`
- si la iniciativa sigue en rama, ese refresco queda
  `PENDIENTE_HASTA_MERGE`; no se reindexa la rama para que los MCP vean el
  delta feature
- si el indice en disco ya esta correcto pero la sesion sigue stale, el cierre
  tecnico acepta reinicio de sesion/MCP como remediacion minima en vez de
  reindexar otra vez
- si tras refresco verificado en disco la sesion MCP viva sigue cacheando la
  rama anterior y no hay proceso reiniciable, se registra como
  `SESION_MCP_RELOAD_REQUIRED` sin reabrir la iniciativa ni repetir refrescos
  en bucle
- si la iniciativa cambia comportamiento observable, superficie operativa,
  flujo de uso, DX o integracion visible, `README.md` debe actualizarse de
  forma incremental antes de declarar cierre
- la politica operativa de first-pass quality del script `ping_pong` en `M4`
  vive en
  `dev/policies/m4_first_pass_quality_policy.md`
- la gobernanza canónica de `BLOQUEADO` y desbloqueo válido en `M4` vive en
  `dev/policies/m4_governed_blocking_unblocking_policy.md`
- el contrato de hallazgo formal para `F2` y `F4` vive en
  `dev/policies/audit_finding_contract_policy.md`
- el contrato estructural base de `plan.md` y `execution.md` vive en
  `dev/policies/m4_artifact_shape_contract_policy.md`
- la capa operativa `Skill-first` para capacidades migradas vive en
  `dev/skills/`
- la policy de Skills vive en `dev/policies/skill_policy.md`
- la policy de validacion proporcional vive en
  `dev/policies/scoped_validation_policy.md`
- `closeout.md` debe declarar explicitamente si el cierre deja backlog vivo o
  si `SIN_CAMBIOS`
- `closeout.md` debe declarar explicitamente:
  - rama de iniciativa
  - commit final de cierre
  - push remoto realizado o pendiente
  - merge a troncal resuelto o pendiente
  - refresco post-merge de `SymDex` y `codebase-memory-mcp` resuelto o pendiente
  - borrado de rama local/remota resuelto o pendiente
  - `README.md` actualizado o `NO_APLICA`
- `closeout.md` solo puede dejar `PENDIENTE_*` en push, merge, borrado de rama
  o refrescos si existe bloqueo real o instruccion explicita del usuario; no se
  usan pendientes como handoff rutinario entre `F6`, `F7` y cierre operativo

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

- solo `motor auditor` emite auditoria formal
- la decision formal solo puede ser `PASS` o `FAIL`
- no se permite `PASS` con hallazgos pendientes
- si el resultado es `FAIL`, no se avanza
- si el `FAIL` contiene solo hallazgos mecanicos del propio expediente y el
  write set permitido queda acotado a artefactos markdown del expediente de la
  iniciativa, el orquestador puede
  ejecutar `SAFE_AUDITOR_AUTOFIX` con `motor auditor` y reauditar en el mismo loop sin
  reabrir `F1` o `F3`
- si el `FAIL` afecta a artefactos de iniciativa o a una reconciliacion
  mecanica entre `plan.md`, DoD, write set, sidecars, `execution.md`,
  `plan_audit.md` o `post_audit.md`, y no cambia objetivo, alcance sustantivo,
  producto, arquitectura, restricciones, criterios PASS/FAIL ni decision
  material, `motor auditor` debe aplicar `SAFE_AUDITOR_AUTOFIX` directamente y
  reauditar en el mismo loop

### Contrato de hallazgo

Todo `FAIL` en `F2` o `F4` debe emitir hallazgos pequenos, tipados y
accionables. Cada hallazgo debe incluir como minimo:

- `Tipo`
- `Artefacto afectado`
- `Seccion exacta`
- `Archivos permitidos`
- `Archivos prohibidos`
- `Cambio minimo requerido`
- `Criterio de cierre`
- `Rerun scope`
- `Reapertura requerida`
- `Evidencia`

Reglas:

- si falta cualquiera de esos campos, la auditoria formal es invalida
- `Cambio minimo requerido` no puede ser una recomendacion vaga
- `Criterio de cierre` debe ser binario y verificable
- `Rerun scope` debe acotar la reejecucion minima necesaria
- `F4` debe auditar primero contra invariantes congeladas si el plan las
  define; si no existen, audita contra `plan.md` congelado, `execution.md` y
  la evidencia registrada
- las observaciones que dejen legacy, dualidad canonica o cleanup estructural
  dentro del scope auditado escalan a bloqueantes
- `SAFE_AUDITOR_AUTOFIX` aplica a artefactos de expediente y reconciliaciones
  mecanicas de gobernanza ya decididas; nunca a codigo de producto, tests,
  runtime, comportamiento observable, scripts canonicos, policies o cambios
  sustantivos de alcance

## Validacion real guiada

La validacion real aplica cuando cambia comportamiento observable del producto.
La conduce motor auditor con el usuario.

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

## Routing de Skills

Reglas:

- si una capacidad ya fue migrada a `dev/skills/`, la Skill es la fuente de
  verdad operativa de esa capacidad
- para capacidades migradas, la precedencia es:
  `dev/skills/` > `dev/prompts/` > `dev/ai/adapters/`
- los prompts legacy pueden sobrevivir solo como compatibilidad de solo
  lectura para tooling o uso manual
- si una Skill y su prompt legacy divergen, se corrige el prompt para
  converger con la Skill
- `governance_search` debe poder resolver tambien `document_type: "skills"`

## Validacion proporcional

Reglas:

- la validacion por iniciativa debe ser proporcional al write set y al blast
  radius reales
- por defecto no se ejecuta la suite completa
- deben priorizarse los tests directamente afectados y los rozados por
  dependencias relevantes
- la suite completa queda reservada a cambios transversales, blast radius no
  acotable, riesgo sistemico real o control periodico del carril weekly

## Routing de contexto

- gobernanza -> `governance_search`
- codigo vivo -> `symdex_code`
- estructura e impacto -> `codebase-memory-mcp`
- validacion observable -> evidencia runtime real

Si `symdex_code` o `codebase-memory-mcp` muestran sintomas de indice stale
respecto al baseline integrado (repo root incorrecto, proyecto de otro repo,
o `main/master` no reflejado tras un cierre integrado), el paso minimo seguro
es refrescar el indice repo-local en `main/master` antes de degradar a fallback:

- `scripts/dev/refresh_symdex_index.ps1`
- `scripts/dev/refresh_codebase_memory_index.ps1`

Contrato de refresh:

- `refresh_symdex_index.ps1` debe considerarse la via canonica completa para
  SymDex: refresca el indice en disco y reinicia los procesos MCP
  `symdex_code_server.mjs` asociados al repo, salvo uso explicito de
  `-SkipMcpRestart`.
- si tras ese refresh SymDex sigue resolviendo repo/proyecto viejos, el siguiente
  paso minimo seguro es recargar la ventana/sesion cliente para que relance el
  MCP; no reindexar en bucle.
- `refresh_codebase_memory_index.ps1` refresca el proyecto estructural y no
  reinicia MCP por defecto; usar `-RestartMcp` solo si `index_status`,
  `search_graph` o `trace_path` siguen stale tras refresh verificado.

Los indices son independientes por repo: cada consumidor mantiene su propio
`.mcp.json`, su propio `.symdex` y su propio proyecto efectivo en
`codebase-memory-mcp`.

Contrato de ramas:

- el indice estructural canonico representa `main/master` tras el ultimo cierre
  integrado
- una rama de iniciativa puede ir por delante del indice sin que eso sea stale
- los simbolos, ficheros y wiring creados en la rama se auditan con `git diff`,
  lectura directa y validacion ejecutable
- no se refrescan indices al arrancar `F2`, `F4` o cualquier fase solo para que
  los MCP vean una rama feature

## Bootstrap obligatorio para motor activo

Todo prompt, Skill o adapter operativo usado por el motor activo debe
exigir, antes de planificar o implementar:

1. cargar `AGENTS.md` y la Skill canonica de la fase si existe
2. usar `governance_search` para gobernanza con `phase` y `document_type`
   cuando aplique
3. usar `symdex_code` para codigo vivo y `codebase-memory-mcp` para wiring,
   impacto, legacy y blast radius cuando la tarea toque codigo
4. declarar cualquier degradacion antes de usar `rg`, `Read`, `Bash` o lectura
   bruta como via principal
5. no continuar si falta una precondicion material de fase

### Filtros recomendados para `governance_search`

- fases de iniciativa: `F1-F7`
- fases weekly: `W1-W4`
- tipos de documento soportados:
  - `workflow`
  - `policies`
  - `guarantees`
  - `skills`
  - `prompts`
  - `templates`
  - `adapters`
  - `profile`
  - `guides`
  - `governance_prompts`
  - `architecture`
  - `tooling_docs`

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
