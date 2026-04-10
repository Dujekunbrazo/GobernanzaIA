# Tooling Quality Policy (Hard)

Proposito:
- fijar que significa usar bien el stack MCP canonico en el repo
- evitar que la gobernanza diga una cosa y el uso real del tooling haga otra

## 1) Regla de calidad

El uso de tooling solo se considera correcto cuando:

- la pregunta se clasifica bien antes de elegir herramienta
- se usa la subtool minima que puede responder con evidencia suficiente
- la degradacion queda declarada cuando existe
- no se presenta un fallback como si fuera capacidad plena

## 2) Reglas por capa

Gobernanza:

- `governance_search` con query breve y filtros antes de leer documentos
- no cargar corpus amplio salvo ambiguedad material

Codigo vivo:

- `search_symbols` -> `get_symbol` como camino primario
- `get_file_outline` -> `get_symbols` para anatomia de archivo
- `semantic_search` solo si existe backend validado
- `search_text(path_pattern=...)` no es happy path por defecto

Estructura:

- `list_projects` antes de un analisis serio
- `get_graph_schema` antes de Cypher si hace falta
- `search_graph` para discovery
- `trace_path` para relaciones reales
- `query_graph` solo para ultima milla y con query acotada

## 3) Antipatrones prohibidos

- arrancar discovery estructural con `query_graph`
- usar BM25 como si demostrara estructura real por si solo
- tratar `semantic_search` expuesto como si implicara semantica validada
- tratar `search_text(path_pattern=...)` como estable sin evidencia observada
- cancelar un lote completo de validaciones por un `FAIL` esperado de un checker

## 4) Declaracion minima en respuestas tecnicas

- herramienta usada
- responsabilidad cubierta
- fuente canonica localizada
- proyecto estructural usado, si aplica
- estado de capacidad degradada, si aplica
- limitacion metodologica observada, si aplica

## 5) Guardarrailes mecanicos

Los siguientes checks forman parte del anti-regresion del repo:

- `scripts/dev/check_direct_governance_contract.py`
- `scripts/dev/check_tooling_governance_guardrails.py`
- `scripts/dev/check_structural_tooling_ready.py`

## 6) Referencias

- `dev/policies/context_routing_policy.md`
- `dev/policies/context_stack_policy.md`
- `dev/policies/symdex_semantic_policy.md`
- `dev/policies/structural_analysis_execution_policy.md`
- `dev/policies/repo_capabilities_policy.md`
