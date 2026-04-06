# Directrices Maestras Multi-IA

## 1) Fuente de verdad

Orden de precedencia:

1. `AGENTS.md`
2. `dev/workflow.md`
3. `dev/guarantees/*.md`
4. `dev/ai/adapters/*.md`
5. `dev/policies/*.md`
6. superficies nativas de producto (`.roo/*`, `.claude/*`, `CLAUDE.md` y equivalentes) como capa de compatibilidad/adaptación

Si hay conflicto, prevalece el nivel superior.

## 2) Objetivo operativo

Trabajar con un proceso cerrado, repetible y auditable.
La gobernanza define como se procede; el código define sobre qué se trabaja.

## 3) Modos M0-M4

- `M0 CONVERSACION`: ideación, aclaraciones y discusión técnica sin ejecución.
- `M1 ANALISIS`: diagnóstico técnico sin cambios de código.
- `M2 DEBUG`: reproducción y aislamiento de fallos sin implementar fix.
- `M3 IMPLEMENTACION_MENOR`: cambio acotado de bajo riesgo.
- `M4 INICIATIVA_COMPLETA`: cambio mediano/grande con trazabilidad formal.

Reglas de activación:

- Si el usuario no declara modo, iniciar en `M0`.
- Para entrar en `M3` o `M4` se requiere aprobación explícita del usuario.
- Toda transición usa:
  `TRANSICION: Mx -> My | motivo | impacto | decision`.
- No existe motor por defecto.
- El usuario designa `motor_activo`.
- En `M4`, el usuario designa `motor_auditor` en `F2`.

## 4) Reglas duras no negociables

1. Si el usuario no declara modo, iniciar en `M0`.
2. Para entrar en `M3` o `M4` se requiere aprobación explícita del usuario.
3. Toda transición usa el formato `TRANSICION: Mx -> My | motivo | impacto | decision`.
4. En `M0/M1/M2` está prohibido editar código.
5. En `M3` solo se permite cambio acotado y trazable.
6. En `M4` aplica pipeline `F1-F10` completo.
7. En `M4` no se planifica sin `ASK CONGELADO`.
8. En `M4` no se implementa sin `PLAN CONGELADO`.
9. Si cambia el alcance, se reabre la fase previa correspondiente.
10. Las auditorías formales solo admiten `PASS` o `FAIL`.
11. No se permite `PASS` mientras exista cualquier hallazgo pendiente.
12. En auditorías formales no existe categoría operativa de observaciones; todo punto señalado por el auditor debe registrarse como hallazgo o no incluirse.
13. No se permite `PASS` mientras exista cualquier punto señalado pendiente, ambigüedad material, debilidad operativa o riesgo descrito por el auditor.
14. Máximo 1 auditoría inicial y 2 re-auditorías por fase.
15. Un cambio lógico por commit.
16. Prohibido refactor encubierto.
17. README solo incremental.
18. No inventar rutas, comandos o features.
19. Prohibido mezclar runtime del proyecto con artefactos de gobernanza.
20. Sin compliance de nomenclatura y state0 no hay cierre formal.
21. Toda capability transversal del sistema debe resolverse mediante abstracción canónica, owner arquitectónico explícito, punto de extensión definido y wiring común.
22. Queda prohibido resolver capabilities transversales mediante branching por `tool`/`path`/`channel`/`filter`, coverage vertical aislada, paths paralelos, fallback legacy conviviendo con el camino canónico o lógica específica por herramienta en `planner`/`generator`/`router`/`execute` cuando corresponda `descriptor`/`policy`/`registry` común.
23. Ninguna capability se considera completada mientras no esté conectada en su wiring canónico sobre todas las superficies incluidas en alcance.
24. Queda prohibido cerrar una iniciativa con wiring parcial, integraciones huérfanas, convivencia legacy/canónico o paths paralelos para la misma capability.
25. En cada nueva iniciativa está prohibido terminar con archivos brillantes, cableado mediocre o legacy vivo. Se considera incumplimiento material cualquier cierre cosmético o documentalmente pulido que oculte wiring deficiente, paths paralelos, integraciones huérfanas o convivencia legacy/canónico.
26. Si una iniciativa `M4` modifica comportamiento observable del producto, no puede cerrar `F8` ni avanzar a `F9` sin `real_validation.md` completado.
27. Durante la validación real guiada no se toca código tras el primer fallo material, salvo bloqueo crítico que impida continuar el barrido.
28. Los artefactos sustantivos de fase pertenecen al motor responsable de esa fase; el orquestador no redacta `ask.md`, `plan.md`, `execution.md`, `ask_audit.md`, `plan_audit.md`, `post_audit.md` ni `real_validation.md`.
29. El orquestador solo puede reparar formato o metadata de un artefacto sustantivo cuando exista autorización explícita del usuario o fallo mecánico de la máquina de estados.
30. La continuidad operativa no puede depender de la memoria del chat; toda reentrada de motor debe arrancar con `phase_ticket` y `resume_packet` emitidos por el orquestador.
31. En `F6` largas, multi-commit o de alto riesgo, la ejecución debe supervisarse por commit con checkpoint antes de liberar el siguiente tramo.
32. En `F8`, la evidencia de primer nivel incluye chat del producto, `trace on`, terminal de la superficie probada y resultados visibles en runtime real.
33. Toda consulta debe rutearse a la capa canónica mínima que la responda; queda prohibido usar dos capas primarias simultáneas para la misma responsabilidad.
34. La memoria estructural del sistema debe resolverse mediante la capa estructural canónica cuando esté disponible; no puede coexistir como vía opcional lateral frente al camino oficial.
35. Todo repo consumidor debe declarar un único perfil local de capacidades reales; el orquestador debe degradar según ese perfil y no asumir tooling homogéneo entre repos.

## 4.1) Apertura durable de M4

- `handoff.md` no puede nacer en `M0`; en `M0` no se crean artefactos.
- Tras la transición `M0 -> M4`, y antes de `F1`, puede crearse
  `dev/records/initiatives/<initiative_id>/handoff.md`.
- `handoff.md` es el artefacto primogénito opcional para conservar análisis y
  planificación previa cuando la conversación o el modo del producto generen
  contenido valioso antes de `F1`.
- `handoff.md` no sustituye `ask.md` ni `plan.md` y no redefine el pipeline
  `F1-F10`.
- Si existe `handoff.md`, `F1` debe derivar el `ask.md` desde ese artefacto.
- Si existe `handoff.md`, `F4` debe derivar el `plan.md` desde ese artefacto y
  desde el `ask.md` congelado.

## 5) Pipeline F1-F10

| Fase | Propósito |
| ---- | --------- |
| `F1` | Ask propuesto |
| `F2` | Validación de ask por usuario + designación de `motor_auditor` |
| `F3` | Auditoría y congelado de ask |
| `F4` | Plan propuesto |
| `F5` | Auditoría y congelado de plan |
| `F6` | Implementación |
| `F7` | Post-auditoría / debug |
| `F8` | Validación real guiada |
| `F9` | Docs + cierre |
| `F10` | Lecciones finales y feedback de gobernanza |

Reglas:

- En `F3`, `F5` y `F7` solo el `motor_auditor` emite la auditoría formal.
- Si el resultado es `FAIL`, no se avanza de fase.
- Si falta precondición, el estado correcto es `BLOQUEADO`.
- Si existe `handoff.md`, se usa como fuente canónica de apertura de `M4`, pero
  la ejecutabilidad formal sigue dependiendo de `ask.md` y `plan.md`.
- `F8` es obligatoria cuando la iniciativa toca comportamiento observable del
  producto; si no aplica, debe trazarse como `NO_APLICA`.

## 5.2) Propiedad de artefactos y continuidad operativa

- `F1`: `ask.md` lo escribe solo el `motor_activo`.
- `F3`: `ask_audit.md` lo escribe solo el `motor_auditor`.
- `F4`: `plan.md` lo escribe solo el `motor_activo`.
- `F5`: `plan_audit.md` lo escribe solo el `motor_auditor`.
- `F6`: `execution.md` lo escribe y mantiene solo el `motor_activo`.
- `F7`: `post_audit.md` lo escribe solo el `motor_auditor`.
- `F8`: `real_validation.md` lo escribe quien guía o ejecuta la validación real.
- el orquestador no sustituye la autoría de los motores; coordina fases,
  gates, intentos, excepciones, tickets y contexto operativo
- toda entrada o reentrada de un motor debe llevar:
  - `phase_ticket`: autorización y límites vigentes de la fase
  - `resume_packet`: estado operativo resumido, hallazgos abiertos, último
    punto aceptado y siguiente paso permitido

## 5.2.1) Gobernanza ejecutiva del orquestador

- el orquestador es la capa ejecutiva del sistema de gobernanza
- coordina:
  - sesiones
  - fase efectiva
  - precondiciones
  - tickets de fase
  - rehidratación
  - intentos
  - excepciones
  - receipts
  - checkpoints
- no redacta artefactos sustantivos de motor
- no sustituye el juicio técnico del `motor_auditor`
- no inventa validación observable
- su contrato operativo de referencia es:
  - `dev/policies/orchestrator_execution_policy.md`

## 5.3) F6 — Ejecución supervisada

- `F6` puede ejecutarse en modo estándar para cambios cortos y acotados
- `F6` debe pasar a modo supervisado por commit cuando:
  - el plan sea multi-commit no trivial
  - exista capability transversal
  - exista riesgo de legacy/canónico
  - el usuario o el orquestador lo exijan por riesgo operativo
- en `F6` supervisada:
  - el orquestador libera solo el siguiente commit o tramo autorizado
  - el `motor_activo` implementa ese tramo y actualiza `execution.md`
  - el orquestador verifica disciplina mecánica y coherencia mínima
  - el `motor_auditor` puede emitir `execution_checkpoint.md` lateral
  - solo después puede liberarse el siguiente tramo
- `execution.md` no se reconstruye desde fuera; debe reflejar lo que hizo el
  `motor_activo` con evidencia real de validación y desvíos

## 5.1) F8 — Validación real guiada

`F8` formaliza el barrido real en Kiminion o superficie equivalente antes del
cierre documental.

Reglas:

- no es una auditoría formal nueva
- su salida obligatoria es `real_validation.md` cuando aplica
- debe ejecutar el barrido real completo antes de decidir fixes
- si aparecen fallos materiales, corresponde reabrir `F6`
- si se reabre `F6`, deben repetirse `F7` y `F8` antes de `F9`
- solo puede avanzar a `F9` cuando `real_validation.md` declare
  `Decisión final: APTA_PARA_F9`
- `F8` se ejecuta en modo guiado en vivo:
  - el motor no replantea `F1-F5`
  - guía al usuario caso por caso
  - registra expected, observed y evidencia viva
  - usa `trace on`, terminal y chat del producto como evidencia de primer nivel
  - se detiene en el primer fallo material salvo bloqueo crítico de entorno

## 6) Precedencia técnica

1. MIT Concept-Sync para macroarquitectura.
2. Clean Code para microimplementación.
3. Krug para UI, CLI, DX y respuestas orientadas a usuario.
4. Rendimiento puede excepcionar Clean Code solo en hot paths con evidencia.
5. Validación determina aceptabilidad final.

## 7) Corpus de contexto

## 7.1) Stack canónico de contexto

El sistema opera sobre cinco capas:

1. `gobernanza normativa`
   - reglas, workflow, guarantees, policies, templates y adapters
2. `gobernanza ejecutiva del orquestador`
   - fase vigente, tickets, reentrada, checkpoints, intentos y excepciones
3. `código vivo local`
   - lectura fina de símbolos y bloques concretos
4. `memoria estructural persistente`
   - wiring global, impacto, legacy y arquitectura estructural
5. `evidencia runtime real`
   - comportamiento observable, trazas, terminal y resultados visibles

La memoria conversacional no forma parte del stack canónico.
La policy operativa de referencia es:

- `dev/policies/context_stack_policy.md`
- `dev/policies/repo_capabilities_policy.md`

### Capa estática siempre presente

- reglas duras no negociables
- resumen del workflow
- precedencia técnica
- instrucciones de recuperación de contexto

### Gobernanza dinámica bajo demanda

Corpus canónico:

- `dev/policies/`
- `dev/guarantees/`
- `dev/prompts/`
- `dev/templates/initiative/`
- `dev/ai/adapters/`
- `dev/workflow.md`
- `doc/architecture/`

Exclusiones duras:

- `dev/records/`
- `dev/records/legacy/`
- `.roo/` como corpus de retrieval
- `.claude/` y `CLAUDE.md` como corpus de retrieval
- histórico, bitácoras y salidas generadas

La recuperación de gobernanza debe ser híbrida:

- filtro determinista por fase, tipo de documento y motor
- ranking semántico dentro del subconjunto
- fallback al documento canónico completo si hay ambigüedad
- herramienta operativa: `governance_search`
- routing obligatorio:
  - consulta de gobernanza -> `governance_search` y luego lectura canónica
  - consulta de estado operativo -> runtime del orquestador y sus artefactos
  - consulta de código -> `semantic_search` y luego `get_symbol` (via symdex_code)
  - consulta de wiring/legacy/impacto estructural -> `codebase-memory-mcp`
    cuando esté disponible; si no, fallback explícito
  - consulta de validación observable -> evidencia runtime real
- `Glob`, `Globpattern`, `Grep`, `find`, `rg` o lecturas directas no cuentan
  como vía principal si el MCP correspondiente está disponible
- herramientas internas solo como fallback si el MCP falla, no está expuesto o
  para lectura final puntual del archivo ya localizado

### SymDex

`SymDex` se usa solo para código vivo del producto.

Incluir:

- `core/`
- `integrations/MCP-Microsoft-Office/src/`
- `scripts/`
- `tests/`
- `manifests/`

Excluir:

- `node_modules`
- `.venv`
- `__pycache__`
- caches
- logs
- `state`
- `sessions`
- `content`
- gobernanza y artefactos históricos
- herramientas operativas (via symdex_code):
  - `semantic_search`, `search_symbols`, `search_text`
  - `get_symbol`, `get_file_outline`, `get_symbols`
- en respuestas técnicas se debe declarar herramienta usada y fuente canónica
  usada

### Memoria estructural persistente

La capa estructural canónica del sistema se reserva para:

- call paths reales
- blast radius
- legacy y dead code
- arquitectura estructural
- contraste entre wiring esperado y wiring real

Mientras no esté instalada, su uso degrada a `SymDex` más lectura canónica del
repo.
Cuando exista, no puede convivir como vía lateral con otra capa estructural
primaria.

### Evidencia runtime real

La validación observable del producto se apoya en:

- chat del producto
- `trace on`
- terminal de la superficie validada
- logs y resultados visibles en runtime real

Si esta evidencia falta donde aplica, el estado correcto es `BLOQUEADO`.

## 8) Motores

- `Codex`, `Claude`, `Gemini` y `Roo` pueden actuar como `motor_activo` o `motor_auditor` si el usuario los designa explícitamente.
- `Roo` debe comportarse como motor general bajo el mismo contrato.
- Los modos nativos de Roo son solo una capa de producto; no redefinen `M0-M4` ni `F1-F10`.
- Los únicos roles operativos de la gobernanza son `motor_activo` y `motor_auditor`.

## 9) Rutas canónicas

- Gobernanza activa: `dev/`
- Guía breve de invocación humana del orquestador:
  `dev/policies/orchestrator_human_quickstart.md`
- Policy de capacidades por repo:
  `dev/policies/repo_capabilities_policy.md`
- Plantilla de perfil local de capacidades:
  `dev/templates/governance/repo_governance_profile.md`
- Perfil local instalado en cada repo consumidor:
  `dev/repo_governance_profile.md`
- Iniciativas: `dev/records/initiatives/<initiative_id>/`
- Handoff de apertura M4 pre-F1:
  `dev/records/initiatives/<initiative_id>/handoff.md`
- Validación real guiada F8:
  `dev/records/initiatives/<initiative_id>/real_validation.md`
- Runtime local del orquestador:
  `.orchestrator_local/`
- Bitácora diaria: `dev/records/bitacora/`
- Script oficial de bitácora: `scripts/ops/bitacora_append.py`
- Validadores de cierre:
  - `scripts/dev/check_naming_compliance.py`
  - `scripts/dev/check_state0.py`

## 9.1) Runtime operativo del orquestador

El runtime del orquestador no forma parte de la iniciativa ni del baseline
exportable. Vive fuera de los artefactos sustantivos y puede incluir:

- `sessions/`
- `prompts_rendered/`
- `phase_tickets/`
- `resume_packets/`
- `checkpoints/`
- `receipts/`

Su propósito es mantener continuidad, trazabilidad operativa y telemetría sin
invadir la autoría de los motores.

## 10) Contrato de bloqueo

Si falta contexto, evidencia o precondición, la IA debe:

1. Parar.
2. Declarar bloqueo con evidencia.
3. Proponer el siguiente paso mínimo seguro.
