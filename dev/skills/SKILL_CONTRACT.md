# SKILL CONTRACT

## Proposito

Definir el contrato canonico minimo que toda Skill de gobernanza debe cumplir.

Una Skill no legisla ni sustituye el canon normativo. Su funcion es encapsular
operativa recurrente con activacion progresiva, write set explicito y
checklist de salida verificable.

## Campo obligatorio por Skill

Toda Skill debe declarar, en este orden logico, los siguientes campos:

- `name`
- `purpose`
- `when_to_use`
- `when_not_to_use`
- `motor`
- `agent_id`
- `agent_profile`
- `phase`
- `preconditions`
- `inputs`
- `read_set`
- `write_set`
- `hard_rules`
- `required_references`
- `optional_references`
- `exit_checklist`
- `fallback_and_escalation`

El lifecycle de la Skill se resuelve en `dev/skills/REGISTRY.md`, no duplicado
en cada `SKILL.md`. Toda Skill debe tener entrada en el registry con:

- capability
- agent_id
- agent_profile
- estado
- owner canonico
- sustitucion
- compatibilidad
- retirada

## Reglas por campo

- `name`: nombre corto, estable y unico dentro de `dev/skills/`
- `purpose`: objetivo operativo concreto de la Skill
- `when_to_use`: escenarios en los que esta Skill es el punto de entrada correcto
- `when_not_to_use`: limites explicitos para evitar scope creep
- `motor`: uno de `shared`, `claude_preferred`, `codex_preferred`
- `agent_id`: identidad canonica del agente operativo que se levanta para la
  fase cuando aplica; `n/a` para Skills meta o no ligadas a M4
- `agent_profile`: perfil operativo canonico del agente
- `phase`: fase canonica o conjunto acotado de fases donde aplica
- `preconditions`: condiciones minimas antes de usar la Skill
- `inputs`: entradas minimas esperadas
- `read_set`: artefactos canonicos que la Skill puede leer
- `write_set`: artefactos canonicos que la Skill puede escribir
- `hard_rules`: reglas duras aplicables ya derivadas del canon; no inventar normativa
- `required_references`: referencias que deben abrirse siempre que la Skill se active
- `optional_references`: referencias de apoyo que solo se cargan si hacen falta
- `exit_checklist`: condiciones verificables antes de dar por terminada la Skill
- `fallback_and_escalation`: que hacer si falta precondicion, evidencia o soporte tecnico

## Reglas duras

1. Una Skill ejecuta; no legisla.
2. La fuente de verdad normativa sigue viviendo en `AGENTS.md`,
   `dev/workflow.md`, `dev/guarantees/` y `dev/policies/`.
3. Si existe una Skill para una capacidad migrada, la Skill es la fuente de
   verdad operativa de esa capacidad.
4. Los prompts legacy solo pueden sobrevivir como compatibilidad de solo
   lectura y deben converger con la Skill.
5. Una Skill no puede tener write set mas amplio que el necesario.
6. La activacion debe ser progresiva: cargar solo la Skill y sus referencias
   obligatorias; abrir referencias opcionales solo si hacen falta.
7. Una Skill no puede tocar codigo de producto ni runtime salvo que el write
   set de la propia capacidad lo autorice de forma explicita.
8. Si una Skill deja dualidad canonica, paths paralelos o cleanup estructural
   dentro de su propio scope, el estado correcto es `FAIL` o `BLOQUEADO`.
9. Una Skill `CANONICA` no puede convivir con prompt legacy como fuente
   operativa alternativa; el prompt solo puede quedar como compatibilidad de
   solo lectura y debe declarar subordinacion.
10. Una Skill sin entrada completa en `REGISTRY.md` no puede considerarse
    canonica.
11. Toda Skill de fase `F1-F7` debe cerrar la respuesta de chat con
    `HANDOFF_SIGUIENTE_AGENTE` cuando el usuario vaya a copiar ese chat a otro
    motor. Ese bloque es chat-only y debe recordar bootstrap, MCP autocheck,
    Skill canonica, artefactos a leer/escribir, write set, siguiente
    `agent_id` y siguiente perfil.

## Estructura recomendada

Cada Skill vive en:

- `dev/skills/<skill_name>/SKILL.md`

Y puede apoyarse en:

- `dev/skills/<skill_name>/references/`
- `dev/skills/<skill_name>/examples/`

No se permiten `scripts/` ejecutables dentro de `dev/skills/`. Los scripts
canonicos viven en `scripts/dev/` o `scripts/ops/`.
