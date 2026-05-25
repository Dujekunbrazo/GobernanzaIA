# M0 a Input De Planificacion
> [!IMPORTANT]
> Bootstrap obligatorio de gobernanza antes de usar este prompt:
> leer `AGENTS.md`, cargar la Skill canonica si existe, usar `governance_search`
> para gobernanza con `phase`/`document_type` cuando aplique, usar `symdex_code`
> para codigo vivo y `codebase-memory-mcp` para wiring/impacto/legacy cuando
> toque codigo, y declarar cualquier degradacion antes de recurrir a lectura
> bruta.

A partir de toda esta conversacion, conviertela en un `input de planificacion`
transitorio y listo para pegar en motor activo.

## Salida canonica del prompt 97 - obligatoria

El output principal de este prompt **no es** un bloque en el chat: es un
archivo persistente con path canonico fijo.

Path canonico obligatorio:

```
doc/_drafts/input_m0_handoff_para_claude_<initiative_short_id>.md
```

Donde `<initiative_short_id>` es la etiqueta corta de la iniciativa en
`snake_case` o `kebab-case` minusculas, derivada del `initiative_id` candidato
declarado dentro del propio input M0. Ejemplos validos:

- `input_m0_handoff_para_claude_m4e.md`
- `input_m0_handoff_para_claude_sectores_canonicos_runtime_seed.md`
- `input_m0_handoff_para_claude_2026-05-14_matching_activable.md`

Reglas duras del path:

- el directorio es siempre `doc/_drafts/`
- el prefijo es siempre `input_m0_handoff_para_claude_`
- la extension es siempre `.md`
- el nombre no cambia entre la pasada 1 (este prompt 97) y la pasada 2
  (prompt 96.3): la pasada 2 sobreescribe el mismo archivo
- el path es referenciable por el launcher `96.3.1`, por scripts internos y
  por agentes posteriores; renombrarlo rompe el flujo

Ese bloque escrito al archivo debe contemplar el arranque manual por agentes.
Como el usuario va a copiarlo en otro chat, el input debe incluir:

- `AGENTE_M4_ACTIVO` para `m4.f1.claude.plan_architect`
- `agent_name`: `motor activo Plan Architect`
- `agent_profile`: `claude_plan_architect`
- Skill canonica: `dev/skills/f1_plan_creation/SKILL.md`
- bootstrap MCP obligatorio de `F1`
- `HANDOFF_M0_A_F1` listo para pegar junto al input
- recordatorio de que motor activo, al cerrar `F1`, debe responder con
  `HANDOFF_SIGUIENTE_AGENTE` hacia `m4.f2.codex.plan_auditor`

Reglas:
- no inventes informacion
- no rellenes huecos con suposiciones implicitas
- marca claramente que es hecho, que es supuesto y que esta abierto
- no propongas commits detallados salvo que ya hayan quedado cerrados en la conversacion
- no escribas nada fuera del bloque final y del archivo canonico
- el bloque debe ser denso, preciso y utilizable por motor activo para producir un `plan.md` fuerte a la primera
- el archivo canonico declarado arriba es obligatorio; el espejo en chat es opcional y solo confirma el path escrito

Estructura del bloque:
- AGENTE_M4_ACTIVO para motor activo F1
- HANDOFF_M0_A_F1
- Idea resumida
- Problema real
- Resultado esperado
- Evidencia conocida
- Contexto tecnico relevante
- Restricciones explicitas
- Alcance tentativo
- No-alcance tentativo
- Modulos, rutas o superficies afectadas
- Riesgos o sensibilidades detectadas
- Decisiones ya tomadas en M0
- Supuestos detectados
- Preguntas abiertas
- Informacion faltante critica
- Notas para planificacion

Escribe el bloque final como archivo en el path canonico declarado en la
seccion "Salida canonica del prompt 97 - obligatoria" arriba. Si el archivo
ya existe (porque venimos de una iteracion previa), sobreescribelo.

Despues del Write, confirma en el chat solo:

- ruta exacta del archivo escrito
- numero de lineas escritas
- `initiative_short_id` derivado y `initiative_id` candidato declarado dentro

No repitas el bloque entero en el chat. El usuario leera el archivo o lanzara
`doc/governance_prompts/96.3.1 Lanzamiento 96.3 contra imput M0` para la
pasada 2 contra ese mismo path.
