# Prompts De Gobernanza

Esta carpeta conserva prompts de uso manual rápido para conversaciones humanas.
No es la capa primaria del canon operativo.

La fuente de verdad para `M4` vive en:

- `AGENTS.md`
- `dev/workflow.md`
- `dev/skills/`
- `dev/policies/`
- `dev/prompts/`
- `doc/governance_ping_pong_guide.md`

Estos ficheros de `doc/governance_prompts/` deben leerse como atajos manuales
alineados con ese canon, no como un workflow paralelo.

Si una capacidad ya fue migrada a `dev/skills/`, la Skill es la fuente de
verdad operativa. El prompt legacy solo queda como compatibilidad o atajo
manual.

## Bootstrap obligatorio de gobernanza

Antes de usar cualquier prompt de esta carpeta:

1. leer `AGENTS.md`
2. cargar la Skill canonica de la fase si existe
3. usar `governance_search` para gobernanza con `phase` y `document_type`
   cuando aplique
4. usar `symdex_code` para codigo vivo y `codebase-memory-mcp` para wiring,
   impacto, legacy y blast radius cuando la tarea toque codigo
5. declarar cualquier degradacion antes de recurrir a lectura bruta

Si falta una precondicion material, el estado correcto es `BLOQUEADO`.

## Regla central

- conversación `M0` -> `input de planificación` -> `plan.md`
- `plan.md` es el primer artefacto formal
- `plan_audit.md` y `post_audit.md` solo admiten `PASS` o `FAIL`
- `ping_pong` usa sidecars `_verdict.txt`, pero la gobernanza sigue viviendo
  en `AGENTS.md`, `dev/workflow.md` y `dev/policies/`
- `F5` usa `dev/skills/f5_real_validation/SKILL.md` cuando aplica y lo conduce
  motor auditor con el usuario.
- `F6` usa `dev/skills/f6_closeout/SKILL.md`.
- `F7` usa `dev/skills/f7_lessons/SKILL.md`.

## Agentes operativos por fase

Los prompts manuales no solo eligen motor; tambien fijan el agente de fase:

| Fase | Motor | Agent ID | Perfil |
| ---- | ----- | -------- | ------ |
| `F1` | motor activo | `m4.f1.claude.plan_architect` | `claude_plan_architect` |
| `F2` | motor auditor | `m4.f2.codex.plan_auditor` | `codex_plan_auditor` |
| `F2/F4 AUTOFIX` | motor auditor | `m4.audit.codex.safe_autofix` | `codex_auditor_autofix` |
| `F3` | motor activo | `m4.f3.claude.implementation_executor` | `claude_implementation_executor` |
| `F3_FINAL` | motor activo | `m4.f3_final.claude.final_validation_executor` | `claude_final_validation_executor` |
| `F4` | motor auditor | `m4.f4.codex.bug_structural_auditor` | `codex_bug_structural_auditor` |
| `F4_FINAL` | motor auditor | `m4.f4_final.codex.final_consistency_auditor` | `codex_final_consistency_auditor` |
| `F5` | motor auditor | `m4.f5.codex.real_validation_guide` | `codex_real_validation_guide` |
| `F6` | motor auditor | `m4.f6.codex.closeout_auditor` | `codex_closeout_auditor` |
| `F7` | motor auditor | `m4.f7.codex.lessons_curator` | `codex_lessons_curator` |

El tramo no cambia. La especializacion vive en el perfil, la Skill canonica y
los criterios de cierre de cada fase.

## Handoff manual obligatorio

Cuando se copia el chat entre motor activo y motor auditor, la respuesta de cierre debe
terminar con `HANDOFF_SIGUIENTE_AGENTE`. Ese bloque es solo de chat; no se
guarda como artefacto formal de iniciativa.

Contenido minimo:

- siguiente motor, fase, `agent_id` y `agent_profile`
- Skill canonica que debe cargar
- artefactos que debe leer
- write set permitido
- recordatorio de leer `AGENTS.md`
- autocheck de `governance_search`, `symdex_code` y `codebase-memory-mcp`
- uso de `governance_search` con `phase` y `document_type` cuando aplique
- instruccion de arranque exacta para el siguiente agente

Si el agente anterior no lo incluye, se debe pedir el bloque antes de continuar.

## Flujo de iniciativa M4 vigente

1. Habla con motor auditor en `M0`
2. Si motor auditor ya genero un `input de planificación M0` en Markdown y quieres
   investigarlo/reforzarlo con investigación multi-agente antes de motor activo F1,
   usa `96.3 investigacion multiagente a input M0.md`. Ese output debe ser una
   version final reemplazable del input original e incluir `AGENTE_M4_ACTIVO` y
   `HANDOFF_M0_A_F1` para levantar `m4.f1.claude.plan_architect` al pegarlo en
   motor activo.
3. Usa `97_m0_idea_codex.md` solo para una idea M0 ligera sin investigación
   adversarial.
4. Usa `98_m0_idea_codex_to_claude_plan.md` solo si ya tienes un input M0
   cerrado y quieres pasarlo a motor activo para crear `plan.md`.
5. Usa `01_f1_plan.md` como atajo manual hacia
   `dev/skills/f1_plan_creation/SKILL.md`
6. Usa `02_f2_auditoria_plan.md` como atajo manual hacia
   `dev/skills/f2_plan_audit/SKILL.md`
7. Si el plan falla, usa `03_f2_remediacion_plan.md` para remediar `plan.md`
8. Usa `04_f3_implementacion.md` como atajo manual hacia
   `dev/skills/f3_implementation_execute/SKILL.md`
9. Usa `05_f4_post_auditoria.md` como atajo manual hacia
   `dev/skills/f4_post_audit/SKILL.md`
10. Si `F5` aplica, usa `dev/skills/f5_real_validation/SKILL.md`
11. Para `F6`, usa `dev/skills/f6_closeout/SKILL.md`
12. Para `F7`, usa `dev/skills/f7_lessons/SKILL.md`

## Lógica de numeración

- `01-06`: flujo manual principal de iniciativa
- `20`: carril weekly review
- `96-98`: utilidades auxiliares de `M0`
- `99`: arranque especializado de perfiles operativos

La serie principal sigue el flujo real:

- `01` -> `F1`
- `02` -> `F2`
- `03` -> remediación del loop `F1 <-> F2`
- `04` -> `F3`
- `05` -> `F4`
- `06` -> `F6/F7`

La serie `9x` queda reservada a apoyo de `M0`:

- `96` -> mejora de `M0` con investigación externa
- `96.1` -> versión extendida legacy de investigación multi-agente
- `96.2` -> complemento legacy para convertir investigación en input M0
- `96.3` -> prompt maestro vigente: investigación multi-agente sobre un input
  M0 MD existente, con salida reforzada y arranque manual de agente
  `m4.f1.claude.plan_architect`
- `97` -> aterrizaje de idea en `M0` con motor auditor
- `98` -> handoff de `M0` a motor activo para crear `plan.md`

## Inventario actual

- `01_f1_plan.md`
- `02_f2_auditoria_plan.md`
- `03_f2_remediacion_plan.md`
- `04_f3_implementacion.md`
- `05_f4_post_auditoria.md`
- `06_f6_f7_cierre_y_lecciones.md`
- `20_weekly_mit_review.md`
- `96_m0_mejora_plan_con_investigacion.md`
- `96.1 mejora plan con investigacion v2.md`
- `96.2 mejora input plan investigado.md`
- `96.3 investigacion multiagente a input M0.md`
- `97_m0_idea_codex.md`
- `98_m0_idea_codex_to_claude_plan.md`

## Weekly review

`20_weekly_mit_review.md` sigue siendo válido para el carril weekly, pero no
abre iniciativa por sí solo ni genera `plan.md`.

## Regla operativa

- si la iniciativa ya existe, detecta la carpeta correcta antes de escribir
- si hay ambigüedad material entre varias iniciativas, el estado correcto es
  `BLOQUEADO`
- estos prompts no sustituyen los contratos de `dev/prompts/` ni las policies
  de `M4`
