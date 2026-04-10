# Policy: Initiative Backlogs

## Objetivo

Definir la memoria operativa viva de ideas, candidatas y remanentes entre
conversaciones, weeklies e iniciativas cerradas.

## Artefactos canonicos

- `initiative_backlog.md`
- `initiative_architecture_backlog.md`
- `candidate_initiatives.md`

## Reglas

- `initiative_backlog.md` recoge ideas vivas y candidatas accionables
- cada entrada debe declarar origen: `conversation` | `weekly` | `closeout`
- `initiative_architecture_backlog.md` recoge remanentes y follow-ups de
  iniciativas cerradas
- `candidate_initiatives.md` agrupa hallazgos semanales, pero no sustituye el
  backlog vivo
- ninguna entrada de backlog puede contener un `plan.md` encubierto
- al promover una entrada a iniciativa debe quedar enlazada con el
  `initiative_id` resultante
- todo `closeout.md` debe declarar una decision explicita sobre backlog:
  - `SIN_CAMBIOS`
  - `ACTUALIZAR_INITIATIVE_BACKLOG`
  - `ACTUALIZAR_INITIATIVE_ARCHITECTURE_BACKLOG`
  - `ACTUALIZAR_FINDINGS_REGISTER`
- si la decision es `SIN_CAMBIOS`, debe justificarse explicitamente que no hay
  idea viva, remanente ni hallazgo persistente que conservar
- si la decision no es `SIN_CAMBIOS`, el artefacto correspondiente debe quedar
  creado o actualizado en el mismo cierre

## Criterio de aceptabilidad

La memoria viva es correcta cuando:

- las ideas no se pierden entre sesiones
- los hallazgos semanales no se duplican al pasar a iniciativa
- los remanentes de cierre no quedan enterrados en `lessons_learned.md`
