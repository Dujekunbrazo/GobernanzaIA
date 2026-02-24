# Dev Workflow — SOP Operativo (Codex Auditor Interno)

Este documento define el proceso oficial de trabajo para cambios técnicos.
No define comportamiento del runtime de la app; solo define gobernanza de desarrollo.

## Fuente de verdad

- `AGENTS.md` (contrato universal multi-IA)
- `dev/workflow.md` (este documento)
- `dev/guarantees/*.md` (gates)
- `dev/policies/*.md` (reglas duras transversales)

Si alguna capa de herramienta (Roo, Claude, etc.) difiere, se corrige en el mismo cambio.

## Roles

- Ask: análisis, evidencia, preguntas y recomendación.
- Architect: plan técnico commit por commit.
- Code: implementación estricta sobre plan congelado.
- Codex Auditor: auditoría interna en F2.5, F5 y F8.
- Documentation Writer: actualización incremental de documentación.
- Orchestrator: verificación de fases/gates y cierre formal.

## Modos operativos

- `M0 CONVERSACION`: discusión/ideación sin ejecución técnica.
- `M1 ANALISIS`: análisis técnico sin cambios de código.
- `M2 DEBUG`: diagnóstico y reproducción de fallos sin aplicar fixes.
- `M3 IMPLEMENTACION_MENOR`: cambio acotado de bajo riesgo.
- `M4 INICIATIVA_COMPLETA`: pipeline formal F1-F9.

Reglas de activación:
- si no se declara modo, iniciar en `M1`.
- para pasar a `M3` o `M4` se requiere aprobación explícita del usuario.
- las transiciones se registran con formato: `TRANSICION: Mx -> My | motivo | impacto | decision`.

Reglas duras por modo:
- `M0/M1/M2`: prohibido editar código.
- `M3`: implementación permitida solo para alcance acotado y trazable.
- `M4`: aplica F1-F9 completo y sus gates.

## Estructura de artefactos por iniciativa

Cada iniciativa usa un ID único:
`YYYY-MM-DD_tema_corto`

Ruta canónica:
`dev/records/initiatives/<initiative_id>/`

Archivos estándar:
- `ask.md`
- `ask_audit.md`
- `plan.md`
- `plan_audit.md`
- `execution.md`
- `post_audit.md`
- `closeout.md`

## Pipeline oficial (solo M4)

### F1 — Ask Propuesto

Entrada obligatoria:
- seed plan inicial (usuario + asistente)
- evidencia mínima del repo (código/docs/logs)

Salida:
- `ask.md` con estado `PROPUESTO`

Gate:
- `dev/guarantees/ask_gate.md`

### F2 — Ask Validación (Usuario)

Objetivo:
- validar alcance, supuestos y preguntas bloqueantes

Salida:
- `ask.md` actualizado con estado `VALIDADO` o `BLOQUEADO`

### F2.5 — Auditoría Codex de Ask

Objetivo:
- revisar consistencia, huecos y riesgos antes de congelar

Salida:
- `ask_audit.md` con resultado `PASS`, `PASS_WITH_OBSERVATIONS` o `FAIL`

Regla:
- si `FAIL`, no se puede avanzar a F3

### F3 — Ask Congelado

Objetivo:
- consolidar versión final del Ask

Salida:
- `ask.md` en estado `CONGELADO`

Regla:
- cualquier cambio de alcance reabre F1

### F4 — Plan Propuesto (Architect)

Prerequisito:
- `ask.md` en `CONGELADO`

Salida:
- `plan.md` con estado `PROPUESTO`
- etiqueta obligatoria: `PENDIENTE DE AUDITORÍA CODEX`

Gate:
- `dev/guarantees/plan_gate.md`

### F5 — Auditoría Codex de Plan

Objetivo:
- detectar inconsistencias técnicas, riesgos de regresión y complejidad innecesaria

Salida:
- `plan_audit.md` con resultado `PASS`, `PASS_WITH_OBSERVATIONS` o `FAIL`

Regla:
- si `FAIL`, no se puede avanzar a F6

### F6 — Plan Congelado

Objetivo:
- congelar plan final tras auditoría

Salida:
- `plan.md` en estado `CONGELADO`

Regla:
- cualquier cambio posterior reabre F4

### F7 — Implementación (Code)

Prerequisito:
- `plan.md` en `CONGELADO`

Salida:
- `execution.md` con commits ejecutados, validaciones y evidencias

Gate:
- `dev/guarantees/implementation_gate.md`

Restricciones:
- 1 cambio lógico por commit
- prohibido refactor encubierto
- prohibido alcance fuera de plan congelado

### F8 — Post-auditoría/Debug Codex

Objetivo:
- verificar comportamiento real vs plan congelado
- detectar bugs/regresiones/tests faltantes

Salida:
- `post_audit.md` con hallazgos numerados por severidad
- decisión `PASS`, `PASS_WITH_OBSERVATIONS` o `FAIL`

Regla:
- si `FAIL`, no se cierra y se programan fixes atómicos

### F9 — Docs + Cierre (Orchestrator)

Objetivo:
- actualizar docs incrementalmente
- confirmar gates en verde y cerrar iniciativa

Salida:
- `closeout.md` con trazabilidad completa de fases

Gate:
- `dev/guarantees/docs_gate.md`

## Reglas no negociables

1. En `M4`, no implementar sin `PLAN CONGELADO`.
2. En `M4`, no planificar sin `ASK CONGELADO`.
3. Un cambio lógico por commit.
4. README solo incremental.
5. No inventar rutas/comandos/features.
6. Si falta precondición, bloquear avance con evidencia.
7. Runbooks heredados no aplicables quedan fuera del flujo operativo.
8. En `M0/M1/M2`, no se modifica código.

## Python en Windows

Orden obligatorio:
- usar `.venv\Scripts\python.exe` si existe
- si no existe, usar `py -3`
- usar `python` solo si está validado en la sesión

## Registro de decisiones

Toda decisión de diseño/proceso debe registrarse en:
`dev/logs/decisions.md`

## Políticas complementarias obligatorias

- Documentación: `dev/policies/documentation_rules.md`
- Scripts: `dev/policies/scripts_rules.md`
- Bitácora IA: `dev/policies/bitacora_rules.md`
- Nomenclatura: `dev/policies/naming_rules.md`
- Layout repo: `dev/policies/repo_layout_rules.md`

## Registro continuo de conversación IA

Además de F1-F9, todo turno de trabajo con IA debe registrarse en:
`dev/records/bitacora/YYYY-MM-DD_<ia>.md`

Mecanismo oficial:
- `scripts/ops/bitacora_append.py`

## Control de nomenclatura

Validación obligatoria antes de cierre:
- `scripts/dev/check_naming_compliance.py`

## Control de estado 0

Checklist:
- `dev/checklists/state0.md`

Validación obligatoria antes de cierre:
- `scripts/dev/check_state0.py`
