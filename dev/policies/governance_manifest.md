# Governance Manifest (Hard)

Propósito:
- minimizar carga de contexto sin perder enforcement.

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
  - `symdex_search_code` y luego `symdex_read_code`
  - evitar `rg` o lecturas amplias salvo fallback operativo real
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
