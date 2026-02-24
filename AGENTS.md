# Directrices Maestras Multi-IA

Este archivo define las reglas universales para cualquier IA que trabaje en este repo:
- Codex
- Claude
- Gemini
- Roo Code

## 1) Fuente de verdad (orden de precedencia)

1. `AGENTS.md` (este archivo)
2. `dev/workflow.md`
3. `dev/guarantees/*.md`
4. Adaptadores por motor en `dev/ai/adapters/*.md`
5. Políticas transversales en `dev/policies/*.md`
6. Reglas de ejecución de la herramienta (por ejemplo `.roo/rules/*`)

Si hay conflicto, prevalece el nivel superior.

## 2) Objetivo operativo

Trabajar con un proceso cerrado, repetible y auditable.
Ninguna IA puede saltarse fases ni inventar rutas, artefactos o estados.

## 3) Estados operativos obligatorios (M0-M4)

- M0 `CONVERSACION`: ideación, aclaraciones y discusión técnica sin ejecución.
- M1 `ANALISIS`: diagnóstico de repo/sistema sin cambios de código.
- M2 `DEBUG`: reproducción y aislamiento de fallos sin implementar fix.
- M3 `IMPLEMENTACION_MENOR`: cambio acotado de bajo riesgo (un objetivo técnico pequeño).
- M4 `INICIATIVA_COMPLETA`: cambio mediano/grande con trazabilidad formal completa.

Activación por defecto:
- Si el usuario no declara modo, iniciar en `M1`.

Protocolo de transición:
- Formato obligatorio: `TRANSICION: Mx -> My | motivo | impacto | decision`.
- Para entrar en `M3` o `M4` se requiere aprobación explícita del usuario.
- Si sube alcance o riesgo durante `M3`, escalar a `M4`.
- Si faltan precondiciones, marcar `BLOQUEADO`.

Reglas duras por modo:
- `M0/M1/M2`: prohibido editar código.
- `M3`: permitido implementar cambio acotado, sin refactor encubierto.
- `M4`: aplica pipeline F1-F9 completo.

## 4) Pipeline oficial obligatorio (solo M4)

- F1: Ask propuesto
- F2: Validación de Ask (usuario)
- F2.5: Auditoría Codex de Ask
- F3: Ask congelado
- F4: Plan propuesto (Architect)
- F5: Auditoría Codex de Plan
- F6: Plan congelado
- F7: Implementación (Code)
- F8: Post-auditoría/Debug Codex
- F9: Docs + Cierre (Orchestrator)

Reglas duras:
- Prohibido implementar en `M4` sin `PLAN CONGELADO`.
- Prohibido planificar en `M4` sin `ASK CONGELADO`.
- Si cambia alcance, se reabre fase previa (F1 o F4).

## 5) Rutas canónicas de artefactos

Toda iniciativa vive en:

`dev/records/initiatives/<initiative_id>/`

Archivos estándar:
- `ask.md`
- `ask_audit.md`
- `plan.md`
- `plan_audit.md`
- `execution.md`
- `post_audit.md`
- `closeout.md`

`<initiative_id>` recomendado:
`YYYY-MM-DD_tema_corto`

## 6) Máquina de estados de documentos

Estados permitidos:
- `PROPUESTO`
- `VALIDADO`
- `CONGELADO`
- `BLOQUEADO`

Cada documento debe mostrar estado explícito y fecha.

## 7) Política de cambios

- 1 cambio lógico por commit.
- Prohibido refactor encubierto.
- README siempre incremental.
- No documentar rutas/comandos/features no verificables.
- Si falta evidencia, la IA debe bloquear y pedir aclaración.

## 8) Política de runbooks heredados

Cualquier runbook heredado debe estar etiquetado como:
- `APLICA`
- `PENDIENTE_ADAPTACION`
- `HEREDADO_NO_APLICA`

Los `HEREDADO_NO_APLICA` no pueden usarse como base operativa.

## 9) Rol de Codex en auditorías

Codex es auditor interno en `M4`:
- F2.5 (Ask audit)
- F5 (Plan audit)
- F8 (Post-audit/debug)

La auditoría debe listar hallazgos numerados con severidad, evidencia y decisión:
- `PASS`
- `PASS_WITH_OBSERVATIONS`
- `FAIL`

## 10) Bootstrap mínimo del repo

Todo entorno operativo debe tener:
- control de versiones (`git`)
- `.gitignore` con exclusiones de secretos/runtime
- trazabilidad de decisiones en `dev/logs/decisions.md`

## 11) Contrato de cumplimiento

Si una IA no puede cumplir una regla por falta de contexto o archivos, debe:
1. Parar.
2. Declarar bloqueo con evidencia.
3. Proponer siguiente paso mínimo seguro.

## 12) Reglas duras de documentación

Las reglas de documentación viven en:
- `dev/policies/documentation_rules.md`

Resumen no negociable:
- no inventar rutas/comandos/features
- README incremental
- separar plantilla (`dev/guarantees`) de historial (`dev/records`)

## 13) Reglas duras de scripts

Las reglas de scripts viven en:
- `dev/policies/scripts_rules.md`

Resumen no negociable:
- estructura por categorías (`dev`, `ops`, `migration`)
- paths robustos (independientes de `cwd`)
- wrappers de compatibilidad cuando haya movimiento de rutas

## 14) Bitácora automática de trabajo con IA

Las reglas de bitácora viven en:
- `dev/policies/bitacora_rules.md`

Resumen no negociable:
- un archivo diario por IA en `dev/records/bitacora/`
- registrar pregunta y respuesta por turno
- usar `scripts/ops/bitacora_append.py` tras cada respuesta final

## 15) Nomenclatura obligatoria

Las reglas de nomenclatura viven en:
- `dev/policies/naming_rules.md`

Validación oficial:
- `scripts/dev/check_naming_compliance.py`

Sin compliance de nomenclatura:
- no hay cierre formal de iniciativa

## 16) Estado 0 de organización

Reglas de layout:
- `dev/policies/repo_layout_rules.md`

Checklist operativo:
- `dev/checklists/state0.md`

Validación oficial:
- `scripts/dev/check_state0.py`

## 17) Separación obligatoria: proyecto Python vs gobernanza IA

Para cualquier trabajo asistido por IA en este repo:
- Directriz maestra: `AGENTS.md`
- Workflow operativo: `dev/workflow.md`
- Gates de proceso: `dev/guarantees/`
- Adaptadores por motor (Codex/Claude/Gemini/Roo): `dev/ai/adapters/`
- Bitácora diaria por IA: `dev/records/bitacora/` (script: `scripts/ops/bitacora_append.py`)

Regla dura:
- Prohibido mezclar código runtime del proyecto Python con artefactos de gobernanza.
- La gobernanza vive en `dev/` y sus subcarpetas; el runtime de la app no debe usarse para guardar reglas, gates, plantillas o bitácoras.
