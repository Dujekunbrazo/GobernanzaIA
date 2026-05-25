# Adapter - <NOMBRE_MOTOR>

Adapter por motor concreto para la gobernanza canonica del kit. Solo afina
detalles de producto del motor; **no crea workflow ni routing paralelos al
canon**. Si una capability esta migrada a `dev/skills/`, la Skill canonica
tiene precedencia operativa sobre lo que diga este adapter
(AGENTS.md §1 Carveout operativo).

## 1. Identidad del motor

- `motor`: <nombre_motor>            (ej. `claude`, `codex`, `gemini`, `kimi`)
- `vendor`: <vendor>                 (ej. `Anthropic`, `OpenAI`, `Google`, `Moonshot`)
- `rol_principal`: `motor_activo` | `motor_auditor`
- `installation_profile`: ver `dev/governance_baseline.json`

## 2. Modelos disponibles

Describe los modelos concretos del motor que se usan en este repo y para
que fase:

- planificacion (F1, M0 estrategico): <modelo>
- implementacion (F3): <modelo>
- auditoria (F2, F4): <modelo>
- validacion real (F5): <modelo>
- cierre (F6, F7): <modelo>
- weekly factual (W1): <modelo>
- weekly estrategico (W2): <modelo>

Si el motor solo expone un modelo unificado, declarar `unificado` y dejar
el resto en `n/a`.

## 3. Continuidad durable

- `mecanismo`: <describe el mecanismo concreto si lo tiene>
  (memoria persistente, contexto extendido, RAG nativo, ninguno, etc.)
- `aplica_a_handoffs`: `si` | `no`
- `aplica_a_iniciativa_completa`: `si` | `no`
- `degradacion_si_falla`: <fallback>

## 4. Routing MCP soportado

Declara compatibilidad real verificada con los MCPs canonicos del kit:

- `governance_search`: `SI` | `NO` | `PARCIAL`
- `symdex_code`:        `SI` | `NO` | `PARCIAL`
- `symdex_code.semantic_search`: `SI` | `NO` | `PARCIAL`
- `codebase-memory-mcp`: `SI` | `NO` | `PARCIAL`

Si alguno marca `NO` o `PARCIAL`, declarar la degradacion canonica en §6.

## 5. Convenciones operativas

- como este motor carga `AGENTS.md` al inicio de sesion (mecanismo concreto)
- como declara `TRANSICION: Mx -> My`
- formato preferido de chat (idioma, registro, longitud)
- restricciones de tooling especificas del motor (rate limits, costes,
  formato de salida, etc.)

## 6. Excepciones y afinaciones

Lista cerrada de excepciones aceptadas para este motor concreto. Cada
excepcion debe:

- referir el canon del que se desvia (regla, fase, policy)
- justificar la razon tecnica de la desviacion
- definir un criterio binario para revertir la excepcion cuando el motor
  evolucione

Ejemplo:

| # | Canon | Excepcion | Razon | Revertir cuando |
| - | ----- | --------- | ----- | --------------- |
| 1 | <regla> | <que se desvia> | <por que> | <criterio binario> |

## 7. Fallbacks declarados

- si `governance_search` no esta disponible:
  - <fallback concreto>
- si `symdex_code` no esta disponible:
  - <fallback>
- si `codebase-memory-mcp` no esta disponible:
  - <fallback>
- si el motor pierde contexto largo:
  - <fallback>

## 8. Notas

- Este adapter no redefine el workflow canonico ni el routing MCP canonico.
- Cualquier ajuste estructural debe entrar via iniciativa M4 sobre el kit,
  no via este adapter.
- Si una capacidad cubierta aqui se migra a `dev/skills/`, este adapter
  debe quedar reducido a lo que la Skill no cubra.
