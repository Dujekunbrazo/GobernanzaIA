# Governance Manifest (Hard)

Proposito:
- minimizar carga de contexto sin perder enforcement
- fijar la estrategia de carga minima para motores directos

## 1) Regla de carga minima

- cargar por defecto solo:
  - `AGENTS.md`
  - `dev/workflow.md` cuando haga falta detalle de proceso
  - un gate relevante
  - una policy de soporte relevante
- no cargar mas de `1 workflow + 1 gate + 1 policy de soporte` salvo ambiguedad
  real

## 2) Routing de carga

- gobernanza general:
  - `AGENTS.md`
  - `dev/workflow.md`
  - `dev/policies/context_routing_policy.md` si existe ambiguedad de capa
    primaria
- `M3`:
  - `dev/workflow.md`
  - `dev/guarantees/m3_delivery_gate.md`
  - `dev/policies/ai_engineering_governance.md`
- `M4` plan:
  - `dev/workflow.md`
  - `dev/guarantees/plan_gate.md`
  - policy de dominio aplicable
- `M4` implementacion y post-auditoria:
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

## 3) Excepciones de carga

- `dev/records/` no forma parte del contexto base
- `dev/records/` solo se carga por ruta exacta cuando la iniciativa activa lo
  exige
- dosieres largos y arquitectura extensa solo se cargan cuando la policy corta
  no basta

## 4) Superficies nativas de producto

- `CLAUDE.md`, `.claude/` y equivalentes son superficies nativas de producto
- no son fuente de verdad normativa
- deben comportarse como adaptadores o compatibilidad local
- si difieren de `AGENTS.md` o `dev/`, prevalece la gobernanza canonica

## 5) Regla de compresion

- preferir tablas, checklists y templates breves frente a prosa larga
- si una regla necesita mas de un documento largo para aplicarse, debe
  resumirse en una policy o manifest mas corto

## 6) Regla de no solape

- una consulta debe tener una sola capa primaria de resolucion
- `symdex_code` no sustituye memoria estructural global
- la evidencia runtime no sustituye analisis estructural
- la memoria del chat no sustituye ninguna capa canonica
- si existe duda sobre el routing correcto, prevalece
  `dev/policies/context_routing_policy.md`
