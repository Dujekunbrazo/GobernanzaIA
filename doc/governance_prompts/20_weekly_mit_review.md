# WEEKLY MIT + KRUG REVIEW

Usar como review semanal en dos capas:
- `Claude Sonnet` para generar o actualizar `weekly_briefing.md`
- `Claude Opus` para producir la revision estrategica final

## Mision

Producir una revision estrategica del repo que:
- mida salud arquitectonica con MIT
- mida claridad y carga cognitiva con Krug
- compare contra la review previa cuando exista
- actualice registros persistentes
- proponga candidatos de iniciativa sin generar `plan.md`

## Reglas no negociables

- toda afirmacion material debe anclarse al briefing o a evidencia canonicamente recuperada
- si falta soporte, escribir `NO EVIDENCIA EN BRIEFING`
- weekly review no sustituye `M0` ni abre una iniciativa por si sola
- weekly review no genera `plan.md`
- `candidate_initiatives.md` y `initiative_backlog.md` solo describen candidatos y entradas vivas, no planes operativos

## Artefactos a actualizar

- `weekly_briefing.md`
- `weekly_review.md`
- `weekly_review_delta.md`
- `architecture_findings_register.md`
- `candidate_initiatives.md`
- `initiative_backlog.md`

## Modo de trabajo

- si el briefing indica `BASELINE_WEEKLY`, trata la review como baseline profunda
- si indica `DELTA_WEEKLY`, compara contra la ultima review valida
- en baseline, no inventes delta previo
- en delta, no reanalices el repo entero si el briefing ya acota cambios

## Estructura minima de `weekly_review.md`

1. Diagnostico ejecutivo
2. Scorecard MIT
3. Scorecard Krug
4. Mapa Behavior -> Concepts -> Synchronizations
5. Riesgo por capas
6. Hallazgos priorizados
7. Candidate initiatives
8. Preguntas abiertas

## Regla de findings

- cada hallazgo debe quedar clasificado como `MIT-FIRST`, `KRUG-FIRST` o `MIXTO`
- cada hallazgo persistente debe actualizar el findings register, no quedarse solo en la weekly

## Regla de candidatas

- agrupa por causa raiz, concept, synchronization o write set dominante
- no abras iniciativa por cada hallazgo trivial
- si propones una candidata, explica por que merece iniciativa propia
