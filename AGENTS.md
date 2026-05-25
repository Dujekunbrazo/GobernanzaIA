# Directrices Maestras Multi-IA

## 1) Fuente de verdad

Orden de precedencia:

1. `AGENTS.md`
2. `dev/workflow.md`
3. `dev/guarantees/*.md`
4. `dev/ai/adapters/*.md`
5. `dev/skills/` como capa operativa preferente para capacidades migradas
6. `dev/policies/*.md`
7. superficies nativas de producto (`CLAUDE.md`, `.claude/*` y equivalentes)
   como capa de compatibilidad

Si hay conflicto, prevalece la capa superior.

Carveout operativo: para capabilities ya migradas a `dev/skills/`, la Skill
canonica tiene precedencia operativa sobre los adapters (`dev/ai/adapters/`),
independientemente del orden general de capas. Un adapter no puede contradecir
ni sustituir la Skill canonica de una capability migrada; solo puede afinar
detalles de producto que la Skill no cubra.

## 2) Objetivo operativo

Trabajar en este repo con un proceso simple, repetible y auditable para:

- convertir conversaciones tecnicas en planes ejecutables de alta calidad
- ejecutar iniciativas con un unico plan formal y sin duplicidad documental
- revisar el repo periodicamente con un carril weekly separado
- mantener memoria operativa viva sin depender del chat

La gobernanza define como se procede.
El codigo define sobre que se trabaja.

## 3) Motores directos

- El sistema opera con dos IAs: un motor activo y un motor auditor.
- Los nombres concretos de cada motor se declaran durante la instalacion en
  `dev/governance_baseline.json`, bajo
  `installation_profile.preferred_working_ia` y
  `installation_profile.preferred_auditor_ia`.
- El motor activo conduce conversacion, lectura de codigo, propuesta y
  ejecucion (modos `M0`, `M1`, `M2`, `M3` y fases `F1`, `F3`).
- El motor auditor emite auditoria formal en `F2` y `F4` con veredicto
  binario `PASS` o `FAIL`.
- Tras `F4 PASS`, el motor auditor conduce operativamente `F5`, `F6` y `F7`.
- `AGENTS.md` es el contrato compartido real para ambos motores,
  independientemente de su nombre concreto.
- Los adapters por motor (`dev/ai/adapters/<motor>.md`) solo pueden afinar
  detalles de producto del motor; no deben crear workflow ni routing
  paralelos al canon.
- La continuidad durable especifica de cada motor se regula en su adapter
  correspondiente.

## 4) Modos M0-M4

- `M0 CONVERSACION`: ideacion, lectura de codigo y aterrizaje tecnico sin
  ejecucion.
- `M1 ANALISIS`: diagnostico tecnico sin cambios de codigo.
- `M2 DEBUG`: reproduccion y aislamiento de fallos sin implementar fix.
- `M3 IMPLEMENTACION_MENOR`: cambio acotado de bajo riesgo.
- `M4 INICIATIVA_COMPLETA`: cambio mediano o grande con trazabilidad formal.

Reglas:

- si el usuario no declara modo, iniciar en `M0`
- para entrar en `M3` o `M4`, se requiere aprobacion explicita del usuario
- toda transicion se registra como:
  `TRANSICION: Mx -> My | motivo | impacto | decision`
- en `M0`, `M1` y `M2` no se modifica codigo
- `M0` puede producir un `input de planificacion` transitorio para el motor
  activo
- ese input no forma parte del expediente formal de la iniciativa

## 5) Reglas duras no negociables

1. Todo prompt, Skill o adapter operativo usado por el motor activo debe
   cargar `AGENTS.md`, respetar el routing MCP canonico y usar las
   herramientas de gobernanza disponibles (`governance_search`,
   `symdex_code` y `codebase-memory-mcp`) antes de degradar a lectura bruta.
2. En `M3` solo se permite cambio acotado y trazable.
3. En `M4` el artefacto primario y unico de planificacion es `plan.md`.
4. El primer artefacto formal de una iniciativa es `plan.md`.
5. En `M4` no se implementa sin `PLAN CONGELADO`.
6. Las auditorias formales solo admiten `PASS` o `FAIL`.
7. No se permite `PASS` mientras exista cualquier hallazgo pendiente.
8. Si cambia el alcance, se reabre la fase previa correspondiente.
9. Un cambio logico por commit.
10. Prohibido refactor encubierto.
11. README solo incremental.
12. No inventar rutas, comandos o features.
13. Prohibido mezclar runtime del proyecto con artefactos de gobernanza.
14. Toda consulta debe rutearse a la capa canonica minima que la responda.
15. Queda prohibido usar dos capas primarias simultaneas para la misma
    responsabilidad.
16. La memoria estructural del sistema debe resolverse mediante la capa
    estructural canonica cuando este disponible.
17. Toda capability transversal debe resolverse mediante abstraccion canonica,
    owner explicito, punto de extension definido y wiring comun.
18. Queda prohibido cerrar una capability con wiring parcial, integraciones
    huerfanas, coexistencia legacy/canonica o paths paralelos.
19. La validacion observable no se inventa: si falta evidencia real donde
    aplica, el estado correcto es `BLOQUEADO`.
20. Si una iniciativa modifica comportamiento observable del producto, no puede
    cerrar sin validacion real completada.
21. La gobernanza debe optimizar coste total por tarea usando retrieval
    dirigido, tooling eficiente y no expansion masiva de contexto.
22. El weekly review descubre y prioriza; no genera planes de iniciativa.
23. Un hecho sustantivo debe escribirse una sola vez; los artefactos
    posteriores solo anaden delta, veredicto o evidencia.
24. Todo `FAIL` en `F2` o `F4` debe incluir remediacion minima verificable,
    criterio de cierre binario y alcance exacto de reejecucion; si no, la
    auditoria esta incompleta.
25. Si un `FAIL` de auditoria afecta solo a artefactos de la iniciativa o a
    una reconciliacion mecanica entre `plan.md`, DoD, write set, sidecars,
    `execution.md`, `plan_audit.md` o `post_audit.md`, el motor auditor debe
    aplicar `SAFE_AUDITOR_AUTOFIX` directamente y reauditar en el mismo loop.
    No se devuelve al motor activo salvo que cambie objetivo, alcance
    sustantivo, producto, arquitectura, restricciones, criterios PASS/FAIL o
    una decision material.
26. Toda observacion que deje legacy, dualidad canonica, cleanup estructural,
    contrato a medias o evidencia material pendiente dentro del scope auditado
    debe escalar a hallazgo bloqueante.
27. Una iniciativa no queda operativamente cerrada mientras el working tree no
    este limpio, los commits finales no existan y el estado Git final no quede
    trazado.
28. Si una iniciativa cambia comportamiento observable, superficie operativa,
    DX, flujo de uso o procedimiento de integracion, el `README.md` del
    proyecto debe actualizarse incrementalmente antes del cierre final.
29. La integracion a troncal y el borrado de ramas no se presuponen: deben
    quedar declarados explicitamente en `closeout.md`.
30. `SymDex` y `codebase-memory-mcp` representan el baseline integrado de
    `main/master`. Una rama de iniciativa adelantada no convierte el indice en
    stale por no contener simbolos nuevos de la rama; ese delta se valida con
    `git diff`, lectura directa y tests. El refresco repo-local se ejecuta en
    `main/master` tras merge/cierre integrado, no como rutina de arranque de
    fases ni para hacer visible una rama feature.
31. Tras `F5` con `APTA_PARA_F6` o `NO_APLICA`, el handoff a `F6` autoriza por
    defecto el cierre completo estandar con el motor auditor: `F6`, `F7`,
    commit final, push de rama, integracion a `main/master`, push de troncal,
    borrado de rama local/remota y refrescos MCP post-merge. Solo se deja
    pendiente si el usuario pide explicitamente PR/merge manual, la proteccion
    remota lo impide, hay cambios ajenos no conciliables o falta una
    precondicion material.
32. Antes de proponer canon nuevo (nueva capability, nuevo identificador
    canon, nuevo `access_pattern`, nuevo arquetipo trigger/receptor, nueva
    seed o renombrado de un tipo, capability o identificador ya canonizado),
    debe ejecutarse o citarse la salida de
    `python scripts/dev/memory_precheck.py <termino_candidato>` con
    `Verdict: ALLOW` o `Verdict: BLOCK` visible y trazable en chat. Si el
    veredicto es `BLOCK`, la propuesta no avanza hasta inventariar los
    matches activos y decidir si lo propuesto es reconciliacion con canon
    existente (no canon nuevo) o si la propuesta se retira. Previene
    regresiones del tipo "renombrado de un identificador canon ya en uso" o
    "creacion de canon paralelo al existente con nombre distinto".

## 6) Carriles canonicos

El sistema opera sobre dos carriles principales:

### Carril iniciativa

Usado para cambios concretos que van a ejecucion.

| Fase | Proposito |
| ---- | --------- |
| `F1` | `plan.md` propuesto |
| `F2` | auditoria y congelado de plan |
| `F3` | implementacion |
| `F4` | post-auditoria |
| `F5` | validacion real guiada cuando aplique |
| `F6` | docs + cierre |
| `F7` | lecciones finales |

Reglas:

- `F1` puede nacer desde `M0` usando un `input de planificacion` transitorio
- en `F2` y `F4` solo el motor auditor emite auditoria formal
- si el resultado es `FAIL`, no se avanza
- si falta precondicion, el estado correcto es `BLOQUEADO`
- `F5` es obligatoria cuando la iniciativa toca comportamiento observable del
  producto; si no aplica, debe trazarse como `NO_APLICA`
- `F5`, `F6` y `F7` se ejecutan con el motor auditor tras `F4 PASS`.
- Desde `F6`, el motor auditor debe ejecutar el cierre completo estandar de
  forma continua cuando no exista bloqueo: documentacion, lecciones,
  commit/push, merge a `main/master`, push de troncal, borrado de ramas y
  refrescos MCP post-merge.
- todo hallazgo formal de `F2` o `F4` debe ser tipado y cerrable:
  `Tipo`, `Artefacto afectado`, `Seccion exacta`, `Cambio minimo requerido`,
  `Criterio de cierre`, `Rerun scope` y `Reapertura requerida`
- `F6` no puede declararse completo sin:
  - `closeout.md` y `lessons_learned.md`
  - estado Git final trazado
  - `README.md` actualizado si la iniciativa cambia superficie visible
  - refresco post-merge de `SymDex` y `codebase-memory-mcp` cuando la
    iniciativa ya este integrada en `main/master`

### Carril weekly review

Usado para revision estrategica recurrente del repo.

| Fase | Proposito |
| ---- | --------- |
| `W1` | briefing factual |
| `W2` | review estrategica |
| `W3` | actualizacion de findings y backlog |
| `W4` | promocion opcional a iniciativa |

Reglas:

- `W1` extrae hechos; no propone planes de implementacion
- `W2` prioriza usando MIT y Krug
- `W4` solo promociona candidatos; la iniciativa formal nace despues en `M0`
- el primer weekly de un repo o de una gobernanza recien implantada se ejecuta
  como `BASELINE`, sin delta previo y con profundidad alta

## 7) Validacion real F5

`F5` formaliza el barrido real antes del cierre documental cuando aplica.
El motor auditor conduce `F5` con el usuario.

Reglas:

- su salida obligatoria es `real_validation.md` cuando aplica
- debe ejecutar el barrido real completo antes de decidir fixes
- si aparecen fallos materiales, corresponde reabrir `F3`
- si se reabre `F3`, deben repetirse `F4` y `F5` antes de `F6`
- `F6` solo puede empezar cuando `real_validation.md` declare
  `Decisión final: APTA_PARA_F6`
- la evidencia de primer nivel incluye:
  - chat del producto
  - `trace on`
  - terminal o logs de la superficie validada
  - resultados visibles en runtime real

## 7.1) Cierre F6/F7

- `F6` lo conduce el motor auditor mediante `dev/skills/f6_closeout/SKILL.md`.
- `F7` lo conduce el motor auditor mediante `dev/skills/f7_lessons/SKILL.md`.
- `closeout.md` y `lessons_learned.md` siguen siendo obligatorios.
- El cierre no queda completo sin README incremental cuando aplique, estado Git
  final trazado, commits finales, push/merge/borrado de ramas ejecutado o
  bloqueo trazado, y refrescos MCP post-merge en `main/master` cuando aplique.

## 8) Precedencia tecnica

1. MIT Concept-Sync para macroarquitectura.
2. Clean Code para microimplementacion.
3. Krug para UI, CLI, DX y respuestas orientadas a usuario.
4. Rendimiento puede excepcionar Clean Code solo en hot paths con evidencia.
5. Validacion determina aceptabilidad final.

## 9) Stack canonico de contexto

El sistema opera sobre cuatro capas:

1. `gobernanza normativa`
   - reglas, workflow, guarantees, policies y adapters
2. `codigo vivo local`
   - lectura fina de simbolos y bloques concretos
3. `memoria estructural persistente`
   - wiring global, impacto, legacy y arquitectura estructural
4. `evidencia runtime real`
   - comportamiento observable, trazas, terminal y resultados visibles

La memoria conversacional no forma parte del stack canonico.

### Capa estatica siempre presente

- reglas duras no negociables
- resumen del workflow
- routing MCP canonico
- instrucciones de degradacion

### Gobernanza dinamica bajo demanda

Corpus canonico:

- `dev/workflow.md`
- `dev/policies/`
- `dev/guarantees/`
- `dev/skills/`
- `dev/prompts/`
- `dev/templates/initiative/`
- `dev/ai/adapters/`
- `dev/governance_guide.md`
- `dev/repo_governance_profile.md`
- `doc/architecture/`
- `doc/governance_ping_pong_guide.md`
- `doc/governance_prompts/`
- `scripts/README.md`
- `scripts/dev/README.md`
- `scripts/ops/context_mcp/README.md`

Exclusiones duras:

- `dev/records/`
- `dev/records/legacy/`
- `.claude/` y `CLAUDE.md` como corpus de retrieval
- historico, bitacoras y salidas generadas

## 10) Routing MCP canonico

Autocheck obligatorio al inicio de sesion o tras recarga:

- `governance_search`
- `symdex_code.semantic_search`
- `symdex_code.get_symbol`
- `codebase-memory-mcp`

Si alguna capacidad falta o falla, debe declararse antes de continuar.
Si `symdex_code` o `codebase-memory-mcp` muestran sintomas de indice stale
respecto al baseline integrado (repo root incorrecto, proyecto de otro repo,
o `main/master` no reflejado tras un cierre integrado), debe ejecutarse primero
el refresco repo-local en `main/master` antes de declararlos como rotos:
- `scripts/dev/refresh_symdex_index.ps1`
- `scripts/dev/refresh_codebase_memory_index.ps1`
La indexacion y su estado en disco son locales por repo; queda prohibido
reusar `.symdex`, proyectos o caches estructurales de otro repositorio.
En una rama de iniciativa, que el MCP no vea simbolos creados por esa rama no
es por si solo sintoma stale; el delta de rama debe auditarse mediante diff
directo, lectura local puntual y validacion ejecutable.

Routing por responsabilidad:

- gobernanza -> `governance_search`
- codigo vivo -> `symdex_code`
- wiring, impacto estructural, blast radius, hubs, legacy y dead code ->
  `codebase-memory-mcp`

Reglas:

- si la consulta esta claramente acotada a una fase de iniciativa o weekly,
  `governance_search` debe ejecutarse con `phase`
- si la consulta esta claramente acotada a un tipo de documento, anadir tambien
  `document_type`
- las fases aceptables del retrieval de gobernanza son `F1-F7` y `W1-W4`
- usar `semantic_search` solo si la capacidad semantica de `SymDex` esta
  validada en el repo
- si no lo esta, degradar a `search_symbols` y `get_symbol`; `search_text`
  queda solo como apoyo textual
- en memoria estructural, verificar primero el proyecto efectivo con
  `list_projects`
- usar `search_graph` y `trace_path` como camino primario de analisis
  estructural; reservar `query_graph` para ultima milla y solo con queries
  acotadas
- usar `codebase-memory-mcp` para localizar relaciones y volver a
  `symdex_code` para leer fino el codigo exacto
- `Glob`, `Grep`, `find`, `rg`, `Read` o `Bash` solo se permiten como fallback
  si el MCP correspondiente falla o no esta disponible, o para lectura final
  puntual del archivo ya localizado

## 11) Memoria operativa viva

La memoria operativa persistente se reparte asi:

- `dev/records/reviews/initiative_backlog.md`
  - ideas vivas y candidatos nacidos en conversacion, weekly o closeout
- `dev/records/reviews/architecture_findings_register.md`
  - hallazgos estructurales persistentes con evidencia
- `dev/records/reviews/initiative_architecture_backlog.md`
  - remanentes y follow-ups de iniciativas cerradas

Reglas:

- una idea no validada no se eleva a findings register
- un hallazgo weekly persistente no debe vivir solo dentro del weekly
- un remanente de iniciativa no debe quedar enterrado solo en `closeout.md` o
  `lessons_learned.md`

## 12) Perfil local de capacidades

Cada repo consumidor debe mantener un unico perfil local en:

- `dev/repo_governance_profile.md`

Ese perfil:

- describe tooling realmente disponible
- declara el estado real de `governance_search`, `symdex_code` y
  `codebase-memory-mcp`
- fija degradaciones aceptables
- no redefine el canon

## 13) Rutas canonicas

- gobernanza activa: `dev/`
- workflow de referencia: `dev/workflow.md`
- perfil local: `dev/repo_governance_profile.md`
- iniciativas: `dev/records/initiatives/<initiative_id>/`
- validacion real guiada: `dev/records/initiatives/<initiative_id>/real_validation.md`
- memoria operativa viva:
  - `dev/records/reviews/initiative_backlog.md`
  - `dev/records/reviews/architecture_findings_register.md`
  - `dev/records/reviews/initiative_architecture_backlog.md`
- validadores de cierre:
  - `scripts/dev/check_naming_compliance.py`
  - `scripts/dev/check_state0.py`

## 14) Contrato de bloqueo

Si falta contexto, evidencia o precondicion, la IA debe:

1. parar
2. declarar bloqueo con evidencia
3. proponer el siguiente paso minimo seguro
