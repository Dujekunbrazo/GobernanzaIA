# Policy: Weekly Briefing Capa 1

## Objetivo

Definir el `weekly_briefing.md` como el input estructurado y canonicamente
auditable de la review semanal.

## Regla principal

La review semanal no debe partir de un briefing manual libre.
Debe partir de un `weekly_briefing.md` con estructura fija y evidencia
anclable.

## Contenido minimo obligatorio

El briefing debe incluir, como minimo:

- identidad del repo y fecha de revision
- modo de revision: `BASELINE_INICIAL_MIT` o `DELTA_SEMANAL_MIT`
- perfil de capacidades reales del repo
- delta temporal o justificacion de ausencia de delta
- surfaces y behaviors relevantes
- evidencia estructural disponible
- legacy, dead code o wiring sospechoso
- estado de tests, CI, logs o runtime si existe evidencia
- riesgos y preguntas abiertas para la revision MIT

## Regla de economia de contexto

- el briefing debe ser `delta-first` cuando exista una revision semanal previa
- no debe volcar logs, traces o grafos completos
- debe enlazar o resumir evidencia, no duplicarla sin necesidad

## Relacion con otras capas

- el briefing usa el stack de contexto canonico
- no sustituye el informe final de review
- no sustituye el registro vivo de hallazgos

## Criterio de aceptabilidad

El briefing es valido cuando:

- permite producir la review semanal sin releer el repo completo
- deja claras sus fuentes de evidencia
- diferencia baseline inicial de delta semanal
