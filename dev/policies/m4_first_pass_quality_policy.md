# M4 First Pass Quality Policy

Proposito:
- optimizar first-pass quality del carril `M4`
- reducir coste total por tarea y retries ciegos
- fijar limites, telemetria y bloqueo con trazabilidad canonica

## 1) Ambito

- esta policy aplica al carril iniciativa `M4`
- no redefine weekly review ni el resto de la gobernanza
- el script `ping_pong` la implementa; no la sustituye
- la gobernanza de `BLOQUEADO` y desbloqueo válido se complementa en
  `dev/policies/m4_governed_blocking_unblocking_policy.md`

## 2) Retry bounds canonicos

Los limites son **hard caps por loop acotado**, no por comando individual ni
por iniciativa completa:

- plan loop `F1 <-> F2`:
  - maximo 3 invocaciones de motor activo
  - maximo 3 invocaciones de motor auditor
- scoped loop `F3 <-> F4`:
  - maximo 3 invocaciones de motor activo
  - maximo 3 invocaciones de motor auditor
- final loop `F3_FINAL <-> F4_FINAL`:
  - maximo 3 invocaciones de motor activo
  - maximo 3 invocaciones de motor auditor

Si `F5` reabre `F3`, nace un nuevo scoped loop y despues un nuevo final loop
con contadores independientes.

Si se agota el limite del loop activo, el estado correcto es `BLOQUEADO`.

## 3) Regla de retry permitido

Un retry solo es aceptable si existe al menos una de estas condiciones:

- evidencia nueva
- cambio de `failure_signature`
- cambio material de condicion de entrada

Si el `failure_signature` se repite sin evidencia nueva, el estado correcto es
`BLOQUEADO`.

## 4) failure_signature

`failure_signature` es una tupla normalizada con estos campos:

- `phase`
- `layer`
- `target_artifact`
- `failure_code`
- `evidence_fingerprint`

Reglas:

- `evidence_fingerprint` debe derivarse de evidencia estructurada del fallo
- no debe depender de texto libre completo ni de historial conversacional
- debe permitir comparar mecanicamente si dos fallos son el mismo o no

## 5) Contrato narrativo y sidecars

- el artefacto canonico de estado es la metadata `Veredicto:` dentro de
  `plan_audit.md` y `post_audit.md`
- `f2_verdict.txt` y `f4_verdict.txt` son sidecars operativos del bridge de
  CLI; no son expediente primario
- antes de calcular estado o gastar otra auditoria, debe ejecutarse un
  pre-gate de reconciliacion sidecar -> narrativo
- si sidecar y narrativo contienen veredictos validos distintos, el estado
  correcto es `BLOQUEADO`

## 6) Pre-gates deterministas minimos

Antes de `F2` y `F4`, el sistema debe comprobar como minimo:

- reconciliacion sidecar -> narrativo
- metadata narrativa coherente
- headings/campos obligatorios del artefacto auditado
- write set declarado fuera de alcance
- gating de validacion final cuando aplique

Si el fallo es mecanico y puede corregirse de forma segura, se corrige antes
de gastar otra auditoria. Si no, se bloquea.

## 7) Politica inicial de modelos

Defaults canonicos:

- `F1`: `claude-sonnet-4-6`, esfuerzo `medium`
- `F3`: `claude-sonnet-4-6`, esfuerzo `medium`
- `F3_FINAL`: `claude-sonnet-4-6`, esfuerzo `medium`
- `F2`: `gpt-5.4`
- `F4`: `gpt-5.4`
- `F4_FINAL`: `gpt-5.4`

Escalado permitido:

- `F1` puede escalar a `claude-opus-4-6` solo si se cumple al menos una
  condicion:
  - el write set esperado cruza 4 o mas superficies entre `dev/workflow.md`,
    `dev/policies/`, `dev/ai/adapters/`,
    `scripts/dev/governance_ping_pong.py` y
    `doc/governance_ping_pong_guide.md`
  - el input de `M0` cierra 3 o mas decisiones estructurales duras
  - el mismo `plan.md` ya recibio un `FAIL` de `F2` con 2 o mas hallazgos
    `HIGH`
- `F3` y `F3_FINAL` pueden escalar a `claude-opus-4-6` solo si el hallazgo
  activo es semantico/arquitectural y ademas:
  - toca 3 o mas ficheros, o
  - cruza 2 o mas superficies de gobernanza
- los fallos mecanicos no justifican escalado

En esta policy no se degrada por debajo de `claude-sonnet-4-6` ni de
`gpt-5.4`.

## 8) Agentes operativos por fase

Los agentes operativos especializan la invocacion real del motor por fase sin
crear fases, artefactos ni rutas paralelas. El canon sigue siendo:

- motor activo: `Claude`
- motor auditor: `Codex`
- artefactos: los ya definidos por `F1-F7`

Matriz canonica:

| Fase | Motor | agent_id | agent_profile | Responsabilidad |
| ---- | ----- | -------- | ------------- | --------------- |
| `F1` | Claude | `m4.f1.claude.plan_architect` | `claude_plan_architect` | convertir input de `M0` en `plan.md` congelable, con alcance, riesgos, DoD y validacion |
| `F2` | Codex | `m4.f2.codex.plan_auditor` | `codex_plan_auditor` | auditar congelabilidad del plan; no auditar implementacion inexistente |
| `F2/F4 AUTOFIX` | Codex | `m4.audit.codex.safe_autofix` | `codex_auditor_autofix` | corregir solo fallos mecanicos elegibles del expediente |
| `F3` | Claude | `m4.f3.claude.implementation_executor` | `claude_implementation_executor` | ejecutar el plan congelado sin replanificar ni ampliar alcance |
| `F3_FINAL` | Claude | `m4.f3_final.claude.final_validation_executor` | `claude_final_validation_executor` | registrar validacion amplia/final del plan congelado ya ejecutado |
| `F4` | Codex | `m4.f4.codex.bug_structural_auditor` | `codex_bug_structural_auditor` | auditar bugs, evidencia, wiring parcial, legacy, paths paralelos y desviaciones |
| `F4_FINAL` | Codex | `m4.f4_final.codex.final_consistency_auditor` | `codex_final_consistency_auditor` | auditar suficiencia de validacion final sin exigir fases posteriores |
| `F5` | Codex | `m4.f5.codex.real_validation_guide` | `codex_real_validation_guide` | conducir evidencia observable real con el usuario |
| `F6` | Codex | `m4.f6.codex.closeout_auditor` | `codex_closeout_auditor` | cerrar expediente, README y estado Git cuando aplique |
| `F7` | Codex | `m4.f7.codex.lessons_curator` | `codex_lessons_curator` | extraer lecciones y enrutar remanentes vivos |

Reglas:

- `agent_id` identifica el agente que se levanta para la fase
- `agent_profile` define la personalidad operativa de ese agente
- `agent_id` y `agent_profile` no sustituyen `phase`, `motor`, `model` ni `effort`
- no se crean `plan.md` alternativos, contratos de sprint separados ni fases
  intermedias
- cada Skill canonica debe declarar el perfil que representa
- el script `ping_pong` debe resolver un `AgentSpec` por fase, envolver el
  prompt con `AGENTE_M4_ACTIVO`, levantar el CLI con variables de entorno
  `GOVERNANCE_AGENT_*` y registrar `agent_id`, `agent_name`,
  `agent_profile` y `skill_path` en `ping_pong_usage.jsonl`

## 9) Contrato de respuesta y handoff manual

Cuando el usuario use el chat como puente manual entre `Claude` y `Codex`, la
respuesta final del motor que acaba de trabajar debe cerrar con un bloque
pegable `HANDOFF_SIGUIENTE_AGENTE`.

Este bloque:

- es contenido de chat, no artefacto formal de iniciativa
- no sustituye `plan.md`, `plan_audit.md`, `execution.md`, `post_audit.md`,
  `real_validation.md`, `closeout.md` ni `lessons_learned.md`
- debe recordar al siguiente motor su `agent_id`, perfil, fase, bootstrap de
  gobernanza, routing MCP y artefactos exactos que debe leer/escribir
- debe evitar que el siguiente motor dependa de memoria conversacional o de
  una transcripcion parcial

Shape obligatorio:

```md
## HANDOFF_SIGUIENTE_AGENTE

- Repo:
- Initiative ID:
- Fase completada:
- Agent ID ejecutado:
- Agent name ejecutado:
- Agent profile ejecutado:
- Estado o veredicto:
- Artefactos modificados:
- Siguiente fase:
- Siguiente agent_id:
- Siguiente agent_name:
- Siguiente agent_profile:
- Bootstrap obligatorio:
  - leer `AGENTS.md`
  - cargar la Skill canonica de la fase siguiente
  - ejecutar autocheck de capacidades: `governance_search`, `symdex_code` y
    `codebase-memory-mcp`
  - usar `governance_search` con `phase` y `document_type` cuando aplique
  - verificar proyecto efectivo con `codebase-memory-mcp.list_projects`
  - verificar estado de `symdex_code`; si indice stale, refrescar antes de
    degradar
- Artefactos que debe leer:
- Write set autorizado:
- Prohibido:
- Comando sugerido o siguiente accion:
- Evidencia y validacion relevante:
- Bloqueos o riesgos pendientes:
```

Reglas:

- si no hay siguiente fase porque la iniciativa ya cerro, el bloque debe decir
  `Siguiente fase: N/A`
- si hubo degradacion de tooling, debe aparecer en `Bloqueos o riesgos
  pendientes`
- si el siguiente motor es auditor, el handoff no debe intentar defender el
  trabajo; debe facilitar una auditoria esceptica

## 10) Telemetria canonica

El ledger append-only canonico es `ping_pong_usage.jsonl`.

Cada linea debe incluir exactamente:

- `ts_utc`
- `initiative_id`
- `phase`
- `attempt`
- `motor`
- `agent_id`
- `agent_name`
- `agent_profile`
- `skill_path`
- `model`
- `effort`
- `prompt_chars`
- `response_chars`
- `wall_time_ms`
- `input_tokens`
- `output_tokens`
- `cached_tokens`
- `cost_usd`
- `usage_source`
- `result`
- `failure_signature`

Reglas:

- `usage_source` solo puede ser `provider` o `estimated`
- si una metrica real no existe, el campo queda en `null`
- si se usa estimacion, debe quedar trazado con `usage_source=estimated`

## 11) F5 y evidencia final

Para iniciativas donde aplica validacion real:

- `F5` exige al menos una ejecucion real del flujo optimizado
- el benchmark comparativo es evidencia complementaria, nunca sustitutiva
- si `F5` encuentra fallo material, corresponde reabrir `F3` y repetir `F4`
  y `F5`
