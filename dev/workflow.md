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

## Roles operativos

- `motor_activo`: propone, planifica e implementa.
- `motor_auditor`: audita y decide `PASS` o `FAIL`.

No hay motores por defecto.
El usuario designa el motor según disponibilidad y contexto.

## Modos operativos

- `M0 CONVERSACION`: discusión y aclaración sin ejecución técnica.
- `M1 ANALISIS`: análisis técnico sin cambios de código.
- `M2 DEBUG`: diagnóstico sin fix.
- `M3 IMPLEMENTACION_MENOR`: cambio acotado y trazable.
- `M4 INICIATIVA_COMPLETA`: pipeline formal `F1-F9`.

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

## Protocolo operativo M3

Objetivo:
- ejecutar un cambio acotado y trazable sin abrir pipeline `F1-F9`.

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
- no autoriza planificar ni implementar fuera de `F1-F9`
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

### F7 — Post-auditoría / Debug

- audita el `motor_auditor`
- salida:
  - `post_audit.md`
  - decisión `PASS` o `FAIL`
- si existe `handoff.md`, puede usarse como referencia de intención original,
  pero el criterio formal de ejecución sigue siendo `plan.md` congelado
- si la initiative tocó una capability transversal, `post_audit.md` y
  `closeout.md` deben ser consistentes con `capability_closure.md`

### F8 — Docs + cierre

- actualizar docs incrementalmente
- confirmar gates en verde
- ejecutar cierre conforme a `dev/policies/git_workflow_rules.md`

Salida:
- `closeout.md`

### F9 — Lecciones finales

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
- los problemas editoriales o cosméticos sin impacto material deben ir a
  `observaciones`
- las `observaciones` no bloquean el `PASS`
- máximo 1 auditoría inicial y 2 re-auditorías por fase
- en re-auditoría no se permite goteo de hallazgos nuevos salvo por cambios
  nuevos o evidencia antes no visible

## Reglas no negociables

1. En `M4`, no planificar sin `ASK CONGELADO`.
2. En `M4`, no implementar sin `PLAN CONGELADO`.
3. Un cambio lógico por commit.
4. README solo incremental.
5. No inventar rutas/comandos/features.
6. Si falta precondición, bloquear avance con evidencia.
7. En `M0/M1/M2`, no se modifica código.
8. No se permite cerrar una fase con hallazgos pendientes.
9. Las observaciones no sustituyen a los hallazgos.
10. `Roo` no define workflow propio por encima del contrato canónico.
11. En `M3` y `M4`, toda capability transversal debe cerrar con wiring canónico completo, sin convivencia legacy/canónico y sin branching oportunista.

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
- aplicar primero filtros por `phase`, `document_type` y `motor` cuando
  existan
- si la recuperación devuelve ambigüedad, cargar el documento canónico por ruta

### SymDex

Usar `SymDex` solo para código vivo:

- `src/`
- `core/`
- `app/`
- `packages/`
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

- consultar `symdex_search_code` para localizar código vivo por intención,
  símbolo o runtime
- consultar `symdex_read_code` para leer el bloque concreto después de la
  búsqueda
- no usar `SymDex` para workflow, policies, logs, records o bitácora

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
