# Directrices Maestras Multi-IA

## 1) Fuente de verdad

Orden de precedencia:

1. `AGENTS.md`
2. `dev/workflow.md`
3. `dev/guarantees/*.md`
4. `dev/ai/adapters/*.md`
5. `dev/policies/*.md`
6. superficies nativas de producto (`CLAUDE.md`, `.claude/*` y equivalentes)
   como capa de compatibilidad

Si hay conflicto, prevalece la capa superior.

## 2) Objetivo operativo

Trabajar en cada repo con un proceso simple, repetible y auditable para motores
directos.

La gobernanza define como se procede.
El codigo define sobre que se trabaja.

## 3) Motores directos

- `Claude` y `Codex` deben trabajar con la misma gobernanza sustantiva.
- `AGENTS.md` es el contrato compartido real para ambos.
- Los adapters por motor solo pueden afinar detalles de producto; no deben
  crear workflow ni routing paralelos.
- No existe motor por defecto.
- El usuario designa `motor_activo` y, cuando aplique, `motor_auditor`.

## 4) Modos M0-M4

- `M0 CONVERSACION`: ideacion, aclaraciones y discusion tecnica sin ejecucion.
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

## 5) Reglas duras no negociables

1. En `M3` solo se permite cambio acotado y trazable.
2. En `M4` aplica el pipeline `F1-F10`.
3. En `M4` no se planifica sin `ASK CONGELADO`.
4. En `M4` no se implementa sin `PLAN CONGELADO`.
5. Las auditorias formales solo admiten `PASS` o `FAIL`.
6. No se permite `PASS` mientras exista cualquier hallazgo pendiente.
7. Si cambia el alcance, se reabre la fase previa correspondiente.
8. Un cambio logico por commit.
9. Prohibido refactor encubierto.
10. README solo incremental.
11. No inventar rutas, comandos o features.
12. Prohibido mezclar runtime del proyecto con artefactos de gobernanza.
13. Toda consulta debe rutearse a la capa canonica minima que la responda.
14. Queda prohibido usar dos capas primarias simultaneas para la misma
    responsabilidad.
15. La memoria estructural del sistema debe resolverse mediante la capa
    estructural canonica cuando este disponible.
16. Toda capability transversal debe resolverse mediante abstraccion canonica,
    owner explicito, punto de extension definido y wiring comun.
17. Queda prohibido cerrar una capability con wiring parcial, integraciones
    huerfanas, coexistencia legacy/canonica o paths paralelos.
18. La validacion observable no se inventa: si falta evidencia real donde
    aplica, el estado correcto es `BLOQUEADO`.
19. Si una iniciativa modifica comportamiento observable del producto, no puede
    cerrar sin validacion real completada.
20. La gobernanza debe optimizar coste total por tarea usando retrieval
    dirigido, no expansion masiva de contexto.

## 6) Pipeline F1-F10

| Fase | Proposito |
| ---- | --------- |
| `F1` | Ask propuesto |
| `F2` | Validacion de ask por usuario |
| `F3` | Auditoria y congelado de ask |
| `F4` | Plan propuesto |
| `F5` | Auditoria y congelado de plan |
| `F6` | Implementacion |
| `F7` | Post-auditoria / debug |
| `F8` | Validacion real guiada |
| `F9` | Docs + cierre |
| `F10` | Lecciones finales |

Reglas:

- en `F3`, `F5` y `F7` solo el `motor_auditor` emite la auditoria formal
- si el resultado es `FAIL`, no se avanza de fase
- si falta precondicion, el estado correcto es `BLOQUEADO`
- `F8` es obligatoria cuando la iniciativa toca comportamiento observable del
  producto; si no aplica, debe trazarse como `NO_APLICA`

## 7) Validacion real F8

`F8` formaliza el barrido real antes del cierre documental.

Reglas:

- su salida obligatoria es `real_validation.md` cuando aplica
- debe ejecutar el barrido real completo antes de decidir fixes
- si aparecen fallos materiales, corresponde reabrir `F6`
- si se reabre `F6`, deben repetirse `F7` y `F8` antes de `F9`
- `F9` solo puede empezar cuando `real_validation.md` declare
  `Decision final: APTA_PARA_F9`
- la evidencia de primer nivel incluye:
  - chat del producto
  - `trace on`
  - terminal o logs de la superficie validada
  - resultados visibles en runtime real

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
- `dev/prompts/`
- `dev/templates/initiative/`
- `dev/ai/adapters/`
- `dev/repo_governance_profile.md`
- `doc/architecture/`

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

Routing por responsabilidad:

- gobernanza -> `governance_search`
- codigo vivo -> `symdex_code`
- wiring, impacto estructural, blast radius, hubs, legacy y dead code ->
  `codebase-memory-mcp`

Reglas:

- usar `semantic_search` solo si la capacidad semantica de `SymDex` esta
  validada en el repo
- si no lo esta, degradar a `search_symbols` y `search_text`
- usar `codebase-memory-mcp` para localizar relaciones y volver a
  `symdex_code` para leer fino el codigo exacto
- `Glob`, `Grep`, `find`, `rg`, `Read` o `Bash` solo se permiten como fallback
  si el MCP correspondiente falla o no esta disponible, o para lectura final
  puntual del archivo ya localizado

## 11) Perfil local de capacidades

Cada repo consumidor debe mantener un unico perfil local en:

- `dev/repo_governance_profile.md`

Ese perfil:

- describe tooling realmente disponible
- declara el estado real de `governance_search`, `symdex_code` y
  `codebase-memory-mcp`
- fija degradaciones aceptables
- no redefine el canon

## 12) Rutas canonicas

- gobernanza activa: `dev/`
- workflow de referencia: `dev/workflow.md`
- perfil local: `dev/repo_governance_profile.md`
- iniciativas: `dev/records/initiatives/<initiative_id>/`
- validacion real guiada: `dev/records/initiatives/<initiative_id>/real_validation.md`
- validadores de cierre:
  - `scripts/dev/check_naming_compliance.py`
  - `scripts/dev/check_state0.py`

## 13) Contrato de bloqueo

Si falta contexto, evidencia o precondicion, la IA debe:

1. parar
2. declarar bloqueo con evidencia
3. proponer el siguiente paso minimo seguro
