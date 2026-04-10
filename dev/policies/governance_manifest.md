# Governance Manifest (Hard)

Proposito:
- minimizar carga de contexto sin perder enforcement
- fijar la estrategia de carga minima para motores directos
- reflejar el workflow canonico real del repo

## 1) Regla de carga minima

- cargar por defecto solo:
  - `AGENTS.md`
  - `dev/workflow.md` cuando haga falta detalle de proceso
  - un gate relevante
  - una policy de soporte relevante
- no cargar mas de `1 workflow + 1 gate + 1 policy de soporte` salvo ambiguedad
  real

## 2) Mapa corto del sistema

- `M0`:
  - conversacion tecnica con `Codex`
  - lectura de codigo y aterrizaje de idea
  - posible `input de planificacion` transitorio para `Claude`
- iniciativa:
  - `plan.md`
  - `plan_audit.md`
  - `execution.md`
  - `post_audit.md`
  - `real_validation.md` cuando aplique
  - `closeout.md`
  - `lessons_learned.md`
- weekly review:
  - briefing factual
  - review estrategica
  - actualizacion de backlog y findings
- memoria operativa viva:
  - `initiative_backlog.md`
  - `architecture_findings_register.md`
  - `initiative_architecture_backlog.md`

## 3) Routing de carga

- gobernanza general:
  - `AGENTS.md`
  - `dev/workflow.md`
  - `dev/policies/context_routing_policy.md` si existe ambiguedad de capa
    primaria
- iniciativa, plan:
  - `dev/workflow.md`
  - `dev/guarantees/plan_gate.md`
  - policy de dominio aplicable
- iniciativa, implementacion y post-auditoria:
  - `dev/workflow.md`
  - `dev/guarantees/implementation_gate.md`
  - policy de dominio aplicable
- codigo vivo:
  - `symdex_code`
- memoria estructural:
  - `codebase-memory-mcp` cuando este disponible
  - si no lo esta, fallback explicito a `symdex_code` mas lectura puntual del
    repo
- validacion observable:
  - evidencia runtime real
  - `trace on`, terminal, logs y resultados visibles
- cierre documental:
  - `dev/guarantees/docs_gate.md`
  - `dev/policies/documentation_rules.md`

## 4) Excepciones de carga

- `dev/records/` no forma parte del contexto base
- `dev/records/` solo se carga por ruta exacta cuando la iniciativa activa, el
  weekly activo o la memoria operativa lo exigen
- dosieres largos y arquitectura extensa solo se cargan cuando la policy corta
  no basta
- el `input de planificacion` es transitorio; no sustituye ningun artefacto
  canonico

## 5) Superficies nativas de producto

- `CLAUDE.md`, `.claude/` y equivalentes son superficies nativas de producto
- no son fuente de verdad normativa
- deben comportarse como adaptadores o compatibilidad local
- si difieren de `AGENTS.md` o `dev/`, prevalece la gobernanza canonica

## 6) Regla de compresion

- preferir tablas, checklists y templates breves frente a prosa larga
- si una regla necesita mas de un documento largo para aplicarse, debe
  resumirse en una policy o manifest mas corto
- weekly, backlog y plan no deben duplicar la misma semantica sustantiva

## 7) Regla de no solape

- una consulta debe tener una sola capa primaria de resolucion
- `symdex_code` no sustituye memoria estructural global
- la evidencia runtime no sustituye analisis estructural
- la memoria del chat no sustituye ninguna capa canonica
- el weekly no sustituye una iniciativa
- el backlog no sustituye un plan
- si existe duda sobre el routing correcto, prevalece
  `dev/policies/context_routing_policy.md`
