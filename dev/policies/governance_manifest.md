# Governance Manifest (Hard)

Propósito:
- minimizar carga de contexto sin perder enforcement.
- la policy de routing detallado es:
  - `dev/policies/context_routing_policy.md`

## 1) Regla de carga mínima

- Cargar por defecto solo:
  - `AGENTS.md`
  - `dev/workflow.md`
  - un gate relevante
  - una policy de dominio relevante
- No cargar más de `1 workflow + 1 gate + 1 policy de dominio + 1 policy de
  soporte` salvo ambigüedad real.

## 2) Routing de carga

- Gobernanza general:
  - `AGENTS.md`
  - `dev/workflow.md`
  - `dev/policies/context_routing_policy.md` si existe ambigüedad de capa
    primaria
- Estado operativo y continuidad:
  - runtime del orquestador
  - `phase_ticket`
  - `resume_packet`
- `M3`:
  - `dev/workflow.md`
  - `dev/guarantees/m3_delivery_gate.md`
  - `dev/policies/ai_engineering_governance.md`
- `M4` plan:
  - `dev/workflow.md`
  - `dev/guarantees/plan_gate.md`
  - policy de dominio aplicable
- `M4` implementación/post-auditoría:
  - `dev/workflow.md`
  - `dev/guarantees/implementation_gate.md`
  - policy de dominio aplicable
- Capacidades transversales del plano de acción:
  - `dev/policies/action_policy.md`
  - gate vigente del modo/fase
- Excepciones:
  - `dev/policies/exception_rules.md`
  - `exception_record.md` de la iniciativa si existe
- Código vivo:
  - `semantic_search` y luego `get_symbol` (via symdex_code)
  - evitar `rg` o lecturas amplias salvo fallback operativo real
- Memoria estructural:
  - `codebase-memory-mcp` cuando esté disponible
  - si no está disponible, fallback explícito a `symdex_code` más lectura
    puntual del repo
- Validación observable:
  - evidencia runtime real
  - `trace on`, terminal, logs y resultados visibles
- Cierre documental:
  - `dev/guarantees/docs_gate.md`
  - `dev/policies/documentation_rules.md`

## 3) Excepciones de carga

- `dev/records/` no forma parte del contexto base.
- `dev/records/` solo se carga por ruta exacta cuando la iniciativa activa lo
  exige.
- Dosieres largos y arquitectura extensa solo se cargan cuando la policy corta
  no basta.

## 4) Superficies nativas de producto

- `.claude/`, `CLAUDE.md`, `.roo/` y equivalentes son superficies nativas de
  producto.
- No son fuente de verdad normativa.
- Deben comportarse como adaptadores o compatibilidad local.
- Si difieren de `AGENTS.md` o `dev/`, prevalece la gobernanza canónica.

## 5) Regla de compresión

- Preferir tablas, checklists y templates breves frente a prosa larga.
- Si una regla necesita más de un documento largo para aplicarse, debe
  resumirse en una policy o manifest más corto.

## 6) Regla de no solape

- una consulta debe tener una sola capa primaria de resolución
- el runtime del orquestador no sustituye retrieval normativo
- `symdex_code` no sustituye memoria estructural global
- la evidencia runtime no sustituye análisis estructural
- la memoria del chat no sustituye ninguna capa canónica
- si existe duda sobre el routing correcto, prevalece
  `dev/policies/context_routing_policy.md`
