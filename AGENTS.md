# Directrices Maestras Multi-IA

## 1) Fuente de verdad

Orden de precedencia:

1. `AGENTS.md`
2. `dev/workflow.md`
3. `dev/guarantees/*.md`
4. `dev/ai/adapters/*.md`
5. `dev/policies/*.md`
6. superficies nativas de producto (`.claude/*`, `CLAUDE.md` y equivalentes) como capa de compatibilidad/adaptacion

Si hay conflicto, prevalece el nivel superior.

## 2) Objetivo operativo

Trabajar con un proceso cerrado, repetible y auditable.
La gobernanza define como se procede; el codigo define sobre que se trabaja.

## 3) Modos M0-M4

- `M0 CONVERSACION`: ideacion, aclaraciones y discusion tecnica sin ejecucion.
- `M1 ANALISIS`: diagnostico tecnico sin cambios de codigo.
- `M2 DEBUG`: reproduccion y aislamiento de fallos sin implementar fix.
- `M3 IMPLEMENTACION_MENOR`: cambio acotado de bajo riesgo.
- `M4 INICIATIVA_COMPLETA`: cambio mediano/grande con trazabilidad formal.

Reglas de activacion:

- Si el usuario no declara modo, iniciar en `M0`.
- Para entrar en `M3` o `M4` se requiere aprobacion explicita del usuario.
- Toda transicion usa:
  `TRANSICION: Mx -> My | motivo | impacto | decision`.
- No existe motor por defecto.
- El usuario designa `motor_activo`.
- En `M4`, el usuario designa `motor_auditor` en `F2`.

## 4) Reglas duras no negociables

1. Si el usuario no declara modo, iniciar en `M0`.
2. Para entrar en `M3` o `M4` se requiere aprobacion explicita del usuario.
3. Toda transicion usa el formato `TRANSICION: Mx -> My | motivo | impacto | decision`.
4. En `M0/M1/M2` esta prohibido editar codigo.
5. En `M3` solo se permite cambio acotado y trazable.
6. En `M4` aplica pipeline `F1-F10` completo.
7. En `M4` no se planifica sin `ASK CONGELADO`.
8. En `M4` no se implementa sin `PLAN CONGELADO`.
9. Si cambia el alcance, se reabre la fase previa correspondiente.
10. Las auditorias formales solo admiten `PASS` o `FAIL`.
11. No se permite `PASS` mientras exista cualquier hallazgo pendiente.
12. En auditorias formales no existe categoria operativa de observaciones; todo punto senalado por el auditor debe registrarse como hallazgo o no incluirse.
13. No se permite `PASS` mientras exista cualquier punto senalado pendiente, ambiguedad material, debilidad operativa o riesgo descrito por el auditor.
14. Maximo 1 auditoria inicial y 2 re-auditorias por fase.
15. Un cambio logico por commit.
16. Prohibido refactor encubierto.
17. README solo incremental.
18. No inventar rutas, comandos o features.
19. Prohibido mezclar runtime del proyecto con artefactos de gobernanza.
20. Sin compliance de nomenclatura y state0 no hay cierre formal.
21. Toda capability transversal del sistema debe resolverse mediante abstraccion canonica, owner arquitectonico explicito, punto de extension definido y wiring comun.
22. Queda prohibido resolver capabilities transversales mediante branching por `tool`/`path`/`channel`/`filter`, coverage vertical aislada, paths paralelos, fallback legacy conviviendo con el camino canonico o logica especifica por herramienta.
23. Ninguna capability se considera completada mientras no este conectada en su wiring canonico sobre todas las superficies incluidas en alcance.
24. Queda prohibido cerrar una iniciativa con wiring parcial, integraciones huerfanas, convivencia legacy/canonico o paths paralelos para la misma capability.
25. En cada nueva iniciativa esta prohibido terminar con archivos brillantes, cableado mediocre o legacy vivo.
26. Si una iniciativa `M4` modifica comportamiento observable del producto, no puede cerrar `F8` ni avanzar a `F9` sin `real_validation.md` completado.
27. Durante la validacion real guiada no se toca codigo tras el primer fallo material, salvo bloqueo critico que impida continuar el barrido.

Reglas 28-37 son especificas del orquestador y viven en el repo Orquestador.

## 4.1) Apertura durable de M4

- `handoff.md` no puede nacer en `M0`; en `M0` no se crean artefactos.
- Tras la transicion `M0 -> M4`, y antes de `F1`, puede crearse
  `dev/records/initiatives/<initiative_id>/handoff.md`.
- `handoff.md` no sustituye `ask.md` ni `plan.md` y no redefine el pipeline
  `F1-F10`.
- Si existe `handoff.md`, `F1` debe derivar el `ask.md` desde ese artefacto.
- Si existe `handoff.md`, `F4` debe derivar el `plan.md` desde ese artefacto y
  desde el `ask.md` congelado.

## 5) Pipeline F1-F10

| Fase | Proposito |
| ---- | --------- |
| `F1` | Ask propuesto |
| `F2` | Validacion de ask por usuario + designacion de `motor_auditor` |
| `F3` | Auditoria y congelado de ask |
| `F4` | Plan propuesto |
| `F5` | Auditoria y congelado de plan |
| `F6` | Implementacion |
| `F7` | Post-auditoria / debug |
| `F8` | Validacion real guiada |
| `F9` | Docs + cierre |
| `F10` | Lecciones finales y feedback de gobernanza |

Reglas:

- En `F3`, `F5` y `F7` solo el `motor_auditor` emite la auditoria formal.
- Si el resultado es `FAIL`, no se avanza de fase.
- Si falta precondicion, el estado correcto es `BLOQUEADO`.
- Si existe `handoff.md`, se usa como fuente canonica de apertura de `M4`, pero
  la ejecutabilidad formal sigue dependiendo de `ask.md` y `plan.md`.
- `F8` es obligatoria cuando la iniciativa toca comportamiento observable del
  producto; si no aplica, debe trazarse como `NO_APLICA`.

## 5.0) Revision semanal canonica

La revision semanal es un control recurrente separado de `M0-M4`.
Policy operativa: `dev/policies/weekly_review_policy.md`

## 5.2) Propiedad de artefactos

- `F1`: `ask.md` lo escribe solo el `motor_activo`.
- `F3`: `ask_audit.md` lo escribe solo el `motor_auditor`.
- `F4`: `plan.md` lo escribe solo el `motor_activo`.
- `F5`: `plan_audit.md` lo escribe solo el `motor_auditor`.
- `F6`: `execution.md` lo escribe y mantiene solo el `motor_activo`.
- `F7`: `post_audit.md` lo escribe solo el `motor_auditor`.
- `F8`: `real_validation.md` lo escribe quien guia o ejecuta la validacion real.
- el orquestador no sustituye la autoria de los motores; coordina fases,
  gates, intentos, excepciones, tickets y contexto operativo.
- detalle operativo del orquestador:
  `dev/policies/orchestrator_execution_policy.md`

## 5.1) F8 — Validacion real guiada

`F8` formaliza el barrido real antes del cierre documental.

Reglas:

- no es una auditoria formal nueva
- su salida obligatoria es `real_validation.md` cuando aplica
- debe ejecutar el barrido real completo antes de decidir fixes
- si aparecen fallos materiales, corresponde reabrir `F6`
- si se reabre `F6`, deben repetirse `F7` y `F8` antes de `F9`
- solo puede avanzar a `F9` cuando `real_validation.md` declare
  `Decision final: APTA_PARA_F9`

## 6) Precedencia tecnica

1. MIT Concept-Sync para macroarquitectura.
2. Clean Code para microimplementacion.
3. Krug para UI, CLI, DX y respuestas orientadas a usuario.
4. Rendimiento puede excepcionar Clean Code solo en hot paths con evidencia.
5. Validacion determina aceptabilidad final.

## 7) Corpus de contexto

Toda consulta debe usar la capa canonica minima que la responda.
La memoria del chat no es fuente valida de continuidad.

Routing de detalle: `dev/policies/context_routing_policy.md`

### Gobernanza recuperable

Corpus canonico:

- `dev/policies/`
- `dev/guarantees/`
- `dev/prompts/`
- `dev/templates/initiative/`
- `dev/ai/adapters/`
- `dev/workflow.md`
- `doc/architecture/`

Exclusiones duras:

- `dev/records/` como historico
- `.claude/` y `CLAUDE.md` como corpus de retrieval

La recuperacion de gobernanza debe ser hibrida:

- filtro determinista por fase, tipo de documento y motor
- ranking semantico dentro del subconjunto
- fallback al documento canonico completo si hay ambiguedad
- herramienta operativa: `governance_search`

### SymDex

`SymDex` se usa solo para codigo vivo del producto.

Excluir: `node_modules`, `.venv`, `__pycache__`, caches, logs, `state`,
`sessions`, `content`, gobernanza y artefactos historicos.

Herramientas operativas (via symdex_code):
- `semantic_search`, `search_symbols`, `search_text`
- `get_symbol`, `get_file_outline`, `get_symbols`

`semantic_search` solo cuenta como capacidad real de busqueda conceptual si
el backend semantico esta validado en el perfil del repo.

### Memoria estructural persistente

Reservada para: call paths reales, blast radius, legacy y dead code,
arquitectura estructural, contraste entre wiring esperado y wiring real.

Cuando no este instalada, degrada a `SymDex` mas lectura canonica del repo.
Policy: `dev/policies/structural_memory_policy.md`

## 8) Motores

- `Codex`, `Claude` y `Gemini` pueden actuar como `motor_activo` o `motor_auditor` si el usuario los designa explicitamente.
- Los unicos roles operativos de la gobernanza son `motor_activo` y `motor_auditor`.

## 9) Rutas canonicas

- Gobernanza activa: `dev/`
- Iniciativas: `dev/records/initiatives/<initiative_id>/`
- Bitacora diaria: `dev/records/bitacora/`
- Script oficial de bitacora: `scripts/ops/bitacora_append.py`
- Validadores de cierre:
  - `scripts/dev/check_naming_compliance.py`
  - `scripts/dev/check_state0.py`
- Perfil local de capacidades:
  `dev/repo_governance_profile.md`

## 10) Contrato de bloqueo

Si falta contexto, evidencia o precondicion, la IA debe:

1. Parar.
2. Declarar bloqueo con evidencia.
3. Proponer el siguiente paso minimo seguro.
