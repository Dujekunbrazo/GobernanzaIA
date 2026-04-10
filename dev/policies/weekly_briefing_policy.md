# Policy: Weekly Briefing Capa 1

## Objetivo

Definir el `weekly_briefing.md` como el input factual estructurado y
canonicamente auditable de la review semanal.

## Regla principal

La review semanal no debe partir de un briefing manual libre.
Debe partir de un `weekly_briefing.md` con estructura fija, evidencia anclable
y delta resumido cuando exista.

## Contenido minimo obligatorio

El briefing debe incluir, como minimo:

- identidad del repo y fecha de revision
- modo de revision: `BASELINE_WEEKLY` o `DELTA_WEEKLY`
- perfil de capacidades reales del repo
- delta temporal o justificacion de ausencia de delta
- surfaces y behaviors relevantes
- evidencia estructural disponible
- legacy, dead code o wiring sospechoso
- estado de tests, CI, logs o runtime si existe evidencia
- riesgos y preguntas abiertas para la revision MIT/Krug

## Regla de economia de contexto

- el briefing debe ser `delta-first` cuando exista una revision semanal previa
- no debe volcar logs, traces o grafos completos
- debe enlazar o resumir evidencia, no duplicarla sin necesidad
- no debe contener plan operativo de iniciativa

## Relacion con otras capas

- el briefing usa el stack de contexto canonico
- no sustituye el informe final de review
- no sustituye el registro vivo de hallazgos
- sirve a `Claude Sonnet` como capa factual previa a `Claude Opus`

## Regla especifica de baseline

Si el modo es `BASELINE_WEEKLY`:

- el briefing debe cubrir el repo completo, no solo un delta
- debe declarar de forma explicita que no existe comparativa previa valida
- debe dejar preparadas las semillas de findings y candidatas iniciales

## Criterio de aceptabilidad

El briefing es valido cuando:

- permite producir la review semanal sin releer el repo completo
- deja claras sus fuentes de evidencia
- diferencia baseline inicial de delta semanal
- no arrastra narrativa innecesaria
