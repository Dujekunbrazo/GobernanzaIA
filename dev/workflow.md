# Dev Workflow — SOP Operativo Multi-IA

Este documento define el proceso oficial de trabajo para cambios técnicos.
No define el runtime de la app; define la gobernanza de desarrollo.

## Fuente de verdad

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/*.md`
- `dev/ai/adapters/*.md`
- `dev/policies/*.md`

Si una capa difiere, se corrige en el mismo cambio.

Guia corta de invocacion humana del orquestador:

- `dev/policies/orchestrator_human_quickstart.md`
- `dev/policies/context_stack_policy.md`

## Roles operativos

- `motor_activo`: propone, planifica e implementa.
- `motor_auditor`: audita y decide `PASS` o `FAIL`.
- `orquestador`: coordina estado, gates, continuidad, esfuerzo, checkpoints y
  excepciones; no sustituye la autoría sustantiva de los motores.

No hay motores por defecto.
El usuario designa el motor según disponibilidad y contexto.

## Modos operativos

- `M0 CONVERSACION`: discusión y aclaración sin ejecución técnica.
- `M1 ANALISIS`: análisis técnico sin cambios de código.
- `M2 DEBUG`: diagnóstico sin fix.
- `M3 IMPLEMENTACION_MENOR`: cambio acotado y trazable.
- `M4 INICIATIVA_COMPLETA`: pipeline formal `F1-F10`.

Reglas:

- si el usuario no declara modo, iniciar en `M0`
- para pasar a `M3` o `M4`, se requiere aprobación explícita del usuario
- toda transición se registra como:
  `TRANSICION: Mx -> My | motivo | impacto | decision`
- en `M0/M1/M2` no se modifica código

## Artefactos por iniciativa

Ruta canónica:
`dev/records/initiatives/<initiative_id>/`

Cabecera mínima obligatoria:

- `Initiative ID`
- `Modo`
- `Estado`
- `Fecha`
- `motor_activo`
- `motor_auditor` (obligatorio en `M4`)
- `Rama`
- `baseline_mit`

Set mínimo:

- `M3`: `ask.md`, `execution.md`, `closeout.md`, `lessons_learned.md`
- `M4`: `ask.md`, `ask_audit.md`, `plan.md`, `plan_audit.md`, `execution.md`,
  `post_audit.md`, `closeout.md`, `lessons_learned.md`

Artefactos opcionales:

- `handoff.md`
- `baseline_freeze.md`
- `capability_closure.md`
- `exception_record.md`
- `real_validation.md`

## Propiedad de artefactos y runtime del orquestador

Reglas:

- el `motor_activo` escribe `ask.md`, `plan.md`, `execution.md` y, cuando
  corresponda, `real_validation.md`
- el `motor_auditor` escribe `ask_audit.md`, `plan_audit.md` y `post_audit.md`
- el orquestador no redacta el contenido sustantivo de esos artefactos
- el orquestador puede reparar formato o metadata solo ante fallo mecánico y
  con trazabilidad explícita
- la continuidad de trabajo no depende del chat; toda reentrada debe usar:
  - `phase_ticket`
  - `resume_packet`

Runtime local del orquestador:

- `.orchestrator_local/`

Contenido típico:

- `sessions/`
- `phase_tickets/`
- `resume_packets/`
- `checkpoints/`
- `receipts/`

Ese runtime no forma parte de la iniciativa ni del baseline exportable.

## Gobernanza ejecutiva del orquestador

El orquestador es la capa ejecutiva del sistema.

Responsabilidades:

- abrir y retomar sesiones
- determinar fase efectiva y siguiente paso permitido
- verificar precondiciones mecánicas
- emitir `phase_ticket` y `resume_packet`
- registrar intents, receipts, errores y checkpoints
- preparar `F8` y la continuidad operativa entre chats

Límites:

- no redacta artefactos sustantivos de fase
- no sustituye auditoría formal
- no reinterpreta alcance por su cuenta
- no convierte ausencia de evidencia en validación implícita

Referencia:

- `dev/policies/orchestrator_execution_policy.md`

## Stack canónico de contexto

Capas:

1. `gobernanza normativa`
   - reglas, workflow, guarantees, policies, templates y adapters
2. `gobernanza ejecutiva del orquestador`
   - fase vigente, reentrada, tickets, checkpoints, excepciones y límites
3. `código vivo local`
   - lectura fina de símbolos y bloques
4. `memoria estructural persistente`
   - wiring global, impacto, legacy y arquitectura estructural
5. `evidencia runtime real`
   - chat del producto, `trace on`, terminal, logs y resultados visibles

Reglas:

- cada consulta debe usar la capa mínima que la responda de forma canónica
- la memoria del chat no es una fuente válida de continuidad operativa
- ninguna capa puede actuar como vía primaria paralela de otra
- si la capa estructural canónica no está disponible, se degrada de forma
  explícita; no se simula como si existiera

## Protocolo operativo M3

Objetivo:
- ejecutar un cambio acotado y trazable sin abrir pipeline `F1-F10`.

Secuencia mínima:
1. `ask.md` con alcance, no-alcance, evidencia y criterio de aceptación.
2. `scripts/dev/initiative_preflight.py` antes de implementación o cierre.
3. Implementación acotada con registro en `execution.md`.
4. Validación de entrega mediante `dev/guarantees/m3_delivery_gate.md`.
5. Cierre en `closeout.md` y `lessons_learned.md`.

Reglas:
- `M3` no autoriza refactor estructural encubierto.
- Si el cambio toca una capability transversal, `M3` exige el mismo estándar
  de abstracción canónica, owner arquitectónico, wiring común, capability
  closure y retiro de legacy que `M4`.
- Si el cambio toca una capability transversal, `M3` debe registrar
  `capability_closure.md` y validar su consistencia con
  `scripts/dev/check_capability_closure.py`.
- Si el cambio requiere excepción formal, `M3` debe registrar
  `exception_record.md` y cumplir `dev/policies/exception_rules.md`.
- En `M3` no se puede cerrar una capability con wiring parcial, integraciones
  huérfanas, coverage vertical aislada o paths paralelos.
- Antes de implementar o cerrar una iniciativa formal, ejecutar
  `scripts/dev/initiative_preflight.py`.
- Si durante `M3` el alcance deja de ser acotado o exige plan multi-commit con
  auditoría formal, corresponde transición a `M4`.

## Apertura durable de M4

Tras la transición `M0 -> M4`, y antes de `F1`, puede existir un artefacto
opcional de apertura de iniciativa:

- `dev/records/initiatives/<initiative_id>/handoff.md`

Propósito:

- persistir el análisis y la planificación previa generados en conversación o
  en modos de producto antes de abrir la fase Ask
- evitar que el plan preliminar quede solo en chat
- servir como fuente canónica para derivar `ask.md` y `plan.md`

Reglas:

- en `M0` no se crean artefactos de iniciativa
- `handoff.md` nace ya dentro de `M4`, antes de `F1`
- `handoff.md` es el artefacto primogénito opcional de apertura de una
  iniciativa `M4`
- no sustituye `ask.md` ni `plan.md`
- no autoriza planificar ni implementar fuera de `F1-F10`
- si existe, `F1` debe derivar el Ask desde ese artefacto
- si existe, `F4` debe derivar el Plan desde ese artefacto y justificar
  cualquier delta material respecto al handoff

## Pipeline oficial M4

### F1 — Ask propuesto

- salida: `ask.md` en `PROPUESTO`
- gate: `dev/guarantees/ask_gate.md`
- si existe `handoff.md`, `ask.md` deriva de ese artefacto y preserva
  evidencia, supuestos, preguntas y trade-offs relevantes

### F2 — Validación usuario

- validar alcance, supuestos y preguntas bloqueantes
- designar `motor_auditor`
- salida: `ask.md` en `VALIDADO` o `BLOQUEADO`

### F3 — Auditoría + congelado de ask

- audita el `motor_auditor`
- salida:
  - `ask_audit.md`
  - `ask.md` en `CONGELADO` si hay `PASS`

### F4 — Plan propuesto

Prerequisito:
- `ask.md` en `CONGELADO`

Salida:
- `plan.md` en `PROPUESTO`
- etiqueta `PENDIENTE DE AUDITORIA DEL MOTOR_AUDITOR`
- si existe `handoff.md`, `plan.md` debe conservar su planificación útil y
  explicar cualquier delta material respecto al handoff
- si el plan toca una capability transversal, debe existir
  `capability_closure.md`

Gate:
- `dev/guarantees/plan_gate.md`

### F5 — Auditoría + congelado de plan

- audita el `motor_auditor`
- salida:
  - `plan_audit.md`
  - `plan.md` en `CONGELADO` si hay `PASS`

### F6 — Implementación

Prerequisito:
- `plan.md` en `CONGELADO`
- `scripts/dev/initiative_preflight.py` ejecutado

Salida:
- `execution.md`

Restricciones:

- un cambio lógico por commit
- prohibido refactor encubierto
- prohibido alcance fuera del plan congelado
- `execution.md` lo actualiza el `motor_activo`
- si la ejecución es larga, multi-commit o de alto riesgo, `F6` pasa a modo
  supervisado por commit
- en `F6` supervisada, el orquestador libera un solo tramo cada vez
- el `motor_auditor` puede emitir `execution_checkpoint.md` lateral antes de
  liberar el siguiente tramo

### F7 — Post-auditoría / Debug

- audita el `motor_auditor`
- salida:
  - `post_audit.md`
  - decisión `PASS` o `FAIL`
- si existe `handoff.md`, puede usarse como referencia de intención original,
  pero el criterio formal de ejecución sigue siendo `plan.md` congelado
- si la initiative tocó una capability transversal, `post_audit.md` y
  `closeout.md` deben ser consistentes con `capability_closure.md`

### F8 — Validación real guiada

Aplica cuando la iniciativa modifica comportamiento observable del producto,
UX verificable en ejecución o integración real que deba probarse en Kiminion
o superficie equivalente.

Salida:
- `real_validation.md`

Objetivo:
- ejecutar un barrido real completo antes de volver a tocar código
- consolidar todos los hallazgos de pruebas reales en un único artefacto
- decidir con evidencia si la iniciativa está apta para `F9` o si debe
  reabrirse `F6`

Reglas:

- no es una auditoría formal nueva; no emite `PASS` o `FAIL`
- si no aplica, debe trazarse explícitamente como `NO_APLICA`
- el `motor_activo` prepara el script de pruebas real usando
  `dev/prompts/real_validation.md`
- el motor entra en `F8` con `phase_ticket` y `resume_packet`; no depende de
  memoria conversacional previa
- cada caso probado debe registrar:
  - frase o acción
  - criterio o CA cubierto
  - esperado
  - observado
  - resultado `PASS` / `FAIL` / `BLOQUEADO`
  - evidencia de logs, traces o resultados visibles
- las fuentes de evidencia de primer nivel son:
  - chat del producto
  - `trace on`
  - terminal y logs de la superficie validada
  - resultados visibles en runtime real
- durante el barrido no se modifica código tras el primer fallo material,
  salvo bloqueo crítico que impida seguir
- si hay fallos materiales, se consolida el artefacto y se reabre `F6`
- si tras la reapertura hay cambios, deben repetirse `F7` y `F8` antes de `F9`
- `F9` solo puede empezar cuando `real_validation.md` declare
  `Decisión final: APTA_PARA_F9`

### F9 — Docs + cierre

- actualizar docs incrementalmente
- confirmar gates en verde
- ejecutar cierre conforme a `dev/policies/git_workflow_rules.md`

Salida:
- `closeout.md`

### F10 — Lecciones finales

Salida:
- `lessons_learned.md`

## Reglas de auditoría formal

Aplica a `F3`, `F5` y `F7`.

Reglas:

- solo existen `PASS` y `FAIL`
- no se permite `PASS` con hallazgos pendientes
- solo cuentan como `hallazgos` los problemas materiales para:
  - mandato de la fase
  - consistencia de fuentes canónicas
  - ejecutabilidad real
  - validación
  - seguridad
  - cierre real de fase
- en auditorías formales no se usa la categoría `observaciones`
- toda debilidad, riesgo, ambigüedad material o recomendación correctiva debe
  registrarse como `hallazgo`
- si un punto no merece convertirse en hallazgo, no debe aparecer en la
  auditoría formal
- un `PASS` debe justificar explícitamente por qué no existe ningún hallazgo
  material ni pendiente
- la auditoría formal debe dejar `## Escalado de remediacion` con motor,
  esfuerzo sugerido y motivo
- máximo 1 auditoría inicial y 2 re-auditorías por fase
- en re-auditoría no se permite goteo de hallazgos nuevos salvo por cambios
  nuevos o evidencia antes no visible

## Esfuerzo adaptativo

El orquestador traduce la salida del auditor a profundidad operativa del
`motor_activo`.

Escala recomendada para `Claude Opus`:

- `medium`: corrección local, claridad, pequeño hueco de evidencia
- `high`: remediación multiarchivo o integración acotada
- `max`: wiring canónico, capability transversal, comportamiento observable,
  legacy/canónico, excepción final o última re-auditoría

Reglas:

- si la auditoría formal fija `Esfuerzo sugerido`, el orquestador debe
  respetarlo salvo excepción trazada
- si una fase entra en excepción final o reapertura crítica, `max` pasa a ser
  el valor por defecto

## Reglas no negociables

1. En `M4`, no planificar sin `ASK CONGELADO`.
2. En `M4`, no implementar sin `PLAN CONGELADO`.
3. Un cambio lógico por commit.
4. README solo incremental.
5. No inventar rutas/comandos/features.
6. Si falta precondición, bloquear avance con evidencia.
7. En `M0/M1/M2`, no se modifica código.
8. No se permite cerrar una fase con hallazgos pendientes.
9. En auditorías formales no se permiten observaciones como categoría aparte; todo punto operativo debe quedar absorbido en hallazgos o eliminarse.
10. `Roo` no define workflow propio por encima del contrato canónico.
11. En `M3` y `M4`, toda capability transversal debe cerrar con wiring canónico completo, sin convivencia legacy/canónico y sin branching oportunista.
12. En toda nueva iniciativa está prohibido cerrar con archivos brillantes, cableado mediocre o legacy vivo; el cierre visible debe coincidir con el wiring real y con el retiro efectivo de caminos paralelos e integraciones huérfanas.

## Contexto y recuperación

### Capa estática

Siempre presente:

- reglas duras
- resumen de pipeline
- precedencia técnica
- instrucciones de recuperación

### Gobernanza recuperable

Usar recuperación híbrida sobre:

- `dev/policies/`
- `dev/guarantees/`
- `dev/prompts/`
- `dev/templates/initiative/`
- `dev/ai/adapters/`
- `doc/architecture/`

Excluir:

- `dev/records/`
- `.roo/`
- legacy y salidas generadas

Uso operativo:

- consultar primero `dev/policies/governance_manifest.md` para routing de carga
  mínima cuando la tarea sea de gobernanza o exista ambigüedad de contexto
- consultar `governance_search` para workflow, gates, prompts, templates,
  adapters y arquitectura
- usar runtime del orquestador para fase vigente, reentrada, checkpoints,
  intentos y excepciones
- aplicar primero filtros por `phase`, `document_type` y `motor` cuando
  existan
- si la recuperación devuelve ambigüedad, cargar el documento canónico por ruta

### SymDex

Usar `SymDex` solo para código vivo:

- `core/`
- `integrations/MCP-Microsoft-Office/src/`
- `scripts/`
- `tests/`
- `manifests/`

Excluir:

- `node_modules`
- caches
- logs
- `state`
- `sessions`
- `content`
- gobernanza

Uso operativo:

- consultar `semantic_search` (via symdex_code) para localizar código vivo por intención,
  símbolo o runtime
- consultar `get_symbol` (via symdex_code) para leer el bloque concreto después de la
  búsqueda
- no usar `SymDex` para workflow, policies, logs, records o bitácora

### Memoria estructural persistente

Uso operativo:

- reservar esta capa para:
  - wiring global
  - impact analysis
  - blast radius
  - legacy y dead code
  - arquitectura estructural
- cuando la capacidad no exista, degradar a `SymDex` más lectura canónica
- cuando exista, usarla como vía estructural primaria y no como ayuda lateral

### Evidencia runtime real

Uso operativo:

- usar esta capa para `F8` y para cualquier validación observable del producto
- las fuentes de primer nivel son:
  - chat del producto
  - `trace on`
  - terminal o logs reales
  - resultados visibles en runtime
- si falta evidencia donde aplica, bloquear avance formal

## Gobernanza de ingeniería

Referencia corta:
- `dev/policies/ai_engineering_governance.md`

Referencia larga:
- `doc/architecture/ai_engineering_dossier.md`

Precedencia técnica:
1. MIT
2. Clean Code
3. Krug
4. Rendimiento con evidencia
5. Validación

## Controles operativos

- Bitácora: `scripts/ops/bitacora_append.py`
- Naming: `scripts/dev/check_naming_compliance.py`
- State0: `scripts/dev/check_state0.py`
- Decisiones: `dev/logs/decisions.md`
